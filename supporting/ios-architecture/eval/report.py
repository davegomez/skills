"""Stage report: per case, per priority, paired old/new acceptance with an exact sign test, the clean review stratum,
usage, invalid blocks, and the check diagnostic apart from the grade.
  python3 -I report.py <stage>                     writes runs/<stage>/report.md
  python3 -I report.py <stage> --old-from <other>  new runs of <stage>, old runs of <other>, paired by case and variant;
                                                   writes runs/<stage>/report-old-from-<other>.md
"""
import json, statistics, sys
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import OUT, cfg, die
import review


def sign_test(b: int, c: int) -> float:
    """Exact two-sided sign test on b and c discordant pairs."""
    n = b + c
    if n == 0: return 1.0
    return min(1.0, 2 * sum(comb(n, k) for k in range(min(b, c) + 1)) / 2 ** n)


def rows(stage: str) -> tuple[list[dict], list[dict]]:
    led = [json.loads(x) for x in (OUT / stage / "ledger.jsonl").read_text().splitlines()]
    key_p = review.review_dir(stage) / "key.json"
    nid_of = {v["run"]: k for k, v in json.loads(key_p.read_text())["items"].items()} if key_p.exists() else {}
    verdicts = review.final_verdicts(stage) if key_p.exists() else {}
    first = review.load_pass(stage, "pass1") if key_p.exists() else {}
    second = review.load_pass(stage, "pass2") if key_p.exists() else {}
    out = []
    for e in led:
        if e["kind"] != "unit" or e["status"] != "valid": continue
        for rid in e["runs"]:
            rdir = OUT / stage / "runs" / rid
            m, g = json.loads((rdir / "meta.json").read_text()), json.loads((rdir / "grade.json").read_text())
            d = json.loads((rdir / "diagnostic.json").read_text()) if (rdir / "diagnostic.json").exists() else {}
            v = verdicts.get(nid_of.get(rid))
            review_ok = None if v is None else not review.critical_fail(v["lines"])
            accepted = None if review_ok is None else bool(g.get("accepted_exec")) and review_ok
            p1 = first.get(nid_of.get(rid))
            out.append({"unit": e["unit"], "id": rid, "case": m["case"], "block": m["block"], "variant": m["variant"], "arm": m["arm"],
                        "accepted_exec": g.get("accepted_exec"), "review_ok": review_ok, "accepted": accepted,
                        "critical_failed": g.get("critical_failed", []) + ([f"review:{r['check']}" for r in v["lines"] if r["result"] == "fail" and r.get("severity") == "critical"] if v else []),
                        "checks": [(c["priority"], c["result"]) for c in g["result"]["checks"]] + ([(r.get("priority") or "unknown", r["result"]) for r in v["lines"]] if v else []),
                        "adjudicated": nid_of.get(rid) in second,
                        "disagree": bool(v and p1 and {r["check"]: r["result"] for r in v["lines"]} != {r["check"]: r["result"] for r in p1["lines"]}),
                        "cost": m.get("cost_usd"), "wall": m["wall_s"], "usage": m.get("usage") or {}, "jev": m.get("jev_calls", 0),
                        "jev_refused": m.get("jev_refused", 0), "pending": sum((m.get("pending_lines") or {}).values()),
                        "subagents": m.get("subagents_by_model") or {}, "stop": m["stop_reason"], "models": m.get("jev_models_observed", []),
                        "diag_violations": len((d.get("files") or d.get("project") or {}).get("violations", [])),
                        "diag_pending": len((d.get("files") or d.get("project") or {}).get("pending", []))})
    return out, led


def yn(x) -> str:
    return "pending review" if x is None else "yes" if x else "no"


def med(xs) -> str:
    xs = [x for x in xs if isinstance(x, (int, float))]
    return f"{statistics.median(xs):.2f}" if xs else "-"


def cross_rows(stage: str, other: str) -> list[dict]:
    """New runs of stage and old runs of other, each keyed by case and variant as 1 pair."""
    rs = [r for r in rows(stage)[0] if r["arm"] == "new"] + [r for r in rows(other)[0] if r["arm"] == "old"]
    for r in rs: r["unit"] = f"{r['case']}-{r['variant'] or '-'}"
    keys = [(r["unit"], r["arm"]) for r in rs]
    if len(set(keys)) != len(keys): die(f"more than 1 run per case, variant, and arm; --old-from pairs only 1 run per case")
    return rs


def inputs(stage: str) -> dict:
    p = OUT / stage / "plan.json"
    return json.loads(p.read_text())["inputs"] if p.exists() else {}


def report(stage: str, old_from: str | None = None) -> str:
    rs, led = rows(stage)
    if old_from: rs = cross_rows(stage, old_from)
    if not rs: die(f"no valid runs in {stage}")
    L = [f"# Report: {stage}" + (f", old runs from {old_from}" if old_from else ""), ""]
    if old_from:
        changed = sorted(k for k, v in inputs(stage).items() if inputs(old_from).get(k) != v)
        L += [f"Old runs come from stage {old_from} (runs/{old_from}); new runs come from stage {stage}. Each new run is paired with the old run "
              f"of the same case and variant. Spend and invalid blocks below are {stage}'s only.",
              cfg()["stages"].get(stage, {}).get("note", ""), f"Cases whose inputs differ between the 2 plans: {', '.join(changed) or 'none'}.", ""]
    L += ["Acceptance = every critical executable check passes or is na (at least 1 passes; a review case's grader checks that the tree holds only the review), "
         "and the final blind review reports no critical failure. The check diagnostic is listed apart and is never part of acceptance.", ""]
    # primary: paired old/new on non-clean blocks
    pairs = {}
    for r in rs:
        if r["arm"] in ("old", "new") and r["variant"] != "clean": pairs.setdefault(r["unit"], {})[r["arm"]] = r
    full = [p for p in pairs.values() if len(p) == 2]
    known = [p for p in full if p["old"]["accepted"] is not None and p["new"]["accepted"] is not None]
    b = sum(p["new"]["accepted"] and not p["old"]["accepted"] for p in known)
    c = sum(p["old"]["accepted"] and not p["new"]["accepted"] for p in known)
    both = sum(p["new"]["accepted"] and p["old"]["accepted"] for p in known)
    L += ["## Paired old/new acceptance (seeded and non-review blocks)", "",
          f"Pairs: {len(full)}, with both reviews done: {len(known)}. Both accepted: {both}. New only: {b}. Old only: {c}. Neither: {len(known) - both - b - c}.",
          f"Exact two-sided sign test on {b + c} discordant pairs: p = {sign_test(b, c):.4f}.", "",
          "| case | pairs | both | new only | old only | neither | p |", "| --- | --- | --- | --- | --- | --- | --- |"]
    for case in sorted({r["case"] for r in rs}):
        k = [p for p in known if p["old"]["case"] == case]
        cb = sum(p["new"]["accepted"] and not p["old"]["accepted"] for p in k); cc = sum(p["old"]["accepted"] and not p["new"]["accepted"] for p in k)
        cboth = sum(p["new"]["accepted"] and p["old"]["accepted"] for p in k)
        L.append(f"| {case} | {len(k)} | {cboth} | {cb} | {cc} | {len(k) - cboth - cb - cc} | {sign_test(cb, cc):.4f} |")
    # per case
    L += ["", "## Runs per case", ""]
    for case in sorted({r["case"] for r in rs}):
        L += [f"### {case}", "", "| run | arm | variant | exec | review | accepted | critical failed | $ | wall s | Jev calls | escalations | stop |",
              "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
        for r in sorted((r for r in rs if r["case"] == case), key=lambda r: (r["block"], r["arm"])):
            L.append(f"| {r['id']} | {r['arm']} | {r['variant'] or '-'} | {yn(r['accepted_exec'])} | {yn(r['review_ok'])} | {yn(r['accepted'])} | "
                     f"{', '.join(r['critical_failed']) or '-'} | {r['cost'] if r['cost'] is not None else 'unknown'} | {r['wall']} | {r['jev']} | {r['pending']} | {r['stop']} |")
        L.append("")
    # clean review stratum
    clean = [r for r in rs if r["variant"] == "clean"]
    L += ["## Clean-diff review stratum (descriptive, not in the paired test)", ""]
    if clean:
        L += ["| run | arm | accepted | failed checks |", "| --- | --- | --- | --- |"]
        L += [f"| {r['id']} | {r['arm']} | {yn(r['accepted'])} | {', '.join(r['critical_failed']) or '-'} |" for r in clean]
    else: L.append("No clean-diff runs.")
    # per priority
    L += ["", "## Per priority (executable checks and final review lines; pass / (pass + fail))", "", "| priority | " + " | ".join(a for a in ("old", "new", "none")) + " |", "| --- | --- | --- | --- |"]
    for pr in sorted({p for r in rs for p, _ in r["checks"]}):
        cells = []
        for arm in ("old", "new", "none"):
            res = [x for r in rs if r["arm"] == arm for p, x in r["checks"] if p == pr]
            pf = sum(x == "pass" for x in res), sum(x == "fail" for x in res)
            cells.append(f"{pf[0]}/{pf[0] + pf[1]}" + (f" ({sum(x == 'unverified' for x in res)} unverified)" if "unverified" in res else "") if res else "-")
        L.append(f"| {pr} | " + " | ".join(cells) + " |")
    # usage
    L += ["", "## Cost, tokens, time, Jev, escalations (attempted valid runs)", "",
          "| arm | runs | total $ | median $ | median wall s | input tok | output tok | cache read | cache write | Jev calls | Jev refused | escalation lines | subagents | budget stops | timeouts |",
          "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for arm in ("old", "new", "none"):
        a = [r for r in rs if r["arm"] == arm]
        if not a: continue
        tok = lambda k: sum(r["usage"].get(k) or 0 for r in a)
        subs = {}
        for r in a:
            for k, v in r["subagents"].items(): subs[k] = subs.get(k, 0) + v
        L.append(f"| {arm} | {len(a)} | {sum(r['cost'] or 0 for r in a):.2f} | {med(r['cost'] for r in a)} | {med(r['wall'] for r in a)} | {tok('input_tokens')} | "
                 f"{tok('output_tokens')} | {tok('cache_read_input_tokens')} | {tok('cache_creation_input_tokens')} | {sum(r['jev'] for r in a)} | "
                 f"{sum(r['jev_refused'] for r in a)} | {sum(r['pending'] for r in a)} | {json.dumps(subs) if subs else '-'} | "
                 f"{sum(r['stop'] == 'budget' for r in a)} | {sum(r['stop'] == 'timeout' for r in a)} |")
    both_ok = [p for p in known if p["new"]["accepted"] and p["old"]["accepted"]]
    if both_ok:
        L.append(f"\nPairs where both passed ({len(both_ok)}): median $ old {med(p['old']['cost'] for p in both_ok)}, new {med(p['new']['cost'] for p in both_ok)}; "
                 f"median wall s old {med(p['old']['wall'] for p in both_ok)}, new {med(p['new']['wall'] for p in both_ok)}.")
    models = sorted({m for r in rs for m in r["models"]})
    L.append(f"\nJev response models observed: {', '.join(models) or 'none'}.")
    # review agreement
    adj = [r for r in rs if r["adjudicated"]]
    L += ["", "## Review", "", f"Adjudicated: {len(adj)}. Adjudication changed a first-pass result: {sum(r['disagree'] for r in adj)}."]
    # invalid blocks, halts, spend
    settle = [e for e in led if e["kind"] == "settle"]
    L += ["", "## Invalid blocks, halts, and spend", ""]
    for e in led:
        if e["kind"] == "invalid": L.append(f"- invalid attempt {e['attempt']} of {e['unit']}: {json.dumps(e['reasons'])}")
        elif e["kind"] == "unit" and e["status"] == "invalid": L.append(f"- block {e['unit']} invalid after the retry; runs {', '.join(e['runs'])}")
        elif e["kind"] == "halt": L.append(f"- halt before {e['unit']}: {e['reason']}")
    L.append(f"- settled spend, all attempts including invalid ones: ${sum(e['usd'] for e in settle):.2f} over {len(settle)} runs, "
             f"{sum(e['seconds'] for e in settle) / 3600:.2f} machine hours")
    # diagnostic apart
    L += ["", "## check diagnostic (new scripts/check, static, Jev blocked; not a grade)", "", "| arm | runs | violations | pending |", "| --- | --- | --- | --- |"]
    for arm in ("old", "new", "none"):
        a = [r for r in rs if r["arm"] == arm]
        if a: L.append(f"| {arm} | {len(a)} | {sum(r['diag_violations'] for r in a)} | {sum(r['diag_pending'] for r in a)} |")
    text = "\n".join(L) + "\n"
    (OUT / stage / (f"report-old-from-{old_from}.md" if old_from else "report.md")).write_text(text)
    return text


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) == 1: print(report(a[0]))
    elif len(a) == 3 and a[1] == "--old-from" and a[2] != a[0]: print(report(a[0], a[2]))
    else: die(__doc__)
