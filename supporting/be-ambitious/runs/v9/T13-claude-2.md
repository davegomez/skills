```text
Our nightly pipeline that rebuilds the reporting tables takes about 4 hours, and analysts wait for it each morning. Get it under 3 hours.
Assumption: the real goal is that the reporting tables analysts use first are correct and ready before analysts start work every morning, including slow nights, not only on an average night.
Assumption: other DAGs and workloads that share this Airflow and Postgres setup must not get slower because of this change.

Baseline from raw evidence before changing anything. Pull per-task start, end, and queued times for the last 30 runs from the Airflow metadata database. Define one metric: wall-clock time from DAG run start to commit of the last reporting table. Record the median and maximum. Do not rely on the "about 4 hours" figure.
Test the belief the task rests on, that the time goes to compute inside this pipeline. Split each task's time into upstream-sensor wait, queue wait (queued to running), and execution. If sensors or queueing dominate, fix those first. Tuning SQL will not move that time.
Use the critical path method from operations research on the DAG. Build it from the task timings, find the chain of dependent tasks that sets end-to-end time, and spend effort only on that chain. Re-derive the critical path after each change, because it moves. Use Amdahl's law to estimate each change's maximum end-to-end gain before building it.
For each critical-path task, profile in Postgres. Use pg_stat_statements for total and mean time per statement. Use EXPLAIN (ANALYZE, BUFFERS), or auto_explain logs from a real run, to find full scans, misestimated row counts, spills to disk, and nested loops over large inputs. Use pg_stat_activity wait events and pg_locks to find lock and I/O waits.
Apply the standard warehouse-rebuild fixes where the profile supports them:
- Build into a new table and swap it in with a rename, instead of DELETE/INSERT or TRUNCATE/INSERT.
- Load staging tables as UNLOGGED.
- Create indexes after the bulk load, not before.
- Run ANALYZE immediately after each load so downstream queries get correct plans.
- Materialize intermediates that several tables recompute.
- Set work_mem, maintenance_work_mem, and parallel-query settings per session within this DAG only.
- Run independent off-critical-path tasks concurrently using this DAG's own task concurrency.
Where a source is append-only or has a reliable change watermark, replace the full rebuild with incremental maintenance that produces identical output.
Treat concurrency as a queueing problem. Raise parallelism only while wait events show the database is not already saturated on CPU, I/O, or locks. Past that point, more parallel tasks lengthen the critical path.
Hard target: aim for under 18 minutes end to end, one order of magnitude past the 3-hour bar, using critical-path profiling plus incremental maintenance. When one approach stalls, try the next one before reporting a miss. The 3-hour bar remains the pass condition. Report the stretch separately as met or missed.
Use analysts' morning query activity from Postgres statistics to rank tables by first use. Order the critical path so the highest-ranked tables finish earliest within a run that still publishes the full set as it does today.
Red-team the equivalence claim. Build adversarial input cases and confirm optimized output matches baseline output on each:
- source rows updated or deleted after an earlier load
- late-arriving rows behind the watermark
- a month-end and a year-end date
- a timezone or DST boundary
- an empty source partition
- the largest historical night by row volume
Requirements: run on the existing Airflow and Postgres setup; no new infrastructure spend; no changes to the report definitions. Every reporting table keeps its current name, schema, and contents for a given input.

With my approval only: change server-wide Postgres configuration (postgresql.conf settings such as shared_buffers, max_parallel_workers, or max_wal_size) that also affects other workloads on that server.
With my approval only: change Airflow-wide settings or shared pools (parallelism, pool sizes, executor slots) that other DAGs also use.
With my approval only: publish each reporting table as soon as it is complete, with a per-table readiness signal analysts can see, instead of publishing the full set together.
With my approval only: add a recurring alert that fires when the nightly end-to-end runtime exceeds 3 hours or a reporting table misses analysts' start time.

First check: read access to the Airflow metadata database (task_instance, dag_run) for at least the last 30 runs. If it is missing, name the gap and leave the baseline unverified.
First check: pg_stat_statements is enabled and readable, and auto_explain can be enabled per session without a server restart. If not, profile with per-session EXPLAIN (ANALYZE, BUFFERS) only.
First check: an existing non-production environment, or a frozen snapshot of the source data, can run the old and new pipelines on the same input without new spend. If none exists, equivalence stays unverified and changes are not deployed to the production pipeline.
First check: analysts' query statistics on the reporting tables are readable under current access. If not, skip first-use ordering.
First check: list other DAGs and workloads that run in the same window on the same Airflow and Postgres instances, with their last 30 runtimes, as the baseline for interference.
Judge: on the same frozen input, every reporting table from the optimized pipeline has an identical schema and an identical row multiset to the baseline pipeline (EXCEPT ALL returns zero rows in both directions; floating-point columns may differ only within 1e-9 relative because of aggregation order, with each such difference listed), including on every red-team case; the end-to-end metric (DAG run start to last reporting-table commit) is under 3 hours on each of at least 5 runs at production data volume, reported as median and max against the 30-run baseline measured the same way; no co-scheduled DAG's median runtime rises above its baseline 30-run maximum; the 18-minute stretch is reported met or missed; a missing snapshot, baseline, or co-scheduled runtime data leaves the affected criterion unverified, not passed.
```

**Ledger**
- `altitude`: the original outcome is a 4-hour job that runs under 3 hours. The improved outcome is that the tables analysts use first are correct and ready before they start work every night. Ordering by first use stays inside the current publish-all-together behavior. Per-table early publishing changes what analysts see, so it sits behind approval.
- `depth`: the baseline comes from Airflow metadata over 30 runs instead of the "about 4 hours" figure. This turns one anecdote into a distribution and a comparable metric.
- `depth`: splitting time into sensor wait, queue wait, and execution tests the core belief that compute is the problem. If waiting dominates, it avoids effort spent tuning SQL that would not help.
- `depth`: Postgres profiling (pg_stat_statements, EXPLAIN ANALYZE/BUFFERS, auto_explain, wait events) plus build-and-swap, UNLOGGED staging, post-load indexes and ANALYZE, and per-session settings. These are the field's standard instruments and fixes, kept inside this DAG so other workloads are unaffected.
- `depth`: incremental maintenance with an identical-output requirement. This offers the largest possible speedup without changing report definitions. Its risk is silent divergence on updates, deletes, or late rows, which the red-team cases cover.
- `depth`: an 18-minute stretch target, with 3 hours kept as the pass condition and the stretch reported separately.
- `range`: the critical path method and Amdahl's law from operations research. They show which tasks can move end-to-end time, and stop effort on tasks off the critical path.
- `range`: queueing and contention analysis. It stops added parallelism from saturating Postgres and making the run slower.
- `range`: an SRE-style judgment over at least 5 runs, using median and max. It guards against a single lucky night passing the bar.
- `range`: red-team adversarial inputs (updates, deletes, late rows, month-end, DST, empty partitions, peak volume). These test the consequential claim that "no changes to report definitions" holds after optimization.
- Approvals: four "With my approval only" lines.
  - Server-wide Postgres configuration and Airflow-wide pools are gated because they affect other workloads.
  - Per-table publishing is gated because it changes what analysts see during a run.
  - The recurring alert is gated because it is a new recurring workflow.
  - None of the four adds spend or changes report definitions.
- Skipped: none of the three lenses. Moving the schedule earlier was left out, because it could change each night's data cutoff and so touch the report definitions.
- Owner actions:
  - Confirm access to Airflow metadata, pg_stat_statements/auto_explain, and analyst query statistics.
  - Confirm that a non-production environment or frozen snapshot exists at no new cost.
  - List the co-scheduled workloads.
  - Decide on the four approval lines.
