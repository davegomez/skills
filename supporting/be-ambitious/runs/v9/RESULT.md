# v9 development batch: result against PR9-amendment.md (v9 declaration)

Candidate `SKILL.v9.md` sha256 92eb4ad8…, rubric 8e8c5396…, interpretations a663b79b…, frozen in `frozen/`. 54 valid runs, 1 invalid attempt (T02-claude-1, stopped by the operator before publish when the batch was restarted with `< /dev/null` for Pi). Grading: `grades-auto.json` (lint + Jev, 0 lint fails, 0 Jev errors), `review-queue.json` (74 items), blind review `review/` (Sonnet 5.5 medium + Astra xhigh), `review/result.md` (44 pass, 4 fail, 26 disputed items), run statuses in `final-status.json`.

Gate: FAIL. Confirmed critical failures exist (B3, B6 on T13-claude), and 2 cells cannot reach their bar (T04 claude 0/1, T13 claude at most 2/5). The overall rate is 35/54 confirmed (64.8%), 50/54 (92.6%) even if every disputed run passed, against 60/66 (90.9%).

| case | claude (P/F/D of n) | pi (P/F/D of n) | v8 claude | v8 pi |
|---|---|---|---|---|
| T01 | 3/0/0 of 3 | 3/0/0 of 3 | 3/0/0 | 3/0/0 |
| T02 | 1/0/0 of 1 | 1/0/0 of 1 | 0/0/1 | 1/0/0 |
| T03 | 1/0/0 of 1 | 1/0/0 of 1 | 0/0/1 | 1/0/0 |
| T04 | 0/1/0 of 1 | 1/0/0 of 1 | 0/1/0 | 1/0/0 |
| T05 | 0/0/1 of 1 | 0/0/1 of 1 | 0/1/0 | 1/0/0 |
| T06 | 0/0/1 of 1 | 1/0/0 of 1 | 1/0/0 | 0/0/1 |
| T07 | 1/0/0 of 1 | 1/0/0 of 1 | 0/0/1 | 1/0/0 |
| T08 | 3/0/0 of 3 | 3/0/0 of 3 | 0/2/1 | 3/0/0 |
| T09 | 0/0/1 of 1 | 1/0/0 of 1 | 0/1/0 | 1/0/0 |
| T10 | 1/0/0 of 1 | 1/0/0 of 1 | 1/0/0 | 1/0/0 |
| T11 | 4/0/1 of 5 | 5/0/0 of 5 | 4/0/1 | 3/0/2 |
| T12 | 1/0/2 of 3 | 0/0/3 of 3 | 0/1/2 | 0/2/1 |
| T13 | 0/3/2 of 5 | 2/0/3 of 5 | 2/2/1 | 3/0/2 |

Claude 15 pass, 4 fail, 8 disputed of 27 (v8: 11/8/8). Pi 20 pass, 0 fail, 7 disputed of 27 (v8: 19/2/6).

Confirmed failures (both reviewers say fail; for 3 of 4 the 2 reviewers give different reasons, which the declared rule still counts as a fail):
- T04-claude-1 T4a: a judge built on `cmp -l` and byte sizes that does not establish the expected insertion (both reviewers).
- T13-claude-1 B6: Sonnet, an approval-gated shadow run and a production deploy; Astra, pool and max_active_tasks changes not limited to the DAG's own resources.
- T13-claude-2 B3: Sonnet, assumed history and query statistics; Astra, "still publishes the full set as it does today", a target fact not in the task.
- T13-claude-4 B3: Sonnet, assumed metadata sources; Astra, "Treat the single Postgres server as a shared queue", an unstated topology.

What v9 fixed: T08 6/6 pass, every run makes only the Q9 freeze repair and no run changes the CI method (v8: 2 Claude fails). T12 0 fails: all 6 runs name both loopholes with the quoted task text (v8: Pi 0 of 3 found the row split); the open T12 items are T12a disputes about extra audit-rubric or freeze lines. No lint fail (v8: T09 L1). T05 and T09 moved from fail to disputed.

What remains: Claude on T13 states target facts that the task does not give (B3) and gates operational changes (B6). These are 3 of the 4 confirmed failures.

Cost: Claude generation $3.24 (including the stopped run, $0.167), Sonnet review $0.479; total $3.72 of the $4.00 approved for v9 (Q10). Jev about 0.36M input tokens (about 4.64M of the 5M guard used). Pi and Astra on the OAuth subscription.
