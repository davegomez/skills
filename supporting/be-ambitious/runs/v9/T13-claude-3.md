```text
Our nightly Airflow pipeline that rebuilds the reporting tables takes about 4 hours, and analysts wait for it each morning. Get it under 3 hours.
Assumption: the real need is that analysts can rely on correct reporting tables earlier every morning, so a typical night and a bad night both matter.
Assumption: runtime means end-to-end DAG wall clock, from the first task's start to the last task's end, as recorded in the Airflow metadata DB.
Assumption: a report definition is each table's columns, grain, and values. Rewriting how the SQL computes those values is allowed only when the equivalence check below proves the output is unchanged.

Baseline from raw evidence before changing anything:
- Pull task_instance history for recent runs from the Airflow metadata DB. For each task, split queued time (queued_dttm to start_date) from execution time. Queued time is waiting on pools, slots, or sensors. Execution time is work.
- Build the DAG's critical path (critical path method, from project scheduling). Only critical-path tasks set wall-clock time, so shortening an off-path task gains nothing until the path shifts.
- Report runtime as p50 and p90 across nights, alongside source row volumes per night, so one lucky night doesn't count as a win.
- For each critical-path task, find where the time goes with EXPLAIN (ANALYZE, BUFFERS), pg_stat_statements or auto_explain if already enabled, and pg_stat_activity wait events. Separate CPU, I/O, lock waits, and spills to disk.

Fix the biggest measured costs first, using only what the existing Airflow and Postgres already provide:
- Parallelize independent branches with existing pools and max_active_tasks.
- Load with CREATE TABLE AS into a new table plus an atomic rename swap, instead of DELETE/INSERT.
- Use UNLOGGED staging tables for intermediates that are rebuilt nightly anyway.
- Build indexes after bulk loads, then ANALYZE before downstream reads.
- Raise work_mem or parallel-query settings per session where spills or serial scans dominate.
- Add indexes or rewrite queries where plans show avoidable scans.
- Use incremental refresh (watermark or changed-key based) for tables whose sources only changed partly, provided updates and deletes in the source are handled.
- Aim for under 18 minutes end-to-end, one order of magnitude below the 3-hour bar. When one approach stalls, try the next. Report the stretch result separately, met or missed. The 3-hour bar remains the pass condition.

Red-team correctness with differential testing:
- Run the baseline pipeline and the optimized pipeline on the same source snapshot and compare every reporting table.
- Replay a night that includes late-arriving, updated, and deleted source rows, so incremental logic that misses changes is caught.
- Run the baseline twice to measure its own run-to-run variation in floating-point columns. Parallel aggregation can reorder float sums.

Requirements: it runs on the existing Airflow and Postgres setup. No new infrastructure spend. No changes to the report definitions. Deliver the changed DAG and SQL, the baseline and after measurements, and the equivalence results.
With my approval only: change server-wide Postgres settings (postgresql.conf, including enabling pg_stat_statements via shared_preload_libraries), which affect every other workload on that server.
With my approval only: change Airflow-level executor, parallelism, or worker configuration beyond this DAG's own settings.
With my approval only: publish each reporting table to analysts as soon as it and its upstream tables are complete, with a per-table readiness signal, ordered by which tables analysts query first according to Postgres statistics.
With my approval only: move the DAG's scheduled start earlier if the upstream source data is reliably complete before the current start time.
First check: read access to the Airflow metadata DB task history for recent runs; a non-production schema or database on existing hardware where a source snapshot and both pipeline versions can run without loading production; permission to deploy DAG and SQL changes to production. Name any missing dependency and continue only with supported, authorized work. Leave the affected results unverified.
Judge: on the same source snapshot, including the late/updated/deleted-row replay, every reporting table from the optimized pipeline matches the baseline's output (equal row counts and empty symmetric EXCEPT in both directions, excluding only columns that record build time, with floating-point columns differing by no more than the baseline's own measured run-to-run variation), and Airflow-recorded end-to-end wall clock is under 3 hours on every one of at least 5 consecutive production nights whose source volumes fall within the baseline nights' range, reported as p50/p90 against the 4-hour baseline with the 18-minute stretch stated separately as met or missed.
```

- `altitude`: the original outcome was a pipeline under 3 hours. The improved outcome is correct tables reliably ready earlier, judged on p50/p90 across nights. Early per-table publishing and an earlier start are offered behind approval because they change what analysts see and the recurring schedule.
- `depth`: the work starts from raw Airflow task_instance timings, the critical path, and EXPLAIN/wait-event evidence instead of guessing. It adds named Postgres bulk-load techniques and an 18-minute stretch target via incremental refresh. Risk: incremental logic can miss source changes, which the replay red-team covers.
- `depth`: a table-level equivalence check enforces "no changes to report definitions," which a runtime-only judge can't detect. It tolerates float variation from parallel aggregation, so correct work isn't rejected.
- `range`: from operations research, the critical path method finds which tasks actually set wall clock. From lean/queueing, splitting queued from executing time exposes slot and pool waits that SQL tuning won't fix.
- `range`: from SRE, using p50/p90 over at least 5 nights at comparable volume stops one fast night from passing.
- `range`: from software testing, differential testing with a late/updated/deleted-row replay red-teams the incremental-refresh correctness claim.
- Scope: server-wide Postgres changes and Airflow-wide config changes are behind approval because they affect other workloads. Per-session settings and this DAG's own settings stay in scope.
- Skipped: none. All three lenses contributed.
- Owner actions:
  - Confirm metadata DB access, a non-production snapshot location on existing hardware, and production deploy rights.
  - Decide on the four approval lines: server Postgres config, Airflow-wide config, per-table early publishing, earlier schedule.
  - Confirm that "report definition" means outputs, not literal SQL text. If you mean the SQL text itself, drop the query-rewrite and incremental items.
