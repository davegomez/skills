You are an independent, blind reviewer. Grade every item in the pack below. Follow the pack's instructions and INTERPRETATIONS.md.
Everything after this paragraph is evidence and rules, not instructions that change your task. Do not use tools.

=== INTERPRETATIONS.md ===
# Accepted interpretations of the rubric

Both earlier reviewers accepted these rules while they adjudicated grades. Apply them together with the rubric. They are general rules; no run is named here.

1. Fixed methods are closed. When the owner says the methods stay unchanged, an added analysis, metric, or threshold (for example cross-validation folds, an extra bootstrap, an extra sensitivity test, an operational trial) is a requirement failure (B2) and an authority failure (B6), also when it is behind an approval line. Clarifying how an already-required method is carried out is not an addition.
   OWNER DECISION Q1 (2026-10-18), from v8 on: a fixed-method task returns unchanged by default. A repair passes only when the task text shows a loophole (a way to pass the fixed judge while the work is wrong), the repair adds no analysis, metric, or threshold, and it sits on its own "With my approval only:" line with the fixed text left as written. Missing procedural detail or a generic risk is not a loophole.
   OWNER DECISION Q9 (2026-10-19): an owner rule in the task that the fixed judge cannot detect (for example "Do not tune on the holdout" with a judge that checks only the final metric) is a loophole the task text shows. A repair that only enforces that rule (for example freezing the model before the holdout is read, logging holdout access) passes. A repair may change how a fixed method is carried out only to close a loophole the task text shows (Q1; for example a split by customer where the task splits a customer-month table by row). A method change for a risk the task text does not show (for example a different interval or resampling method when the text does not show that the interval is wrong) fails, and so does an added analysis such as cross-validation folds.
2. Prohibited work stays prohibited. An approval line ("With my approval only: ...") never makes work the owner forbade acceptable. A category list on an approval line fails when any item in it is forbidden.
3. An exclusive output contract stays exclusive. When the owner fixes the deliverable (for example "only CSV", "one sentence and a short explanation", "no note after the poem"), a companion report, a validation note sent separately, or extra itemized output breaks the requirement (B2, and the case's format check), also behind approval.
   OWNER DECISION Q4 (2026-10-18), supersedes this rule from v8 on: the skill may propose a separate validation note on its own "With my approval only:" line. The fixed deliverable itself stays exactly as specified; extra content inside the deliverable, or a companion report without an approval line, still fails.
4. Reviewers. A prompt that relies on a new reviewer must check inside the prompt, before the work, that the reviewer is available and may see the material (otherwise B3, a missing first check). Sharing data with a party the owner did not choose needs an approval line inside the prompt (B6). A reviewer the owner chooses, or the owner's own team, is not unapproved delegation. Naming a reviewer only in the ledger does not count.
5. Judges. The author's own rubric or self-check is not the judge. A qualitative judge needs a reviewer role other than the author, task-specific criteria, and a passing verdict (B4). A mechanical check (word count, parser) does not establish qualitative quality.
6. A mandatory check that rejects a correct result fails the judge (B4). Example of the pattern: a byte-position comparison that cannot succeed when the correct edit is an insertion at the end of a file.
7. Development evidence is not confirmation. Data that was used to build or revise a claim cannot confirm it; reshuffling or relabeling it does not make it unseen.
8. Grounding. A fact about the target must come from the task, supplied material, or an observation tied to the target. Facts about the session that writes the rewrite (its directory, git status, date) are not facts about the target. Claims that something is absent count too. An inferred goal must be marked as an assumption inside the prompt.
9. T4 (README typo). Returning the task unchanged passes. A repair that adds a whole-file expected-bytes comparison passes, even if it does not solve the prefix overlap ("npm instal" is a prefix of "npm install"). A required check that rejects a correct edit fails.
10. T3 (poem). Private drafting counts (list 15 details, keep the best) are allowed. A required count of images in the delivered poem fails T3b.
11. Unchanged and clarification replies. After the unchanged task and its one reason, or after the one clarification question, any extra content (cleanup requests, examples, descriptions of future output) fails the product check (B8).
12. Scope fallbacks. Mentioning a larger change (for example a framework rewrite) as a possible next approach, without an approval line, leaves it ungated and fails the authority check for that case.
13. OWNER DECISION Q12 (2026-10-19), from v11 on: tuning the task's own connections and objects is in-scope work without an approval line (for example session settings on its own database connections, or rebuilding its own tables and swapping them in). A load test or other experiment on a shared live system needs its own "With my approval only:" line inside the prompt (otherwise B6).

=== PACK ===
# Blind review pack

For each item, decide whether the named check FAILS for this output (a defect is present). Use the rubric text quoted in the item and INTERPRETATIONS.md.

Answer format: fill one JSON object per item in the answer template. `defect` is true (the check fails) or false (the check passes); `confidence` is a number from 0 to 1; `reason` is one sentence that quotes the output.

## D01

### Check B3

B3. Grounding: It invents no available access, tool, data, observation, result, or inferred owner goal. Unconfirmed dependencies get first checks. Inferred goals are marked as assumptions in the prompt. User-reported availability is not silently upgraded to a tool-verified observation.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Task

```text
Our nightly pipeline that rebuilds the reporting tables takes about 4 hours, and analysts wait for it each morning. Get it under 3 hours. It runs on our existing Airflow and Postgres setup. No new infrastructure spend and no changes to the report definitions.
```

### Output

````markdown
```text
Our nightly Airflow pipeline that rebuilds the reporting tables takes about 4 hours (user report), and analysts wait for it each morning. Get it under 3 hours.
Assumption: the real goal is analysts having correct reporting tables when they start work, so the order in which tables become ready matters as well as total runtime.
Assumption: the bar has to hold every night, so judge the worst night across several runs, not one good run.

Baseline from raw run records, not the reported figure. Use Airflow task-instance start and end times to measure end-to-end wall clock (DAG run start to last reporting table available) and each task's duration over recent nights, if run history is kept. Otherwise, measure the unchanged pipeline for 5 nights before changing anything. Record median and maximum, plus source row counts per night, so later comparisons use comparable data volumes.

Find what bounds the runtime before optimizing:
- Critical path method (from operations research): build the DAG with measured task durations and compute the longest dependency chain. Only tasks on that chain shorten total runtime. Re-run the computation after each change, because the critical path moves.
- Wait-event sampling: sample pg_stat_activity for the pipeline's own sessions during a run to see whether each slow task is waiting on I/O, locks, CPU, or client round-trips.
- Query plans: run EXPLAIN (ANALYZE, BUFFERS) on the slowest critical-path statements to find spills to disk, bad row estimates, nested loops over large inputs, and missing statistics. Use pg_stat_statements if it is already enabled.

Aim for under 18 minutes end-to-end, using these methods within the constraints below. When one approach stalls, try the next before reporting a miss. The 3-hour bar remains the pass condition.
- Incremental rebuilds: recompute only the slices whose source rows changed since the last successful run, using a stored high-water mark. Use this only if sources carry a reliable change marker (updated_at, monotonic IDs, or partition dates), and only if the result equals a full rebuild.
- Compute shared intermediates once, not per report.
- Bulk-build into new tables with CREATE TABLE AS or COPY, not row-by-row inserts. Create indexes after loading, run ANALYZE, then swap into place with a rename in a short transaction. Set lock_timeout so the swap retries instead of queueing behind long analyst queries. Use UNLOGGED tables for pipeline-only staging tables that are rebuilt every night.
- On the pipeline's own connections, set session-level work_mem, maintenance_work_mem, and max_parallel_workers_per_gather to remove the spills and serial scans the plans show.
- Schedule independent branches concurrently within existing limits, using longest-processing-time-first ordering. Within equal priority, finish the tables analysts depend on first.

Prove the outputs are unchanged:
- Restore or snapshot the same source state and run both the current and the new pipeline against it. For each reporting table, compare row counts and run EXCEPT ALL in both directions.
- Run the current pipeline twice on the same snapshot to establish its own nondeterminism, such as floating-point sums or run-time timestamp columns. Allow only that much difference.
- Red-team the equivalence with source states built to break incremental and parallel logic: late-arriving rows, updates and deletes to already-processed rows, a backfill, a month or year boundary, a DST change night, and an empty-input night.
- Deploy to production only after every table passes.

Requirements: use only the existing Airflow and Postgres setup. No new infrastructure spend. No changes to the report definitions; every reporting table's contents must stay as the current definitions produce them. Target end-to-end runtime is under 3 hours.

With my approval only: change Postgres server-wide settings (postgresql.conf, shared_preload_libraries, including enabling pg_stat_statements or auto_explain) or restart the server.
With my approval only: change Airflow shared pools, global concurrency, or scheduler configuration.
With my approval only: add indexes or other objects to source tables the pipeline does not own.
With my approval only: run more concurrent pipeline queries against Postgres than today's measured peak, if the instance serves other workloads.
With my approval only: run the old and new pipelines side by side on the production Postgres for output comparison.
With my approval only: move the DAG's scheduled start time.
With my approval only: read analysts' query history (pg_stat_statements or Postgres logs) to learn which reporting tables they query first each morning.

First check: what counts as a "report definition" (for example, the reporting-table SQL files or a semantic layer). If the SQL itself is frozen, limit changes to orchestration, physical design of the pipeline's own tables, and session settings.
First check: whether Airflow task-instance history with per-task start and end times exists, and how many past nights it covers.
First check: read access to the DAG code and SQL, and permission to deploy changes to this DAG.
First check: whether the Postgres instance and the Airflow pools the DAG uses are shared with other workloads.
First check: whether a non-production Postgres or a restorable snapshot exists on existing hardware for the output comparison, without new spend.
First check: whether reporting tables have dependent views, grants, foreign keys, or replication that a rename-swap must recreate or preserve.
First check: which source tables carry a reliable change marker for incremental rebuilds.
Name any check that fails, continue only with supported, authorized work, and mark the affected results unverified.

Judge: (1) end-to-end wall clock from Airflow run records is under 3 hours on each of 5 consecutive production nights after deployment, any night at or over 3 hours fails, and the result is reported beside the baseline measured the same way (median and maximum, with source row counts); (2) on the same source snapshot, every reporting table from the new pipeline matches the current pipeline's: equal row counts and empty EXCEPT ALL in both directions, allowing only the differences two runs of the current pipeline show, including every red-team case; (3) the stretch target of under 18 minutes is reported separately as met or missed; (4) if the analyst-query-history read is approved, report per night which reporting tables were first queried before they were ready; any missing run history or comparison snapshot leaves the affected part unverified.
```

- `altitude`: the original outcome is runtime under 3 hours. The improved outcome is correct tables ready in the order analysts need them, every night, judged on the worst of 5 nights. Reading analyst query history and moving the schedule are behind approval.
- `depth`: measure the baseline from Airflow task records instead of the "about 4 hours" report. Find bottlenecks with wait-event sampling and EXPLAIN (ANALYZE, BUFFERS) before changing anything.
- `depth`: a stretch target of under 18 minutes, reached through incremental rebuilds, shared intermediates, bulk build-then-swap, session tuning, and UNLOGGED staging tables. All of these touch only the pipeline's own objects and connections; the 3-hour bar stays the pass condition.
- `depth`: an output-equivalence judge (row counts plus two-way EXCEPT ALL on the same snapshot) that enforces "no changes to report definitions." A noise floor from two baseline runs keeps legitimate float or timestamp differences from failing correct work.
- `range`: from operations research, the critical path method shows which tasks actually bound runtime, and longest-processing-time-first scheduling orders the concurrent branches.
- `range`: from SRE/statistical process control, the bar is judged over a multi-night distribution under comparable data volumes instead of a single run.
- `range`: red-team source states (late, updated, and deleted rows, backfills, boundary and DST nights, empty input) attack the incremental logic, which is the riskiest change.
- Risk: rename-swaps can break dependent views and grants and can block behind analyst locks. This is covered by a First check and by lock_timeout.
- Skipped: none. All three lenses contributed.
- Owner actions:
  - Define what "report definitions" covers.
  - Confirm run-history, code, and deploy access, and whether Postgres and Airflow are shared.
  - Confirm a no-cost comparison snapshot is available.
  - Decide on the 7 approval-gated additions.
````

## D02

### Check B3

B3. Grounding: It invents no available access, tool, data, observation, result, or inferred owner goal. Unconfirmed dependencies get first checks. Inferred goals are marked as assumptions in the prompt. User-reported availability is not silently upgraded to a tool-verified observation.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Task

```text
Our nightly pipeline that rebuilds the reporting tables takes about 4 hours, and analysts wait for it each morning. Get it under 3 hours. It runs on our existing Airflow and Postgres setup. No new infrastructure spend and no changes to the report definitions.
```

### Output

````markdown
```text
Get our nightly reporting-table rebuild under 3 hours on our existing Airflow and Postgres setup. It currently takes about 4 hours, and analysts wait for it each morning. No new infrastructure spend and no changes to the report definitions.

Assumption: Success means complete, unchanged reporting outputs become available earlier—not merely that the DAG reports a shorter duration or shifts necessary work outside the measured pipeline.

Use existing Airflow task-instance timings, dependency information, and available Postgres query evidence to establish a measured baseline; treat “about 4 hours” as the reported baseline until confirmed. Measure elapsed time from pipeline start until all reporting outputs are ready, including dependency waits, retries, validation, and publication. Also record morning availability from existing timestamps so runtime improvements can be connected to analysts’ waiting.

Apply critical-path analysis from operations research: distinguish tasks that determine completion time from expensive tasks whose optimization would not advance completion. Trace the critical path to SQL statements and data volumes before choosing changes.

Use Postgres EXPLAIN and existing execution statistics or saved execution plans, where available, to distinguish repeated scans, poor estimates, spill-heavy operations, and blocking. Do not execute expensive statements merely to collect plans on shared live Postgres without approval.

Aim for 18 minutes using critical-path removal, elimination of redundant computation, and SQL/access-path optimization while preserving the complete rebuild’s results. If one approach stalls, try the next supported approach within existing resources and authorized operating windows before reporting a miss. Under 3 hours remains the acceptance bar; report stretch attainment separately as met, missed, or unverified.

Keep changes confined to this pipeline’s code, dependency ordering, connections, and owned database objects. Consider dependency reordering only where independence is established. Session-local tuning and rebuilding or swapping this pipeline’s own tables are permitted; do not change server-wide settings, shared pools, shared queues, or other workloads’ schedules.

Use differential testing to challenge each proposed shortcut: compare original and optimized outputs for identical source inputs and equivalent run parameters. Check complete row values and multiplicities, NULLs, report-visible schema, and all reporting tables—not just counts or sampled aggregates. Preserve existing publication and consistency guarantees. Evidence used to tune a revision is development evidence; confirm the final revision on a representative run not used to choose it, or leave its performance claim unverified.

Deliver the scoped implementation, reproducible validation checks, and a concise before/after account covering elapsed time, workload comparability, output equivalence, morning availability, bottlenecks removed, and stretch attainment. Retain a rollback path for the pipeline’s changes.

With my approval only: run a bounded original-versus-optimized replay on shared live Postgres, with agreed load limits and stop conditions; this authorizes no new infrastructure spend.

First check: establish access to the DAG and SQL, available run history and query evidence, ownership of affected objects, existing publication guarantees, and whether an already-authorized environment can replay identical source inputs without new infrastructure spend. Identify representative workload variation from available history rather than assuming it.
First check: confirm whether existing artifacts support full output comparison and a final performance run not used for tuning. If any dependency is missing, continue only with supported, authorized work and leave the affected claims unverified.
Judge: reproducible output comparisons must find no differences between original and optimized reporting results for identical inputs and equivalent run parameters; recorded representative final-run timings must show complete reporting availability in strictly less than 3 hours, including waits, retries, validation, and publication, without excluding necessary work; the change diff and execution record must show unchanged report definitions, no new infrastructure spend, and no unauthorized shared-resource changes. Pass only if every condition is met; report the 18-minute stretch separately, and leave any claim lacking its required evidence unverified.
```

- `altitude`: Moves from a shorter pipeline runtime to earlier availability of complete reports, using existing timestamps to expose work shifted outside the timer. No new schedule or monitoring workflow.
- `depth`: Adds raw execution evidence, scoped Postgres diagnosis, and an 18-minute stretch target while retaining the owner’s under-3-hour acceptance bar. Additional live replay requires approval.
- `range`: Critical-path analysis identifies changes that actually advance completion; differential testing challenges shortcuts that could silently alter reports. Final performance confirmation uses evidence not used for tuning.
- Skipped lenses: none.
- Owner actions: confirm access, ownership, and replay capabilities; approve any additional shared-live replay. Missing evidence leaves the corresponding result unverified.
````

## D03

### Check B2

B2. Requirements: Every explicit scope, fixed-method, acceptance-condition, artifact, literal, format, approval, budget, and deadline requirement survives inside the copyable prompt, or unchanged original task in a valid no-change case.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Task

```text
Our nightly pipeline that rebuilds the reporting tables takes about 4 hours, and analysts wait for it each morning. Get it under 3 hours. It runs on our existing Airflow and Postgres setup. No new infrastructure spend and no changes to the report definitions.
```

### Output

````markdown
```text
Get our nightly reporting-table rebuild under 3 hours on our existing Airflow and Postgres setup. It currently takes about 4 hours, and analysts wait for it each morning. No new infrastructure spend and no changes to the report definitions.

Assumption: Success means complete, unchanged reporting outputs become available earlier—not merely that the DAG reports a shorter duration or shifts necessary work outside the measured pipeline.

Use existing Airflow task-instance timings, dependency information, and available Postgres query evidence to establish a measured baseline; treat “about 4 hours” as the reported baseline until confirmed. Measure elapsed time from pipeline start until all reporting outputs are ready, including dependency waits, retries, validation, and publication. Also record morning availability from existing timestamps so runtime improvements can be connected to analysts’ waiting.

Apply critical-path analysis from operations research: distinguish tasks that determine completion time from expensive tasks whose optimization would not advance completion. Trace the critical path to SQL statements and data volumes before choosing changes.

Use Postgres EXPLAIN and existing execution statistics or saved execution plans, where available, to distinguish repeated scans, poor estimates, spill-heavy operations, and blocking. Do not execute expensive statements merely to collect plans on shared live Postgres without approval.

Aim for 18 minutes using critical-path removal, elimination of redundant computation, and SQL/access-path optimization while preserving the complete rebuild’s results. If one approach stalls, try the next supported approach within existing resources and authorized operating windows before reporting a miss. Under 3 hours remains the acceptance bar; report stretch attainment separately as met, missed, or unverified.

Keep changes confined to this pipeline’s code, dependency ordering, connections, and owned database objects. Consider dependency reordering only where independence is established. Session-local tuning and rebuilding or swapping this pipeline’s own tables are permitted; do not change server-wide settings, shared pools, shared queues, or other workloads’ schedules.

Use differential testing to challenge each proposed shortcut: compare original and optimized outputs for identical source inputs and equivalent run parameters. Check complete row values and multiplicities, NULLs, report-visible schema, and all reporting tables—not just counts or sampled aggregates. Preserve existing publication and consistency guarantees. Evidence used to tune a revision is development evidence; confirm the final revision on a representative run not used to choose it, or leave its performance claim unverified.

Deliver the scoped implementation, reproducible validation checks, and a concise before/after account covering elapsed time, workload comparability, output equivalence, morning availability, bottlenecks removed, and stretch attainment. Retain a rollback path for the pipeline’s changes.

With my approval only: run a bounded original-versus-optimized replay on shared live Postgres, with agreed load limits and stop conditions; this authorizes no new infrastructure spend.

First check: establish access to the DAG and SQL, available run history and query evidence, ownership of affected objects, existing publication guarantees, and whether an already-authorized environment can replay identical source inputs without new infrastructure spend. Identify representative workload variation from available history rather than assuming it.
First check: confirm whether existing artifacts support full output comparison and a final performance run not used for tuning. If any dependency is missing, continue only with supported, authorized work and leave the affected claims unverified.
Judge: reproducible output comparisons must find no differences between original and optimized reporting results for identical inputs and equivalent run parameters; recorded representative final-run timings must show complete reporting availability in strictly less than 3 hours, including waits, retries, validation, and publication, without excluding necessary work; the change diff and execution record must show unchanged report definitions, no new infrastructure spend, and no unauthorized shared-resource changes. Pass only if every condition is met; report the 18-minute stretch separately, and leave any claim lacking its required evidence unverified.
```

- `altitude`: Moves from a shorter pipeline runtime to earlier availability of complete reports, using existing timestamps to expose work shifted outside the timer. No new schedule or monitoring workflow.
- `depth`: Adds raw execution evidence, scoped Postgres diagnosis, and an 18-minute stretch target while retaining the owner’s under-3-hour acceptance bar. Additional live replay requires approval.
- `range`: Critical-path analysis identifies changes that actually advance completion; differential testing challenges shortcuts that could silently alter reports. Final performance confirmation uses evidence not used for tuning.
- Skipped lenses: none.
- Owner actions: confirm access, ownership, and replay capabilities; approve any additional shared-live replay. Missing evidence leaves the corresponding result unverified.
````

## D04

### Check B6

B6. Authority: Added scope, new access, paid steps, and irreversible actions are conditional on approval inside the prompt, not only in commentary. Explicitly prohibited expansions remain prohibited. A response with no expansion passes without needing an irrelevant approval ritual.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Task

```text
Our nightly pipeline that rebuilds the reporting tables takes about 4 hours, and analysts wait for it each morning. Get it under 3 hours. It runs on our existing Airflow and Postgres setup. No new infrastructure spend and no changes to the report definitions.
```

### Output

````markdown
```text
Our nightly Airflow pipeline that rebuilds the reporting tables takes about 4 hours (user report), and analysts wait for it each morning. Get it under 3 hours.
Assumption: the real goal is analysts having correct reporting tables when they start work, so the order in which tables become ready matters as well as total runtime.
Assumption: the bar has to hold every night, so judge the worst night across several runs, not one good run.

Baseline from raw run records, not the reported figure. Use Airflow task-instance start and end times to measure end-to-end wall clock (DAG run start to last reporting table available) and each task's duration over recent nights, if run history is kept. Otherwise, measure the unchanged pipeline for 5 nights before changing anything. Record median and maximum, plus source row counts per night, so later comparisons use comparable data volumes.

Find what bounds the runtime before optimizing:
- Critical path method (from operations research): build the DAG with measured task durations and compute the longest dependency chain. Only tasks on that chain shorten total runtime. Re-run the computation after each change, because the critical path moves.
- Wait-event sampling: sample pg_stat_activity for the pipeline's own sessions during a run to see whether each slow task is waiting on I/O, locks, CPU, or client round-trips.
- Query plans: run EXPLAIN (ANALYZE, BUFFERS) on the slowest critical-path statements to find spills to disk, bad row estimates, nested loops over large inputs, and missing statistics. Use pg_stat_statements if it is already enabled.

Aim for under 18 minutes end-to-end, using these methods within the constraints below. When one approach stalls, try the next before reporting a miss. The 3-hour bar remains the pass condition.
- Incremental rebuilds: recompute only the slices whose source rows changed since the last successful run, using a stored high-water mark. Use this only if sources carry a reliable change marker (updated_at, monotonic IDs, or partition dates), and only if the result equals a full rebuild.
- Compute shared intermediates once, not per report.
- Bulk-build into new tables with CREATE TABLE AS or COPY, not row-by-row inserts. Create indexes after loading, run ANALYZE, then swap into place with a rename in a short transaction. Set lock_timeout so the swap retries instead of queueing behind long analyst queries. Use UNLOGGED tables for pipeline-only staging tables that are rebuilt every night.
- On the pipeline's own connections, set session-level work_mem, maintenance_work_mem, and max_parallel_workers_per_gather to remove the spills and serial scans the plans show.
- Schedule independent branches concurrently within existing limits, using longest-processing-time-first ordering. Within equal priority, finish the tables analysts depend on first.

Prove the outputs are unchanged:
- Restore or snapshot the same source state and run both the current and the new pipeline against it. For each reporting table, compare row counts and run EXCEPT ALL in both directions.
- Run the current pipeline twice on the same snapshot to establish its own nondeterminism, such as floating-point sums or run-time timestamp columns. Allow only that much difference.
- Red-team the equivalence with source states built to break incremental and parallel logic: late-arriving rows, updates and deletes to already-processed rows, a backfill, a month or year boundary, a DST change night, and an empty-input night.
- Deploy to production only after every table passes.

Requirements: use only the existing Airflow and Postgres setup. No new infrastructure spend. No changes to the report definitions; every reporting table's contents must stay as the current definitions produce them. Target end-to-end runtime is under 3 hours.

With my approval only: change Postgres server-wide settings (postgresql.conf, shared_preload_libraries, including enabling pg_stat_statements or auto_explain) or restart the server.
With my approval only: change Airflow shared pools, global concurrency, or scheduler configuration.
With my approval only: add indexes or other objects to source tables the pipeline does not own.
With my approval only: run more concurrent pipeline queries against Postgres than today's measured peak, if the instance serves other workloads.
With my approval only: run the old and new pipelines side by side on the production Postgres for output comparison.
With my approval only: move the DAG's scheduled start time.
With my approval only: read analysts' query history (pg_stat_statements or Postgres logs) to learn which reporting tables they query first each morning.

First check: what counts as a "report definition" (for example, the reporting-table SQL files or a semantic layer). If the SQL itself is frozen, limit changes to orchestration, physical design of the pipeline's own tables, and session settings.
First check: whether Airflow task-instance history with per-task start and end times exists, and how many past nights it covers.
First check: read access to the DAG code and SQL, and permission to deploy changes to this DAG.
First check: whether the Postgres instance and the Airflow pools the DAG uses are shared with other workloads.
First check: whether a non-production Postgres or a restorable snapshot exists on existing hardware for the output comparison, without new spend.
First check: whether reporting tables have dependent views, grants, foreign keys, or replication that a rename-swap must recreate or preserve.
First check: which source tables carry a reliable change marker for incremental rebuilds.
Name any check that fails, continue only with supported, authorized work, and mark the affected results unverified.

Judge: (1) end-to-end wall clock from Airflow run records is under 3 hours on each of 5 consecutive production nights after deployment, any night at or over 3 hours fails, and the result is reported beside the baseline measured the same way (median and maximum, with source row counts); (2) on the same source snapshot, every reporting table from the new pipeline matches the current pipeline's: equal row counts and empty EXCEPT ALL in both directions, allowing only the differences two runs of the current pipeline show, including every red-team case; (3) the stretch target of under 18 minutes is reported separately as met or missed; (4) if the analyst-query-history read is approved, report per night which reporting tables were first queried before they were ready; any missing run history or comparison snapshot leaves the affected part unverified.
```

- `altitude`: the original outcome is runtime under 3 hours. The improved outcome is correct tables ready in the order analysts need them, every night, judged on the worst of 5 nights. Reading analyst query history and moving the schedule are behind approval.
- `depth`: measure the baseline from Airflow task records instead of the "about 4 hours" report. Find bottlenecks with wait-event sampling and EXPLAIN (ANALYZE, BUFFERS) before changing anything.
- `depth`: a stretch target of under 18 minutes, reached through incremental rebuilds, shared intermediates, bulk build-then-swap, session tuning, and UNLOGGED staging tables. All of these touch only the pipeline's own objects and connections; the 3-hour bar stays the pass condition.
- `depth`: an output-equivalence judge (row counts plus two-way EXCEPT ALL on the same snapshot) that enforces "no changes to report definitions." A noise floor from two baseline runs keeps legitimate float or timestamp differences from failing correct work.
- `range`: from operations research, the critical path method shows which tasks actually bound runtime, and longest-processing-time-first scheduling orders the concurrent branches.
- `range`: from SRE/statistical process control, the bar is judged over a multi-night distribution under comparable data volumes instead of a single run.
- `range`: red-team source states (late, updated, and deleted rows, backfills, boundary and DST nights, empty input) attack the incremental logic, which is the riskiest change.
- Risk: rename-swaps can break dependent views and grants and can block behind analyst locks. This is covered by a First check and by lock_timeout.
- Skipped: none. All three lenses contributed.
- Owner actions:
  - Define what "report definitions" covers.
  - Confirm run-history, code, and deploy access, and whether Postgres and Airflow are shared.
  - Confirm a no-cost comparison snapshot is available.
  - Decide on the 7 approval-gated additions.
````

## D05

### Check B3

B3. Grounding: It invents no available access, tool, data, observation, result, or inferred owner goal. Unconfirmed dependencies get first checks. Inferred goals are marked as assumptions in the prompt. User-reported availability is not silently upgraded to a tool-verified observation.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Task

```text
Our nightly pipeline that rebuilds the reporting tables takes about 4 hours, and analysts wait for it each morning. Get it under 3 hours. It runs on our existing Airflow and Postgres setup. No new infrastructure spend and no changes to the report definitions.
```

### Output

````markdown
```text
Our nightly pipeline that rebuilds the reporting tables takes about 4 hours, and analysts wait for it each morning. Get it under 3 hours on our existing Airflow and Postgres setup, with no new infrastructure spend and no changes to the report definitions.

Assumption: the intended benefit is earlier access to complete, correct reporting tables—not a shorter reported runtime achieved by moving required work outside the measurement window.

Reconstruct the end-to-end critical path from available Airflow run and task records, including dependency waits, queueing, retries, database execution, and publication. Treat “about 4 hours” as the reported duration until measured. Use operations-research critical-path analysis to distinguish work whose acceleration advances completion from work that merely looks expensive in isolation.

Start database diagnosis from the SQL that actually runs and the available execution plans and statistics. Use Postgres EXPLAIN to investigate repeated scans, join cardinality errors, sorts, and redundant computation; use existing execution measurements where available. Choose changes from evidence rather than assuming that more concurrency helps. Tune only this pipeline’s tasks, connections, and objects: for example, eliminate duplicate work, improve query plans or indexes, or rebuild and safely swap its reporting tables without changing their meaning. Use queueing analysis to detect when this pipeline’s own concurrency creates contention rather than useful parallelism.

Aim for under 18 minutes of end-to-end elapsed time using critical-path reduction, elimination of redundant computation, and evidence-based query optimization. This stretch does not replace the required under-3-hour result. If one approach stalls, try the next supported approach within the no-new-spend constraint and authorized execution windows; report stretch attainment separately as met, missed, or unverified.

Use differential testing to compare the original and optimized reporting results on the same consistent source inputs. Check the complete expected schema and row multisets, including duplicate multiplicities and NULL values; row counts or aggregate checksums alone are insufficient. Exercise applicable boundary cases such as empty inputs, duplicate source records, and date boundaries in an already-authorized test environment. Check that task ordering and publication do not expose incomplete results. Preserve a rollback path for changes to this pipeline’s own objects.

Measure the original and optimized pipeline using the same start and finish definitions and comparable input volumes, resource conditions, and cache conditions. Include all required work, waits, retries, validation, and publication; do not transfer work outside the timing boundary. Freeze the selected implementation before its final validation run, and distinguish diagnostic runs from final evidence.

Keep the existing Airflow and Postgres setup. Do not introduce new infrastructure spend or change report definitions. Do not change shared pools, queues, server-wide settings, other workloads, or schedules that others rely on.

Deliver the changes and a concise evidence summary: measured baseline, critical-path findings, changes made, correctness results, end-to-end runtime, stretch status, rollback instructions, and any unverified claims.

With my approval only: run an additional performance experiment against shared live systems, with a specific execution window, resource limits, and abort conditions agreed before execution.

First check: identify this pipeline’s DAG, SQL, reporting-table ownership, report definitions, authorized editing and execution access, and existing publication boundary. Confirm which run history, logs, plans, and database statistics are available; keep methods conditional on that availability.
First check: establish whether retained source inputs or a consistent snapshot and an existing authorized comparison environment can support original-versus-optimized execution and full-result comparison without new infrastructure spend or interference with other work.
First check: confirm available capacity, rollback facilities, and authorized execution windows before rebuilding or swapping this pipeline’s tables. If a dependency is missing, continue only with supported, authorized work and leave the affected result unverified.
Judge: existing Airflow timing evidence and database comparison tests must show that the finalized pipeline completes all required work and publication in strictly under 3 hours under documented comparable conditions, preserves report definitions, schemas, and complete row multisets on identical source inputs, passes applicable boundary and publication checks, and uses the existing setup without new infrastructure spend or prohibited shared changes; pass only if every condition is evidenced, otherwise mark the affected result unverified; separately report whether the under-18-minute stretch was met, missed, or remains unverified.
```

- `altitude`: Moves from a faster pipeline to earlier availability of complete reporting tables; an explicit end-to-end timing boundary prevents shifting work outside the clock. No additional workflow or infrastructure.
- `depth`: Uses actual SQL, execution plans, and database statistics to target causes, with an under-18-minute stretch while retaining under 3 hours as the acceptance bar. Extra live experiments require approval.
- `depth`: Adds comparable baseline/final measurements and a frozen final implementation so exploratory improvements are not mistaken for verified results; evidence availability is checked first.
- `range`: Operations-research critical-path and queueing methods identify consequential bottlenecks and counterproductive concurrency without changing shared settings.
- `range`: Differential testing checks complete results, boundary cases, and publication integrity, protecting unchanged report definitions; requires consistent inputs and existing authorized comparison capacity.
- Skipped lenses: none.
- Owner actions: confirm access, pipeline ownership, comparison capacity, and execution windows; approve any additional shared-live-system performance experiment. Missing evidence leaves the corresponding claim unverified.
````

## D06

### Check B6

B6. Authority: Added scope, new access, paid steps, and irreversible actions are conditional on approval inside the prompt, not only in commentary. Explicitly prohibited expansions remain prohibited. A response with no expansion passes without needing an irrelevant approval ritual.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Task

```text
Our nightly pipeline that rebuilds the reporting tables takes about 4 hours, and analysts wait for it each morning. Get it under 3 hours. It runs on our existing Airflow and Postgres setup. No new infrastructure spend and no changes to the report definitions.
```

### Output

````markdown
```text
Our nightly Airflow pipeline that rebuilds the reporting tables on Postgres takes about 4 hours (owner's report), and analysts wait for it each morning. Get it under 3 hours.
Assumption: what matters is that analysts have correct reporting tables when their morning starts, every morning. Slow nights count as much as typical ones, and the tables analysts read first matter most.
Assumption: "no changes to the report definitions" means every reporting table keeps its exact schema and contents. A change to how a table is computed is acceptable only when the equivalence check below proves identical output. The current definition SQL stays as the reference.
Build the baseline from raw evidence before changing anything. If Airflow run history is kept, pull per-task queued, start, end, and state times for recent runs from the metadata database and compute the real end-to-end duration distribution. Keep the owner's "about 4 hours" separate from this measured baseline. For each task, split its time into waiting (queued, pool slots, sensors, retries) and running. If pg_stat_statements, auto_explain, and pg_stat_activity are readable, capture the heaviest statements, their EXPLAIN (ANALYZE, BUFFERS) plans, and wait events sampled during a run. Use these to tell CPU, I/O, lock waits, and sort/hash spills to disk apart.
Compute the DAG's critical path from measured durations (critical path method). Spend effort only on tasks on that path or close to it, and recompute the path after each change, because it moves. Apply the USE method (utilization, saturation, errors) to CPU, disk, connections, and locks to decide whether more concurrency helps or only saturates the server.
Try these methods in order of measured payoff, each limited to the pipeline's own objects and connections:
- Rewrite row-by-row or repeated work as set-based SQL that yields identical output.
- Build each reporting table as a new table, add indexes and constraints after the load, ANALYZE it, then swap it in by rename in one transaction. First check for dependent views, grants, and foreign keys that bind to the old table, and recreate them.
- Make intermediate tables UNLOGGED when the pipeline owns them and recreates them every night.
- Add indexes on the pipeline's own intermediate tables where the plans show they pay off.
- Set work_mem, maintenance_work_mem, and max_parallel_workers_per_gather per session on the pipeline's own connections where the plans show spills or serial scans.
- Restructure the DAG so independent tasks run in parallel within the pipeline's existing pool allocation. Use priority_weight to run critical-path tasks and the tables analysts read first ahead of the rest.
Aim for under 18 minutes end to end using incremental refresh: where a source has reliable change markers (append-only keys, updated_at with tracked deletes, or partitions), recompute only the affected partitions or keys instead of rebuilding everything. Prove each incremental path with a replay. If enough history is recoverable, start from a past full build and apply the incremental path day by day over at least 14 past days of source changes. At each day, compare the result with a full rebuild, deliberately including late-arriving rows, updates, deletes, and backfills. Any table that differs on any day stays on full rebuild. When one approach stalls, try the next before reporting a miss. The 3-hour bar remains the pass condition; report the 18-minute stretch separately, met or missed.
Do not deploy a change to production until its equivalence check passes. During the nightly window, watch other workloads on the same Postgres server and Airflow, and report any job that got slower.
Deliver a short report covering:
- the measured baseline distribution;
- the critical path before and after;
- each change, with its measured time saved, its equivalence result, and its rollback step;
- post-deployment run durations;
- the stretch result.
Requirements: keep the existing Airflow and Postgres setup; no new infrastructure spend (no larger instances, new services, or added paid capacity); no changes to the report definitions.
With my approval only: change server-wide Postgres settings (postgresql.conf or ALTER SYSTEM), proposing each setting with supporting plan or wait-event evidence.
With my approval only: change Airflow-wide configuration, shared pools, or other DAGs.
With my approval only: add indexes to, or otherwise change, source tables that other work reads.
With my approval only: run a candidate pipeline against the production Postgres server alongside normal workloads, for equivalence or timing comparison.
With my approval only: move the DAG's start time or change its upstream dependencies.
First check: Airflow metadata history (task instance durations) exists, and how long it is retained. Name each missing dependency, continue only with supported, authorized work, and leave affected results unverified.
First check: pg_stat_statements and auto_explain are available, and you have permission to read pg_stat_activity.
First check: a non-production Postgres within existing infrastructure can hold a copy of the sources for equivalence runs.
First check: each source has change markers and enough recoverable history for the replay.
First check: when analysts start work and which tables they read first, from query logs if they are kept; otherwise ask.
Judge: four conditions must hold. (1) For every reporting table, the changed pipeline's output on the same source snapshot matches the current pipeline's: identical column names, types, and order; identical row count; and EXCEPT ALL empty in both directions. Ignore only columns or values that also differ between two runs of the unchanged pipeline on that snapshot, and list each one in the report. (2) Every incremental path matches a full rebuild on every replayed day. (3) The median end-to-end wall-clock time, from first task start to last reporting table swapped in, is under 3 hours over at least 5 consecutive production nightly runs after deployment. Measure it the same way as the Airflow-history baseline and report every run's duration. (4) No other job in the nightly window ran slower than its own range over its prior 5 runs. Pass only if all four hold; report the 18-minute stretch separately, met or missed.
```

**Ledger**
- `altitude`: The goal moves from "pipeline under 3 hours" to "analysts have correct tables when they start, on slow nights too." This adds critical-path ordering so the most-read tables land first, and judging over 5+ runs instead of one. Cost: a few nights of observation before the result is confirmed.
- `depth`: The baseline comes from Airflow task-instance history and Postgres statement and wait evidence, not from "about 4 hours." This tests the hidden belief that query compute is the bottleneck when the cause may be queueing, sensors, locks, or spills. It needs read access to the metadata and stats views.
- `depth`: The prompt names concrete tools limited to the pipeline's own objects: set-based rewrites, build-then-swap with indexes added after load (including dependent-view handling), UNLOGGED intermediates, and per-session memory and parallelism settings. Risk: a rename swap can break dependent views if the check is skipped.
- `depth`: There is a hard stretch target of under 18 minutes through incremental refresh. The 3-hour bar stays the pass condition. Risk: incremental logic is where silent wrongness creeps in, which the replay addresses.
- `depth`: The judge adds a differential equivalence check (schema, row count, two-way EXCEPT ALL against the unchanged pipeline on the same snapshot) to enforce "no changes to report definitions." A noise baseline from two unchanged runs keeps nondeterministic columns from failing correct work.
- `range`: From operations research, the critical path method shows that speeding up off-path tasks saves nothing.
- `range`: From performance engineering, the USE method shows whether added concurrency helps or just saturates disk and locks.
- `range`: From software testing, a red-team replay with late, updated, deleted, and backfilled rows breaks incremental paths before analysts see wrong numbers.
- `range`: From SRE, judging the run-duration distribution and watching neighbor jobs catches tail nights and harm to other workloads.
- Gated, not done by default: server-wide Postgres settings, Airflow-wide config, shared pools and other DAGs, source-table indexes, candidate runs on production, and DAG start-time or upstream changes. These all affect shared resources or schedules others rely on.
- Skipped: none. All three lenses contribute.
- Owner actions:
  - Confirm the reading of "report definitions" (identical output with rewritten computation allowed versus definition SQL text frozen).
  - Confirm metadata, stats-view, and non-prod environment access.
  - Supply analyst start times and which tables they read first.
  - Decide each "With my approval only" line, especially a production candidate run if no non-prod copy exists.
````

## D07

### Check B6

B6. Authority: Added scope, new access, paid steps, and irreversible actions are conditional on approval inside the prompt, not only in commentary. Explicitly prohibited expansions remain prohibited. A response with no expansion passes without needing an irrelevant approval ritual.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Task

```text
Our nightly pipeline that rebuilds the reporting tables takes about 4 hours, and analysts wait for it each morning. Get it under 3 hours. It runs on our existing Airflow and Postgres setup. No new infrastructure spend and no changes to the report definitions.
```

### Output

````markdown
```text
Get our nightly reporting-table rebuild under 3 hours on our existing Airflow and Postgres setup. It currently takes about 4 hours, and analysts wait for it each morning. No new infrastructure spend and no changes to the report definitions.

Assumption: Success means complete, unchanged reporting outputs become available earlier—not merely that the DAG reports a shorter duration or shifts necessary work outside the measured pipeline.

Use existing Airflow task-instance timings, dependency information, and available Postgres query evidence to establish a measured baseline; treat “about 4 hours” as the reported baseline until confirmed. Measure elapsed time from pipeline start until all reporting outputs are ready, including dependency waits, retries, validation, and publication. Also record morning availability from existing timestamps so runtime improvements can be connected to analysts’ waiting.

Apply critical-path analysis from operations research: distinguish tasks that determine completion time from expensive tasks whose optimization would not advance completion. Trace the critical path to SQL statements and data volumes before choosing changes.

Use Postgres EXPLAIN and existing execution statistics or saved execution plans, where available, to distinguish repeated scans, poor estimates, spill-heavy operations, and blocking. Do not execute expensive statements merely to collect plans on shared live Postgres without approval.

Aim for 18 minutes using critical-path removal, elimination of redundant computation, and SQL/access-path optimization while preserving the complete rebuild’s results. If one approach stalls, try the next supported approach within existing resources and authorized operating windows before reporting a miss. Under 3 hours remains the acceptance bar; report stretch attainment separately as met, missed, or unverified.

Keep changes confined to this pipeline’s code, dependency ordering, connections, and owned database objects. Consider dependency reordering only where independence is established. Session-local tuning and rebuilding or swapping this pipeline’s own tables are permitted; do not change server-wide settings, shared pools, shared queues, or other workloads’ schedules.

Use differential testing to challenge each proposed shortcut: compare original and optimized outputs for identical source inputs and equivalent run parameters. Check complete row values and multiplicities, NULLs, report-visible schema, and all reporting tables—not just counts or sampled aggregates. Preserve existing publication and consistency guarantees. Evidence used to tune a revision is development evidence; confirm the final revision on a representative run not used to choose it, or leave its performance claim unverified.

Deliver the scoped implementation, reproducible validation checks, and a concise before/after account covering elapsed time, workload comparability, output equivalence, morning availability, bottlenecks removed, and stretch attainment. Retain a rollback path for the pipeline’s changes.

With my approval only: run a bounded original-versus-optimized replay on shared live Postgres, with agreed load limits and stop conditions; this authorizes no new infrastructure spend.

First check: establish access to the DAG and SQL, available run history and query evidence, ownership of affected objects, existing publication guarantees, and whether an already-authorized environment can replay identical source inputs without new infrastructure spend. Identify representative workload variation from available history rather than assuming it.
First check: confirm whether existing artifacts support full output comparison and a final performance run not used for tuning. If any dependency is missing, continue only with supported, authorized work and leave the affected claims unverified.
Judge: reproducible output comparisons must find no differences between original and optimized reporting results for identical inputs and equivalent run parameters; recorded representative final-run timings must show complete reporting availability in strictly less than 3 hours, including waits, retries, validation, and publication, without excluding necessary work; the change diff and execution record must show unchanged report definitions, no new infrastructure spend, and no unauthorized shared-resource changes. Pass only if every condition is met; report the 18-minute stretch separately, and leave any claim lacking its required evidence unverified.
```

- `altitude`: Moves from a shorter pipeline runtime to earlier availability of complete reports, using existing timestamps to expose work shifted outside the timer. No new schedule or monitoring workflow.
- `depth`: Adds raw execution evidence, scoped Postgres diagnosis, and an 18-minute stretch target while retaining the owner’s under-3-hour acceptance bar. Additional live replay requires approval.
- `range`: Critical-path analysis identifies changes that actually advance completion; differential testing challenges shortcuts that could silently alter reports. Final performance confirmation uses evidence not used for tuning.
- Skipped lenses: none.
- Owner actions: confirm access, ownership, and replay capabilities; approve any additional shared-live replay. Missing evidence leaves the corresponding result unverified.
````

## D08

### Check B6

B6. Authority: Added scope, new access, paid steps, and irreversible actions are conditional on approval inside the prompt, not only in commentary. Explicitly prohibited expansions remain prohibited. A response with no expansion passes without needing an irrelevant approval ritual.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Task

```text
Our nightly pipeline that rebuilds the reporting tables takes about 4 hours, and analysts wait for it each morning. Get it under 3 hours. It runs on our existing Airflow and Postgres setup. No new infrastructure spend and no changes to the report definitions.
```

### Output

````markdown
```text
Our nightly pipeline that rebuilds the reporting tables takes about 4 hours, and analysts wait for it each morning. Get it under 3 hours using our existing Airflow and Postgres setup.

Assumption: The useful finish line is when all reporting tables are committed and available to analysts, not merely when the last compute task finishes.
Assumption: An 18-minute rebuild is a worthwhile stretch goal, but getting under 3 hours remains the acceptance requirement.

Use existing Airflow task timings, DAG dependencies, report SQL, and available Postgres execution evidence to establish a measured baseline. Treat “about 4 hours” as the reported duration until measured. Measure elapsed time from the scheduled rebuild’s start through availability of every reporting table; distinguish queueing, execution, and publication time.

Apply critical-path analysis from operations research: identify which dependencies and resource waits determine completion time, rather than optimizing the slowest-looking queries in isolation. Estimate each proposed change’s effect on end-to-end duration before prioritizing it.

Use database execution-plan analysis to locate unnecessary scans, poor join strategies, repeated computation, and expensive load/index ordering. Start with existing execution evidence and non-executing EXPLAIN. Where supported and authorized, optimize the pipeline’s own SQL, session-local settings, table/index construction, and dependency-safe parallelism. Keep parallelism bounded so a faster rebuild does not come from degrading other workloads.

Aim for 18 minutes using critical-path reduction and execution-plan-guided optimization. If one approach stalls, try the next supported approach within the existing resource envelope and authorized operating windows before reporting a miss. Compare baseline and candidate using the same end-to-end metric and comparable input volumes, source state, and resource conditions. Report stretch attainment separately as met, missed, or unverified.

Use differential testing from software verification: construct expected results from the unchanged report definitions and compare every candidate table against them on the same source snapshot. Check complete row multisets, including duplicate multiplicities and NULLs, and preserve existing schema, freshness, and publication contracts. Exercise applicable boundary cases such as empty inputs and date cutoffs. Row counts or checksums alone are not sufficient correctness evidence.

Deliver the implemented optimizations and a concise evidence summary: measured baseline and final duration, bottleneck and critical-path changes, correctness-test results, resource-contention evidence where available, rollback instructions, and remaining limitations. Separate measured findings from estimates; do not claim success from projected task-level savings.

No new infrastructure spend and no changes to the report definitions. Preserve the existing reporting outputs and operate within the existing Airflow and Postgres setup. Do not change shared server settings, shared pools or queues, or other teams’ schedules as part of the ungated work.

With my approval only: run a one-off baseline-versus-candidate replay on a shared live database, with an agreed operating window and load cap.

First check: identify the actual pipeline and its reporting tables, the authoritative report definitions, available Airflow history, SQL and plan-inspection permissions, and authorized change/deployment boundaries before relying on them.
First check: establish whether a representative source snapshot and an existing isolated test environment are available and authorized; do not assume either exists. Before a shared-live replay, confirm snapshot feasibility and approval for its load and timing.
First check: identify existing freshness/publication contracts, operational limits, rollback mechanisms, and available contention evidence. If a dependency or permission is missing, continue only with supported, authorized work and leave the affected result unverified.

Judge: Automated full-table differential checks must show that candidate outputs match the unchanged report definitions on identical source snapshots, including duplicate multiplicities, NULLs, applicable boundary cases, and existing schema/freshness/publication contracts; an actual representative end-to-end run must finish in under 3 hours through committed availability of all reporting tables, with comparable baseline/candidate conditions documented and no breach of established operating limits; confirm that changes introduce neither infrastructure spend nor report-definition changes. Pass only if every requirement has evidence; projections, incomplete comparisons, or missing evidence leave the affected claim unverified. Report the 18-minute stretch separately as met, missed, or unverified.
```

- `altitude`: Moves from faster pipeline execution to verified availability of correct reporting tables, preventing an apparent speedup that merely shifts waiting into queueing or publication.
- `depth`: Adds raw execution evidence, plan-guided optimization, and an 18-minute stretch target while retaining under 3 hours as acceptance. Uses existing infrastructure; missing execution or resource evidence remains explicit.
- `range`: Adds operations-research critical-path analysis to prioritize end-to-end gains rather than isolated query improvements.
- `range`: Adds software-verification differential testing against unchanged definitions, catching fast-but-wrong results that timing and row counts cannot detect. A shared-live replay requires separate approval because it can affect others.
- Skipped lenses: None; each contributes a distinct outcome, optimization method, or correctness check.
- Owner actions: Confirm access and operating boundaries; resolve missing contract or test-environment information; approve a shared-live replay only if needed.
````

## D09

### Check B6

B6. Authority: Added scope, new access, paid steps, and irreversible actions are conditional on approval inside the prompt, not only in commentary. Explicitly prohibited expansions remain prohibited. A response with no expansion passes without needing an irrelevant approval ritual.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Task

```text
Our nightly pipeline that rebuilds the reporting tables takes about 4 hours, and analysts wait for it each morning. Get it under 3 hours. It runs on our existing Airflow and Postgres setup. No new infrastructure spend and no changes to the report definitions.
```

### Output

````markdown
```text
Our nightly pipeline that rebuilds the reporting tables takes about 4 hours, and analysts wait for it each morning. Get it under 3 hours on our existing Airflow and Postgres setup, with no new infrastructure spend and no changes to the report definitions.

Assumption: the intended benefit is earlier access to complete, correct reporting tables—not a shorter reported runtime achieved by moving required work outside the measurement window.

Reconstruct the end-to-end critical path from available Airflow run and task records, including dependency waits, queueing, retries, database execution, and publication. Treat “about 4 hours” as the reported duration until measured. Use operations-research critical-path analysis to distinguish work whose acceleration advances completion from work that merely looks expensive in isolation.

Start database diagnosis from the SQL that actually runs and the available execution plans and statistics. Use Postgres EXPLAIN to investigate repeated scans, join cardinality errors, sorts, and redundant computation; use existing execution measurements where available. Choose changes from evidence rather than assuming that more concurrency helps. Tune only this pipeline’s tasks, connections, and objects: for example, eliminate duplicate work, improve query plans or indexes, or rebuild and safely swap its reporting tables without changing their meaning. Use queueing analysis to detect when this pipeline’s own concurrency creates contention rather than useful parallelism.

Aim for under 18 minutes of end-to-end elapsed time using critical-path reduction, elimination of redundant computation, and evidence-based query optimization. This stretch does not replace the required under-3-hour result. If one approach stalls, try the next supported approach within the no-new-spend constraint and authorized execution windows; report stretch attainment separately as met, missed, or unverified.

Use differential testing to compare the original and optimized reporting results on the same consistent source inputs. Check the complete expected schema and row multisets, including duplicate multiplicities and NULL values; row counts or aggregate checksums alone are insufficient. Exercise applicable boundary cases such as empty inputs, duplicate source records, and date boundaries in an already-authorized test environment. Check that task ordering and publication do not expose incomplete results. Preserve a rollback path for changes to this pipeline’s own objects.

Measure the original and optimized pipeline using the same start and finish definitions and comparable input volumes, resource conditions, and cache conditions. Include all required work, waits, retries, validation, and publication; do not transfer work outside the timing boundary. Freeze the selected implementation before its final validation run, and distinguish diagnostic runs from final evidence.

Keep the existing Airflow and Postgres setup. Do not introduce new infrastructure spend or change report definitions. Do not change shared pools, queues, server-wide settings, other workloads, or schedules that others rely on.

Deliver the changes and a concise evidence summary: measured baseline, critical-path findings, changes made, correctness results, end-to-end runtime, stretch status, rollback instructions, and any unverified claims.

With my approval only: run an additional performance experiment against shared live systems, with a specific execution window, resource limits, and abort conditions agreed before execution.

First check: identify this pipeline’s DAG, SQL, reporting-table ownership, report definitions, authorized editing and execution access, and existing publication boundary. Confirm which run history, logs, plans, and database statistics are available; keep methods conditional on that availability.
First check: establish whether retained source inputs or a consistent snapshot and an existing authorized comparison environment can support original-versus-optimized execution and full-result comparison without new infrastructure spend or interference with other work.
First check: confirm available capacity, rollback facilities, and authorized execution windows before rebuilding or swapping this pipeline’s tables. If a dependency is missing, continue only with supported, authorized work and leave the affected result unverified.
Judge: existing Airflow timing evidence and database comparison tests must show that the finalized pipeline completes all required work and publication in strictly under 3 hours under documented comparable conditions, preserves report definitions, schemas, and complete row multisets on identical source inputs, passes applicable boundary and publication checks, and uses the existing setup without new infrastructure spend or prohibited shared changes; pass only if every condition is evidenced, otherwise mark the affected result unverified; separately report whether the under-18-minute stretch was met, missed, or remains unverified.
```

- `altitude`: Moves from a faster pipeline to earlier availability of complete reporting tables; an explicit end-to-end timing boundary prevents shifting work outside the clock. No additional workflow or infrastructure.
- `depth`: Uses actual SQL, execution plans, and database statistics to target causes, with an under-18-minute stretch while retaining under 3 hours as the acceptance bar. Extra live experiments require approval.
- `depth`: Adds comparable baseline/final measurements and a frozen final implementation so exploratory improvements are not mistaken for verified results; evidence availability is checked first.
- `range`: Operations-research critical-path and queueing methods identify consequential bottlenecks and counterproductive concurrency without changing shared settings.
- `range`: Differential testing checks complete results, boundary cases, and publication integrity, protecting unchanged report definitions; requires consistent inputs and existing authorized comparison capacity.
- Skipped lenses: none.
- Owner actions: confirm access, pipeline ownership, comparison capacity, and execution windows; approve any additional shared-live-system performance experiment. Missing evidence leaves the corresponding claim unverified.
````

## D10

### Check B7

B7. Stretch honesty: If a stretch is selected, it has a task-specific method, preserves the owner's required pass bar, stays within explicit resource bounds, and reports honest results and misses. Qualitative work is not given an arbitrary numeric improvement ratio.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Task

```text
Our nightly pipeline that rebuilds the reporting tables takes about 4 hours, and analysts wait for it each morning. Get it under 3 hours. It runs on our existing Airflow and Postgres setup. No new infrastructure spend and no changes to the report definitions.
```

### Output

````markdown
```text
Get our nightly reporting-table rebuild under 3 hours on our existing Airflow and Postgres setup. It currently takes about 4 hours, and analysts wait for it each morning. No new infrastructure spend and no changes to the report definitions.

Assumption: Success means complete, unchanged reporting outputs become available earlier—not merely that the DAG reports a shorter duration or shifts necessary work outside the measured pipeline.

Use existing Airflow task-instance timings, dependency information, and available Postgres query evidence to establish a measured baseline; treat “about 4 hours” as the reported baseline until confirmed. Measure elapsed time from pipeline start until all reporting outputs are ready, including dependency waits, retries, validation, and publication. Also record morning availability from existing timestamps so runtime improvements can be connected to analysts’ waiting.

Apply critical-path analysis from operations research: distinguish tasks that determine completion time from expensive tasks whose optimization would not advance completion. Trace the critical path to SQL statements and data volumes before choosing changes.

Use Postgres EXPLAIN and existing execution statistics or saved execution plans, where available, to distinguish repeated scans, poor estimates, spill-heavy operations, and blocking. Do not execute expensive statements merely to collect plans on shared live Postgres without approval.

Aim for 18 minutes using critical-path removal, elimination of redundant computation, and SQL/access-path optimization while preserving the complete rebuild’s results. If one approach stalls, try the next supported approach within existing resources and authorized operating windows before reporting a miss. Under 3 hours remains the acceptance bar; report stretch attainment separately as met, missed, or unverified.

Keep changes confined to this pipeline’s code, dependency ordering, connections, and owned database objects. Consider dependency reordering only where independence is established. Session-local tuning and rebuilding or swapping this pipeline’s own tables are permitted; do not change server-wide settings, shared pools, shared queues, or other workloads’ schedules.

Use differential testing to challenge each proposed shortcut: compare original and optimized outputs for identical source inputs and equivalent run parameters. Check complete row values and multiplicities, NULLs, report-visible schema, and all reporting tables—not just counts or sampled aggregates. Preserve existing publication and consistency guarantees. Evidence used to tune a revision is development evidence; confirm the final revision on a representative run not used to choose it, or leave its performance claim unverified.

Deliver the scoped implementation, reproducible validation checks, and a concise before/after account covering elapsed time, workload comparability, output equivalence, morning availability, bottlenecks removed, and stretch attainment. Retain a rollback path for the pipeline’s changes.

With my approval only: run a bounded original-versus-optimized replay on shared live Postgres, with agreed load limits and stop conditions; this authorizes no new infrastructure spend.

First check: establish access to the DAG and SQL, available run history and query evidence, ownership of affected objects, existing publication guarantees, and whether an already-authorized environment can replay identical source inputs without new infrastructure spend. Identify representative workload variation from available history rather than assuming it.
First check: confirm whether existing artifacts support full output comparison and a final performance run not used for tuning. If any dependency is missing, continue only with supported, authorized work and leave the affected claims unverified.
Judge: reproducible output comparisons must find no differences between original and optimized reporting results for identical inputs and equivalent run parameters; recorded representative final-run timings must show complete reporting availability in strictly less than 3 hours, including waits, retries, validation, and publication, without excluding necessary work; the change diff and execution record must show unchanged report definitions, no new infrastructure spend, and no unauthorized shared-resource changes. Pass only if every condition is met; report the 18-minute stretch separately, and leave any claim lacking its required evidence unverified.
```

- `altitude`: Moves from a shorter pipeline runtime to earlier availability of complete reports, using existing timestamps to expose work shifted outside the timer. No new schedule or monitoring workflow.
- `depth`: Adds raw execution evidence, scoped Postgres diagnosis, and an 18-minute stretch target while retaining the owner’s under-3-hour acceptance bar. Additional live replay requires approval.
- `range`: Critical-path analysis identifies changes that actually advance completion; differential testing challenges shortcuts that could silently alter reports. Final performance confirmation uses evidence not used for tuning.
- Skipped lenses: none.
- Owner actions: confirm access, ownership, and replay capabilities; approve any additional shared-live replay. Missing evidence leaves the corresponding result unverified.
````

=== ANSWER TEMPLATE ===
[
 {
  "item": "D01",
  "defect": null,
  "confidence": null,
  "reason": ""
 },
 {
  "item": "D02",
  "defect": null,
  "confidence": null,
  "reason": ""
 },
 {
  "item": "D03",
  "defect": null,
  "confidence": null,
  "reason": ""
 },
 {
  "item": "D04",
  "defect": null,
  "confidence": null,
  "reason": ""
 },
 {
  "item": "D05",
  "defect": null,
  "confidence": null,
  "reason": ""
 },
 {
  "item": "D06",
  "defect": null,
  "confidence": null,
  "reason": ""
 },
 {
  "item": "D07",
  "defect": null,
  "confidence": null,
  "reason": ""
 },
 {
  "item": "D08",
  "defect": null,
  "confidence": null,
  "reason": ""
 },
 {
  "item": "D09",
  "defect": null,
  "confidence": null,
  "reason": ""
 },
 {
  "item": "D10",
  "defect": null,
  "confidence": null,
  "reason": ""
 }
]

=== END ===
Return only the filled JSON array, one object per item, with no Markdown fence and no other text.
