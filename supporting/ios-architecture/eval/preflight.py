"""Preflight of a case folder (CASES.md): run it before the case is frozen.
  python3 -I preflight.py <case-dir> [<case-dir> ...]
1. The fixture alone fails a critical check.  2. The fixture plus the reference passes every check (na allowed).
3. Each negative fails the check its file name names.  4. 2 grades of the reference give the same results.
A review case (case.json "variants") runs every step on each variant, with the variant's own reference and negatives. A .patch is applied on top; a .md is the builder's final message (EVAL_FINAL_TEXT).
Each grade waits for the machine-wide grading queue and runs on its own new simulator. Exit 0 when every case passes every step.
"""
import json, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import OUT, SCRATCH, cfg, die, grading_simulator, is_review, load_case, lock, make_work, run_grader, variant_spec

PF = SCRATCH / "pf"


def grade_tree(case, variant=None, delivery: Path | None = None) -> tuple[dict | None, str, float]:
    """Grade the fixture (+ variant) + delivery. Returns (result, infrastructure error, grade seconds)."""
    work = PF / "w" / "work"
    patches = [delivery] if delivery and delivery.suffix == ".patch" else []
    try: make_work(case, work, variant, patches)
    except RuntimeError as e: return None, str(e), 0.0
    (PF / "final.txt").write_text(delivery.read_text() if delivery and delivery.suffix == ".md" else "")
    with grading_simulator(case) as udid:
        t0 = time.monotonic()
        res, err = run_grader(case, work, PF / "out.json", PF / "final.txt", udid, cfg()["caps"]["grade_s"], variant)
        return res, err, round(time.monotonic() - t0, 1)


def results(res) -> dict:
    return {c["id"]: c["result"] for c in res["checks"]} if res else {}


def preflight(case_dir: Path) -> dict:
    try: case = load_case(case_dir)
    except (OSError, ValueError) as e: return {"case": str(case_dir), "ok": False, "steps": [{"step": "case.json", "ok": False, "detail": str(e)}]}
    steps, d = [], case["dir"]

    def add(step, ok, detail, secs=None):
        steps.append({"step": step, "ok": bool(ok), "detail": detail, "grade_s": secs})

    for variant in (["seeded", "clean"] if is_review(case) else [None]):
        tag = f" ({variant})" if variant else ""
        res, err, secs = grade_tree(case, variant)
        crit_fail = [c["id"] for c in (res or {}).get("checks", []) if c["critical"] and c["result"] == "fail"]
        add(f"1 fixture fails a critical check{tag}", res and crit_fail, err or f"critical fails: {crit_fail or 'none'}", secs)
        spec = variant_spec(case, variant) if variant else {"reference": d / "reference.patch", "negatives": sorted((d / "negative").glob("*.patch"))}
        ref = spec["reference"]
        if not ref or not ref.exists():
            add(f"2 reference passes every check{tag}", False, f"no {ref.relative_to(d)}" if ref else "no reference in case.json")
        else:
            res, err, secs = grade_tree(case, variant, ref)
            failed = [k for k, v in results(res).items() if v == "fail"]
            add(f"2 reference passes every check{tag}", res and not failed,
                err or f"fails: {failed or 'none'}, na: {[k for k, v in results(res).items() if v == 'na']}", secs)
            again, err2, secs = grade_tree(case, variant, ref)
            same = results(res) == results(again)
            add(f"4 reference graded twice gives the same results{tag}", res and again and same,
                err2 or ("same" if same else f"differs: {sorted(k for k in results(res) if results(res)[k] != results(again).get(k))}"), secs)
        if not spec["negatives"]: add(f"3 negatives{tag}", False, "no negatives")
        for neg in spec["negatives"]:
            res, err, secs = grade_tree(case, variant, neg)
            got = results(res).get(neg.stem)
            add(f"3 negative {neg.relative_to(d)} fails {neg.stem}{tag}", got == "fail", err or f"{neg.stem}: {got or 'no such check'}", secs)
    return {"case": case["id"], "ok": all(s["ok"] for s in steps), "steps": steps}


if __name__ == "__main__":
    if len(sys.argv) < 2: die(__doc__)
    lock()
    reports = [preflight(Path(a).resolve()) for a in sys.argv[1:]]
    (OUT / "preflight").mkdir(parents=True, exist_ok=True)
    for r in reports:
        (OUT / "preflight" / f"{Path(r['case']).name}.json").write_text(json.dumps(r, indent=1))
        print(f"# {r['case']}: {'PASS' if r['ok'] else 'FAIL'}")
        for s in r["steps"]: print(f"  {'ok  ' if s['ok'] else 'FAIL'} {s['step']}: {s['detail']}" + (f" [{s['grade_s']} s]" if s["grade_s"] else ""))
    sys.exit(0 if all(r["ok"] for r in reports) else 1)
