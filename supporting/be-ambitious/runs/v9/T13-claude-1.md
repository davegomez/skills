```text
Our nightly pipeline that rebuilds the reporting tables takes about 4 hours, and analysts wait for it each morning. Get it under 3 hours. It runs on our existing Airflow and Postgres setup.
Assumption: what analysts care about is the clock time when the reporting tables they use are ready, not runtime alone. Alongside total runtime, report when each reporting table is committed relative to the scheduled start.
Assumption: "no changes to the report definitions" means every reporting table keeps its schema, rows, and values. The SQL and physical execution that produce them may change. If the definitions are meant to be the SQL text itself, limit the work to scheduling, concurrency, indexing, and physical storage changes, and make no query rewrites or incremental logic.
Start from raw evidence, not impressions. Pull start, end, queue, and retry times for every task over at least the last 30 runs from the Airflow metadata database (task_instance, dag_run). Split each morning's wait into four parts: upstream data arrival delay, scheduler queue time, run time, and retries. If late upstream data dominates, say so before optimizing runtime, because a faster run will not help analysts in that case.
Build the DAG's critical path from those durations (critical path method from project scheduling). The wall clock equals the longest chain of dependent tasks. Speeding up tasks off that chain changes nothing, so rank the work by each task's contribution to the critical path.
Treat database capacity as a shared, limited resource. Sample pg_stat_activity wait events during a run to see whether parallel tasks are waiting on CPU, I/O, or locks. Set Airflow pools and max_active_tasks to the concurrency the database actually sustains, which can be lower than what the DAG allows.
For each heavy critical-path query, use EXPLAIN (ANALYZE, BUFFERS) and pg_stat_statements, where already enabled, to find the cause: bad join order from stale statistics, missing indexes, sorts spilling to disk, row-by-row loops. Apply the matching fix inside the pipeline:
- set-based rewrites;
- session-level SET work_mem;
- loading into staging or UNLOGGED tables, then building indexes and running ANALYZE after the load;
- CREATE TABLE AS plus a rename swap instead of DELETE and INSERT;
- incremental rebuilds that recompute only the partitions or keys whose source rows changed, where this provably yields the same output as a full rebuild.
Aim for under 18 minutes wall clock, measured the same way as the baseline. Get there by combining critical-path shortening, right-sized concurrency, and incremental rebuilds. When one approach stalls, try the next before reporting a miss. The under-3-hours bar remains the pass condition. Report the 18-minute stretch separately, met or missed.
Red-team any incremental logic. Pick past dates where the full rebuild and an incremental rebuild are most likely to diverge: late-arriving rows, updates or deletes to rows from earlier days, backfills, month or quarter boundaries. Replay those dates through both and compare.
Deliver the changed pipeline code and a short report with these parts:
- baseline and candidate timings measured under comparable conditions;
- the critical path before and after;
- per-table ready times;
- the morning wait decomposition;
- equivalence results for every reporting table.
Keep it on the existing Airflow and Postgres setup, with no new infrastructure spend and no changes to the report definitions.
With my approval only: change Postgres server-level parameters (for example max_parallel_workers, maintenance_work_mem, or enabling pg_stat_statements/auto_explain via shared_preload_libraries), which may need a restart and affect other workloads on the server.
With my approval only: add indexes or partitioning to source tables the pipeline reads but does not own.
With my approval only: run the candidate pipeline in a shadow schema alongside production for 5 consecutive nights, on existing storage and capacity, before it replaces the production DAG.
With my approval only: deploy the changed DAG to the production nightly schedule.
First check: read access to the Airflow metadata database exists. A non-production Postgres environment with production-volume data exists, or an off-hours window on production is permitted for test runs. pg_stat_statements is already enabled or not. Disk headroom can hold a second copy of the reporting tables for comparison and shadow runs without new spend. Other workloads share the Postgres server or not. Analysts' usual start time is known. If any check fails, name it, continue only with supported and authorized work, and leave the affected results unverified.
Judge: run the baseline pipeline twice and the candidate pipeline at least 3 times on the same production-volume input snapshot (or across the approved shadow nights) under comparable load; pass only if every candidate run's wall clock from first task start to last reporting table committed is under 3 hours, and every reporting table matches the baseline as a multiset of rows (equal row counts and empty symmetric EXCEPT, or equal hashes over all columns), with the only allowed differences being columns or values that also differ between the two baseline runs (such as load timestamps or float sums from parallel aggregation), including on the replayed late-arrival, correction, backfill, and period-boundary dates; any other mismatch fails, and the 18-minute stretch is reported separately as met or missed.
```

**Ledger**

- `altitude`: The original outcome was a 4-hour runtime cut to under 3 hours. The improved outcome is reporting tables ready when analysts start, shown by per-table ready times and a breakdown of the morning wait. This catches the case where upstream data, not runtime, causes the wait. It adds no scope beyond measurement.
- `depth`: Raw Airflow task history, EXPLAIN (ANALYZE, BUFFERS), pg_stat_statements, and wait-event sampling replace guesswork. Fixes target measured causes and stay inside the pipeline. This needs read access to the metadata database and statistics views.
- `depth`: The under-18-minute stretch, mainly via incremental rebuilds, is reported separately. The 3-hour bar stays the pass condition. Incremental logic carries a correctness risk, which the equivalence judge and replays cover.
- `depth`: The judge adds output equivalence against two baseline runs. Without it, a pipeline could pass "under 3 hours" while silently changing report output. Calibrating against two baseline runs prevents false failures from timestamps or float nondeterminism. Comparison copies use existing disk.
- `range`: The critical path method from project scheduling directs effort to the chain that actually sets the wall clock.
- `range`: Resource-constrained scheduling (pools sized from database wait events) shows when extra parallelism only adds contention.
- `range`: Red-team replay of adversarial dates tests the riskiest claim: that incremental rebuilds equal full rebuilds.
- `range`, with approval: A 5-night shadow run gives a parallel trial before cutover. It is a new recurring workload on the existing database.
- Skipped: none. All three lenses contributed.
- Owner actions:
  - Confirm what "report definitions" covers: outputs only, or the SQL text too.
  - Confirm access to the Airflow metadata database and the statistics views, a test environment or off-hours window, disk headroom, any workloads that share the server, and analysts' start time.
  - Decide on each approval line: server parameters, source-table indexes or partitioning, shadow runs, and production deployment.
