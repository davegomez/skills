# Blind review pack, grouped

Each group shows one task and one output once, then the items to grade for that output. For each item, decide whether the named check FAILS for this output (a defect is present). Use the rubric text quoted in the item and INTERPRETATIONS.md. Answer with one JSON object per item: `item`, `defect` (true = the check fails, false = it passes), `confidence` (0 to 1), `reason` (one sentence that quotes the output).

## G07

### Task

```text
Our nightly pipeline that rebuilds the reporting tables takes about 4 hours, and analysts wait for it each morning. Get it under 3 hours. It runs on our existing Airflow and Postgres setup. No new infrastructure spend and no changes to the report definitions.
```

### Output

````markdown
```text
Our nightly pipeline that rebuilds the reporting tables takes about 4 hours, and analysts wait for it each morning. Get it under 3 hours.
Assumption: the outcome that matters is analysts having correct reporting tables when they start work, so also report when each table becomes available, not only total runtime.
Assumption: the rebuilt tables must contain exactly the same data the current pipeline produces for the same inputs; speed must not change results.
Baseline before changing anything. "About 4 hours" is a user report, not a measurement. If Airflow metadata history is kept, pull task-instance start, end, queued, and retry times for recent runs. Compute run-to-run variance and each run's wall-clock time from DAG run start to the final reporting-table commit. Record source row counts per run so runtime can be compared against data volume.
Find the critical path. Treat the DAG as a scheduling graph and compute the longest dependency path from the measured task durations. Only tasks on that path shorten wall-clock time. Report slack per task, and separate queued time (waiting for pool slots or workers) from running time. Recompute the path after each change, because it moves.
Diagnose critical-path tasks from raw database evidence, not task durations alone: EXPLAIN (ANALYZE, BUFFERS) on their queries, pg_stat_statements if enabled, and wait events and lock waits from pg_stat_activity and pg_locks sampled during a run. Classify each task's time as CPU, I/O, lock wait, or queueing. For each bottleneck, try the fix suited to its cause: rewrite plans that use nested loops over large sets or repeat scans; ANALYZE staging tables after bulk loads so the planner's statistics are current; drop indexes on pipeline-owned staging tables before bulk loads and rebuild them afterward; use UNLOGGED tables for intermediate data the pipeline can regenerate; replace row-by-row or DELETE-then-INSERT patterns with set-based or COPY loads; remove false DAG dependencies so independent branches run in parallel.
Test parallelism against contention, not by assumption. Adding concurrent tasks helps only while the database is not saturated. Measure throughput at increasing concurrency and stop where I/O or lock waits start rising.
Where source tables support reliable change detection, replace full rebuilds with incremental refresh using a watermark kept in a pipeline-owned state table. Keep the full rebuild as a fallback path.
Red-team every incremental or rewritten step before trusting it. Construct inputs with late-arriving rows, updates and deletes in source tables, duplicate keys, NULLs in join and grouping keys, and a backfill of an old date. Show that the optimized output still matches a full rebuild on each.
Once the critical path is short, order the remaining work so the tables analysts open first commit earliest. In Airflow, use priority_weight on this DAG's own tasks.
Aim for under 18 minutes of wall-clock time (one-tenth of the 3-hour bar), using incremental refresh plus critical-path work. When one approach stalls, try the next before reporting a miss. The pass bar stays under 3 hours. Report the stretch result separately, met or missed.
Compare baseline and new runtimes under comparable conditions: same data volume, or runtime normalized by row counts, on the same database, at a comparable time of night.
Requirements: run on the existing Airflow and Postgres setup; no new infrastructure spend; no changes to the report definitions.
With my approval only: change Postgres server-wide settings (postgresql.conf, shared_preload_libraries, or anything that needs a restart), including enabling pg_stat_statements or auto_explain if they are not already on.
With my approval only: raise work_mem, maintenance_work_mem, or parallel-worker settings inside pipeline sessions, because these draw on the memory and worker pool shared with other database users.
With my approval only: add indexes to, or otherwise alter, source tables that the pipeline does not own.
With my approval only: change Airflow pool sizes, global parallelism, or scheduler and executor settings shared with other DAGs.
With my approval only: move the DAG's scheduled start time.
With my approval only: publish reporting tables by build-then-rename swap, which affects dependent views, grants, and readers of those tables.
With my approval only: run benchmark replays or parallel trial runs against the production Postgres instance.
With my approval only: add a recurring runtime and table-availability SLO alert for this DAG.
First check: how many days of task-instance history the Airflow metadata database keeps.
First check: whether pg_stat_statements and auto_explain are already enabled.
First check: whether a non-production Postgres instance with production-scale data exists within current infrastructure for replays. If none exists, do not replay against production without the approval above.
First check: what time analysts start work, and which reporting tables they open first. Get this from the owner, or from query logs if those are kept.
First check: whether source tables have trustworthy change-tracking (updated_at columns, soft deletes, or change data capture) that makes incremental refresh correct. Where they don't, keep full rebuilds for those tables.
First check: which Airflow pools, workers, and Postgres resources this DAG shares with other workloads.
Name any failed check, continue only with supported, authorized work, and mark the affected results unverified.
Judge: on at least 5 runs, either consecutive production nights or replays of 5 distinct nightly input snapshots at comparable volume, with the unmodified pipeline run on the same inputs as the baseline, wall-clock time from DAG run start to final reporting-table commit is under 3 hours on every run, and every reporting table matches the baseline output. Matching means equal row counts and empty EXCEPT ALL in both directions, compared as multisets. Two allowances must be listed before the comparison: pipeline-metadata columns such as refresh timestamps are excluded, and floating-point columns are compared at a stated tolerance. The red-team cases also pass. Report per run: baseline and new runtime, source row counts, the critical path before and after, each table's commit time against analysts' start time, and the 18-minute stretch, met or missed. Any run not measured or table not compared leaves the result unverified.
```

- `altitude`: The outcome moves from total runtime under 3 hours to correct tables in analysts' hands by start of day. Each table's commit time is reported against analysts' start time, and first-needed tables are ordered first. Needs the analysts' start time and table priorities from the owner.
- `depth`: Measures the baseline from Airflow task-instance history, because "about 4 hours" is unverified and nightly runs vary. Comparisons are normalized for data volume.
- `depth`: Uses critical-path analysis of the DAG so effort goes only to tasks that set wall-clock time. Separates queued time from running time.
- `depth`: Diagnoses tasks from EXPLAIN (ANALYZE, BUFFERS), pg_stat_statements, and wait and lock sampling, then applies cause-specific fixes. Ungated fixes touch only pipeline-owned objects and queries.
- `depth`: Sets an 18-minute stretch target through incremental refresh, reported separately from the 3-hour pass bar. Risk: incremental logic can be subtly wrong, which the red-team and equivalence checks below cover.
- `depth`: The judge compares outputs as multisets against the unmodified pipeline in both directions, with tolerances declared before comparison. This enforces "no changes to report definitions" mechanically and doesn't reject correct float results.
- `range`: Borrows from capacity and queueing analysis. Concurrency is raised only until contention appears, so added parallelism doesn't slow the run.
- `range`: Borrows red-team and differential testing. Late, updated, deleted, duplicate, and NULL-key inputs plus a backfill are run against a full rebuild to catch incremental-refresh errors that a normal night would hide.
- Gated, with shared-resource effects:
  - server-wide Postgres settings and extensions
  - session memory and parallel-worker increases
  - indexes on source tables the pipeline doesn't own
  - shared Airflow pools and executor settings
  - schedule changes
  - rename-swap publishing
  - load from benchmarking on production
  - a new recurring SLO alert
- Skipped: none. All three lenses contribute.
- Owner actions:
  - Supply the analysts' start time and which tables they need first.
  - Confirm how long Airflow keeps history, whether pg_stat_statements is enabled, whether a non-production replay database exists, whether source tables support change tracking, and which resources are shared.
  - Decide each "With my approval only" line.
````

### Item D09

### Check B2

B2. Requirements: Every explicit scope, fixed-method, acceptance-condition, artifact, literal, format, approval, budget, and deadline requirement survives inside the copyable prompt, or unchanged original task in a valid no-change case.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

## G08

### Task

```text
In README.md replace the single exact string "npm instal" with "npm install". Change no other byte. Verify that the diff contains exactly that one replacement. Do not add a test file, run an install, or reformat the document.
```

### Output

````markdown
```text
In README.md replace the single exact string "npm instal" with "npm install". Change no other byte.
Locate the target before editing. "npm instal" is a prefix of "npm install", so a plain search or replace-all also matches text that is already correct. Count only occurrences of "npm instal" that are not immediately followed by "l". If that count is not exactly 1, stop without editing and report each match's line and byte offset.
Make the change as a single insertion of "l" directly after the one identified occurrence, not as a replace-all. Keep the original bytes in memory for comparison, and add no file to the project.
Do not add a test file, run an install, or reformat the document.
First check: README.md exists and is readable and writable. If it is not, report that and stop.
Judge: build the expected bytes from the original README.md by inserting the single byte "l" at offset (match offset + 10) of the one identified occurrence, then compare them with the edited file. Pass only if all of these hold: the comparison is byte-for-byte identical, including encoding, line endings, BOM, and final newline; the file grew by exactly 1 byte; the diff shows exactly one changed line, differing only by that inserted "l"; no test file was added and no install was run. A match count other than 1 leaves the result unverified.
```

- `depth`: the prompt now guards against the prefix collision. "npm instal" also matches inside the correct "npm install", so a naive count or replace-all could miscount, or turn correct text into "npm installl". The prompt counts only occurrences not followed by "l" and stops if the count is not exactly 1. No scope, cost, or access effect.
- `depth`: the judge now compares the whole file against the expected bytes, built from the original plus only the specified insertion. A line diff alone can miss changes to line endings, the BOM, the final newline, or encoding that an editor might make silently. This enforces "Change no other byte" directly and keeps the owner's diff check. It adds no file.
- Skipped: `altitude`, because this is a one-string typo fix with stated boundaries and nothing worth climbing toward. `range`, because no other field's method improves an exact single-byte edit.
- Owner actions: none required. If the executor reports zero or several misspelled occurrences, decide which one, if any, to fix.
````

### Item D11

### Check B2

B2. Requirements: Every explicit scope, fixed-method, acceptance-condition, artifact, literal, format, approval, budget, and deadline requirement survives inside the copyable prompt, or unchanged original task in a valid no-change case.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Item D22

### Check T4a

T4a. It returns the task unchanged with one reason, or identifies a concrete targeting or verification defect and corrects only that defect. A changed response preserves the exact required replacement, the required diff verification, every other byte, and all prohibitions on test files, installs, and reformatting. Paraphrase or an extra checklist without a concrete repair fails. Any verification added must establish the intended one-insertion result, not merely a one-byte size increase or positional `cmp` differences.

Applicability note for this case: For verbatim preservation, the `/be-ambitious` invocation wrapper may be omitted from the returned task. The task payload must otherwise remain unchanged. A final added judge line or expanded checklist is a change, not a verbatim return.

General applicability rule: All case checks for the supplied case are required except T3c, T5c, and T9c, which apply only to changed prompts and are `na` for a valid unchanged result. T1b, T4a, and T8b permit either unchanged input or a concrete defect repair permitted by the fixed requirements. T12 requires a changed response. A changed response still requires all applicable common checks. Empty input is an allowed branch only for T10.

## G09

### Task

```text
Our nightly pipeline that rebuilds the reporting tables takes about 4 hours, and analysts wait for it each morning. Get it under 3 hours. It runs on our existing Airflow and Postgres setup. No new infrastructure spend and no changes to the report definitions.
```

### Output

````markdown
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
````

### Item D18

### Check B6

B6. Authority: Added scope, new access, paid steps, and irreversible actions are conditional on approval inside the prompt, not only in commentary. Explicitly prohibited expansions remain prohibited. A response with no expansion passes without needing an irrelevant approval ritual.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

