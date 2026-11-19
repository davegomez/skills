# Helpers for grade.sh. Bash; source it, do not run it. Each case keeps its own copy, so hidden/ stays
# self-contained. The functions find the result's project from its files, not from a template layout.

# An infrastructure failure: no result is written, and the harness must not count the run.
infra() {
    printf 'grade: infrastructure failure: %s\n' "$*" >&2
    exit 2
}

# Appends 1 check to $CHECKS (JSON lines). Arguments: id priority critical(true|false) result evidence.
add_check() {
    jq -nc --arg id "$1" --arg priority "$2" --argjson critical "$3" --arg result "$4" --arg evidence "$5" \
        '{id: $id, priority: $priority, critical: $critical, result: $result, evidence: $evidence}' >>"$CHECKS" ||
        infra "cannot record check $1"
}

# Writes {"case": ..., "checks": [...]} to $1.
write_result() {
    jq -s --arg case "$CASE" '{case: $case, checks: .}' "$CHECKS" >"$1" || infra "cannot write $1"
}

# Runs a command with a time limit in seconds; on timeout the command gets SIGALRM.
with_timeout() {
    perl -e '$t = shift @ARGV; alarm $t; exec @ARGV or die "exec: $!"' "$@"
}

# Checks the tools and the simulator named by $EVAL_SIM, and boots it.
check_environment() {
    for tool in xcodebuild xcrun jq plutil perl rsync; do
        command -v "$tool" >/dev/null || infra "$tool not found"
    done
    [ -n "${EVAL_SIM:-}" ] || infra "EVAL_SIM is not set (a simulator UDID)"
    xcrun simctl list devices -j | jq -e --arg u "$EVAL_SIM" '[.devices[][] | select(.udid == $u)] | length == 1' >/dev/null ||
        infra "no simulator with UDID $EVAL_SIM"
    xcrun simctl bootstatus "$EVAL_SIM" -b >/dev/null 2>&1 || infra "cannot boot simulator $EVAL_SIM"
}

# Copies the result to $2 without version control, build output, or user state.
copy_result() {
    mkdir -p "$2" && rsync -a --exclude .git --exclude DerivedData --exclude .build --exclude xcuserdata \
        --exclude '*.xcresult' "$1/" "$2/" || infra "cannot copy $1"
}

# Prints the workspace (preferred) or project nearest to the root of $1, as 2 lines: the xcodebuild flag
# and the path. Searches 3 levels deep, so a project in 1 subfolder also counts. Exit 1 when none.
find_container() {
    local kind path
    for kind in xcworkspace xcodeproj; do
        path=$(find "$1" -maxdepth 3 -name "*.$kind" -not -path '*.xcodeproj/*' -not -path '*/.swiftpm/*' \
            -not -path '*/.build/*' 2>/dev/null | awk '{ print length($0) "\t" $0 }' | sort -n | head -n 1 | cut -f2-)
        if [ -n "$path" ]; then
            [ "$kind" = xcworkspace ] && printf -- '-workspace\n%s\n' "$path" || printf -- '-project\n%s\n' "$path"
            return 0
        fi
    done
    return 1
}

# Prints 1 JSON line per test case in xcresult $1: bundle, type (unit or ui), id, result, first failure message.
test_cases() {
    xcrun xcresulttool get test-results tests --path "$1" --format json 2>/dev/null | jq -c '
        .testNodes[] | .. | objects
        | select(.nodeType == "Unit test bundle" or .nodeType == "UI test bundle") as $bundle
        | $bundle | .. | objects | select(.nodeType == "Test Case")
        | {bundle: $bundle.name, type: (if $bundle.nodeType == "UI test bundle" then "ui" else "unit" end),
           id: (.nodeIdentifier // .name), result: .result,
           message: ([.. | objects | select(.nodeType == "Failure Message") | .name][0] // "")}'
}

# The last lines of a log, for evidence.
tail_of() {
    grep -E 'error:|\*\* [A-Z -]+ (FAILED|SUCCEEDED) \*\*' "$1" 2>/dev/null | tail -n 3 | tr '\n' ' ' | cut -c1-400
}
