#!/bin/sh
# Tests skills/ios-architecture/scripts/scaffold and new-feature end to end. Needs Xcode.
# usage: run-scaffold-tests.sh        (KEEP=1 keeps the temporary folder for inspection)
set -u

repo=$(cd "$(dirname "$0")/../../.." && pwd) || exit 1
scripts=$repo/skills/ios-architecture/scripts
tmp=$(mktemp -d) || exit 1
[ "${KEEP:-}" = 1 ] && echo "temporary folder: $tmp" || trap 'rm -rf "$tmp"' EXIT
trap 'exit 1' HUP INT TERM
pass=0
fail=0

ok() { pass=$((pass + 1)); printf 'ok    %s\n' "$1"; }
not_ok() { fail=$((fail + 1)); printf 'FAIL  %s\n' "$1"; [ -f "$tmp/log" ] && tail -n 30 "$tmp/log" | sed 's/^/      /'; }

# expect_pass <name> <command...>: the command exits 0.
expect_pass() {
    name=$1; shift
    if "$@" >"$tmp/log" 2>&1; then ok "$name"; else not_ok "$name"; fi
}

# expect_fail <name> <message-pattern> <command...>: the command exits non-zero and prints the pattern.
expect_fail() {
    name=$1; pattern=$2; shift 2
    if "$@" >"$tmp/log" 2>&1; then
        not_ok "$name (exit status 0)"
    elif grep -q -- "$pattern" "$tmp/log"; then
        ok "$name"
    else
        not_ok "$name (no message matching '$pattern')"
    fi
}

GOOD_PROFILE='{"app_name":"MyApp","bundle_id_prefix":"com.example","minimum_ios":"MIN","team_size":3,
"regulated_data":false,"cross_device_sync":false,"cross_platform_accounts":false,"store":"files",
"code_may_leave_machine":true}'
sdk=$(xcrun --sdk iphoneos --show-sdk-version) || { echo "Xcode is not installed" >&2; exit 1; }

# new_target <dir> <jq-patch>: a folder with a profile, changed by the jq patch.
new_target() {
    mkdir -p "$1" && printf '%s' "$GOOD_PROFILE" | sed "s/MIN/$sdk/" | /usr/bin/jq "$2" >"$1/ios-architecture.json"
}

build_app() {
    xcodebuild -workspace "$app/MyApp.xcworkspace" -scheme MyApp -destination 'generic/platform=iOS Simulator' \
        -derivedDataPath "$tmp/derived" CODE_SIGNING_ALLOWED=NO "$@"
}

swift_package() {
    (cd "$1" && swift build --build-path "$tmp/swiftpm/${1##*/}" && { [ ! -d Tests ] || swift test --build-path "$tmp/swiftpm/${1##*/}"; })
}

echo "# self-checks"
expect_pass "scaffold --self-check" "$scripts/scaffold" --self-check
expect_pass "new-feature --self-check" "$scripts/new-feature" --self-check

echo "# profile validation"
n=0
for case in \
    'del(.store)|store: missing' \
    '.app_name = "1App"|app_name' \
    '.app_name = "class"|app_name' \
    '.app_name = "Core"|app_name' \
    '.bundle_id_prefix = "example"|bundle_id_prefix' \
    '.bundle_id_prefix = "com.ex ample"|bundle_id_prefix' \
    '.minimum_ios = "latest"|minimum_ios' \
    '.minimum_ios = "999.0"|newer than the iOS SDK' \
    '.team_size = 0|team_size' \
    '.team_size = "3"|team_size: must be a number' \
    '.regulated_data = "yes"|regulated_data: must be a boolean' \
    '.store = "realm"|store: must be' \
    '[.]|must be a JSON object'; do
    n=$((n + 1))
    new_target "$tmp/bad$n" "${case%%|*}"
    expect_fail "rejects profile: ${case%%|*}" "${case#*|}" "$scripts/scaffold" "$tmp/bad$n"
    [ "$(ls -A "$tmp/bad$n")" = ios-architecture.json ] || not_ok "failed run left files in $tmp/bad$n"
done
mkdir "$tmp/nojson" && printf '{' >"$tmp/nojson/ios-architecture.json"
expect_fail "rejects a profile that is not JSON" "not valid JSON" "$scripts/scaffold" "$tmp/nojson"
mkdir "$tmp/noprofile"
expect_fail "rejects a target with no profile" "not found" "$scripts/scaffold" "$tmp/noprofile"
new_target "$tmp/nonempty" . && touch "$tmp/nonempty/README.md"
expect_fail "rejects a non-empty target" "must contain only" "$scripts/scaffold" "$tmp/nonempty"
[ ! -e "$tmp/nonempty/App" ] || not_ok "scaffold wrote into a non-empty target"

echo "# regulated data"
new_target "$tmp/regulated" '.regulated_data = true'
expect_pass "scaffold with regulated_data" "$scripts/scaffold" "$tmp/regulated"
expect_pass "regulated entitlements use NSFileProtectionComplete" \
    grep -q '<string>NSFileProtectionComplete</string>' "$tmp/regulated/App/MyApp/MyApp.entitlements"
expect_pass "regulated file store uses .completeFileProtection" \
    grep -q 'protection: .completeFileProtection$' "$tmp/regulated/App/MyApp/MyApp.swift"

echo "# scaffold"
app=$tmp/app
new_target "$app" .
expect_pass "scaffold" "$scripts/scaffold" "$app"
expect_fail "rejects a second scaffold into the same target" "must contain only" "$scripts/scaffold" "$app"
expect_pass "no placeholders remain" sh -c "! grep -rlE '__[A-Z][A-Z_]*__' '$app' && [ -z \"\$(find '$app' -name '*__*__*')\" ]"
expect_pass "swift-tools-version is read from the toolchain" \
    grep -q "^// swift-tools-version: $(xcrun swift --version 2>/dev/null | sed -n 's/.*Swift version \([0-9]*\.[0-9]*\).*/\1/p')$" \
    "$app/Packages/Core/Package.swift"
expect_pass "minimum iOS comes from the profile" grep -q "IPHONEOS_DEPLOYMENT_TARGET = $sdk$" "$app/App/Config/Shared.xcconfig"
for package in Core DesignSystem Networking Persistence; do
    expect_pass "swift build and test: $package" swift_package "$app/Packages/$package"
done
expect_pass "xcodebuild build: app" build_app build

echo "# new-feature"
expect_fail "rejects a lowercase name" "uppercase" "$scripts/new-feature" "$app" checkout
expect_fail "rejects a non-identifier name" "Swift identifier" "$scripts/new-feature" "$app" "Check-out"
expect_fail "rejects a reserved name" "Swift identifier" "$scripts/new-feature" "$app" Networking
expect_fail "rejects the app name" "differ from the app name" "$scripts/new-feature" "$app" MyApp
expect_fail "rejects a folder with no project" "not found" "$scripts/new-feature" "$tmp/noprofile" Checkout
expect_pass "new-feature Checkout" "$scripts/new-feature" "$app" Checkout
cp -R "$app" "$tmp/before-duplicate"
expect_fail "rejects a duplicate feature" "already exists" "$scripts/new-feature" "$app" Checkout
expect_pass "duplicate run changes nothing" diff -r -x .build "$tmp/before-duplicate" "$app"
expect_pass "composition root registers CheckoutEntry once" \
    sh -c "[ \"\$(grep -c 'registry.register(CheckoutEntry())' '$app/App/MyApp/MyApp.swift')\" = 1 ]"
expect_pass "project file is a valid property list" plutil -lint "$app/App/MyApp.xcodeproj/project.pbxproj"
expect_pass "test plan lists the feature tests" /usr/bin/jq -e \
    '[.testTargets[].target.name] | contains(["CheckoutDomainTests", "CheckoutFeatureTests"])' "$app/ci/test-plan.xctestplan"
expect_pass "swift build and test: Checkout" swift_package "$app/Packages/Features/Checkout"
expect_pass "xcodebuild build: app with Checkout" build_app build
expect_pass "xcodebuild build-for-testing: test plan" build_app build-for-testing
expect_pass "new-feature Settings (second feature)" "$scripts/new-feature" "$app" Settings
expect_pass "new-feature Out (a suffix of an existing name)" "$scripts/new-feature" "$app" Out
expect_pass "xcodebuild build: app with 3 features" build_app build

echo "# result: $pass passed, $fail failed"
[ "$fail" -eq 0 ]
