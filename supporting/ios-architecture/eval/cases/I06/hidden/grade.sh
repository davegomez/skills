#!/usr/bin/env bash
# Hidden grader for I06 (authenticated reading list).
# Usage: grade.sh <work-dir> <out.json>   Needs EVAL_SIM = simulator UDID.
# Exit 0 when it wrote a result (also when checks fail); 2 on an infrastructure failure.
set -uo pipefail

[ $# -eq 2 ] || { echo "usage: grade.sh <work-dir> <out.json>" >&2; exit 2; }
WORK=$(cd "$1" 2>/dev/null && pwd) || { echo "no work dir: $1" >&2; exit 2; }
OUT=$2
SIM=${EVAL_SIM:-}
[ -n "$SIM" ] || { echo "EVAL_SIM is not set" >&2; exit 2; }
HERE=$(cd "$(dirname "$0")" && pwd)
CASE=$(dirname "$HERE")
FIXTURE="$CASE/fixture"
TOKEN=$(sed -n 's/.*static let token = "\(.*\)"/\1/p' "$FIXTURE/Shelf/Seams/FakeAuthService.swift")
[ -n "$TOKEN" ] || { echo "cannot read the fake token from the fixture" >&2; exit 2; }

TMP=$(mktemp -d "${TMPDIR:-/tmp}/i06-grade.XXXXXX")
LOGPID=""
cleanup() { [ -n "$LOGPID" ] && kill "$LOGPID" 2>/dev/null; rm -rf "$TMP"; }
trap cleanup EXIT
RESULTS="$TMP/results.tsv"
: > "$RESULTS"
record() { printf '%s\t%s\t%s\n' "$1" "$2" "$3" >> "$RESULTS"; }

xcrun simctl bootstatus "$SIM" -b >/dev/null 2>&1 || { echo "simulator $SIM does not boot" >&2; exit 2; }

APP="$TMP/app"
mkdir -p "$APP"
rsync -a --exclude .git "$WORK/" "$APP/" || { echo "copy failed" >&2; exit 2; }

# Test seam: the fake transport, fake auth, and launch contract must be byte-identical somewhere in the tree.
find "$APP" -name '*.swift' -type f -exec shasum -a 256 {} + | awk '{print $1}' | sort -u > "$TMP/tree.sha"
missing=""
for f in "$FIXTURE"/Shelf/Seams/*.swift; do
    sha=$(shasum -a 256 "$f" | awk '{print $1}')
    grep -qx "$sha" "$TMP/tree.sha" || missing="$missing $(basename "$f")"
done
if [ -z "$missing" ]; then
    record I06-test-seam-intact pass "all files of Shelf/Seams are unchanged"
else
    record I06-test-seam-intact fail "changed or missing:$missing"
fi

# String Catalog with the Spanish title.
catalog=$(python3 -I - "$APP" <<'PY'
import json, pathlib, sys
root = pathlib.Path(sys.argv[1])
for path in root.rglob("*.xcstrings"):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        continue
    for entry in data.get("strings", {}).values():
        unit = entry.get("localizations", {}).get("es", {}).get("stringUnit", {})
        if unit.get("value") == "Lista de lectura":
            print(path.relative_to(root))
            sys.exit(0)
PY
)
if [ -n "$catalog" ]; then
    record I06-strings-in-catalog pass "Spanish title in $catalog"
else
    record I06-strings-in-catalog fail "no .xcstrings file has the Spanish title"
fi

TESTS="testStateLoading testStateList testStateEmpty testStateError testOfflineShowsCache testRetryTransientRecovers testRetryTransientLimit testRetryPermanentNoRetry testRetryCancel testSecondLocale testAccessibilityAudit"
fail_build_checks() {
    record I06-build fail "$1"
    for t in $TESTS; do record "test:$t" fail "$1"; done
    record I06-token-not-in-logs fail "$1"
    record I06-token-not-in-preferences fail "$1"
}

if [ ! -d "$APP/Shelf.xcodeproj" ] || [ ! -d "$APP/ShelfUITests" ]; then
    fail_build_checks "Shelf.xcodeproj or ShelfUITests/ is missing"
else
    cp "$HERE/HiddenAcceptanceTests.swift" "$APP/ShelfUITests/HiddenAcceptanceTests.swift"
    if [ -d "$APP/Shelf.xcworkspace" ]; then CONTAINER=(-workspace "$APP/Shelf.xcworkspace"); else CONTAINER=(-project "$APP/Shelf.xcodeproj"); fi
    XCB=(xcodebuild "${CONTAINER[@]}" -scheme Shelf -destination "id=$SIM" -derivedDataPath "$TMP/dd" CODE_SIGNING_ALLOWED=NO)
    if ! "${XCB[@]}" build-for-testing > "$TMP/build.log" 2>&1; then
        fail_build_checks "build failed: $(grep -m1 'error:' "$TMP/build.log" | cut -c1-200)"
    else
        record I06-build pass "build-for-testing succeeded"
        PRODUCT=$(find "$TMP/dd/Build/Products/Debug-iphonesimulator" -maxdepth 1 -name '*.app' ! -name '*-Runner.app' | head -1)
        BUNDLE=$(/usr/libexec/PlistBuddy -c 'Print :CFBundleIdentifier' "$PRODUCT/Info.plist" 2>/dev/null)
        EXEC=$(/usr/libexec/PlistBuddy -c 'Print :CFBundleExecutable' "$PRODUCT/Info.plist" 2>/dev/null)
        [ -n "$BUNDLE" ] && [ -n "$EXEC" ] || { echo "cannot read the built app" >&2; exit 2; }
        xcrun simctl terminate "$SIM" "$BUNDLE" >/dev/null 2>&1
        xcrun simctl uninstall "$SIM" "$BUNDLE" >/dev/null 2>&1

        # Capture os_log (the simulator shows private values) for the whole run.
        xcrun simctl spawn "$SIM" log stream --level debug --style compact --predicate "process == \"$EXEC\"" > "$TMP/oslog.txt" 2>&1 &
        LOGPID=$!
        sleep 2

        "${XCB[@]}" test-without-building -only-testing:ShelfUITests/HiddenAcceptanceTests \
            -resultBundlePath "$TMP/result.xcresult" > "$TMP/test.log" 2>&1
        [ -d "$TMP/result.xcresult" ] || { echo "no result bundle; see test log" >&2; tail -20 "$TMP/test.log" >&2; exit 2; }

        # Capture stdout and stderr (print, NSLog) in 3 launches that open the list.
        for scenario in success permanent transient-exhausted; do
            SIMCTL_CHILD_EVAL_SCENARIO=$scenario SIMCTL_CHILD_EVAL_START=list SIMCTL_CHILD_OS_ACTIVITY_DT_MODE=YES \
                xcrun simctl launch --console-pty --terminate-running-process "$SIM" "$BUNDLE" > "$TMP/console-$scenario.txt" 2>&1 &
            CPID=$!
            sleep 8
            xcrun simctl terminate "$SIM" "$BUNDLE" >/dev/null 2>&1
            sleep 1
            kill "$CPID" 2>/dev/null
            wait "$CPID" 2>/dev/null
        done
        sleep 2
        kill "$LOGPID" 2>/dev/null
        LOGPID=""

        leaks=$(cat "$TMP/oslog.txt" "$TMP"/console-*.txt | grep -ac -- "$TOKEN")
        oslog_requests=$(grep -ac 'seam attempt=' "$TMP/oslog.txt")
        console_passes=0
        for c in "$TMP"/console-*.txt; do grep -aq '\[seam\] attempt=' "$c" && console_passes=$((console_passes + 1)); done
        if [ "$leaks" -gt 0 ]; then
            record I06-token-not-in-logs fail "token found in $leaks captured log lines"
        elif [ "$oslog_requests" -eq 0 ] || [ "$console_passes" -lt 3 ]; then
            record I06-token-not-in-logs fail "no request observed (os_log requests: $oslog_requests, console launches with a request: $console_passes of 3)"
        else
            record I06-token-not-in-logs pass "0 token lines in os_log ($oslog_requests requests) and 3 console captures"
        fi

        CONTAINER_DIR=$(xcrun simctl get_app_container "$SIM" "$BUNDLE" data 2>/dev/null)
        if [ -z "$CONTAINER_DIR" ]; then
            record I06-token-not-in-preferences fail "no app data container"
        else
            prefs=$(grep -rlaF -- "$TOKEN" "$CONTAINER_DIR/Library/Preferences" 2>/dev/null | wc -l | tr -d ' ')
            if [ "$prefs" -gt 0 ]; then
                record I06-token-not-in-preferences fail "token found in $prefs preferences file(s)"
            else
                record I06-token-not-in-preferences pass "token not in Library/Preferences"
            fi
        fi

        # The fake logs this line only when the caller cancels the request (testRetryCancel goes back mid-load).
        CANCELLED=$(grep -ac 'seam attempt=1 scenario=cancel cancelled' "$TMP/oslog.txt")

        xcrun xcresulttool get test-results tests --path "$TMP/result.xcresult" > "$TMP/tests.json" 2>/dev/null
        python3 -I - "$TMP/tests.json" "$TESTS" "$CANCELLED" >> "$RESULTS" <<'PY'
import json, sys
try:
    data = json.load(open(sys.argv[1]))
except (OSError, ValueError):
    data = {"testNodes": []}
found = {}
def walk(node):
    if node.get("nodeType") == "Test Case":
        name = node.get("name", "").split("(")[0]
        messages = [c.get("name", "") for c in node.get("children", []) if c.get("nodeType") == "Failure Message"]
        found[name] = (node.get("result"), messages)
    for child in node.get("children", []):
        walk(child)
for node in data.get("testNodes", []):
    walk(node)
for test in sys.argv[2].split():
    result, messages = found.get(test, (None, []))
    if test == "testRetryCancel" and result == "Passed" and sys.argv[3] == "0":
        print(f"test:{test}\tfail\tXCUITest {test} passed, but the transport never saw the request cancelled")
    elif result == "Passed":
        print(f"test:{test}\tpass\tXCUITest {test} passed")
    elif result is None:
        print(f"test:{test}\tfail\tXCUITest {test} did not run")
    else:
        detail = (messages[0] if messages else result).replace("\t", " ").replace("\n", " ")[:200]
        print(f"test:{test}\tfail\tXCUITest {test}: {detail}")
PY
    fi
fi

python3 -I - "$RESULTS" "$OUT" <<'PY'
import json, sys
meta = {
    "I06-test-seam-intact": ("reliability", True),
    "I06-build": ("reliability", True),
    "test:testStateLoading": ("I06-state-loading", "reliability", True),
    "test:testStateList": ("I06-state-list", "reliability", True),
    "test:testStateEmpty": ("I06-state-empty", "reliability", True),
    "test:testStateError": ("I06-state-error", "reliability", True),
    "test:testOfflineShowsCache": ("I06-offline-shows-cache", "reliability", True),
    "test:testRetryTransientRecovers": ("I06-retry-transient-recovers", "reliability", True),
    "test:testRetryTransientLimit": ("I06-retry-transient-limit", "reliability", True),
    "test:testRetryPermanentNoRetry": ("I06-retry-permanent-no-retry", "reliability", True),
    "test:testRetryCancel": ("I06-retry-cancel", "reliability", True),
    "test:testSecondLocale": ("I06-second-locale", "accessibility", True),
    "test:testAccessibilityAudit": ("I06-accessibility-audit", "accessibility", False),
    "I06-token-not-in-logs": ("security", True),
    "I06-token-not-in-preferences": ("security", True),
    "I06-strings-in-catalog": ("maintainability", False),
}
checks = []
for line in open(sys.argv[1], encoding="utf-8"):
    key, result, evidence = line.rstrip("\n").split("\t", 2)
    m = meta[key]
    check_id, priority, critical = (m if len(m) == 3 else (key, *m))
    checks.append({"id": check_id, "priority": priority, "critical": critical, "result": result, "evidence": evidence})
order = [m[0] if len(m) == 3 else k for k, m in meta.items()]
checks.sort(key=lambda c: order.index(c["id"]))
json.dump({"case": "I06", "checks": checks}, open(sys.argv[2], "w"), indent=2)
PY
