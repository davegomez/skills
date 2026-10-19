"""Score two blind answer files against key.json and write result.md. Stdlib only.

usage: REVIEWERS=sonnet,astra python3 -I review2/score.py <folder>   a queue pack (key items with a reason) is
       python3 -I review2/score.py --selftest                       scored against its auto verdict, Jev p, and threshold
"""
import json
import os
import sys
from pathlib import Path

REVIEWERS = tuple(os.environ.get("REVIEWERS", "fable,astra").split(","))


def verdict(answer):
    d = answer.get("defect") if answer else None
    return {True: "fail", False: "pass"}.get(d, "missing")


def jev_verdict(k):
    return "fail" if k["jev_p"] >= k["threshold"] else "pass"


def score(key, a, b):
    a = {x["item"]: x for x in a}
    b = {x["item"]: x for x in b}
    rows, counts = [], {"agreed_label": 0, "agreed_jev": 0, "disputed": 0}
    for k in key:
        va, vb = verdict(a.get(k["item"])), verdict(b.get(k["item"]))
        agree = va == vb and va != "missing"
        new = va if agree else "disputed"
        if not agree:
            counts["disputed"] += 1
        elif new == k["label"]:
            counts["agreed_label"] += 1
        elif new == jev_verdict(k):
            counts["agreed_jev"] += 1
        rows.append((k, va, vb, agree, new))
    return rows, counts


def render(rows, counts):
    out = ["# Review 2 result", "",
           "| item | version | run | check | archive label | jev | fable | astra | agree | new label |",
           "|---|---|---|---|---|---|---|---|---|---|"]
    for k, va, vb, agree, new in rows:
        out.append(f"| {k['item']} | {k['version']} | {k['run']} | {k['check']} | {k['label']} | "
                   f"{jev_verdict(k)} ({k['jev_p']} vs {k['threshold']}) | {va} | {vb} | "
                   f"{'yes' if agree else 'no'} | {new} |")
    out += ["", f"- Agreed with archive label: {counts['agreed_label']}",
            f"- Agreed with Jev: {counts['agreed_jev']}",
            f"- Disputed: {counts['disputed']}", ""]
    return "\n".join(out)


def selftest():
    key = [{"item": "D01", "version": "v1", "run": "r", "check": "B2", "label": "pass", "jev_p": 0.9, "threshold": 0.5},
           {"item": "D02", "version": "v1", "run": "r", "check": "B3", "label": "fail", "jev_p": 0.1, "threshold": 0.5},
           {"item": "D03", "version": "v1", "run": "r", "check": "B4", "label": "pass", "jev_p": 0.5, "threshold": 0.5},
           {"item": "D04", "version": "v1", "run": "r", "check": "B5", "label": "pass", "jev_p": 0.9, "threshold": 0.5}]
    a = [{"item": "D01", "defect": True}, {"item": "D02", "defect": True},
         {"item": "D03", "defect": False}, {"item": "D04", "defect": None}]
    b = [{"item": "D01", "defect": True}, {"item": "D02", "defect": True},
         {"item": "D03", "defect": True}]
    rows, counts = score(key, a, b)
    assert [r[4] for r in rows] == ["fail", "fail", "disputed", "disputed"], rows
    assert counts == {"agreed_label": 1, "agreed_jev": 1, "disputed": 2}, counts
    assert jev_verdict(key[2]) == "fail"
    assert "| D02 |" in render(rows, counts)
    qkey = [dict(k, label="review", reason="jev p>=thr", calibrated=i != 1) for i, k in enumerate(key)]
    qkey[0]["reason"] = "L7 flag: a <- x || b <- y"
    text, qc = render_queue(score(qkey, a, b)[0])
    assert qc == {"fail": 2, "pass": 0, "disputed": 2}, qc
    assert "| D02 | r | B3 | review | jev p>=thr | 0.1 | 0.5 (uncalibrated) | fail | fail | yes | fail |" in text, text
    assert "| L7 flag: a <- x \\|\\| b <- y |" in text, text
    print("selftest ok")


def render_queue(rows):
    """Queue pack: the auto verdict sent each item to review; the reviewers' agreement is the result."""
    out = ["# Review result", "",
           f"| item | run | check | auto verdict | reason | jev p | threshold | {REVIEWERS[0]} | {REVIEWERS[1]} | agree | result |",
           "|---|---|---|---|---|---|---|---|---|---|---|"]
    counts = {"fail": 0, "pass": 0, "disputed": 0}
    for k, va, vb, agree, new in rows:
        counts[new] += 1
        thr = "n/a" if k["threshold"] is None else f"{k['threshold']}{'' if k.get('calibrated') else ' (uncalibrated)'}"
        out.append(f"| {k['item']} | {k['run']} | {k['check']} | {k['label']} | {k['reason'].replace('|', chr(92) + '|')} | "
                   f"{'n/a' if k['jev_p'] is None else k['jev_p']} | {thr} | {va} | {vb} | {'yes' if agree else 'no'} | {new} |")
    out += ["", f"- Both reviewers: fail {counts['fail']}, pass {counts['pass']}", f"- Disputed: {counts['disputed']}", ""]
    return "\n".join(out), counts


def main(folder):
    if "--selftest" in sys.argv:
        return selftest()
    key = json.loads((folder / "key.json").read_text())
    answers = []
    for name in REVIEWERS:
        path = folder / f"answers-{name}.json"
        if not path.exists():
            sys.exit(f"missing {path.name}")
        answers.append(json.loads(path.read_text()))
    rows, counts = score(key, *answers)
    if key and "reason" in key[0]:
        text, counts = render_queue(rows)
    else:
        text = render(rows, counts)
    (folder / "result.md").write_text(text)
    print(f"wrote result.md: {counts}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(Path(sys.argv[1]))
