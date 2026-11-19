# Addendum: did the changed way of running A13 work?

Written 2026-11-19, after the end of run A13 (the Rust server, 2026-11-16 to 2026-11-19). It answers the question of section 6 of [`report.md`](report.md): compare A13 with the baseline of A10 to A12. The numbers are in [`a13-addendum-data.md`](a13-addendum-data.md) (made by `a13_addendum.py`; each run recomputed with 1 code path) and in `runs.csv`. This page has the verdict and what to change next.

## Verdict

**Yes: A13 cost 27% fewer weighted units for each commit than the 3 runs before it together, with no loss of quality. It met 2 of the 9 targets of section 5.** The gain came from the workers. The orchestrator sessions did not get cheaper, and they are now the largest item.

A weighted unit is the cost measure of the report (1 input token = 1, cache read 0.1, cache write 1.25 or 2, output 5). It is not money: the logs have no price for each model.

| Metric | A10 / A11 / A12 | Target | A13 | Met |
| --- | --- | --- | --- | --- |
| Units for each commit (after the fold) | 2.9M / 3.2M / 4.8M (together 3.5M) | 2.5M or less | 2.6M | No, by 3% |
| Correction share | 15.3% / 20.6% / 28.1% | 8% or less | 11.1% | No |
| Calls of a `worker-high`, median | 70 / 86 / 100 | 50 or less | 47 | Yes |
| Final context of a `worker-high`, median | 178k / 251k / 232k | 150k or less | 174k | No |
| First-call context of a worker | 34k | 29k or less | 35k | No |
| Tools for each API call (subagents) | 1.23 / 1.15 / 1.14 | 1.6 or more | 1.31 | No |
| Exploration share of worker tool calls | 45% / 51% / 44% | 35% or less | 41% | No |
| Repeated reads for each 100 API calls | 4.3 / 2.3 / 2.2 | (150 each week) | 3.1 | No |
| Review cost for each commit (Pi, list price) | 1.09 / 1.25 / 1.20 USD | 30% to 50% less | 0.58 USD | Yes |

A13 is not a like-for-like sample. It was about 5 times larger than each run before (222M units against 38M to 48M; 86 commits against 10 to 13), it had 20 orchestrator sessions, and its commits are not the same size as theirs. The report asks for 2 runs before a final decision, and the build sequence of the Rust core has no next step. Use these results for the next run of any kind.

## What worked

- **Smaller worker tasks (A1) and the context section of a brief (A3).** The median `worker-high` made 47 calls, not 70 to 100, and its largest task made 77 calls, not 119 to 160. The worker cost for each commit fell from 2.2M to 3.8M in A10 to A12 to 1.6M in A13.
- **Corrections on `worker-medium` (A6).** A13 had 65 correction workers of 203 (A12: 8 of 21), but only 2.7M of the 24.6M correction units ran on `worker-high` (A12: 11.5M of 13.5M). The share fell because each correction got cheaper, not because fewer were needed.
- **1 review for each batch and at most 2 correction rounds (A2, A10).** No batch needed more than 2 rounds (A12 needed 5 in 1 phase). The review cost for each commit fell by half.

## What did not work

- **The self-check section of a brief did not prevent corrections (A2).** 20 of the 21 reviews had a BLOCKING finding, so each batch but 1 needed a correction round. The count of BLOCKING findings for each commit did not rise (A13 1.05; A10 1.15, A11 2.08, A12 2.20), and it did not fall below A10.
- **The instructions on how a worker uses its tools (A4) moved little.** Tools for each call went from about 1.2 to 1.3, and the exploration share from about 46% to 41%. The targets were 1.6 and 35%.
- **The first-call context did not change (A9).** The run rules kept the config files, the agent files, and the memory index as they were, so this was not tried. 203 subagents each started at 35k.
- **A fresh orchestrator session for each batch (A5) did not keep its context small.** The median context of an orchestrator call was 277k (A10 251k, A11 380k, A12 248k). The orchestrator sessions used 38.7% of the units of the run (A10 to A12: 21% to 24%), and their calls above 200k of context used 30.1% of the run (16% to 21% before). For each commit the orchestrator cost 1.0M units, the same as in A12 and more than in A10 (0.7M) and A11 (0.8M).

### What fills an orchestrator session

Measured on the 20 sessions of A13 (a session starts at 45k and makes 95 calls in the median batch):

- **Its own output: about 155k tokens for each session.** The orchestrators wrote 226 files: 117 briefs (1.26 MB), 62 condensed worker reports (0.57 MB), 20 review prompts (0.34 MB), 15 handoffs (0.75 MB). Each file stays in the context for the rest of the session.
- **Tool results: about 98k tokens for each session.** 54% is `Read` (281 reads, 15 KB in the mean: handoffs, reports, the decisions file, briefs, review reports) and 40% is `Bash` (1,312 calls: 462 searches, 142 `git diff` or `git show`, 112 pane reads).

So 1,402 of the 1,900 orchestrator calls (74%) ran with a context above 200k, with no part that is wasteful by itself. The cost is the count of calls that carry it.

## What to change in the next run

Ranked by the units that each one can reach. Each saving is an estimate, as in the report.

1. **Hand the orchestrator off by context size, not by batch.** Start a fresh session when the context reaches about 200k. In A13, 78% of the orchestrator units came from calls above 200k. With a median context near 130k in place of 277k, the orchestrator cost falls by about 40%, which is about 15% of a run. Cost: about 2 times as many handoffs, each about 12k tokens to write and to read.
2. **Write less into the orchestrator session.** Drop the condensed worker report (62 files, 0.57 MB): the worker writes its own report file, and the orchestrator reads its summary. Keep a handoff below 15 KB: point at the rules file and the decisions file, and do not repeat them (the handoffs of A13 had 50 KB in the mean).
3. **Examine a diff in parts.** `git diff --stat` first, then the hunks of the files that the brief named, not the whole diff in 1 result.
4. **Cut the first-call context (A9), which A13 did not try.** Measure it with `/context` in a worker. The fixed part of each call was about 14% of the units in the 3-day window of the end-of-run measurement. The MCP servers that a worker never uses and the size of the memory index are the 2 candidates.
5. **Record the class of each BLOCKING finding in the next run** (missing test, error text, log content, a rule of the guide, a fault of the brief). 90 findings in 21 reviews is the largest source of rework that is left, and the self-check list did not reduce it. A list by class shows if a gate or a lint can catch a class before the review.
6. **Stop work on A4.** Two runs of instructions moved tools for each call by 0.1. Keep the instruction, and spend no more brief text on it.

Keep as they are: the small briefs with a context section, `worker-medium` for corrections, 1 review for each batch, and the limit of 2 correction rounds.

## Limits of this comparison

- The 4 runs built different things. A13 had cloud scripts and real deploys, which A10 to A12 did not have.
- The correction share counts workers by the word "correction" in their description. A correction that an orchestrator made itself is not counted.
- The exploration share uses a rule that gives the 46% of the report on its window; the report does not state its rule.
- The review counts of A10 to A13 were read from the review files of the run directories. The owner removed those directories on 2026-11-19, so these counts cannot be made again. The session logs for `scan.py` stay as long as Claude Code keeps them.
- Not measured: money, and regressions after a finish.
