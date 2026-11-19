# Shared helpers for the ios-architecture scripts. Source this file; do not run it.
# Patterns use POSIX ERE with [[:space:]], so BSD grep and GNU grep give the same result.

# Literal values of common secret formats. A file that matches never leaves the machine.
SECRET_VALUE_ERE='sk_live_[0-9A-Za-z]{10,}|AKIA[0-9A-Z]{16}|-----BEGIN ([A-Z]+ )?PRIVATE KEY-----|ghp_[0-9A-Za-z]{36}|xox[abprs]-[0-9A-Za-z-]{10,}|AIza[0-9A-Za-z_-]{35}'

# Directories that hold build output or vendored code.
PRUNE_ERE='/(\.git|\.build|DerivedData|Pods|Carthage|node_modules|\.swiftpm)/'

# macOS mktemp ignores TMPDIR without a template and writes in /var/folders, which a sandbox blocks.
TMP_TEMPLATE=${TMPDIR:-/tmp}
TMP_TEMPLATE=${TMP_TEMPLATE%/}/ios-arch.XXXXXX

die() { printf '%s\n' "$*" >&2; exit 2; }

# Set PROJECT to the physical path of directory $1.
set_project() {
  [ -d "$1" ] || die "not a directory: $1"
  PROJECT=$(cd "$1" && pwd -P)
}

# Print file argument $1 relative to PROJECT. Accept a path relative to PROJECT or an absolute path.
rel_path() {
  case $1 in /*) _a=$1 ;; *) _a=$PROJECT/$1 ;; esac
  [ -f "$_a" ] || die "not a file: $1"
  _d=$(cd "$(dirname "$_a")" && pwd -P)
  case $_d/ in "$PROJECT"/*) ;; *) die "outside the project: $1" ;; esac
  _r=${_d#"$PROJECT"}
  _r=${_r#/}
  printf '%s\n' "${_r:+$_r/}$(basename "$_a")"
}

# Print every file of the project relative to PROJECT, without build output.
project_files() {
  (cd "$PROJECT" && find . -type f | grep -vE "$PRUNE_ERE" | sed 's#^\./##' | sort)
}

# Print the change set relative to PROJECT: modified, staged, and untracked files that exist.
change_set() {
  git -C "$PROJECT" rev-parse --is-inside-work-tree >/dev/null 2>&1 || return 0
  {
    git -C "$PROJECT" diff --name-only --relative HEAD 2>/dev/null || git -C "$PROJECT" diff --name-only --relative
    git -C "$PROJECT" ls-files --others --exclude-standard
  } | sort -u | while IFS= read -r _f; do
    [ -f "$PROJECT/$_f" ] && printf '%s\n' "$_f"
  done
}

# Print the "pending:" line of escalated decide result $2 for file $1, with its next action; $3 is the calling script.
pending_line() {
  printf '%s\n' "$2" | jq -r --arg f "$1" --arg s "$3" '
    "pending: \($f): \(.decision): escalate=\(.escalate)"
    + (if .fallback_tier then " tier=\(.fallback_tier)" else "" end)
    + (if .reason then " reason=\(.reason)" else "" end)
    + "; next: run scripts/decide \(.decision) \($f), "
    + (if .escalate == "fallback" then "give only its request object to a subagent of tier \(.fallback_tier)"
       else "decide its request object in the orchestrator" end)
    + ", record that answer with scripts/decide --resolve \(.decision) \($f) --answer <json> --source \(.escalate)"
    + ", then run scripts/\($s) again"'
}

# Print the "decided:" line of decide result $2 for file $1 when Jev gave the result.
jev_line() {
  printf '%s\n' "$2" | jq -r --arg f "$1" 'select(.source == "jev") | "decided: \($f): \(.decision): jev model \(.model // "unknown")"'
}

# Print the Swift package target that holds path $1, or nothing.
target_of() {
  printf '%s\n' "$1" | sed -n 's#^\(.*/\)\{0,1\}Sources/\([^/]*\)/.*#\2#p'
}

# Print the kind of Swift path $1: test, domain, feature, or src.
swift_kind() {
  case $1 in
    *Tests/* | *Tests.swift) echo test; return ;;
  esac
  case $(target_of "$1") in
    *Domain) echo domain ;;
    *Feature) echo feature ;;
    *) echo src ;;
  esac
}
