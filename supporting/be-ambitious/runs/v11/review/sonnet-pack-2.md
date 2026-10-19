# Blind review pack, grouped

Each group shows one task and one output once, then the items to grade for that output. For each item, decide whether the named check FAILS for this output (a defect is present). Use the rubric text quoted in the item and INTERPRETATIONS.md. Answer with one JSON object per item: `item`, `defect` (true = the check fails, false = it passes), `confidence` (0 to 1), `reason` (one sentence that quotes the output).

## G03

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

### Item D05

### Check B3

B3. Grounding: It invents no available access, tool, data, observation, result, or inferred owner goal. Unconfirmed dependencies get first checks. Inferred goals are marked as assumptions in the prompt. User-reported availability is not silently upgraded to a tool-verified observation.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Item D09

### Check B6

B6. Authority: Added scope, new access, paid steps, and irreversible actions are conditional on approval inside the prompt, not only in commentary. Explicitly prohibited expansions remain prohibited. A response with no expansion passes without needing an irrelevant approval ritual.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

## G04

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

### Item D06

### Check B6

B6. Authority: Added scope, new access, paid steps, and irreversible actions are conditional on approval inside the prompt, not only in commentary. Explicitly prohibited expansions remain prohibited. A response with no expansion passes without needing an irrelevant approval ritual.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

## G05

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

### Item D08

### Check B6

B6. Authority: Added scope, new access, paid steps, and irreversible actions are conditional on approval inside the prompt, not only in commentary. Explicitly prohibited expansions remain prohibited. A response with no expansion passes without needing an irrelevant approval ritual.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

