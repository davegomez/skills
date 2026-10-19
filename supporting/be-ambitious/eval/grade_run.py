"""Grade one batch with lint and Jev; route every Jev fail and lint hint to blind review.

usage: TYPESAFE_API_KEY=... python3 -I grade_run.py <version> [--dry-run]
       python3 -I grade_run.py --selftest                                  offline, fake Jev answers
Jev answers are cached per run and question hash in runs/<version>/jev/; a rerun asks only missing or changed
questions. Writes runs/<version>/grades-auto.json and runs/<version>/review-queue.json.
A question whose hash is not in the archive cache (eval/cache/) is uncalibrated: threshold 0.5.
"""
import asyncio
import json
import os
import re
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

EVAL = Path(__file__).resolve().parent
sys.dont_write_bytecode = True  # keep imports from writing __pycache__ beside validate_grade.py
sys.path[:0] = [str(EVAL), str(EVAL.parent)]
import calibrate  # noqa: E402
import jev_grade  # noqa: E402
from lint import case_id, case_task, lint  # noqa: E402

RUNS = EVAL.parent / "runs"
REPORT = EVAL / "calibration-report.md"
UNCALIBRATED = 0.5
ROUND = "auto"
CASES = tuple(f"T{i}" for i in range(1, 14))
# deterministic lint failures -> the rubric checks they fail ({c} is the case, e.g. L6 -> T11b)
LINT_FAIL = {"L1": ("B4",), "L3": ("B2", "{c}a"), "L4": ("B8",), "L5": ("B8", "T10a"), "L6": ("{c}b",)}
LINT_FLAG = {"L7": "B6", "L8": "B3"}  # review hints, never a fail
RANK = {"pass": 0, "review": 1, "fail": 2}

Hashes = dict[str, set[str]]


def report_thresholds(text: str) -> dict[str, float]:
    """`thr (all)` per row of the report's per-check table."""
    out, inside = {}, False
    for line in text.splitlines():
        if line.startswith("## "):
            inside = line == "## Per-check calibration"
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if inside and len(cells) == 15 and re.fullmatch(r"[BT]\d+[a-z]?", cells[0]):
            out[cells[0]] = float(cells[4])
    return out


def archive_hashes(cache: Path = calibrate.CACHE) -> Hashes:
    out: Hashes = {}
    for path in cache.glob("*/*.json"):
        for check, h in json.loads(path.read_text(encoding="utf-8"))["qhashes"].items():
            out.setdefault(check, set()).add(h)
    return out


def calibrated(case: str, question: str, archive: Hashes) -> bool:
    return calibrate.qhash(jev_grade.build_questions(case)[question]) in archive.get(question, set())


def changed_questions(archive: Hashes) -> list[str]:
    return sorted({qn for c in CASES for qn in jev_grade.build_questions(c) if not calibrated(c, qn, archive)}, key=calibrate.row_order)


def threshold(case: str, check: str, thresholds: dict[str, float], archive: Hashes) -> tuple[float, bool]:
    """A rubric check keeps its calibrated threshold only while every question that grades it is unchanged."""
    parts = jev_grade.SPLITS.get(check, (check,))
    if check in thresholds and all(calibrated(case, s, archive) for s in parts):
        return thresholds[check], True
    return UNCALIBRATED, False


def task_for(run_dir: Path, case: str) -> str:
    frozen = run_dir / "frozen" / "cases" / f"T{int(case_id(case)[1:]):02d}.txt"
    return frozen.read_text(encoding="utf-8") if frozen.exists() else case_task(case)


def entry(checks: dict[str, dict[str, Any]], check: str) -> dict[str, Any]:
    return checks.setdefault(check, {"p": None, "threshold": None, "calibrated": None, "lint": [], "source": "", "verdict": "pass"})


def raise_to(e: dict[str, Any], verdict: str, source: str) -> None:
    if RANK[verdict] > RANK[e["verdict"]]:
        e["verdict"], e["source"] = verdict, source


def grade_one(case: str, jev: dict[str, float], lint_out: dict[str, dict[str, str]], thresholds: dict[str, float], archive: Hashes) -> dict[str, dict[str, Any]]:
    c = case_id(case)
    checks: dict[str, dict[str, Any]] = {}
    for check, p in calibrate.combined(jev).items():
        e = entry(checks, check)
        t, cal = threshold(c, check, thresholds, archive)
        e |= {"p": p, "threshold": t, "calibrated": cal, "source": "jev" if cal else "jev (uncalibrated)"}
        if check in jev_grade.SPLITS:
            e["parts"] = {s: jev[s] for s in jev_grade.SPLITS[check]}
        if p >= t:
            e["verdict"] = "review"
    for lid, res in lint_out.items():
        if res["status"] == "flag" and lid in LINT_FLAG:
            e = entry(checks, LINT_FLAG[lid])
            e["lint"].append({"id": lid, **res})
            raise_to(e, "review", f"lint {lid} flag")
        elif lid in LINT_FAIL and res["status"] in ("pass", "fail"):
            for check in (x.format(c=c) for x in LINT_FAIL[lid]):
                e = entry(checks, check)
                e["lint"].append({"id": lid, **res})
                e["source"] = e["source"] or f"lint {lid}"
                if res["status"] == "fail":
                    raise_to(e, "fail", f"lint {lid}")
    return checks


def reason(e: dict[str, Any]) -> str:
    parts = []
    if e["p"] is not None and e["p"] >= e["threshold"]:
        parts.append(f"jev p={e['p']:.2f} >= {e['threshold']:g}" + ("" if e["calibrated"] else " (uncalibrated)"))
    parts += [f"{x['id']} flag: {x['quote'][:160]}" for x in e["lint"] if x["status"] == "flag"]
    return "; ".join(parts)


def run_verdict(checks: dict[str, dict[str, Any]]) -> str:
    return max((e["verdict"] for e in checks.values()), key=RANK.get, default="pass")


def build_outputs(runs: dict[str, dict[str, Any]]) -> tuple[dict[str, Any], list[dict[str, str]]]:
    """runs: run id -> {case, checks}. Returns grades-auto.json and review-queue.json contents."""
    grades = {r: {"case": v["case"], "model": r.split("-")[1], "verdict": run_verdict(v["checks"]), "checks": v["checks"]} for r, v in sorted(runs.items())}
    queue = [{"run": r, "check": c, "reason": reason(e)} for r, g in grades.items() for c, e in sorted(g["checks"].items(), key=lambda x: calibrate.row_order(x[0])) if e["verdict"] == "review"]
    return grades, queue


def table(grades: dict[str, Any]) -> list[str]:
    models = sorted({g["model"] for g in grades.values()})
    cases = sorted({r.split("-")[0] for r in grades})
    out = ["pass/review/fail per case and model", "| case | " + " | ".join(models) + " |", "|---|" + "---|" * len(models)]
    for c in cases:
        cells = []
        for m in models:
            vs = [g["verdict"] for r, g in grades.items() if r.split("-")[0] == c and g["model"] == m]
            cells.append("/".join(str(vs.count(v)) for v in ("pass", "review", "fail")) if vs else "-")
        out.append(f"| {c} | " + " | ".join(cells) + " |")
    return out


def cache_file(run_dir: Path, run: str) -> Path:
    return run_dir / "jev" / f"{run}.json"


def load(path: Path) -> dict[str, Any] | None:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


DELETED_TOKENS = 294_333  # runs/v8/jev, deleted 2026-10-19; still counts against the guard


def spent_all() -> int:
    """Cumulative input tokens over the archive cache, every batch cache, and deleted batches."""
    recs = [load(p) for p in [*calibrate.CACHE.glob("*/*.json"), *RUNS.glob("*/jev/*.json")]]
    return DELETED_TOKENS + sum(r["input_tokens"] for rec in recs if rec for r in rec["requests"])


def estimate(case: str, task: str, reply: str, checks: list[str]) -> float:
    qs = {c: v for c, v in jev_grade.build_questions(case).items() if c in checks}
    s, q = jev_grade.request_chars(jev_grade.build_state(case, task, reply), qs)
    return (s + q) / calibrate.CHARS_PER_TOKEN


async def ask_all(todo: list[dict[str, Any]], version: str, run_dir: Path) -> list[str]:
    sem = asyncio.Semaphore(calibrate.CONCURRENCY)

    async def one(client: Any, it: dict[str, Any]) -> str | None:
        qs = jev_grade.build_questions(it["case"])
        async with sem:
            start = time.monotonic()
            try:
                out = await jev_grade.ask(client, it["case"], it["task"], it["reply"], only=it["stale"])
            except Exception as e:  # noqa: BLE001 - one failed run must not stop the batch; no message text, it may echo the request
                return f"{it['run']}: {type(e).__name__} status={getattr(e, 'status', None)}"
        request = {"checks": sorted(it["stale"]), "input_tokens": out["input_tokens"], "raw_estimate": round(it["estimate"]),
                   "elapsed_s": round(time.monotonic() - start, 2), "model": out["model"], "round": ROUND, "repeat": False}
        it["rec"] = calibrate.merge(it["rec"], (version, it["run"]), out, {c: calibrate.qhash(qs[c]) for c in it["stale"]}, ROUND, request, False)
        path = cache_file(run_dir, it["run"])
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(it["rec"], indent=1) + "\n", encoding="utf-8")
        return None

    async with jev_grade.make_client() as client:
        errors = await asyncio.gather(*(one(client, it) for it in todo))
    return [e for e in errors if e]


def plan(run_dir: Path, version: str) -> list[dict[str, Any]]:
    items = []
    for path in sorted(run_dir.glob("T*.md")):
        run, case = path.stem, case_id(path.stem.split("-")[0])
        task, reply = task_for(run_dir, case), path.read_text(encoding="utf-8")
        rec = load(cache_file(run_dir, run))
        stale = calibrate.stale_checks((version, run), rec)
        items.append({"run": run, "case": case, "task": task, "reply": reply, "rec": rec, "stale": stale,
                      "estimate": estimate(case, task, reply, stale) if stale else 0.0})
    return items


def finish(run_dir: Path, version: str, items: list[dict[str, Any]], thresholds: dict[str, float], archive: Hashes) -> tuple[dict[str, Any], list[dict[str, str]]]:
    runs = {}
    for it in items:
        jev = calibrate.fresh((version, it["run"]), it["rec"]) if it["rec"] else {}
        runs[it["run"]] = {"case": it["case"], "checks": grade_one(it["case"], jev, lint(it["case"], it["reply"], it["task"]), thresholds, archive)}
    grades, queue = build_outputs(runs)
    (run_dir / "grades-auto.json").write_text(json.dumps(grades, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    (run_dir / "review-queue.json").write_text(json.dumps(queue, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return grades, queue


def main(argv: list[str]) -> int:
    if argv == ["--selftest"]:
        _selftest()
        return 0
    if len(argv) not in (1, 2) or (len(argv) == 2 and argv[1] != "--dry-run") or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", argv[0]):
        print(__doc__)
        return 2
    version, dry = argv[0], len(argv) == 2
    run_dir = RUNS / version
    if not run_dir.is_dir():
        print(f"abort: no batch {run_dir}")
        return 2
    archive = archive_hashes()
    print("changed or new questions (uncalibrated, threshold 0.5): " + ", ".join(changed_questions(archive)))
    items = plan(run_dir, version)
    todo = [it for it in items if it["stale"]]
    counts: dict[str, int] = {}
    for it in todo:
        for c in it["stale"]:
            counts[c] = counts.get(c, 0) + 1
    est, spent = sum(it["estimate"] for it in todo), spent_all()
    print(f"runs {len(items)}, requests to send {len(todo)}, questions {sum(counts.values())}, estimated {est:,.0f} input tokens, already spent {spent:,}")
    print("questions to ask: " + (", ".join(f"{c} {n}" for c, n in sorted(counts.items(), key=lambda x: calibrate.row_order(x[0]))) or "none"))
    if dry:
        return 0
    if spent + est > calibrate.TOKEN_BUDGET:
        print(f"abort: estimated total {spent + est:,.0f} exceeds {calibrate.TOKEN_BUDGET:,} input tokens")
        return 2
    if todo and not os.environ.get("TYPESAFE_API_KEY"):
        print("abort: TYPESAFE_API_KEY is not set in this process")
        return 2
    errors = asyncio.run(ask_all(todo, version, run_dir)) if todo else []
    for e in errors:
        print("ERROR", e)
    grades, queue = finish(run_dir, version, items, report_thresholds(REPORT.read_text(encoding="utf-8")), archive)
    print(*table(grades), sep="\n")
    print(f"wrote grades-auto.json ({len(grades)} runs) and review-queue.json ({len(queue)} items); Jev errors {len(errors)}")
    return 1 if errors else 0


def _selftest() -> None:
    report = "## Per-check calibration\n\n| check | n | fails | AUC | thr (all) |" + " x |" * 10 + "\n" + "".join(
        f"| {c} | 1 | 1 | 0.9 | {t} |" + " x |" * 10 + "\n" for c, t in (("B2", 0.43), ("B3", 0.37), ("B6", 0.41), ("B6@r1", 0.1), ("T5b", 0.5))) + "\n## Held-out\n| B4 | 1 | 1 | 0.9 | 0.9 |" + " x |" * 10
    thr = report_thresholds(report)
    assert thr == {"B2": 0.43, "B3": 0.37, "B6": 0.41, "T5b": 0.5}, thr
    q5 = jev_grade.build_questions("T5")
    # archive: B6b, B3, T5b unchanged; B2a, B2b, B6a changed (absent); B7_REQUIRED known from T11
    archive = {c: {calibrate.qhash(q5[c])} for c in ("B3", "B6b", "T5b")} | {"B7": {calibrate.qhash(jev_grade.B7_REQUIRED)}}
    assert threshold("T5", "B3", thr, archive) == (0.37, True)
    assert threshold("T5", "B6", thr, archive) == (0.5, False), "a split check with a changed part is uncalibrated"
    assert threshold("T5", "T5a", thr, archive) == (0.5, False)
    assert calibrated("T13", "B7", archive) and not calibrated("T5", "B7", archive)
    changed = changed_questions(archive)
    assert "B2a" in changed and "T13a" in changed and "B3" not in changed and "T5b" not in changed, changed
    with tempfile.TemporaryDirectory() as tmp:
        run_dir = Path(tmp)
        csv_lost = "```text\nAnalyze.\nWith my approval only: share the codebook with a vendor to contact customers.\nJudge: an independent analyst checks traceability.\n```\n\n- `depth`: x\n"
        (run_dir / "T05-claude-1.md").write_text(csv_lost, encoding="utf-8")
        (run_dir / "T13-pi-1.md").write_text("```text\nSpeed it up.\nAim for 15 minutes using the critical path.\nJudge: before/after runtime.\n```\n", encoding="utf-8")
        (run_dir / "T13-claude-1.md").write_text("```text\nSpeed it up.\nAim for 2 hours using the critical path.\nJudge: before/after runtime.\n```\n", encoding="utf-8")
        assert [it["stale"] for it in plan(run_dir, "vself")][0] == list(q5), "no cache: every question is stale"
        fake = {"T05-claude-1": {c: 0.1 for c in q5} | {"B3": 0.2, "B6a": 0.6},
                "T13-pi-1": {c: 0.05 for c in jev_grade.build_questions("T13")},
                "T13-claude-1": {c: 0.05 for c in jev_grade.build_questions("T13")}}
        for run, answers in fake.items():
            qs = jev_grade.build_questions(run[:3])
            rec = calibrate.merge(None, ("vself", run), {"jev": answers, "model": "fake"}, {c: calibrate.qhash(qs[c]) for c in answers}, ROUND, {"input_tokens": 7}, False)
            (run_dir / "jev").mkdir(exist_ok=True)
            cache_file(run_dir, run).write_text(json.dumps(rec), encoding="utf-8")
        items = plan(run_dir, "vself")
        assert all(not it["stale"] for it in items), "a complete cache asks nothing"
        grades, queue = finish(run_dir, "vself", items, thr, archive)
        g5 = grades["T05-claude-1"]["checks"]
        assert g5["B6"]["verdict"] == "review" and g5["B6"]["threshold"] == 0.5 and g5["B6"]["parts"] == {"B6a": 0.6, "B6b": 0.1}, g5["B6"]
        assert g5["B3"]["verdict"] == "review" and g5["B3"]["source"] == "lint L8 flag", g5["B3"]  # p 0.2 < 0.37, L8 hint
        assert g5["B2"]["verdict"] == "fail" and g5["B2"]["source"] == "lint L3", g5["B2"]  # header literal missing
        assert g5["T5a"]["verdict"] == "fail" and g5["T5b"]["verdict"] == "pass" and g5["T5b"]["calibrated"] is True
        assert grades["T05-claude-1"]["verdict"] == "fail" and grades["T13-pi-1"]["verdict"] == "pass"
        assert grades["T13-claude-1"]["checks"]["T13b"]["verdict"] == "fail", grades["T13-claude-1"]["checks"]["T13b"]
        assert {(q["run"], q["check"]) for q in queue} == {("T05-claude-1", "B6"), ("T05-claude-1", "B3")}, queue
        b6 = next(q for q in queue if q["check"] == "B6")["reason"]
        assert b6.startswith("jev p=0.60 >= 0.5 (uncalibrated); L7 flag: ") and "contact" in b6, b6  # L7: approval line reuses a prohibition
        assert json.loads((run_dir / "review-queue.json").read_text()) == queue
        tab = table(grades)
        assert "| T05 | 0/0/1 | - |" in tab and "| T13 | 0/0/1 | 1/0/0 |" in tab, tab
        assert "TYPESAFE" not in (run_dir / "grades-auto.json").read_text()
    print("selftest ok")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
