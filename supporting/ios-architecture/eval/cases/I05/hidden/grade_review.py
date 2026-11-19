"""Hidden grader for I05 (read-only review). Called by grade.sh; run with python3 -I.

Usage: grade_review.py <case-dir> <work-dir> <out.json>
Exit 0 when it wrote a result; 2 on an infrastructure failure.
"""

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SEVERITIES = ("critical", "major", "minor")
FINDING = re.compile(
    r"^\s*[-*]\s*\**\s*(critical|major|minor)\s*\**\s*\|\s*`?([^`|]+?)`?\s*\|\s*(.+?)\s*$",
    re.IGNORECASE,
)
LOCATION = re.compile(r"^(.*?):(\d+)(?:\s*[-–]\s*(\d+))?$")
NO_FINDINGS = re.compile(r"^\s*No findings\.?\s*$", re.IGNORECASE | re.MULTILINE)
GIT_ENV = {
    **os.environ,
    "GIT_AUTHOR_NAME": "grader", "GIT_AUTHOR_EMAIL": "grader@example.invalid",
    "GIT_COMMITTER_NAME": "grader", "GIT_COMMITTER_EMAIL": "grader@example.invalid",
    "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_NOSYSTEM": "1",
}


class Infra(Exception):
    pass


def git(cwd, *args):
    run = subprocess.run(["git", *args], cwd=cwd, env=GIT_ENV, capture_output=True, text=True)
    if run.returncode != 0:
        raise Infra(f"git {' '.join(args)} failed: {run.stderr.strip()[:200]}")
    return run.stdout


def snapshot(source, dest, patch=None, drop=()):
    """Copy a tree without .git, apply a patch, and return {path: sha256} of non-ignored files."""
    shutil.copytree(source, dest, ignore=shutil.ignore_patterns(".git"), symlinks=True)
    for name in drop:
        target = Path(dest, name)
        if target.is_file():
            target.unlink()
    git(dest, "init", "-q")
    if patch:
        git(dest, "apply", str(patch))
    files = git(dest, "ls-files", "-co", "--exclude-standard", "-z").split("\0")
    tree = {}
    for name in filter(None, files):
        path = Path(dest, name)
        mode = "x" if os.access(path, os.X_OK) else "-"
        tree[name] = mode + hashlib.sha256(path.read_bytes()).hexdigest()
    return tree


def parse_review(text):
    findings, malformed = [], 0
    for raw in text.splitlines():
        match = FINDING.match(raw)
        if not match:
            if re.match(r"^\s*[-*]\s", raw) and re.search(r"\.swift|\.xcstrings", raw):
                malformed += 1
            continue
        location = LOCATION.match(match.group(2).strip())
        if not location:
            malformed += 1
            continue
        start = int(location.group(2))
        end = int(location.group(3) or start)
        path = location.group(1).strip().lstrip("./")
        findings.append({
            "severity": match.group(1).lower(),
            "file": path,
            "start": min(start, end),
            "end": max(start, end),
            "reason": match.group(3),
        })
    return findings, malformed


def same_file(gold, claimed):
    return gold == claimed or gold.endswith("/" + claimed)


def hits(site, finding, window):
    if not same_file(site["file"], finding["file"]):
        return False
    if finding["end"] < site["line"] - window or finding["start"] > site["line"] + window:
        return False
    reason = finding["reason"]
    return all(re.search(group, reason, re.IGNORECASE) for group in site["cause"])


def grade(case_dir, work_dir, out_path):
    case = json.loads(Path(case_dir, "case.json").read_text())
    window = case["match"]["line_window"]
    traps = {t["id"]: t for t in case["traps"]}

    with tempfile.TemporaryDirectory() as tmp:
        expected = {
            name: snapshot(Path(case_dir, "fixture"), Path(tmp, name), Path(case_dir, spec["diff"]))
            for name, spec in case["variants"].items()
        }
        actual = snapshot(work_dir, Path(tmp, "actual"), drop=("REVIEW.md",))

    variant = os.environ.get("EVAL_VARIANT")
    matched = [name for name, tree in expected.items() if tree == actual]
    if variant and variant not in case["variants"]:
        raise Infra(f"unknown EVAL_VARIANT {variant}")
    if not variant:
        if matched:
            variant = matched[0]
        else:  # Edited tree: take the variant with the fewest differing files.
            def distance(tree):
                return sum(1 for k in set(tree) | set(actual) if tree.get(k) != actual.get(k))
            variant = min(expected, key=lambda name: distance(expected[name]))
    spec = case["variants"][variant]
    changed = sorted(k for k in set(expected[variant]) | set(actual) if expected[variant].get(k) != actual.get(k))

    checks = []

    def check(check_id, priority, critical, result, evidence):
        checks.append({"id": check_id, "priority": priority, "critical": critical, "result": result, "evidence": evidence})

    if changed:
        check("I05-no-edits", "reliability", True, "fail", f"{len(changed)} file(s) differ from the {variant} tree: {', '.join(changed[:5])}")
    else:
        check("I05-no-edits", "reliability", True, "pass", f"tree equals the {variant} tree apart from REVIEW.md")

    review_path = Path(work_dir, "REVIEW.md")
    text = review_path.read_text(encoding="utf-8", errors="replace") if review_path.is_file() else None
    findings, malformed = parse_review(text or "")
    declared_none = bool(text and NO_FINDINGS.search(text))
    if text is None:
        check("I05-review-written", "reliability", True, "fail", "REVIEW.md is missing")
    elif not findings and not declared_none:
        check("I05-review-written", "reliability", True, "fail", f"REVIEW.md has no parseable finding and no 'No findings.' line ({malformed} malformed)")
    else:
        check("I05-review-written", "reliability", True, "pass", f"{len(findings)} finding(s), {malformed} malformed line(s)")

    active = [traps[t] for t in spec["traps"]]
    for finding in findings:
        finding["traps"] = [t["id"] for t in active if hits(t, finding, window)]
        finding["lookalikes"] = [] if finding["traps"] else [l["id"] for l in spec["lookalikes"] if hits(l, finding, window)]

    for trap in case["traps"]:
        if trap["id"] not in spec["traps"]:
            check(trap["id"], trap["priority"], True, "na", f"not seeded in the {variant} variant")
            continue
        found = [f for f in findings if trap["id"] in f["traps"]]
        if found:
            check(trap["id"], trap["priority"], True, "pass", f"matched by {found[0]['severity']} finding at {found[0]['file']}:{found[0]['start']}")
        else:
            check(trap["id"], trap["priority"], True, "fail", f"no finding at {trap['file']}:{trap['line']}±{window} with the cause")

    flagged = sorted({l for f in findings for l in f["lookalikes"]})
    if flagged:
        check("I05-no-lookalike-flagged", "reliability", False, "fail", f"flagged benign code: {', '.join(flagged)}")
    else:
        check("I05-no-lookalike-flagged", "reliability", False, "pass", "no lookalike flagged")

    unsupported = [f for f in findings if not f["traps"]]
    material = [f for f in unsupported if f["severity"] in ("critical", "major")]
    if variant == "clean":
        result = "fail" if material else "pass"
        check("I05-clean-no-unsupported-material", "reliability", False, result,
              f"{len(material)} unsupported critical or major finding(s), {len(unsupported)} unsupported in total")
    else:
        check("I05-clean-no-unsupported-material", "reliability", False, "na", "seeded variant")

    recall, precision = {}, {}
    for severity in SEVERITIES:
        gold = [t for t in active if t["severity"] == severity]
        recall[severity] = None if not gold else sum(any(t["id"] in f["traps"] for f in findings) for t in gold) / len(gold)
        claimed = [f for f in findings if f["severity"] == severity]
        precision[severity] = None if not claimed else sum(bool(f["traps"]) for f in claimed) / len(claimed)
    agreement = [f["severity"] == traps[f["traps"][0]]["severity"] for f in findings if f["traps"]]

    result = {
        "case": "I05",
        "variant": variant,
        "checks": checks,
        "metrics": {
            "findings": len(findings),
            "malformed_lines": malformed,
            "recall_by_gold_severity": recall,
            "precision_by_claimed_severity": precision,
            "severity_agreement": None if not agreement else sum(agreement) / len(agreement),
            "unsupported": len(unsupported),
            "unsupported_material": len(material),
            "lookalikes_flagged": flagged,
            "unsupported_findings": [
                {k: f[k] for k in ("severity", "file", "start", "end", "reason")} for f in unsupported
            ],
        },
    }
    Path(out_path).write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")


def main():
    if len(sys.argv) != 4:
        print("usage: grade_review.py <case-dir> <work-dir> <out.json>", file=sys.stderr)
        return 2
    case_dir, work_dir, out_path = sys.argv[1:]
    if not Path(work_dir).is_dir():
        print(f"no work dir: {work_dir}", file=sys.stderr)
        return 2
    try:
        grade(Path(case_dir), Path(work_dir), out_path)
    except Infra as error:
        print(error, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
