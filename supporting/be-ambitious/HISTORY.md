# Be-ambitious history, candidates v1 to v11

Claude (Opus 5.5) and Pi (GPT-6.1 Sol) co-wrote the skill as peers on 2026-10-18 and 2026-10-19, from Felix Rieseberg's article and 3 earlier skills, in rounds of independent drafts and cross-critiques until neither had an open objection. Candidate v11 became release 1 (Q13).

## Scores

v2 to v7: 11 cases x 3 runs x 2 models, recorded cross-grades, runs passed of 66. v8 on: lint, Jev, and blind review; runs pass/fail/disputed.

| candidate | sha256 | batch | result | Claude | Pi |
|---|---|---|---|---|---|
| v1 | 837183ba | not run | first merged draft, amended into v2 | | |
| v2 | 04e38791 | 66 | 33 | 8 | 25 |
| v3 | c2f2f6c7 | 66 | 44 | 17 | 27 |
| v4 | e8d80129 | 66 | 49 | 19 | 30 |
| v5 | 2adb48a7 | 66 | 48 | 18 | 30 |
| v6 | 4cacc915 | 66 | 52 | 22 | 30 |
| v7 | 5a97f2da | 66 | 53 | 22 | 31 |
| v8 | 5fc452ca | 54, development | 30/10/14 | 11/8/8 | 19/2/6 |
| v9 | 92eb4ad8 | 54, development | 35/4/15 | 15/4/8 | 20/0/7 |
| v10 | cf0c2de9 | 12, T04 and T13 | 6/2/4 | 1/2/3 | 5/0/1 |
| v11 | f773074d | 5, T13 | 3/1/1 | 0/1/1 | 3/0/0 |

No candidate passed the gate. The frozen copies of v2 to v7 are in `eval/calibration-runs/<v>/frozen/`, of v9 to v11 in `runs/<v>/frozen/`; v1 and v8 are gone. Details: [`runs/v9/RESULT.md`](runs/v9/RESULT.md), [`runs/v10/RESULT.md`](runs/v10/RESULT.md), [`runs/v11/RESULT.md`](runs/v11/RESULT.md).

## What each candidate fixed

- v2 to v7: recurring failures got fixed phrases (`Assumption:`, `With my approval only:`, `Aim for [target] using [method]`, `Unchanged:`), which helped the most. v7 failed the gate (Claude T05, T07, T08, T09 at 1/3) and hit the predeclared v7 stop.
- v8, from the 2 reviews of v7 and Q1, Q2, Q4: a `First check:` line for reviewer availability; `Judge:` as the last prompt line; each approval line names 1 item the owner did not forbid; target facts from the task, not the runner's session; a bold target (Q2); a small, clear task returns `Unchanged:` (X1). Result: T01 unchanged 6/6, T11 aims at an LCP of about 1 s 10/10, T13 at 18 minutes 10/10, a tools-on run made 0 tool calls.
- v9, E1 to E8 from the v8 failures: no repair for a detail the task leaves open (T08 CI unit); no new method in a repair (T12 out-of-fold); find the row-split loophole (Pi T12); a one-line judge; a First check for a reviewer named anywhere; an inferred goal on an `Assumption:` line; no approval line for an addition that changes what a prohibition protects; no judge check that rejects a correct result. Result: T08 6/6, T12 0 fails, no lint fail.
- v10, F1 to F3 from the v9 failures: target facts inside methods (topology, configuration, history) need a First check; shared-resource effects need approval; the judge compares the whole expected result. F3 fixed T04; F1 and F2 did not fix Claude on T13.
- v11, Q12: 1 sentence replaced; tuning the task's own connections and objects is in scope, a load test on a shared live system needs approval. No B3 fail remains on T13; 1 Claude B6 fail with different reasons per reviewer.

## Owner decisions

- Q1 (2026-10-18): a fixed-method task returns unchanged by default; a repair only for a loophole the task text shows, with no added analysis, metric, or threshold, on its own approval line.
- Q2 (2026-10-18): the stretch target lies past the field's "good" threshold, else 1 order of magnitude past the stated bar.
- Q3 (2026-10-18): the budget for model calls; asked, no separate answer recorded; Q5, Q10, and Q11 set the limits.
- Q4 (2026-10-18): an exclusive output may get a separate validation note on its own approval line.
- Q5 (2026-10-19): Claude limit $10 for the v8 work.
- Q6 (2026-10-19): skip the executor rerun.
- Q7 (2026-10-19): Sonnet 5.5 medium replaces Fable as the second reviewer.
- Q8 (2026-10-19): write v9.
- Q9 (2026-10-19): an owner rule the fixed judge cannot detect is a loophole; a repair that only enforces it passes.
- Q10 (2026-10-19): Claude limit $4.00 for the v9 batch and its review.
- Q11 (2026-10-19): option O1, a v10 fix check on T04 and T13, limit $1.10.
- Q12 (2026-10-19): the v11 rule above; 1 more T13 check approved, limit $0.60.
- Q13 (2026-10-19): candidate v11 becomes release 1.
- Q14 to Q16 (2026-10-19): consolidate this archive with no backup; move the calibration runs into `eval/`; keep the executor scripts and results, delete its logs, packages, and fixtures.
- Q19 to Q21 (2026-10-19): release 1 is the defined version. Later changes follow the maintenance process in [README.md](README.md): $1.00 cap per change, Pi as the reviewer, no full batch unless the owner asks for a new release. The gate below is retired. Q17 and Q18 (batch size and executor cap for a new gate) lapsed with it.

The full rule text is in [`review2/INTERPRETATIONS.md`](review2/INTERPRETATIONS.md) and [`rubric.md`](rubric.md).

## Retired gate (PR9)

A candidate needed one predeclared acceptance batch where every case and model cell passed at least 2 of 3 runs, at least 60 of 66 runs passed, there were zero adjudicated B1, B2, B3, B4, B6, or B7 failures, and both reviewers agreed every remaining failure was noncritical and disclosed. No candidate passed it.

## Review method

- v2 to v7: one fresh grader per run, cross-family (Pi graded Claude runs, Claude graded Pi runs), checked by `validate_grade.py`. Pi and Claude adjudicated disputes in rounds 6 to 12; the accepted changes are `eval/overrides.json`.
- After v7: Fable 5.1 xhigh and Astra xhigh reviewed v7 and the suite. Both found that cross-grading confounds model and grader strictness, so the owner chose measurement first.
- Jev calibration: Jev answered every check for the 396 runs of v2 to v7, and thresholds were chosen per check, held out per candidate, against the recorded grades plus 89 overrides. No check reached the ready bar (held-out balanced accuracy 0.85), so a Jev fail only sends an item to blind review.
- v8 on: lint and Jev route items to 2 blind reviewers. Fable cost $5.12 for 57 items and returned nothing, because `--max-budget-usd` stops only after the turn; the owner rejected Opus as too expensive, and Sonnet 5.5 medium replaced Fable (Q7).

## Executor test

Opus 5.5 executed the original task and the v7 rewrite on 3 fixtures, 3 runs per arm, $34 of the $40 cap ([`exec/results.md`](exec/results.md)). X1 (T01) and X2 (T04) had the same outcome; the X1 rewrite cost 4 times more. X3 (T11): median LCP 1.80 s for the rewrite vs 7.03 s for the original (n=3), at about 7 times the cost. Rewrite runs respected approval lines; 2 of 3 original runs changed the analytics tag without asking.

## Harness lessons

- Pi loads `~/.pi/agent/APPEND_SYSTEM.md` despite `-nc`; use `PI_CODING_AGENT_DIR=/tmp/pi-clean-agent`.
- The Claude base prompt (cwd, git status, date) leaks into tools-off outputs as "facts" about the target.
- Give `pi -p` and `run.sh` `< /dev/null`; the Bash tool's stdin is an open socket and Pi hangs on it. In a background subshell, pass Pi `@file` arguments as absolute paths.
- A cost cap near the expected cost skips runs, because each Claude run in flight reserves `RESERVE_USD`.
- Before a rule or interpretation edit after a batch, check it against the pre-batch rubric text. The first Q9 wording contradicted Q1 and its re-review was invalid.
- Executor sandbox: a `$TMPDIR` path longer than about 30 characters silently falls back to the shared `/tmp/claude-<uid>`; a per-command Bash allowlist denied harmless commands.

## Deleted on 2026-10-19

By owner decision, with no backup: candidates v1 to v10 (`SKILL.v*.md`), the round transcripts and briefs (`claude-*.md`, `pi-*.md`, `BRIEF*.md`), the v7 reviews (`review-fable.md`, `review-astra.md`, `review-summary.html`, `REVIEW-BRIEF.md`), `results-all.md`, `results-v2.md`, `PR9-amendment.md`, `HANDOFF.md`, `grade.sh`, runs v8 and v8-toolson, the raw executor logs (`exec/runs/`), and the v7 review pack in `review2/`. `SKILL.v11.md` was also removed; release 1 and `runs/v11/frozen/SKILL.md` are byte-identical copies. `eval/overrides.json` still names the deleted round files and review items as its sources.

## Changes after release 1

None yet. One line per shipped change: version, reason, cost, result.
