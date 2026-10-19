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
Get our nightly reporting-table rebuild under 3 hours on our existing Airflow and Postgres setup. It reportedly takes about 4 hours, and analysts wait for it each morning. No new infrastructure spend and no changes to report definitions.

Assumption: The intended improvement is earlier availability of complete, equivalent reporting tables—not merely an earlier Airflow success status or work moved outside the measured window.
Assumption: Aim for an end-to-end runtime under 18 minutes using critical-path reduction and evidence-led SQL optimization. This is a stretch target; under 3 hours remains the acceptance threshold.

Establish a measured baseline rather than treating the reported 4 hours as a measurement. Use the same start and analyst-ready completion boundaries for baseline and candidate, accounting for required preparation, queueing, retries, and publication. Compare equivalent input volumes, data cutoffs, resource limits, and competing workloads; disclose differences that prevent a fair comparison.

Use operations research’s critical-path analysis: reconstruct the Airflow dependency graph from the DAG and available task timings, distinguish elapsed time from summed task time, and identify which bottleneck reductions would actually advance completion. Prioritize those changes over optimizing tasks with scheduling slack.

Use database execution-plan analysis to identify the causes of expensive critical-path queries: inspect SQL and EXPLAIN plans, and use EXPLAIN (ANALYZE, BUFFERS) only in an authorized environment where its execution and load are safe. Distinguish excessive row processing, repeated scans, spills, lock waits, and avoidable serialization using available evidence. Make targeted changes and remeasure; when an approach stalls, try the next evidence-supported approach within the existing resource constraints and any owner-confirmed time limit.

Use differential testing from software verification to challenge the claim that faster means equivalent. On identical source snapshots and cutoffs, compare baseline and candidate table schemas and complete row multisets, preserving duplicates and NULL semantics; bidirectional EXCEPT ALL is suitable where supported by the data types. Check report-defined time boundaries, precision, and publication behavior. Use isolated fixtures for relevant duplicate, NULL, empty-input, and date-boundary cases where supported. Hashes or matching row counts alone do not establish equivalence.

Prepare the scoped code changes and a concise evidence summary: measured baseline, bottleneck evidence, changes made, comparable candidate timings, equivalence results, and rollback steps. Report the under-3-hour result and the under-18-minute stretch separately as met, missed, or unverified. Do not claim production performance from an unrepresentative test.

Keep the existing Airflow/Postgres setup. Do not incur new infrastructure spend or alter report definitions, required freshness, or completeness. Do not change server-wide settings or unrelated workloads.

With my approval only: run a bounded deployment and measurement pilot on the shared Airflow/Postgres environment, including any candidate SQL, index, staging-object, or task-concurrency changes that affect shared tables or capacity; present the exact changes, expected load, rollback, and stop conditions before approval.

First check: confirm access and permission to inspect the relevant DAGs, SQL, report definitions, available run history, and execution-plan evidence. Establish the actual pipeline boundaries and available history rather than assuming them.
First check: confirm whether an already-authorized isolated environment, representative source snapshots, and sufficient existing capacity are available for equivalent baseline/candidate runs and differential tests; do not assume a replica or create shared database objects without approval.
First check: confirm any time limit for this work and, before an approved shared pilot, the permitted capacity envelope, workload observations, and rollback mechanism. If a dependency is missing, continue only with supported, authorized work and leave the affected conclusion unverified.

Judge: Automated full-result differential checks must find no schema or row-multiset differences on identical inputs, and report-defined cutoff and publication checks must pass; timing evidence must show three comparable full-scale candidate runs each completing in under 3 hours using the same end-to-end boundaries as the baseline, without hidden preparatory work or extra infrastructure spend; production attainment remains unverified without an approved representative shared-environment pilot; report the under-18-minute stretch separately, and leave any claim with missing evidence unverified.
```

- `altitude`: Moves from a shorter rebuild to earlier availability of equivalent, complete tables; consistent timing boundaries prevent shifting work outside the clock. Shared-environment deployment and measurement require approval.
- `depth`: Replaces the reported four-hour figure with measured baseline evidence and execution-plan diagnosis; adds an under-18-minute stretch while retaining under three hours as the pass condition. Uses existing authorized resources only.
- `range`: Critical-path analysis identifies optimizations that advance completion; differential testing challenges semantic equivalence using complete results and boundary cases rather than counts alone.
- Skipped lenses: None; each contributes a distinct method or outcome check.
- Owner actions: Confirm access, representative test resources, and any time limit; approve the bounded shared-environment pilot before shared-resource changes or measurement load.
````

### Item D03

### Check B2

B2. Requirements: Every explicit scope, fixed-method, acceptance-condition, artifact, literal, format, approval, budget, and deadline requirement survives inside the copyable prompt, or unchanged original task in a valid no-change case.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Item D21

### Check B3

B3. Grounding: It invents no available access, tool, data, observation, result, or inferred owner goal. Unconfirmed dependencies get first checks. Inferred goals are marked as assumptions in the prompt. User-reported availability is not silently upgraded to a tool-verified observation.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Item D23

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
Our nightly Airflow pipeline that rebuilds the reporting tables takes about 4 hours, and analysts wait for it each morning. Get it under 3 hours.
Assumption: the underlying goal is that every reporting table is correct and ready before analysts start reading it each morning, every night, including the heaviest nights. Average-night speed alone is not the goal.
Measure the baseline before changing anything. "About 4 hours" is a user report. Replace it with the measured end-to-end wall-clock of recent nightly runs (first task start to last task end), using Airflow metadata if run history is kept. For each task, separate queued time from running time, and record the median and worst night. Compare later results on the same metric, at comparable source-data volume.
Find the critical path. Build the DAG's dependency graph with measured task durations and compute the critical path (critical path method from project scheduling). Only work on the critical path shortens the run. Then apply the Theory of Constraints: exploit the current bottleneck task before adding resources, re-measure, and move to the next bottleneck.
Remove false serialization in Airflow: dependencies that no data flow requires, sensor waits, retries, scheduler/queue lag, and parallelism caps inside this DAG. Within the DAG's own slots, order ready tasks longest-critical-path-first (list scheduling) so the makespan shrinks.
Diagnose each slow critical-path statement from raw evidence. Use EXPLAIN (ANALYZE, BUFFERS) on the actual statements, plus wait events and lock waits from pg_stat_activity and pg_locks while the pipeline runs. Do not rely on summary durations alone. Fix the cause: repeated scans of the same source, missing statistics after loads (run ANALYZE after each bulk load), sort or hash spills, lock contention between parallel tasks, row-by-row DELETE/INSERT instead of build-into-staging-then-swap, and indexes maintained during bulk load instead of built after it.
Use session-level settings (SET work_mem, SET max_parallel_workers_per_gather) only in the pipeline's own sessions and within the memory the server already has. Pipeline-private intermediate tables the pipeline creates and drops may be UNLOGGED. Published reporting tables stay logged.
Where a definition already takes a date or partition parameter and the source tables have reliable change tracking, rebuild only the partitions whose inputs changed instead of rebuilding everything. Keep the definition text itself as written.
Aim for under 18 minutes end to end (one-tenth of the 3-hour bar) using incremental changed-partition rebuilds and critical-path parallelism. When one approach stalls, move to the next: bottleneck fixes, then removing serialization, then incremental rebuilds, then load-phase restructuring. Report a miss only after trying each one that applies. The 3-hour bar stays the pass condition. Report the stretch separately, met or missed.
Red-team any incremental or reordered build before trusting it. Use a source snapshot with injected cases: late-arriving rows for past dates, updates and deletes to old rows, rows on timezone/DST and month-end boundaries, and an empty day. Try to make its output diverge from a full rebuild.
Calibrate the equality check first. Run the current pipeline twice on the same snapshot and record which columns legitimately differ between those two runs (build timestamps, surrogate ids, floating-point rounding from parallel aggregation). Compare those columns under the same rule, and require exact equality for everything else.
If logs of analyst queries exist, report each table's ready time against its first analyst read on the same nights. This is the measure of whether analysts still wait.
Requirements: run on the existing Airflow and Postgres setup. No new infrastructure spend. No changes to the report definitions: the definitions and the table contents they specify stay as written. If a speedup would need a definition edit, list it as a proposal and do not apply it. Deploy a change to the nightly DAG only after it passes the equality check.
With my approval only: raise pool slots or task priority weights in any Airflow pool this DAG shares with other DAGs.
With my approval only: change Postgres server-wide parameters (for example max_parallel_workers, maintenance_work_mem, checkpoint/WAL settings), with before/after measurement of other workloads during the window.
With my approval only: enable pg_stat_statements, auto_explain, or log_min_duration_statement on the server if they are not already enabled.
With my approval only: add indexes or change the physical layout of source tables or published reporting tables that other pipelines or analysts read.
With my approval only: publish each reporting table as soon as it is built and verified, instead of all at the end of the run, which lets analysts see tables of mixed freshness.
With my approval only: move the DAG's scheduled start time.
With my approval only: run timed trial builds, including the two calibration runs, on an existing non-production Postgres loaded from a recent production snapshot, or in a separate schema on the production server during off-peak hours.
First check: Airflow metadata keeps task-instance history (start, end, queued time, tries) for recent nightly runs; without it, the baseline stays the user-reported ~4 hours and the speedup claim stays unverified until new runs are measured.
First check: you can run EXPLAIN and read pg_stat_activity and pg_locks on the reporting database, and you know which statistics extensions and logging are already enabled.
First check: whether this DAG's Airflow pools and the Postgres server are shared with other DAGs or workloads during the nightly window.
First check: which report definitions are already date- or partition-parameterized and which source tables have reliable change tracking (append-only, or updated_at/deleted markers); incremental rebuilds apply only where both hold.
First check: whether an existing non-production Postgres with comparable data volume exists, and whether analyst query logs exist; missing either leaves the dependent trial or wait-time result unverified.
Judge: on the same source snapshot, including the injected red-team cases, every reporting table from the changed pipeline matches the current pipeline's output (identical schema, equal row counts, EXCEPT ALL empty in both directions, with only the columns shown nondeterministic by the two calibration runs compared under their recorded rule), and measured end-to-end wall-clock from Airflow metadata is under 3 hours on each of the first 5 consecutive nightly production runs after deploy (plus the heaviest periodic night if run history shows one), reported against the measured pre-change median and worst night, with the under-18-minute stretch reported separately, met or missed; any failed equality, missing calibration, or missing run history leaves the speedup unverified.
```

- `altitude`: The original outcome was a pipeline under 3 hours. The improved outcome is every table correct and ready before analysts read it, every night, measured as per-table ready time against first analyst read where logs exist. Early per-table publishing and a schedule shift are gated because they change what analysts see and when.
- `depth`: Replaces the reported "about 4 hours" with a measured median and worst night from Airflow task-instance history, so before and after use the same metric.
- `depth`: Statement-level diagnosis (EXPLAIN ANALYZE/BUFFERS, wait events, lock waits) with named fixes: staging-then-swap, ANALYZE after load, indexes built after load, session-scoped memory, UNLOGGED for private intermediates only. All are inside existing infrastructure.
- `depth`: Hard target of under 18 minutes via incremental rebuilds and parallelism, with an ordered fallback sequence. The 3-hour bar stays the pass condition. Incremental rebuilds apply only where definitions are already parameterized, so definitions are not edited.
- `depth`: The judge requires output equality as well as speed. It is calibrated by running the current pipeline twice, so legitimate nondeterminism (timestamps, ids, float rounding) does not fail correct work. This costs two extra full runs, which are gated.
- `range`: Project scheduling (critical path method, list scheduling) shows which speedups actually shorten the run. Theory of Constraints sequences bottleneck work.
- `range`: Red-team differential testing with late-arriving rows, old-row updates and deletes, DST/month-end boundaries, and an empty day exposes incremental-build errors that a normal night would hide.
- `range`: An SRE-style freshness view judges the worst night and per-table readiness, not the average.
- Gated (approval each): shared pool slots and priorities; server-wide Postgres parameters; enabling server statistics or logging; indexes or layout on shared source or reporting tables; per-table publishing; DAG schedule change; trial and calibration runs on non-prod or off-peak production.
- Skipped: none. All three lenses contributed.
- Owner actions:
  - Confirm Airflow run-history and Postgres diagnostic access.
  - Say whether pools and the server are shared during the window.
  - Identify parameterized definitions and change-tracked sources.
  - Confirm whether a non-prod environment and analyst query logs exist.
  - Decide on each "With my approval only:" line.
````

### Item D04

### Check B3

B3. Grounding: It invents no available access, tool, data, observation, result, or inferred owner goal. Unconfirmed dependencies get first checks. Inferred goals are marked as assumptions in the prompt. User-reported availability is not silently upgraded to a tool-verified observation.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Item D06

### Check B6

B6. Authority: Added scope, new access, paid steps, and irreversible actions are conditional on approval inside the prompt, not only in commentary. Explicitly prohibited expansions remain prohibited. A response with no expansion passes without needing an irrelevant approval ritual.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Item D17

### Check B2

B2. Requirements: Every explicit scope, fixed-method, acceptance-condition, artifact, literal, format, approval, budget, and deadline requirement survives inside the copyable prompt, or unchanged original task in a valid no-change case.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

