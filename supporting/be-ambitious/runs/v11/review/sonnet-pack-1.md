# Blind review pack, grouped

Each group shows one task and one output once, then the items to grade for that output. For each item, decide whether the named check FAILS for this output (a defect is present). Use the rubric text quoted in the item and INTERPRETATIONS.md. Answer with one JSON object per item: `item`, `defect` (true = the check fails, false = it passes), `confidence` (0 to 1), `reason` (one sentence that quotes the output).

## G01

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

### Item D01

### Check B3

B3. Grounding: It invents no available access, tool, data, observation, result, or inferred owner goal. Unconfirmed dependencies get first checks. Inferred goals are marked as assumptions in the prompt. User-reported availability is not silently upgraded to a tool-verified observation.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Item D04

### Check B6

B6. Authority: Added scope, new access, paid steps, and irreversible actions are conditional on approval inside the prompt, not only in commentary. Explicitly prohibited expansions remain prohibited. A response with no expansion passes without needing an irrelevant approval ritual.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

## G02

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

### Item D02

### Check B3

B3. Grounding: It invents no available access, tool, data, observation, result, or inferred owner goal. Unconfirmed dependencies get first checks. Inferred goals are marked as assumptions in the prompt. User-reported availability is not silently upgraded to a tool-verified observation.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Item D03

### Check B2

B2. Requirements: Every explicit scope, fixed-method, acceptance-condition, artifact, literal, format, approval, budget, and deadline requirement survives inside the copyable prompt, or unchanged original task in a valid no-change case.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Item D07

### Check B6

B6. Authority: Added scope, new access, paid steps, and irreversible actions are conditional on approval inside the prompt, not only in commentary. Explicitly prohibited expansions remain prohibited. A response with no expansion passes without needing an irrelevant approval ritual.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Item D10

### Check B7

B7. Stretch honesty: If a stretch is selected, it has a task-specific method, preserves the owner's required pass bar, stays within explicit resource bounds, and reports honest results and misses. Qualitative work is not given an arbitrary numeric improvement ratio.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

