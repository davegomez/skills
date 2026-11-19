"""Layer 1 runner: arms, isolation dry run, one run, and the ledgered batch.
  python3 -I runner.py freeze                                   freeze the old and new arms (once)
  python3 -I runner.py isolation [--case ID] [--live]           list what the builder can discover (--live is paid)
  python3 -I runner.py run <stage> <case> <arm> <block> [variant]   one run, then grade (ledgered)
  python3 -I runner.py batch <stage> --approved-cap <usd>       every planned unit, pairs reserved before they start
  python3 -I runner.py selftest                                 offline policy checks
"""
import json, os, random, re, secrets, shutil, signal, subprocess, sys, tarfile, threading, time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (CASES, EVAL, OUT, REPO, SCRATCH, SKILL_SRC, Redactor, cfg, case_dirs, changed_files, die, find_case, git,
                    is_review, load_case, lock, make_work, manifest, patch_of, sha256_bytes, snapshot, tree_files, tree_sha)
import grade

ARMS = ("old", "new", "none")
WORK, TMP, PLUGIN, BIN, LOG, ZDOT = (SCRATCH / n for n in ("w/work", "t", "plugin", "bin", "log", "z"))
REPO_GIT = WORK.parent / ".git"  # the repository of a case with an empty fixture (make_work)
SKILL_DIR = PLUGIN / "skills" / "ios-architecture"
SKILL_NAME = "skills:ios-architecture"  # plugin "skills", skill "ios-architecture"
ARMS_DIR = OUT / "arms"
SCRIPTS = re.compile(r"scripts/(route|check|decide|scaffold|new-feature|migration-sort)\b")
BUILD_TOOLS = re.compile(r"\b(xcodebuild|swift (?:build|test)|xcrun simctl)\b")
# Unsandboxed commands the host allows: 1 build or simulator tool, no shell syntax that could chain a second command.
UNSANDBOXED = re.compile(r"(?:xcodebuild|xcrun (?:simctl|xcresulttool|swift)|swift (?:build|test|package))(?:\s+[^;&|`$<>(){}\\\n\r]*)?")
PROVIDER_ERROR = re.compile(r"API Error|authentication|unauthori[sz]ed|invalid api key|credit balance|billing|overloaded|rate limit|not logged in|please run /login", re.I)


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def both(p: Path) -> list[str]:
    """A path in both its given and its physical form (/tmp is /private/tmp on macOS)."""
    return sorted({str(p), os.path.realpath(p)})


# ---------- arms ----------

def freeze():
    if (ARMS_DIR / "MANIFEST.json").exists(): die(f"arms are frozen already: {ARMS_DIR}; delete it to freeze again")
    c = cfg()
    tmp = ARMS_DIR.with_name("arms.tmp")
    shutil.rmtree(tmp, ignore_errors=True)
    (tmp / "old").mkdir(parents=True)
    archive = subprocess.run(["git", "-C", str(REPO), "archive", c["old_commit"], "skills/ios-architecture"], capture_output=True, check=True).stdout
    subprocess.run(["tar", "-x", "-C", str(tmp / "old"), "--strip-components", "1"], input=archive, check=True)
    shutil.copytree(SKILL_SRC, tmp / "new" / "ios-architecture", ignore=shutil.ignore_patterns(".DS_Store"))
    status = subprocess.run(["git", "-C", str(REPO), "status", "--porcelain", "--", "skills/ios-architecture"], capture_output=True, text=True).stdout
    head = subprocess.run(["git", "-C", str(REPO), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    man = {"frozen": now(),
           "old": {"source": f"git archive {c['old_commit']} skills/ios-architecture", "files": manifest(tmp / "old" / "ios-architecture")},
           "new": {"source": f"working tree at {head}", "git_status": status.splitlines(), "files": manifest(tmp / "new" / "ios-architecture")}}
    (tmp / "MANIFEST.json").write_text(json.dumps(man, indent=1, sort_keys=True))
    tmp.rename(ARMS_DIR)
    print(f"frozen: old {len(man['old']['files'])} files, new {len(man['new']['files'])} files -> {ARMS_DIR}")


def arm_manifest(arm: str) -> dict:
    p = ARMS_DIR / "MANIFEST.json"
    if not p.exists(): die("arms are not frozen; run: python3 -I runner.py freeze")
    return json.loads(p.read_text())[arm]["files"]


def install(arm: str) -> str | None:
    """Install the arm's skill as plugin 'skills' at the fixed neutral path. Returns the manifest sha, None for 'none'."""
    shutil.rmtree(PLUGIN, ignore_errors=True)
    if arm == "none": return None
    want = arm_manifest(arm)
    if manifest(ARMS_DIR / arm / "ios-architecture") != want: die(f"frozen arm {arm} changed since freeze")
    shutil.copytree(ARMS_DIR / arm / "ios-architecture", SKILL_DIR)
    (PLUGIN / ".claude-plugin").mkdir()
    (PLUGIN / ".claude-plugin" / "plugin.json").write_text('{"name": "skills"}\n')
    if manifest(SKILL_DIR) != want: die("installed skill differs from the frozen arm")
    return sha256_bytes(json.dumps(want, sort_keys=True).encode())


# ---------- builder session ----------

def write_curl_wrapper(max_calls: int, host: str):
    """PATH shim: logs URL (no query), HTTP status, exit, and time of each curl call; never headers or bodies.
    It refuses a Jev call past max_calls, which bounds Jev spend per run."""
    BIN.mkdir(parents=True, exist_ok=True)
    real = os.environ.get("IOS_EVAL_REAL_CURL", "/usr/bin/curl")
    (BIN / "curl").write_text(f"""#!/bin/sh
log='{LOG}/curl.log'; real='{real}'; max={max_calls}
url=; for a do case $a in http://*|https://*) url=${{a%%\\?*}};; esac; done
host=$(printf '%s' "$url" | sed -n 's#^[a-z]*://\\([^/:]*\\).*#\\1#p')
t0=$(date -u +%Y-%m-%dT%H:%M:%SZ); s0=$(date +%s)
if [ "$host" = '{host}' ] && [ "$(grep -c ' host={host} ' "$log" 2>/dev/null)" -ge "$max" ]; then
  printf 'time=%s host=%s url=%s status=refused exit=7 seconds=0\\n' "$t0" "$host" "$url" >>"$log"
  echo 'curl: call cap of this run reached' >&2; exit 7
fi
out=$(mktemp "${{TMPDIR:-/tmp}}/curl.XXXXXX") || exit 7
"$real" "$@" >"$out"; rc=$?
st=unknown; [ "$(wc -c <"$out" | tr -d ' ')" -le 3 ] && grep -qE '^[0-9]{{3}}$' "$out" && st=$(cat "$out")
printf 'time=%s host=%s url=%s status=%s exit=%s seconds=%s\\n' "$t0" "$host" "$url" "$st" "$rc" "$(( $(date +%s) - s0 ))" >>"$log"
cat "$out"; rm -f "$out"; exit $rc
""")
    (BIN / "curl").chmod(0o755)


def sandbox_settings(arm: str) -> dict:
    """Reads are open except denyRead. The run's folders (SCRATCH) sit under no denied root, so no allowRead carve-out is needed:
    a denied /tmp blocks every path spelled through that symlink, allowRead or not. Writes: cwd (by default), git, tmp, and the curl log."""
    c = cfg()
    deny = sorted({p for d in (Path.home(), Path("/tmp"), Path("/Volumes"), REPO, OUT) for p in both(d)})
    return {"sandbox": {"enabled": True, "autoAllowBashIfSandboxed": True, "allowUnsandboxedCommands": True,
                        "network": {"allowLocalBinding": True, "allowedDomains": [c["jev"]["host"]] if arm == "new" else []},
                        "filesystem": {"denyRead": deny, "allowWrite": both(LOG) + both(REPO_GIT) + both(TMP)}}}


def inside(path, *roots) -> bool:
    p = Path(path) if os.path.isabs(str(path)) else WORK / str(path)
    p = Path(os.path.realpath(p))
    return any(p.is_relative_to(os.path.realpath(r)) for r in roots)


def unsandboxed_ok(cmd: str) -> bool:
    if "\n" in cmd or "\r" in cmd or not UNSANDBOXED.fullmatch(cmd.strip()): return False
    for tok in cmd.split():
        v = tok.split("=", 1)[-1].strip("'\"")
        if ".." in v or v.startswith("~"): return False
        if v.startswith("/") and not inside(v, WORK, TMP) and not v.startswith(("/Applications/Xcode", "/dev/null")): return False
    return True


DENY_NET = "Network access is not available in this environment."
DENY_UNSANDBOXED = "Only 1 xcodebuild, swift, or xcrun command on this project can run outside the sandbox."
DENY_READ = "Files outside the working directory are not available here."
DENY_WRITE = "Only files in the working directory can change."


def policy(tool: str, inp: dict, arm: str) -> tuple[bool, str]:
    if tool == "SandboxNetworkAccess":
        host = str(inp.get("host", "")).rsplit(":", 1)[0].strip("[]")
        return arm == "new" and host == cfg()["jev"]["host"], DENY_NET
    if tool == "Bash":
        if not inp.get("dangerouslyDisableSandbox"): return True, ""
        return unsandboxed_ok(inp.get("command", "")), DENY_UNSANDBOXED
    if tool in ("Read", "Glob", "Grep"):
        path = inp.get("file_path") or inp.get("path") or str(WORK)
        return inside(path, WORK, TMP, PLUGIN), DENY_READ
    if tool in ("Edit", "Write", "NotebookEdit", "MultiEdit"):
        path = inp.get("file_path") or inp.get("notebook_path") or ""
        return bool(path) and inside(path, WORK, TMP), DENY_WRITE
    if tool in ("Skill", "Agent", "Task", "TodoWrite"): return True, ""
    return False, f"{tool} is not available in this environment."


def claude_bin() -> str:
    return os.environ.get("IOS_EVAL_CLAUDE") or shutil.which("claude") or die("claude not found")


def build_cmd(arm: str, budget: float, model: str, effort: str) -> list[str]:
    c = cfg()
    cmd = [claude_bin(), "-p", "--restricted", "--strict-mcp-config", "--setting-sources", "project", "--no-session-persistence",
           "--model", model, "--effort", effort, "--tools", c["builder"]["tools"], "--allowedTools", "Skill", "Agent",
           "--permission-prompt-tool", "stdio", "--settings", json.dumps(sandbox_settings(arm)), "--max-budget-usd", f"{budget:.2f}",
           "--input-format", "stream-json", "--replay-user-messages", "--output-format", "stream-json", "--verbose"]
    return cmd + (["--plugin-dir", str(PLUGIN)] if arm != "none" else [])


def builder_env(arm: str, key: str | None) -> dict:
    """A minimal environment: no harness variables, no user shell startup files, a neutral git config."""
    b = cfg()["builder"]
    env = {k: os.environ[k] for k in ("HOME", "USER", "LOGNAME", "LANG", "TERM") if k in os.environ}
    env |= {"PATH": f"{BIN}:/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin", "SHELL": "/bin/zsh", "ZDOTDIR": str(ZDOT),
            "CLAUDE_CODE_TMPDIR": str(TMP), "GIT_CONFIG_GLOBAL": str(SCRATCH / "gitconfig"), "GIT_CONFIG_NOSYSTEM": "1",
            "TYPESAFE_KEYCHAIN_SERVICE": "ios-eval-no-keychain",
            "ANTHROPIC_DEFAULT_HAIKU_MODEL": b["fallback_small"], "ANTHROPIC_DEFAULT_SONNET_MODEL": b["fallback_medium"],
            "ANTHROPIC_DEFAULT_OPUS_MODEL": b["model"]}
    if arm == "new": env["TYPESAFE_API_KEY"] = key
    return env


def jev_key() -> str:
    key = os.environ.get("TYPESAFE_API_KEY") or subprocess.run(
        ["security", "find-generic-password", "-s", "typesafe-api-key", "-w"], capture_output=True, text=True).stdout.strip()
    if not key: die("no TypeSafe key: set TYPESAFE_API_KEY or the Keychain item typesafe-api-key")
    return key


def reset_scratch():
    for d in (WORK.parent, TMP, PLUGIN, BIN, LOG, ZDOT):
        shutil.rmtree(d, ignore_errors=True)
    for d in (TMP, LOG, ZDOT): d.mkdir(parents=True)
    (SCRATCH / "gitconfig").write_text("[user]\n\tname = Developer\n\temail = developer@example.invalid\n[commit]\n\tgpgsign = false\n")


def kill_by_path(*paths: Path):
    out = subprocess.run(["lsof", "-d", "cwd", "-F", "pn"], capture_output=True, text=True).stdout
    pid, roots = None, [os.path.realpath(p) for p in paths]
    for line in out.splitlines():
        if line.startswith("p"): pid = int(line[1:])
        elif line.startswith("n") and pid and pid != os.getpid() and any(line[1:].startswith(r) for r in roots):
            try: os.kill(pid, signal.SIGKILL)
            except ProcessLookupError: pass


def execute(cmd, env, text, arm, stream: Path, err: Path, wall_s: float, redact: Redactor) -> dict:
    """Run claude -p, answer each permission prompt with policy(), write the redacted stream and per-line times."""
    times, state = [], {"timed_out": False}
    t0 = time.monotonic()
    with open(stream, "w") as out, open(err, "w") as er:
        proc = subprocess.Popen(cmd, cwd=WORK, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=er, text=True,
                                env=env, start_new_session=True)

        def stop(timeout=False):
            state["timed_out"] |= timeout
            for sig in (signal.SIGTERM, signal.SIGKILL):
                try: os.killpg(proc.pid, sig); time.sleep(3)
                except ProcessLookupError: return

        def send(obj):
            try: proc.stdin.write(json.dumps(obj) + "\n"); proc.stdin.flush()
            except (BrokenPipeError, ValueError, OSError): pass

        def emit(line):
            out.write(redact(line.rstrip("\n")) + "\n"); out.flush(); times.append(round(time.monotonic() - t0, 3))

        watchdog = threading.Timer(wall_s, stop, kwargs={"timeout": True}); watchdog.start()
        send({"type": "user", "message": {"role": "user", "content": text}})
        for line in proc.stdout:
            emit(line)
            try: e = json.loads(line)
            except ValueError: continue
            if e.get("type") == "control_request" and e.get("request", {}).get("subtype") == "can_use_tool":
                r = e["request"]
                ok, why = policy(r.get("tool_name"), r.get("input") or {}, arm)
                emit(json.dumps({"type": "host_decision", "tool": r.get("tool_name"), "allow": ok, "input": r.get("input")}))
                resp = {"behavior": "allow", "updatedInput": r.get("input")} if ok else {"behavior": "deny", "message": why}
                send({"type": "control_response", "response": {"subtype": "success", "request_id": e.get("request_id"), "response": resp}})
            elif e.get("type") == "result":
                try: proc.stdin.close()
                except OSError: pass
                threading.Timer(10, stop).start()
        proc.wait()
        watchdog.cancel()
    err.write_text(redact(err.read_text()))
    stream.with_suffix(".times").write_text("\n".join(map(str, times)) + "\n")
    return {"timed_out": state["timed_out"], "wall_s": round(time.monotonic() - t0, 1)}


# ---------- parsing ----------

def _text(content) -> str:
    if isinstance(content, str): return content
    if isinstance(content, list): return "\n".join(c.get("text", "") for c in content if isinstance(c, dict))
    return ""


def parse_stream(stream: Path) -> dict:
    lines = stream.read_text().splitlines()
    tp = stream.with_suffix(".times")
    times = [float(x) for x in tp.read_text().split()] if tp.exists() else [0.0] * len(lines)
    init, results, host, received, uses, res_at, res_text = {}, [], [], None, {}, {}, {}
    for line, t in zip(lines, times):
        try: e = json.loads(line)
        except ValueError: continue
        k = e.get("type")
        if k == "system" and e.get("subtype") == "init":
            init = {x: e.get(x) for x in ("model", "tools", "mcp_servers", "plugins", "skills", "permissionMode", "cwd", "claude_code_version")}
        elif k == "assistant":
            for c in e.get("message", {}).get("content", []):
                if c.get("type") == "tool_use": uses[c["id"]] = (c.get("name"), c.get("input") or {}, t)
        elif k == "user":
            content = e.get("message", {}).get("content")
            if isinstance(content, str): received = received or content
            for c in content if isinstance(content, list) else []:
                if isinstance(c, dict) and c.get("type") == "tool_result":
                    res_at[c.get("tool_use_id")] = t; res_text[c.get("tool_use_id")] = _text(c.get("content"))
        elif k == "host_decision": host.append(e)
        elif k == "result": results.append(e)
    result = results[-1] if results else {}
    by, scripts, agents, refs = {}, {}, {}, set()
    build_s = decide_s = 0.0
    for uid, (name, inp, t) in uses.items():
        by[name] = by.get(name, 0) + 1
        dt = max(0.0, res_at.get(uid, t) - t)
        if name == "Bash":
            cmd = str(inp.get("command", ""))
            for s in SCRIPTS.findall(cmd): scripts[s] = scripts.get(s, 0) + 1
            if BUILD_TOOLS.search(cmd): build_s += dt
            elif SCRIPTS.search(cmd): decide_s += dt
        elif name in ("Agent", "Task"):
            m = inp.get("model") or "inherit"; agents[m] = agents.get(m, 0) + 1
        elif name == "Read" and "/references/" in str(inp.get("file_path", "")):
            refs.add(Path(inp["file_path"]).stem)
    decides, pending, decided_models = [], {"fallback": 0, "orchestrator": 0}, set()
    for txt in res_text.values():
        for ln in txt.splitlines():
            ln = ln.strip()
            m = re.match(r"decided: .*: jev model (\S+)$", ln)
            if m: decided_models.add(m.group(1))
            if ln.startswith("{") and '"decision"' in ln:
                try: d = json.loads(ln)
                except ValueError: continue
                if isinstance(d, dict) and "source" in d:
                    decides.append({k: d.get(k) for k in ("decision", "source", "model", "escalate", "fallback_tier", "reason")})
            m = re.search(r"pending: .*escalate=(fallback|orchestrator)", ln)
            if m: pending[m.group(1)] += 1
    usage = result.get("usage") or {}
    return {"init": init, "received_prompt_sha256": sha256_bytes(received.encode()) if received else None,
            "result_subtype": result.get("subtype"), "is_error": result.get("is_error"), "result_events": len(results),
            "cost_usd": result.get("total_cost_usd"), "cost_label": "claude total_cost_usd (CLI estimate)",
            "usage": {k: usage.get(k) for k in ("input_tokens", "output_tokens", "cache_read_input_tokens", "cache_creation_input_tokens")},
            "reasoning_tokens": (usage.get("output_tokens_details") or {}).get("reasoning_tokens"),
            "model_usage": result.get("modelUsage"), "num_turns": result.get("num_turns"),
            "duration_ms": result.get("duration_ms"), "duration_api_ms": result.get("duration_api_ms"),
            "tool_calls": len(uses), "tool_calls_by_name": by, "script_runs": scripts, "subagents_by_model": agents,
            "references_read": sorted(refs), "build_test_s": round(build_s, 1), "script_wait_s": round(decide_s, 1),
            "decide_results": decides, "decide_by_source": {s: sum(d["source"] == s for d in decides) for s in {d["source"] for d in decides}},
            "pending_lines": pending, "no_egress_skips": sum(d.get("reason") == "code_may_not_leave_machine" for d in decides),
            "jev_models_observed": sorted({d["model"] for d in decides if d["source"] == "jev" and d.get("model")} | decided_models),
            "host_prompts": len(host), "host_denials": [h.get("input") for h in host if not h.get("allow")],
            "permission_denials": len(result.get("permission_denials") or []),
            "final_text": max((r.get("result") or "" for r in results), key=len, default="")}


def parse_curl_log(p: Path, host: str) -> dict:
    lines = p.read_text().splitlines() if p.exists() else []
    rows = [dict(kv.split("=", 1) for kv in ln.split() if "=" in kv) for ln in lines]
    jev = [r for r in rows if r.get("host") == host]
    return {"curl_calls": len(rows), "jev_calls": sum(r.get("status") != "refused" for r in jev),
            "jev_refused": sum(r.get("status") == "refused" for r in jev),
            "jev_status": {s: sum(r.get("status") == s for r in jev) for s in {r.get("status") for r in jev}},
            "other_hosts": sorted({r.get("host", "") for r in rows} - {host})}


# ---------- one run ----------

def rid_of(unit: dict, arm: str, attempt: int) -> str:
    return f"{unit['case']}-{unit['block']}-{arm}" + (f"-r{attempt}" if attempt > 1 else "")


def run_one(stage: str, unit: dict, arm: str, attempt: int = 1, key: str | None = None) -> Path:
    c = cfg()
    rid = rid_of(unit, arm, attempt)
    rdir = OUT / stage / "runs" / rid
    if (rdir / "meta.json").exists(): return rdir
    shutil.rmtree(rdir, ignore_errors=True); rdir.mkdir(parents=True)
    case = find_case(unit["case"])
    reset_scratch()
    make_work(case, WORK, unit.get("variant"))
    skill_sha = install(arm)
    write_curl_wrapper(c["jev"]["max_calls_per_run"], c["jev"]["host"])
    text = (case["dir"] / "task.md").read_text()
    before, start_tree = tree_sha(WORK), snapshot(WORK) if is_review(case) else None
    redact = Redactor(key)
    start, b = now(), c["builder"]
    run = execute(build_cmd(arm, c["caps"]["run_usd"], b["model"], b["effort"]), builder_env(arm, key), text, arm,
                  rdir / "stream.jsonl", rdir / "stderr.txt", c["caps"]["wall_s"], redact)
    stop = now()
    kill_by_path(WORK, TMP)
    after = tree_sha(WORK)
    meta = parse_stream(rdir / "stream.jsonl")
    if (LOG / "curl.log").exists(): (rdir / "curl.log").write_text(redact((LOG / "curl.log").read_text()))
    meta |= parse_curl_log(rdir / "curl.log", c["jev"]["host"])
    key_in_result = 0
    for p in (tree_files(WORK, skip=()) if key else []):  # a key the builder wrote into a file never reaches the archive
        data = p.read_bytes()
        if not p.is_symlink() and key.encode() in data:
            key_in_result += data.count(key.encode()); p.write_bytes(data.replace(key.encode(), b"[REDACTED]"))
    with tarfile.open(rdir / "result.tgz", "w:gz") as tar:  # the result as left, before the harness touches its index
        tar.add(WORK, arcname="work", filter=lambda ti: None if any(p in ti.name.split("/") for p in ("DerivedData", ".build")) or ti.name.endswith(".xcresult") else ti)
    files = changed_files(WORK)
    if start_tree:  # a review case: the reviewer's own files, without the diff under review
        (rdir / "review.diff").write_text(redact(git(WORK, "diff", "--binary", "--relative", start_tree, snapshot(WORK)).stdout))
    (rdir / "patch.diff").write_text(redact(patch_of(WORK)))
    (rdir / "final.txt").write_text(redact(meta.pop("final_text")))
    skill_after = sha256_bytes(json.dumps(manifest(SKILL_DIR), sort_keys=True).encode()) if arm != "none" else None
    meta |= {"id": rid, "stage": stage, "case": unit["case"], "block": unit["block"], "variant": unit.get("variant"), "arm": arm,
             "attempt": attempt, "start": start, "stop": stop, **run,
             "pins": {"model": b["model"], "effort": b["effort"], "fallback_small": b["fallback_small"], "fallback_medium": b["fallback_medium"],
                      "claude_version": c["claude_version"], "run_usd_cap": c["caps"]["run_usd"], "wall_s_cap": c["caps"]["wall_s"]},
             "hashes": {"task": sha256_bytes(text.encode()), "case": tree_sha(case["dir"]), "skill": skill_sha, "skill_after": skill_after,
                        "config": sha256_bytes(Path(os.environ.get("IOS_EVAL_CONFIG", EVAL / "config.json")).read_bytes()),
                        "harness": sha256_bytes(b"".join(p.read_bytes() for p in sorted(EVAL.glob("*.py"))))},
             "tree_changed": before != after, "files_changed": files,
             "shared_tmp_refs": (rdir / "stream.jsonl").read_text().count(f"/tmp/claude-{os.getuid()}/"),
             "redactions": redact.hits, "key_in_result": key_in_result}
    meta["prompt_delivered"] = meta["received_prompt_sha256"] == meta["hashes"]["task"]
    meta["budget_stop"] = meta["result_subtype"] == "error_max_budget_usd"
    meta["stop_reason"] = "timeout" if run["timed_out"] else "budget" if meta["budget_stop"] else (meta["result_subtype"] or "no_result")
    (rdir / "meta.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False))
    return rdir


def invalid_reasons(meta: dict, g: dict) -> list[str]:
    """Infrastructure failures that invalidate a block. A timeout, a budget stop, or a bad delivery is an attempted run."""
    c, why = cfg(), []
    init = meta.get("init") or {}
    if not meta.get("result_events") and not meta.get("timed_out"): why.append("no_result_event")
    if meta.get("is_error") and not meta.get("budget_stop") and PROVIDER_ERROR.search(Path(OUT / meta["stage"] / "runs" / meta["id"] / "final.txt").read_text()):
        why.append("provider_error")
    if init and not meta.get("prompt_delivered"): why.append("prompt_not_delivered")
    if init and init.get("model") != c["builder"]["model"]: why.append(f"model_mismatch:{init.get('model')}")
    if init and init.get("mcp_servers"): why.append("mcp_servers_loaded")
    has = SKILL_NAME in (init.get("skills") or [])
    if init and has != (meta["arm"] != "none"): why.append("skill_missing" if meta["arm"] != "none" else "skill_present_in_none")
    if meta["hashes"]["skill"] != meta["hashes"]["skill_after"]: why.append("skill_modified")
    if meta.get("shared_tmp_refs"): why.append("shared_tmp")
    if g.get("error"): why.append("grade_infrastructure")
    if drift(meta): why.append("jev_model_drift")
    return why


def drift(meta: dict) -> bool:
    pinned = cfg()["jev"]["model"]
    return meta["arm"] == "new" and any(m != pinned for m in meta.get("jev_models_observed", []))


# ---------- ledger and batch ----------

def ledger_path(stage: str) -> Path:
    return OUT / stage / "ledger.jsonl"


def ledger(stage: str) -> list[dict]:
    p = ledger_path(stage)
    return [json.loads(x) for x in p.read_text().splitlines()] if p.exists() else []


def log(stage: str, **entry):
    ledger_path(stage).parent.mkdir(parents=True, exist_ok=True)
    with open(ledger_path(stage), "a") as f: f.write(json.dumps({"t": now(), **entry}) + "\n")


def spent(stage: str | None = None) -> tuple[float, float]:
    """(usd, machine hours) of every settled run, valid or invalid, in the stage or in all stages."""
    stages = [stage] if stage else [p.parent.name for p in OUT.glob("*/ledger.jsonl")]
    rows = [e for s in stages for e in ledger(s) if e["kind"] == "settle"]
    return round(sum(e["usd"] for e in rows), 4), sum(e["seconds"] for e in rows) / 3600


def worst_usd(arm: str) -> float:
    c = cfg()
    jev = c["jev"]["max_calls_per_run"] * 2 * c["jev"]["usd_per_call"] if arm == "new" else 0.0  # curl --retry 1: up to 2 requests per call
    return c["caps"]["run_reserve_usd"] + jev


def settled_usd(meta: dict) -> float:
    c = cfg()
    claude = meta["cost_usd"] if isinstance(meta.get("cost_usd"), (int, float)) else c["caps"]["run_reserve_usd"]  # unknown cost: a full reserve
    return round(claude + meta.get("jev_calls", 0) * (c["jev"]["usd_per_call"] or 0) * 2, 4)


def fits(stage: str, arms: list[str]) -> tuple[bool, str]:
    c = cfg()
    need = sum(worst_usd(a) for a in arms)
    s_usd, _ = spent(stage); t_usd, hours = spent()
    hours_need = len(arms) * (c["caps"]["wall_s"] + c["caps"]["grade_s"]) / 3600
    if s_usd + need > c["stages"][stage]["cap_usd"]: return False, f"stage {stage}: spent ${s_usd:.2f} + reserve ${need:.2f} > cap ${c['stages'][stage]['cap_usd']:.2f}"
    if t_usd + need > c["caps"]["total_usd"]: return False, f"total: spent ${t_usd:.2f} + reserve ${need:.2f} > ceiling ${c['caps']['total_usd']:.2f}"
    if hours + hours_need > c["caps"]["machine_hours"]: return False, f"machine hours: {hours:.1f} + {hours_need:.1f} > {c['caps']['machine_hours']}"
    return True, f"reserve ${need:.2f}"


def run_and_grade(stage: str, unit: dict, arm: str, attempt: int, key) -> dict:
    rdir = run_one(stage, unit, arm, attempt, key)
    meta = json.loads((rdir / "meta.json").read_text())
    g = grade.grade_run(rdir)
    grade.diagnose(rdir)
    if not any(e["kind"] == "settle" and e["run"] == meta["id"] for e in ledger(stage)):
        log(stage, kind="settle", run=meta["id"], usd=settled_usd(meta), claude_usd=meta.get("cost_usd"), jev_calls=meta.get("jev_calls", 0),
            seconds=round(meta["wall_s"] + g.get("grade_s", 0), 1))
    return {"meta": meta, "grade": g, "invalid": invalid_reasons(meta, g)}


def claude_version() -> str:
    v = subprocess.run([claude_bin(), "--version"], capture_output=True, text=True).stdout.split()
    return v[0] if v else ""


def arms_sha() -> str:
    return sha256_bytes((ARMS_DIR / "MANIFEST.json").read_bytes())


def preconditions(arms):
    c = cfg()
    if claude_version() != c["claude_version"]: die(f"claude {claude_version()!r} is not the pinned {c['claude_version']}")
    if "new" in arms and (not c["jev"]["model"] or not c["jev"]["usd_per_call"]):
        die("config jev.model and jev.usd_per_call must be set (verified model id, current price) before a new-arm run")
    arm_manifest("old")
    p = PROBE_RECORD
    rec = json.loads(p.read_text()) if p.exists() else {}
    if not rec.get("passed") or rec.get("arms_manifest_sha256") != arms_sha() or rec.get("claude_version") != c["claude_version"]:
        die(f"the last live sandbox probe ({p}) did not pass for the frozen arms on the pinned claude; run: python3 -I runner.py isolation --live")


def unit_key(u: dict) -> str:
    return f"{u['case']}-{u['block']}"


def run_unit(stage: str, unit: dict, key) -> bool:
    """Run a unit (a pair, or 1 control run); retry an invalid block once. False when the batch must halt."""
    for attempt in (1, 2):
        ok, why = fits(stage, unit["arms"])
        if not ok:
            log(stage, kind="halt", unit=unit_key(unit), reason=why); print(f"HALT before {unit_key(unit)}: {why}"); return False
        log(stage, kind="reserve", unit=unit_key(unit), attempt=attempt, usd=sum(worst_usd(a) for a in unit["arms"]))
        outs = [run_and_grade(stage, unit, arm, attempt, key) for arm in unit["arms"]]
        reasons = {o["meta"]["id"]: o["invalid"] for o in outs if o["invalid"]}
        for o in outs:
            print(f"{o['meta']['id']}: ${o['meta'].get('cost_usd')} {o['meta']['wall_s']}s stop={o['meta']['stop_reason']} "
                  f"accepted_exec={o['grade'].get('accepted_exec')} invalid={o['invalid'] or '-'}", flush=True)
        if any(drift(o["meta"]) for o in outs):
            log(stage, kind="halt", unit=unit_key(unit), reason="jev model drift", invalid=reasons); print("HALT: Jev model drift"); return False
        if not reasons:
            log(stage, kind="unit", unit=unit_key(unit), status="valid", runs=[o["meta"]["id"] for o in outs]); return True
        log(stage, kind="invalid", unit=unit_key(unit), attempt=attempt, reasons=reasons)
    log(stage, kind="unit", unit=unit_key(unit), status="invalid", runs=[o["meta"]["id"] for o in outs])
    return True


def case_inputs() -> dict:
    return {load_case(d)["id"]: tree_sha(d) for d in case_dirs()}


def make_plan(stage: str) -> dict:
    """Pilot: 1 old/new pair per case (the I05-type case on its clean variant). Main: 6 pairs per case (seeded variant),
    2 clean pairs per review case, 1 control run per case. Old/new order balanced within case; units shuffled.
    A stage with "arms": 1 unit per case with those arms, block = the stage name (no clash with another stage's run ids),
    and with "like": <stage>, each case's variant from that stage's plan, so the runs compare like for like."""
    seed = secrets.randbits(32)
    rng, units = random.Random(seed), []
    st = cfg()["stages"][stage]
    like_p = OUT / st.get("like", "") / "plan.json"
    if "like" in st and not like_p.exists(): die(f"stage {stage} copies variants from {st['like']}, but {like_p} is missing")
    like = {u["case"]: u["variant"] for u in json.loads(like_p.read_text())["units"]} if "like" in st else {}
    if not set(st.get("arms", ARMS)) <= set(ARMS) or st.get("arms") == []: die(f"stage {stage}: arms must be a non-empty subset of {ARMS}")
    for d in case_dirs():
        case = load_case(d)
        rv = is_review(case)
        if like and case["id"] not in like: die(f"case {case['id']} is not in the plan of {st['like']}")
        if "arms" in st:
            units.append({"case": case["id"], "block": stage, "variant": like.get(case["id"], "clean" if rv else None),
                          "arms": rng.sample(st["arms"], len(st["arms"]))})
            continue
        if stage == "pilot":
            units.append({"case": case["id"], "block": "p1", "variant": "clean" if rv else None, "arms": rng.sample(["old", "new"], 2)})
            continue
        firsts = ["old", "new"] * 3; rng.shuffle(firsts)
        units += [{"case": case["id"], "block": str(i + 1), "variant": "seeded" if rv else None, "arms": [f, "new" if f == "old" else "old"]}
                  for i, f in enumerate(firsts)]
        if rv:
            cf = ["old", "new"]; rng.shuffle(cf)
            units += [{"case": case["id"], "block": f"c{i + 1}", "variant": "clean", "arms": [f, "new" if f == "old" else "old"]} for i, f in enumerate(cf)]
        units.append({"case": case["id"], "block": "n1", "variant": "seeded" if rv else None, "arms": ["none"]})
    rng.shuffle(units)
    return {"stage": stage, "created": now(), "seed": seed, "inputs": case_inputs(), "arms": json.loads((ARMS_DIR / "MANIFEST.json").read_text())["frozen"],
            "units": units}


def batch(stage: str, approved_cap: float):
    c = cfg()
    if stage not in c["stages"]: die(f"unknown stage {stage}")
    if abs(approved_cap - c["stages"][stage]["cap_usd"]) > 1e-9: die(f"--approved-cap must equal the configured cap of {stage}: {c['stages'][stage]['cap_usd']}")
    lock()
    plan_p = OUT / stage / "plan.json"
    if not plan_p.exists():
        arm_manifest("old"); plan_p.parent.mkdir(parents=True, exist_ok=True); plan_p.write_text(json.dumps(make_plan(stage), indent=1))
    plan = json.loads(plan_p.read_text())
    if plan["inputs"] != case_inputs(): die("frozen case inputs changed since the plan was made", 1)
    arms = {a for u in plan["units"] for a in u["arms"]}
    if not arms <= set(c["stages"][stage].get("arms", ARMS)): die(f"plan {plan_p} runs arms {sorted(arms)} outside the stage's arms")
    preconditions(arms)
    key = jev_key() if "new" in arms else None
    done = {e["unit"] for e in ledger(stage) if e["kind"] == "unit"}
    for unit in plan["units"]:
        if unit_key(unit) in done: continue
        if not run_unit(stage, unit, key): break
    usd, hours = spent(stage)
    print(f"stage {stage}: spent ${usd:.2f} of ${c['stages'][stage]['cap_usd']:.2f}, {hours:.2f} machine hours")


def single(stage, case_id, arm, block, variant=None):
    if arm not in ARMS or stage not in cfg()["stages"] or not re.fullmatch(r"[A-Za-z0-9]+", block): die(__doc__)
    lock()
    preconditions({arm})
    unit = {"case": case_id, "block": block, "variant": variant, "arms": [arm]}
    find_case(case_id)
    run_unit(stage, unit, jev_key() if arm == "new" else None)


# ---------- isolation ----------

PROBE_RECORD = OUT / "isolation" / "probe.json"  # the last live probe; paid runs start only when it passed
PROBE_USD = 0.05  # Claude cap per arm of the live probe
DENIED = re.compile("Operation not permitted|Permission denied|<sandbox_violations>|CONNECT tunnel failed|"
                    + "|".join(map(re.escape, (DENY_NET, DENY_UNSANDBOXED, DENY_READ, DENY_WRITE))), re.I)  # zsh says "operation not permitted"


def live_probes(arm: str) -> list[dict]:
    """The shell commands of the live probe with the outcome each must have in this arm. An allowed result must print 'out'
    when it is set; a command with sandbox False runs through the host-approved unsandboxed path, as builds do."""
    def p(cmd, want, out=None, sandbox=True): return {"cmd": cmd, "want": want, "out": out, "sandbox": sandbox}
    rows = [p("ls ~", "denied"), p("cat ~/.claude/CLAUDE.md", "denied"), p(f"ls {REPO}", "denied"), p(f"ls {OUT}", "denied"),
            p("ls /tmp", "denied"), p("ls /Volumes", "denied"),
            p("curl -sS -m 5 -o /dev/null -w '%{http_code}' https://example.com", "denied"),
            p("cat ~/.zshrc", "denied", sandbox=False),
            p("echo probe > probe.txt && cat probe.txt", "allowed", "(?m)^probe$"),
            p('echo probe > "$TMPDIR/probe.txt" && cat "$TMPDIR/probe.txt"', "allowed", "(?m)^probe$"),
            p("git status --short", "allowed"), p("git config --get user.name", "allowed", "(?m)^Developer$"),
            p("swift --version", "allowed", r"Swift version"), p("xcodebuild -version", "allowed", r"Xcode \d", sandbox=False)]
    if arm != "none": rows += [p(f"ls {SKILL_DIR}", "allowed", "SKILL.md"), p(f"touch {SKILL_DIR}/probe.txt", "denied")]
    if arm == "new":
        rows += [p(f"{SKILL_DIR}/scripts/route --help", "allowed", "Usage: route"),
                 p(f"{SKILL_DIR}/scripts/decide check-swallowed-error Probe.swift", "allowed",
                   '"source":"jev","model":"' + re.escape(str(cfg()["jev"]["model"])) + '"')]
    return rows


def probe_prompt(probes: list[dict]) -> str:
    def cmds(sandbox): return "; ".join(f"`{x['cmd']}`" for x in probes if x["sandbox"] == sandbox)
    return ("Run each of these commands with the Bash tool exactly as written, one call per command, in order. Do not retry or change "
            f"a command that fails. Then stop and reply 'done'. In the sandbox: {cmds(True)}. "
            f"With dangerouslyDisableSandbox set to true: {cmds(False)}.")


def tool_calls(stream: Path) -> list[dict]:
    """Every tool call of a session in order, with its result: name, input, is_error, text (None when no result came)."""
    calls, at = [], {}
    for line in stream.read_text().splitlines():
        try: e = json.loads(line)
        except ValueError: continue
        if not isinstance(e, dict): continue
        content = (e.get("message") or {}).get("content") if e.get("type") in ("assistant", "user") else None
        for c in content if isinstance(content, list) else []:
            if not isinstance(c, dict): continue
            if c.get("type") == "tool_use":
                at[c.get("id")] = len(calls); calls.append({"name": c.get("name"), "input": c.get("input") or {}, "is_error": None, "text": None})
            elif c.get("type") == "tool_result" and c.get("tool_use_id") in at:
                calls[at[c["tool_use_id"]]] |= {"is_error": bool(c.get("is_error")), "text": _text(c.get("content"))}
    return calls


def outcome(probe: dict, call: dict | None) -> str:
    """allowed, denied, error (failed for another reason, or printed no expected output), or not run."""
    if not call or call["text"] is None: return "not run"
    if call["is_error"] and DENIED.search(call["text"]): return "denied"
    if probe["out"]:
        if re.search(probe["out"], call["text"]): return "allowed"
    elif not call["is_error"]: return "allowed"
    return "error"


def probe_table(probes: list[dict], calls: list[dict]) -> list[dict]:
    """Each probe against the first Bash call of the same command and sandbox mode; ok when the outcome is the expected one."""
    def norm(s): return " ".join(str(s).split())
    rows = []
    for x in probes:
        call = next((c for c in calls if c["name"] == "Bash" and norm(c["input"].get("command", "")) == norm(x["cmd"])
                     and bool(c["input"].get("dangerouslyDisableSandbox")) != x["sandbox"]), None)
        got = outcome(x, call)
        rows.append({"cmd": x["cmd"], "sandbox": x["sandbox"], "want": x["want"], "got": got, "ok": got == x["want"],
                     "result": ((call or {}).get("text") or "")[:200]})
    return rows


def context_tables(text: str) -> dict:
    out, sec = {}, None
    for ln in text.splitlines():
        if ln.startswith("### "): sec = ln[4:].strip(); out[sec] = []
        elif sec and ln.startswith("|") and not set(ln) <= set("|- "):
            cells = [x.strip() for x in ln.strip("|").split("|")]
            if cells[0] not in ("Category", "Skill", "Type", "Name", "Tool"): out[sec].append(cells)
    return out


def isolation(case_id: str | None, live: bool):
    lock()
    case = find_case(case_id) if case_id else load_case(case_dirs()[0])
    c, report = cfg(), {"case": case["id"], "live": live, "arms": {}}
    key = jev_key() if live else "probe-key-not-real"  # the live probe makes 1 real decide call in the new arm
    for arm in ARMS:
        reset_scratch(); make_work(case, WORK); skill = install(arm)
        write_curl_wrapper(1 if live else c["jev"]["max_calls_per_run"], c["jev"]["host"])
        idir = OUT / "isolation" / arm; shutil.rmtree(idir, ignore_errors=True); idir.mkdir(parents=True)
        probes = live_probes(arm) if live else []
        if live and arm == "new":  # a tiny synthetic file in a project that lets code leave the machine
            (WORK / "Probe.swift").write_text("func load() throws -> Int { 1 }\nlet value = try? load()\n")
            (WORK / "ios-architecture.json").write_text('{"code_may_leave_machine": true}\n')
        model, effort, budget, prompt = (c["builder"]["fallback_small"], "low", PROBE_USD, probe_prompt(probes)) if live \
            else (c["builder"]["model"], c["builder"]["effort"], c["caps"]["run_usd"], "/context")
        env = builder_env(arm, key if arm == "new" else None)
        redact = Redactor(key)
        execute(build_cmd(arm, budget, model, effort), env, prompt, arm, idir / "stream.jsonl", idir / "stderr.txt", 180 if live else 120, redact)
        kill_by_path(WORK, TMP)
        m = parse_stream(idir / "stream.jsonl")
        tables = context_tables(m["final_text"])
        report["arms"][arm] = {"skill_manifest_sha256": skill, "cwd": (m["init"] or {}).get("cwd"), "model": (m["init"] or {}).get("model"),
                               "tools": (m["init"] or {}).get("tools"), "mcp_servers": (m["init"] or {}).get("mcp_servers"),
                               "plugins": [p.get("name") for p in (m["init"] or {}).get("plugins") or []],
                               "skills_init": (m["init"] or {}).get("skills"),
                               "skills_context": [(r[0], r[1]) for r in tables.get("Skills", [])],
                               "memory_files": [r[1] for r in tables.get("Memory Files", [])],
                               "env_names": sorted(env), "sandbox": sandbox_settings(arm)["sandbox"], "cost_usd": m["cost_usd"],
                               "host_denials": m["host_denials"]}
        r = report["arms"][arm]
        foreign = [s for s, src in r["skills_context"] if not (src == "Built-in" or s == SKILL_NAME)]
        r["verdict"] = {"memory_files": not r["memory_files"], "no_mcp": not r["mcp_servers"], "no_foreign_skills": not foreign,
                        "arm_skill": (SKILL_NAME in (r["skills_init"] or [])) == (arm != "none"), "free": live or r["cost_usd"] in (0, None)}
        r["foreign_skills"] = foreign
        if live:
            if (LOG / "curl.log").exists(): (idir / "curl.log").write_text(redact((LOG / "curl.log").read_text()))
            r["probes"] = probe_table(probes, tool_calls(idir / "stream.jsonl"))
            r["jev_calls"] = parse_curl_log(idir / "curl.log", c["jev"]["host"])["jev_calls"]
            r["verdict"]["probes"] = all(x["ok"] for x in r["probes"])
    builtin = {arm: set(r["plugins"]) - {"skills"} for arm, r in report["arms"].items()}
    report["builtin_plugins_differ"] = sorted(set.union(*builtin.values()) - set.intersection(*builtin.values()))
    report["policy_probes"] = policy_probes()
    (OUT / "isolation" / "isolation.json").write_text(json.dumps(report, indent=1))
    for arm, r in report["arms"].items():
        print(f"{arm}: cwd={r['cwd']} model={r['model']} tools={r['tools']} plugins={r['plugins']} mcp={r['mcp_servers']}")
        print(f"   skills (non built-in): {[s for s, src in r['skills_context'] if src != 'Built-in']}  memory files: {r['memory_files']}  cost: {r['cost_usd']}")
        print(f"   verdict: {r['verdict']}")
    print("built-in plugins not loaded in every arm:", report["builtin_plugins_differ"] or "none")
    print("policy probes:", "all as expected" if all(p["ok"] for p in report["policy_probes"]) else report["policy_probes"])
    print(f"written: {OUT / 'isolation' / 'isolation.json'}")
    if not live: return
    for arm, r in report["arms"].items():
        for x in r["probes"]:
            print(f"{arm:4} {'ok  ' if x['ok'] else 'FAIL'} want={x['want']:7} got={x['got']:7} {'' if x['sandbox'] else '[unsandboxed] '}{x['cmd']}")
    passed = all(all(r["verdict"].values()) for r in report["arms"].values()) and all(p["ok"] for p in report["policy_probes"])
    PROBE_RECORD.write_text(json.dumps({"t": now(), "passed": passed, "arms_manifest_sha256": arms_sha(), "claude_version": claude_version(),
                                        "case": case["id"], "cost_usd": {a: r["cost_usd"] for a, r in report["arms"].items()},
                                        "jev_calls": sum(r["jev_calls"] for r in report["arms"].values())}, indent=1))
    print(f"live probe: {'PASS' if passed else 'FAIL'} -> {PROBE_RECORD}")
    if not passed: sys.exit(1)


def policy_probes() -> list[dict]:
    home, rows = Path.home(), []
    cases = [("Read", {"file_path": str(home / ".claude/CLAUDE.md")}, "new", False),
             ("Read", {"file_path": str(REPO / "skills/ios-architecture/SKILL.md")}, "old", False),
             ("Read", {"file_path": str(OUT)}, "new", False),
             ("Glob", {"path": "/tmp"}, "none", False),
             ("Grep", {"path": str(home)}, "none", False),
             ("Read", {"file_path": str(WORK / "x.swift")}, "none", True),
             ("Read", {"file_path": str(SKILL_DIR / "SKILL.md")}, "new", True),
             ("Write", {"file_path": str(SKILL_DIR / "SKILL.md")}, "new", False),
             ("Write", {"file_path": str(WORK / "../escape.txt")}, "new", False),
             ("Edit", {"file_path": "App/A.swift"}, "old", True),
             ("SandboxNetworkAccess", {"host": "api.typesafe.ai:443"}, "new", True),
             ("SandboxNetworkAccess", {"host": "api.typesafe.ai:443"}, "old", False),
             ("SandboxNetworkAccess", {"host": "github.com"}, "new", False),
             ("Bash", {"command": "ls", "dangerouslyDisableSandbox": False}, "none", True),
             ("Bash", {"command": "xcodebuild -scheme App test -destination 'platform=iOS Simulator,name=iPhone 17'", "dangerouslyDisableSandbox": True}, "none", True),
             ("Bash", {"command": "xcodebuild test; cat ~/.claude/CLAUDE.md", "dangerouslyDisableSandbox": True}, "none", False),
             ("Bash", {"command": "xcodebuild test\ncat /etc/hosts", "dangerouslyDisableSandbox": True}, "none", False),
             ("Bash", {"command": f"xcodebuild -workspace {REPO}/x.xcworkspace build", "dangerouslyDisableSandbox": True}, "none", False),
             ("Bash", {"command": "cat ~/.zshrc", "dangerouslyDisableSandbox": True}, "none", False),
             ("WebFetch", {"url": "https://example.com"}, "new", False)]
    for tool, inp, arm, want in cases:
        got = policy(tool, inp, arm)[0]
        rows.append({"tool": tool, "input": inp, "arm": arm, "allowed": got, "ok": got == want})
    return rows


def selftest():
    bad = [p for p in policy_probes() if not p["ok"]]
    assert not bad, bad
    assert parse_curl_log(Path("/nonexistent"), "api.typesafe.ai")["jev_calls"] == 0
    print("selftest ok")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a: die(__doc__)
    if a[0] == "freeze": freeze()
    elif a[0] == "isolation": isolation(a[a.index("--case") + 1] if "--case" in a else None, "--live" in a)
    elif a[0] == "run" and len(a) in (5, 6): single(a[1], a[2], a[3], a[4], a[5] if len(a) == 6 else None)
    elif a[0] == "batch" and len(a) == 4 and a[2] == "--approved-cap": batch(a[1], float(a[3]))
    elif a[0] == "selftest": selftest()
    else: die(__doc__)
