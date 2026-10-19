```text
Our nightly Airflow pipeline that rebuilds the reporting tables in Postgres takes about 4 hours, and analysts wait for it each morning. Get its end-to-end runtime under 3 hours.
Assumption: the underlying goal is that analysts have correct reporting tables when they start work, and runtime is the lever for that.
Assumption: "report definitions" means the logic that determines each table's contents. Execution changes are allowed only when every table's contents stay identical. These include task ordering and dependencies, parallelism, load method, indexing, statistics, and session-level Postgres settings.
Baseline from raw evidence before changing anything: pull per-task start, end, and queued times for at least the last 14 nightly runs from the Airflow metadata database (task_instance). Pull per-statement timings from pg_stat_statements, the Postgres logs, or auto_explain. Report the baseline end-to-end wall clock (first task start to last task end) as the median and the slowest run, with source row volumes for those nights.
Find where the time goes using the critical path method. Compute the DAG's longest dependency chain from measured durations, and separate time spent running from time spent queued waiting for a slot. Only critical-path work shortens the night (Amdahl's law). Recompute the path after each change, because it moves.
For each critical-path task, diagnose with EXPLAIN (ANALYZE, BUFFERS) and pg_stat_activity wait events. Look for:
- missing or stale statistics
- sorts and hashes spilling to disk
- sequential scans an index would serve
- lock waits between concurrent tasks
- indexes maintained row by row during bulk loads
- DAG dependency edges the SQL does not require
Candidate fixes; keep each only if it measurably helps:
- Remove false dependencies, and raise this DAG's own max_active_tasks so independent rebuilds overlap.
- Build into a staging table with CREATE TABLE AS or COPY. Create indexes and run ANALYZE after the load, then swap tables by rename in one transaction.
- Set work_mem, maintenance_work_mem, and max_parallel_workers_per_gather per session in the heavy tasks.
- Start the longest chains first (longest-processing-time list scheduling).
Treat the single Postgres server as a shared queue. Added concurrency can slow every task by saturating I/O or CPU, so measure throughput at several concurrency levels instead of assuming more is faster.
Aim for an end-to-end runtime under 18 minutes using the critical-path, query-plan, and scheduling work above. Treat this target as solvable: when one approach stalls, try the next candidate before reporting a miss. The 3-hour bar remains the pass condition. Report the stretch result separately, met or missed.
Report the time each reporting table became available in every measured run, so it is visible when analysts can actually start.
Requirements: use the existing Airflow and Postgres setup; no new infrastructure spend; no changes to the report definitions.
With my approval only: change Airflow pool sizes or global parallelism settings that are shared with other DAGs.
With my approval only: change server-wide Postgres settings (postgresql.conf or ALTER SYSTEM), which affect every workload on that server.
With my approval only: rebuild tables incrementally from changed source rows instead of in full. This applies only to tables where I confirm the change does not alter a report definition, and the equivalence check below must pass against a full rebuild, including late-arriving rows and day-boundary records.
With my approval only: run the candidate pipeline in parallel with the current one on production Postgres for comparison. This adds load to production and writes to separate schemas.
With my approval only: move the DAG's start time earlier, if upstream source data is reliably complete earlier.
First check: confirm access to the Airflow metadata database, confirm pg_stat_statements or statement logging is available, and confirm permission to run EXPLAIN ANALYZE on the reporting queries. Name anything missing.
First check: confirm that a non-production Postgres instance exists on existing hardware with production-equivalent data volume for replays. If none exists, report that, and run no experiments against production without the approval above.
First check: confirm that the current pipeline's output for one fixed source snapshot can be preserved as the equivalence baseline. Without it, output equivalence stays unverified.
Judge: pass only if two conditions hold. (1) For at least 5 consecutive runs at production data volume on production or production-equivalent hardware, Airflow metadata shows an end-to-end wall clock (first task start to last task end) under 3 hours on every run. (2) Built from the preserved fixed source snapshot, every reporting table matches the current pipeline's output, with equal row counts and an empty EXCEPT ALL difference in both directions. Numeric and text columns must match exactly, float columns within 1e-9 relative difference, and build-timestamp columns are excluded and listed. Report the stretch result (under 18 minutes) and per-table availability times separately, met or missed.
```

- `altitude`: The original outcome was a pipeline under 3 hours. The improved outcome adds per-table availability times, which show when analysts can actually start work. Earlier start times and incremental rebuilds are offered behind approval. Scope is unchanged without approval.
- `depth`: The baseline comes from raw Airflow task_instance data and pg_stat_statements instead of the reported "about 4 hours". This shows whether the time goes to running work, queueing, or locks. It requires read access to Airflow metadata and Postgres statistics.
- `depth`: EXPLAIN (ANALYZE, BUFFERS), wait events, a staging-table-and-swap load method, and session-level memory and parallelism settings target the actual slow statements. Running EXPLAIN ANALYZE executes the queries, so it adds load wherever it runs.
- `depth`: The hard target of under 18 minutes is reported separately. The 3-hour bar stays the pass condition. The risk is extra effort on a stretch that may be missed.
- `depth`: The judge adds an output-equivalence diff on a fixed source snapshot. This catches speedups that silently change results, which would breach the no-definition-change rule. Float tolerance and excluded timestamp columns stop the check from rejecting correct parallel plans. It requires preserving one baseline output.
- `range`: Operations research contributes the critical path method and longest-processing-time list scheduling. These show which tasks actually set the night's length and keep effort off tasks that don't affect it.
- `range`: Queueing theory treats the single Postgres server as a shared resource. Measuring throughput across concurrency levels exposes the point where added parallelism slows everything.
- `range` (red team): Equivalence edge cases (late-arriving rows, day boundaries) are built into the incremental-rebuild approval line, so a faster but wrong rebuild cannot pass.
- Approval lines: shared Airflow pools and parallelism, server-wide Postgres settings, incremental rebuilds, a parallel trial on production, and an earlier start time. Each one affects other workloads, production load, or the meaning of "report definition", so each is gated.
- Skipped: none. All three lenses contributed.
- Owner actions:
  - Confirm the Assumption reading of "report definitions", and decide whether incremental rebuilds count as a definition change.
  - Decide on each approval line.
  - Confirm Airflow metadata and Postgres statistics access.
  - Confirm whether a production-equivalent non-production instance exists.
  - Allow preserving one baseline output snapshot for the equivalence check.
