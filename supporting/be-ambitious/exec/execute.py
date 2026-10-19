"""Execute ORIGINAL vs REWRITE prompts on fixtures and judge them.
  python3 -I execute.py run X1 REWRITE 1      one run + judge
  python3 -I execute.py batch                 every missing run, cost-gated
  python3 -I execute.py report                write results.md
  python3 -I execute.py selftest              offline policy() checks
"""
import hashlib, json, os, re, shutil, signal, statistics, subprocess, sys, threading, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

EXEC = Path(__file__).resolve().parent
WORK = EXEC.parent
RUNS, PROMPTS = EXEC / "runs", EXEC / "prompts"
ARCHIVES = {"v1-allowlist": "harness v1: per-command Bash allowlist in dontAsk mode. Harmless compound commands (echo, loops) were denied, and the model read one denial as \"no Bash\"",
            "v2-shared-tmp": "harness v2 before tmp isolation: all runs shared the sandbox $TMPDIR, and one X3 run found X1 files there",
            "v2-tmp-leak": "harness v2 with a 35-char CLAUDE_CODE_TMPDIR, which the sandbox silently replaced with the shared /tmp/claude-501; X3-REWRITE-1 and -3 both used $TMPDIR/perf"}
SCRATCH = Path("/tmp/ambition-exec")
BIN = SCRATCH / "bin"
TOTAL_CAP, RUN_CAP, WALL_S = 40.0, 6.0, 45 * 60
SUFFIX = "Work in the current directory. You cannot ask questions; where the prompt asks for approval, do not do that part and say so."
FIX = {"X1": ("fixture-ts", "x1", "T01"), "X2": ("fixture-readme", "x2", "T04"), "X3": ("fixture-site", "x3", "T11")}
REWRITE_SRC = {"T01": "T01-claude-1", "T04": "T04-claude-1", "T11": "T11-claude-1"}  # all three grade pass in eval/calibration-runs/v7/grades
ARMS = ("ORIGINAL", "REWRITE")

# Harness v2. v1 used a per-command Bash allowlist in dontAsk mode; harmless compound commands (echo, loops) were
# denied and the model read one denial as "no Bash", which penalised the verification-heavy arm (tables in results.md).
# v2: every Bash command runs in the OS sandbox (no network, writes only in cwd + tmp); this host answers each
# permission prompt with policy() and logs the decision into the transcript.
SANDBOX = {"enabled": True, "autoAllowBashIfSandboxed": True, "allowUnsandboxedCommands": False,
           "network": {"allowLocalBinding": True, "allowedDomains": []}}
# Chrome cannot start inside the sandbox, so X3 runs Lighthouse outside it, for localhost URLs only.
SANDBOX_X3 = {**SANDBOX, "allowUnsandboxedCommands": True, "excludedCommands": ["lighthouse:*"]}
LH_LOCAL = re.compile(r"""lighthouse\s+['"]?https?://(localhost|127\.0\.0\.1)(:\d+)?(/[^\s;&|`$<>]*)?['"]?(\s+[^;&|`$<>]*)?""")
LOCAL_HOSTS = {"localhost", "127.0.0.1", "::1", "0.0.0.0"}


def policy(tool: str, inp: dict, dest: Path) -> tuple[bool, str]:
    if tool == "SandboxNetworkAccess":
        host = str(inp.get("host", "")).rsplit(":", 1)[0].strip("[]")
        return host in LOCAL_HOSTS, "Network access beyond localhost is not available in this environment."
    if tool == "Bash":
        if not inp.get("dangerouslyDisableSandbox"):
            return True, ""
        cmd = inp.get("command", "")
        # a newline or CR ends the Lighthouse command and starts a second, unsandboxed one
        ok = "\n" not in cmd and "\r" not in cmd and bool(LH_LOCAL.fullmatch(cmd.strip()))
        return ok, "Only Lighthouse on localhost can run outside the sandbox here."
    if tool in ("Read", "Edit", "Write", "Glob", "Grep"):
        path = str(inp.get("file_path") or inp.get("path") or dest)
        inside = Path(path).resolve().is_relative_to(dest.resolve()) or path.startswith(("/tmp/", "/private/tmp/"))
        return inside, "Files outside the working directory are not available here."
    return False, f"{tool} is not available in this environment."


def prompt(fx: str, arm: str) -> str:
    PROMPTS.mkdir(exist_ok=True)
    p = PROMPTS / f"{fx}-{arm}.txt"
    if not p.exists():
        case = FIX[fx][2]
        if arm == "ORIGINAL":
            text = (WORK / "cases" / f"{case}.txt").read_text().strip()
        else:
            md = (WORK / "eval/calibration-runs/v7" / f"{REWRITE_SRC[case]}.md").read_text()
            text = re.search(r"```[^\n]*\n(.*?)\n```", md, re.S).group(1).strip()
        p.write_text(text + "\n")
    return p.read_text().strip() + "\n\n" + SUFFIX


def kill_by_cwd(dest: Path):
    out = subprocess.run(["lsof", "-d", "cwd", "-F", "pn"], capture_output=True, text=True).stdout
    pid = None
    for line in out.splitlines():
        if line.startswith("p"): pid = int(line[1:])
        elif line.startswith("n") and pid and str(dest.resolve()) in line and pid != os.getpid():
            try: os.kill(pid, signal.SIGKILL)
            except ProcessLookupError: pass


def parse_stream(path: Path) -> dict:
    tools, init, results, host, received = {}, {}, [], [], None
    for line in path.read_text().splitlines():
        try: e = json.loads(line)
        except ValueError: continue
        t = e.get("type")
        if t == "system" and e.get("subtype") == "init":
            init = {k: e.get(k) for k in ("tools", "mcp_servers", "slash_commands", "plugins", "permissionMode", "model", "skills")}
        elif t == "assistant":
            for c in e["message"]["content"]:
                if c.get("type") == "tool_use": tools[c["id"]] = c["name"]
        elif t == "user" and isinstance(e.get("message", {}).get("content"), str):
            received = received or e["message"]["content"]
        elif t == "host_decision":
            host.append(e)
        elif t == "result":  # a background-task notification can add a short second result; cost is cumulative
            results.append(e)
    result = results[-1] if results else {}
    by = {}
    for name in tools.values(): by[name] = by.get(name, 0) + 1
    return {"init": init, "tool_calls": len(tools), "tool_calls_by_name": by,
            "cost_usd": result.get("total_cost_usd"), "duration_ms": sum(r.get("duration_ms") or 0 for r in results),
            "num_turns": sum(r.get("num_turns") or 0 for r in results), "result_events": len(results),
            "subtype": result.get("subtype"), "is_error": result.get("is_error"), "denials": len(result.get("permission_denials") or []),
            "host_prompts": len(host), "host_denials": [h["input"] for h in host if not h["allow"]],
            "received_prompt_sha256": hashlib.sha256(received.encode()).hexdigest() if received else None,
            "final_text": max((r.get("result") or "" for r in results), key=len, default="")[-4000:], "usage": result.get("usage")}


def execute(fx: str, text: str, dest: Path, tmp: Path, stream: Path, err: Path, budget: float):
    allowed = ["Read", "Edit", "Write", "Glob", "Grep"]
    if fx == "X3": allowed += ["Bash(lighthouse http://localhost*)", "Bash(lighthouse http://127.0.0.1*)"]
    cmd = ["claude", "-p", "--restricted", "--safe-mode", "--strict-mcp-config", "--setting-sources", "project",
           "--no-session-persistence", "--model", "claude-opus-5-5", "--effort", "high",
           "--tools", "Read,Edit,Write,Glob,Grep,Bash", "--allowedTools", *allowed, "--permission-prompt-tool", "stdio",
           "--settings", json.dumps({"sandbox": SANDBOX_X3 if fx == "X3" else SANDBOX}), "--max-budget-usd", f"{budget:.2f}",
           "--input-format", "stream-json", "--replay-user-messages", "--output-format", "stream-json", "--verbose"]
    # a private CLAUDE_CODE_TMPDIR per run: the default sandbox $TMPDIR (/tmp/claude-<uid>) is shared and leaked files across
    # runs. Claude Code ignores CLAUDE_CODE_TMPDIR while TMPDIR is set, so TMPDIR is removed.
    env = {k: v for k, v in os.environ.items() if k != "TMPDIR"} | {"PATH": f"{BIN}:{os.environ['PATH']}", "CLAUDE_CODE_TMPDIR": str(tmp)}
    with open(stream, "w") as out, open(err, "w") as er:
        proc = subprocess.Popen(cmd, cwd=dest, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=er, text=True,
                                env=env, start_new_session=True)

        def stop():
            for sig in (signal.SIGTERM, signal.SIGKILL):
                try: os.killpg(proc.pid, sig); time.sleep(3)
                except ProcessLookupError: return

        def send(obj):
            try: proc.stdin.write(json.dumps(obj) + "\n"); proc.stdin.flush()
            except (BrokenPipeError, ValueError): pass

        watchdog = threading.Timer(WALL_S, stop); watchdog.start()
        send({"type": "user", "message": {"role": "user", "content": text}})
        for line in proc.stdout:
            out.write(line)
            try: e = json.loads(line)
            except ValueError: continue
            if e.get("type") == "control_request" and e.get("request", {}).get("subtype") == "can_use_tool":
                r = e["request"]
                ok, why = policy(r.get("tool_name"), r.get("input") or {}, dest)
                out.write(json.dumps({"type": "host_decision", "tool": r.get("tool_name"), "allow": ok, "input": r.get("input")}) + "\n")
                resp = {"behavior": "allow", "updatedInput": r.get("input")} if ok else {"behavior": "deny", "message": why}
                send({"type": "control_response", "response": {"subtype": "success", "request_id": e["request_id"], "response": resp}})
            elif e.get("type") == "result":
                proc.stdin.close()
                threading.Timer(10, stop).start()  # claude -p can wait on a background dev server after its result
        proc.wait()
        watchdog.cancel()


def run_one(fx: str, arm: str, n: int, budget: float = RUN_CAP) -> dict:
    rid = f"{fx}-{arm}-{n}"
    summary = RUNS / f"{rid}.json"
    if summary.exists(): return json.loads(summary.read_text())
    RUNS.mkdir(exist_ok=True)
    fixture, kind, _ = FIX[fx]
    dest = SCRATCH / f"{fixture}-{arm}-{n}"
    if dest.exists(): shutil.rmtree(dest)
    shutil.copytree(EXEC / "fixtures" / fixture, dest, symlinks=True)
    # short on purpose: a CLAUDE_CODE_TMPDIR longer than ~30 chars makes the sandbox fall back to the shared /tmp/claude-<uid>
    tmp = SCRATCH / "t" / f"{fx}{arm[0]}{n}"
    if tmp.exists(): shutil.rmtree(tmp)
    tmp.mkdir(parents=True)
    text = prompt(fx, arm)
    stream = RUNS / f"{rid}.jsonl"
    t0 = time.time()
    execute(fx, text, dest, tmp, stream, RUNS / f"{rid}.err", budget)
    wall = time.time() - t0
    kill_by_cwd(dest); kill_by_cwd(tmp)
    meta = parse_stream(stream)
    meta |= {"id": rid, "fixture": fx, "arm": arm, "n": n, "workdir": str(dest), "wall_s": round(wall, 1), "timed_out": wall > WALL_S,
             "prompt_sha256": hashlib.sha256(text.encode()).hexdigest()}
    meta["prompt_delivered"] = meta["received_prompt_sha256"] == meta["prompt_sha256"]
    meta["shared_tmp_refs"] = stream.read_text().count(f"/tmp/claude-{os.getuid()}/")  # must be 0: proves the run used its own tmp
    port = 18300 + n + (10 if arm == "REWRITE" else 0)
    jargs = ["python3", "-I", str(EXEC / "judges/judges.py"), kind, str(dest)] + ([str(port)] if kind == "x3" else [])
    j = subprocess.run(jargs, capture_output=True, text=True, timeout=1800)
    meta["judge"] = json.loads(j.stdout) if j.returncode == 0 else {"error": j.stderr[-1000:]}
    summary.write_text(json.dumps(meta, indent=1, ensure_ascii=False))
    print(f"{rid}: cost=${meta['cost_usd']} wall={meta['wall_s']}s tools={meta['tool_calls']} delivered={meta['prompt_delivered']} "
          f"host_denials={len(meta['host_denials'])} shared_tmp_refs={meta['shared_tmp_refs']} judge={meta['judge'].get('items')}", flush=True)
    return meta


# cost with no summary file: a deleted leaky gate run ($0.41), probes ($0.05), two runs killed mid-flight (estimate <= $1)
UNTRACKED_USD = 1.50
DELETED_USD = 32.53  # the 64 recorded runs whose logs in runs/ were deleted on 2026-10-19; their tables stay in results.md


def spent() -> float:  # every executor run so far, all harnesses, plus UNTRACKED_USD and DELETED_USD
    return UNTRACKED_USD + DELETED_USD + sum(json.loads(p.read_text()).get("cost_usd") or 0 for p in RUNS.glob("**/X*-*-[0-9].json"))


def batch():
    todo = [(fx, arm, n) for fx in ("X1", "X2") for arm in ARMS for n in (1, 2, 3) if not (RUNS / f"{fx}-{arm}-{n}.json").exists()]
    with ThreadPoolExecutor(3) as pool:
        futures = []
        for job in todo:
            # each in-flight run is bounded by RUN_CAP; launch only while the worst case stays under the total cap
            while sum(not f.done() for f in futures) and spent() + RUN_CAP * (sum(not f.done() for f in futures) + 1) > TOTAL_CAP:
                time.sleep(5)
            if spent() + RUN_CAP > TOTAL_CAP: print("STOP: total cap reached", spent()); return
            futures.append(pool.submit(run_one, *job))
        for f in futures: f.result()
    for arm in ARMS:  # sequential: one dev server port and one Lighthouse at a time
        for n in (1, 2, 3):
            if (RUNS / f"X3-{arm}-{n}.json").exists(): continue
            if spent() + RUN_CAP > TOTAL_CAP: print("STOP: total cap reached", spent()); return
            run_one("X3", arm, n)
    print("total spent", round(spent(), 2))


NAMES = {"X1": "X1 fixture-ts (T01, formatLabel null)", "X2": "X2 fixture-readme (T04, one-byte typo)", "X3": "X3 fixture-site (T11, mobile load)"}


def tables(runs_dir: Path, base: dict, level: str = "##") -> list[str]:
    tick = lambda b: "pass" if b else "FAIL"
    out = []
    for fx in FIX:
        arms = {arm: [json.loads(p.read_text()) for n in (1, 2, 3) if (p := runs_dir / f"{fx}-{arm}-{n}.json").exists()] for arm in ARMS}
        out += [f"{level} {NAMES[fx]}", ""]
        all_runs = [r for arm in ARMS for r in arms[arm]]
        if not all_runs: out += ["Not run.", ""]; continue
        items = list(next(r["judge"]["items"] for r in all_runs if "items" in r["judge"]))
        extra = ["LCP improved", "LCP median ms", "vs baseline", "bytes median", "FCP median ms"] if fx == "X3" else []
        head = items + extra + ["files changed", "tool calls", "cost $", "time s"]
        out += ["| run | " + " | ".join(head) + " |", "|---" * (len(head) + 1) + "|"]
        for r in all_runs:
            j = r["judge"]
            if "items" not in j: out.append(f"| {r['id']} | judge error |"); continue
            m = j["measured"]
            cells = [tick(j["items"][k]) for k in items]
            if fx == "X3":
                cells += [tick(m["lcp_median"] < base["lcp_median"]), f"{m['lcp_median']:.0f}",
                          f"{(m['lcp_median'] / base['lcp_median'] - 1) * 100:+.0f}%", f"{m['bytes_median']:.0f}", f"{m['fcp_median']:.0f}"]
            cells += [", ".join(m["files_changed"]) or "none", str(r["tool_calls"]), f"{r['cost_usd'] or 0:.2f}", f"{(r['duration_ms'] or 0) / 1000:.0f}"]
            out.append(f"| {r['id']} | " + " | ".join(cells) + " |")
        out.append("")
        for arm in ARMS:
            rs = [r for r in arms[arm] if "items" in r["judge"]]
            if not rs: continue
            ok = sum(all(r["judge"]["items"].values()) and (fx != "X3" or r["judge"]["measured"]["lcp_median"] < base["lcp_median"]) for r in rs)
            med = lambda f: statistics.median(f(r) for r in rs)
            line = (f"- {arm}: {ok}/{len(rs)} runs pass every judge item; median cost ${med(lambda r: r['cost_usd'] or 0):.2f}, "
                    f"median time {med(lambda r: (r['duration_ms'] or 0) / 1000):.0f} s, median tool calls {med(lambda r: r['tool_calls']):.0f}")
            if fx == "X3": line += f", median LCP {med(lambda r: r['judge']['measured']['lcp_median']):.0f} ms (baseline {base['lcp_median']:.0f} ms)"
            out.append(line)
        out.append("")
    return out


def report():
    if not any(RUNS.glob("**/X*-*-[0-9].json")): sys.exit("no run summaries in runs/; results.md keeps its recorded tables")
    base = json.loads((EXEC / "judges/x3-baseline.json").read_text())["measured"]
    out = ["# Execution results: ORIGINAL vs REWRITE", "",
           "Executor: `claude -p`, claude-opus-5-5, effort high, `--restricted --safe-mode --strict-mcp-config`, Bash in the OS sandbox "
           "(no network; Lighthouse on localhost only), 3 fresh fixture copies per arm. "
           f"X3 baseline (pristine fixture, 5 Lighthouse mobile runs): LCP median {base['lcp_median']:.0f} ms, "
           f"FCP {base['fcp_median']:.0f} ms, {base['bytes_median']:.0f} bytes.", "",
           *tables(RUNS, base)]
    for name, why in ARCHIVES.items():
        if (RUNS / name).exists():
            out += [f"## Appendix: {name}, superseded", "", f"Superseded: {why}.", "", *tables(RUNS / name, base, "###")]
    out += [f"Total executor cost, all harnesses, including ${UNTRACKED_USD:.2f} untracked (probes, a deleted gate run, killed runs): ${spent():.2f}.", ""]
    res = EXEC / "results.md"
    old = res.read_text() if res.exists() else ""
    keep = old[old.find("<!-- summary -->"):old.find("<!-- /summary -->") + len("<!-- /summary -->")] if "<!-- /summary -->" in old else ""
    if keep: out[2:2] = [keep, ""]  # the hand-written summary survives a regenerated report
    res.write_text("\n".join(out))
    print("\n".join(out))


if __name__ == "__main__":
    def reparse():  # refresh transcript-derived fields of every summary, keep the judge result
        for p in RUNS.glob("**/X*-*-[0-9].json"):
            m = json.loads(p.read_text()); m |= parse_stream(p.with_suffix(".jsonl")); p.write_text(json.dumps(m, indent=1, ensure_ascii=False))
    def selftest():  # offline
        unsandboxed = lambda c: policy("Bash", {"command": c, "dangerouslyDisableSandbox": True}, SCRATCH)[0]
        assert unsandboxed("lighthouse http://localhost:8080 --quiet")
        for chained in ("lighthouse http://localhost:8080 --quiet\ntouch /tmp/x", "lighthouse http://localhost:8080 --quiet\rtouch /tmp/x"):
            assert not unsandboxed(chained), repr(chained)
        print("selftest ok")
    {"run": lambda: run_one(sys.argv[2], sys.argv[3], int(sys.argv[4])), "batch": batch, "report": report, "reparse": reparse, "selftest": selftest}[sys.argv[1]]()
