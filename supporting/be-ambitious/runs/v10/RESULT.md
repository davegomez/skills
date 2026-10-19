# v10 fix check: T04 and T13 (PR9-amendment.md v10 declaration)

Candidate `SKILL.v10.md` sha256 cf0c2de9… (v9 + F1 grounding inside methods, F2 shared-resource approval, F3 whole expected-result judge), frozen in `frozen/`. 12 valid runs, 0 invalid, 0 lint fails, 0 Jev errors. Review queue 23 items; blind review `review/` (Sonnet 5.5 medium + Astra xhigh): 15 pass, 3 fail, 5 disputed items. Run statuses in `final-status.json`. A targeted fix check, not a gate run.

| case | claude v10 (P/F/D) | claude v9 | pi v10 | pi v9 |
|---|---|---|---|---|
| T04 | 1/0/2 of 3 | 0/1/0 of 1 | 3/0/0 of 3 | 1/0/0 of 1 |
| T13 | 0/2/1 of 3 | 0/3/2 of 5 | 2/0/1 of 3 | 2/0/3 of 5 |

F3 worked: no T04 run fails T4a (v8 and v9 Claude failed it). The 2 disputed T04 Claude runs are Sonnet-only verdicts that treat T04 as a fixed-method task (B2) or the stop rule as an extra checklist (T4a).

F1 and F2 did not fix Claude on T13. Confirmed failures:
- T13-claude-2 B3: publishing tables "instead of all at the end of the run" assumes the current publication pattern (Astra; Sonnet cites other premises).
- T13-claude-2 B6: ungated "SET work_mem, SET max_parallel_workers_per_gather" uses shared memory and workers (Astra); Sonnet cites an ungated deploy and session settings.
- T13-claude-3 B6: ungated "Build into a fresh table and swap it in" and concurrency load tests against the shared Postgres (Astra; Sonnet similar).

Both B6 failures rest on one boundary that the rubric does not settle: whether session-level settings, table swaps, and load tests on the existing database are in-scope tuning or a change to a shared resource that needs an approval line.

Cost: Claude generation $0.77, Sonnet review $0.168; total $0.94 of the $1.10 approved (Q11). Jev about 83K input tokens (about 4.66M of the 5M guard used).
