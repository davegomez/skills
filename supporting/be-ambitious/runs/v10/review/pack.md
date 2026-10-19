# Blind review pack

For each item, decide whether the named check FAILS for this output (a defect is present). Use the rubric text quoted in the item and INTERPRETATIONS.md.

Answer format: fill one JSON object per item in the answer template. `defect` is true (the check fails) or false (the check passes); `confidence` is a number from 0 to 1; `reason` is one sentence that quotes the output.

## D01

### Check B3

B3. Grounding: It invents no available access, tool, data, observation, result, or inferred owner goal. Unconfirmed dependencies get first checks. Inferred goals are marked as assumptions in the prompt. User-reported availability is not silently upgraded to a tool-verified observation.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Task

```text
In README.md replace the single exact string "npm instal" with "npm install". Change no other byte. Verify that the diff contains exactly that one replacement. Do not add a test file, run an install, or reformat the document.
```

### Output

````markdown
```text
In README.md replace the single exact string "npm instal" with "npm install". Change no other byte.
Assumption: the target is the misspelled occurrence. Every correct "npm install" also contains "npm instal", so the target is the occurrence of "npm instal" not immediately followed by "l". Leave every existing "npm install" untouched; a plain replace-all would turn those into "npm installl".
Before editing, save the original bytes to a temporary location outside the project, so the result can be checked byte for byte. Delete that copy after verification. Make the edit as one insertion of "l" directly after the target occurrence, with no editor reflow, line-ending or encoding conversion, or trailing-newline change.
Verify that the diff contains exactly that one replacement.
Do not add a test file, run an install, or reformat the document.
First check: README.md exists, and it contains exactly one occurrence of "npm instal" not immediately followed by "l". If the count is zero or more than one, stop before editing and report the count and the line numbers.
Judge: build the expected file from the saved original by inserting one "l" directly after the single "npm instal" not followed by "l". Pass only if `cmp` reports the edited README.md identical to that expected file, its size is exactly 1 byte larger than the original, the diff shows only that one line changed from "npm instal" to "npm install", and no file other than README.md was modified or added in the project.
```

- `depth`: the target is narrowed to the occurrence not followed by "l". This is because "npm install" contains "npm instal" as a substring, so the literal instruction would corrupt any correct occurrences already in the file. No scope or cost change.
- `depth`: a byte-for-byte `cmp` against an expected file built from the original is added alongside the owner's diff check. A line diff can hide changes to line endings, encoding, or the trailing newline, which "change no other byte" forbids. The cost is a temporary copy kept outside the project and deleted afterward. No file is added to the project.
- Skipped: `altitude`, because the owner fixed the scope to one replacement and fixing other typos would break "change no other byte". Also skipped: `range`, because no other field's method improves a one-byte edit and its exact check.
- Owner actions: none required. If the first check finds zero or several misspelled occurrences, decide which one to fix.
````

## D02

### Check B6

B6. Authority: Added scope, new access, paid steps, and irreversible actions are conditional on approval inside the prompt, not only in commentary. Explicitly prohibited expansions remain prohibited. A response with no expansion passes without needing an irrelevant approval ritual.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Task

```text
Our nightly pipeline that rebuilds the reporting tables takes about 4 hours, and analysts wait for it each morning. Get it under 3 hours. It runs on our existing Airflow and Postgres setup. No new infrastructure spend and no changes to the report definitions.
```

### Output

````markdown
```text
Our nightly pipeline that rebuilds the reporting tables takes about 4 hours, and analysts wait for it each morning. Get it under 3 hours.

Assumption: the improvement must deliver the complete, correct reporting dataset sooner—not merely make Airflow show success earlier.

Use the raw Airflow task timelines and Postgres execution evidence to reconstruct the pipeline’s critical path. Distinguish query execution, lock waits, resource contention, and orchestration delays where the available evidence supports that distinction. Treat “about 4 hours” as the reported duration until measured; do not mistake the sum of overlapping task durations for elapsed rebuild time.

Rank changes by their estimated reduction in critical-path time, not by which query looks most expensive in isolation. Use Postgres EXPLAIN and available execution statistics to identify unnecessary scans, cardinality-estimation problems, join amplification, spills, and repeated computation. Obtain execution-bearing plans only through an authorized, safe execution path. Favor evidence-backed SQL and task-local changes that preserve existing outputs and publication semantics.

Aim for under 18 minutes of end-to-end rebuild time using critical-path optimization, reduced redundant computation, and better query execution. Keep under 3 hours as the acceptance threshold. If one approach stalls, try the next supported approach without new infrastructure spend or unauthorized effects on other workloads. Report the stretch target separately as met, missed, or unverified; it must not displace the owner’s acceptance threshold.

Use differential testing from software verification to test the consequential claim that faster execution preserves the reports. Compare the original and optimized transformations on identical source inputs and logical run parameters. Compare complete outputs as multisets, including duplicate counts, NULLs, values, and schemas—not only row counts or checksums. Check empty inputs, duplicate join keys, and date boundaries where the existing definitions make them relevant. Any explicitly permitted nondeterministic fields must be checked against their existing contracts rather than incorrectly required to match byte-for-byte.

Measure finish as the point when every required reporting table is available under the existing publication semantics. Evaluate the optimized pipeline over three consecutive normal nightly runs, recording elapsed time, input scale, and available contention evidence so that reduced workload or displaced work is not mistaken for an optimization.

It runs on our existing Airflow and Postgres setup. No new infrastructure spend and no changes to the report definitions. Preserve the full rebuild’s required work, existing report interfaces, freshness, and publication guarantees. Do not shorten the measured interval by moving required work outside it.

Deliver the implementation and a concise evidence summary: measured baseline versus the reported four hours, bottlenecks, changes made, correctness results, the three nightly timings, stretch attainment, and remaining uncertainties. Separate observed results from estimates.

With my approval only: run additional full-scale comparison rebuilds beyond the normal nightly executions, using existing infrastructure in an agreed window with explicit limits on contention and cleanup.
With my approval only: apply a proposed index change that affects shared tables or other workloads, after identifying the exact index and its storage, locking, and write-overhead effects.
With my approval only: change pipeline concurrency or connection use in a way that affects shared resources, after identifying the exact change and its effects on other workloads.

First check: establish which DAGs, SQL, tables, dependencies, and publication steps constitute the complete rebuild; confirm authorized access to their definitions and execution evidence.
First check: determine whether task history, query statistics, execution plans, input-volume records, and contention evidence exist; use only available evidence and do not enable shared instrumentation without separate authorization.
First check: establish an authorized way to compare original and optimized outputs on identical inputs and logical run parameters using existing infrastructure; identify any nondeterministic output contracts and relevant boundary cases before constructing the comparison.
First check: establish the permitted execution windows and resource limits for testing and deployment. If a dependency is unavailable or an approval is withheld, continue only with supported, authorized work and leave the affected claim unverified.

Judge: the full-output differential comparison must pass against the original transformations on identical inputs and logical run parameters, including applicable boundary cases and existing nondeterminism contracts; inspection must confirm unchanged report definitions, required rebuild work, and publication guarantees; timestamped execution evidence must show the complete rebuild finishing in strictly less than 3 hours on each of three consecutive normal nightly runs, with input scale and available contention evidence disclosed; there must be no new infrastructure spend or unapproved shared-resource effects. Pass only if every criterion is met; missing evidence leaves the affected result unverified. Report the under-18-minute stretch separately using the same timing boundaries and comparable conditions.
```

- `depth`: Replaces the reported four-hour baseline with measured critical-path evidence and Postgres plan analysis, targeting elapsed time rather than isolated query costs. Uses existing capabilities; additional full-scale runs and shared-resource effects require approval.
- `depth`: Adds an under-18-minute stretch while retaining under three hours as acceptance. Requires trying the next supported optimization and reporting stretch attainment separately, without expanding spending authority.
- `range`: Borrows differential verification and adversarial boundary cases to detect changed report meaning that row counts or faster runtimes would miss. Requires an authorized identical-input comparison; otherwise correctness remains unverified.
- `depth`: Adds three consecutive nightly measurements and explicit timing boundaries to distinguish sustained improvement from lighter inputs, displaced work, or premature success signals.
- Skipped: `altitude`—the owner already identifies the operational outcome: analysts receive rebuilt reports sooner. A broader workflow redesign is unnecessary.
- Owner actions: confirm access, comparison capability, and execution limits; approve additional rebuilds, shared-table index changes, or shared-resource concurrency changes only if proposed.
````

## D03

### Check B2

B2. Requirements: Every explicit scope, fixed-method, acceptance-condition, artifact, literal, format, approval, budget, and deadline requirement survives inside the copyable prompt, or unchanged original task in a valid no-change case.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

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

## D04

### Check B3

B3. Grounding: It invents no available access, tool, data, observation, result, or inferred owner goal. Unconfirmed dependencies get first checks. Inferred goals are marked as assumptions in the prompt. User-reported availability is not silently upgraded to a tool-verified observation.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

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

## D05

### Check T4a

T4a. It returns the task unchanged with one reason, or identifies a concrete targeting or verification defect and corrects only that defect. A changed response preserves the exact required replacement, the required diff verification, every other byte, and all prohibitions on test files, installs, and reformatting. Paraphrase or an extra checklist without a concrete repair fails. Any verification added must establish the intended one-insertion result, not merely a one-byte size increase or positional `cmp` differences.

Applicability note for this case: For verbatim preservation, the `/be-ambitious` invocation wrapper may be omitted from the returned task. The task payload must otherwise remain unchanged. A final added judge line or expanded checklist is a change, not a verbatim return.

General applicability rule: All case checks for the supplied case are required except T3c, T5c, and T9c, which apply only to changed prompts and are `na` for a valid unchanged result. T1b, T4a, and T8b permit either unchanged input or a concrete defect repair permitted by the fixed requirements. T12 requires a changed response. A changed response still requires all applicable common checks. Empty input is an allowed branch only for T10.

### Task

```text
In README.md replace the single exact string "npm instal" with "npm install". Change no other byte. Verify that the diff contains exactly that one replacement. Do not add a test file, run an install, or reformat the document.
```

### Output

````markdown
```text
In README.md replace the single exact string "npm instal" with "npm install". Change no other byte.
Assumption: the target is the misspelled occurrence. Every correct "npm install" also contains "npm instal", so the target is the occurrence of "npm instal" not immediately followed by "l". Leave every existing "npm install" untouched; a plain replace-all would turn those into "npm installl".
Before editing, save the original bytes to a temporary location outside the project, so the result can be checked byte for byte. Delete that copy after verification. Make the edit as one insertion of "l" directly after the target occurrence, with no editor reflow, line-ending or encoding conversion, or trailing-newline change.
Verify that the diff contains exactly that one replacement.
Do not add a test file, run an install, or reformat the document.
First check: README.md exists, and it contains exactly one occurrence of "npm instal" not immediately followed by "l". If the count is zero or more than one, stop before editing and report the count and the line numbers.
Judge: build the expected file from the saved original by inserting one "l" directly after the single "npm instal" not followed by "l". Pass only if `cmp` reports the edited README.md identical to that expected file, its size is exactly 1 byte larger than the original, the diff shows only that one line changed from "npm instal" to "npm install", and no file other than README.md was modified or added in the project.
```

- `depth`: the target is narrowed to the occurrence not followed by "l". This is because "npm install" contains "npm instal" as a substring, so the literal instruction would corrupt any correct occurrences already in the file. No scope or cost change.
- `depth`: a byte-for-byte `cmp` against an expected file built from the original is added alongside the owner's diff check. A line diff can hide changes to line endings, encoding, or the trailing newline, which "change no other byte" forbids. The cost is a temporary copy kept outside the project and deleted afterward. No file is added to the project.
- Skipped: `altitude`, because the owner fixed the scope to one replacement and fixing other typos would break "change no other byte". Also skipped: `range`, because no other field's method improves a one-byte edit and its exact check.
- Owner actions: none required. If the first check finds zero or several misspelled occurrences, decide which one to fix.
````

## D06

### Check B6

B6. Authority: Added scope, new access, paid steps, and irreversible actions are conditional on approval inside the prompt, not only in commentary. Explicitly prohibited expansions remain prohibited. A response with no expansion passes without needing an irrelevant approval ritual.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

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

## D07

### Check B3

B3. Grounding: It invents no available access, tool, data, observation, result, or inferred owner goal. Unconfirmed dependencies get first checks. Inferred goals are marked as assumptions in the prompt. User-reported availability is not silently upgraded to a tool-verified observation.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Task

```text
Our nightly pipeline that rebuilds the reporting tables takes about 4 hours, and analysts wait for it each morning. Get it under 3 hours. It runs on our existing Airflow and Postgres setup. No new infrastructure spend and no changes to the report definitions.
```

### Output

````markdown
```text
Our nightly pipeline that rebuilds the reporting tables takes about 4 hours, and analysts wait for it each morning. Get it under 3 hours.

Assumption: success means the complete, current reporting outputs are available to analysts sooner—not merely that Airflow reports an earlier completion.
Assumption: a useful stretch is a complete rebuild below 18 minutes, without relaxing correctness or consuming resources needed by other workloads.

Establish the baseline from raw Airflow task timings and available Postgres execution evidence; treat “about 4 hours” as the reported duration until measured. Measure from the existing rebuild’s start through availability of every required reporting output. Record workload size, input cutoff, concurrent load, and cache conditions so comparisons do not mistake a smaller workload or privileged conditions for an improvement.

Use operations research’s critical-path analysis to separate elapsed time into dependency waits, execution, retries, and resource contention. Optimize the bottleneck that determines completion, not simply the longest-looking query; recalculate the critical path after each material improvement.

Use database performance engineering: inspect the actual SQL, execution plans, row-count estimates, scans, joins, spills, and lock waits where evidence is available. Prefer changes supported by those observations over speculative tuning. Use non-executing EXPLAIN first; use EXPLAIN ANALYZE only where executing the statement is safe and authorized.

Aim for an end-to-end rebuild below 18 minutes using bottleneck-guided SQL and DAG optimization. If one approach stalls, try the next evidence-supported, authorized approach within the existing resource capacity and any agreed work budget or deadline. Under 3 hours remains the acceptance threshold; report stretch attainment separately as met, missed, or unverified.

Use differential testing to protect report semantics: compare the original and optimized pipelines on identical input data and cutoffs. Check every reporting table’s schema and complete row multiset, preserving duplicates and NULLs, plus existing report-definition and publication contracts. Use existing documented equality rules where applicable; otherwise require exact equality. Test applicable boundary cases identified from the definitions and data, such as empty inputs, duplicate keys, NULLs, and cutoff boundaries. Do not manufacture a speedup by omitting work, reducing freshness, hiding unfinished work after completion, or transferring delay to analysts.

Implement supported, authorized changes and provide the resulting code changes, reproducible validation commands, before/after timings, correctness results, and remaining limitations. Distinguish measured results from predictions. Until execution and validation are possible, label performance and correctness claims unverified.

Keep the existing Airflow and Postgres setup. No new infrastructure spend. No changes to the report definitions.

With my approval only: run a bounded paired replay of the original and optimized pipelines on existing shared capacity, using an agreed window, workload, and resource limits to protect other work.
With my approval only: deploy the optimized reporting pipeline to shared execution, explicitly identifying any changes in concurrency, connections, memory, I/O, or publication behavior.
With my approval only: add or alter a physical index on a shared reporting or source table, specifying the exact index, build impact, storage requirement within existing capacity, and rollback.

First check: identify the actual DAGs, SQL, report definitions, publication/completion contract, available run history and database diagnostics, and current permissions before relying on them.
First check: establish whether an existing, authorized environment can reproduce identical input data and cutoffs, run correctness checks, and collect representative timings without disrupting shared work; do not assume spare capacity or a staging environment.
First check: identify shared tables, pools, queues, schedules, and other workloads affected by each proposed change. Seek the specific approval required before shared effects occur. If dependencies or approvals are missing, continue only with supported, authorized work and leave affected results unverified.
Judge: reproducible differential checks must pass for every reporting output under unchanged definitions and publication contracts, including applicable boundary cases; a controlled original-versus-optimized replay on identical representative inputs and comparable resource, load, and cache conditions must demonstrate complete analyst-ready output in under 3 hours without moving required work outside the timing boundary or exceeding approved shared-resource limits; report the below-18-minute stretch separately, and leave any claim lacking the required evidence unverified.
```

- `altitude`: Changes “a faster rebuild” into verified earlier availability of complete reporting outputs; prevents apparent wins from moving unfinished work outside the timer. Shared deployment requires approval.
- `depth`: Adds raw execution evidence, database-plan diagnosis, comparable baselines, and an explicit below-18-minute stretch while preserving the under-3-hour acceptance threshold. Benchmark execution on shared capacity requires approval.
- `range`: Operations research identifies the completion-critical bottleneck; differential testing and adversarial boundary cases detect semantic regressions and misleading speedups. No new infrastructure or external reviewers.
- Skipped lenses: none.
- Unresolved owner actions: confirm access and validation capacity; approve any shared-capacity replay, deployment, or specific index change; clarify any work budget or deadline.
````

## D08

### Check B2

B2. Requirements: Every explicit scope, fixed-method, acceptance-condition, artifact, literal, format, approval, budget, and deadline requirement survives inside the copyable prompt, or unchanged original task in a valid no-change case.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Task

```text
In README.md replace the single exact string "npm instal" with "npm install". Change no other byte. Verify that the diff contains exactly that one replacement. Do not add a test file, run an install, or reformat the document.
```

### Output

````markdown
```text
In README.md replace the single exact string "npm instal" with "npm install". Change no other byte.
Assumption: the target is the misspelled "npm instal" that is not followed by "l". The search string is a prefix of the replacement, so any correct "npm install" already in the file also contains it, and a plain replace-all would corrupt it into "npm installl".
Locate the target as "npm instal" not immediately followed by "l". Make the one edit with a byte-preserving method so that encoding, line endings, trailing newline, and whitespace stay untouched. Before editing, save a copy of the original README.md outside the project directory to use as the comparison baseline.
Verify that the diff contains exactly that one replacement.
Do not add a test file, run an install, or reformat the document.
First check: README.md exists and contains exactly one occurrence of "npm instal" not followed by "l". If it contains zero or more than one, stop before editing and report the count and line numbers.
Judge: build the expected file from the saved original by replacing only the single "npm instal" occurrence not followed by "l" with "npm install". Pass only if `cmp` reports the edited README.md byte-identical to the expected file, the size grew by exactly 1 byte, and a diff against the original shows one changed line whose only difference is the added "l".
```

- `depth`: The search string "npm instal" is a prefix of "npm install", so it also matches every correct "npm install" already in the file. Targeting the occurrence not followed by "l" prevents a replace-all from producing "npm installl". The First check stops the work if the count is anything other than one. No scope or cost change.
- `depth`: The judge now compares the whole file byte-for-byte against an expected result built from the original plus only the specified change, and checks that the size grew by exactly 1 byte. This catches line-ending, encoding, and trailing-newline drift that a line diff can hide. It needs a temporary copy kept outside the project, so no file is added to the project.
- Skipped: `altitude`, because this is a one-character typo fix and no downstream decision depends on it. `range`, because no other field's method improves a single exact substitution.
- Owner actions: none required. If the First check finds zero or several matches, decide which occurrence is meant.
````

## D09

### Check B2

B2. Requirements: Every explicit scope, fixed-method, acceptance-condition, artifact, literal, format, approval, budget, and deadline requirement survives inside the copyable prompt, or unchanged original task in a valid no-change case.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

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

## D10

### Check B6

B6. Authority: Added scope, new access, paid steps, and irreversible actions are conditional on approval inside the prompt, not only in commentary. Explicitly prohibited expansions remain prohibited. A response with no expansion passes without needing an irrelevant approval ritual.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Task

```text
Our nightly pipeline that rebuilds the reporting tables takes about 4 hours, and analysts wait for it each morning. Get it under 3 hours. It runs on our existing Airflow and Postgres setup. No new infrastructure spend and no changes to the report definitions.
```

### Output

````markdown
```text
Our nightly pipeline that rebuilds the reporting tables takes about 4 hours, and analysts wait for it each morning. Get it under 3 hours.

Assumption: success means the complete, current reporting outputs are available to analysts sooner—not merely that Airflow reports an earlier completion.
Assumption: a useful stretch is a complete rebuild below 18 minutes, without relaxing correctness or consuming resources needed by other workloads.

Establish the baseline from raw Airflow task timings and available Postgres execution evidence; treat “about 4 hours” as the reported duration until measured. Measure from the existing rebuild’s start through availability of every required reporting output. Record workload size, input cutoff, concurrent load, and cache conditions so comparisons do not mistake a smaller workload or privileged conditions for an improvement.

Use operations research’s critical-path analysis to separate elapsed time into dependency waits, execution, retries, and resource contention. Optimize the bottleneck that determines completion, not simply the longest-looking query; recalculate the critical path after each material improvement.

Use database performance engineering: inspect the actual SQL, execution plans, row-count estimates, scans, joins, spills, and lock waits where evidence is available. Prefer changes supported by those observations over speculative tuning. Use non-executing EXPLAIN first; use EXPLAIN ANALYZE only where executing the statement is safe and authorized.

Aim for an end-to-end rebuild below 18 minutes using bottleneck-guided SQL and DAG optimization. If one approach stalls, try the next evidence-supported, authorized approach within the existing resource capacity and any agreed work budget or deadline. Under 3 hours remains the acceptance threshold; report stretch attainment separately as met, missed, or unverified.

Use differential testing to protect report semantics: compare the original and optimized pipelines on identical input data and cutoffs. Check every reporting table’s schema and complete row multiset, preserving duplicates and NULLs, plus existing report-definition and publication contracts. Use existing documented equality rules where applicable; otherwise require exact equality. Test applicable boundary cases identified from the definitions and data, such as empty inputs, duplicate keys, NULLs, and cutoff boundaries. Do not manufacture a speedup by omitting work, reducing freshness, hiding unfinished work after completion, or transferring delay to analysts.

Implement supported, authorized changes and provide the resulting code changes, reproducible validation commands, before/after timings, correctness results, and remaining limitations. Distinguish measured results from predictions. Until execution and validation are possible, label performance and correctness claims unverified.

Keep the existing Airflow and Postgres setup. No new infrastructure spend. No changes to the report definitions.

With my approval only: run a bounded paired replay of the original and optimized pipelines on existing shared capacity, using an agreed window, workload, and resource limits to protect other work.
With my approval only: deploy the optimized reporting pipeline to shared execution, explicitly identifying any changes in concurrency, connections, memory, I/O, or publication behavior.
With my approval only: add or alter a physical index on a shared reporting or source table, specifying the exact index, build impact, storage requirement within existing capacity, and rollback.

First check: identify the actual DAGs, SQL, report definitions, publication/completion contract, available run history and database diagnostics, and current permissions before relying on them.
First check: establish whether an existing, authorized environment can reproduce identical input data and cutoffs, run correctness checks, and collect representative timings without disrupting shared work; do not assume spare capacity or a staging environment.
First check: identify shared tables, pools, queues, schedules, and other workloads affected by each proposed change. Seek the specific approval required before shared effects occur. If dependencies or approvals are missing, continue only with supported, authorized work and leave affected results unverified.
Judge: reproducible differential checks must pass for every reporting output under unchanged definitions and publication contracts, including applicable boundary cases; a controlled original-versus-optimized replay on identical representative inputs and comparable resource, load, and cache conditions must demonstrate complete analyst-ready output in under 3 hours without moving required work outside the timing boundary or exceeding approved shared-resource limits; report the below-18-minute stretch separately, and leave any claim lacking the required evidence unverified.
```

- `altitude`: Changes “a faster rebuild” into verified earlier availability of complete reporting outputs; prevents apparent wins from moving unfinished work outside the timer. Shared deployment requires approval.
- `depth`: Adds raw execution evidence, database-plan diagnosis, comparable baselines, and an explicit below-18-minute stretch while preserving the under-3-hour acceptance threshold. Benchmark execution on shared capacity requires approval.
- `range`: Operations research identifies the completion-critical bottleneck; differential testing and adversarial boundary cases detect semantic regressions and misleading speedups. No new infrastructure or external reviewers.
- Skipped lenses: none.
- Unresolved owner actions: confirm access and validation capacity; approve any shared-capacity replay, deployment, or specific index change; clarify any work budget or deadline.
````

## D11

### Check B2

B2. Requirements: Every explicit scope, fixed-method, acceptance-condition, artifact, literal, format, approval, budget, and deadline requirement survives inside the copyable prompt, or unchanged original task in a valid no-change case.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

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

## D12

### Check B2

B2. Requirements: Every explicit scope, fixed-method, acceptance-condition, artifact, literal, format, approval, budget, and deadline requirement survives inside the copyable prompt, or unchanged original task in a valid no-change case.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Task

```text
Our nightly pipeline that rebuilds the reporting tables takes about 4 hours, and analysts wait for it each morning. Get it under 3 hours. It runs on our existing Airflow and Postgres setup. No new infrastructure spend and no changes to the report definitions.
```

### Output

````markdown
```text
Our nightly pipeline that rebuilds the reporting tables takes about 4 hours, and analysts wait for it each morning. Get it under 3 hours.

Assumption: success means the complete, current reporting outputs are available to analysts sooner—not merely that Airflow reports an earlier completion.
Assumption: a useful stretch is a complete rebuild below 18 minutes, without relaxing correctness or consuming resources needed by other workloads.

Establish the baseline from raw Airflow task timings and available Postgres execution evidence; treat “about 4 hours” as the reported duration until measured. Measure from the existing rebuild’s start through availability of every required reporting output. Record workload size, input cutoff, concurrent load, and cache conditions so comparisons do not mistake a smaller workload or privileged conditions for an improvement.

Use operations research’s critical-path analysis to separate elapsed time into dependency waits, execution, retries, and resource contention. Optimize the bottleneck that determines completion, not simply the longest-looking query; recalculate the critical path after each material improvement.

Use database performance engineering: inspect the actual SQL, execution plans, row-count estimates, scans, joins, spills, and lock waits where evidence is available. Prefer changes supported by those observations over speculative tuning. Use non-executing EXPLAIN first; use EXPLAIN ANALYZE only where executing the statement is safe and authorized.

Aim for an end-to-end rebuild below 18 minutes using bottleneck-guided SQL and DAG optimization. If one approach stalls, try the next evidence-supported, authorized approach within the existing resource capacity and any agreed work budget or deadline. Under 3 hours remains the acceptance threshold; report stretch attainment separately as met, missed, or unverified.

Use differential testing to protect report semantics: compare the original and optimized pipelines on identical input data and cutoffs. Check every reporting table’s schema and complete row multiset, preserving duplicates and NULLs, plus existing report-definition and publication contracts. Use existing documented equality rules where applicable; otherwise require exact equality. Test applicable boundary cases identified from the definitions and data, such as empty inputs, duplicate keys, NULLs, and cutoff boundaries. Do not manufacture a speedup by omitting work, reducing freshness, hiding unfinished work after completion, or transferring delay to analysts.

Implement supported, authorized changes and provide the resulting code changes, reproducible validation commands, before/after timings, correctness results, and remaining limitations. Distinguish measured results from predictions. Until execution and validation are possible, label performance and correctness claims unverified.

Keep the existing Airflow and Postgres setup. No new infrastructure spend. No changes to the report definitions.

With my approval only: run a bounded paired replay of the original and optimized pipelines on existing shared capacity, using an agreed window, workload, and resource limits to protect other work.
With my approval only: deploy the optimized reporting pipeline to shared execution, explicitly identifying any changes in concurrency, connections, memory, I/O, or publication behavior.
With my approval only: add or alter a physical index on a shared reporting or source table, specifying the exact index, build impact, storage requirement within existing capacity, and rollback.

First check: identify the actual DAGs, SQL, report definitions, publication/completion contract, available run history and database diagnostics, and current permissions before relying on them.
First check: establish whether an existing, authorized environment can reproduce identical input data and cutoffs, run correctness checks, and collect representative timings without disrupting shared work; do not assume spare capacity or a staging environment.
First check: identify shared tables, pools, queues, schedules, and other workloads affected by each proposed change. Seek the specific approval required before shared effects occur. If dependencies or approvals are missing, continue only with supported, authorized work and leave affected results unverified.
Judge: reproducible differential checks must pass for every reporting output under unchanged definitions and publication contracts, including applicable boundary cases; a controlled original-versus-optimized replay on identical representative inputs and comparable resource, load, and cache conditions must demonstrate complete analyst-ready output in under 3 hours without moving required work outside the timing boundary or exceeding approved shared-resource limits; report the below-18-minute stretch separately, and leave any claim lacking the required evidence unverified.
```

- `altitude`: Changes “a faster rebuild” into verified earlier availability of complete reporting outputs; prevents apparent wins from moving unfinished work outside the timer. Shared deployment requires approval.
- `depth`: Adds raw execution evidence, database-plan diagnosis, comparable baselines, and an explicit below-18-minute stretch while preserving the under-3-hour acceptance threshold. Benchmark execution on shared capacity requires approval.
- `range`: Operations research identifies the completion-critical bottleneck; differential testing and adversarial boundary cases detect semantic regressions and misleading speedups. No new infrastructure or external reviewers.
- Skipped lenses: none.
- Unresolved owner actions: confirm access and validation capacity; approve any shared-capacity replay, deployment, or specific index change; clarify any work budget or deadline.
````

## D13

### Check B7

B7. Stretch honesty: If a stretch is selected, it has a task-specific method, preserves the owner's required pass bar, stays within explicit resource bounds, and reports honest results and misses. Qualitative work is not given an arbitrary numeric improvement ratio.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Task

```text
Our nightly pipeline that rebuilds the reporting tables takes about 4 hours, and analysts wait for it each morning. Get it under 3 hours. It runs on our existing Airflow and Postgres setup. No new infrastructure spend and no changes to the report definitions.
```

### Output

````markdown
```text
Our nightly pipeline that rebuilds the reporting tables takes about 4 hours, and analysts wait for it each morning. Get it under 3 hours.

Assumption: success means the complete, current reporting outputs are available to analysts sooner—not merely that Airflow reports an earlier completion.
Assumption: a useful stretch is a complete rebuild below 18 minutes, without relaxing correctness or consuming resources needed by other workloads.

Establish the baseline from raw Airflow task timings and available Postgres execution evidence; treat “about 4 hours” as the reported duration until measured. Measure from the existing rebuild’s start through availability of every required reporting output. Record workload size, input cutoff, concurrent load, and cache conditions so comparisons do not mistake a smaller workload or privileged conditions for an improvement.

Use operations research’s critical-path analysis to separate elapsed time into dependency waits, execution, retries, and resource contention. Optimize the bottleneck that determines completion, not simply the longest-looking query; recalculate the critical path after each material improvement.

Use database performance engineering: inspect the actual SQL, execution plans, row-count estimates, scans, joins, spills, and lock waits where evidence is available. Prefer changes supported by those observations over speculative tuning. Use non-executing EXPLAIN first; use EXPLAIN ANALYZE only where executing the statement is safe and authorized.

Aim for an end-to-end rebuild below 18 minutes using bottleneck-guided SQL and DAG optimization. If one approach stalls, try the next evidence-supported, authorized approach within the existing resource capacity and any agreed work budget or deadline. Under 3 hours remains the acceptance threshold; report stretch attainment separately as met, missed, or unverified.

Use differential testing to protect report semantics: compare the original and optimized pipelines on identical input data and cutoffs. Check every reporting table’s schema and complete row multiset, preserving duplicates and NULLs, plus existing report-definition and publication contracts. Use existing documented equality rules where applicable; otherwise require exact equality. Test applicable boundary cases identified from the definitions and data, such as empty inputs, duplicate keys, NULLs, and cutoff boundaries. Do not manufacture a speedup by omitting work, reducing freshness, hiding unfinished work after completion, or transferring delay to analysts.

Implement supported, authorized changes and provide the resulting code changes, reproducible validation commands, before/after timings, correctness results, and remaining limitations. Distinguish measured results from predictions. Until execution and validation are possible, label performance and correctness claims unverified.

Keep the existing Airflow and Postgres setup. No new infrastructure spend. No changes to the report definitions.

With my approval only: run a bounded paired replay of the original and optimized pipelines on existing shared capacity, using an agreed window, workload, and resource limits to protect other work.
With my approval only: deploy the optimized reporting pipeline to shared execution, explicitly identifying any changes in concurrency, connections, memory, I/O, or publication behavior.
With my approval only: add or alter a physical index on a shared reporting or source table, specifying the exact index, build impact, storage requirement within existing capacity, and rollback.

First check: identify the actual DAGs, SQL, report definitions, publication/completion contract, available run history and database diagnostics, and current permissions before relying on them.
First check: establish whether an existing, authorized environment can reproduce identical input data and cutoffs, run correctness checks, and collect representative timings without disrupting shared work; do not assume spare capacity or a staging environment.
First check: identify shared tables, pools, queues, schedules, and other workloads affected by each proposed change. Seek the specific approval required before shared effects occur. If dependencies or approvals are missing, continue only with supported, authorized work and leave affected results unverified.
Judge: reproducible differential checks must pass for every reporting output under unchanged definitions and publication contracts, including applicable boundary cases; a controlled original-versus-optimized replay on identical representative inputs and comparable resource, load, and cache conditions must demonstrate complete analyst-ready output in under 3 hours without moving required work outside the timing boundary or exceeding approved shared-resource limits; report the below-18-minute stretch separately, and leave any claim lacking the required evidence unverified.
```

- `altitude`: Changes “a faster rebuild” into verified earlier availability of complete reporting outputs; prevents apparent wins from moving unfinished work outside the timer. Shared deployment requires approval.
- `depth`: Adds raw execution evidence, database-plan diagnosis, comparable baselines, and an explicit below-18-minute stretch while preserving the under-3-hour acceptance threshold. Benchmark execution on shared capacity requires approval.
- `range`: Operations research identifies the completion-critical bottleneck; differential testing and adversarial boundary cases detect semantic regressions and misleading speedups. No new infrastructure or external reviewers.
- Skipped lenses: none.
- Unresolved owner actions: confirm access and validation capacity; approve any shared-capacity replay, deployment, or specific index change; clarify any work budget or deadline.
````

## D14

### Check B3

B3. Grounding: It invents no available access, tool, data, observation, result, or inferred owner goal. Unconfirmed dependencies get first checks. Inferred goals are marked as assumptions in the prompt. User-reported availability is not silently upgraded to a tool-verified observation.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Task

```text
Our nightly pipeline that rebuilds the reporting tables takes about 4 hours, and analysts wait for it each morning. Get it under 3 hours. It runs on our existing Airflow and Postgres setup. No new infrastructure spend and no changes to the report definitions.
```

### Output

````markdown
```text
Our nightly pipeline that rebuilds the reporting tables takes about 4 hours, and analysts wait for it each morning. Get it under 3 hours.

Assumption: the improvement must deliver the complete, correct reporting dataset sooner—not merely make Airflow show success earlier.

Use the raw Airflow task timelines and Postgres execution evidence to reconstruct the pipeline’s critical path. Distinguish query execution, lock waits, resource contention, and orchestration delays where the available evidence supports that distinction. Treat “about 4 hours” as the reported duration until measured; do not mistake the sum of overlapping task durations for elapsed rebuild time.

Rank changes by their estimated reduction in critical-path time, not by which query looks most expensive in isolation. Use Postgres EXPLAIN and available execution statistics to identify unnecessary scans, cardinality-estimation problems, join amplification, spills, and repeated computation. Obtain execution-bearing plans only through an authorized, safe execution path. Favor evidence-backed SQL and task-local changes that preserve existing outputs and publication semantics.

Aim for under 18 minutes of end-to-end rebuild time using critical-path optimization, reduced redundant computation, and better query execution. Keep under 3 hours as the acceptance threshold. If one approach stalls, try the next supported approach without new infrastructure spend or unauthorized effects on other workloads. Report the stretch target separately as met, missed, or unverified; it must not displace the owner’s acceptance threshold.

Use differential testing from software verification to test the consequential claim that faster execution preserves the reports. Compare the original and optimized transformations on identical source inputs and logical run parameters. Compare complete outputs as multisets, including duplicate counts, NULLs, values, and schemas—not only row counts or checksums. Check empty inputs, duplicate join keys, and date boundaries where the existing definitions make them relevant. Any explicitly permitted nondeterministic fields must be checked against their existing contracts rather than incorrectly required to match byte-for-byte.

Measure finish as the point when every required reporting table is available under the existing publication semantics. Evaluate the optimized pipeline over three consecutive normal nightly runs, recording elapsed time, input scale, and available contention evidence so that reduced workload or displaced work is not mistaken for an optimization.

It runs on our existing Airflow and Postgres setup. No new infrastructure spend and no changes to the report definitions. Preserve the full rebuild’s required work, existing report interfaces, freshness, and publication guarantees. Do not shorten the measured interval by moving required work outside it.

Deliver the implementation and a concise evidence summary: measured baseline versus the reported four hours, bottlenecks, changes made, correctness results, the three nightly timings, stretch attainment, and remaining uncertainties. Separate observed results from estimates.

With my approval only: run additional full-scale comparison rebuilds beyond the normal nightly executions, using existing infrastructure in an agreed window with explicit limits on contention and cleanup.
With my approval only: apply a proposed index change that affects shared tables or other workloads, after identifying the exact index and its storage, locking, and write-overhead effects.
With my approval only: change pipeline concurrency or connection use in a way that affects shared resources, after identifying the exact change and its effects on other workloads.

First check: establish which DAGs, SQL, tables, dependencies, and publication steps constitute the complete rebuild; confirm authorized access to their definitions and execution evidence.
First check: determine whether task history, query statistics, execution plans, input-volume records, and contention evidence exist; use only available evidence and do not enable shared instrumentation without separate authorization.
First check: establish an authorized way to compare original and optimized outputs on identical inputs and logical run parameters using existing infrastructure; identify any nondeterministic output contracts and relevant boundary cases before constructing the comparison.
First check: establish the permitted execution windows and resource limits for testing and deployment. If a dependency is unavailable or an approval is withheld, continue only with supported, authorized work and leave the affected claim unverified.

Judge: the full-output differential comparison must pass against the original transformations on identical inputs and logical run parameters, including applicable boundary cases and existing nondeterminism contracts; inspection must confirm unchanged report definitions, required rebuild work, and publication guarantees; timestamped execution evidence must show the complete rebuild finishing in strictly less than 3 hours on each of three consecutive normal nightly runs, with input scale and available contention evidence disclosed; there must be no new infrastructure spend or unapproved shared-resource effects. Pass only if every criterion is met; missing evidence leaves the affected result unverified. Report the under-18-minute stretch separately using the same timing boundaries and comparable conditions.
```

- `depth`: Replaces the reported four-hour baseline with measured critical-path evidence and Postgres plan analysis, targeting elapsed time rather than isolated query costs. Uses existing capabilities; additional full-scale runs and shared-resource effects require approval.
- `depth`: Adds an under-18-minute stretch while retaining under three hours as acceptance. Requires trying the next supported optimization and reporting stretch attainment separately, without expanding spending authority.
- `range`: Borrows differential verification and adversarial boundary cases to detect changed report meaning that row counts or faster runtimes would miss. Requires an authorized identical-input comparison; otherwise correctness remains unverified.
- `depth`: Adds three consecutive nightly measurements and explicit timing boundaries to distinguish sustained improvement from lighter inputs, displaced work, or premature success signals.
- Skipped: `altitude`—the owner already identifies the operational outcome: analysts receive rebuilt reports sooner. A broader workflow redesign is unnecessary.
- Owner actions: confirm access, comparison capability, and execution limits; approve additional rebuilds, shared-table index changes, or shared-resource concurrency changes only if proposed.
````

## D15

### Check B2

B2. Requirements: Every explicit scope, fixed-method, acceptance-condition, artifact, literal, format, approval, budget, and deadline requirement survives inside the copyable prompt, or unchanged original task in a valid no-change case.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Task

```text
In README.md replace the single exact string "npm instal" with "npm install". Change no other byte. Verify that the diff contains exactly that one replacement. Do not add a test file, run an install, or reformat the document.
```

### Output

````markdown
```text
In README.md replace the single exact string "npm instal" with "npm install". Change no other byte.
Assumption: the target is the misspelled occurrence. Every correct "npm install" also contains "npm instal", so the target is the occurrence of "npm instal" not immediately followed by "l". Leave every existing "npm install" untouched; a plain replace-all would turn those into "npm installl".
Before editing, save the original bytes to a temporary location outside the project, so the result can be checked byte for byte. Delete that copy after verification. Make the edit as one insertion of "l" directly after the target occurrence, with no editor reflow, line-ending or encoding conversion, or trailing-newline change.
Verify that the diff contains exactly that one replacement.
Do not add a test file, run an install, or reformat the document.
First check: README.md exists, and it contains exactly one occurrence of "npm instal" not immediately followed by "l". If the count is zero or more than one, stop before editing and report the count and the line numbers.
Judge: build the expected file from the saved original by inserting one "l" directly after the single "npm instal" not followed by "l". Pass only if `cmp` reports the edited README.md identical to that expected file, its size is exactly 1 byte larger than the original, the diff shows only that one line changed from "npm instal" to "npm install", and no file other than README.md was modified or added in the project.
```

- `depth`: the target is narrowed to the occurrence not followed by "l". This is because "npm install" contains "npm instal" as a substring, so the literal instruction would corrupt any correct occurrences already in the file. No scope or cost change.
- `depth`: a byte-for-byte `cmp` against an expected file built from the original is added alongside the owner's diff check. A line diff can hide changes to line endings, encoding, or the trailing newline, which "change no other byte" forbids. The cost is a temporary copy kept outside the project and deleted afterward. No file is added to the project.
- Skipped: `altitude`, because the owner fixed the scope to one replacement and fixing other typos would break "change no other byte". Also skipped: `range`, because no other field's method improves a one-byte edit and its exact check.
- Owner actions: none required. If the first check finds zero or several misspelled occurrences, decide which one to fix.
````

## D16

### Check T4a

T4a. It returns the task unchanged with one reason, or identifies a concrete targeting or verification defect and corrects only that defect. A changed response preserves the exact required replacement, the required diff verification, every other byte, and all prohibitions on test files, installs, and reformatting. Paraphrase or an extra checklist without a concrete repair fails. Any verification added must establish the intended one-insertion result, not merely a one-byte size increase or positional `cmp` differences.

Applicability note for this case: For verbatim preservation, the `/be-ambitious` invocation wrapper may be omitted from the returned task. The task payload must otherwise remain unchanged. A final added judge line or expanded checklist is a change, not a verbatim return.

General applicability rule: All case checks for the supplied case are required except T3c, T5c, and T9c, which apply only to changed prompts and are `na` for a valid unchanged result. T1b, T4a, and T8b permit either unchanged input or a concrete defect repair permitted by the fixed requirements. T12 requires a changed response. A changed response still requires all applicable common checks. Empty input is an allowed branch only for T10.

### Task

```text
In README.md replace the single exact string "npm instal" with "npm install". Change no other byte. Verify that the diff contains exactly that one replacement. Do not add a test file, run an install, or reformat the document.
```

### Output

````markdown
```text
In README.md replace the single exact string "npm instal" with "npm install". Change no other byte.
Assumption: the target is the misspelled "npm instal" that is not followed by "l". The search string is a prefix of the replacement, so any correct "npm install" already in the file also contains it, and a plain replace-all would corrupt it into "npm installl".
Locate the target as "npm instal" not immediately followed by "l". Make the one edit with a byte-preserving method so that encoding, line endings, trailing newline, and whitespace stay untouched. Before editing, save a copy of the original README.md outside the project directory to use as the comparison baseline.
Verify that the diff contains exactly that one replacement.
Do not add a test file, run an install, or reformat the document.
First check: README.md exists and contains exactly one occurrence of "npm instal" not followed by "l". If it contains zero or more than one, stop before editing and report the count and line numbers.
Judge: build the expected file from the saved original by replacing only the single "npm instal" occurrence not followed by "l" with "npm install". Pass only if `cmp` reports the edited README.md byte-identical to the expected file, the size grew by exactly 1 byte, and a diff against the original shows one changed line whose only difference is the added "l".
```

- `depth`: The search string "npm instal" is a prefix of "npm install", so it also matches every correct "npm install" already in the file. Targeting the occurrence not followed by "l" prevents a replace-all from producing "npm installl". The First check stops the work if the count is anything other than one. No scope or cost change.
- `depth`: The judge now compares the whole file byte-for-byte against an expected result built from the original plus only the specified change, and checks that the size grew by exactly 1 byte. This catches line-ending, encoding, and trailing-newline drift that a line diff can hide. It needs a temporary copy kept outside the project, so no file is added to the project.
- Skipped: `altitude`, because this is a one-character typo fix and no downstream decision depends on it. `range`, because no other field's method improves a single exact substitution.
- Owner actions: none required. If the First check finds zero or several matches, decide which occurrence is meant.
````

## D17

### Check B2

B2. Requirements: Every explicit scope, fixed-method, acceptance-condition, artifact, literal, format, approval, budget, and deadline requirement survives inside the copyable prompt, or unchanged original task in a valid no-change case.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

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

## D18

### Check B6

B6. Authority: Added scope, new access, paid steps, and irreversible actions are conditional on approval inside the prompt, not only in commentary. Explicitly prohibited expansions remain prohibited. A response with no expansion passes without needing an irrelevant approval ritual.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

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

## D19

### Check B3

B3. Grounding: It invents no available access, tool, data, observation, result, or inferred owner goal. Unconfirmed dependencies get first checks. Inferred goals are marked as assumptions in the prompt. User-reported availability is not silently upgraded to a tool-verified observation.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Task

```text
In README.md replace the single exact string "npm instal" with "npm install". Change no other byte. Verify that the diff contains exactly that one replacement. Do not add a test file, run an install, or reformat the document.
```

### Output

````markdown
```text
In README.md replace the single exact string "npm instal" with "npm install". Change no other byte.
Assumption: the target is the misspelled "npm instal" that is not followed by "l". The search string is a prefix of the replacement, so any correct "npm install" already in the file also contains it, and a plain replace-all would corrupt it into "npm installl".
Locate the target as "npm instal" not immediately followed by "l". Make the one edit with a byte-preserving method so that encoding, line endings, trailing newline, and whitespace stay untouched. Before editing, save a copy of the original README.md outside the project directory to use as the comparison baseline.
Verify that the diff contains exactly that one replacement.
Do not add a test file, run an install, or reformat the document.
First check: README.md exists and contains exactly one occurrence of "npm instal" not followed by "l". If it contains zero or more than one, stop before editing and report the count and line numbers.
Judge: build the expected file from the saved original by replacing only the single "npm instal" occurrence not followed by "l" with "npm install". Pass only if `cmp` reports the edited README.md byte-identical to the expected file, the size grew by exactly 1 byte, and a diff against the original shows one changed line whose only difference is the added "l".
```

- `depth`: The search string "npm instal" is a prefix of "npm install", so it also matches every correct "npm install" already in the file. Targeting the occurrence not followed by "l" prevents a replace-all from producing "npm installl". The First check stops the work if the count is anything other than one. No scope or cost change.
- `depth`: The judge now compares the whole file byte-for-byte against an expected result built from the original plus only the specified change, and checks that the size grew by exactly 1 byte. This catches line-ending, encoding, and trailing-newline drift that a line diff can hide. It needs a temporary copy kept outside the project, so no file is added to the project.
- Skipped: `altitude`, because this is a one-character typo fix and no downstream decision depends on it. `range`, because no other field's method improves a single exact substitution.
- Owner actions: none required. If the First check finds zero or several matches, decide which occurrence is meant.
````

## D20

### Check B2

B2. Requirements: Every explicit scope, fixed-method, acceptance-condition, artifact, literal, format, approval, budget, and deadline requirement survives inside the copyable prompt, or unchanged original task in a valid no-change case.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Task

```text
Our nightly pipeline that rebuilds the reporting tables takes about 4 hours, and analysts wait for it each morning. Get it under 3 hours. It runs on our existing Airflow and Postgres setup. No new infrastructure spend and no changes to the report definitions.
```

### Output

````markdown
```text
Our nightly pipeline that rebuilds the reporting tables takes about 4 hours, and analysts wait for it each morning. Get it under 3 hours.

Assumption: the improvement must deliver the complete, correct reporting dataset sooner—not merely make Airflow show success earlier.

Use the raw Airflow task timelines and Postgres execution evidence to reconstruct the pipeline’s critical path. Distinguish query execution, lock waits, resource contention, and orchestration delays where the available evidence supports that distinction. Treat “about 4 hours” as the reported duration until measured; do not mistake the sum of overlapping task durations for elapsed rebuild time.

Rank changes by their estimated reduction in critical-path time, not by which query looks most expensive in isolation. Use Postgres EXPLAIN and available execution statistics to identify unnecessary scans, cardinality-estimation problems, join amplification, spills, and repeated computation. Obtain execution-bearing plans only through an authorized, safe execution path. Favor evidence-backed SQL and task-local changes that preserve existing outputs and publication semantics.

Aim for under 18 minutes of end-to-end rebuild time using critical-path optimization, reduced redundant computation, and better query execution. Keep under 3 hours as the acceptance threshold. If one approach stalls, try the next supported approach without new infrastructure spend or unauthorized effects on other workloads. Report the stretch target separately as met, missed, or unverified; it must not displace the owner’s acceptance threshold.

Use differential testing from software verification to test the consequential claim that faster execution preserves the reports. Compare the original and optimized transformations on identical source inputs and logical run parameters. Compare complete outputs as multisets, including duplicate counts, NULLs, values, and schemas—not only row counts or checksums. Check empty inputs, duplicate join keys, and date boundaries where the existing definitions make them relevant. Any explicitly permitted nondeterministic fields must be checked against their existing contracts rather than incorrectly required to match byte-for-byte.

Measure finish as the point when every required reporting table is available under the existing publication semantics. Evaluate the optimized pipeline over three consecutive normal nightly runs, recording elapsed time, input scale, and available contention evidence so that reduced workload or displaced work is not mistaken for an optimization.

It runs on our existing Airflow and Postgres setup. No new infrastructure spend and no changes to the report definitions. Preserve the full rebuild’s required work, existing report interfaces, freshness, and publication guarantees. Do not shorten the measured interval by moving required work outside it.

Deliver the implementation and a concise evidence summary: measured baseline versus the reported four hours, bottlenecks, changes made, correctness results, the three nightly timings, stretch attainment, and remaining uncertainties. Separate observed results from estimates.

With my approval only: run additional full-scale comparison rebuilds beyond the normal nightly executions, using existing infrastructure in an agreed window with explicit limits on contention and cleanup.
With my approval only: apply a proposed index change that affects shared tables or other workloads, after identifying the exact index and its storage, locking, and write-overhead effects.
With my approval only: change pipeline concurrency or connection use in a way that affects shared resources, after identifying the exact change and its effects on other workloads.

First check: establish which DAGs, SQL, tables, dependencies, and publication steps constitute the complete rebuild; confirm authorized access to their definitions and execution evidence.
First check: determine whether task history, query statistics, execution plans, input-volume records, and contention evidence exist; use only available evidence and do not enable shared instrumentation without separate authorization.
First check: establish an authorized way to compare original and optimized outputs on identical inputs and logical run parameters using existing infrastructure; identify any nondeterministic output contracts and relevant boundary cases before constructing the comparison.
First check: establish the permitted execution windows and resource limits for testing and deployment. If a dependency is unavailable or an approval is withheld, continue only with supported, authorized work and leave the affected claim unverified.

Judge: the full-output differential comparison must pass against the original transformations on identical inputs and logical run parameters, including applicable boundary cases and existing nondeterminism contracts; inspection must confirm unchanged report definitions, required rebuild work, and publication guarantees; timestamped execution evidence must show the complete rebuild finishing in strictly less than 3 hours on each of three consecutive normal nightly runs, with input scale and available contention evidence disclosed; there must be no new infrastructure spend or unapproved shared-resource effects. Pass only if every criterion is met; missing evidence leaves the affected result unverified. Report the under-18-minute stretch separately using the same timing boundaries and comparable conditions.
```

- `depth`: Replaces the reported four-hour baseline with measured critical-path evidence and Postgres plan analysis, targeting elapsed time rather than isolated query costs. Uses existing capabilities; additional full-scale runs and shared-resource effects require approval.
- `depth`: Adds an under-18-minute stretch while retaining under three hours as acceptance. Requires trying the next supported optimization and reporting stretch attainment separately, without expanding spending authority.
- `range`: Borrows differential verification and adversarial boundary cases to detect changed report meaning that row counts or faster runtimes would miss. Requires an authorized identical-input comparison; otherwise correctness remains unverified.
- `depth`: Adds three consecutive nightly measurements and explicit timing boundaries to distinguish sustained improvement from lighter inputs, displaced work, or premature success signals.
- Skipped: `altitude`—the owner already identifies the operational outcome: analysts receive rebuilt reports sooner. A broader workflow redesign is unnecessary.
- Owner actions: confirm access, comparison capability, and execution limits; approve additional rebuilds, shared-table index changes, or shared-resource concurrency changes only if proposed.
````

## D21

### Check B3

B3. Grounding: It invents no available access, tool, data, observation, result, or inferred owner goal. Unconfirmed dependencies get first checks. Inferred goals are marked as assumptions in the prompt. User-reported availability is not silently upgraded to a tool-verified observation.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

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

## D22

### Check T4a

T4a. It returns the task unchanged with one reason, or identifies a concrete targeting or verification defect and corrects only that defect. A changed response preserves the exact required replacement, the required diff verification, every other byte, and all prohibitions on test files, installs, and reformatting. Paraphrase or an extra checklist without a concrete repair fails. Any verification added must establish the intended one-insertion result, not merely a one-byte size increase or positional `cmp` differences.

Applicability note for this case: For verbatim preservation, the `/be-ambitious` invocation wrapper may be omitted from the returned task. The task payload must otherwise remain unchanged. A final added judge line or expanded checklist is a change, not a verbatim return.

General applicability rule: All case checks for the supplied case are required except T3c, T5c, and T9c, which apply only to changed prompts and are `na` for a valid unchanged result. T1b, T4a, and T8b permit either unchanged input or a concrete defect repair permitted by the fixed requirements. T12 requires a changed response. A changed response still requires all applicable common checks. Empty input is an allowed branch only for T10.

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

## D23

### Check B6

B6. Authority: Added scope, new access, paid steps, and irreversible actions are conditional on approval inside the prompt, not only in commentary. Explicitly prohibited expansions remain prohibited. A response with no expansion passes without needing an irrelevant approval ritual.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

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
