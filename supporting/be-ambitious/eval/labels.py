"""Ground-truth labels per (version, run, check): the recorded grade, then the accepted overrides.

usage: python3 -I labels.py              writes eval/labels.json, prints a summary
       python3 -I labels.py --selftest
"""
import json
import sys
from pathlib import Path
from typing import TypedDict

EVAL = Path(__file__).resolve().parent
RUNS = EVAL / "calibration-runs"
VERSIONS = ("v2", "v3", "v4", "v5", "v6", "v7")
STATUSES = ("pass", "fail", "na")

Labels = dict[tuple[str, str], dict[str, str]]


class Override(TypedDict):
    version: str
    run: str
    check: str
    to: str
    source: str


def load_recorded(runs: Path = RUNS) -> Labels:
    out: Labels = {}
    for v in VERSIONS:
        for path in sorted((runs / v / "grades").glob("T*.json")):
            grade = json.loads(path.read_text(encoding="utf-8"))
            if grade.get("run") != path.stem:
                raise ValueError(f"{v}/{path.name}: run id {grade.get('run')!r}")
            out[(v, path.stem)] = dict(grade["checks"])
    return out


def apply_overrides(recorded: Labels, overrides: list[dict[str, str]]) -> tuple[Labels, list[str]]:
    """Return new labels and a list of problems; a problem never applies its override."""
    labels = {key: dict(checks) for key, checks in recorded.items()}
    problems: list[str] = []
    for o in overrides:
        key, check = (o["version"], o["run"]), o["check"]
        where = f"{o['source']} {o['version']}/{o['run']} {check}"
        if key not in labels or check not in labels[key]:
            problems.append(f"{where}: no such run or check")
        elif o["to"] not in STATUSES:
            problems.append(f"{where}: bad status {o['to']!r}")
        elif labels[key][check] != o["from"]:
            problems.append(f"{where}: recorded {labels[key][check]!r}, override says from {o['from']!r}")
        else:
            labels[key][check] = o["to"]
    return labels, problems


def load_labels() -> tuple[Labels, list[str]]:
    overrides = json.loads((EVAL / "overrides.json").read_text(encoding="utf-8"))
    return apply_overrides(load_recorded(), overrides)


def _selftest() -> None:
    rec: Labels = {("v2", "T01-pi-1"): {"B1": "pass", "B4": "fail"}}
    good = {"version": "v2", "run": "T01-pi-1", "check": "B4", "from": "fail", "to": "pass", "source": "x"}
    labels, problems = apply_overrides(rec, [good])
    assert labels[("v2", "T01-pi-1")]["B4"] == "pass" and not problems
    assert rec[("v2", "T01-pi-1")]["B4"] == "fail", "recorded labels must not be mutated"
    for bad in ({**good, "from": "pass"}, {**good, "check": "B9"}, {**good, "run": "T02-pi-1"}, {**good, "to": "maybe"}):
        labels, problems = apply_overrides(rec, [bad])
        assert labels[("v2", "T01-pi-1")]["B4"] == "fail" and len(problems) == 1, bad
    print("selftest ok")


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        _selftest()
        sys.exit(0)
    labels, problems = load_labels()
    (EVAL / "labels.json").write_text(
        json.dumps({f"{v}/{run}": checks for (v, run), checks in sorted(labels.items())}, indent=1) + "\n", encoding="utf-8"
    )
    fails = sum(s == "fail" for checks in labels.values() for s in checks.values())
    print(f"{len(labels)} runs, {fails} fail labels, {len(problems)} override problems")
    for p in problems:
        print("PROBLEM", p)
    sys.exit(1 if problems else 0)
