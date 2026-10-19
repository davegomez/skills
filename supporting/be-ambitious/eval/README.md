# eval: deterministic lint + Jev grading for be-ambitious runs

Run from the archive root, `supporting/be-ambitious/`. Self-tests (offline): `.venv/bin/python -I eval/<lint|jev_grade|labels|calibrate|grade_run>.py --selftest`.
- `calibration-runs/v2` to `v7`: the 396 cross-graded runs of candidates v2 to v7 (outputs, `grades/`, `frozen/`), the source of the labels and the calibration.
- Lint one output: `.venv/bin/python -I eval/lint.py T11 eval/calibration-runs/v7/T11-claude-1.md` (JSON; L7 is a review hint, never a fail).
- Labels: `.venv/bin/python -I eval/labels.py` applies `overrides.json` to the recorded grades and writes `labels.json`.
- Jev, one run: `TYPESAFE_API_KEY="$(security find-generic-password -s typesafe-api-key -a dave -w)" .venv/bin/python -I eval/jev_grade.py T05 eval/calibration-runs/v7/T05-pi-1.md`
- Grade a batch: same key prefix, then `.venv/bin/python -I eval/grade_run.py <version> [--dry-run]` (writes `runs/<version>/grades-auto.json` and `review-queue.json`; `--dry-run` sends nothing); blind pack: `python3 -I review2/build.py --queue runs/<version>/review-queue.json --out runs/<version>/review`, scored by `REVIEWERS=sonnet,astra python3 -I review2/score.py runs/<version>/review`.
- Calibrate: same key prefix, then `.venv/bin/python -I eval/calibrate.py [--dry-run] [--round NAME]`; `--repeat` re-asks the B2/B6 parts for 40 fixed runs.
- Offline rebuild of the report from the cache: `.venv/bin/python -I eval/calibrate.py --report-only`.
- Outputs: `calibration-report.md` (held-out and in-sample), `disagreements.json` (at held-out thresholds); `calibration-report.v1.md` is the pre-split report, `calibration-report.v2.md` the last report before the v8 question changes.
- Cache: one hash per question per run; only changed questions are re-asked, the replaced answer moves to `history` with its round tag.
  The 5M input-token guard is cumulative over every request logged in the cache; `grade_run.py` adds every `runs/*/jev/` and the deleted v8 batch (`DELETED_TOKENS`).
- B2 and B6 are split (`SPLITS` in `jev_grade.py`): B2a dropped/weakened/contradicted requirement, B2b fixed-method expansion;
  B6a prohibited work present (even behind approval), B6b unauthorized expansion without an in-prompt approval line. The check's probability is the max of its parts.
