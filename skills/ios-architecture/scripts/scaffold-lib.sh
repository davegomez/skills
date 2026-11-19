# Shared functions for scripts/scaffold and scripts/new-feature. POSIX sh; source it, do not run it.
# sh has no local variables, so each function names its own variables with a leading "_".

LC_ALL=C
export LC_ALL

# Names that collide with Swift keywords or with modules of the template.
RESERVED_NAMES="Any App Core CoreClients CoreTesting DesignSystem FeatureKit Features Foundation \
Networking Observation Persistence Self Swift SwiftUI Testing UIKit XCTest actor any as associatedtype \
async await break case catch class consume continue default defer deinit do else enum extension \
fallthrough false fileprivate for func guard if import in init inout internal is let macro nil open \
operator os package precedencegroup private protocol public repeat rethrows return self some static \
struct subscript super switch throw throws true try typealias var where while"

# macOS mktemp ignores TMPDIR without a template and writes in /var/folders, which a sandbox blocks.
TMP_TEMPLATE=${TMPDIR:-/tmp}
TMP_TEMPLATE=${TMP_TEMPLATE%/}/ios-arch.XXXXXX

die() {
    printf 'error: %s\n' "$*" >&2
    exit 1
}

# ASCII Swift identifier that starts with a letter and is not reserved.
is_identifier() {
    case $1 in
        '' | [!A-Za-z]* | *[!A-Za-z0-9_]*) return 1 ;;
    esac
    case " $RESERVED_NAMES " in
        *" $1 "*) return 1 ;;
    esac
    return 0
}

# Reverse-DNS string: 2 or more labels of letters, digits, and inner hyphens.
is_reverse_dns() {
    case $1 in
        '' | *[!A-Za-z0-9.-]* | .* | *. | *..* | -* | *-.* | *.-* | *-) return 1 ;;
        *.*) return 0 ;;
    esac
    return 1
}

# Version string with 2 or 3 numeric parts: major.minor or major.minor.patch.
is_version() {
    case $1 in
        '' | *[!0-9.]* | .* | *. | *..* | *.*.*.*) return 1 ;;
        *.*) return 0 ;;
    esac
    return 1
}

# Exit status 0 when version $1 is lower than or equal to version $2.
version_le() {
    awk -v a="$1" -v b="$2" 'BEGIN {
        n = split(a, x, "."); m = split(b, y, "."); k = (n > m) ? n : m
        for (i = 1; i <= k; i++) {
            if (x[i] + 0 < y[i] + 0) exit 0
            if (x[i] + 0 > y[i] + 0) exit 1
        }
        exit 0
    }'
}

# Reads "major.minor" from the output of `swift --version` on stdin.
parse_swift_version() {
    sed -n 's/.*Swift version \([0-9][0-9]*\.[0-9][0-9]*\).*/\1/p' | head -n 1
}

# The swift-tools-version of the active toolchain.
tools_version() {
    _version=$(xcrun swift --version 2>/dev/null | parse_swift_version)
    [ -n "$_version" ] || die "cannot read the Swift version from 'xcrun swift --version'"
    printf '%s\n' "$_version"
}

# Copies template directory $1 to $2, then replaces each placeholder in file contents and path names.
# Remaining arguments are sed commands, for example 's|__APP__|MyApp|g'. Validate each value first.
render_template() {
    _src=$1
    _dst=$2
    shift 2
    cp -R "$_src/." "$_dst/" || die "cannot copy $_src"
    _script=$(mktemp "$TMP_TEMPLATE") && _list=$(mktemp "$TMP_TEMPLATE") || die "cannot create a temporary file"
    printf '%s\n' "$@" >"$_script"
    find "$_dst" -type f -exec sed -i '' -f "$_script" {} + || die "cannot replace placeholders"
    # Rename the deepest paths first, so that each parent still has its template name.
    find "$_dst" -depth -name '*__*__*' >"$_list"
    while IFS= read -r _old; do
        _name=$(printf '%s\n' "${_old##*/}" | sed -f "$_script")
        mv "$_old" "${_old%/*}/$_name" || die "cannot rename $_old"
    done <"$_list"
    rm -f "$_script" "$_list"
    _left=$(grep -rlE '__[A-Z][A-Z_]*__' "$_dst"; find "$_dst" -name '*__*__*')
    [ -z "$_left" ] || die "placeholders remain in: $_left"
}

# Assertions for the parsing above. Each script runs them with --self-check.
lib_self_check() {
    for _good in MyApp Checkout A1 my_app; do
        is_identifier "$_good" || die "self-check: is_identifier rejected '$_good'"
    done
    for _bad in '' 1App _App My-App 'My App' class Core SwiftUI "$(printf 'A\nB')"; do
        is_identifier "$_bad" && die "self-check: is_identifier accepted '$_bad'"
    done
    for _good in com.example com.example.app io.my-co; do
        is_reverse_dns "$_good" || die "self-check: is_reverse_dns rejected '$_good'"
    done
    for _bad in '' com .com com. com..x -com.x com-.x com.-x 'com.ex ample' com.ex_ample; do
        is_reverse_dns "$_bad" && die "self-check: is_reverse_dns accepted '$_bad'"
    done
    for _good in 1.0 2.4 3.0.1; do
        is_version "$_good" || die "self-check: is_version rejected '$_good'"
    done
    for _bad in '' 1 1. .0 1..0 1.2.3.4 x.y 1.0b; do
        is_version "$_bad" && die "self-check: is_version accepted '$_bad'"
    done
    version_le 1.0 2.3 || die "self-check: 1.0 <= 2.3"
    version_le 2.3 2.3 || die "self-check: 2.3 <= 2.3"
    version_le 2.10 2.3 && die "self-check: 2.10 > 2.3"
    version_le 2.3.1 2.3 && die "self-check: 2.3.1 > 2.3"
    _sample='swift-driver version: 1.2.3 Apple Swift version 9.8.7 (swiftlang-9.8.7.1 clang-1)'
    [ "$(printf '%s\n' "$_sample" | parse_swift_version)" = 9.8 ] || die "self-check: parse_swift_version"
    [ -z "$(printf 'no version here\n' | parse_swift_version)" ] || die "self-check: parse_swift_version on bad input"
    return 0
}
