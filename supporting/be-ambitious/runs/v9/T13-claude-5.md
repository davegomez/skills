```text
Cut the nightly pipeline that rebuilds the reporting tables from about 4 hours to under 3 hours, so analysts stop waiting for it each morning.
Assumption: the outcome that matters is every reporting table being correct and ready before analysts start work, with the tables they open first landing first, on slow nights as well as typical ones.
Build the baseline from raw evidence before changing anything. Pull per-task start, end, and queued times for the last 30 nightly runs from the Airflow metadata database (task_instance). Pull per-statement time, rows, and buffer reads from pg_stat_statements, and run EXPLAIN (ANALYZE, BUFFERS) on the slowest statements. Separate time spent running from time spent waiting for a worker slot or pool.
Compute the DAG's critical path, using the critical path method from project scheduling: the chain of dependent tasks whose summed duration sets the finish time. Only shortening that chain shortens the run. After each change, recompute it, because the bottleneck moves (theory of constraints).
Work the critical path with a Postgres performance engineer's instruments, and measure each change on its own:
- Airflow parallelism, pool, and dependency settings, so independent tasks run at the same time.
- Query plans fixed with indexes, fresh statistics (ANALYZE after each load), and rewrites of how a table is built that leave its definition's logic intact.
- Bulk-load patterns: build into a staging table and swap it in, create indexes after the load, and set work_mem and maintenance_work_mem per session.
- Incremental rebuilds, only where the existing report definition is applied unchanged to the changed slice (for example, changed partitions) instead of to the full history.
Aim for under 18 minutes end to end (an order of magnitude past the 3-hour bar) using critical-path reduction and incremental rebuilds. When one approach stalls, try the next before reporting a miss. The 3-hour bar remains the pass condition; report stretch attainment separately, met or missed.
Order the critical path so the tables analysts open first finish first, and report each table's ready time alongside the total.
Prove each change leaves outputs unchanged: run the old and new pipeline on the same input snapshot and compare every reporting table by row count and a two-way EXCEPT ALL on all columns. Compare floating-point columns at the precision the reports display, and exclude columns filled from the run's clock (load timestamps), listing each excluded column.
Red-team the incremental paths. Replay nights with late-arriving rows, updates and deletes to already-loaded history, and a backfill, and confirm the outputs still match a full rebuild.
Report timing from the distribution, as SRE practice does: median and worst night, before and after, at comparable data volumes.
Use only the existing Airflow and Postgres setup. No new infrastructure spend. No changes to the report definitions.
With my approval only: change server-wide Postgres settings (postgresql.conf, such as shared_buffers, max_parallel_workers, or shared_preload_libraries).
With my approval only: run old-versus-new comparison runs on the production Postgres instance, if no non-production environment with a representative data snapshot exists.
With my approval only: add a recurring nightly alert that fires when the run exceeds its time target or an output comparison fails.
First check: read access to the Airflow metadata database covering the last 30 nightly runs; whether pg_stat_statements is already enabled (if not, time statements from Airflow task logs and EXPLAIN ANALYZE on a non-production copy rather than enabling it); a non-production environment with a representative input snapshot for old-versus-new runs; the time analysts need the tables and which tables they open first, confirmed by me; and the deployment path and approver for DAG and SQL changes to the nightly run. Name each missing dependency, continue only with supported, authorized work, and mark affected results unverified.
Judge: Airflow records each of 5 consecutive post-change nightly runs, from DAG start to the last reporting-table task success, under 3 hours, against a baseline of the same metric from the prior 30 runs; and on a shared input snapshot every reporting table matches the old pipeline's output in row count, with a two-way EXCEPT ALL returning zero rows (floating-point columns compared at report display precision, clock-filled columns excluded and listed); the report gives the median, the worst night, per-table ready times, and the 18-minute stretch, met or missed; pass only if every condition holds.
```

**Ledger**
- `altitude`: The original outcome was a total runtime under 3 hours. The improved outcome is correct tables that are ready before analysts start, with the tables they use first landing first and per-table ready times reported. The cost is one owner input (analyst start time and table priority), and there is no scope change.
- `depth`: The baseline comes from raw Airflow task_instance history, pg_stat_statements, and EXPLAIN plans instead of a single "about 4 hours" figure. Separating run time from queue time shows whether the problem is the scheduler or the queries.
- `depth`: The tuning instruments are named: parallelism and pools, plan fixes, staging-and-swap loads, indexes after load, session memory settings, and incremental rebuilds. All of these stay inside the existing Airflow and Postgres setup with no spend.
- `depth`: A stretch target of under 18 minutes, with the 3-hour bar still the pass condition. Plausibly only incremental rebuilds can reach it, and missing it costs nothing.
- `depth`: Old-versus-new output equivalence (row count plus EXCEPT ALL) on a shared snapshot. This enforces "no changes to the report definitions" by its effect, not just by the SQL text. Incremental rebuilds are limited to applying the existing definitions unchanged.
- `range`: The critical path method from operations research, plus the theory of constraints. This keeps effort on the tasks that actually set the finish time.
- `range`: SRE distribution reporting (median and worst night over 5 runs) instead of one good night. This shows whether analysts can rely on the result.
- `range`: Red-teaming the incremental paths with late rows, history updates and deletes, and backfills. These are the cases where incremental refresh silently drifts from a full rebuild.
- Approval-gated:
  - Server-wide Postgres configuration, because it affects other workloads and may need a restart.
  - Comparison runs on production, because of the load they add.
  - A recurring nightly alert, because it is a new workflow.
- Skipped: none. All three lenses contributed.
- Owner actions:
  - Confirm the analyst start time and which tables they open first.
  - Confirm access to the Airflow metadata DB and pg_stat_statements status.
  - Confirm a non-production snapshot environment and the deployment path for DAG and SQL changes.
  - Decide on the three approval-gated additions.
