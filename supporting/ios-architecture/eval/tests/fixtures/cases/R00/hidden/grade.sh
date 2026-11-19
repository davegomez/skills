#!/bin/sh
# Toy hidden review grader: the seeded diff needs the finding, the clean diff needs no finding.
set -u
w=$1 out=$2
[ -n "${EVAL_SIM:-}" ] || { echo 'EVAL_SIM is not set' >&2; exit 3; }
text=$(cat "${EVAL_FINAL_TEXT:-/dev/null}")
if grep -q 'log(email)' "$w/app.txt"; then
  f=fail; printf '%s' "$text" | grep -q 'app.txt:2' && f=pass; c=na
else
  f=na; c=pass; [ -n "$text" ] || c=fail; printf '%s' "$text" | grep -qi 'issue' && c=fail
fi
printf '{"case": "R00", "checks": [{"id": "R00-finds-log", "priority": "security", "critical": true, "result": "%s", "evidence": "review text"}, {"id": "R00-no-false-alarm", "priority": "reliability", "critical": true, "result": "%s", "evidence": "review text"}]}\n' "$f" "$c" >"$out"
