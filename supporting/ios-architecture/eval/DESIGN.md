# Agreed design: ios-architecture evaluation suite

Agreed design of the evaluation suite. The case format is in [CASES.md](CASES.md).

## Question
Does the new skill give better iOS results than the old skill (`0ab47d0`), in the owner's order: quality first, then cost and time?

## Before any paid run (C1)
Fix 2 defects, add offline regression tests for them, then freeze the new arm:
- `route` routes only the git change set, so it routes nothing before the first edit (`scripts/lib/common.sh:35-43`).
- `check` cannot accept a resolved escalation, so it never exits 0 after a Jev escalation (`scripts/check:367-394, 430-434`).
The result compares the old skill with the fixed candidate.

## Layer 1: end-to-end study (answers the question)
- Arms: old, new (frozen full copy, live Jev with synthetic code, observed model id verified, halt on drift), no-skill control (descriptive only).
- Builder: 1 pinned Claude Code model and effort, headless, structured output; exit-3 fallback tiers and the exit-4 policy pinned before the pilot.
- Cases (independent fixtures, reference solutions, negative variants, hidden tests outside the builder's tree):
  - I01 new project from a profile (offline packing list).
  - I02 new feature in a frozen scaffold-made app.
  - I03 deep link with a confirmation step, in an independently authored app.
  - I04 migration of 1 UIKit screen into a local package.
  - I05 read-only review of a seeded diff, plus 2 clean-diff pairs as a separate stratum (C7).
  - I06 authenticated list: networking states, retry matrix, localization in a second locale, no token in logs or preferences (C3).
- Primary endpoint: independently accepted delivery per attempted run; per-case and per-dimension reports; no weighted score.
- Graders: build, tests, hidden acceptance tests, XCUI accessibility audit, parsed configuration; blind tools-off Pi reviewer with neutral IDs and a second adjudication. New `check` is a separate diagnostic, never a grade.
- Performance is not claimed (no stable timed workload).

## Layer 2: offline component regression gates (for later skill changes) (C4)
- Route: pre-edit and post-edit routing scored separately against frozen required and optional rows.
- Check: seeded and clean inputs; detections, false flags, suppressions, clears, and pending decisions reported separately; replay keyed to the exact request and model id.
- Scaffold: the existing suite plus a simulator `xcodebuild test` that proves the accessibility audit ran.

## Budget (owner approval required for each stage) (C6)
- Pilot: 12 runs (1 old/new pair per case), cap $20. It is the paid study.
- The size of a paid evaluation matches the value of the decision. The main batch (82 runs, $114) was dropped on 2026-11-19 because its cost did not match the value of the ship-or-keep decision.
- Total ceiling: $20. Caps of 15 minutes per run and 40 machine hours. A pair starts only when its worst-case cost fits.
- Later skill changes use the Layer 2 gates only. A paid check needs the owner's approval and its own cap.

## Not verified
Current Jev model id and prices, real classification quality today, fallback completion, case difficulty, reviewer agreement, and telemetry parity for delegated usage.
