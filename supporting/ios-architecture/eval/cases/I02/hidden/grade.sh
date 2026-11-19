#!/bin/bash
# Hidden grader of case I02 (new feature: order summary in a frozen scaffold-made app).
# Usage: EVAL_SIM=<simulator UDID> grade.sh <work-dir> <out.json>
# Exit 0 when it wrote a result, also when checks fail; exit 2 on an infrastructure failure.
set -u

here=$(cd "$(dirname "$0")" && pwd) || exit 2
. "$here/lib.sh"

CASE=I02
SCHEME=Storefront
FIXTURE=$here/../fixture
# Packages that task.md says to leave unchanged.
ADJACENT="Packages/Core Packages/DesignSystem Packages/Networking Packages/Persistence"

[ $# -eq 2 ] || { echo "usage: grade.sh <work-dir> <out.json>" >&2; exit 2; }
work=$(cd "$1" 2>/dev/null && pwd) || infra "$1 is not a directory"
out=$2
[ -d "$FIXTURE" ] || infra "fixture not found at $FIXTURE"
[ -f "$here/baseline-tests.txt" ] || infra "baseline-tests.txt not found"
check_environment

tmp=$(mktemp -d "${TMPDIR:-/tmp}/grade-$CASE.XXXXXX") || infra "cannot create a temporary folder"
trap 'rm -rf "$tmp"' EXIT
CHECKS=$tmp/checks.jsonl
: >"$CHECKS"
copy_result "$work" "$tmp/src"
dd=$tmp/dd
dest="id=$EVAL_SIM"

# 1. Build the app scheme for the simulator.
built=false
app=""
build_evidence=""
if ! container_lines=$(find_container "$tmp/src"); then
    build_evidence="no Xcode workspace or project within 3 levels of the folder root"
else
    container=("$(sed -n 1p <<<"$container_lines")" "$(sed -n 2p <<<"$container_lines")")
    if ! xcodebuild "${container[@]}" -list -json 2>/dev/null | jq -e --arg s "$SCHEME" \
        '(.workspace.schemes // .project.schemes // []) | any(.[]; . == $s)' >/dev/null; then
        build_evidence="no scheme named $SCHEME in ${container[1]#$tmp/src/}"
    elif with_timeout 1500 xcodebuild build "${container[@]}" -scheme "$SCHEME" -destination "$dest" \
        -derivedDataPath "$dd" CODE_SIGNING_ALLOWED=NO >"$tmp/build.log" 2>&1; then
        app=$(xcodebuild "${container[@]}" -scheme "$SCHEME" -destination "$dest" -derivedDataPath "$dd" \
            -showBuildSettings -json 2>/dev/null | jq -r '
            [.[] | select(.buildSettings.PRODUCT_TYPE == "com.apple.product-type.application")][0].buildSettings
            | if . then .TARGET_BUILD_DIR + "/" + .FULL_PRODUCT_NAME else "" end')
        if [ -n "$app" ] && [ -f "$app/Info.plist" ]; then
            built=true
            build_evidence="xcodebuild build -scheme $SCHEME succeeded; app ${app##*/}"
        else
            build_evidence="build succeeded, but the scheme builds no application target"
        fi
    else
        build_evidence="xcodebuild build failed: $(tail_of "$tmp/build.log")"
    fi
fi
$built && add_check I02-builds reliability true pass "$build_evidence" ||
    add_check I02-builds reliability true fail "$build_evidence"

# 2. Adjacent packages are byte-identical to the fixture.
changed=""
for dir in $ADJACENT; do
    if ! diff -rq -x .build -x .swiftpm -x xcuserdata "$FIXTURE/$dir" "$tmp/src/$dir" >>"$tmp/adjacent.log" 2>&1; then
        changed="$changed $dir"
    fi
done
if [ -z "$changed" ]; then
    add_check I02-adjacent-code-unchanged maintainability true pass "$ADJACENT are identical to the fixture"
else
    add_check I02-adjacent-code-unchanged maintainability true fail \
        "changed:$changed; $(head -n 3 "$tmp/adjacent.log" | sed "s|$tmp/src/||g; s|$FIXTURE/||g" | tr '\n' ' ' | cut -c1-300)"
fi

# 3. The scheme's test action (its test plan) runs tests that the fixture did not have, and they pass.
# Only new tests decide the check: the fixture's root audit fails once any feature row is on the root
# (the scaffold's sidebar row trips the text-clipping heuristic), which is not the builder's fault.
# Failed fixture tests are listed in the evidence.
if $built; then
    with_timeout 1800 xcodebuild test "${container[@]}" -scheme "$SCHEME" -destination "$dest" -derivedDataPath "$dd" \
        -resultBundlePath "$tmp/own.xcresult" CODE_SIGNING_ALLOWED=NO >"$tmp/own.log" 2>&1
    test_cases "$tmp/own.xcresult" >"$tmp/own.jsonl" 2>/dev/null
    jq -cs --rawfile base "$here/baseline-tests.txt" '
        ($base | split("\n") | map(select(length > 0))) as $known
        | map(. + {new: ((.bundle + "|" + .id) as $k | $known | any(.[]; . == $k) | not)})
        | {new_total: (map(select(.new)) | length),
           new_failed: [.[] | select(.new and .result == "Failed") | .id],
           old_failed: [.[] | select((.new | not) and .result == "Failed") | .id + " (" + .message + ")"]}' \
        "$tmp/own.jsonl" >"$tmp/own-summary.json"
    new_total=$(jq -r .new_total "$tmp/own-summary.json")
    new_failed=$(jq -r '.new_failed | length' "$tmp/own-summary.json")
    evidence="$new_total tests not in the fixture ran in the $SCHEME test action; $new_failed of them failed$(jq -r '
        (if (.new_failed | length) > 0 then ": " + (.new_failed | join(", ")) else "" end)
        + (if (.old_failed | length) > 0 then "; failed fixture tests (not graded): " + (.old_failed | join(", ")) else "" end)' \
        "$tmp/own-summary.json" | cut -c1-400)"
    if [ "${new_total:-0}" -ge 1 ] && [ "${new_failed:-0}" -eq 0 ]; then
        add_check I02-test-plan-runs-new-tests reliability true pass "$evidence"
    else
        add_check I02-test-plan-runs-new-tests reliability true fail "$evidence"
    fi
else
    add_check I02-test-plan-runs-new-tests reliability true fail "no build: $build_evidence"
fi

# 4. Hidden black-box UI tests on a fresh install of the built app.
ui_checks="testEntryReachableExactlyOnce()=I02-reachable-exactly-once=reliability testSampleOrderTotals()=I02-totals-match-spec=reliability testEmptyState()=I02-empty-state=reliability testErrorState()=I02-error-state=reliability"
if $built; then
    bundle_id=$(plutil -extract CFBundleIdentifier raw "$app/Info.plist") || infra "cannot read the bundle ID of ${app##*/}"
    xcrun simctl terminate "$EVAL_SIM" "$bundle_id" >/dev/null 2>&1
    xcrun simctl uninstall "$EVAL_SIM" "$bundle_id" >/dev/null 2>&1
    xcrun simctl install "$EVAL_SIM" "$app" >"$tmp/install.log" 2>&1 || infra "cannot install ${app##*/}: $(tail -n 2 "$tmp/install.log")"
    cp -R "$here/runner" "$tmp/runner" || infra "cannot copy the hidden runner"
    TEST_RUNNER_EVAL_APP_BUNDLE_ID=$bundle_id with_timeout 1200 xcodebuild test -project "$tmp/runner/EvalUITests.xcodeproj" \
        -scheme EvalUITests -destination "$dest" -derivedDataPath "$tmp/ddr" -resultBundlePath "$tmp/hidden.xcresult" \
        CODE_SIGNING_ALLOWED=NO >"$tmp/hidden.log" 2>&1
    [ -d "$tmp/hidden.xcresult" ] || infra "the hidden UI tests did not run: $(tail_of "$tmp/hidden.log")"
    test_cases "$tmp/hidden.xcresult" >"$tmp/hidden.jsonl"
    for entry in $ui_checks; do
        IFS== read -r test id priority <<<"$entry"
        row=$(jq -cs --arg t "$test" '[.[] | select(.id | endswith("/" + $t))][0] // {result: "missing", message: ""}' "$tmp/hidden.jsonl")
        result=$(jq -r .result <<<"$row")
        case $result in
            Passed) add_check "$id" "$priority" true pass "XCUITest $test passed" ;;
            missing) infra "hidden test $test has no result" ;;
            *) add_check "$id" "$priority" true fail "XCUITest $test: $result. $(jq -r .message <<<"$row" | cut -c1-300)" ;;
        esac
    done
else
    for entry in $ui_checks; do
        IFS== read -r test id priority <<<"$entry"
        add_check "$id" "$priority" true fail "no build: $build_evidence"
    done
fi

write_result "$out"
