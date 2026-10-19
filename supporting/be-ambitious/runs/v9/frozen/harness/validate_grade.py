"""Validate one grader reply against the rubric's JSON contract (G1-G4).

usage: python3 -I validate_grade.py <run-id> <raw-file>
prints the normalised JSON on success, exits 1 with the reason on failure.
"""
import json
import sys

CASE_CHECKS = {f"T{i}": "abc" for i in range(1, 10)} | {"T10": "ab", "T11": "abcd", "T12": "abc", "T13": "abc"}
COMMON = [f"B{i}" for i in range(1, 11)]
# the rubric's applicability table: R = required (never na), N = always na, other = conditional
_ROW = {"T2": "RRRRRRCRRR", "T6": "RRRRRRCRRR", "T10": "RNRNNNNRRN", "T11": "RRRRRRRRRR", "T12": "RRRRRRCRRN", "T13": "RRRRRRRRRR"}
APPLY = {c: dict(zip(COMMON, _ROW.get(c, "RRRCCRCRRN"))) for c in CASE_CHECKS}
CONDITIONAL_CASE_CHECKS = {"T3c", "T5c", "T9c"}


def validate(run_id: str, raw: str) -> dict:
    lines = [l for l in raw.strip().splitlines() if l.strip()]
    if len(lines) != 1:
        raise ValueError(f"expected 1 non-empty line, got {len(lines)}")
    g = json.loads(lines[0], object_pairs_hook=_no_dupes, parse_constant=_reject_constant)
    if g.get("run") != run_id:
        raise ValueError(f"run is {g.get('run')!r}, expected {run_id!r}")
    case = "T" + str(int(run_id.split("-")[0][1:]))
    want = set(COMMON) | {case + s for s in CASE_CHECKS[case]}
    checks = g.get("checks")
    if not isinstance(checks, dict) or set(checks) != want:
        raise ValueError(f"check keys differ: missing {sorted(want - set(checks or {}))}, extra {sorted(set(checks or {}) - want)}")
    if any(v not in ("pass", "fail", "na") for v in checks.values()):
        raise ValueError("a check value is not pass/fail/na")
    for k, rule in APPLY[case].items():
        if rule == "R" and checks[k] == "na":
            raise ValueError(f"{k} is na but required for {case}")
        if rule == "N" and checks[k] != "na":
            raise ValueError(f"{k} must be na for {case}")
    for k in want - set(COMMON) - CONDITIONAL_CASE_CHECKS:
        if checks[k] == "na":
            raise ValueError(f"{k} is na but required")
    if case != "T10":
        unchanged = checks["B4"] == "na"
        if (checks["B5"] == "na") != unchanged:
            raise ValueError("B4 and B5 disagree about the unchanged branch")
        for k in want & CONDITIONAL_CASE_CHECKS:
            if (checks[k] == "na") != unchanged:
                raise ValueError(f"{k} applicability disagrees with B4/B5")
        if unchanged and checks["B7"] != "na":
            raise ValueError("an unchanged task cannot select a new stretch")
    failed = {k for k, v in checks.items() if v == "fail"}
    fail = g.get("fail")
    if not isinstance(fail, list) or {f.get("check") for f in fail} != failed:
        raise ValueError("fail list does not match failed checks")
    if any(not isinstance(f.get("quote"), str) for f in fail):
        raise ValueError("a failure has no string quote")
    if any(not isinstance(f.get("reason"), str) or not f["reason"].strip() for f in fail):
        raise ValueError("a failure has no reason")
    if g.get("pass") is not (not failed):
        raise ValueError("pass flag is inconsistent with the checks")
    return g


def _reject_constant(value):
    raise ValueError(f"invalid JSON constant: {value}")


def _no_dupes(pairs):
    keys = [k for k, _ in pairs]
    if len(keys) != len(set(keys)):
        raise ValueError("duplicate JSON key")
    return dict(pairs)


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--selftest":
        ok = {"run": "T10-pi-1", "checks": {**{k: "na" for k in COMMON}, "B1": "pass", "B3": "pass", "B8": "pass", "B9": "pass", "T10a": "pass", "T10b": "pass"}, "pass": True, "fail": []}
        assert validate("T10-pi-1", json.dumps(ok))["pass"] is True
        bad_grades = (
            '{"run":"T10-pi-2"}',
            json.dumps(ok) + "\n" + json.dumps(ok),
            json.dumps({**ok, "pass": False}),
            *(json.dumps({**ok, "extra": float(v)}) for v in ("nan", "inf", "-inf")),
        )
        t12 = {"run": "T12-pi-1", "checks": {**{k: "pass" for k in COMMON}, "B7": "na", "B10": "na", "T12a": "pass", "T12b": "pass", "T12c": "pass"}, "pass": True, "fail": []}
        assert validate("T12-pi-1", json.dumps(t12))["pass"] is True
        t13 = {**t12, "run": "T13-pi-1", "checks": {**{k: "pass" for k in COMMON}, "T13a": "pass", "T13b": "pass", "T13c": "pass"}}
        assert validate("T13-pi-1", json.dumps(t13))["pass"] is True
        t1 = {**t12, "run": "T01-pi-1", "checks": {**{k: "pass" for k in COMMON}, "B4": "na", "B5": "na", "B7": "na", "B10": "na", "T1a": "pass", "T1b": "na", "T1c": "pass"}}
        bad_cases = (
            ("T12-pi-1", {**t12, "checks": {**t12["checks"], "B4": "na", "B5": "na"}}),  # T12 requires a changed response
            ("T12-pi-1", {**t12, "checks": {**t12["checks"], "B10": "pass"}}),
            ("T13-pi-1", {**t13, "checks": {**t13["checks"], "B7": "na"}}),  # T13 requires a stretch
            ("T01-pi-1", t1),  # T1b stays required on the unchanged branch
        )
        for run_id, bad in bad_cases:
            try:
                validate(run_id, json.dumps(bad))
            except ValueError:
                continue
            raise AssertionError(f"accepted bad grade for {run_id}")
        for bad in bad_grades:
            try:
                validate("T10-pi-1", bad)
            except ValueError:
                continue
            raise AssertionError(f"accepted bad grade: {bad[:60]}")
        print("selftest ok")
        sys.exit(0)
    run_id, path = sys.argv[1], sys.argv[2]
    try:
        print(json.dumps(validate(run_id, open(path, encoding="utf-8").read())))
    except (ValueError, json.JSONDecodeError) as e:
        print(f"INVALID {run_id}: {e}", file=sys.stderr)
        sys.exit(1)
