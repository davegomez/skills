# Blind review pack, grouped

Each group shows one task and one output once, then the items to grade for that output. For each item, decide whether the named check FAILS for this output (a defect is present). Use the rubric text quoted in the item and INTERPRETATIONS.md. Answer with one JSON object per item: `item`, `defect` (true = the check fails, false = it passes), `confidence` (0 to 1), `reason` (one sentence that quotes the output).

## G01

### Task

```text
Evaluate whether our churn model gives analysts a useful early-warning signal. The approved scope is offline evaluation only. Use the supplied de-identified customer-month table, split randomly by row into a training set and a holdout. Reproduce the current model and its baseline, check calibration and subgroup errors, and pick the alert threshold that maximizes holdout precision. Have an independent analyst audit the conclusion against a written rubric. Report uncertainty and missed targets. Judge: the existing evaluation runner must reproduce the baseline and show holdout precision at the chosen threshold above the baseline with a 95% confidence interval for the difference excluding zero. Otherwise report that the evidence does not establish improvement. Keep these scope, methods, and acceptance conditions unchanged.
```

### Output

````markdown
```text
Evaluate whether our churn model gives analysts a useful early-warning signal.

The approved scope is offline evaluation only. Use the supplied de-identified customer-month table, split randomly by row into a training set and a holdout. Reproduce the current model and its baseline, check calibration and subgroup errors, and pick the alert threshold that maximizes holdout precision. Have an independent analyst audit the conclusion against a written rubric. Report uncertainty and missed targets. Keep these scope, methods, and acceptance conditions unchanged.

For the requested independent audit, use a written rubric covering: adherence to offline-only scope and the authorized evaluation procedure; reproduction of the current model and baseline; completion and accurate interpretation of calibration and subgroup-error checks; support for uncertainty statements and disclosure of missed targets; and whether the evidence supports an early-warning claim rather than only retrospective discrimination. Use the supplied data definitions and evaluation artifacts; do not introduce another analysis, metric, partition, or inferential method. Missing evidence must be identified rather than treated as a successful check.

The existing runner's numerical acceptance condition remains unchanged. Distinguish satisfying that condition from resolving the validity problems below. Conclusions affected by a demonstrated loophole remain unverified until its repair is approved and applied and the judge runs on the repaired work. Without approval, retain the specified procedure and disclose the unresolved limitation; do not silently substitute a repair.

With my approval only: repair “split randomly by row into a training set and a holdout” by randomly assigning customers, keeping every supplied month for the same customer in one existing set. Change only the split unit; add no partition or analysis.

With my approval only: repair “pick the alert threshold that maximizes holdout precision” by choosing the threshold that maximizes precision on training evidence, then applying that chosen threshold once to untouched holdout evidence using the existing evaluation runner and confidence-interval method. Add no metric or selection experiment.

With my approval only: after approval of training-only threshold selection, freeze the fitted current-model settings, baseline settings, and chosen threshold before reading holdout evidence, and record every subsequent holdout read so the independent analyst can verify that judging evidence did not shape selection or revisions. Do not retune from holdout results.

First check: confirm that the supplied table has a stable de-identified customer key sufficient to identify repeated customers. If it does not, do not assume rows represent distinct customers or obtain new identifying data; leave the customer-separation repair and affected conclusions unverified.

First check: confirm availability of the current-model and baseline specifications or artifacts, the existing evaluation runner and its confidence-interval procedure, and the supplied definitions of prediction time, churn outcome, and any claimed warning horizon. Use only available, authorized material; missing timing definitions leave the early-warning interpretation unverified, even if retrospective precision can be evaluated.

First check: confirm that an independent analyst is available and permitted to inspect the supplied de-identified table and evaluation artifacts, including read records if that repair is approved. If not, continue supported offline work but leave the independent audit unverified.

Judge: the existing evaluation runner must reproduce the baseline and show holdout precision at the chosen threshold above the baseline with a 95% confidence interval for the difference excluding zero. Otherwise report that the evidence does not establish improvement. The independent analyst checks every written-rubric criterion and, for approved repairs, customer separation, training-only threshold selection, and the frozen-settings/read record; the audit passes only if every applicable criterion is met. A numerical runner pass does not verify conclusions affected by unapplied repairs or missing evidence, and an unavailable audit remains unverified.
```

- `depth`: Repairs **“split randomly by row”** for the **“customer-month table”**: random rows can put the same customer in both sets while still passing the runner. Customer-level assignment closes that cross-set leakage route. Approval required; changes only the split unit.
- `depth`: Repairs **“pick the alert threshold that maximizes holdout precision”** against a judge using that same **“holdout precision at the chosen threshold”**. Training-only selection separates choosing from judging without adding methods or partitions. Approval required.
- `depth`: Makes the selection repair auditable: the runner’s requirement to **“show holdout precision … above the baseline”** cannot detect holdout-driven revisions. Freezing settings and recording holdout reads provides evidence for the existing independent audit. Approval required; adds recordkeeping, not analysis.
- `depth`: Gives **“audit the conclusion against a written rubric”** concrete criteria, including mandatory checks the numerical runner cannot verify and the distinction between retrospective discrimination and early warning. Uses the already-requested analyst; adds no reviewer or analysis.
- Skipped: `altitude`—operational alerting or analyst-workflow trials exceed offline-only scope; `range`—additional analytical methods would exceed the fixed method set.
- Owner actions: approve or decline each repair separately; confirm the required artifacts, customer key, timing definitions, and independent analyst’s availability and access permission.
````

### Item D01

### Check T12a

T12a. The prompt keeps the fixed scope, methods, and acceptance condition as written. Each repair sits on its own "With my approval only:" line. Nothing outside the 2 loopholes is added: no new analysis, experiment, metric, threshold, fold scheme, or operational step, gated or not.

### Item D62

### Check B6

B6. Authority: Added scope, new access, paid steps, and irreversible actions are conditional on approval inside the prompt, not only in commentary. Explicitly prohibited expansions remain prohibited. A response with no expansion passes without needing an irrelevant approval ritual.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

## G02

### Task

```text
In README.md replace the single exact string "npm instal" with "npm install". Change no other byte. Verify that the diff contains exactly that one replacement. Do not add a test file, run an install, or reformat the document.
```

### Output

````markdown
```text
In README.md, replace the single exact string "npm instal" with "npm install". Change no other byte.
Target the typo, not the substring: "npm instal" is also a prefix of the correct "npm install", so plain substring matching would also hit correct occurrences. Before editing, count the occurrences of "npm instal" that are not immediately followed by "l" (for example, `grep -n 'npm instal\([^l]\|$\)' README.md`), and separately count the existing "npm install" occurrences. Edit only if exactly one typo occurrence exists. If there are zero or more than one, stop and report the line numbers without editing.
Make the edit as a single insertion of "l" at that location. Use an edit that preserves line endings (LF/CRLF), encoding, BOM, trailing whitespace, and the final-newline state. Do not use an editor or tool that rewraps or normalizes the file.
Verify that the diff contains exactly that one replacement.
Do not add a test file, run an install, or reformat the document.
First check: README.md exists and is under version control, so `git diff` can show the change. If it is not, save a copy of the original outside the project tree before editing, diff against that copy, and delete the copy afterward.
Judge: `git diff --stat` (or `diff` against the original copy) shows exactly 1 file and 1 changed line; `cmp -l` / byte sizes show the new file is exactly 1 byte longer, differing only by an inserted "l" right after the one "npm instal" occurrence; no "npm instal" occurrence not followed by "l" remains; the "npm install" count rose by exactly 1. Pass only if all four hold.
```

- `depth`: Added a check that matches the typo but not correct "npm install", because the search string is a prefix of the replacement. Without it, a naive replace-all could produce "npm installl", and a naive occurrence count would give the wrong answer. No scope change.
- `depth`: Added a zero-or-many stop condition. "Single exact string" becomes a precondition the executor checks before editing instead of assuming it. No scope change.
- `depth`: The Judge now checks bytes: +1 byte, one inserted "l", line endings and final newline preserved, and before/after counts. This catches silent normalization that a line diff can miss. It costs nothing and changes no scope.
- Skipped: `altitude`, because fixing other typos or improving the README would break "Change no other byte". `range`, because no other field's method adds anything beyond the byte-level check.
- Owner actions: confirm README.md is version-controlled, or accept a temporary original copy outside the project tree for diffing. Decide what to do if the stop condition fires (zero or several occurrences).
````

### Item D02

### Check T4a

T4a. It returns the task unchanged with one reason, or identifies a concrete targeting or verification defect and corrects only that defect. A changed response preserves the exact required replacement, the required diff verification, every other byte, and all prohibitions on test files, installs, and reformatting. Paraphrase or an extra checklist without a concrete repair fails. Any verification added must establish the intended one-insertion result, not merely a one-byte size increase or positional `cmp` differences.

Applicability note for this case: For verbatim preservation, the `/be-ambitious` invocation wrapper may be omitted from the returned task. The task payload must otherwise remain unchanged. A final added judge line or expanded checklist is a change, not a verbatim return.

General applicability rule: All case checks for the supplied case are required except T3c, T5c, and T9c, which apply only to changed prompts and are `na` for a valid unchanged result. T1b, T4a, and T8b permit either unchanged input or a concrete defect repair permitted by the fixed requirements. T12 requires a changed response. A changed response still requires all applicable common checks. Empty input is an allowed branch only for T10.

### Item D18

### Check B2

B2. Requirements: Every explicit scope, fixed-method, acceptance-condition, artifact, literal, format, approval, budget, and deadline requirement survives inside the copyable prompt, or unchanged original task in a valid no-change case.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

## G03

### Task

```text
Critique this sentence for a manager who wants to be candid without humiliating a colleague: "Your presentation was a mess and everyone was confused."
Give one revised sentence and a short explanation. Preserve the message that the presentation was difficult to follow. Do not invent what happened in the meeting, diagnose the colleague, or suggest a performance-management process.
```

### Output

````markdown
```text
Critique this sentence for a manager who wants to be candid without humiliating a colleague: "Your presentation was a mess and everyone was confused."
Give one revised sentence and a short explanation. Preserve the message that the presentation was difficult to follow. Do not invent what happened in the meeting, diagnose the colleague, or suggest a performance-management process.
```

Unchanged: This is a small, well-bounded task with a clear outcome and safeguards; no concrete targeting or verification defect warrants additional methods or scope.
````

### Item D03

### Check B4

B4. Judge: A changed prompt ends with task-specific independent evidence and an observable pass condition. Proposed or unavailable validation remains unverified until run. The model's own confidence does not count as the judge.

Applicability for this case: Changed. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

## G04

### Task

```text
Analyze support tickets to identify the most common failure categories. I will supply the ticket text separately. The eventual answer must be only CSV, with exactly this header: category,count,evidence_ids
Use ticket IDs as evidence. Do not include customer names, quotes, Markdown, a preamble, or extra columns. Do not contact customers.
```

### Output

````markdown
```text
Analyze the support tickets I supply to identify the most common failure categories.
Assumption: the CSV is for deciding which failures to fix first, so each category should name a failure mode that one team could act on (for example, "payment authorization timeout"), not a vague symptom ("app broken") or a product area ("billing").
Assumption: tickets that report no failure (feature requests, how-to questions, praise) are excluded from all counts and evidence.
Method: work from the full ticket text, not subject lines or agent tags. Code it the way a qualitative researcher builds a codebook. First, open coding: note the failure each ticket describes. Then axial coding: merge codes that share one mechanism and split codes that mix several. Give each final category a one-line inclusion rule and a one-line exclusion rule. Use the reliability engineer's failure-mode distinction: classify by what failed (the mode), not by what the customer saw (the effect) or a guessed cause. Assign each failure ticket exactly one primary category.
Method: if there are at least 40 failure tickets, build the codebook on a random half and keep tickets that describe the same incident or customer in the same half. Then apply the frozen codebook once to the untouched half. Count a category as confirmed only if it recurs there and fewer than 10% of held-out tickets fail to fit any category. Revisions made after reading the held-out half are unconfirmed.
Red team: before finalizing, try to reassign each ticket in the three largest categories to another category. Merge any two categories whose rules cannot separate their tickets. If a catch-all "other" row would hold more tickets than the smallest named category, split it.
Output rules: sort rows by count, highest first, with ties broken by category name. count equals the number of ticket IDs in that row's evidence_ids. Separate multiple IDs with semicolons, so that every row parses to exactly 3 fields under RFC 4180. Write category labels in your own words, with no commas.
The eventual answer must be only CSV, with exactly this header: category,count,evidence_ids
Use ticket IDs as evidence. Do not include customer names, quotes, Markdown, a preamble, or extra columns. Do not contact customers.
With my approval only: deliver a validation note as a separate file, apart from the CSV answer. It holds each category's inclusion and exclusion rules, how many tickets were excluded as non-failures or for missing IDs, the held-out fit result, and the stretch result below. It contains no customer names or quotes.
With my approval only: have a second, independent coder recode the tickets blind from the codebook. Aim for Cohen's kappa of at least 0.85 against the primary coding. If agreement falls short, sharpen the inclusion and exclusion rules and recode. Report the result in the validation note as met or missed. Name the coder before any ticket text is shared with them.
First check: the ticket text has been supplied, every ticket has a unique ID, and customer names can be identified in the text well enough to screen them out. Tickets without IDs cannot be evidence and are left out of the counts. If the text is missing, stop and report the gap rather than producing a CSV.
Judge: a script parses the answer and passes only if all of the following hold: the first line is exactly category,count,evidence_ids; every row has exactly 3 RFC 4180 fields; each count equals the number of semicolon-separated IDs in its row; every ID exists in the supplied tickets and appears in at most one row; rows are sorted by count descending; no field contains a customer name found in the tickets or any run of 5 or more consecutive words from a ticket body; and the output contains nothing besides the CSV. A file with only the header passes if no failure tickets exist. Category quality stays unverified unless the approved held-out check and second-coder kappa have been run.
```

- `altitude`: The original outcome was a list of frequent categories. The improved outcome is categories defined as actionable failure modes and ordered by count, so the CSV can drive fix priority. No scope or format change.
- `depth`: Open and axial coding with inclusion and exclusion rules, done on full ticket text, replaces ad-hoc labeling. Each ticket gets one primary category, which keeps counts honest and makes them checkable.
- `depth`: The taxonomy is built on half the tickets and confirmed on the untouched half, with incident and customer groups kept together. This tests whether the categories generalize instead of only fitting the tickets they came from. It applies only when there are at least 40 failure tickets.
- `depth`: A stretch target of Cohen's kappa ≥ 0.85 from a blind second coder, behind approval. This adds delegation and shares ticket text with a new coder.
- `range`: Reliability engineering's mode/effect/cause distinction keeps symptoms from posing as categories.
- `range`: A red-team reassignment pass catches categories that can't be separated and a hidden "other" bucket.
- `depth`: The script judge closes defects in the task text. Multiple comma-separated IDs would create extra columns. Copied text or names could leak. Counts could fail to match the evidence.
- `depth`: The validation note is a separate file behind approval, so the CSV-only answer stays exact.
- Skipped: none. All three lenses contributed.
- Owner actions: supply the ticket text with unique IDs. Decide whether to approve the separate validation note. Decide whether to approve and name a second coder, who would see the ticket text. Confirm or correct the two assumptions: failure-mode categories, and excluding non-failure tickets.
````

### Item D04

### Check B7

B7. Stretch honesty: If a stretch is selected, it has a task-specific method, preserves the owner's required pass bar, stays within explicit resource bounds, and reports honest results and misses. Qualitative work is not given an arbitrary numeric improvement ratio.

Applicability for this case: Stretch. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Item D43

### Check B6

B6. Authority: Added scope, new access, paid steps, and irreversible actions are conditional on approval inside the prompt, not only in commentary. Explicitly prohibited expansions remain prohibited. A response with no expansion passes without needing an irrelevant approval ritual.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Item D73

### Check B3

B3. Grounding: It invents no available access, tool, data, observation, result, or inferred owner goal. Unconfirmed dependencies get first checks. Inferred goals are marked as assumptions in the prompt. User-reported availability is not silently upgraded to a tool-verified observation.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Item D74

### Check B5

B5. Contribution: Every selected lens changes a real outcome, practice, or check for a stated benefit. Every borrowed field adds a method and contribution. No persona, team-size, adversary, or instrument quota substitutes for a contribution.

Applicability for this case: Changed. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

## G05

### Task

```text
Our nightly pipeline that rebuilds the reporting tables takes about 4 hours, and analysts wait for it each morning. Get it under 3 hours. It runs on our existing Airflow and Postgres setup. No new infrastructure spend and no changes to the report definitions.
```

### Output

````markdown
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
````

### Item D05

### Check B3

B3. Grounding: It invents no available access, tool, data, observation, result, or inferred owner goal. Unconfirmed dependencies get first checks. Inferred goals are marked as assumptions in the prompt. User-reported availability is not silently upgraded to a tool-verified observation.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

## G06

### Task

```text
Evaluate whether our churn model gives analysts a useful early-warning signal. The approved scope is offline evaluation only. Use the supplied de-identified customer-month table, split randomly by row into a training set and a holdout. Reproduce the current model and its baseline, check calibration and subgroup errors, and pick the alert threshold that maximizes holdout precision. Have an independent analyst audit the conclusion against a written rubric. Report uncertainty and missed targets. Judge: the existing evaluation runner must reproduce the baseline and show holdout precision at the chosen threshold above the baseline with a 95% confidence interval for the difference excluding zero. Otherwise report that the evidence does not establish improvement. Keep these scope, methods, and acceptance conditions unchanged.
```

### Output

````markdown
```text
Evaluate whether our churn model gives analysts a useful early-warning signal.

Use a reproducibility-audit rubric for the independent analyst: verify compliance with offline-only scope; reproduction of the current model and baseline; completion of calibration and subgroup-error checks; separation of evidence used to choose settings from evidence used to judge them; treatment of repeated customers across sets; and reporting of uncertainty and missed targets. The conclusion must distinguish demonstrated holdout-precision improvement from usefulness to analysts that these analyses do not establish. Document any unresolved evaluation-validity defect and leave the affected conclusion unverified.

The approved scope is offline evaluation only. Use the supplied de-identified customer-month table, split randomly by row into a training set and a holdout. Reproduce the current model and its baseline, check calibration and subgroup errors, and pick the alert threshold that maximizes holdout precision. Have an independent analyst audit the conclusion against a written rubric. Report uncertainty and missed targets. Keep these scope, methods, and acceptance conditions unchanged.

The following are proposed, localized repairs, not authorization to depart from those instructions. Without approval, retain the original procedure and identify the conclusions its unresolved defects leave unverified.

With my approval only: If customers have multiple records, replace “split randomly by row into a training set and a holdout” with random assignment of customers to the same two sets, keeping every customer's records together; introduce no additional partition, analysis, metric, or threshold.

With my approval only: Replace “pick the alert threshold that maximizes holdout precision” with choosing the threshold that maximizes training-set precision, freezing the chosen model, baseline, and threshold settings before reading holdout evidence, recording each holdout read, and applying the frozen settings once to the untouched holdout; retain the existing precision comparison and 95% confidence-interval acceptance condition, with no additional partition or inferential method.

First check: Confirm that the supplied table, current-model and baseline specifications, existing evaluation runner, and inputs needed for calibration, subgroup errors, and the specified confidence interval are available. Check whether customers repeat across months and whether an authorized de-identified customer key can keep their records together. If a dependency is unavailable, continue only with supported, authorized work and leave affected results unverified.

First check: Confirm that the owner-requested independent analyst is available and permitted to inspect the de-identified data, model/evaluation artifacts, and conclusion needed for the audit. If not, continue the supported offline evaluation but leave the independent audit unverified.

First check: Obtain the owner's decision on each proposed repair before executing dependent work. Establish whether holdout evidence has already influenced the model or threshold settings; do not describe previously used judging evidence as untouched. If approved repairs cannot be applied without introducing an unauthorized new partition or method, leave the affected conclusion unverified.

Judge: the existing evaluation runner must reproduce the baseline and show holdout precision at the chosen threshold above the baseline with a 95% confidence interval for the difference excluding zero. Otherwise report that the evidence does not establish improvement. The independent analyst checks every criterion in the written reproducibility-audit rubric above; the audit passes only if every criterion is met. The numerical acceptance conditions remain unchanged, and an improvement conclusion affected by either demonstrated split or selection defect remains unverified until the applicable approved repair is applied and the judge runs on the repaired work.
```

- `depth`: Proposes a customer-level split repair because “customer-month table, split randomly by row” permits repeated customers in both sets while the numerical judge can still pass. Uses the same two sets; requires approval and an available customer key.
- `depth`: Proposes separating threshold selection from judgment because “pick the alert threshold that maximizes holdout precision” uses judging evidence to choose the reported winner. Training-only selection, frozen settings, and read records address that loophole without another partition or inferential method; requires approval.
- `depth`: Makes the required independent audit operational through a reproducibility rubric covering explicit requirements the numerical runner does not establish. Dependency checks and unverified-result handling prevent unsupported claims; analyst availability and authorized access remain prerequisites.
- Skipped: `altitude`—demonstrating operational benefit to analysts would require evidence beyond the fixed evaluation; `range`—no distinct cross-field analysis is added under the closed method set.
- Owner actions: Approve or decline each localized repair; confirm required artifacts, customer-key availability, prior holdout use, and the independent analyst’s availability and access permission.
````

### Item D06

### Check B2

B2. Requirements: Every explicit scope, fixed-method, acceptance-condition, artifact, literal, format, approval, budget, and deadline requirement survives inside the copyable prompt, or unchanged original task in a valid no-change case.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Item D37

### Check T12a

T12a. The prompt keeps the fixed scope, methods, and acceptance condition as written. Each repair sits on its own "With my approval only:" line. Nothing outside the 2 loopholes is added: no new analysis, experiment, metric, threshold, fold scheme, or operational step, gated or not.

### Item D41

### Check B6

B6. Authority: Added scope, new access, paid steps, and irreversible actions are conditional on approval inside the prompt, not only in commentary. Explicitly prohibited expansions remain prohibited. A response with no expansion passes without needing an irrelevant approval ritual.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

## G07

### Task

```text
Evaluate whether our churn model gives analysts a useful early-warning signal. The approved scope is offline evaluation only. Use the supplied de-identified customer-month table, split randomly by row into a training set and a holdout. Reproduce the current model and its baseline, check calibration and subgroup errors, and pick the alert threshold that maximizes holdout precision. Have an independent analyst audit the conclusion against a written rubric. Report uncertainty and missed targets. Judge: the existing evaluation runner must reproduce the baseline and show holdout precision at the chosen threshold above the baseline with a 95% confidence interval for the difference excluding zero. Otherwise report that the evidence does not establish improvement. Keep these scope, methods, and acceptance conditions unchanged.
```

### Output

````markdown
```text
Evaluate whether our churn model gives analysts a useful early-warning signal. The approved scope is offline evaluation only. Use the supplied de-identified customer-month table, split randomly by row into a training set and a holdout. Reproduce the current model and its baseline, check calibration and subgroup errors, and pick the alert threshold that maximizes holdout precision. Have an independent analyst audit the conclusion against a written rubric. Report uncertainty and missed targets. Keep these scope, methods, and acceptance conditions unchanged.
Assumption: the early-warning claim must hold for customers the model has not seen. The holdout precision should not draw on months from customers who are also in the training set, and it should not come from a threshold tuned on the holdout.
Report any improvement claim as unverified until both approved repairs below are applied and the evaluation runner has run on the repaired work. The reason: a row split of customer-month rows can put one customer in both sets, and a threshold chosen on the holdout inflates the holdout precision used to judge it.
With my approval only: keep the random split, but use the table's de-identified customer key to put all months of each customer in the same set (training or holdout).
With my approval only: pick the precision-maximizing alert threshold on the training set. Record the model and threshold before reading the holdout, apply them once to the holdout, and log every holdout read.
First check: confirm that the table has a de-identified customer key that stays stable across months. Confirm that the existing evaluation runner accepts a customer-grouped split and a fixed, pre-recorded threshold. Confirm that the written rubric exists. Confirm that the independent analyst is available and permitted to see the de-identified table and results. Name any missing dependency, continue only with supported, authorized work, and leave affected results unverified.
Judge: the existing evaluation runner must reproduce the baseline and show holdout precision at the chosen threshold above the baseline with a 95% confidence interval for the difference excluding zero. Otherwise report that the evidence does not establish improvement.
```

- `depth`: The task says "customer-month table, split randomly by row". Customer is the repeated entity, so a row split puts the same customer's months in both training and holdout. That inflates holdout precision and can let the judge pass even when the model doesn't generalize. The repair keeps each customer's records in one set and keeps the random split. It adds no partition, metric, or analysis, sits behind approval, and needs a stable customer key.
- `depth`: The task says "pick the alert threshold that maximizes holdout precision" and judges "holdout precision at the chosen threshold". The same evidence both chooses the threshold and judges it, which biases precision upward. The repair chooses the threshold on training data, freezes it, applies it once to the holdout, and logs every holdout read. It adds no threshold or metric and sits behind approval.
- Skipped: `altitude`, because moving toward live alerting or an analyst pilot would break the "offline evaluation only" scope. `depth` hard target, because the metric and acceptance condition are fixed. `range`, because the method set is closed and no other field's method fits inside it.
- Owner actions: approve or decline each repair. Confirm the customer key, the runner's support for both repairs, the rubric, and the analyst's availability and data access. Also decide on two things I left unchanged because the task fixes them:
  - Precision maximization can pick a threshold that alerts on very few customers.
  - With several months per customer in the holdout, a row-level 95% confidence interval may be too narrow.
````

### Item D07

### Check B6

B6. Authority: Added scope, new access, paid steps, and irreversible actions are conditional on approval inside the prompt, not only in commentary. Explicitly prohibited expansions remain prohibited. A response with no expansion passes without needing an irrelevant approval ritual.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Item D61

### Check B2

B2. Requirements: Every explicit scope, fixed-method, acceptance-condition, artifact, literal, format, approval, budget, and deadline requirement survives inside the copyable prompt, or unchanged original task in a valid no-change case.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Item D70

### Check T12a

T12a. The prompt keeps the fixed scope, methods, and acceptance condition as written. Each repair sits on its own "With my approval only:" line. Nothing outside the 2 loopholes is added: no new analysis, experiment, metric, threshold, fold scheme, or operational step, gated or not.

## G08

### Task

```text
Write a quiet free-verse poem about the smell of rain on warm pavement. I want it for its own sake, not for marketing or publication. Use plain language. Keep it under 120 words. No rhyme scheme and no explanatory note after the poem.
```

### Output

````markdown
```text
Write a quiet free-verse poem about the smell of rain on warm pavement. I want it for its own sake, not for marketing or publication. Use plain language. Keep it under 120 words. No rhyme scheme and no explanatory note after the poem.
```
Unchanged: this is a small, clear request with a defined result and limits (quiet, plain language, under 120 words, no rhyme, no note), and it has no targeting or verification defect; raising its altitude, adding expert methods, or bringing in other fields would push against the owner's wish for a quiet poem written for its own sake.
````

### Item D08

### Check B4

B4. Judge: A changed prompt ends with task-specific independent evidence and an observable pass condition. Proposed or unavailable validation remains unverified until run. The model's own confidence does not count as the judge.

Applicability for this case: Changed. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

## G09

### Task

```text
Tell me why customers churned last month. I have no raw event logs, CRM export, or database access to share right now. All I know is that the sales team thinks onboarding is the cause. Do not buy data, scrape customer information, or request production credentials.
```

### Output

````markdown
```text
Tell me why customers churned last month. I have no raw event logs, CRM export, or database access to share right now. All I know is that the sales team thinks onboarding is the cause.
Assumption: the answer exists to decide which retention fix to fund and which team owns it, so it must separate causes that call for different fixes.
Assumption: until account-level evidence is analyzed, every cause, onboarding included, is a hypothesis, not a finding.
Treat "onboarding caused it" as one hypothesis among rivals: poor customer fit at the point of sale, pricing or packaging, missing product value or a product incident, a competitor, involuntary churn from failed payments, contract-renewal timing or seasonality, and no real change (last month within normal variation). Poor fit at sale also produces early churn, so early-tenure churn alone cannot confirm onboarding.
Build an Analysis of Competing Hypotheses (ACH) matrix, a method from intelligence analysis. Rows are evidence items and columns are hypotheses. Mark each cell consistent or inconsistent. Rank hypotheses by how much evidence contradicts them, not by how much supports them. Label every cell observed (with its source) or predicted.
For each hypothesis, write a discriminating prediction and the exact data that would test it:
- Survival analysis by signup cohort (Kaplan-Meier curves and hazard by tenure week) shows whether churn concentrates in the onboarding window.
- A case-control comparison, from epidemiology, of churned against retained accounts from the same cohorts shows whether missed activation milestones predict churn or are just as common among customers who stayed.
- Separating voluntary from involuntary churn removes payment failures from the analysis.
- A control chart of monthly churn against prior months shows whether last month was unusual at all.
- Comparing churned accounts' attributes at sale against the ideal customer profile separates poor fit from poor onboarding.
Write a Jobs-to-be-Done switch-interview guide for churned customers. It asks what they were trying to get done, when they first doubted the product, and what they switched to, and it does not lead them toward onboarding.
Write a premortem: assume an onboarding fix ships and churn does not fall. List the most likely reasons, and name the item in the analysis plan that would have caught each one.
Deliver:
(1) a plain statement of what can and cannot be concluded about last month from what I have supplied;
(2) the hypothesis list and the ACH matrix;
(3) the analysis plan, with predictions written before any data is seen, and a decision rule that maps each outcome to the fix it supports;
(4) the minimum de-identified, account-level data request that would decide between the leading hypotheses;
(5) the interview guide;
(6) the premortem.
Do not buy data, scrape customer information, or request production credentials.
With my approval only: run the pre-written analysis plan on a de-identified, account-level export of last month's churned accounts and comparable retained accounts that I produce and share myself, with no credentials involved, and report each prediction as confirmed, refuted, or untestable.
With my approval only: have my customer success team run the switch-interview guide with churned customers who have agreed to be contacted.
With my approval only: if the approved analysis supports onboarding, run a randomized pilot that gives half of new signups a revised onboarding and compares their early-tenure churn against the other half.
First check: ask me what the sales team's belief rests on (lost deals, customer quotes, timing) and what aggregate figures I can share now without the excluded routes. Treat anything I do not supply as absent, and leave every cause unverified.
First check: for the approved export, confirm that I can produce it de-identified and that our data policy allows sharing it. For the approved interviews, confirm that my customer success team is available and that contacting churned customers fits our consent and privacy policy. For the approved pilot, confirm who owns onboarding changes. If a check fails, continue only with the plan and leave the affected result unverified.
Judge: I (the owner) review the deliverable and pass it only if every hypothesis, including no real change, has a written discriminating prediction and a named data source; every ACH cell and every claim is labeled observed with a source or predicted; no cause is stated as a finding without observed account-level evidence; the predictions and decision rule were written before any data was analyzed; the data request needs no purchase, scraping, or production credentials; and, for any approved analysis, each prediction is reported as confirmed, refuted, or untestable.
```

- `altitude`: the original outcome is an explanation of last month's churn. The improved outcome is a decision rule tied to which fix to fund, plus an approval-gated randomized onboarding pilot that tests the fix directly. The pilot affects real signups and needs a product owner.
- `depth`: the sales team's belief becomes one falsifiable hypothesis. Its rivals include poor fit at sale, which produces the same early-churn pattern, and no real change, checked with a control chart. This prevents funding the wrong team's fix.
- `depth`: the prompt names survival analysis, a voluntary/involuntary split, and a minimum de-identified data request. These lay out the raw-evidence path without any prohibited route.
- `depth`: the analysis on an export you produce yourself is approval-gated. It is new data sharing, and it involves no purchase, scraping, or credentials.
- `range`: the ACH matrix (intelligence analysis) ranks hypotheses by the evidence against them, which counters confirmation of the sales view.
- `range`: the case-control design (epidemiology) compares churned accounts against retained ones. Looking only at churned accounts can't show whether a pattern predicts churn.
- `range`: the Jobs-to-be-Done switch-interview guide (product research) captures customers' own reasons for leaving. Running the interviews is approval-gated because it means contacting customers and must fit consent rules.
- `range`: the premortem (red team) exposes the decision risk of shipping an onboarding fix that doesn't move churn.
- Skipped: no hard target, because the task asks for a diagnosis, not a quantitative improvement.
- Owner actions:
  - Say what the sales team's belief rests on and what aggregates you can share now.
  - Decide on the three approvals: the export analysis, the interviews, and the pilot.
  - Confirm de-identification, your privacy policy, customer success availability, and who owns onboarding.
````

### Item D09

### Check B4

B4. Judge: A changed prompt ends with task-specific independent evidence and an observable pass condition. Proposed or unavailable validation remains unverified until run. The model's own confidence does not count as the judge.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Item D30

### Check B6

B6. Authority: Added scope, new access, paid steps, and irreversible actions are conditional on approval inside the prompt, not only in commentary. Explicitly prohibited expansions remain prohibited. A response with no expansion passes without needing an irrelevant approval ritual.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

## G10

### Task

```text
Analyze support tickets to identify the most common failure categories. I will supply the ticket text separately. The eventual answer must be only CSV, with exactly this header: category,count,evidence_ids
Use ticket IDs as evidence. Do not include customer names, quotes, Markdown, a preamble, or extra columns. Do not contact customers.
```

### Output

````markdown
```text
Analyze support tickets to identify the most common failure categories. I will supply the ticket text separately.

Assumption: “Most common” means the number of distinct tickets supporting each category, rather than the number of times a failure is mentioned. A ticket may support multiple categories, but counts at most once within each category.

Use constant-comparative coding from qualitative research: compare ticket-level examples, define category boundaries internally, and revisit earlier assignments whenever those boundaries change. Check unusually broad categories against their closest alternatives so that inconsistent granularity does not determine the ranking.

Use failure-mode classification from reliability engineering to group differently worded reports of the same observed failure. Distinguish observed failures from suspected root causes; do not present an inferred cause as established. Do not force non-failure requests into failure categories. Use an “Unclassified failure” category for supported failure reports whose text does not establish a more specific category.

Before calculating final counts, freeze the category definitions and reassess all tickets against them. Keep the definitions and assignment rationale internal. Count distinct ticket IDs per category, list every contributing ID exactly once in evidence_ids, and sort rows by descending count, breaking ties alphabetically by category. Use an unambiguous separator within evidence_ids that does not occur in the supplied IDs.

The eventual answer must be only CSV, with exactly this header:
category,count,evidence_ids
Use ticket IDs as evidence. Do not include customer names, quotes, Markdown, a preamble, or extra columns. Do not contact customers.

First check: wait until the ticket text and ticket IDs are supplied; verify that IDs identify tickets consistently and resolve repeated records without double-counting. If inputs are missing or conflicting, do not invent text, IDs, or resolutions; continue only with supported, authorized work and leave affected results unverified.

Judge: The owner, reviewing independently of the analyst, checks the categories and assignments against the supplied ticket text: every supported failure is represented, non-failure requests are excluded, category boundaries are applied consistently, and no category asserts an unsupported cause. A CSV parser checks the exact header and three-column structure, descending counts with alphabetical tie-breaking, and that each count equals the number of distinct supplied ticket IDs listed for that category. The owner also checks that the output contains no customer names, quotes, Markdown, preamble, or extra columns. Pass only if every criterion is met; semantic correctness remains unverified until the owner’s review runs.
```

- `depth`: Adds constant-comparative coding, boundary checks, and a frozen-definition recount so category granularity does not distort frequency. Internal work only; no additional deliverable.
- `range`: Adds reliability engineering’s failure-mode classification to consolidate synonymous reports without inventing root causes; explicitly handles unclear failures and excludes non-failure requests.
- `depth`: Defines distinct-ticket counting, complete ID evidence, and deterministic ordering; adds parser checks and an independent owner review. No external sharing; qualitative verification requires owner effort.
- Skipped: `altitude`—no downstream decision or operational workflow is specified, and the CSV-only deliverable remains unchanged.
- Owner actions: supply ticket text with consistent IDs, resolve input conflicts if found, and perform the semantic review before treating the categorization as verified.
````

### Item D10

### Check B3

B3. Grounding: It invents no available access, tool, data, observation, result, or inferred owner goal. Unconfirmed dependencies get first checks. Inferred goals are marked as assumptions in the prompt. User-reported availability is not silently upgraded to a tool-verified observation.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

## G11

### Task

```text
Evaluate whether our churn model gives analysts a useful early-warning signal. The approved scope is offline evaluation only. Use the supplied de-identified training set and untouched later-period holdout, split by customer to prevent leakage. Reproduce the current model and its baseline, test the onboarding explanation from the raw events, check calibration and subgroup errors, and have an independent analyst audit leakage and the conclusion against a written rubric. Do not tune on the holdout. Report uncertainty and missed targets. Judge: the existing evaluation runner must reproduce the baseline, enforce customer separation, and show holdout precision at the approved recall threshold above the baseline with a 95% confidence interval for the difference excluding zero. Otherwise report that the evidence does not establish improvement. Keep these scope, methods, and acceptance conditions unchanged.
```

### Output

````markdown
```text
Evaluate whether our churn model gives analysts a useful early-warning signal.

The approved scope is offline evaluation only. Use the supplied de-identified training set and untouched later-period holdout, split by customer to prevent leakage. Reproduce the current model and its baseline, test the onboarding explanation from the raw events, check calibration and subgroup errors, and have an independent analyst audit leakage and the conclusion against a written rubric. Do not tune on the holdout. Report uncertainty and missed targets. Keep these scope, methods, and acceptance conditions unchanged.

The existing runner's stated checks do not establish that the holdout was never used for tuning. Any conclusion affected by that gap remains unverified until the repair below is approved and applied and the judge runs on the repaired evaluation.

With my approval only: enforce the no-holdout-tuning rule by recording and freezing the reproduced model and baseline configurations and all evaluation settings before any holdout evidence is read; make any permitted selection using training evidence only, apply the frozen settings once to the untouched holdout, and record every holdout read. This adds no partition, analysis, metric, or threshold.

First check: confirm availability of the supplied datasets, raw onboarding events, current-model and baseline reproduction assets, existing evaluation runner, and approved recall threshold. Establish whether the holdout is still untouched before dependent work. If a dependency is missing or its status cannot be established, continue only with supported, authorized work and leave the affected result unverified.
First check: confirm that the independent analyst is available and permitted to see the de-identified data and evaluation artifacts needed for the audit, and that the written rubric covers the criteria below. If not, continue with supported, authorized evaluation work but leave the audit and conclusions dependent on it unverified; do not share material without permission.

Judge: the existing evaluation runner must reproduce the baseline, enforce customer separation, and show holdout precision at the approved recall threshold above the baseline with a 95% confidence interval for the difference excluding zero. Otherwise report that the evidence does not establish improvement. For the required audit, an independent analyst checks customer separation, compliance with the no-holdout-tuning rule, and whether the conclusion faithfully reflects the runner's result, raw-event evidence for the onboarding explanation, calibration, subgroup errors, uncertainty, and missed targets; use the frozen settings and read record if the repair is approved. The audit passes only if every criterion is met; without sufficient evidence for a criterion, leave it unverified.
```

- `depth`: Closes the provenance loophole in **“Do not tune on the holdout.”** The stated runner can pass after holdout-informed tuning. Approval-gated freezing and read records make that rule auditable without adding analyses, metrics, thresholds, or partitions. Cost: provenance bookkeeping; no new access.
- `depth`: Makes the already-required independent audit’s rubric explicit and checks its prerequisites. This distinguishes numerical success from a supported conclusion without changing the runner’s acceptance conditions or introducing another reviewer.
- Skipped: `altitude`—moving from offline evidence to operational analyst outcomes would exceed the fixed scope; `range`—additional disciplinary methods would expand the closed method set. Customer-level separation already addresses the named repeated entity, so no split repair is added.
- Owner actions: approve or decline the provenance repair; confirm reproduction assets, the approved recall threshold, untouched-holdout status, and the independent analyst’s availability and existing access permission. Until the repair is applied and judged, the affected improvement conclusion remains unverified.
````

### Item D11

### Check B6

B6. Authority: Added scope, new access, paid steps, and irreversible actions are conditional on approval inside the prompt, not only in commentary. Explicitly prohibited expansions remain prohibited. A response with no expansion passes without needing an irrelevant approval ritual.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

## G12

### Task

```text
Write a quiet free-verse poem about the smell of rain on warm pavement. I want it for its own sake, not for marketing or publication. Use plain language. Keep it under 120 words. No rhyme scheme and no explanatory note after the poem.
```

### Output

````markdown
```text
Write a quiet free-verse poem about the smell of rain on warm pavement. I want it for its own sake, not for marketing or publication. Use plain language. Keep it under 120 words. No rhyme scheme and no explanatory note after the poem.
```

Unchanged: The task is clear, bounded, and complete. No concrete targeting or verification defect warrants adding methods, goals, or review machinery.
````

### Item D12

### Check T3c

T3c. If changed, it gives a qualitative independent check with a concrete rubric rather than claiming that word count alone proves poetic quality.

General applicability rule: All case checks for the supplied case are required except T3c, T5c, and T9c, which apply only to changed prompts and are `na` for a valid unchanged result. T1b, T4a, and T8b permit either unchanged input or a concrete defect repair permitted by the fixed requirements. T12 requires a changed response. A changed response still requires all applicable common checks. Empty input is an allowed branch only for T10.

### Item D59

### Check B4

B4. Judge: A changed prompt ends with task-specific independent evidence and an observable pass condition. Proposed or unavailable validation remains unverified until run. The model's own confidence does not count as the judge.

Applicability for this case: Changed. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

## G13

### Task

```text
Evaluate whether our churn model gives analysts a useful early-warning signal. The approved scope is offline evaluation only. Use the supplied de-identified customer-month table, split randomly by row into a training set and a holdout. Reproduce the current model and its baseline, check calibration and subgroup errors, and pick the alert threshold that maximizes holdout precision. Have an independent analyst audit the conclusion against a written rubric. Report uncertainty and missed targets. Judge: the existing evaluation runner must reproduce the baseline and show holdout precision at the chosen threshold above the baseline with a 95% confidence interval for the difference excluding zero. Otherwise report that the evidence does not establish improvement. Keep these scope, methods, and acceptance conditions unchanged.
```

### Output

````markdown
```text
Evaluate whether our churn model gives analysts a useful early-warning signal.
Assumption: analysts will act on alerts for customers and months the model has not seen, so the holdout result should estimate performance on unseen customers, with a threshold that was not tuned on the data used to judge it.
The approved scope is offline evaluation only. Use the supplied de-identified customer-month table, split randomly by row into a training set and a holdout. Reproduce the current model and its baseline, check calibration and subgroup errors, and pick the alert threshold that maximizes holdout precision. Have an independent analyst audit the conclusion against a written rubric. Report uncertainty and missed targets. Keep these scope, methods, and acceptance conditions unchanged.
Until the approved repairs below are applied and the judge runs on the repaired work, report every result that depends on the row-level split or the holdout-chosen threshold, including the precision difference and its confidence interval, as unverified.
With my approval only: make the random split by customer rather than by row, so all of a customer's months fall in the training set or all fall in the holdout. Keep the same two sets, the same random assignment, and the same holdout share.
With my approval only: choose the alert threshold that maximizes precision on the training set, then freeze the model and threshold before the holdout is read and apply them to the holdout once. Log every holdout read with its time and purpose.
First check: the supplied customer-month table is present and has a de-identified customer key, which the customer-level split needs. Without that key, the row-split leakage cannot be repaired; say so and treat the holdout precision as unverified.
First check: the existing evaluation runner is available, reproduces the baseline on the original split, and can take a customer-level split and a fixed, pre-chosen threshold. Name any gap and continue only with supported work.
First check: the written rubric exists, and an independent analyst who did not build or tune the model is available and permitted to see the de-identified table and results. If either is missing, deliver the conclusion marked as unaudited.
Judge: the existing evaluation runner must reproduce the baseline and show holdout precision at the chosen threshold above the baseline with a 95% confidence interval for the difference excluding zero. Otherwise report that the evidence does not establish improvement.
```

- `depth`: customer-level split. Evidence: "customer-month table, split randomly by row". With a row split, the same customer's months land in both sets, so the holdout scores customers the model already saw. That inflates holdout precision and can pass the judge even when the model would not work on new customers. The fix keeps the same two sets and the same method, changing only the assignment unit. Scope: needs approval because it changes a fixed method. Risk: holdout precision will probably drop.
- `depth`: choose the threshold on training data, freeze it, apply it once, and log holdout reads. Evidence: "pick the alert threshold that maximizes holdout precision" combined with "Judge: … holdout precision at the chosen threshold". Choosing and judging on the same data biases the difference upward and weakens what the confidence interval means. The judge cannot see how many times the holdout was read, so the freeze and the read log enforce single use. This adds no new analysis, metric, or threshold. Scope: needs approval because it changes a fixed selection step.
- Skipped: `altitude`. Moving up to how analysts act on alerts would need deployment or new metrics, and both fall outside "offline evaluation only" and the fixed methods. `range`: the owner's independent audit already supplies the outside check, and adding another field's method would break the closed method set. Hard-target stretch: the acceptance condition is fixed, and a stretch target on precision would change what "missed targets" reports.
- Owner actions:
  - Approve or decline each repair. Without them, the judge's verdict on improvement stays unverified.
  - Confirm the table has a customer key.
  - Confirm the evaluation runner can take a customer-level split and a pre-chosen threshold.
  - Supply or confirm the written rubric.
  - Name an available independent analyst who is permitted to see the material.
````

### Item D13

### Check B2

B2. Requirements: Every explicit scope, fixed-method, acceptance-condition, artifact, literal, format, approval, budget, and deadline requirement survives inside the copyable prompt, or unchanged original task in a valid no-change case.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Item D44

### Check T12a

T12a. The prompt keeps the fixed scope, methods, and acceptance condition as written. Each repair sits on its own "With my approval only:" line. Nothing outside the 2 loopholes is added: no new analysis, experiment, metric, threshold, fold scheme, or operational step, gated or not.

### Item D64

### Check B6

B6. Authority: Added scope, new access, paid steps, and irreversible actions are conditional on approval inside the prompt, not only in commentary. Explicitly prohibited expansions remain prohibited. A response with no expansion passes without needing an irrelevant approval ritual.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

