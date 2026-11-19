#!/bin/sh
# Run every labeled calibration fixture through scripts/decide with real Jev calls.
# Prints 1 TSV line per fixture: decision, input, expected, source, answer, probabilities, model.
# Each line costs 1 Jev request. The run test suite does not call this script.
set -u
here=$(cd "$(dirname "$0")" && pwd -P)
decide=$here/../../../skills/ios-architecture/scripts/decide
cal=$here/fixtures/calibration
tab=$(printf '\t')
cd "$cal" || exit 2
grep -v '^#' labels.tsv | while IFS=$tab read -r id input expected; do
  [ -n "${ONLY:-}" ] && [ "$id" != "$ONLY" ] && continue
  if [ -f "$input" ]; then out=$("$decide" "$id" "$input"); else out=$("$decide" "$id" $input); fi
  printf '%s\t%s\t%s\t%s\n' "$id" "$input" "$expected" \
    "$(printf '%s' "$out" | jq -r '[.source, (.answer | tojson), (.probabilities | tojson), (.model // "-"), (.reason // "-")] | join("\t")')"
done
