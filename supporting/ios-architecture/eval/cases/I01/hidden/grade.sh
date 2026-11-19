#!/bin/bash
# Hidden grader of case I01 (new project: offline packing list).
# Usage: EVAL_SIM=<simulator UDID> grade.sh <work-dir> <out.json>
# Exit 0 when it wrote a result, also when checks fail; exit 2 on an infrastructure failure.
set -u

here=$(cd "$(dirname "$0")" && pwd) || exit 2
. "$here/lib.sh"

CASE=I01
SCHEME=PackingList
MIN_IOS=27.3
BUNDLE_PREFIX=com.example.eval.
# Test bundles that the new skill's scaffold generates; they prove nothing about the packing-list logic.
SCAFFOLD_BUNDLES='["CoreClientsTests", "FeatureKitTests", "NetworkingTests", "PersistenceTests"]'

[ $# -eq 2 ] || { echo "usage: grade.sh <work-dir> <out.json>" >&2; exit 2; }
work=$(cd "$1" 2>/dev/null && pwd) || infra "$1 is not a directory"
out=$2
check_environment

tmp=$(mktemp -d "${TMPDIR:-/tmp}/grade-$CASE.XXXXXX") || infra "cannot create a temporary folder"
trap 'rm -rf "$tmp"' EXIT
CHECKS=$tmp/checks.jsonl
: >"$CHECKS"
copy_result "$work" "$tmp/src"
dd=$tmp/dd
dest="id=$EVAL_SIM"

# 1. Find the project and the scheme, then build for the simulator.
built=false
app=""
settings="{}"
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
        settings=$(xcodebuild "${container[@]}" -scheme "$SCHEME" -destination "$dest" -derivedDataPath "$dd" \
            -showBuildSettings -json 2>/dev/null |
            jq -c '[.[] | select(.buildSettings.PRODUCT_TYPE == "com.apple.product-type.application")][0].buildSettings // {}')
        app=$(jq -r 'if .TARGET_BUILD_DIR then .TARGET_BUILD_DIR + "/" + .FULL_PRODUCT_NAME else "" end' <<<"$settings")
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
$built && add_check I01-builds reliability true pass "$build_evidence" ||
    add_check I01-builds reliability true fail "$build_evidence"

# 2. Build settings of the app target, as xcodebuild resolves them (xcconfig files included).
if $built; then
    read -r swift_version isolation min_ios bundle_id < <(jq -r '[.SWIFT_VERSION // "-", .SWIFT_DEFAULT_ACTOR_ISOLATION // "-",
        .IPHONEOS_DEPLOYMENT_TARGET // "-", .PRODUCT_BUNDLE_IDENTIFIER // "-"] | @tsv' <<<"$settings")
    evidence="SWIFT_VERSION=$swift_version SWIFT_DEFAULT_ACTOR_ISOLATION=$isolation"
    case $swift_version in 6 | 6.*) swift6=true ;; *) swift6=false ;; esac
    if $swift6 && [ "$isolation" = MainActor ]; then
        add_check I01-app-target-settings reliability false pass "$evidence"
    else
        add_check I01-app-target-settings reliability false fail "$evidence"
    fi
    evidence="IPHONEOS_DEPLOYMENT_TARGET=$min_ios PRODUCT_BUNDLE_IDENTIFIER=$bundle_id"
    if [ "$min_ios" = "$MIN_IOS" ] && [ "${bundle_id#"$BUNDLE_PREFIX"}" != "$bundle_id" ]; then
        add_check I01-profile-facts maintainability true pass "$evidence"
    else
        add_check I01-profile-facts maintainability true fail "$evidence (want $MIN_IOS and prefix $BUNDLE_PREFIX)"
    fi
else
    add_check I01-app-target-settings reliability false fail "no build: $build_evidence"
    add_check I01-profile-facts maintainability true fail "no build: $build_evidence"
fi

# 3. Privacy manifest at the root of the built app.
if $built; then
    manifest=$app/PrivacyInfo.xcprivacy
    if [ -f "$manifest" ] && plutil -lint -s "$manifest" >/dev/null 2>&1 &&
        [ "$(plutil -extract NSPrivacyTracking raw "$manifest" 2>/dev/null)" != "" ]; then
        add_check I01-privacy-manifest security false pass "${app##*/}/PrivacyInfo.xcprivacy is a valid plist with NSPrivacyTracking"
    else
        add_check I01-privacy-manifest security false fail "no valid PrivacyInfo.xcprivacy with NSPrivacyTracking at the root of ${app##*/}"
    fi
else
    add_check I01-privacy-manifest security false fail "no build: $build_evidence"
fi

# 4. The result's own tests, through the scheme's test action.
if $built; then
    with_timeout 1800 xcodebuild test "${container[@]}" -scheme "$SCHEME" -destination "$dest" -derivedDataPath "$dd" \
        -resultBundlePath "$tmp/own.xcresult" CODE_SIGNING_ALLOWED=NO >"$tmp/own.log" 2>&1
    test_cases "$tmp/own.xcresult" >"$tmp/own.jsonl" 2>/dev/null
    read -r own_total own_failed < <(jq -rs --argjson skip "$SCAFFOLD_BUNDLES" '
        [.[] | select(.type == "unit")] as $unit
        | [($unit | map(select(.bundle as $b | $skip | any(.[]; . == $b) | not)) | length),
           ($unit | map(select(.result == "Failed")) | length)] | @tsv' "$tmp/own.jsonl")
    evidence="$own_total unit tests outside the scaffold bundles ran; $own_failed unit tests failed$(jq -rs '
        [.[] | select(.type == "unit" and .result == "Failed") | .id] | if length > 0 then ": " + join(", ") else "" end' \
        "$tmp/own.jsonl" | cut -c1-300)"
    if [ "${own_total:-0}" -ge 1 ] && [ "${own_failed:-0}" -eq 0 ]; then
        add_check I01-unit-tests-pass reliability true pass "$evidence"
    else
        add_check I01-unit-tests-pass reliability true fail "$evidence; $(tail_of "$tmp/own.log")"
    fi
else
    add_check I01-unit-tests-pass reliability true fail "no build: $build_evidence"
fi

# 5. Hidden black-box UI tests on a fresh install of the built app.
ui_checks="testAddAndToggle()=I01-add-and-toggle=reliability testStateSurvivesRelaunch()=I01-state-survives-relaunch=reliability testListScreenAccessibilityAudit()=I01-list-accessibility-audit=accessibility"
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
