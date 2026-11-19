#!/usr/bin/env bash
# Hidden grader for case I03 (deep link to an archive preview).
# Usage: grade.sh <work-dir> <out.json>
# Needs EVAL_SIM (a simulator UDID). Exit 0 when it wrote a result, also when checks fail;
# exit 2 for a usage error and 3 for an infrastructure failure.
set -euo pipefail

usage() { echo "usage: EVAL_SIM=<udid> grade.sh <work-dir> <out.json>" >&2; exit 2; }
[ $# -eq 2 ] || usage
[ -d "$1" ] || usage
[ -n "${EVAL_SIM:-}" ] || usage

here=$(cd "$(dirname "$0")" && pwd)
work=$(cd "$1" && pwd)
out=$2
tmp=$(mktemp -d "${TMPDIR:-/tmp}/grade-i03.XXXXXX")
trap 'rm -rf "$tmp"' EXIT

# Grade a copy of the result, never the builder's tree.
rsync -a --exclude .git --exclude DerivedData --exclude build "$work/" "$tmp/src/"
if [ -d "$tmp/src/QuickNotesUITests" ]; then
  mkdir -p "$tmp/src/QuickNotesUITests/HiddenI03"
  cp "$here/HiddenI03AcceptanceTests.swift" "$tmp/src/QuickNotesUITests/HiddenI03/"
fi

xcrun simctl boot "$EVAL_SIM" >/dev/null 2>&1 || true
xcrun simctl bootstatus "$EVAL_SIM" >/dev/null 2>&1 || { echo "simulator $EVAL_SIM did not boot" >&2; exit 3; }
xcrun simctl uninstall "$EVAL_SIM" com.example.quicknotes >/dev/null 2>&1 || true

common=(-project "$tmp/src/QuickNotes.xcodeproj" -scheme QuickNotes -destination "id=$EVAL_SIM"
  -derivedDataPath "$tmp/dd" CODE_SIGNING_ALLOWED=NO)
build=pass
xcodebuild build-for-testing "${common[@]}" >"$tmp/build.log" 2>&1 || build=fail

tests=skipped
if [ "$build" = pass ]; then
  tests=ran
  xcodebuild test-without-building "${common[@]}" -resultBundlePath "$tmp/r.xcresult" \
    -parallel-testing-enabled NO -only-testing:QuickNotesUITests/HiddenI03AcceptanceTests \
    >"$tmp/test.log" 2>&1 || true
  [ -d "$tmp/r.xcresult" ] || { tail -20 "$tmp/test.log" >&2; echo "no result bundle" >&2; exit 3; }
  xcrun xcresulttool get test-results tests --path "$tmp/r.xcresult" >"$tmp/tests.json" \
    || { echo "xcresulttool failed" >&2; exit 3; }
fi

python3 -I - "$build" "$tests" "$tmp" "$out" <<'PY'
import json, re, sys
build, tests, tmp, out = sys.argv[1:5]

# id, priority, critical, test method (None: the build itself)
CHECKS = [
    ("I03-build", "reliability", True, None),
    ("I03-valid-link-confirmation", "reliability", True, "testValidLinkShowsConfirmation"),
    ("I03-malformed-link-rejected", "security", True, "testMalformedAndUnknownLinksAreRejected"),
    ("I03-link-needs-confirmation", "security", True, "testLinkAloneDoesNotChangeState"),
    ("I03-cancel-keeps-data", "reliability", True, "testCancelKeepsData"),
    ("I03-confirm-archives-once", "reliability", True, "testConfirmArchivesExactlyOnce"),
    ("I03-existing-navigation", "reliability", True, "testExistingNavigationStillWorks"),
    ("I03-preview-accessibility-audit", "accessibility", False, "testPreviewPassesAccessibilityAudit"),
]

results = {}
if tests == "ran":
    def walk(node):
        if node.get("nodeType") == "Test Case":
            name = node.get("name", "").split("(")[0]
            results.setdefault(name, []).append(node.get("result", "unknown"))
        for child in node.get("children", []):
            walk(child)
    for node in json.load(open(f"{tmp}/tests.json")).get("testNodes", []):
        walk(node)
    log = open(f"{tmp}/test.log", errors="replace").read()

def first_error(method):
    m = re.search(r"error: -\[\S+ " + method + r"\] : (.{0,160})", log)
    return m.group(1).strip() if m else ""

checks = []
for cid, priority, critical, method in CHECKS:
    if method is None:
        result = build
        evidence = "xcodebuild build-for-testing " + ("succeeded" if build == "pass" else "failed")
    elif build != "pass":
        result, evidence = "fail", "build failed"
    else:
        runs = results.get(method, [])
        if len(runs) != 1:
            result, evidence = "fail", f"XCUITest {method} ran {len(runs)} times, expected 1"
        elif runs[0] == "Passed":
            result, evidence = "pass", f"XCUITest {method} passed"
        else:
            result = "fail"
            evidence = f"XCUITest {method} {runs[0].lower()}: {first_error(method)}".rstrip(": ")
    checks.append({"id": cid, "priority": priority, "critical": critical,
                   "result": result, "evidence": evidence})

json.dump({"case": "I03", "checks": checks}, open(out, "w"), indent=2)
PY
