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
