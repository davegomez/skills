"""Blind review: pack, first pass, adjudication. The key (neutral id -> run) stays outside the pack.
  python3 -I review.py pack <stage>         neutral ids, random order, preselected adjudication sample
  python3 -I review.py review <stage>       1 tools-off Pi reviewer per item (subscription)
  python3 -I review.py adjudicate <stage>   2nd blind pass: critical fails, disputed items, the preselected sample
"""
import json, math, os, random, re, secrets, shutil, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import OUT, cfg, die, find_case, is_review, variant_patch

PACK_ROOT = Path(os.environ.get("IOS_EVAL_PACK", "/tmp/iosev-review"))
MAX_CHARS = 400_000
RESULTS = ("pass", "fail", "na", "unverified")
LINE = ('{{"item": "{nid}", "check": "<check id>", "priority": "<priority>", "severity": "critical|major|minor", '
        '"result": "pass|fail|na|unverified", "evidence": "<file:line, or a short quote>"}}')
PASS1 = ("{nid}.md is 1 delivery for the task in task.md: the executable test results and the change or the review text. "
         "Grade it against every check in rubric.md, using only evidence in these files. "
         "Reply with JSON lines only, 1 line per rubric check, in this form: " + LINE)
PASS2 = ("{nid}.md is 1 delivery for the task in task.md: the executable test results and the change or the review text. "
         "A first reviewer graded it against rubric.md; its lines are in {nid}.first.jsonl. Check each line against the evidence "
         "in the delivery and decide the final result of every rubric check, using only evidence in these files. "
         "Reply with the final JSON lines only, 1 line per rubric check, in this form: " + LINE)


def review_dir(stage: str) -> Path:
    return OUT / stage / "review"


def valid_runs(stage: str) -> list[str]:
    led = OUT / stage / "ledger.jsonl"
    rows = [json.loads(x) for x in led.read_text().splitlines()] if led.exists() else []
    return [r for e in rows if e["kind"] == "unit" and e["status"] == "valid" for r in e["runs"]]


def rubric_ids(case: dict) -> list[str]:
    text = (case["dir"] / "rubric.md").read_text()
    return list(dict.fromkeys(re.findall(rf"\b{re.escape(case['id'])}-[A-Za-z0-9][A-Za-z0-9-]*\b", text)))


def clip(text: str) -> str:
    return text if len(text) <= MAX_CHARS else text[:MAX_CHARS] + f"\n[truncated: {len(text) - MAX_CHARS} more characters]\n"


def item_text(nid: str, rdir: Path, case: dict) -> str:
    meta = json.loads((rdir / "meta.json").read_text())
    g = json.loads((rdir / "grade.json").read_text())
    out = [f"# Delivery {nid}", "", "## Executable test results", "", "| check | priority | critical | result | evidence |", "| --- | --- | --- | --- | --- |"]
    for c in g["result"]["checks"]:
        ev = str(c.get("evidence", "")).replace("|", "/").replace("\n", " ")[:300]
        out.append(f"| {c['id']} | {c['priority']} | {'yes' if c['critical'] else 'no'} | {c['result']} | {ev} |")
    if is_review(case):
        diff = variant_patch(case, meta["variant"]).read_text()
        out += ["", "## The diff under review", "", "```diff", clip(diff), "```", "", "## Files the reviewer wrote (a patch on top of the diff under review)", "",
                "```diff", clip((rdir / "review.diff").read_text()) or "(none)", "```", "", "## Final message", "", clip((rdir / "final.txt").read_text())]
    else:
        out += ["", "## Change (a patch against the starting tree)", "", "```diff", clip((rdir / "patch.diff").read_text()), "```",
                "", "## Final message", "", clip((rdir / "final.txt").read_text())]
    return "\n".join(out) + "\n"


def pack(stage: str):
    key_p = review_dir(stage) / "key.json"
    if key_p.exists(): die(f"pack exists: {key_p}; delete it and {PACK_ROOT / stage} to rebuild")
    runs = valid_runs(stage)
    if not runs: die(f"no valid runs in {stage}")
    root = PACK_ROOT / stage
    shutil.rmtree(root, ignore_errors=True)
    rng = random.Random(secrets.randbits(32))
    rng.shuffle(runs)
    key = {}
    for rid in runs:
        rdir = OUT / stage / "runs" / rid
        case = find_case(json.loads((rdir / "meta.json").read_text())["case"])
        cdir = root / case["id"]
        if not cdir.exists():
            cdir.mkdir(parents=True)
            shutil.copy(case["dir"] / "rubric.md", cdir / "rubric.md"); shutil.copy(case["dir"] / "task.md", cdir / "task.md")
        nid = "d" + secrets.token_hex(4)
        (cdir / f"{nid}.md").write_text(item_text(nid, rdir, case))
        key[nid] = {"run": rid, "case": case["id"]}
    sample = sorted(rng.sample(sorted(key), math.ceil(cfg()["adjudication_sample"] * len(key))))
    review_dir(stage).mkdir(parents=True, exist_ok=True)
    key_p.write_text(json.dumps({"pack": str(root), "order": list(key), "items": key, "sample": sample}, indent=1))
    print(f"packed {len(key)} items in {root}; key and preselected sample ({len(sample)}) in {key_p}")


def parse_lines(text: str, nid: str, ids: list[str]) -> tuple[list[dict], bool]:
    rows = {}
    for ln in text.splitlines():
        ln = ln.strip().strip("`")
        if not ln.startswith("{"): continue
        try: d = json.loads(ln)
        except ValueError: continue
        if isinstance(d, dict) and d.get("item") == nid and d.get("result") in RESULTS and (not ids or d.get("check") in ids):
            rows[d["check"]] = {k: d.get(k) for k in ("check", "priority", "severity", "result", "evidence")}
    return list(rows.values()), all(i in rows for i in ids)


def pi(model: str, thinking: str, cwd: Path, files: list[Path], prompt: str) -> tuple[int, str, str]:
    agent = cfg()["pi_agent_dir"]
    if not (Path(agent) / "auth.json").exists(): die(f"{agent}/auth.json is missing; see README setup")
    cmd = [os.environ.get("IOS_EVAL_PI", "pi"), "-p", "--no-session", "-ne", "-nc", "-ns", "-np", "--no-tools",
           "--model", model, "--thinking", thinking, *[f"@{f.resolve()}" for f in files], prompt]
    try:
        r = subprocess.run(cmd, cwd=cwd, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=1800,
                           env=os.environ | {"PI_CODING_AGENT_DIR": agent})
    except subprocess.TimeoutExpired:
        return -1, "", "timeout"
    return r.returncode, r.stdout, r.stderr[-1000:]


def run_pass(stage: str, which: str, nids: list[str], first: dict | None = None):
    key = json.loads((review_dir(stage) / "key.json").read_text())
    who = cfg()["reviewer" if which == "pass1" else "adjudicator"]
    odir = review_dir(stage) / which; odir.mkdir(parents=True, exist_ok=True)
    for nid in nids:
        if (odir / f"{nid}.json").exists(): continue
        case = find_case(key["items"][nid]["case"])
        cdir = Path(key["pack"]) / case["id"]
        files = [cdir / "rubric.md", cdir / "task.md", cdir / f"{nid}.md"]
        prompt = PASS1.format(nid=nid)
        if first is not None:
            (cdir / f"{nid}.first.jsonl").write_text("".join(json.dumps({"item": nid, **r}) + "\n" for r in first[nid]["lines"]))
            files.append(cdir / f"{nid}.first.jsonl"); prompt = PASS2.format(nid=nid)
        code, out, err = pi(who["model"], who["thinking"], cdir, files, prompt)
        (odir / f"{nid}.txt").write_text(out)
        lines, complete = parse_lines(out, nid, rubric_ids(case))
        (odir / f"{nid}.json").write_text(json.dumps({"item": nid, "model": who["model"], "thinking": who["thinking"], "exit": code,
                                                      "stderr": err, "complete": complete, "lines": lines}, indent=1))
        print(f"{which} {nid}: exit {code}, {len(lines)} lines, complete={complete}")


def load_pass(stage: str, which: str) -> dict:
    return {p.stem: json.loads(p.read_text()) for p in (review_dir(stage) / which).glob("*.json")}


def critical_fail(lines: list[dict]) -> bool:
    return any(r["result"] == "fail" and r.get("severity") == "critical" for r in lines)


def needs_adjudication(stage: str) -> list[str]:
    key = json.loads((review_dir(stage) / "key.json").read_text())
    first = load_pass(stage, "pass1")
    out = []
    for nid in key["order"]:
        p1 = first.get(nid)
        if p1 is None: continue
        disputed = not p1["complete"] or any(r["result"] == "unverified" for r in p1["lines"])
        if critical_fail(p1["lines"]) or disputed or nid in key["sample"]: out.append(nid)
    return out


def final_verdicts(stage: str) -> dict:
    """nid -> final review record: the adjudication when there is one, else the first pass."""
    return load_pass(stage, "pass1") | load_pass(stage, "pass2")


if __name__ == "__main__":
    if len(sys.argv) != 3: die(__doc__)
    cmd, stage = sys.argv[1:]
    if cmd == "pack": pack(stage)
    elif cmd == "review":
        run_pass(stage, "pass1", json.loads((review_dir(stage) / "key.json").read_text())["order"])
    elif cmd == "adjudicate":
        missing = set(json.loads((review_dir(stage) / "key.json").read_text())["order"]) - set(load_pass(stage, "pass1"))
        if missing: die(f"first pass incomplete: {len(missing)} items")
        run_pass(stage, "pass2", needs_adjudication(stage), first=load_pass(stage, "pass1"))
    else: die(__doc__)
