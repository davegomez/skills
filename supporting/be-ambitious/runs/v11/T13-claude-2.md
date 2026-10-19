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
