"""Grade every archived run with Jev (cached per question), then calibrate each check against the labels.

usage: TYPESAFE_API_KEY=... python3 -I calibrate.py [--dry-run | --report-only | --repeat] [--round NAME]
  --dry-run      ask stale questions only for DRY_RUNS (one per version), print tokens per run, write no report
  --report-only  no network; report on whatever is cached
  --repeat       ask the split questions (B2a/B2b/B6a/B6b) a second time for REPEAT_N fixed runs, then report
  --round NAME   tag stored with every new answer (default r1); the report compares question versions by tag
Each cache file keeps one hash per question; only questions whose hash changed are re-asked, and the
replaced answer moves to the file's `history`.
"""
import asyncio
import hashlib
import json
import os
import random
import sys
import time
from pathlib import Path
from typing import Any

EVAL = Path(__file__).resolve().parent
sys.dont_write_bytecode = True  # keep imports from writing __pycache__ beside validate_grade.py
sys.path[:0] = [str(EVAL), str(EVAL.parent)]
import jev_grade  # noqa: E402
from labels import RUNS, VERSIONS, load_labels  # noqa: E402
from lint import case_task, lint  # noqa: E402

CACHE = EVAL / "cache"
TOKEN_BUDGET = 5_000_000  # cumulative over every request ever logged in the cache
USD_PER_M_INPUT = 0.042
CONCURRENCY = 8
CHARS_PER_TOKEN = 3.5  # observed billing is ~0.71x of (state + questions) chars / 3.5, so this over-estimates
BAND = (0.3, 0.7)
MIN_FAILS = 5
READY_BA, CLOSE_BA = 0.85, 0.75
REPEAT_N, REPEAT_SEED = 40, 20261018
DRY_RUNS = (("v2", "T02-claude-1"), ("v3", "T05-pi-1"), ("v4", "T08-claude-1"), ("v5", "T11-pi-1"), ("v6", "T04-claude-2"), ("v7", "T03-pi-1"))
# frozen-rubric drift: v2's T4a required an unchanged return; the questions use the current rubric
DRIFT = frozenset({("v2", "T4a")})
SPLITS = jev_grade.SPLITS
SUBS = tuple(s for subs in SPLITS.values() for s in subs)

Run = tuple[str, str]
Item = tuple[Run, float, bool]


def all_runs() -> list[Run]:
    return [(v, p.stem) for v in VERSIONS for p in sorted((RUNS / v).glob("T*.md"))]


def case_of(run: str) -> str:
    return run.split("-")[0]


def reply_of(key: Run) -> str:
    return (RUNS / key[0] / f"{key[1]}.md").read_text(encoding="utf-8")


def qhash(question: dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(question, sort_keys=True).encode()).hexdigest()[:16]


def cache_path(key: Run) -> Path:
    return CACHE / key[0] / f"{key[1]}.json"


def load_record(key: Run) -> dict[str, Any] | None:
    path = cache_path(key)
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def stale_checks(key: Run, rec: dict[str, Any] | None) -> list[str]:
    qs = jev_grade.build_questions(case_of(key[1]))
    have = (rec or {}).get("qhashes", {})
    return [c for c, question in qs.items() if have.get(c) != qhash(question)]


def fresh(key: Run, rec: dict[str, Any]) -> dict[str, float]:
    stale = set(stale_checks(key, rec))
    return {c: p for c, p in rec["jev"].items() if c in jev_grade.build_questions(case_of(key[1])) and c not in stale}


def raw_estimate(key: Run, checks: list[str]) -> float:
    case = case_of(key[1])
    qs = {c: v for c, v in jev_grade.build_questions(case).items() if c in checks}
    state_chars, q_chars = jev_grade.request_chars(jev_grade.build_state(case, case_task(case), reply_of(key)), qs)
    return (state_chars + q_chars) / CHARS_PER_TOKEN


def spent_tokens(records: dict[Run, dict[str, Any]]) -> int:
    return sum(r["input_tokens"] for rec in records.values() for r in rec["requests"])


def merge(rec: dict[str, Any] | None, key: Run, out: dict[str, Any], hashes: dict[str, str], rnd: str, request: dict[str, Any], repeat: bool) -> dict[str, Any]:
    """Fold one Jev answer into a cache record; replaced or obsolete answers move to history."""
    rec = rec or {"version": key[0], "run": key[1], "model": out["model"], "jev": {}, "qhashes": {}, "rounds": {}, "requests": [], "history": []}
    rec.setdefault("rounds", {})
    rec["requests"].append(request)
    if repeat:
        rec.setdefault("repeats", []).append({"round": rnd, "qhashes": hashes, "jev": out["jev"]})
        return rec
    current = jev_grade.build_questions(case_of(key[1]))
    for c in [c for c in rec["jev"] if c in out["jev"] or c not in current]:
        rec["history"].append({"check": c, "qhash": rec["qhashes"].get(c), "round": rec["rounds"].get(c, "v1"), "p": rec["jev"].pop(c)})
        rec["qhashes"].pop(c, None)
        rec["rounds"].pop(c, None)
    rec["jev"] |= out["jev"]
    rec["qhashes"] |= hashes
    rec["rounds"] |= {c: rnd for c in out["jev"]}
    rec["model"] = out["model"]
    return rec


async def grade_one(client: Any, sem: asyncio.Semaphore, key: Run, checks: list[str], rnd: str, repeat: bool) -> dict[str, Any]:
    case = case_of(key[1])
    qs = jev_grade.build_questions(case)
    async with sem:
        start = time.monotonic()
        try:
            out = await jev_grade.ask(client, case, case_task(case), reply_of(key), only=checks)
        except Exception as e:  # noqa: BLE001 - one failed run must not stop the batch
            return {"error": f"{type(e).__name__} status={getattr(e, 'status', None)}"}
    request = {"checks": sorted(checks), "input_tokens": out["input_tokens"], "raw_estimate": round(raw_estimate(key, checks)),
               "elapsed_s": round(time.monotonic() - start, 2), "model": out["model"], "round": rnd, "repeat": repeat}
    rec = merge(load_record(key), key, out, {c: qhash(qs[c]) for c in checks}, rnd, request, repeat)
    cache_path(key).parent.mkdir(parents=True, exist_ok=True)
    cache_path(key).write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")
    return rec


async def grade_all(todo: list[tuple[Run, list[str]]], rnd: str, repeat: bool) -> tuple[dict[Run, dict[str, Any]], list[str]]:
    sem = asyncio.Semaphore(CONCURRENCY)
    async with jev_grade.make_client() as client:
        results = await asyncio.gather(*(grade_one(client, sem, k, c, rnd, repeat) for k, c in todo))
    done = {k: r for (k, _), r in zip(todo, results) if "error" not in r}
    errors = [f"{k[0]}/{k[1]}: {r['error']}" for (k, _), r in zip(todo, results) if "error" in r]
    return done, errors


def auc(pairs: list[tuple[float, bool]]) -> float | None:
    pos = [p for p, fail in pairs if fail]
    neg = [p for p, fail in pairs if not fail]
    if not pos or not neg:
        return None
    wins = sum((p > n) + 0.5 * (p == n) for p in pos for n in neg)
    return wins / (len(pos) * len(neg))


def confusion(pairs: list[tuple[float, bool]], t: float) -> dict[str, int]:
    return {
        "tp": sum(p >= t and f for p, f in pairs),
        "fn": sum(p < t and f for p, f in pairs),
        "fp": sum(p >= t and not f for p, f in pairs),
        "tn": sum(p < t and not f for p, f in pairs),
    }


def balanced_accuracy(c: dict[str, int]) -> float | None:
    pos, neg = c["tp"] + c["fn"], c["fp"] + c["tn"]
    return None if not pos or not neg else (c["tp"] / pos + c["tn"] / neg) / 2


def best_threshold(pairs: list[tuple[float, bool]]) -> float:
    """Max balanced accuracy over observed cut points; ties go to the cut nearest 0.5. One class only: 0.5."""
    candidates = sorted({p for p, _ in pairs} | {0.5})
    scored = [(balanced_accuracy(confusion(pairs, t)), t) for t in candidates]
    scored = [(ba, t) for ba, t in scored if ba is not None]
    if not scored:
        return 0.5
    top = max(ba for ba, _ in scored)
    return min((t for ba, t in scored if ba == top), key=lambda t: (abs(t - 0.5), t))


def scores(c: dict[str, int], n: int) -> dict[str, Any]:
    return {"balanced_accuracy": balanced_accuracy(c), "accuracy": (c["tp"] + c["tn"]) / n if n else None, "false_pass": c["fn"], "false_fail": c["fp"]}


def held_out(items: list[Item]) -> dict[str, Any]:
    """Leave one version out: pick the threshold on the other versions, score the held-out version, pool the confusions."""
    pooled = {"tp": 0, "fn": 0, "fp": 0, "tn": 0}
    per_version = {}
    for v in sorted({k[0] for k, _, _ in items}):
        train = [(p, f) for k, p, f in items if k[0] != v]
        test = [(p, f) for k, p, f in items if k[0] == v]
        t = best_threshold(train)
        c = confusion(test, t)
        pooled = {x: pooled[x] + c[x] for x in pooled}
        per_version[v] = {"n": len(test), "fails": sum(f for _, f in test), "threshold": t, "auc": auc(test), "balanced_accuracy": balanced_accuracy(c)}
    return {**scores(pooled, len(items)), "per_version": per_version}


def check_metrics(items: list[Item]) -> dict[str, Any]:
    pairs = [(p, f) for _, p, f in items]
    t = best_threshold(pairs)
    fails = sum(f for _, f in pairs)
    return {
        "n": len(pairs),
        "fails": fails,
        "auc": auc(pairs),
        "threshold": t,
        "in_sample": scores(confusion(pairs, t), len(pairs)),
        "held_out": held_out(items),
        "uncertain": sum(BAND[0] <= p <= BAND[1] for p, _ in pairs),
    }


def status(m: dict[str, Any]) -> str:
    ba = m["held_out"]["balanced_accuracy"]
    if m["fails"] < MIN_FAILS:
        return "too few fails to measure"
    return "ready" if ba >= READY_BA else "close" if ba >= CLOSE_BA else "not usable"


def combined(p: dict[str, float]) -> dict[str, float]:
    """Rubric-check probabilities: a split check takes the max of its parts (fails if either part is over the shared threshold)."""
    out = {c: v for c, v in p.items() if c not in SUBS}
    out |= {c: max(p[s] for s in subs) for c, subs in SPLITS.items() if all(s in p for s in subs)}
    return out


def label_for(row: str) -> str:
    """Row name -> the rubric label it is scored against: 'B2a' -> 'B2', 'B6@v1' -> 'B6'."""
    base = row.split("@")[0]
    return next((c for c, subs in SPLITS.items() if base in subs), base)


def rows_of(rec: dict[str, Any], key: Run) -> dict[str, float]:
    """Every scored row for one run: current checks, the split parts, and earlier question versions from history (row@round)."""
    now = fresh(key, rec)
    rows = combined(now) | {s: now[s] for s in SUBS if s in now}
    by_round: dict[str, dict[str, float]] = {}
    for h in rec.get("history", []):
        if label_for(h["check"]) in SPLITS:
            by_round.setdefault(h["round"], {})[h["check"]] = h["p"]
    for rnd, old in by_round.items():
        for c, subs in SPLITS.items():
            if c in old:  # the single question that preceded the split
                rows[f"{c}@{rnd}"] = old[c]
            elif any(s in old for s in subs) and all(s in old or s in now for s in subs):
                rows[f"{c}@{rnd}"] = max(old.get(s, now.get(s)) for s in subs)  # a part not re-asked later kept its answer
        rows |= {f"{s}@{rnd}": v for s, v in old.items() if s in SUBS}
    return rows


def items_by_row(labels: dict[Run, dict[str, str]], jev: dict[Run, dict[str, Any]]) -> dict[str, list[Item]]:
    out: dict[str, list[Item]] = {}
    for key, rec in jev.items():
        for row, p in rows_of(rec, key).items():
            check = label_for(row)
            label = labels[key].get(check)
            if label in ("pass", "fail") and (key[0], check) not in DRIFT:
                out.setdefault(row, []).append((key, p, label == "fail"))
    return out


def fmt(x: float | None, digits: int = 2) -> str:
    return "n/a" if x is None else f"{x:.{digits}f}"


def row_order(row: str) -> tuple[int, int, int, str]:
    check = label_for(row)
    return (0 if check.startswith("B") else 1, int("".join(ch for ch in check[1:] if ch.isdigit())), row != check, row)


def is_component(row: str) -> bool:
    return row != label_for(row)


def calibration_section(by_row: dict[str, list[Item]]) -> tuple[list[str], list[str], dict[str, dict[str, Any]]]:
    head = ("| check | n | fails | AUC | thr (all) | in-sample bal. acc | in-sample acc | in-sample false-pass | in-sample false-fail | "
            "held-out bal. acc | held-out acc | held-out false-pass | held-out false-fail | uncertain 0.3-0.7 | status |")
    rows = [head, "|" + "---|" * 15]
    per_v = ["| check | " + " | ".join(VERSIONS) + " |", "|" + "---|" * (len(VERSIONS) + 1)]
    metrics: dict[str, dict[str, Any]] = {}
    for row in sorted(by_row, key=row_order):
        m = metrics[row] = check_metrics(by_row[row])
        i, h = m["in_sample"], m["held_out"]
        st = "earlier wording" if "@" in row else "component of " + label_for(row) if is_component(row) else status(m)
        rows.append(
            f"| {row} | {m['n']} | {m['fails']} | {fmt(m['auc'])} | {m['threshold']:.3f} | {fmt(i['balanced_accuracy'])} | {fmt(i['accuracy'])} | "
            f"{i['false_pass']} | {i['false_fail']} | {fmt(h['balanced_accuracy'])} | {fmt(h['accuracy'])} | {h['false_pass']} | {h['false_fail']} | "
            f"{m['uncertain']} | {st} |"
        )
        if m["fails"]:
            cells = [h["per_version"].get(v) for v in VERSIONS]
            per_v.append(f"| {row} | " + " | ".join("-" if c is None else f"{fmt(c['auc'])} / {c['threshold']:.2f} ({c['fails']}/{c['n']})" for c in cells) + " |")
    return rows, per_v, metrics


def disagreements(by_row: dict[str, list[Item]], jev: dict[Run, dict[str, Any]]) -> list[dict[str, Any]]:
    """Rubric checks only, judged at the held-out threshold for the run's version."""
    out = []
    for row, items in by_row.items():
        if is_component(row) or "@" in row:
            continue
        per_version = held_out(items)["per_version"]
        for key, p, fail in items:
            t = per_version[key[0]]["threshold"]
            says_fail = p >= t
            if says_fail != fail:
                d = {"version": key[0], "run": key[1], "check": row, "label": "fail" if fail else "pass", "jev_says": "fail" if says_fail else "pass",
                     "p_defect": round(p, 4), "threshold": t, "confidence": round(p if says_fail else 1 - p, 4)}
                if row in SPLITS:
                    now = fresh(key, jev[key])
                    d["parts"] = {s: now[s] for s in SPLITS[row]}
                out.append(d)
    return sorted(out, key=lambda d: -d["confidence"])


def repeat_sample(labels: dict[Run, dict[str, str]]) -> list[Run]:
    """Fixed sample, half labelled fail on B2 or B6, half labelled pass on both."""
    graded = [k for k in all_runs() if all(labels[k].get(c) in ("pass", "fail") for c in SPLITS)]
    fails = [k for k in graded if any(labels[k][c] == "fail" for c in SPLITS)]
    passes = [k for k in graded if k not in fails]
    rng = random.Random(REPEAT_SEED)
    return sorted(rng.sample(fails, REPEAT_N // 2) + rng.sample(passes, REPEAT_N // 2))


def repeat_section(jev: dict[Run, dict[str, Any]], labels: dict[Run, dict[str, str]], metrics: dict[str, dict[str, Any]]) -> list[str]:
    diffs: dict[str, list[float]] = {}
    flips: dict[str, int] = {}
    runs = 0
    for key in repeat_sample(labels):
        rec = jev.get(key)
        now = fresh(key, rec) if rec else {}
        again = next((r["jev"] for r in reversed(rec.get("repeats", [])) if all(now.get(s) is not None and r["qhashes"].get(s) == rec["qhashes"].get(s) for s in r["jev"])), None) if rec else None
        if not again or not all(s in again for s in SUBS):
            continue
        runs += 1
        a, b = combined({s: now[s] for s in SUBS}), combined(again)
        for row, (x, y) in {**{s: (now[s], again[s]) for s in SUBS}, **{c: (a[c], b[c]) for c in SPLITS}}.items():
            diffs.setdefault(row, []).append(abs(x - y))
            if row in metrics and not is_component(row):
                t = metrics[row]["threshold"]
                flips[row] = flips.get(row, 0) + ((x >= t) != (y >= t))
    if not runs:
        return ["## Repeatability", "", "Not run yet (`--repeat`)."]
    out = ["## Repeatability", "", f"Same question, same run, asked twice; {runs} runs (seed {REPEAT_SEED}, half labelled fail on B2 or B6, half pass on both).",
           "Flips count verdict changes at the all-labels threshold.", "", "| question | mean abs change | max abs change | verdict flips |", "|---|---|---|---|"]
    for row in sorted(diffs, key=row_order):
        out.append(f"| {row} | {sum(diffs[row]) / len(diffs[row]):.3f} | {max(diffs[row]):.3f} | {flips.get(row, '-')} |")
    return out


def lint_section(labels: dict[Run, dict[str, str]]) -> list[str]:
    pairs = {"B4 vs L1": ("B4", "L1", None), "T10a vs L5": ("T10a", "L5", "T10"), "T1a vs L3": ("T1a", "L3", "T1"), "B2 vs L3 (T1)": ("B2", "L3", "T1"),
             "T5a vs L3": ("T5a", "L3", "T5"), "B2 vs L3 (T5)": ("B2", "L3", "T5"), "T11b vs L6": ("T11b", "L6", "T11")}
    v7 = [k for k in all_runs() if k[0] == "v7"]
    results = {k: lint(case_of(k[1]), reply_of(k), case_task(case_of(k[1]))) for k in v7}
    out = ["## Lint vs v7 labels", "", "Counts are label/lint status pairs over the 66 v7 runs (na pairs dropped).", "", "| comparison | agree | label pass, lint fail | label fail, lint pass | other |", "|---|---|---|---|---|"]
    detail: list[str] = []
    for name, (check, lcheck, only) in pairs.items():
        agree = lf = fl = other = 0
        for k in v7:
            case = "T" + str(int(case_of(k[1])[1:]))
            if only and case != only:
                continue
            label, ls = labels[k].get(check), results[k][lcheck]["status"]
            if label in (None, "na") or ls == "na":
                continue
            if label == ls:
                agree += 1
            elif label == "pass" and ls == "fail":
                lf += 1
                detail.append(f"- {name} `{k[1]}`: label pass, lint fail: {results[k][lcheck]['quote'][:110]}")
            elif label == "fail" and ls == "pass":
                fl += 1
                detail.append(f"- {name} `{k[1]}`: label fail, lint pass: {results[k][lcheck]['quote'][:110]}")
            else:
                other += 1
        out.append(f"| {name} | {agree} | {lf} | {fl} | {other} |")
    t11 = [f"`{k[1]}` {results[k]['L6']['status']} ({results[k]['L6']['quote'].split(':')[0]})" for k in v7 if case_of(k[1]) == "T11"]
    out += ["", "T11 parsed LCP targets (L6 passes only below 2.5 s): " + ", ".join(t11), ""]
    for lcheck in ("L2", "L4", "L7"):
        counts: dict[str, int] = {}
        for k in v7:
            counts[results[k][lcheck]["status"]] = counts.get(results[k][lcheck]["status"], 0) + 1
        out.append(f"- {lcheck} statuses over v7: " + ", ".join(f"{s} {n}" for s, n in sorted(counts.items())))
    flags = [f"  - `{k[1]}`: {results[k]['L7']['quote'][:200]}" for k in v7 if results[k]["L7"]["status"] == "flag"]
    out += ["- L7 review hints (approval lines sharing words with a prohibition):", *(flags or ["  - none"]), "", "Disagreement detail:", *(detail or ["- none"])]
    return out


HOW_TO_READ = [
    "## How to read this report",
    "",
    "- Trust the held-out columns. For each check and each version v, the threshold is chosen on the other 5 versions (max balanced accuracy,",
    "  ties nearest 0.5) and only then applied to v; the 6 held-out confusions are pooled. The in-sample columns fit and score on the same labels",
    "  and are kept only to show the gap; a large gap means the threshold does not transfer across skill versions.",
    "- AUC needs no threshold, so it is computed on all labels; the per-version table shows held-out AUC / chosen threshold (fails/n) per version.",
    f"- status: ready = held-out balanced accuracy >= {READY_BA} with >= {MIN_FAILS} fails; close = >= {CLOSE_BA}; not usable = below; "
    f"fewer than {MIN_FAILS} fail labels = too few fails to measure (its numbers are noise).",
    "- `thr (all)` is the threshold fitted on all labels: the one to use going forward. p >= threshold means Jev says fail.",
    "- B2 and B6 are each graded by two Jev questions (B2a/B2b, B6a/B6b); the check's probability is the max of its parts, so it fails",
    "  when either part is over the shared threshold. Part rows are scored against the parent label and are diagnostic only.",
    "- `X@v1` rows are the previous single-question wording, `X@r1` rows an earlier round of the current wording, on the same labels.",
    "- false-pass = label fail, Jev pass. false-fail = label pass, Jev fail. uncertain = answers in 0.3..0.7.",
    "",
]


def write_report(jev: dict[Run, dict[str, Any]], labels: dict[Run, dict[str, str]], stats: dict[str, Any]) -> None:
    by_row = items_by_row(labels, jev)
    rows, per_v, metrics = calibration_section(by_row)
    dis = disagreements(by_row, jev)
    (EVAL / "disagreements.json").write_text(json.dumps(dis, indent=1) + "\n", encoding="utf-8")
    tokens = spent_tokens(jev)
    n_requests = sum(len(r["requests"]) for r in jev.values())
    by_round: dict[str, int] = {}
    for rec in jev.values():
        for r in rec["requests"]:
            name = r["round"] + (" repeat" if r.get("repeat") else "")
            by_round[name] = by_round.get(name, 0) + r["input_tokens"]
    complete = sum(not stale_checks(k, r) for k, r in jev.items())
    lines = [
        "# Jev calibration report",
        "",
        "Labels: recorded grades plus `overrides.json`. Probabilities are P(defect). Excluded as rubric drift: " + ", ".join(f"{v} {c}" for v, c in sorted(DRIFT)) + ".",
        "Previous report (single B2/B6 questions, in-sample numbers only): `calibration-report.v1.md`.",
        "",
        *HOW_TO_READ,
        "## Per-check calibration",
        "",
        *rows,
        "",
        "## Held-out per version (AUC / threshold chosen on the other versions (fails/n))",
        "",
        *per_v,
        "",
        *repeat_section(jev, labels, metrics),
        "",
        "## Totals",
        "",
        f"- runs with every current question answered: {complete} of {len(all_runs())}; Jev requests this invocation: {stats['sent']}; failed requests: {len(stats['errors'])}",
        f"- Jev requests logged in the cache: {n_requests}; input tokens: {tokens:,} (" + ", ".join(f"{k} {v:,}" for k, v in sorted(by_round.items())) + ")",
        f"- cost (all logged requests): ${tokens * USD_PER_M_INPUT / 1e6:.4f} at ${USD_PER_M_INPUT}/M input tokens; output free",
        f"- wall time this invocation: {stats['wall_s']:.1f} s",
        f"- disagreements at the held-out thresholds: {len(dis)} (see disagreements.json)",
        "",
        *lint_section(labels),
    ]
    (EVAL / "calibration-report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _selftest() -> None:
    pairs = [(0.9, True), (0.8, True), (0.4, False), (0.1, False)]
    assert auc(pairs) == 1.0 and auc([(0.5, True), (0.5, False)]) == 0.5 and auc([(0.2, False)]) is None
    t = best_threshold(pairs)
    assert 0.4 < t <= 0.8 and balanced_accuracy(confusion(pairs, t)) == 1.0, t
    assert best_threshold([(0.9, False), (0.1, False)]) == 0.5
    # held-out: v2's cut is learned on v3 (0.6), so v2's 0.55 fail becomes a false pass that in-sample fitting hides
    items = [(("v2", "a"), 0.55, True), (("v2", "b"), 0.2, False), (("v3", "c"), 0.6, True), (("v3", "d"), 0.58, False)]
    h = held_out(items)
    assert h["per_version"]["v2"]["threshold"] == 0.6 and h["false_pass"] == 1, h
    m = check_metrics(items)
    assert m["in_sample"]["balanced_accuracy"] > h["balanced_accuracy"] and m["fails"] == 2 and status(m) == "too few fails to measure", m
    assert combined({"B2a": 0.2, "B2b": 0.7, "B3": 0.1}) == {"B2": 0.7, "B3": 0.1}
    assert label_for("B6b") == "B6" and label_for("B2@v1") == "B2" and label_for("T5a") == "T5a"
    # merge: a re-asked answer replaces the current one and the old one moves to history; obsolete checks move too
    key = ("v7", "T05-x-1")
    rec = {"version": "v7", "run": "T05-x-1", "model": "m", "jev": {"B2": 0.4, "B3": 0.3}, "qhashes": {"B2": "old", "B3": "h3"}, "requests": [], "history": []}
    rec = merge(rec, key, {"jev": {"B3": 0.9, "B2a": 0.1}, "model": "m"}, {"B3": "n3", "B2a": "na"}, "r1", {"input_tokens": 5}, False)
    assert rec["jev"] == {"B3": 0.9, "B2a": 0.1} and rec["rounds"] == {"B3": "r1", "B2a": "r1"}, rec
    assert {(x["check"], x["round"], x["p"]) for x in rec["history"]} == {("B2", "v1", 0.4), ("B3", "v1", 0.3)}, rec["history"]
    rec = merge(rec, key, {"jev": {"B2a": 0.5}, "model": "m"}, {"B2a": "na"}, "r1", {"input_tokens": 3}, True)
    assert rec["jev"]["B2a"] == 0.1 and rec["repeats"][0]["jev"] == {"B2a": 0.5} and spent_tokens({key: rec}) == 8
    # stale detection: only the question whose hash changed is re-asked
    fake = {"qhashes": {c: qhash(v) for c, v in jev_grade.build_questions("T05").items()}}
    assert stale_checks(("v7", "T05-pi-1"), fake) == []
    fake["qhashes"]["B6a"] = "x"
    assert stale_checks(("v7", "T05-pi-1"), fake) == ["B6a"]
    # rows: the v1 single question stays its own row; a later round combines its re-asked part with the unchanged one
    now = {c: 0.1 for c in fake["qhashes"]} | {"B6a": 0.3, "B6b": 0.2}
    fake["qhashes"]["B6a"] = qhash(jev_grade.build_questions("T05")["B6a"])
    hist = [{"check": "B6", "round": "v1", "p": 0.8}, {"check": "B6a", "round": "r1", "p": 0.9}]
    rows = rows_of({**fake, "jev": now, "history": hist}, ("v7", "T05-pi-1"))
    assert rows["B6"] == 0.3 and rows["B6@v1"] == 0.8 and rows["B6@r1"] == 0.9 and rows["B6a@r1"] == 0.9 and "B2@v1" not in rows, rows
    print("selftest ok")


def main(argv: list[str]) -> int:
    if argv == ["--selftest"]:
        _selftest()
        return 0
    dry, report_only, repeat = "--dry-run" in argv, "--report-only" in argv, "--repeat" in argv
    rnd = argv[argv.index("--round") + 1] if "--round" in argv else "r1"
    labels, problems = load_labels()
    if problems:
        print("abort: override problems", *problems, sep="\n")
        return 2
    cached = {k: r for k in all_runs() if (r := load_record(k))}
    if repeat:
        todo = [(k, list(SUBS)) for k in repeat_sample(labels) if not stale_checks(k, cached.get(k)) and
                not any(all(r["qhashes"].get(s) == cached[k]["qhashes"].get(s) for s in SUBS) for r in cached[k].get("repeats", []))]
    else:
        wanted = list(DRY_RUNS) if dry else all_runs()
        todo = [] if report_only else [(k, s) for k in wanted if (s := stale_checks(k, cached.get(k)))]
    est = sum(raw_estimate(k, c) for k, c in todo)
    spent = spent_tokens(cached)
    print(f"cached {len(cached)}, requests to send {len(todo)}, questions {sum(len(c) for _, c in todo)}, estimated {est:,.0f} tokens, already spent {spent:,}")
    if spent + est > TOKEN_BUDGET:
        print(f"abort: estimated total {spent + est:,.0f} exceeds {TOKEN_BUDGET:,} input tokens")
        return 2
    if todo and not os.environ.get("TYPESAFE_API_KEY"):
        print("abort: TYPESAFE_API_KEY is not set in this process")
        return 2
    start = time.monotonic()
    done, errors = asyncio.run(grade_all(todo, rnd, repeat)) if todo else ({}, [])
    wall = time.monotonic() - start
    for e in errors:
        print("ERROR", e)
    cached |= done
    if dry:
        for k, _ in todo:
            if k in done:
                r = done[k]["requests"][-1]
                print(f"{k[0]}/{k[1]}: {len(r['checks'])} questions, {r['input_tokens']:,} tokens, estimate {r['raw_estimate']:,}, {r['elapsed_s']} s, model {r['model']}")
        print(f"wall {wall:.1f} s")
        return 1 if errors else 0
    write_report(cached, labels, {"sent": len(todo), "errors": errors, "wall_s": wall})
    print(f"report written; {len(cached)} runs, wall {wall:.1f} s, errors {len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
