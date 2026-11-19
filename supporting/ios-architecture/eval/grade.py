"""Grade a run with the hidden grader, and run new scripts/check as a separate diagnostic (never part of the grade).
  python3 -I grade.py <run-dir>            grade (writes grade.json) and diagnose (writes diagnostic.json)
"""
import json, re, shutil, subprocess, sys, tarfile, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import OUT, SCRATCH, blocked_env, cfg, die, find_case, grading_simulator, run_grader

VIOLATION = re.compile(r"^(?P<file>[^:\s][^:]*):(?P<line>\d+): (?P<rule>[\w.-]+)(?::|$)")


def extract(rdir: Path, dest: Path) -> Path:
    shutil.rmtree(dest, ignore_errors=True); dest.mkdir(parents=True)
    with tarfile.open(rdir / "result.tgz") as tar: tar.extractall(dest, filter="tar")
    return dest / "work"


def acceptance(res: dict) -> tuple[bool, list[str]]:
    """Executable acceptance: no critical check fails and at least 1 critical check passes. A review case's grader checks its tree."""
    crit = [c for c in res["checks"] if c["critical"]]
    failed = [c["id"] for c in crit if c["result"] == "fail"]
    return (not failed and any(c["result"] == "pass" for c in crit)), failed


def grade_run(rdir: Path) -> dict:
    out = rdir / "grade.json"
    if out.exists(): return json.loads(out.read_text())
    meta = json.loads((rdir / "meta.json").read_text())
    case = find_case(meta["case"])
    g = SCRATCH / "g"
    work = extract(rdir, g)
    shutil.copy(rdir / "final.txt", g / "final.txt")
    t0 = time.monotonic()
    try:
        with grading_simulator(case) as udid:
            t0 = time.monotonic()  # the grade itself, not the wait in the queue
            res, err = run_grader(case, work, g / "grade-out.json", g / "final.txt", udid, cfg()["caps"]["grade_s"], meta.get("variant"))
    except (subprocess.CalledProcessError, OSError) as e:
        res, err = None, f"simulator: {e}"
    rec = {"result": res, "error": err, "grade_s": round(time.monotonic() - t0, 1)}
    if res:
        rec["accepted_exec"], rec["critical_failed"] = acceptance(res)
    out.write_text(json.dumps(rec, indent=1))
    shutil.rmtree(g, ignore_errors=True)
    return rec


def parse_check(text: str) -> dict:
    lines = text.splitlines()
    return {"violations": [ln for ln in lines if VIOLATION.match(ln) and not ln.startswith("suppressed:")],
            "pending": [ln for ln in lines if ": pending: " in ln or ln.startswith("pending: ")],
            "suppressed": [ln for ln in lines if ln.startswith("suppressed: ")],
            "summary": next((ln for ln in reversed(lines) if ln.startswith("check: ")), None)}


def run_check(script: Path, work: Path, files=(), timeout=600) -> dict:
    """scripts/check, offline: no key, no Keychain item, curl blocked; pending decisions stay pending."""
    try:
        r = subprocess.run([str(script), str(work), *files], capture_output=True, text=True, timeout=timeout,
                           env=blocked_env(SCRATCH / "dbin"), cwd=work)
    except subprocess.TimeoutExpired:
        return {"exit": None, "error": "timeout"}
    return {"exit": r.returncode, **parse_check(r.stdout), "stderr": r.stderr[-1000:]}


def diagnose(rdir: Path) -> dict:
    out = rdir / "diagnostic.json"
    if out.exists(): return json.loads(out.read_text())
    meta = json.loads((rdir / "meta.json").read_text())
    script = OUT / "arms" / "new" / "ios-architecture" / "scripts" / "check"
    work = extract(rdir, SCRATCH / "d")
    rec = {"note": "diagnostic only, never part of the grade", "check": str(script)}
    if not script.exists(): rec["error"] = "frozen new arm has no scripts/check"
    else:
        rec["project"] = run_check(script, work)
        if meta.get("files_changed"): rec["files"] = run_check(script, work, meta["files_changed"])
    out.write_text(json.dumps(rec, indent=1))
    shutil.rmtree(SCRATCH / "d", ignore_errors=True)
    return rec


if __name__ == "__main__":
    if len(sys.argv) != 2: die(__doc__)
    r = Path(sys.argv[1]).resolve()
    print(json.dumps({"grade": grade_run(r), "diagnostic_exit": diagnose(r).get("project", {}).get("exit")}, indent=1))
