```text
Our nightly pipeline that rebuilds the reporting tables takes about 4 hours, and analysts wait for it each morning. Get it under 3 hours.
Assumption: the outcome that matters is analysts having correct, complete reporting tables when their morning starts, every morning, not only a lower average runtime.
Assumption: "about 4 hours" is a user report; the baseline is the wall-clock time measured from Airflow run history, from DAG run start to the last reporting table written.

Method:
- Baseline from raw evidence, not impressions. If run history is kept, extract per-task start, end, queued time, retries, and sensor wait from Airflow's task-instance records over as many recent nightly runs as exist. Report median and slowest run. Note source row counts per night so later runs are compared under comparable volumes.
- Critical path first. Treat the DAG as a project schedule and compute its critical path (critical path method from operations research) from the measured durations. Only tasks on that path shorten wall-clock time. Separate each critical task's time into compute, waiting on locks or I/O, queueing for an Airflow slot, and waiting on upstream sensors. Use theory of constraints: work on the single biggest constraint, re-measure, then move to the next. Do not tune off-path tasks.
- Diagnose critical SQL with Postgres's own instruments. Use EXPLAIN (ANALYZE, BUFFERS) on the critical statements, use pg_stat_statements or slow-query logs if they are enabled, and sample pg_stat_activity wait events and pg_locks during a run. These show whether time goes to sequential scans, spills to disk, index maintenance during loads, lock contention between parallel tasks, or stale planner statistics.
- Apply fixes within the existing setup, highest measured gain first:
  - Build into a fresh table and swap it in, so indexes are created after the bulk load instead of maintained row by row.
  - Load with COPY or INSERT ... SELECT, not row-at-a-time writes.
  - Run ANALYZE on newly built tables before downstream steps read them.
  - Remove redundant recomputation shared by several reports.
  - Rewrite slow queries into equivalent plans.
  - Split independent work so the DAG runs it in parallel.
- Incremental refresh. Where source tables have reliable change tracking, rebuild only affected partitions or keys instead of everything. Change tracking means update timestamps, soft deletes, or append-only history. The output must equal a full rebuild, including after source updates, deletes, late-arriving rows, and a mid-run failure followed by retry.
- Concurrency limit. Before raising parallelism, measure throughput at increasing concurrency against Postgres. Fit the curve with the Universal Scalability Law (from queueing and capacity planning) to find where contention makes more parallel tasks slower. Set concurrency at or below that peak.
- Aim for under 18 minutes wall-clock using incremental refresh plus the critical-path fixes. If one approach stalls, try the next before reporting a miss. The owner's 3-hour bar remains the pass condition. Report the 18-minute stretch separately, met or missed, using the same metric and comparable volumes as the baseline.
- Red-team the result before cutover. Look for nights on which the new pipeline would be slower or wrong: the largest historical source volume, month-end or backfill loads, late-arriving upstream data, and a retry after a partial failure. Run each case you can reproduce and report the outcome.
- Report per-table finish times as well as total runtime, so the owner can see when the tables analysts use first become available.

Requirements:
- Runs on the existing Airflow and Postgres setup.
- No new infrastructure spend.
- No changes to the report definitions. Every reporting table's contents must equal what the current pipeline produces from the same source data.

With my approval only: run the modified pipeline as a shadow build into a separate schema on the shared Postgres server, alongside or after the production run, to compare outputs and timings on identical source data.
With my approval only: change Airflow pool sizes, worker slots, or DAG-level concurrency limits that other DAGs share.
With my approval only: change Postgres server-wide settings, such as parallel worker limits, checkpoint, WAL, or autovacuum settings, including any that require a restart.
With my approval only: raise per-session work_mem or maintenance_work_mem for pipeline sessions above current values, since this draws on memory shared with other workloads.
With my approval only: use UNLOGGED tables for intermediate staging data, which are lost on crash and are not replicated.
With my approval only: add indexes to source tables that other systems write to or read from.
With my approval only: publish each reporting table as soon as it is built, instead of all tables together, which changes when and in what combination analysts see updated data.
With my approval only: change the DAG's schedule or start time, which analysts and downstream jobs rely on.

First check: whether Airflow task-instance history is kept for recent nightly runs, how many runs it covers, and whether its measured runtime matches the reported ~4 hours.
First check: whether you can run EXPLAIN on the pipeline's queries and read pg_stat_activity and pg_locks, and whether pg_stat_statements or slow-query logging is already enabled.
First check: which source tables have reliable change tracking (update timestamps, soft deletes, or append-only design) suitable for incremental refresh.
First check: whether a non-production environment exists on the current infrastructure for comparison runs, and whether analysts read reporting tables from a replica.
First check: when analysts start each morning and which tables they open first; ask the owner if this is not documented.
If a check fails, name what is missing, continue only with supported, authorized work, and mark the affected result unverified.

Judge: pass only if all three hold. (1) Runtime: wall-clock time from DAG run start to the last reporting table written is under 3 hours on every one of at least 5 measured runs on source volumes comparable to the baseline, with median, slowest, and volumes reported against the measured baseline. (2) Correctness: every reporting table is identical to the current pipeline's output from the same source snapshot, checked as a full two-way EXCEPT ALL row diff plus row counts. The only differences allowed are ones that also appear between two runs of the current pipeline on that same snapshot. For incremental refresh, this includes snapshots with source updates, deletes, late-arriving rows, and a retry after a mid-run failure. (3) The 18-minute stretch is reported separately as met or missed. Any result not covered by these runs stays unverified.
```

**Ledger**

- `altitude`: The original outcome was a pipeline under 3 hours. The improved outcome is correct tables ready when analysts start, every morning. This adds per-table finish times, a slowest-night check, and gated options for early publishing and schedule changes. Scope stays the same unless the owner approves those options.
- `depth`: Measured baseline from Airflow task-instance history instead of the reported ~4 hours. This avoids optimizing against a wrong number. It needs run history to be kept.
- `depth`: Critical-path analysis plus Postgres diagnostics (EXPLAIN ANALYZE/BUFFERS, pg_stat_statements, wait events, locks). Effort goes only to tasks that shorten wall-clock time. It needs read access to the database.
- `depth`: Build-and-swap, bulk loads, post-load ANALYZE, and incremental refresh, with full-rebuild equivalence required. This is the largest likely gain. Incremental refresh carries correctness risk, which the judge's update/delete/late-row/retry snapshots cover.
- `depth`: Stretch target of under 18 minutes (one order of magnitude past the 3-hour bar), reported separately. This pushes toward incremental designs. Missing it does not fail the task.
- `depth`: Exact two-way row diff, with a baseline-vs-baseline run setting the noise floor. This proves "no changes to report definitions" without rejecting correct work over nondeterminism already present in the current pipeline.
- `range`: Operations research (critical path method) and theory of constraints. These keep tuning focused on the one bottleneck that sets total runtime.
- `range`: Capacity planning (Universal Scalability Law). This finds the concurrency at which Postgres contention makes more parallel tasks slower, so parallelism doesn't backfire.
- `range`: Red-team pass on worst-case nights and failure/retry. This exposes slow-night and silent-wrong-data risks before analysts depend on the new pipeline.
- Skipped: none. All three lenses contributed.
- Owner actions:
  - Confirm access to Airflow run history and to Postgres diagnostics.
  - Tell the runner when analysts start and which tables they use first.
  - Decide on each "With my approval only" line: shadow runs, shared pools, server settings, session memory, UNLOGGED staging, source-table indexes, per-table publishing, schedule change.
