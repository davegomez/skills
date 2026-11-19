#!/usr/bin/env bash
# Hidden grader for I05 (read-only review).
# Usage: grade.sh <work-dir> <out.json>
# Optional EVAL_VARIANT=seeded|clean; without it the grader infers the variant from the tree.
# No build and no simulator: the task edits no code. Exit 0 when it wrote a result; 2 on an infrastructure failure.
set -euo pipefail
[ $# -eq 2 ] || { echo "usage: grade.sh <work-dir> <out.json>" >&2; exit 2; }
HERE=$(cd "$(dirname "$0")" && pwd)
exec python3 -I "$HERE/grade_review.py" "$(dirname "$HERE")" "$1" "$2"
