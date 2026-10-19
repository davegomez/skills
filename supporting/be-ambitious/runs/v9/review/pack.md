# Blind review pack

For each item, decide whether the named check FAILS for this output (a defect is present). Use the rubric text quoted in the item and INTERPRETATIONS.md.

Answer format: fill one JSON object per item in the answer template. `defect` is true (the check fails) or false (the check passes); `confidence` is a number from 0 to 1; `reason` is one sentence that quotes the output.

## D01

### Check T12a

T12a. The prompt keeps the fixed scope, methods, and acceptance condition as written. Each repair sits on its own "With my approval only:" line. Nothing outside the 2 loopholes is added: no new analysis, experiment, metric, threshold, fold scheme, or operational step, gated or not.

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

## D02

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

## D03

### Check B4

B4. Judge: A changed prompt ends with task-specific independent evidence and an observable pass condition. Proposed or unavailable validation remains unverified until run. The model's own confidence does not count as the judge.

Applicability for this case: Changed. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

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

## D04

### Check B7

B7. Stretch honesty: If a stretch is selected, it has a task-specific method, preserves the owner's required pass bar, stays within explicit resource bounds, and reports honest results and misses. Qualitative work is not given an arbitrary numeric improvement ratio.

Applicability for this case: Stretch. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

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

## D05

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

## D06

### Check B2

B2. Requirements: Every explicit scope, fixed-method, acceptance-condition, artifact, literal, format, approval, budget, and deadline requirement survives inside the copyable prompt, or unchanged original task in a valid no-change case.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

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

## D07

### Check B6

B6. Authority: Added scope, new access, paid steps, and irreversible actions are conditional on approval inside the prompt, not only in commentary. Explicitly prohibited expansions remain prohibited. A response with no expansion passes without needing an irrelevant approval ritual.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

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

## D08

### Check B4

B4. Judge: A changed prompt ends with task-specific independent evidence and an observable pass condition. Proposed or unavailable validation remains unverified until run. The model's own confidence does not count as the judge.

Applicability for this case: Changed. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

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

## D09

### Check B4

B4. Judge: A changed prompt ends with task-specific independent evidence and an observable pass condition. Proposed or unavailable validation remains unverified until run. The model's own confidence does not count as the judge.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

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

## D10

### Check B3

B3. Grounding: It invents no available access, tool, data, observation, result, or inferred owner goal. Unconfirmed dependencies get first checks. Inferred goals are marked as assumptions in the prompt. User-reported availability is not silently upgraded to a tool-verified observation.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

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

## D11

### Check B6

B6. Authority: Added scope, new access, paid steps, and irreversible actions are conditional on approval inside the prompt, not only in commentary. Explicitly prohibited expansions remain prohibited. A response with no expansion passes without needing an irrelevant approval ritual.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

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

## D12

### Check T3c

T3c. If changed, it gives a qualitative independent check with a concrete rubric rather than claiming that word count alone proves poetic quality.

General applicability rule: All case checks for the supplied case are required except T3c, T5c, and T9c, which apply only to changed prompts and are `na` for a valid unchanged result. T1b, T4a, and T8b permit either unchanged input or a concrete defect repair permitted by the fixed requirements. T12 requires a changed response. A changed response still requires all applicable common checks. Empty input is an allowed branch only for T10.

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

## D13

### Check B2

B2. Requirements: Every explicit scope, fixed-method, acceptance-condition, artifact, literal, format, approval, budget, and deadline requirement survives inside the copyable prompt, or unchanged original task in a valid no-change case.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

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

## D14

### Check B5

B5. Contribution: Every selected lens changes a real outcome, practice, or check for a stated benefit. Every borrowed field adds a method and contribution. No persona, team-size, adversary, or instrument quota substitutes for a contribution.

Applicability for this case: Changed. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Task

```text
Critique this sentence for a manager who wants to be candid without humiliating a colleague: "Your presentation was a mess and everyone was confused."
Give one revised sentence and a short explanation. Preserve the message that the presentation was difficult to follow. Do not invent what happened in the meeting, diagnose the colleague, or suggest a performance-management process.
```

### Output

````markdown
```text
Critique this sentence for a manager who wants to be candid without humiliating a colleague: "Your presentation was a mess and everyone was confused."
Assumption: success means the colleague clearly hears that the presentation was hard to follow and stays open to talking about it.
Separate observation from evaluation (nonviolent communication): flag words that condemn the work or person wholesale ("a mess") and words that make a sweeping claim about others ("everyone"). Keep only what the manager can stand behind from their own experience, stated about the presentation, not about the colleague.
Use politeness theory (Brown and Levinson) to name which phrase threatens the colleague's face most, and choose redress that reduces that threat without hedging away the point.
Red-team the draft twice before finalizing. First, read it as the colleague: does any word still read as contempt? Second, read it as a skeptic: has it become so soft that it no longer says the presentation was hard to follow?
Fold these findings into the short explanation; do not add other sections.
Give one revised sentence and a short explanation. Preserve the message that the presentation was difficult to follow. Do not invent what happened in the meeting, diagnose the colleague, or suggest a performance-management process.
Judge: the manager reviews the output and passes it only if all of these hold: it contains exactly one revised sentence plus a short explanation; a reader shown only the revised sentence would conclude the presentation was difficult to follow; the sentence uses no wholesale label of the work or colleague (such as "mess"); it adds no event, detail, cause, motive, or trait absent from the original; any claim about others' reactions is no stronger than the original's; and it proposes no performance-management step.
```

- `depth`: The observation-versus-evaluation split targets the two specific problems in the sentence: the wholesale verdict "a mess" and the unverifiable "everyone." The fix states the point from the manager's own experience without inventing meeting details. No scope or cost change.
- `range`: Politeness theory names the face threat and the redress, so the explanation gives a reason the manager can reuse instead of a matter of taste. No scope change.
- `range`: The two-reader red team catches both ways this can fail. One is a revision that still humiliates. The other, which is more likely, is a revision so softened that the "hard to follow" message is lost. No scope change.
- `depth`: The task had no judge. The added judge is the manager, already the owner, checking criteria taken directly from the task's own constraints. It needs no new reviewer and shares nothing.
- Skipped: `altitude`. The deliverable is fixed as one sentence plus a short explanation, so climbing to a full feedback conversation or a follow-up plan would go beyond it.
- Owner actions: none required. Run the judge on the output yourself.
````

## D15

### Check B3

B3. Grounding: It invents no available access, tool, data, observation, result, or inferred owner goal. Unconfirmed dependencies get first checks. Inferred goals are marked as assumptions in the prompt. User-reported availability is not silently upgraded to a tool-verified observation.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Task

```text
Prepare the quarterly business review deck for our leadership meeting in two weeks. We want leaders to decide whether to invest in retention or acquisition. The deck is required and must be at most 12 slides. I can provide the raw customer and revenue exports, but have not shared them yet. Use existing staff and tools. Do not change our operating cadence or contact customers.
```

### Output

````markdown
```text
Prepare the quarterly business review deck for our leadership meeting in two weeks, so leaders can decide whether to invest in retention or acquisition.
Assumption: leaders are deciding where the next increment of budget goes. The deck must compare the marginal return of one more unit of spend on each option, not average returns, and may conclude that a targeted split beats either pure choice.
Assumption: the exports cover enough quarters to build cohorts and hold out the latest quarter. If they don't, say so and mark the dependent results unverified.
Open the deck with the recommendation and the decision asked of leaders. Give each slide a title that states its conclusion, and build the supporting slides into one cause-and-effect story.
Before reading results, write the decision rule and record it, dated, in the working files. The rule states which comparison of retention and acquisition returns favors which option, over which horizon, and what margin counts as a tie. Apply it unchanged.
Work from the raw customer and revenue exports, not summary reports. Build a revenue bridge for the quarter (starting revenue, new, expansion, contraction, churn) that reconciles to the export totals. Compute gross and net revenue retention by cohort.
Use survival analysis (Kaplan-Meier retention curves by start cohort and segment) to show when and where customers churn, and whether churn is concentrated in segments that retention spend would reach.
Estimate customer lifetime value from the observed curves and margins. Where spend data is available, compute acquisition cost and payback by channel or segment, and the cost to retain an at-risk customer.
Quantify uncertainty. Bootstrap the key figures and show ranges, not points. Run a sensitivity (tornado) analysis showing which assumption, at what value, flips the recommendation, and put that flip point on a slide.
Treat churn drivers as development findings: find them on earlier quarters, then confirm them once on the most recent quarter, which stays untouched until then. Report drivers that fail confirmation as unconfirmed. Label correlations as correlations; do not claim a retention action causes retention without evidence that it does.
Red team: include one slide that makes the strongest case for the option not recommended. Add a pre-mortem naming how the recommendation could fail and the leading indicator in our existing reports that would show it failing.
State what the exports cannot answer and what data would resolve it.
The deck is required and must be at most 12 slides, appendix included.
Use existing staff and tools. Do not change our operating cadence. Do not contact customers: no surveys or interviews.
With my approval only: obtain acquisition and retention spend data (sales, marketing, and customer-success cost by quarter and, where recorded, by channel or segment) from existing finance records.
With my approval only: deliver a separate validation note that maps each figure in the deck to its source query or calculation on the exports.
First check: I have shared the raw customer and revenue exports, and they contain customer ID, start and end or cancellation dates, revenue by period, and segment. Name any missing fields and continue only with supported work.
First check: if spend data is approved, confirm it exists and the finance records are accessible. Without it, mark acquisition cost, payback, and the marginal-return comparison unverified rather than estimating them from assumptions presented as fact.
First check: a finance or analytics staff member other than the author is available to review before the meeting and is permitted to see the customer and revenue data.
Judge: an existing finance or analytics staff member other than the author recomputes every figure in the deck from the raw exports (and approved spend data) and checks that the deck has at most 12 slides; each figure matches its recomputation within rounding; the revenue bridge reconciles to export totals; the dated decision rule predates the results and was applied as written; each comparative claim is backed by computed figures with ranges or is labeled unverified with the missing data named; every churn driver presented as confirmed held up on the held-out quarter; the flip-point assumption and the case for the other option are shown; no customer was contacted and no cadence change is proposed; pass only if every criterion is met.
```

- `altitude`: The original outcome was a QBR deck. The improved outcome is a deck that drives one allocation decision, with a pre-written decision rule, a marginal-return comparison, and the assumption that would flip the answer. There is no added scope. Post-decision tracking was left out because it would change the operating cadence.
- `depth`: The deck is built from the raw exports, with a revenue bridge, cohort net and gross retention, Kaplan-Meier curves, LTV, CAC, and payback. This replaces summary figures with reconciled, segment-level evidence. Cost: analyst time from existing staff.
- `depth`: Churn drivers must be confirmed on a held-out latest quarter, and bootstrap ranges are required. This stops leaders from acting on drivers or point estimates that don't hold. Risk: short history leaves the drivers unverified.
- `depth`: The spend data needed for acquisition ROI is behind approval. Without it, the core comparison can't be computed and is marked unverified. Access effect: the executor gets finance records that were not offered.
- `range`: Decision analysis contributes the pre-written decision rule and the tornado flip point, so leaders see what they would have to believe to choose otherwise.
- `range`: Epidemiology and causal inference contribute correlation labeling and development-versus-confirmation separation. This blocks "retained customers got X, so X causes retention."
- `range`: Red team contributes the strongest-opposing-case slide and a pre-mortem tied to existing reports. This exposes decision risk without adding a cadence.
- `range`: Consulting communication (answer first, conclusion titles) fits the decision into a 12-slide leadership read.
- Skipped: the hard-target move, because this is not a quantitative improvement request. Also skipped: any customer research or new monitoring cadence, which the owner prohibited.
- Owner actions: share the exports; approve or decline access to the spend data and the separate validation note; name a finance or analytics reviewer, other than the author, who can see the data before the meeting.
````

## D16

### Check B3

B3. Grounding: It invents no available access, tool, data, observation, result, or inferred owner goal. Unconfirmed dependencies get first checks. Inferred goals are marked as assumptions in the prompt. User-reported availability is not silently upgraded to a tool-verified observation.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Task

```text
Draft a weekly report about recurring checkout failures so our team can choose what to fix. You may inspect only the redacted incident notes I provide. You may not access production, change checkout code, create accounts, send messages, or change incident-response policy. If you think we should move beyond the report, make that a separate proposal needing my approval.
```

### Output

````markdown
```text
Draft a weekly report about recurring checkout failures so our team can choose what to fix.
Assumption: the team will choose in one prioritization discussion, so the report leads with a ranked, evidence-backed shortlist of fix candidates and the open questions that could change that ranking.
Assumption: "recurring" means the same underlying cause appears in two or more incidents, not only the same symptom.

Method:
- Work from the full text of each redacted incident note, not from summaries. Give each note an ID and extract one record per note: date and time, checkout step affected (cart, address, shipping, payment, confirmation, other), symptom, stated or suspected cause, detection source (alert, customer report, staff), duration, stated customer impact, and mitigation. Mark any field the notes lack or redaction hides as "unknown". Do not infer or reconstruct redacted content.
- Build a short codebook of failure modes using thematic coding. Give each mode a definition and an inclusion/exclusion rule, and group notes by cause, not symptom. Derive the codebook from the earlier half of the notes by date, then freeze it. Apply it unchanged to the later half. Report how many later notes fit an existing mode, how many needed a new one, and which modes appear in both halves. A mode seen only in the half used to define it stays labeled "unconfirmed".
- Rank the modes with an FMEA-style table. Score occurrence (count of notes), severity (from stated duration and impact), and detection (how late, and by whom, the failure was caught), each 1–5, and show the scoring rule. A failure first caught by customers scores worse on detection than one caught by an alert.
- For each top mode, write a contributing-factor chain (5 whys, stopping where the notes stop). Name system conditions, not "human error", and list the candidate fixes the evidence supports.
- Red-team the top three modes. For each, state the strongest alternative explanation and whether the notes rule it out. Examples: the same symptom from different causes, one noisy incident counted several times, or uneven note-taking across teams.
- For each candidate fix, state which mode it targets, its expected effect, its confidence (high, medium, or low, with a reason), and the one unanswered question that would most change its rank.
- Label every claim as observed (cite note IDs or quote) or inferred.
- Report structure: a one-page summary with the ranked shortlist; the FMEA table; per-mode evidence and contributing factors; red-team results; the holdout result; data gaps; an appendix of extracted records.

Requirements:
- Inspect only the redacted incident notes I provide.
- Do not access production, change checkout code, create accounts, send messages, or change incident-response policy.
- If you think we should move beyond the report, make that a separate proposal needing my approval, and do not act on it.

With my approval only: a recurring week-over-week tracker that applies the frozen codebook to each new week's redacted notes, to show whether the chosen fixes reduce recurrence of their target modes. Present it only as the separate proposal and take no step toward setting it up.
First check: the redacted notes are provided. Record the note count, the date range, and which fields survived redaction. With fewer than 6 notes, say so, skip the date split, and label every mode "unconfirmed".
First check: a member of our team other than the report's author is available to review and is permitted to see these redacted notes. I will give them the notes and report, since you send nothing. If no such reviewer is available, deliver the report marked "unverified".
Judge: a member of our team other than the author, given the same redacted notes, checks that (1) every claim cites note IDs and is labeled observed or inferred; (2) every mode reported as recurring has at least 2 notes sharing a stated cause, not only a symptom; (3) recoding up to 10 randomly chosen notes (all if fewer) with the frozen codebook, without seeing the author's codes, matches the author's mode on at least 80% of them; (4) the shortlist order follows from the shown FMEA scores; (5) the holdout result is reported with counts, or its omission is explained by the note count; (6) no information beyond the redacted notes was used, redaction gaps are marked "unknown", and anything beyond the report appears only as a separate unexecuted proposal. Pass only if every criterion is met.
```

**Ledger**
- `altitude`: The original outcome was a report about failures. The improved outcome is a ranked fix shortlist with confidence levels and rank-changing questions, built for the team's actual choice. No scope change.
- `altitude`: The week-over-week tracker shows whether the chosen fixes worked. It sits behind approval as a separate proposal only, and it adds a recurring workflow if approved.
- `depth`: Records are extracted from raw note text, with redaction gaps marked "unknown" instead of guessed. This stops invented causes and adds no access.
- `depth`: The codebook is defined on earlier notes and confirmed on later ones. This tests whether "recurring" modes are real instead of artifacts of how they were found. With few notes, modes stay "unconfirmed".
- `range` (reliability engineering): The FMEA table ranks by occurrence, severity, and detection. It shows costly or customer-detected failures that a raw frequency count hides.
- `range` (safety science): Contributing-factor chains that exclude "human error" point fixes at system conditions instead of blame.
- `range` (decision analysis): Each fix gets a confidence label and the one question that would most change its rank. This tells the team what to find out before committing.
- `range` (red team): Alternative explanations for the top three modes expose miscounted or misattributed recurrences before the team acts on them.
- `range` (qualitative research): The reviewer blindly recodes a sample, which checks that the clusters are reproducible and not one author's reading. It needs a team reviewer's time.
- Skipped: the hard-target move, because this is not a quantitative improvement request and the report has no metric to stretch.
- Owner actions: provide the redacted notes; name a team reviewer, confirm they may see the notes, and pass them the material; decide whether to approve the tracker proposal.
````

## D17

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
````

## D18

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

## D19

### Check B4

B4. Judge: A changed prompt ends with task-specific independent evidence and an observable pass condition. Proposed or unavailable validation remains unverified until run. The model's own confidence does not count as the judge.

Applicability for this case: Changed. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Task

```text
Critique this sentence for a manager who wants to be candid without humiliating a colleague: "Your presentation was a mess and everyone was confused."
Give one revised sentence and a short explanation. Preserve the message that the presentation was difficult to follow. Do not invent what happened in the meeting, diagnose the colleague, or suggest a performance-management process.
```

### Output

````markdown
```text
Critique this sentence for a manager who wants to be candid without humiliating a colleague: "Your presentation was a mess and everyone was confused."
Assumption: success means the colleague clearly hears that the presentation was hard to follow and stays open to talking about it.
Separate observation from evaluation (nonviolent communication): flag words that condemn the work or person wholesale ("a mess") and words that make a sweeping claim about others ("everyone"). Keep only what the manager can stand behind from their own experience, stated about the presentation, not about the colleague.
Use politeness theory (Brown and Levinson) to name which phrase threatens the colleague's face most, and choose redress that reduces that threat without hedging away the point.
Red-team the draft twice before finalizing. First, read it as the colleague: does any word still read as contempt? Second, read it as a skeptic: has it become so soft that it no longer says the presentation was hard to follow?
Fold these findings into the short explanation; do not add other sections.
Give one revised sentence and a short explanation. Preserve the message that the presentation was difficult to follow. Do not invent what happened in the meeting, diagnose the colleague, or suggest a performance-management process.
Judge: the manager reviews the output and passes it only if all of these hold: it contains exactly one revised sentence plus a short explanation; a reader shown only the revised sentence would conclude the presentation was difficult to follow; the sentence uses no wholesale label of the work or colleague (such as "mess"); it adds no event, detail, cause, motive, or trait absent from the original; any claim about others' reactions is no stronger than the original's; and it proposes no performance-management step.
```

- `depth`: The observation-versus-evaluation split targets the two specific problems in the sentence: the wholesale verdict "a mess" and the unverifiable "everyone." The fix states the point from the manager's own experience without inventing meeting details. No scope or cost change.
- `range`: Politeness theory names the face threat and the redress, so the explanation gives a reason the manager can reuse instead of a matter of taste. No scope change.
- `range`: The two-reader red team catches both ways this can fail. One is a revision that still humiliates. The other, which is more likely, is a revision so softened that the "hard to follow" message is lost. No scope change.
- `depth`: The task had no judge. The added judge is the manager, already the owner, checking criteria taken directly from the task's own constraints. It needs no new reviewer and shares nothing.
- Skipped: `altitude`. The deliverable is fixed as one sentence plus a short explanation, so climbing to a full feedback conversation or a follow-up plan would go beyond it.
- Owner actions: none required. Run the judge on the output yourself.
````

## D20

### Check B6

B6. Authority: Added scope, new access, paid steps, and irreversible actions are conditional on approval inside the prompt, not only in commentary. Explicitly prohibited expansions remain prohibited. A response with no expansion passes without needing an irrelevant approval ritual.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Task

```text
Evaluate whether our churn model gives analysts a useful early-warning signal. The approved scope is offline evaluation only. Use the supplied de-identified training set and untouched later-period holdout, split by customer to prevent leakage. Reproduce the current model and its baseline, test the onboarding explanation from the raw events, check calibration and subgroup errors, and have an independent analyst audit leakage and the conclusion against a written rubric. Do not tune on the holdout. Report uncertainty and missed targets. Judge: the existing evaluation runner must reproduce the baseline, enforce customer separation, and show holdout precision at the approved recall threshold above the baseline with a 95% confidence interval for the difference excluding zero. Otherwise report that the evidence does not establish improvement. Keep these scope, methods, and acceptance conditions unchanged.
```

### Output

````markdown
```text
Evaluate whether our churn model gives analysts a useful early-warning signal. The approved scope is offline evaluation only. Use the supplied de-identified training set and untouched later-period holdout, split by customer to prevent leakage. Reproduce the current model and its baseline, test the onboarding explanation from the raw events, check calibration and subgroup errors, and have an independent analyst audit leakage and the conclusion against a written rubric. Do not tune on the holdout. Report uncertainty and missed targets. Keep these scope, methods, and acceptance conditions unchanged.
Until the freeze-and-log step below is approved and applied, and the judge has run on the result, report any improvement conclusion as unverified. The runner cannot detect whether the holdout was used for tuning.
With my approval only: before reading the holdout, freeze the model, baseline, and feature settings chosen on training evidence. Then apply them once to the holdout and record each holdout read with its time, purpose, and settings version.
First check: confirm the following before any dependent work. The existing evaluation runner is available. The approved recall threshold is documented. The later-period holdout has not been read yet. The independent analyst is available and permitted to see the de-identified data and results. Name any missing dependency, continue only with supported, authorized work, and leave each affected result unverified.
Judge: the existing evaluation runner must reproduce the baseline, enforce customer separation, and show holdout precision at the approved recall threshold above the baseline with a 95% confidence interval for the difference excluding zero. Otherwise report that the evidence does not establish improvement.
```

- `depth` (loophole repair): the task says "Do not tune on the holdout", but the judge only checks baseline reproduction, customer separation, and the CI. A model tuned on the holdout could pass undetected. Freezing settings before the first holdout read and logging each read closes this gap at its source. It adds no new analysis, metric, threshold, or partition, and there is no scope or access change. It is behind approval.
- Unverified note: until the repair is applied and the judge runs, a passing result cannot rule out holdout tuning. It stays unverified.
- Skipped:
  - `altitude`: the scope is fixed to offline evaluation, so higher rungs such as live alerting or analyst-workflow pilots are outside it.
  - `depth` hard target and `range`: the method set and acceptance conditions are closed. Stretch metrics or borrowed methods would change them. The customer split already matches the repeated entity, which is the customer.
- Owner actions:
  - Approve the freeze-and-log step.
  - Confirm the evaluation runner exists, the approved recall threshold is documented, and the holdout is untouched.
  - Confirm the independent analyst's availability and permission to see the material.
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
Our nightly pipeline that rebuilds the reporting tables takes about 4 hours, and analysts wait for it each morning. Get it under 3 hours. It runs on our existing Airflow and Postgres setup. No new infrastructure spend and no changes to the report definitions.

Assumption: Success means the complete, correct nightly reporting tables are ready for analysts sooner—not merely that Airflow reports success sooner, required work moves outside the timer, or other workloads absorb the delay.

Use these methods to find and remove the actual bottleneck:
- Apply critical-path analysis from operations research to the Airflow DAG. Use task timings, dependencies, retries, queue delays, and concurrency limits to distinguish work that controls completion time from work whose acceleration would not help. Estimate the best achievable runtime from each proposed change before pursuing it.
- Start from the deployed DAGs, executed SQL, task logs, input volumes, and database execution evidence—not just aggregate runtime. Use Postgres EXPLAIN and, where safe and authorized, EXPLAIN (ANALYZE, BUFFERS) to identify expensive scans, join amplification, spills, estimation errors, and lock waits. Use existing database telemetry where available; do not assume additional extensions or services.
- Optimize the measured bottlenecks using the existing Airflow and Postgres setup. Consider equivalent SQL rewrites, existing-capacity indexing or statistics improvements, and dependency or concurrency adjustments. Increase parallelism only when measurements show that shared database contention does not erase the benefit.
- Aim for 18 minutes end to end using critical-path reduction and evidence-led query optimization, under the same workload and resource envelope as the baseline. Under 3 hours remains the required pass condition. If one approach stalls, try the next supported approach within existing resources and authorized execution time before reporting the stretch target missed.

Validate performance and meaning together:
- Establish a baseline and compare changes on matching source-data snapshots and logical run dates, with comparable database state, cache conditions, resource limits, and competing workload. Measure from the same nightly start boundary through completion of every required refresh and availability of all reporting tables.
- Use differential testing from software verification: compare baseline and optimized outputs as multisets, preserving duplicates and NULLs, and compare schemas and all report-definition-dependent behavior. Include relevant empty-input, date-boundary, and duplicate-key cases supported by the actual definitions.
- Use fault injection on existing authorized test capacity to check consequential retry, partial-refresh, and concurrency risks introduced by the optimization. Do not let a faster run expose incomplete or inconsistent results to analysts.
- Keep representative validation inputs unused during tuning, including a high-volume case if available. Freeze the candidate before evaluating it on those inputs; if validation causes another revision, obtain fresh validation evidence or leave the revised result unverified.
- Report the implemented changes, comparable before/after runtimes, correctness evidence, remaining bottleneck, and whether the 18-minute stretch was met or missed. Separate measured results from estimates.

Keep the nightly rebuild on the existing Airflow and Postgres setup. Spend nothing on new infrastructure. Do not change report definitions, omit required work, or weaken correctness to meet either runtime target.

First check: Confirm access and permission for the deployed DAGs and SQL, Airflow timing records, Postgres execution evidence, representative source snapshots, and the existing resource configuration. Confirm that authorized existing capacity can support comparable benchmarks, output comparisons, and any fault-injection tests without disrupting analysts or other workloads. Identify available unused validation inputs. If a dependency is missing, continue only with supported, authorized work and leave the affected claims unverified.

Judge: A reproducible replay-and-comparison harness records all validation attempts and checks the frozen candidate against the baseline on matching snapshots and logical run dates; pass only if every representative held-out validation run finishes in strictly under 3 hours through complete analyst-ready publication, output multisets and schemas match, report definitions remain unchanged, applicable retry and publication checks pass, and resource/configuration evidence shows no new infrastructure spend or displaced required work; record comparable baseline timings and the 18-minute stretch separately as met or missed, and leave any claim without its required evidence unverified.
```

- `altitude`: Moves from a shorter Airflow runtime to earlier **complete, correct analyst availability**. The measured boundary includes publication and all required refreshes, preventing a nominal speedup that merely hides work. No new platform or recurring workflow.
- `depth`: Adds critical-path estimates and raw Postgres execution evidence to target changes that can actually reduce completion time. Sets an **18-minute stretch**, while preserving **under 3 hours** as acceptance; experiments stay within existing resources and authorized execution time.
- `range`: Borrows differential testing and fault injection from software verification to detect semantic drift, partial publication, and retry/concurrency failures. Held-out replays distinguish demonstrated improvement from tuning success; these require authorized existing test capacity.
- Skipped lenses: None; each contributes a distinct outcome, optimization method, or correctness check.
- Owner actions: Confirm evidence access, representative validation inputs, and authorized benchmark capacity and execution time. No new spending, external sharing, or recurring operational workflow is authorized.
````

## D22

### Check B6

B6. Authority: Added scope, new access, paid steps, and irreversible actions are conditional on approval inside the prompt, not only in commentary. Explicitly prohibited expansions remain prohibited. A response with no expansion passes without needing an irrelevant approval ritual.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Task

```text
Evaluate whether our churn model gives analysts a useful early-warning signal. The approved scope is offline evaluation only. Use the supplied de-identified training set and untouched later-period holdout, split by customer to prevent leakage. Reproduce the current model and its baseline, test the onboarding explanation from the raw events, check calibration and subgroup errors, and have an independent analyst audit leakage and the conclusion against a written rubric. Do not tune on the holdout. Report uncertainty and missed targets. Judge: the existing evaluation runner must reproduce the baseline, enforce customer separation, and show holdout precision at the approved recall threshold above the baseline with a 95% confidence interval for the difference excluding zero. Otherwise report that the evidence does not establish improvement. Keep these scope, methods, and acceptance conditions unchanged.
```

### Output

````markdown
```text
Evaluate whether our churn model gives analysts a useful early-warning signal. The approved scope is offline evaluation only. Use the supplied de-identified training set and untouched later-period holdout, split by customer to prevent leakage. Reproduce the current model and its baseline, test the onboarding explanation from the raw events, check calibration and subgroup errors, and have an independent analyst audit leakage and the conclusion against a written rubric. Do not tune on the holdout. Report uncertainty and missed targets. Keep these scope, methods, and acceptance conditions unchanged.
With my approval only: before the evaluation runner first reads the holdout, freeze the model, baseline, features, and every setting chosen on training evidence, and record a hash and timestamp for each. Log every holdout read, with its time and purpose, and apply the frozen settings to the holdout once. Give the freeze record and read log to the independent analyst for the leakage audit. Until this is applied and the judge runs on the frozen work, the improvement conclusion stays unverified.
First check: the supplied de-identified training set, the later-period holdout, the raw onboarding events, the existing evaluation runner, the approved recall threshold value, and the written rubric are all available. Confirm the holdout has not yet been read for model or threshold choices. Name anything missing, continue only with supported, authorized work, and leave dependent results unverified.
First check: the independent analyst is available, is independent of the model's authors and of this evaluation, and is permitted to see the de-identified data, the runner output, and the freeze record. If not, the leakage audit and the conclusion audit stay unverified.
Judge: the existing evaluation runner must reproduce the baseline, enforce customer separation, and show holdout precision at the approved recall threshold above the baseline with a 95% confidence interval for the difference excluding zero. Otherwise report that the evidence does not establish improvement.
```

**Ledger**

- `depth`: Closes a loophole between the rule "Do not tune on the holdout" and the judge. The judge reads only the final holdout comparison, so a model or setting picked by repeatedly reading the holdout could pass while the result is biased by that selection. The fix freezes settings chosen on training data before any holdout read, logs every read, and gives both records to the analyst the owner already chose. It adds no analysis, metric, threshold, or partition. Cost: a hash, a timestamp, and a log. It sits behind approval.
- `depth`: Adds First-check lines for the unconfirmed dependencies:
  - the data sets, raw events, runner, threshold value, and rubric
  - whether the holdout is still untouched
  - the analyst's availability, independence, and permission to see the material

  The owner chose this analyst, so no separate approval is needed to share material with them.
- **Skipped:**
  - `altitude`: the approved scope is offline evaluation only, so the work can't move up to driving analyst decisions or a pilot.
  - Depth hard-target and new-finding moves: the metrics and acceptance conditions are fixed.
  - `range`: the method set is closed.
- **Owner actions:**
  - Approve or decline the freeze-and-read-log repair.
  - Confirm the approved recall threshold value.
  - Confirm the holdout is untouched.
  - Confirm the independent analyst's availability and data permissions.
````

## D23

### Check T11d

T11d. Any rebuild, framework change, or paid service is behind approval.

Applicability note for this case: The task's “about 10 seconds to load” is a user report, not an established LCP, percentile, device profile, or measured baseline. A prompt may choose a named metric and stretch, but must establish the corresponding baseline before claiming improvement. Any LCP target below 2.5 s passes T11b; do not require a specific value such as 200 ms. A target on another metric passes T11b only if it lies past that metric's "good" threshold. A before/after comparison must use a comparable metric and profile.

### Task

```text
Make our marketing website load faster. The home page takes about 10 seconds to load on mobile.
```

### Output

````markdown
```text
Make our marketing website load faster. The home page takes about 10 seconds to load on mobile.
Assumption: the goal is that mobile visitors see the home page's main content and can act on it (sign up, contact, buy) before they give up and leave.
Assumption: "about 10 seconds" reflects what typical mobile visitors on real devices and networks experience, and is not one slow test.
Baseline from raw evidence before changing anything. Find out what the 10-second figure measured (which metric, device, network, first or repeat view). Then reproduce it on a cold-cache first view of the home page, emulating a mid-tier Android phone on a 4G throttling profile in WebPageTest or Lighthouse. Take the median of at least 5 runs and record LCP, FCP, TTFB, TBT, CLS, total bytes, and request count. Pull field data at p75 for mobile (LCP, INP, CLS) from the Chrome UX Report through PageSpeed Insights for the home page URL. Use it to test whether lab and field agree, and report any disagreement.
Diagnose the critical path. Read the waterfall and a Chrome DevTools Performance trace as a dependency graph. Identify the LCP element and the longest chain of requests that blocks it: server response, redirects, render-blocking CSS and JS, web fonts, the LCP image, third-party scripts, and any consent banner. Fix that chain first, then the next-longest one.
Apply the standard instruments as the trace justifies:
- Responsive AVIF or WebP images with srcset, and explicit dimensions to prevent layout shift.
- preload or fetchpriority="high" on the LCP resource; never lazy-load it.
- Inline critical CSS and defer the rest.
- Code-split and defer non-critical JS, using a bundle analyzer to find dead or oversized dependencies.
- font-display with subsetted, preloaded fonts.
- Long-lived cache headers and compression (Brotli).
- CDN and TTFB fixes where the server is the bottleneck.
- Defer or delay third-party marketing tags until after load or interaction.
Build an inventory of every third-party tag that records its byte and main-thread cost, what it does, and which team relies on it. Put this inventory in the report so its owners can decide what each tag is worth.
Measure each change on its own against the baseline, under the same conditions and with the same run count. The report must attribute the gain to specific changes, and must drop or revert changes that do not help.
Red-team the result before claiming a win:
- Confirm that gains hold on a cold cache, a first view, and with the consent banner shown.
- Confirm that the LCP element is still the meaningful content and not a placeholder.
- Confirm that no content, layout, form, or analytics/conversion event broke. Capture before/after screenshots at mobile and desktop widths and before/after lists of fired analytics events.
Aim for mobile LCP at or below 2.0 s (lab median, then field p75), TBT at or below 150 ms, and CLS at or below 0.05, by removing work from the critical path. If one approach stalls, try the next within this task's scope before reporting a miss. The pass bar remains "faster than the reproduced baseline." Report attainment of the stretch target separately, as met or missed.
Deliver a report with: the baseline and how it was reproduced; the critical-path diagnosis; each change with its measured effect; before/after metrics under identical conditions; the third-party tag inventory; red-team results; the stretch result, met or missed; and field-data status.
With my approval only: deploy the changes to the production website.
With my approval only: remove (not merely defer) any third-party marketing or analytics tag, with each tag's owning team named in the request.
With my approval only: change paid hosting or CDN plans or settings that carry a cost.
With my approval only: add real-user monitoring by sending web-vitals metrics (LCP, INP, CLS) from visitors' browsers to our existing analytics.
With my approval only: add a Lighthouse CI performance budget to the site's build pipeline so regressions fail the build.
With my approval only: after deployment, serve the previous build to a small holdout share of mobile traffic for two weeks and compare bounce rate and conversion rate against the new build.
First check: confirm access to the site's source code, build system, hosting/CDN configuration, and a preview or staging environment to test on. Confirm what the 10-second figure measured and on what device. Confirm that WebPageTest or Lighthouse can run against the site and that PageSpeed Insights/CrUX has field data for the home page (low-traffic pages may have none). Confirm read access to the analytics configuration so the list of fired events can be verified. Name any missing dependency, continue only with supported, authorized work, and leave affected results unverified.
Judge: on the same URL, device emulation, network profile, cold-cache first view, and run count (median of ≥5) as the reproduced baseline, the changed home page must score lower than baseline on the metric matching the reported 10-second figure. Before/after screenshots must differ only in listed, intended changes. Every analytics/conversion event that fired at baseline must still fire, except tags removed with approval. Pass only if all three hold. Report the LCP ≤ 2.0 s / TBT ≤ 150 ms / CLS ≤ 0.05 stretch as met or missed in lab. Field p75 stays unverified until the 28-day CrUX window (or approved RUM) covers the post-deploy period.
```

**Ledger**
- `altitude`: the outcome moves from "a faster home page" to "visitors see content and convert before leaving." The holdout bounce/conversion comparison sits behind approval because it touches production traffic.
- `depth`: the work starts by reproducing the 10-second baseline from raw lab runs and CrUX field data instead of the anecdote. This exposes whether the figure is lab or field and what it measured.
- `depth`: diagnosis works from the critical path and LCP element (waterfall plus DevTools trace) instead of generic tips. Effort goes to what actually blocks rendering.
- `depth`: each change is measured on its own. Gains are attributed and useless changes are dropped. This costs extra test runs.
- `depth`: the hard target is LCP ≤ 2.0 s, TBT ≤ 150 ms, CLS ≤ 0.05, which is past Core Web Vitals "good." It is reported separately, and the owner's "faster" bar stays the pass condition.
- `range`: from performance engineering, the waterfall is treated as a dependency graph so the longest blocking chain is fixed first.
- `range`: from measurement statistics, the prompt requires a median of ≥5 runs under identical conditions, with lab and field p75 kept separate. This stops single-run noise from being claimed as a win.
- `range`: from marketing-ops tag governance, a per-tag cost/owner inventory turns third-party script decisions into owner choices. Removing a tag requires approval because it can break other teams' attribution.
- `range`: a red-team pass checks cold cache, the consent banner, LCP placeholders, visual regressions, and analytics event parity. This catches fake speedups and broken tracking.
- New-scope items behind approval: the production deploy (outward-facing), paid CDN/hosting changes (cost), RUM collection (new data flow from visitors), the Lighthouse CI budget (CI change), and the traffic holdout (production experiment).
- Skipped lenses: none.
- Owner actions:
  - Confirm source, build, hosting/CDN, staging, and analytics access.
  - Say what the 10-second figure measured.
  - Decide on each approval line: deploy, tag removal, paid CDN changes, RUM, CI budget, and holdout.
  - Name the owners of the third-party tags.
````

## D24

### Check T11d

T11d. Any rebuild, framework change, or paid service is behind approval.

Applicability note for this case: The task's “about 10 seconds to load” is a user report, not an established LCP, percentile, device profile, or measured baseline. A prompt may choose a named metric and stretch, but must establish the corresponding baseline before claiming improvement. Any LCP target below 2.5 s passes T11b; do not require a specific value such as 200 ms. A target on another metric passes T11b only if it lies past that metric's "good" threshold. A before/after comparison must use a comparable metric and profile.

### Task

```text
Make our marketing website load faster. The home page takes about 10 seconds to load on mobile.
```

### Output

````markdown
```text
Make our marketing website load faster. The home page takes about 10 seconds to load on mobile.

Assumption: the priority is a visibly usable mobile home page, not merely a better performance score.
Assumption: preserve the site's content, branding, accessibility, analytics behavior, and primary marketing journeys.

Start with the home page. Establish what the reported “10 seconds to load” measures; do not treat it as an observed Largest Contentful Paint (LCP) baseline without measurement.

Use browser Performance traces and Network waterfalls to identify the actual critical rendering path: document response, render-blocking resources, main-thread work, and the resource responsible for LCP. Inspect the source assets and implementation behind the bottleneck rather than optimizing from a Lighthouse score alone. Rank changes by measured contribution to the delay, then implement and remeasure the highest-impact fixes.

Use controlled paired benchmarking: measure the original and optimized versions on the same mobile device or emulation profile, network and CPU settings, page state, and cache conditions. Alternate versions across at least five runs each, with separate cold-cache and warm-cache results. Report median LCP, load-event timing, and run-to-run variability; distinguish measurements from hypotheses.

Aim for median mobile LCP below 1.5 seconds using the measured bottleneck's appropriate remedy—for example, prioritizing the actual hero resource, removing render-blocking work, reducing JavaScript execution, or improving document delivery. Establish the baseline under those same conditions. If one approach stalls, try the next supported bottleneck within the available budget and deadline. The stretch is not the acceptance threshold: demonstrate a real improvement over baseline and report stretch attainment separately as met, missed, or unverified.

Apply human-computer interaction's critical-task walkthrough: identify the existing primary marketing action, then check that the headline and call to action become visible and usable without waiting for nonessential work. Do not improve timing by hiding required content, disabling behavior, or moving necessary work past the measurement window.

Deliver the implementation changes and a concise before/after evidence report: test conditions, measurements, trace-supported causes, preserved user journeys, stretch status, and remaining limitations. Treat conclusions as unverified until their checks run. Do not deploy or purchase services without authorization.

With my approval only: after a separately authorized release, conduct a seven-day validation using existing mobile real-user telemetry to compare home-page p75 LCP with a comparable pre-release window; add no new tracking or data collection.

First check: identify the target website, relevant source repository, authorized editing environment, available browser/profiling tools, supported mobile conditions, and any budget or deadline constraints. Use only existing authorized access; name missing dependencies and continue only with supported work.
First check: for approved field validation, confirm existing telemetry access, sufficient observations, comparable pre-release data, and a reliable release identifier; otherwise leave field effectiveness unverified.

Judge: paired browser benchmarks and saved traces must show lower median mobile LCP beyond observed run-to-run variability under identical conditions, without a load-event regression beyond baseline variability; browser checks must preserve required content, the primary marketing journey, analytics behavior, and accessibility without new regressions. Report the below-1.5-second stretch separately, not as a pass requirement. For approved field validation, pass only if comparable mobile p75 LCP improves; insufficient or noncomparable evidence leaves that result unverified.
```

- `altitude`: Moves from a faster implementation to evidence of faster real-user experience after release; optional seven-day validation requires approval and existing telemetry, with no new tracking.
- `depth`: Replaces the approximate load-time claim with reproducible baselines, raw rendering evidence, bottleneck-directed fixes, and a below-1.5-second LCP stretch; adds local measurement effort, not paid tooling.
- `range`: Uses controlled paired benchmarking to separate improvement from measurement noise, and an HCI critical-task walkthrough to prevent gains that sacrifice the marketing experience.
- Skipped lenses: none; each contributes a distinct outcome or check.
- Owner actions: identify the website and authorized source access, clarify budget/deadline constraints, and decide whether to approve post-release field validation.
````

## D25

### Check B6

B6. Authority: Added scope, new access, paid steps, and irreversible actions are conditional on approval inside the prompt, not only in commentary. Explicitly prohibited expansions remain prohibited. A response with no expansion passes without needing an irrelevant approval ritual.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Task

```text
Evaluate whether our churn model gives analysts a useful early-warning signal. The approved scope is offline evaluation only. Use the supplied de-identified training set and untouched later-period holdout, split by customer to prevent leakage. Reproduce the current model and its baseline, test the onboarding explanation from the raw events, check calibration and subgroup errors, and have an independent analyst audit leakage and the conclusion against a written rubric. Do not tune on the holdout. Report uncertainty and missed targets. Judge: the existing evaluation runner must reproduce the baseline, enforce customer separation, and show holdout precision at the approved recall threshold above the baseline with a 95% confidence interval for the difference excluding zero. Otherwise report that the evidence does not establish improvement. Keep these scope, methods, and acceptance conditions unchanged.
```

### Output

````markdown
```text
Evaluate whether our churn model gives analysts a useful early-warning signal.

The approved scope is offline evaluation only. Use the supplied de-identified training set and untouched later-period holdout, split by customer to prevent leakage. Reproduce the current model and its baseline, test the onboarding explanation from the raw events, check calibration and subgroup errors, and have an independent analyst audit leakage and the conclusion against a written rubric. Do not tune on the holdout. Report uncertainty and missed targets. Keep these scope, methods, and acceptance conditions unchanged.

With my approval only: close the enforcement gap in “Do not tune on the holdout” by freezing the reproduced model, baseline, and evaluation settings before any holdout read, recording every holdout read, and applying the frozen settings once to the untouched holdout without revising them in response to its results. This adds no analysis, metric, threshold, or partition.

First check: the supplied datasets, raw events, model and baseline reproduction artifacts, existing evaluation runner, and approved recall threshold are available; the independent analyst is available and permitted to see the evaluation material. Confirm whether the holdout has already been read and whether the freeze-and-read-record repair is approved and feasible. If any check fails, continue only with supported, authorized work. Any conclusion affected by the enforcement gap remains unverified until the approved repair is applied and the runner and audit run on the repaired evaluation.

Judge: the existing evaluation runner must reproduce the baseline, enforce customer separation, and show holdout precision at the approved recall threshold above the baseline with a 95% confidence interval for the difference excluding zero. Otherwise report that the evidence does not establish improvement. The independent analyst checks leakage and whether the conclusion follows these acceptance conditions against a written rubric. For that audit, pass only if every criterion is met; the model-improvement acceptance conditions remain unchanged.
```

- `depth`: “Do not tune on the holdout” is not enforced by the stated runner: customer separation and a positive confidence interval can still pass after holdout-driven tuning. The approval-gated freeze and read record make that explicit prohibition auditable without changing the fixed analyses, metrics, thresholds, or partitions. Dependencies and analyst access are checked before execution; affected conclusions remain unverified pending repair and validation.
- Skipped: `altitude`—operational deployment or analyst-workflow trials would exceed offline evaluation; `range`—the fixed methods already require an independent audit, and no additional field’s method is needed to close the demonstrated loophole.
- Owner actions: approve or decline the freeze-and-read-record repair; confirm artifact availability, prior holdout access, and the independent analyst’s availability and permission to review the material.
````

## D26

### Check B4

B4. Judge: A changed prompt ends with task-specific independent evidence and an observable pass condition. Proposed or unavailable validation remains unverified until run. The model's own confidence does not count as the judge.

Applicability for this case: Changed. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Task

```text
Fix this TypeScript function: function formatLabel(value: string | null) { return value.trim(); }
It throws for null. Return the literal em dash "—" for null and preserve current trimming for every non-null string. Keep the public signature. No new dependencies and no changes outside this helper and its tests.
```

### Output

````markdown
```text
Fix this TypeScript function: function formatLabel(value: string | null) { return value.trim(); }
It throws for null. Return the literal em dash "—" for null and preserve current trimming for every non-null string. Keep the public signature. No new dependencies and no changes outside this helper and its tests.
```
Unchanged: this is one small, clearly bounded change with a stated result, and the task text shows no targeting or verification defect. The obvious tests (null returns "—", and non-null strings including whitespace-only ones still match `value.trim()`) are ones the executor would write anyway, and a property-based library would break the no-new-dependencies rule.
````

## D27

### Check T11a

T11a. Depth: the prompt names raw material a performance engineer starts from (field data or traces, a waterfall, the bundle) and instruments by name (for example a lab tool and real-user measurement), not "optimize images".

Applicability note for this case: The task's “about 10 seconds to load” is a user report, not an established LCP, percentile, device profile, or measured baseline. A prompt may choose a named metric and stretch, but must establish the corresponding baseline before claiming improvement. Any LCP target below 2.5 s passes T11b; do not require a specific value such as 200 ms. A target on another metric passes T11b only if it lies past that metric's "good" threshold. A before/after comparison must use a comparable metric and profile.

### Task

```text
Make our marketing website load faster. The home page takes about 10 seconds to load on mobile.
```

### Output

````markdown
```text
Make our marketing website load faster. The home page takes about 10 seconds to load on mobile.

Assumption: The intended outcome is that mobile visitors can see the main marketing message and use the primary call to action sooner—not merely that a load event fires earlier.
Assumption: Preserve the page’s content, branding, accessibility, consent behavior, and essential functionality.

Measure before optimizing. Establish what the reported “about 10 seconds” measures; do not assume it is Largest Contentful Paint (LCP). Capture raw Chrome performance traces and network waterfalls for the current home page under a documented, representative mobile device/network profile, with a cold cache. Record LCP and when the primary call to action becomes usable.

Use critical-path analysis to identify the dependencies delaying the main content: distinguish server response, resource discovery, download time, and rendering delay. Prioritize changes that shorten that measured path rather than merely improve a synthetic score. Test each proposed cause with a controlled intervention before attributing the improvement to it.

Aim for median mobile LCP below 1.5 seconds using the bottlenecks demonstrated by those traces. Compare baseline and candidate using at least five cold-cache runs each under the same device, network, browser, and serving conditions. If one approach stalls, try the next evidence-supported bottleneck within the available time and authorized resources before reporting a miss. Treat 1.5 seconds as a stretch target, not a replacement for demonstrating improvement.

Use an adversarial check against misleading speedups: verify that the main message and primary call to action have not been hidden, removed, or deferred beyond the measurement window. Check that faster initial rendering has not made the primary action usable later.

Implement supported improvements in the existing website. Provide the changes and a concise before/after report identifying the test conditions, measurements, demonstrated causes, remaining bottlenecks, and whether the stretch target was met or missed. Do not claim a conversion improvement without conversion evidence. Do not deploy to production, introduce paid services, or establish recurring monitoring as part of this task.

First check: confirm the home-page URL, authorized source/build access, a reproducible serving environment, and browser performance tooling are available; establish a representative mobile test profile. If a dependency is unavailable, continue only with supported, authorized work and leave affected claims unverified.
Judge: A reproducible browser benchmark shows lower median LCP across at least five comparable cold-cache mobile runs per version, with no later primary-action usability; the owner checks that the main message, primary action, branding, accessibility, consent behavior, and essential functionality remain intact. Pass only if both the benchmark and every owner-review criterion pass; report the below-1.5-second stretch separately as met or missed, and leave any untested claim unverified.
```

- `altitude`: Moves from a faster-loading page to earlier access to its message and primary action; adds usability evidence without claiming conversion gains or requiring a new workflow.
- `depth`: Replaces the ambiguous 10-second baseline with comparable raw traces, controlled interventions, and a below-1.5-second LCP stretch target. Requires authorized build access and local benchmarking; no deployment or paid services.
- `range`: Applies adversarial testing to expose speedups achieved by hiding or deferring meaningful content; adds a content-integrity and action-readiness check.
- Skipped lenses: none.
- Owner actions: confirm access and representative mobile conditions; perform the final qualitative review. Missing evidence leaves the relevant result unverified.
````

## D28

### Check B6

B6. Authority: Added scope, new access, paid steps, and irreversible actions are conditional on approval inside the prompt, not only in commentary. Explicitly prohibited expansions remain prohibited. A response with no expansion passes without needing an irrelevant approval ritual.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Task

```text
Tell me why customers churned last month. I have no raw event logs, CRM export, or database access to share right now. All I know is that the sales team thinks onboarding is the cause. Do not buy data, scrape customer information, or request production credentials.
```

### Output

````markdown
```text
Tell me why customers churned last month. I have no raw event logs, CRM export, or database access to share right now. All I know is that the sales team thinks onboarding is the cause. Do not buy data, scrape customer information, or request production credentials.

Assumption: You want to know whether the onboarding explanation is supported enough to guide retention priorities, rather than receive a plausible but unverified story.

Start with what can actually be concluded from the supplied information. Treat the sales team's belief as a hypothesis, not an observed churn cause. Do not invent customer behavior, cancellation reasons, churn rates, or the relative contribution of different causes.

Use causal inference's competing-explanations method to test the onboarding hypothesis conceptually. Distinguish onboarding causing churn from onboarding difficulties being a symptom of poor product fit or mismatched sales expectations. Include other explanations only when they materially change how the onboarding claim should be tested. Label every proposed explanation unverified.

For each explanation, identify a discriminating observation: evidence that would favor it over a named alternative, and evidence that would weaken it. Explain why a pattern among churned customers alone may be misleading without a comparable retained-customer group. These are proposed tests, not analyses you have performed. Acknowledge that even a group difference would not by itself establish causation.

Use decision theory's value-of-information method to identify the smallest evidence package that could change whether onboarding deserves priority. Specify what decision it could inform, not just what data would be interesting. Do not assume that this evidence exists or that you can obtain it.

Present a concise diagnostic brief: what is known, what remains unknown, the competing explanations and their discriminating tests, and whether the current evidence warrants prioritizing onboarding. If it does not, say so without implying that onboarding has been ruled out. Keep causal conclusions unverified until suitable evidence is available and the relevant tests have been run.

With my approval only: analyze an owner-supplied, non-identifying aggregate comparison of last month's churned customers and a comparable retained group against the proposed onboarding test; do not obtain the data yourself.
First check: establish the owner's definition of churn and the period meant by “last month” before specifying a cohort comparison; if unresolved, describe the tests conditionally rather than inventing definitions or dates.
First check: before any approved aggregate analysis, confirm that the owner can supply the comparison, that its use is authorized, and that the groups and measurements support the proposed test. The raw logs, CRM export, and database access are unavailable; proceed with the limited diagnostic brief, and leave unsupported conclusions unverified.
Judge: The owner, as business-context reviewer, checks that every claimed observation is traceable to the supplied information, the sales belief is not presented as a finding, each proposed explanation has evidence that could distinguish it from a named alternative and evidence that could weaken it, the prioritization advice reflects the evidence limits, and all access prohibitions are preserved. Pass only if every criterion is met; passing validates the brief's reasoning and calibration, not an untested churn attribution.
```

- `altitude`: Changes the outcome from a churn explanation alone to an evidence-calibrated basis for deciding whether to prioritize onboarding; adds no authority to change retention workflows.
- `depth`: Uses competing causal explanations and falsifying observations to challenge the sales hypothesis rather than elaborate it. Raw evidence remains unavailable; optional aggregate analysis requires approval, availability, and authorization.
- `range`: Uses decision theory’s value of information to identify the smallest evidence package that could change the prioritization decision, avoiding an indiscriminate data request.
- `depth`: Adds an owner-reviewed evidence-traceability rubric; passing cannot certify a causal explanation without supporting evidence.
- Skipped lenses: None; each contributes a distinct improvement.
- Owner actions: Clarify churn and “last month”; review the brief. Optionally approve aggregate analysis and supply suitable authorized material when available.
````

## D29

### Check B2

B2. Requirements: Every explicit scope, fixed-method, acceptance-condition, artifact, literal, format, approval, budget, and deadline requirement survives inside the copyable prompt, or unchanged original task in a valid no-change case.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Task

```text
Evaluate whether our churn model gives analysts a useful early-warning signal. The approved scope is offline evaluation only. Use the supplied de-identified training set and untouched later-period holdout, split by customer to prevent leakage. Reproduce the current model and its baseline, test the onboarding explanation from the raw events, check calibration and subgroup errors, and have an independent analyst audit leakage and the conclusion against a written rubric. Do not tune on the holdout. Report uncertainty and missed targets. Judge: the existing evaluation runner must reproduce the baseline, enforce customer separation, and show holdout precision at the approved recall threshold above the baseline with a 95% confidence interval for the difference excluding zero. Otherwise report that the evidence does not establish improvement. Keep these scope, methods, and acceptance conditions unchanged.
```

### Output

````markdown
```text
Evaluate whether our churn model gives analysts a useful early-warning signal.

The approved scope is offline evaluation only. Use the supplied de-identified training set and untouched later-period holdout, split by customer to prevent leakage. Reproduce the current model and its baseline, test the onboarding explanation from the raw events, check calibration and subgroup errors, and have an independent analyst audit leakage and the conclusion against a written rubric. Do not tune on the holdout. Report uncertainty and missed targets. Keep these scope, methods, and acceptance conditions unchanged.

With my approval only: use a freeze-and-read-log protocol to enforce the existing no-tuning rule: freeze the reproduced model, baseline, approved recall threshold, and evaluation settings before reading the holdout; record every holdout read and have the already-required independent analyst inspect that record. This adds no partition, analysis, metric, or threshold.

First check: confirm availability of the supplied datasets, raw events, model and baseline reproduction artifacts, existing evaluation runner, approved recall threshold, and written audit rubric. Confirm that the independent analyst is available and permitted to inspect the evaluation material.

First check: before dependent work, establish whether the freeze-and-read-log protocol is approved and can be applied before any holdout read. If a dependency check fails, continue only with supported, authorized work. Any conclusion affected by the no-tuning enforcement gap remains unverified until the approved repair is applied and the existing judge runs on the repaired work.

Judge: the existing evaluation runner must reproduce the baseline, enforce customer separation, and show holdout precision at the approved recall threshold above the baseline with a 95% confidence interval for the difference excluding zero. Otherwise report that the evidence does not establish improvement.
```

- `depth`: Adds experimental-design controls—freezing settings and recording holdout reads—to enforce **“Do not tune on the holdout.”** The stated runner could pass after holdout-guided tuning because its listed checks do not detect that behavior. The repair addresses that loophole without changing the fixed methods or statistical acceptance conditions; it requires approval and adds recordkeeping.
- `depth`: Adds dependency and analyst-authorization checks, and explicitly leaves affected conclusions unverified when enforcement or required evidence is unavailable. No new reviewer or data sharing is introduced.
- Skipped: `altitude`—deployment or analyst-workflow trials would exceed offline-only scope; `range`—no distinct additional method is justified within the fixed-method boundary.
- Owner actions: approve or decline the freeze-and-read-log protocol; resolve missing artifacts or rubric; confirm the independent analyst’s availability and permission.
````

## D30

### Check B6

B6. Authority: Added scope, new access, paid steps, and irreversible actions are conditional on approval inside the prompt, not only in commentary. Explicitly prohibited expansions remain prohibited. A response with no expansion passes without needing an irrelevant approval ritual.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

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

## D31

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
Our nightly pipeline that rebuilds the reporting tables takes about 4 hours, and analysts wait for it each morning. Get it under 3 hours. It runs on our existing Airflow and Postgres setup.
Assumption: what analysts care about is the clock time when the reporting tables they use are ready, not runtime alone. Alongside total runtime, report when each reporting table is committed relative to the scheduled start.
Assumption: "no changes to the report definitions" means every reporting table keeps its schema, rows, and values. The SQL and physical execution that produce them may change. If the definitions are meant to be the SQL text itself, limit the work to scheduling, concurrency, indexing, and physical storage changes, and make no query rewrites or incremental logic.
Start from raw evidence, not impressions. Pull start, end, queue, and retry times for every task over at least the last 30 runs from the Airflow metadata database (task_instance, dag_run). Split each morning's wait into four parts: upstream data arrival delay, scheduler queue time, run time, and retries. If late upstream data dominates, say so before optimizing runtime, because a faster run will not help analysts in that case.
Build the DAG's critical path from those durations (critical path method from project scheduling). The wall clock equals the longest chain of dependent tasks. Speeding up tasks off that chain changes nothing, so rank the work by each task's contribution to the critical path.
Treat database capacity as a shared, limited resource. Sample pg_stat_activity wait events during a run to see whether parallel tasks are waiting on CPU, I/O, or locks. Set Airflow pools and max_active_tasks to the concurrency the database actually sustains, which can be lower than what the DAG allows.
For each heavy critical-path query, use EXPLAIN (ANALYZE, BUFFERS) and pg_stat_statements, where already enabled, to find the cause: bad join order from stale statistics, missing indexes, sorts spilling to disk, row-by-row loops. Apply the matching fix inside the pipeline:
- set-based rewrites;
- session-level SET work_mem;
- loading into staging or UNLOGGED tables, then building indexes and running ANALYZE after the load;
- CREATE TABLE AS plus a rename swap instead of DELETE and INSERT;
- incremental rebuilds that recompute only the partitions or keys whose source rows changed, where this provably yields the same output as a full rebuild.
Aim for under 18 minutes wall clock, measured the same way as the baseline. Get there by combining critical-path shortening, right-sized concurrency, and incremental rebuilds. When one approach stalls, try the next before reporting a miss. The under-3-hours bar remains the pass condition. Report the 18-minute stretch separately, met or missed.
Red-team any incremental logic. Pick past dates where the full rebuild and an incremental rebuild are most likely to diverge: late-arriving rows, updates or deletes to rows from earlier days, backfills, month or quarter boundaries. Replay those dates through both and compare.
Deliver the changed pipeline code and a short report with these parts:
- baseline and candidate timings measured under comparable conditions;
- the critical path before and after;
- per-table ready times;
- the morning wait decomposition;
- equivalence results for every reporting table.
Keep it on the existing Airflow and Postgres setup, with no new infrastructure spend and no changes to the report definitions.
With my approval only: change Postgres server-level parameters (for example max_parallel_workers, maintenance_work_mem, or enabling pg_stat_statements/auto_explain via shared_preload_libraries), which may need a restart and affect other workloads on the server.
With my approval only: add indexes or partitioning to source tables the pipeline reads but does not own.
With my approval only: run the candidate pipeline in a shadow schema alongside production for 5 consecutive nights, on existing storage and capacity, before it replaces the production DAG.
With my approval only: deploy the changed DAG to the production nightly schedule.
First check: read access to the Airflow metadata database exists. A non-production Postgres environment with production-volume data exists, or an off-hours window on production is permitted for test runs. pg_stat_statements is already enabled or not. Disk headroom can hold a second copy of the reporting tables for comparison and shadow runs without new spend. Other workloads share the Postgres server or not. Analysts' usual start time is known. If any check fails, name it, continue only with supported and authorized work, and leave the affected results unverified.
Judge: run the baseline pipeline twice and the candidate pipeline at least 3 times on the same production-volume input snapshot (or across the approved shadow nights) under comparable load; pass only if every candidate run's wall clock from first task start to last reporting table committed is under 3 hours, and every reporting table matches the baseline as a multiset of rows (equal row counts and empty symmetric EXCEPT, or equal hashes over all columns), with the only allowed differences being columns or values that also differ between the two baseline runs (such as load timestamps or float sums from parallel aggregation), including on the replayed late-arrival, correction, backfill, and period-boundary dates; any other mismatch fails, and the 18-minute stretch is reported separately as met or missed.
```

**Ledger**

- `altitude`: The original outcome was a 4-hour runtime cut to under 3 hours. The improved outcome is reporting tables ready when analysts start, shown by per-table ready times and a breakdown of the morning wait. This catches the case where upstream data, not runtime, causes the wait. It adds no scope beyond measurement.
- `depth`: Raw Airflow task history, EXPLAIN (ANALYZE, BUFFERS), pg_stat_statements, and wait-event sampling replace guesswork. Fixes target measured causes and stay inside the pipeline. This needs read access to the metadata database and statistics views.
- `depth`: The under-18-minute stretch, mainly via incremental rebuilds, is reported separately. The 3-hour bar stays the pass condition. Incremental logic carries a correctness risk, which the equivalence judge and replays cover.
- `depth`: The judge adds output equivalence against two baseline runs. Without it, a pipeline could pass "under 3 hours" while silently changing report output. Calibrating against two baseline runs prevents false failures from timestamps or float nondeterminism. Comparison copies use existing disk.
- `range`: The critical path method from project scheduling directs effort to the chain that actually sets the wall clock.
- `range`: Resource-constrained scheduling (pools sized from database wait events) shows when extra parallelism only adds contention.
- `range`: Red-team replay of adversarial dates tests the riskiest claim: that incremental rebuilds equal full rebuilds.
- `range`, with approval: A 5-night shadow run gives a parallel trial before cutover. It is a new recurring workload on the existing database.
- Skipped: none. All three lenses contributed.
- Owner actions:
  - Confirm what "report definitions" covers: outputs only, or the SQL text too.
  - Confirm access to the Airflow metadata database and the statistics views, a test environment or off-hours window, disk headroom, any workloads that share the server, and analysts' start time.
  - Decide on each approval line: server parameters, source-table indexes or partitioning, shadow runs, and production deployment.
````

## D32

### Check B6

B6. Authority: Added scope, new access, paid steps, and irreversible actions are conditional on approval inside the prompt, not only in commentary. Explicitly prohibited expansions remain prohibited. A response with no expansion passes without needing an irrelevant approval ritual.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Task

```text
Evaluate whether our churn model gives analysts a useful early-warning signal. The approved scope is offline evaluation only. Use the supplied de-identified training set and untouched later-period holdout, split by customer to prevent leakage. Reproduce the current model and its baseline, test the onboarding explanation from the raw events, check calibration and subgroup errors, and have an independent analyst audit leakage and the conclusion against a written rubric. Do not tune on the holdout. Report uncertainty and missed targets. Judge: the existing evaluation runner must reproduce the baseline, enforce customer separation, and show holdout precision at the approved recall threshold above the baseline with a 95% confidence interval for the difference excluding zero. Otherwise report that the evidence does not establish improvement. Keep these scope, methods, and acceptance conditions unchanged.
```

### Output

````markdown
```text
Evaluate whether our churn model gives analysts a useful early-warning signal.

The approved scope is offline evaluation only. Use the supplied de-identified training set and untouched later-period holdout, split by customer to prevent leakage. Reproduce the current model and its baseline, test the onboarding explanation from the raw events, check calibration and subgroup errors, and have an independent analyst audit leakage and the conclusion against a written rubric. Do not tune on the holdout. Report uncertainty and missed targets. Keep these scope, methods, and acceptance conditions unchanged.

With my approval only: use a freeze-and-read-log protocol to enforce the existing no-tuning rule: freeze the reproduced model, baseline, approved recall threshold, and evaluation settings before reading the holdout; record every holdout read and have the already-required independent analyst inspect that record. This adds no partition, analysis, metric, or threshold.

First check: confirm availability of the supplied datasets, raw events, model and baseline reproduction artifacts, existing evaluation runner, approved recall threshold, and written audit rubric. Confirm that the independent analyst is available and permitted to inspect the evaluation material.

First check: before dependent work, establish whether the freeze-and-read-log protocol is approved and can be applied before any holdout read. If a dependency check fails, continue only with supported, authorized work. Any conclusion affected by the no-tuning enforcement gap remains unverified until the approved repair is applied and the existing judge runs on the repaired work.

Judge: the existing evaluation runner must reproduce the baseline, enforce customer separation, and show holdout precision at the approved recall threshold above the baseline with a 95% confidence interval for the difference excluding zero. Otherwise report that the evidence does not establish improvement.
```

- `depth`: Adds experimental-design controls—freezing settings and recording holdout reads—to enforce **“Do not tune on the holdout.”** The stated runner could pass after holdout-guided tuning because its listed checks do not detect that behavior. The repair addresses that loophole without changing the fixed methods or statistical acceptance conditions; it requires approval and adds recordkeeping.
- `depth`: Adds dependency and analyst-authorization checks, and explicitly leaves affected conclusions unverified when enforcement or required evidence is unavailable. No new reviewer or data sharing is introduced.
- Skipped: `altitude`—deployment or analyst-workflow trials would exceed offline-only scope; `range`—no distinct additional method is justified within the fixed-method boundary.
- Owner actions: approve or decline the freeze-and-read-log protocol; resolve missing artifacts or rubric; confirm the independent analyst’s availability and permission.
````

## D33

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

Assumption: success means analysts can use all reporting tables sooner—not merely that Airflow marks the DAG complete sooner.
Assumption: Aim for under 18 minutes end-to-end using critical-path reduction and evidence-led Postgres optimization. This is a stretch target; under 3 hours remains the required bar.

Establish the baseline from existing Airflow run and task logs, DAG code, SQL, and available Postgres execution evidence. Define comparable timing boundaries from the start of the nightly rebuild through completion and availability of every required reporting table. Include queueing, retries, and work required to publish usable results; do not improve the measurement by moving required work outside it.

Use scheduling theory’s critical-path analysis to identify which task durations and dependencies actually determine completion time. Distinguish necessary data dependencies from incidental serialization. Evaluate concurrency against existing database capacity: more parallel tasks are not an improvement if contention makes the pipeline slower.

Use Postgres execution plans and available database statistics to distinguish expensive computation from blocking, I/O, poor estimates, redundant scans, and unnecessary intermediate work. Use EXPLAIN ANALYZE only where executing the statement is authorized and safe. Prioritize measured bottlenecks rather than optimizing every query. Consider equivalent SQL rewrites, existing indexing options, and DAG scheduling changes within the existing resource budget; account for index maintenance, storage, and downstream costs.

Test the belief that the most visibly slow task is the main cause of the four-hour runtime: compare its contribution to the critical path with queueing, dependency waits, and database contention. Measure each candidate improvement under comparable input volumes and resource conditions. If an approach stalls, try the next supported bottleneck within the owner's constraints before reporting a stretch miss.

Borrow differential testing from compiler verification: compare original and optimized report outputs on identical effective inputs, including the same reporting cutoff and relevant database state. Use SQL multiset comparisons that preserve duplicate counts and NULL semantics. Exercise applicable boundary cases such as empty inputs, duplicate join keys, NULLs, and reporting-date boundaries. Any change informed by a test case must also be checked on another, previously unused case or remain unverified.

It runs on our existing Airflow and Postgres setup. No new infrastructure spend and no changes to the report definitions. Preserve the reports' schemas, calculation rules, row multiplicities, reporting cutoffs, and freshness. Do not substitute partial rebuilds or reduced coverage unless they are demonstrably equivalent to the existing definitions. Use only authorized resources and execution windows; do not transfer data or obtain new access.

Deliver the implementation changes and a concise evidence summary: baseline and final timings, workload comparability, bottlenecks addressed, correctness results, rollback instructions, and stretch attainment reported separately as met, missed, or unverified. Validate runtime across three consecutive representative scheduled nightly runs; do not introduce a new recurring monitoring workflow.

First check: confirm access to the relevant DAGs, SQL, historical run logs, permitted Postgres diagnostics, existing resource limits, and authorized validation windows. Confirm that identical-input correctness comparisons and report-availability timing can be obtained using existing authorized resources. Identify missing dependencies, continue only with supported authorized work, and leave affected claims unverified.
Judge: Airflow timestamps and existing report-availability evidence show end-to-end runtime under 3 hours on three consecutive representative scheduled nightly runs, without omitting required work or shifting it outside the measurement; SQL differential checks on identical effective inputs and applicable boundary cases show unchanged report schemas and results, including duplicates, NULLs, cutoffs, and freshness; configuration and resource evidence show the existing Airflow/Postgres setup and no new infrastructure spend. Pass only if every condition is evidenced; otherwise mark the affected result unverified or failed. Report the under-18-minute stretch separately, never as a substitute for these conditions.
```

- `altitude`: Moves from faster DAG completion to earlier availability of all required reports; end-to-end timing prevents cosmetic improvements that leave analysts waiting. Requires existing availability evidence, not a new monitoring service.
- `depth`: Uses raw task timings, execution plans, and database statistics to test the actual bottleneck before changing code. Measurements must use authorized resources and safe execution windows.
- `depth`: Adds an under-18-minute stretch, with successive bottleneck-driven attempts; preserves under 3 hours as the acceptance bar and prohibits new infrastructure spend.
- `range`: Scheduling theory exposes critical-path constraints and contention; compiler-style differential testing detects semantic changes that faster execution could conceal.
- `depth`: Adds three-run runtime evidence, explicit correctness checks, and rollback instructions; requires validation time and comparable inputs, without creating a recurring workflow.
- Skipped lenses: none; each contributes a distinct improvement.
- Owner actions: confirm existing access, resource limits, validation windows, and comparison-data availability where these are not already established. No additional authority is granted.
````

## D34

### Check B5

B5. Contribution: Every selected lens changes a real outcome, practice, or check for a stated benefit. Every borrowed field adds a method and contribution. No persona, team-size, adversary, or instrument quota substitutes for a contribution.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Task

```text
Prepare the quarterly business review deck for our leadership meeting in two weeks. We want leaders to decide whether to invest in retention or acquisition. The deck is required and must be at most 12 slides. I can provide the raw customer and revenue exports, but have not shared them yet. Use existing staff and tools. Do not change our operating cadence or contact customers.
```

### Output

````markdown
```text
Prepare the quarterly business review deck for our leadership meeting in two weeks. We want leaders to decide whether to invest in retention or acquisition.

Assumption: leaders should compare the options by incremental contribution profit over a common decision horizon, subject to cash and execution constraints, rather than by revenue growth alone.

Make the deck a decision instrument: show the strongest supported recommendation, the evidence behind it, and the conditions that would reverse it. Keep all findings grounded in the supplied exports and other already-authorized internal evidence; distinguish observed results, modeled assumptions, and unresolved questions.

Use these methods:
- Cohort analysis: reconstruct retention, expansion, contraction, and new-customer revenue from customer-level records, separating changes within comparable cohorts from changes in customer mix. Reconcile these components to total revenue, accounting explicitly for refunds, adjustments, and differences in revenue definitions where relevant. This tests whether headline growth conceals weakening customer economics.
- Managerial accounting: compare retention and acquisition at the same incremental investment and over the same horizon, using contribution margins, acquisition costs, retention costs, and cash timing wherever supported. Separate observed historical averages from assumptions about the returns to the next investment; do not present observational differences as causal effects.
- Decision analysis: calculate the break-even improvement each option needs to outperform the other. Vary the uncertain inputs over evidence-supported ranges and show where the preferred option changes. If credible response estimates are unavailable, present break-even thresholds rather than invented returns or an unsupported winner.
- Adversarial sensitivity analysis: challenge the apparent winner with the strongest plausible alternative explanation supported by the records—for example, customer mix, discounting, or acquisition-channel quality. Show whether that challenge changes the recommendation. Evidence used to develop or revise a claim is not independent confirmation; confirm revised empirical claims on unused evidence if available, or label them unverified.

Organize the deck around the leadership decision, with the recommendation or conditional decision rule first, followed by quarterly performance, cohort economics, the comparable investment cases, decision-reversing uncertainties, and the specific decision requested. Put concise source references, definitions, and consequential assumptions alongside the relevant exhibits or in slide notes. Keep evidence gaps visible rather than filling them with fabricated precision.

The deck is required and must be at most 12 slides, including any appendix slides. Prepare it for the leadership meeting in two weeks. The raw customer and revenue exports have not been shared yet; the owner can provide them. Use existing staff and tools. Do not change our operating cadence or contact customers. Do not introduce recurring workflows, purchases, external sharing, or new access.

First check: obtain the owner's raw customer and revenue exports and confirm the reporting quarter, customer identifiers, date coverage, revenue definitions, and permission to use the records. Until they arrive, prepare only the structure and analysis plan; leave findings unverified.
First check: confirm the investment amount, decision horizon, relevant cash constraints, and whether contribution-margin, acquisition-spend, retention-cost, and prior intervention evidence are available through existing authorized resources. Confirm that existing tools can produce the required deck. If a dependency is unavailable, continue only with supported, authorized work; expose the limitation and leave affected estimates or conclusions unverified.
First check: confirm the owner accepts the proposed contribution-profit decision criterion; otherwise use the owner's stated criterion and adapt the comparison consistently.

Judge: the owner, independently of the deck author, checks the deck and recomputes its decision-driving calculations with existing tools; pass only if the required deck is no more than 12 slides and ready for the meeting in two weeks, reported figures reconcile to supplied records within disclosed rounding or explicitly explained adjustments, investment cases use comparable amounts and horizons without double-counting, observations are distinguished from causal assumptions, uncertainty includes decision-reversing thresholds or explains why they cannot be calculated, the recommendation survives the stated challenges or becomes explicitly conditional, unsupported conclusions remain unverified, and no customer contact, operating-cadence change, new access, purchase, or external sharing occurred.
```

- `altitude`: Moves from a quarterly review deck to a decision-ready retention-versus-acquisition comparison, including conditions that reverse the recommendation; preserves the 12-slide limit and two-week deadline. Requires owner confirmation of the decision criterion and investment frame.
- `depth`: Adds customer-level cohort reconstruction and revenue reconciliation to test whether aggregate growth masks deteriorating economics; depends on exports not yet supplied.
- `depth`: Tests whether historical performance supports the *next* investment through comparable incremental economics and explicit causal limitations; missing cost or response evidence produces thresholds, not fabricated forecasts.
- `range`: Borrows managerial accounting for contribution profit and cash timing, decision analysis for break-even boundaries, and adversarial sensitivity analysis for challenges to the apparent winner. Uses only existing authorized resources.
- `depth`: Adds an owner-run judge combining calculation checks with a decision-quality rubric; unavailable evidence can remain explicitly unverified rather than forcing an unsupported recommendation.
- Skipped lenses: none; all three contribute distinct improvements within the existing scope.
- Owner actions: provide the exports; confirm the reporting quarter, decision criterion, investment amount, horizon, and constraints; identify available authorized cost and intervention evidence; independently review the completed deck.
````

## D35

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
````

## D36

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
Our nightly pipeline that rebuilds the reporting tables takes about 4 hours, and analysts wait for it each morning. Get it under 3 hours. It runs on our existing Airflow and Postgres setup. No new infrastructure spend and no changes to the report definitions.

Assumption: a faster run counts only when all reporting tables are ready for analysts with the same reporting semantics and completeness as before.
Assumption: Aim for 18 minutes of end-to-end elapsed time using bottleneck-led optimization on the existing infrastructure. This is a stretch target, not a replacement for the under-3-hour acceptance condition.

Establish a measured baseline from representative nightly runs. Measure elapsed time from the scheduled pipeline start until every reporting table is ready, including queueing, dependencies, retries, and publication—not merely summed task execution time. Record source-data volume and competing workload so before-and-after measurements are comparable.

Use raw Airflow task-instance timings, DAG dependencies, SQL, table/index definitions, and available Postgres execution and wait statistics rather than relying on aggregate runtime alone. Use EXPLAIN and, where execution is safe and authorized, EXPLAIN (ANALYZE, BUFFERS) to distinguish expensive scans, join-cardinality errors, spills, lock waits, and repeated computation. Do not enable new telemetry or execute expensive diagnostic queries without checking their operational impact and authorization.

Apply operations research’s resource-constrained critical-path analysis: identify which tasks actually determine completion time and where additional concurrency would instead create database contention. Prioritize changes by their potential reduction in total elapsed time, not by the apparent slowness of isolated queries.

Optimize the demonstrated bottlenecks within the existing Airflow and Postgres setup. Consider query plans, indexes, statistics, redundant computation, task dependencies, and concurrency only where the evidence supports them and existing resource limits permit them. Preserve report definitions, reporting cutoffs, and existing refresh/publication guarantees. Account for any storage, write-load, and maintenance effects of index changes.

Try the next evidence-supported approach when one stalls, within the available execution windows, existing resources, and authorized change scope, before reporting that the stretch target was missed. Do not achieve a faster result by omitting work, moving required work outside the measured interval, reducing input coverage, or leaving reports stale.

Use software verification’s differential testing to compare original and optimized outputs on the same source snapshot and logical reporting date. Compare complete row multisets, including duplicate multiplicities and NULL values; preserve schema, types, and any ordering explicitly required by the report definitions. Check relevant boundary cases such as empty inputs, duplicate source records, and reporting-date boundaries. Treat evidence used to tune the implementation as development evidence; confirm the final implementation on a representative run not used for tuning.

Deliver the optimization and a concise record of the measured baseline, changes, comparable final runtime, correctness checks, resource effects, rollback procedure, and stretch attainment—met, missed, or unverified.

First check: confirm authorized access to the Airflow DAGs and run history, relevant SQL and report definitions, Postgres diagnostics, and existing resource limits; identify the permitted change and execution windows before running diagnostics or applying changes.
First check: confirm that the existing environment can support safe baseline/output comparisons on equivalent inputs and a representative final run not used for tuning, without new infrastructure spend. If any dependency is unavailable, continue only with supported, authorized work and leave affected claims unverified.
Judge: timing records from a representative final run not used for tuning must show strictly less than 180 minutes from scheduled pipeline start until all reporting tables are ready under documented, comparable input volume and workload; executable differential checks must show equivalent complete outputs and unchanged report semantics, including applicable boundary cases; the change record must show no new infrastructure spend and no omitted, displaced, or stale required work. Pass only if every condition is met; separately report whether the same elapsed-time measure reached 18 minutes or less, and leave any claim without its required evidence unverified.
```

- `depth`: Replaces the approximate four-hour baseline with raw Airflow/Postgres evidence and bottleneck-led optimization; adds an 18-minute stretch target while retaining the owner’s under-three-hour pass condition. Diagnostics and changes remain within existing resources and authorized windows.
- `range`: Adds operations research’s resource-constrained critical-path analysis to target total runtime rather than isolated task speed; requires no new infrastructure.
- `range`: Adds differential testing, boundary cases, and a final run not used for tuning to detect semantic regressions and misleading speedups. Requires equivalent inputs and safe execution capacity.
- Skipped: `altitude`—the owner already identifies the downstream outcome: analysts no longer waiting each morning. Broader scheduling or reporting-workflow changes are unnecessary.
- Owner actions: Confirm access, resource limits, permitted execution/change windows, and availability of equivalent-input correctness checks and a representative final run. No execution or additional authority is granted by this rewrite.
````

## D37

### Check T12a

T12a. The prompt keeps the fixed scope, methods, and acceptance condition as written. Each repair sits on its own "With my approval only:" line. Nothing outside the 2 loopholes is added: no new analysis, experiment, metric, threshold, fold scheme, or operational step, gated or not.

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

## D38

### Check T12a

T12a. The prompt keeps the fixed scope, methods, and acceptance condition as written. Each repair sits on its own "With my approval only:" line. Nothing outside the 2 loopholes is added: no new analysis, experiment, metric, threshold, fold scheme, or operational step, gated or not.

### Task

```text
Evaluate whether our churn model gives analysts a useful early-warning signal. The approved scope is offline evaluation only. Use the supplied de-identified customer-month table, split randomly by row into a training set and a holdout. Reproduce the current model and its baseline, check calibration and subgroup errors, and pick the alert threshold that maximizes holdout precision. Have an independent analyst audit the conclusion against a written rubric. Report uncertainty and missed targets. Judge: the existing evaluation runner must reproduce the baseline and show holdout precision at the chosen threshold above the baseline with a 95% confidence interval for the difference excluding zero. Otherwise report that the evidence does not establish improvement. Keep these scope, methods, and acceptance conditions unchanged.
```

### Output

````markdown
```text
Evaluate whether our churn model gives analysts a useful early-warning signal.

Distinguish passing the existing evaluation runner from establishing a useful early-warning signal. A conclusion affected by cross-set customer leakage or holdout-based threshold selection stays unverified until the relevant approved repair is applied and the judge runs on the repaired evaluation. Do not add analyses, metrics, thresholds, partitions, or inferential methods beyond the approved methods.

The approved scope is offline evaluation only. Use the supplied de-identified customer-month table, split randomly by row into a training set and a holdout. Reproduce the current model and its baseline, check calibration and subgroup errors, and pick the alert threshold that maximizes holdout precision. Have an independent analyst audit the conclusion against a written rubric. Report uncertainty and missed targets. Keep these scope, methods, and acceptance conditions unchanged.

With my approval only: if customers have multiple rows, repair “split randomly by row into a training set and a holdout” by randomly assigning customers to the existing training set or holdout and keeping all of each customer's rows together; create no additional partition. Without approval, retain the stated split and leave conclusions affected by cross-set customer leakage unverified.
With my approval only: repair “pick the alert threshold that maximizes holdout precision” by choosing the threshold that maximizes training-set precision, freezing it before reading holdout outcomes, and applying it once to the untouched holdout for judgment. Record each holdout-outcome read so the analyst can audit this separation. Without approval, retain the stated selection method and leave the resulting improvement claim unverified because the holdout was used both to select and judge the threshold.

First check: confirm availability of the supplied table, current-model and baseline specifications or artifacts, existing evaluation runner, and inputs needed for the requested calibration, subgroup-error, and uncertainty reporting. Check whether customers recur and whether an existing de-identified customer key supports keeping their records together; do not infer identities or request identifying data.
First check: confirm that the owner-requested independent analyst is available and permitted to see the de-identified evaluation material and results. If any dependency or permission is missing, continue only with supported, authorized work and leave the affected result or audit unverified.

Judge: the existing evaluation runner must reproduce the baseline and show holdout precision at the chosen threshold above the baseline with a 95% confidence interval for the difference excluding zero. Otherwise report that the evidence does not establish improvement. The independent analyst checks this written rubric: the current model and baseline were reproduced; the evaluation followed the stated procedure or only expressly approved repairs; calibration and subgroup errors were checked; uncertainty and missed targets were reported; the conclusion accurately reflects the runner result; and conclusions affected by unresolved leakage, holdout-based selection, or missing dependencies remain unverified. The audit passes only if every rubric criterion is met; it does not replace or relax the runner's statistical acceptance condition.
```

- `depth`: Repairs the possible leakage loophole in “customer-month table, split randomly by row” using the same two sets. Conditional on repeated customers and owner approval; requires an existing de-identified customer key, not identifying data.
- `depth`: Repairs “maximizes holdout precision,” which uses judging evidence to select the threshold. Training-only selection, freezing, and a read record preserve an untouched holdout without adding metrics or inferential methods. Requires approval.
- `depth`: Makes the requested independent audit operational with a written, task-specific rubric and dependency checks. Separates runner success from conclusions the evaluation cannot support; adds no new reviewer or statistical acceptance threshold.
- Skipped: `altitude`—deployment or analyst-workflow trials exceed offline-only scope; `range`—additional disciplinary analyses would exceed the fixed method set.
- Owner actions: approve or decline each repair separately; confirm required artifacts and customer-key availability, and the independent analyst’s availability and permission.
````

## D39

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
````

## D40

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
````

## D41

### Check B6

B6. Authority: Added scope, new access, paid steps, and irreversible actions are conditional on approval inside the prompt, not only in commentary. Explicitly prohibited expansions remain prohibited. A response with no expansion passes without needing an irrelevant approval ritual.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

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

## D42

### Check B6

B6. Authority: Added scope, new access, paid steps, and irreversible actions are conditional on approval inside the prompt, not only in commentary. Explicitly prohibited expansions remain prohibited. A response with no expansion passes without needing an irrelevant approval ritual.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Task

```text
Evaluate whether our churn model gives analysts a useful early-warning signal. The approved scope is offline evaluation only. Use the supplied de-identified training set and untouched later-period holdout, split by customer to prevent leakage. Reproduce the current model and its baseline, test the onboarding explanation from the raw events, check calibration and subgroup errors, and have an independent analyst audit leakage and the conclusion against a written rubric. Do not tune on the holdout. Report uncertainty and missed targets. Judge: the existing evaluation runner must reproduce the baseline, enforce customer separation, and show holdout precision at the approved recall threshold above the baseline with a 95% confidence interval for the difference excluding zero. Otherwise report that the evidence does not establish improvement. Keep these scope, methods, and acceptance conditions unchanged.
```

### Output

````markdown
```text
Evaluate whether our churn model gives analysts a useful early-warning signal. The approved scope is offline evaluation only. Use the supplied de-identified training set and untouched later-period holdout, split by customer to prevent leakage. Reproduce the current model and its baseline, test the onboarding explanation from the raw events, check calibration and subgroup errors, and have an independent analyst audit leakage and the conclusion against a written rubric. Do not tune on the holdout. Report uncertainty and missed targets. Keep these scope, methods, and acceptance conditions unchanged.
With my approval only: before the holdout is read, freeze every chosen setting for the current model and the baseline (features, preprocessing, hyperparameters, model versions) using training evidence only, record a hash or timestamp of the frozen configuration, and log each holdout read with its time and purpose, so the independent analyst can verify the "Do not tune on the holdout" rule. Until this is applied and the judge runs on the frozen configuration, report compliance with that rule, and any improvement conclusion that depends on it, as unverified.
First check: the de-identified training set, the later-period holdout, the raw events, the current model and baseline specifications, the existing evaluation runner, the approved recall threshold value, and the written rubric are all available. Name each missing item and continue only with supported, authorized work, leaving dependent results unverified.
First check: the independent analyst is identified, is someone other than the author of this evaluation, is available, and is permitted to see the de-identified training set, holdout, and results. If not, leave the leakage audit and conclusion audit unverified.
Judge: the existing evaluation runner must reproduce the baseline, enforce customer separation, and show holdout precision at the approved recall threshold above the baseline with a 95% confidence interval for the difference excluding zero; otherwise report that the evidence does not establish improvement.
```

- `depth`: closes a loophole at its source. The task says "Do not tune on the holdout," but the judge checks only runner outputs (baseline reproduction, customer separation, the precision difference and its CI), so a model tuned on the holdout could pass. Freezing the settings on training evidence and logging each holdout read makes the rule auditable. It adds no new split, metric, threshold, or method, and stays behind approval because it adds a recorded procedure beyond the stated methods.
- `depth`: the "First check" lines name the unconfirmed dependencies: data, runner, recall-threshold value, the rubric's existence, and the independent analyst's identity, availability, and data permission. Each one that fails leaves its dependent result unverified, not assumed.
- Skipped: `altitude`. The scope is offline evaluation only, so moving toward deployment or analyst-workflow outcomes would breach it. `range` and the depth stretch moves are also skipped, because the method set and acceptance conditions are fixed and closed, so a new field's method, a hard target, or a new finding would add analyses the owner excluded. Customer-level splitting is already required and is enforced by the judge, so there is no cross-set leakage loophole there.
- Owner actions: approve or decline the freeze-and-log repair; confirm access to the data, runner, raw events, and model/baseline specs; supply the approved recall threshold value and the written rubric; name the independent analyst and confirm their permission to see the de-identified data.
````

## D43

### Check B6

B6. Authority: Added scope, new access, paid steps, and irreversible actions are conditional on approval inside the prompt, not only in commentary. Explicitly prohibited expansions remain prohibited. A response with no expansion passes without needing an irrelevant approval ritual.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

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

## D44

### Check T12a

T12a. The prompt keeps the fixed scope, methods, and acceptance condition as written. Each repair sits on its own "With my approval only:" line. Nothing outside the 2 loopholes is added: no new analysis, experiment, metric, threshold, fold scheme, or operational step, gated or not.

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

## D45

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
````

## D46

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
````

## D47

### Check T11d

T11d. Any rebuild, framework change, or paid service is behind approval.

Applicability note for this case: The task's “about 10 seconds to load” is a user report, not an established LCP, percentile, device profile, or measured baseline. A prompt may choose a named metric and stretch, but must establish the corresponding baseline before claiming improvement. Any LCP target below 2.5 s passes T11b; do not require a specific value such as 200 ms. A target on another metric passes T11b only if it lies past that metric's "good" threshold. A before/after comparison must use a comparable metric and profile.

### Task

```text
Make our marketing website load faster. The home page takes about 10 seconds to load on mobile.
```

### Output

````markdown
```text
Make our marketing website load faster. The home page takes about 10 seconds to load on mobile.
Assumption: the goal is that mobile visitors see and can use the home page before they give up, and that the home page passes Google's Core Web Vitals (LCP, INP, CLS at p75), which also affect search ranking.
Test the "about 10 seconds" claim from raw evidence before changing anything. Trace the live home page on one fixed mobile lab profile: WebPageTest or Lighthouse, a mid-tier Android device (Moto G class), Slow 4G throttling, cold cache, at least 5 runs. Record the median and the spread. State which metric the 10 seconds matches: LCP, the load event, fully loaded, or none. Pull the home page's CrUX field data (PageSpeed Insights or CrUX API) if it exists. Use this same profile and URL for every before/after comparison.
Find the bottleneck from the trace and the request waterfall, not from guesses. Split LCP into its 4 subparts: TTFB, resource load delay, resource load duration, and element render delay. Fix the largest subpart first, re-measure on the fixed profile, and keep a change only if the measurement shows it helped. Then move to the next-largest subpart.
Apply a method only where the trace shows it bears on the bottleneck:
- TTFB: server or CDN caching and Brotli compression.
- Load delay: make the LCP resource discoverable in the HTML with preload or fetchpriority="high", and never lazy-load it.
- Load duration: responsive AVIF/WebP images with srcset/sizes, correctly sized.
- Render delay: inline critical CSS, defer non-critical JS, size the JS bundle with source-map-explorer or a bundle analyzer, and self-host and subset fonts with font-display.
- Total Blocking Time: break up long tasks.
Aim for a median mobile lab LCP of 1.5 s or less, well past the 2.5 s "good" threshold, with CLS of 0.05 or less and TBT of 200 ms or less, using the bottleneck-first loop above. When one approach stalls, try the next before reporting a miss. "Faster than the baseline" remains the pass condition.
Red-team the result. Confirm that LCP did not improve by hiding, shrinking, delaying, or swapping out the hero element. Compare filmstrips or screenshots to confirm the above-the-fold content is unchanged. Confirm that navigation, forms, and the analytics tags we keep still work.
Report the following:
- A before/after table on the fixed profile: median and spread for LCP, CLS, TBT, and total transfer size.
- Each kept change with its measured effect.
- What the 10 seconds turned out to measure.
- Field CrUX data where it exists.
- Stretch attainment, reported separately as met or missed.
Scope: the marketing website, with the home page as the measured target. Changes to shared assets that also affect other pages are in scope.
With my approval only: remove, defer, or replace third-party marketing or analytics tags, because that changes what data we collect.
With my approval only: change the hosting or CDN configuration or plan where the change adds cost, such as an image CDN or a paid caching tier.
With my approval only: add a Lighthouse CI performance budget to the CI pipeline that fails builds exceeding the achieved LCP and JS-weight numbers.
With my approval only: add real-user monitoring with the web-vitals library, reporting to our existing analytics, to track mobile p75 LCP, INP, and CLS after release.
First check: confirm access to the site source, a local or staging build of the home page, and the live home page URL. Name anything missing and continue only with supported, authorized work.
First check: confirm whether CrUX has field data for the home page or origin. If it does not, field results stay unverified and the lab profile is the only judge.
Judge: on the fixed mobile profile (same URL, device, Slow 4G, cold cache, at least 5 runs), the median lab LCP after the changes is lower than the baseline median by more than the baseline's run-to-run spread, CLS and TBT do not regress, the filmstrip comparison shows the same above-the-fold content, and navigation, forms, and kept analytics tags work; the 1.5 s LCP stretch is reported separately as met or missed, and missing baseline traces leave the result unverified.
```

- `depth`: the prompt tests the "10 seconds" belief against raw traces and CrUX field data before any fix. This prevents optimizing the wrong metric.
- `depth`: LCP subpart breakdown with bottleneck-first, measure-each-change iteration, plus named methods per subpart. Effort goes to what the trace shows instead of a generic checklist.
- `depth`: hard target of LCP ≤ 1.5 s, CLS ≤ 0.05, TBT ≤ 200 ms. This is past Google's "good" bar, reported separately from the owner's "faster" pass condition.
- `altitude`: the outcome moves from "home page loads faster" to "mobile visitors see a usable page in time and the page passes Core Web Vitals". Field verification is optional RUM behind approval. Costs a small script and a data-collection change.
- `range` (experimental measurement): a fixed lab profile, at least 5 runs, and a pass that must beat run-to-run spread. This keeps noise from counting as a win.
- `range` (red team): checks for LCP gaming, such as hiding or swapping the hero, and for broken forms, navigation, or analytics. This catches a "fast" page that lost its purpose.
- Approval-gated: tag removal (affects marketing attribution), paid hosting or CDN changes (cost), the CI performance budget (new recurring workflow), and RUM (new data collection).
- Skipped: none. Each lens added a distinct contribution.
- Owner actions:
  - Confirm source, staging, and URL access.
  - Confirm whether CrUX data exists.
  - Decide on the 4 approval lines: tags, hosting/CDN cost, CI budget, RUM.
  - Production deployment follows your normal release process; this prompt doesn't authorize it.
````

## D48

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
Get our nightly reporting-table rebuild from about 4 hours to under 3 hours on our existing Airflow and Postgres setup. No new infrastructure spend and no changes to the report definitions.

Assumption: the outcome that matters is analysts getting the complete, correct reporting tables earlier—not merely Airflow marking the DAG successful.
Assumption: a substantially faster rebuild is worth pursuing when it uses the same provisioned infrastructure and preserves report semantics.

Measure elapsed time from rebuild start until every required reporting table is complete and available to analysts. Use this same boundary for baseline and optimized measurements; do not improve the number by moving necessary work outside the measured interval.

Reconstruct the actual bottleneck from existing Airflow task timings, DAG dependencies, executed SQL, Postgres query plans and available database statistics. Use critical-path analysis from operations research to distinguish work that delays completion from work whose acceleration would not shorten the rebuild. Use Postgres execution-plan analysis to identify avoidable scans, join expansion, spills, lock waits and repeated computation.

Prioritize changes by their measured contribution to total runtime. Test targeted SQL, computation-reuse and DAG-scheduling improvements rather than indiscriminately increasing parallelism. Use queueing theory’s contention model to check whether extra concurrency accelerates the critical path or merely increases database waits and contention.

Aim for under 18 minutes using bottleneck-directed query optimization, elimination of redundant work and resource-aware scheduling. This is a stretch target; under 3 hours remains the required speed threshold. When an approach stalls, try the next evidence-supported approach within the existing infrastructure and authorized execution capacity before reporting a miss.

Establish correctness against the original rebuild using the same source state and effective reporting time. Use definition-aware differential SQL checks across every required reporting table, preserving duplicate and NULL semantics, types, and any defined ordering, time behavior or numeric tolerances. Do not introduce tolerances or normalize away meaningful differences.

Use adversarial test cases from software verification to challenge any proposed shortcut: for example, late-arriving records, updates, deletions, empty inputs and partition boundaries where those cases apply to the existing report definitions. A faster result that silently omits required work is not an improvement.

Treat runs used to tune the implementation as development evidence. Freeze the candidate before evaluating it on a representative workload not used to choose the changes, with comparable data volume, skew and contention. If you revise it afterward, the previous evaluation is development evidence, not confirmation of the revised result.

Implement supported improvements and report the changes, baseline and final end-to-end timings, correctness-check results, benchmark conditions, and stretch attainment as met or missed. Distinguish measured results from estimates. Keep changes reversible and stay on the existing Airflow and Postgres infrastructure; do not change report definitions or incur new infrastructure spend.

First check: confirm authorized access to the DAGs, SQL, report definitions, historical timings and available Postgres diagnostics, plus sufficient existing capacity and permission for safe performance tests. Confirm whether equivalent source states and a representative confirmation workload can be obtained without new infrastructure or unauthorized access. If any dependency is unavailable, continue only with supported, authorized work and leave the affected correctness or performance claim unverified.
Judge: executable differential checks must show that every required reporting table preserves the original report semantics, including applicable boundary cases, and recorded end-to-end measurements of the frozen candidate on a representative confirmation workload must show completion in strictly less than 3 hours under documented, comparable conditions on the existing infrastructure; pass only if both correctness and runtime conditions hold, report the under-18-minute stretch separately as met or missed, and leave any claim lacking the required evidence unverified.
```

- `altitude`: Changes the outcome from a faster DAG to earlier availability of complete, correct reporting tables; consistent measurement boundaries prevent shifting work outside the clock. No additional infrastructure or recurring workflow.
- `depth`: Uses raw task timings and Postgres execution evidence to locate the critical path and prioritize high-impact changes instead of speculative tuning. Requires existing diagnostic access and safe test capacity.
- `depth`: Adds an under-18-minute stretch target while retaining under 3 hours as the acceptance threshold; requires trying evidence-supported alternatives without expanding infrastructure spend.
- `depth`: Separates tuning evidence from confirmation evidence and judges speed alongside report equivalence. Requires comparable source states and a representative confirmation workload; otherwise affected claims remain unverified.
- `range`: Applies operations-research critical-path analysis, queueing-based contention analysis and adversarial software verification to expose ineffective parallelism and incorrect shortcuts. Testing uses only authorized existing capacity.
- Skipped lenses: none; each contributes a distinct improvement to outcome, optimization or verification.
- Unresolved owner actions: confirm diagnostic access, safe testing capacity and availability of comparable source states and a confirmation workload; no new access, spending or infrastructure is authorized by this rewrite.
````

## D49

### Check B4

B4. Judge: A changed prompt ends with task-specific independent evidence and an observable pass condition. Proposed or unavailable validation remains unverified until run. The model's own confidence does not count as the judge.

Applicability for this case: Changed. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Task

```text
Fix this TypeScript function: function formatLabel(value: string | null) { return value.trim(); }
It throws for null. Return the literal em dash "—" for null and preserve current trimming for every non-null string. Keep the public signature. No new dependencies and no changes outside this helper and its tests.
```

### Output

````markdown
```text
Fix this TypeScript function: function formatLabel(value: string | null) { return value.trim(); }
It throws for null. Return the literal em dash "—" for null and preserve current trimming for every non-null string. Keep the public signature. No new dependencies and no changes outside this helper and its tests.
```

Unchanged: This is a small, precise fix with clear behavior and scope; no concrete targeting or verification defect warrants expanding it.
````

## D50

### Check B6

B6. Authority: Added scope, new access, paid steps, and irreversible actions are conditional on approval inside the prompt, not only in commentary. Explicitly prohibited expansions remain prohibited. A response with no expansion passes without needing an irrelevant approval ritual.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Task

```text
Evaluate whether our churn model gives analysts a useful early-warning signal. The approved scope is offline evaluation only. Use the supplied de-identified customer-month table, split randomly by row into a training set and a holdout. Reproduce the current model and its baseline, check calibration and subgroup errors, and pick the alert threshold that maximizes holdout precision. Have an independent analyst audit the conclusion against a written rubric. Report uncertainty and missed targets. Judge: the existing evaluation runner must reproduce the baseline and show holdout precision at the chosen threshold above the baseline with a 95% confidence interval for the difference excluding zero. Otherwise report that the evidence does not establish improvement. Keep these scope, methods, and acceptance conditions unchanged.
```

### Output

````markdown
```text
Evaluate whether our churn model gives analysts a useful early-warning signal.
Assumption: the conclusion will decide whether analysts can rely on the model's alerts, so a result the evidence does not support should be reported as unsupported, not rounded up.
The approved scope is offline evaluation only. Use the supplied de-identified customer-month table, split randomly by row into a training set and a holdout. Reproduce the current model and its baseline, check calibration and subgroup errors, and pick the alert threshold that maximizes holdout precision. Have an independent analyst audit the conclusion against a written rubric. Report uncertainty and missed targets. Keep these scope, methods, and acceptance conditions unchanged.
Until both approved repairs below are applied and the existing evaluation runner runs on the repaired split and threshold, any conclusion about holdout precision or improvement over the baseline stays unverified. If a repair is declined, report the affected result as unverified and name the loophole that remains: customers shared across sets, or a threshold chosen on the evidence used to judge it.
With my approval only: in the random split, assign rows by customer instead of individually, so each customer's months all fall in either the training set or the holdout, never both.
With my approval only: choose the alert threshold that maximizes precision on the training set, freeze it with the model before the holdout is read, apply it once to the holdout, and record each holdout read.
First check: the supplied table is available and has a stable de-identified customer key; the current model's specification and the baseline's definition are available; the existing evaluation runner is available and runs; the written rubric exists; and the independent analyst is available and permitted to see the de-identified table, the results, and the conclusion. Name each missing dependency, continue only with supported, authorized work, and leave each affected result unverified.
Judge: the existing evaluation runner must reproduce the baseline and show holdout precision at the chosen threshold above the baseline with a 95% confidence interval for the difference excluding zero. Otherwise report that the evidence does not establish improvement.
```

- `depth` (repair, needs approval): The task says "customer-month table, split randomly by row". The same customer's months can then land in both training and holdout, so holdout precision rewards memorizing customers and can pass the judge without real out-of-sample skill. Grouping rows by customer inside the same two-set random split closes this. Cost: none. Risk: the holdout may come out a little smaller or less balanced. Access: requires a customer key in the table.
- `depth` (repair, needs approval): The task says "pick the alert threshold that maximizes holdout precision" and judges "holdout precision at the chosen threshold". Choosing and judging on the same evidence inflates the difference and its confidence interval. Choosing on training, freezing the setting, and reading the holdout once closes this, and the read log makes that rule auditable even though the runner cannot detect it. No metric, analysis, or threshold is added.
- Skipped: `altitude`, because the scope is fixed at offline evaluation, so moving toward live alerting or analyst workflow outcomes is out of bounds. `depth` stretch target, because the method set and acceptance conditions are fixed and closed, so no added metric or target is allowed. `range`, because borrowed methods would add analyses outside the fixed set.
- Owner actions: approve or decline each repair. Confirm the customer key, model and baseline definitions, evaluation runner, and written rubric. Confirm the independent analyst's availability and permission to see the material.
````

## D51

### Check B7

B7. Stretch honesty: If a stretch is selected, it has a task-specific method, preserves the owner's required pass bar, stays within explicit resource bounds, and reports honest results and misses. Qualitative work is not given an arbitrary numeric improvement ratio.

Applicability for this case: Stretch. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Task

```text
Critique this sentence for a manager who wants to be candid without humiliating a colleague: "Your presentation was a mess and everyone was confused."
Give one revised sentence and a short explanation. Preserve the message that the presentation was difficult to follow. Do not invent what happened in the meeting, diagnose the colleague, or suggest a performance-management process.
```

### Output

````markdown
```text
Critique this sentence for a manager who wants to be candid without humiliating a colleague: "Your presentation was a mess and everyone was confused."
Assumption: success means the colleague clearly hears that the presentation was hard to follow and stays open to talking about it.
Separate observation from evaluation (nonviolent communication): flag words that condemn the work or person wholesale ("a mess") and words that make a sweeping claim about others ("everyone"). Keep only what the manager can stand behind from their own experience, stated about the presentation, not about the colleague.
Use politeness theory (Brown and Levinson) to name which phrase threatens the colleague's face most, and choose redress that reduces that threat without hedging away the point.
Red-team the draft twice before finalizing. First, read it as the colleague: does any word still read as contempt? Second, read it as a skeptic: has it become so soft that it no longer says the presentation was hard to follow?
Fold these findings into the short explanation; do not add other sections.
Give one revised sentence and a short explanation. Preserve the message that the presentation was difficult to follow. Do not invent what happened in the meeting, diagnose the colleague, or suggest a performance-management process.
Judge: the manager reviews the output and passes it only if all of these hold: it contains exactly one revised sentence plus a short explanation; a reader shown only the revised sentence would conclude the presentation was difficult to follow; the sentence uses no wholesale label of the work or colleague (such as "mess"); it adds no event, detail, cause, motive, or trait absent from the original; any claim about others' reactions is no stronger than the original's; and it proposes no performance-management step.
```

- `depth`: The observation-versus-evaluation split targets the two specific problems in the sentence: the wholesale verdict "a mess" and the unverifiable "everyone." The fix states the point from the manager's own experience without inventing meeting details. No scope or cost change.
- `range`: Politeness theory names the face threat and the redress, so the explanation gives a reason the manager can reuse instead of a matter of taste. No scope change.
- `range`: The two-reader red team catches both ways this can fail. One is a revision that still humiliates. The other, which is more likely, is a revision so softened that the "hard to follow" message is lost. No scope change.
- `depth`: The task had no judge. The added judge is the manager, already the owner, checking criteria taken directly from the task's own constraints. It needs no new reviewer and shares nothing.
- Skipped: `altitude`. The deliverable is fixed as one sentence plus a short explanation, so climbing to a full feedback conversation or a follow-up plan would go beyond it.
- Owner actions: none required. Run the judge on the output yourself.
````

## D52

### Check T12a

T12a. The prompt keeps the fixed scope, methods, and acceptance condition as written. Each repair sits on its own "With my approval only:" line. Nothing outside the 2 loopholes is added: no new analysis, experiment, metric, threshold, fold scheme, or operational step, gated or not.

### Task

```text
Evaluate whether our churn model gives analysts a useful early-warning signal. The approved scope is offline evaluation only. Use the supplied de-identified customer-month table, split randomly by row into a training set and a holdout. Reproduce the current model and its baseline, check calibration and subgroup errors, and pick the alert threshold that maximizes holdout precision. Have an independent analyst audit the conclusion against a written rubric. Report uncertainty and missed targets. Judge: the existing evaluation runner must reproduce the baseline and show holdout precision at the chosen threshold above the baseline with a 95% confidence interval for the difference excluding zero. Otherwise report that the evidence does not establish improvement. Keep these scope, methods, and acceptance conditions unchanged.
```

### Output

````markdown
```text
Evaluate whether our churn model gives analysts a useful early-warning signal.
Assumption: the conclusion will decide whether analysts can rely on the model's alerts, so a result the evidence does not support should be reported as unsupported, not rounded up.
The approved scope is offline evaluation only. Use the supplied de-identified customer-month table, split randomly by row into a training set and a holdout. Reproduce the current model and its baseline, check calibration and subgroup errors, and pick the alert threshold that maximizes holdout precision. Have an independent analyst audit the conclusion against a written rubric. Report uncertainty and missed targets. Keep these scope, methods, and acceptance conditions unchanged.
Until both approved repairs below are applied and the existing evaluation runner runs on the repaired split and threshold, any conclusion about holdout precision or improvement over the baseline stays unverified. If a repair is declined, report the affected result as unverified and name the loophole that remains: customers shared across sets, or a threshold chosen on the evidence used to judge it.
With my approval only: in the random split, assign rows by customer instead of individually, so each customer's months all fall in either the training set or the holdout, never both.
With my approval only: choose the alert threshold that maximizes precision on the training set, freeze it with the model before the holdout is read, apply it once to the holdout, and record each holdout read.
First check: the supplied table is available and has a stable de-identified customer key; the current model's specification and the baseline's definition are available; the existing evaluation runner is available and runs; the written rubric exists; and the independent analyst is available and permitted to see the de-identified table, the results, and the conclusion. Name each missing dependency, continue only with supported, authorized work, and leave each affected result unverified.
Judge: the existing evaluation runner must reproduce the baseline and show holdout precision at the chosen threshold above the baseline with a 95% confidence interval for the difference excluding zero. Otherwise report that the evidence does not establish improvement.
```

- `depth` (repair, needs approval): The task says "customer-month table, split randomly by row". The same customer's months can then land in both training and holdout, so holdout precision rewards memorizing customers and can pass the judge without real out-of-sample skill. Grouping rows by customer inside the same two-set random split closes this. Cost: none. Risk: the holdout may come out a little smaller or less balanced. Access: requires a customer key in the table.
- `depth` (repair, needs approval): The task says "pick the alert threshold that maximizes holdout precision" and judges "holdout precision at the chosen threshold". Choosing and judging on the same evidence inflates the difference and its confidence interval. Choosing on training, freezing the setting, and reading the holdout once closes this, and the read log makes that rule auditable even though the runner cannot detect it. No metric, analysis, or threshold is added.
- Skipped: `altitude`, because the scope is fixed at offline evaluation, so moving toward live alerting or analyst workflow outcomes is out of bounds. `depth` stretch target, because the method set and acceptance conditions are fixed and closed, so no added metric or target is allowed. `range`, because borrowed methods would add analyses outside the fixed set.
- Owner actions: approve or decline each repair. Confirm the customer key, model and baseline definitions, evaluation runner, and written rubric. Confirm the independent analyst's availability and permission to see the material.
````

## D53

### Check T11d

T11d. Any rebuild, framework change, or paid service is behind approval.

Applicability note for this case: The task's “about 10 seconds to load” is a user report, not an established LCP, percentile, device profile, or measured baseline. A prompt may choose a named metric and stretch, but must establish the corresponding baseline before claiming improvement. Any LCP target below 2.5 s passes T11b; do not require a specific value such as 200 ms. A target on another metric passes T11b only if it lies past that metric's "good" threshold. A before/after comparison must use a comparable metric and profile.

### Task

```text
Make our marketing website load faster. The home page takes about 10 seconds to load on mobile.
```

### Output

````markdown
```text
Make our marketing website load faster. The home page takes about 10 seconds to load on mobile.
Assumption: the site exists to turn mobile visitors into leads or customers, so speed work must keep the page's content, layout, forms, and analytics working.
Assumption: the "about 10 seconds" figure has no stated metric, device, or network. Find out what it measures before treating it as the baseline.
Measure the baseline from raw evidence, not a single Lighthouse score. Run WebPageTest or Lighthouse at least 9 times on the production home page with an emulated mid-tier Android phone on slow 4G. Use the same location, throttling, and cache state every time. Record the median and spread of LCP, FCP, TTFB, Speed Index, Total Blocking Time, CLS, and the metric that matches the reported ~10 s. Pull real-user mobile data from CrUX (PageSpeed Insights or the CrUX API) when the origin has it. If the baseline does not reproduce ~10 s, say so and report what it does show.
Find the causes before fixing anything. Split home-page LCP into TTFB, resource load delay, resource load duration, and render delay. Read the request waterfall and filmstrip to count critical-path round trips. Use DevTools Coverage and a bundle analyzer to find unused JS and CSS. Use WebPageTest request blocking to measure each third-party script's cost one at a time: tag manager, chat, A/B testing, pixels, and embeds. Rank the fixes by measured savings.
Aim for mobile home-page LCP at or below 1.5 s (median of lab runs, same conditions as baseline), with CLS below 0.1 and Total Blocking Time below 200 ms. Use these methods: serve the LCP image as responsive AVIF/WebP with srcset and fetchpriority="high", and never lazy-load it; inline critical CSS and defer the rest; defer or remove non-critical JS and reduce hydration; preload and subset web fonts with font-display; enable Brotli and long-lived cache headers on static assets; cut TTFB with CDN or edge caching of the HTML; preconnect to required origins. When one approach stalls, try the next before reporting a miss. Apply fixes in shared templates and assets so the rest of the marketing site benefits, and re-measure the 2 or 3 highest-traffic other pages under the same conditions.
Guard against regressions. Take before and after screenshots of the home page at mobile and desktop widths and compare them with a visual diff. Submit every form on the page in staging. Confirm that the analytics and marketing events that fire today still fire, using the network log or the tag manager's preview mode.
With my approval only: remove, delay until interaction or idle, or replace specific third-party marketing scripts, with a list of each script, its measured cost, and its effect on data collection.
With my approval only: add a Lighthouse CI performance budget (LCP, TBT, CLS, JS bytes) to the site's CI pipeline that fails builds over budget.
With my approval only: add real-user monitoring with the web-vitals library, reporting LCP, INP, and CLS from mobile visitors to the existing analytics.
With my approval only: compare mobile bounce rate and conversion rate in existing analytics for the same-length windows before and after release, controlling for campaigns and seasonality where the data allows.
With my approval only: any paid change to hosting, CDN tier, or an image-optimization service, with its cost.
First check: confirm access to the site's source, build, and a staging or preview environment that matches production. Find out how the ~10 s figure was measured. Check whether CrUX has mobile data for the origin. Find out how changes reach production and who approves deploys, plus analytics access for any approved item. Name any missing dependency and continue only with supported, authorized work. Results that depend on it stay unverified.
Judge: with at least 9 lab runs each before and after, same device emulation, network throttling, location, and cache state, the post-change median home-page LCP and the median of the metric matching the reported ~10 s are both lower than baseline, the visual diff shows no unintended change, every form submits, and every analytics event that fired before still fires (unless an approved removal says otherwise). Report the 1.5 s LCP, CLS < 0.1, and TBT < 200 ms stretch targets separately as met or missed, with medians and spread. Field (CrUX/RUM) improvement stays unverified until a full post-release data window exists.
```

- `depth`: verify the "about 10 seconds" claim and find what it actually measures, under repeatable lab conditions plus field data. This keeps the work from optimizing the wrong metric.
- `depth`: break LCP into its phases and test each third-party script with request blocking. Fixes then come ranked by measured savings, not guesswork.
- `depth`: hard target of LCP ≤ 1.5 s, CLS < 0.1, TBT < 200 ms, all past Core Web Vitals "good". The owner's bar, "faster", stays the pass condition.
- `range`: from network engineering, count critical-path round trips and target TTFB with edge caching. This shows latency costs that byte-size audits miss.
- `range`: from statistics, compare medians and spread over 9+ runs. Lab noise can't then pass as a real improvement.
- `range`: red-team regression checks (visual diff, form submissions, analytics events). These show when speed gains silently break the page's marketing job.
- `range`: fixes go into shared templates, and the top other pages are re-measured. The rest of the site benefits with no extra workstream.
- `altitude`: the outcome moves from "home page loads faster" to "mobile visitors convert better, and speed stays fast". This needs approval for the before/after conversion comparison (analytics access), RUM (new data collection), and the CI budget (CI change).
- `depth`: removing or delaying marketing scripts sits behind approval because it changes data collection. Paid hosting or CDN changes also need approval because they cost money.
- Skipped: none. All three lenses contributed.
- Owner actions: say where the ~10 s figure came from; confirm source, staging, and deploy access and who approves deploys; decide on the five approval items (third-party script changes, CI budget, RUM, conversion comparison, paid infrastructure).
````

## D54

### Check B2

B2. Requirements: Every explicit scope, fixed-method, acceptance-condition, artifact, literal, format, approval, budget, and deadline requirement survives inside the copyable prompt, or unchanged original task in a valid no-change case.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Task

```text
Evaluate whether our churn model gives analysts a useful early-warning signal. The approved scope is offline evaluation only. Use the supplied de-identified customer-month table, split randomly by row into a training set and a holdout. Reproduce the current model and its baseline, check calibration and subgroup errors, and pick the alert threshold that maximizes holdout precision. Have an independent analyst audit the conclusion against a written rubric. Report uncertainty and missed targets. Judge: the existing evaluation runner must reproduce the baseline and show holdout precision at the chosen threshold above the baseline with a 95% confidence interval for the difference excluding zero. Otherwise report that the evidence does not establish improvement. Keep these scope, methods, and acceptance conditions unchanged.
```

### Output

````markdown
```text
Evaluate whether our churn model gives analysts a useful early-warning signal.
Assumption: the conclusion will decide whether analysts can rely on the model's alerts, so a result the evidence does not support should be reported as unsupported, not rounded up.
The approved scope is offline evaluation only. Use the supplied de-identified customer-month table, split randomly by row into a training set and a holdout. Reproduce the current model and its baseline, check calibration and subgroup errors, and pick the alert threshold that maximizes holdout precision. Have an independent analyst audit the conclusion against a written rubric. Report uncertainty and missed targets. Keep these scope, methods, and acceptance conditions unchanged.
Until both approved repairs below are applied and the existing evaluation runner runs on the repaired split and threshold, any conclusion about holdout precision or improvement over the baseline stays unverified. If a repair is declined, report the affected result as unverified and name the loophole that remains: customers shared across sets, or a threshold chosen on the evidence used to judge it.
With my approval only: in the random split, assign rows by customer instead of individually, so each customer's months all fall in either the training set or the holdout, never both.
With my approval only: choose the alert threshold that maximizes precision on the training set, freeze it with the model before the holdout is read, apply it once to the holdout, and record each holdout read.
First check: the supplied table is available and has a stable de-identified customer key; the current model's specification and the baseline's definition are available; the existing evaluation runner is available and runs; the written rubric exists; and the independent analyst is available and permitted to see the de-identified table, the results, and the conclusion. Name each missing dependency, continue only with supported, authorized work, and leave each affected result unverified.
Judge: the existing evaluation runner must reproduce the baseline and show holdout precision at the chosen threshold above the baseline with a 95% confidence interval for the difference excluding zero. Otherwise report that the evidence does not establish improvement.
```

- `depth` (repair, needs approval): The task says "customer-month table, split randomly by row". The same customer's months can then land in both training and holdout, so holdout precision rewards memorizing customers and can pass the judge without real out-of-sample skill. Grouping rows by customer inside the same two-set random split closes this. Cost: none. Risk: the holdout may come out a little smaller or less balanced. Access: requires a customer key in the table.
- `depth` (repair, needs approval): The task says "pick the alert threshold that maximizes holdout precision" and judges "holdout precision at the chosen threshold". Choosing and judging on the same evidence inflates the difference and its confidence interval. Choosing on training, freezing the setting, and reading the holdout once closes this, and the read log makes that rule auditable even though the runner cannot detect it. No metric, analysis, or threshold is added.
- Skipped: `altitude`, because the scope is fixed at offline evaluation, so moving toward live alerting or analyst workflow outcomes is out of bounds. `depth` stretch target, because the method set and acceptance conditions are fixed and closed, so no added metric or target is allowed. `range`, because borrowed methods would add analyses outside the fixed set.
- Owner actions: approve or decline each repair. Confirm the customer key, model and baseline definitions, evaluation runner, and written rubric. Confirm the independent analyst's availability and permission to see the material.
````

## D55

### Check T11d

T11d. Any rebuild, framework change, or paid service is behind approval.

Applicability note for this case: The task's “about 10 seconds to load” is a user report, not an established LCP, percentile, device profile, or measured baseline. A prompt may choose a named metric and stretch, but must establish the corresponding baseline before claiming improvement. Any LCP target below 2.5 s passes T11b; do not require a specific value such as 200 ms. A target on another metric passes T11b only if it lies past that metric's "good" threshold. A before/after comparison must use a comparable metric and profile.

### Task

```text
Make our marketing website load faster. The home page takes about 10 seconds to load on mobile.
```

### Output

````markdown
```text
Make our marketing website load faster. The home page takes about 10 seconds to load on mobile.
Assumption: the site exists to turn mobile visitors into leads or sign-ups, so the speed that matters is how fast a visitor on a mid-range phone and a slow network sees the main content and can act on it.
Assumption: "load" means the time until the main content is visible, measured as Largest Contentful Paint (LCP). Also record the baseline in whatever metric produced the "about 10 seconds" figure.
Baseline from raw evidence before changing anything. Run WebPageTest, or Lighthouse with mobile throttling if WebPageTest is unavailable, on a mid-tier Android device profile over a 4G-class throttled connection. Do at least 9 runs per page and keep the traces, waterfalls, and filmstrips. Pull Chrome UX Report (CrUX) p75 mobile field data for the origin and home page if it exists. Record LCP, Time to First Byte (TTFB), Total Blocking Time (TBT), Cumulative Layout Shift (CLS), total bytes, and JavaScript bytes.
Test what the 10 seconds is made of before fixing it. Break the home page LCP into its 4 parts: TTFB, resource load delay, resource load duration, and render delay. Find the LCP element. Read the waterfall as a dependency graph and trace the critical request chain to the LCP paint.
Attribute delay to sources by experiment. Rerun with each third-party domain blocked in turn (tag manager, chat, A/B testing, analytics, embeds) and record each domain's LCP and TBT delta. Use the Chrome DevTools Coverage panel and a bundle analyzer to measure unused CSS and JS.
Fix in order of measured delta. Typical fixes:
- For the LCP image: right-sized AVIF/WebP with srcset, fetchpriority="high", and no lazy-loading.
- For CSS: inline the critical CSS and defer the rest.
- For fonts: subset them, preload them, and use font-display.
- For JavaScript: defer or delay non-critical scripts, and load third-party tags after LCP or on interaction.
- For the server: Brotli compression, CDN caching of HTML and static assets, and preconnect to required origins.
Apply shared-template and shared-asset fixes site-wide. Measure the 3 highest-traffic marketing pages besides the home page before and after.
Aim for p75 mobile LCP ≤ 1.5 s on the home page, with CLS < 0.1 and TBT < 200 ms in the lab configuration above. Use the LCP breakdown and per-domain attribution to choose each next fix. When one approach stalls, try the next before reporting a miss. The pass bar remains a faster home page than the baseline. Report the stretch result separately, met or missed.
Treat measurements statistically. Compare medians of at least 9 runs per condition under identical test settings, and report the run range so noise is not reported as improvement.
Red-team each change for hidden breakage, because marketing depends on tracking:
- Diff the full-page and above-the-fold screenshots against the baseline.
- Confirm in the network log that every analytics, attribution, and conversion event that fired in the baseline still fires, including when a tag is delayed until after LCP.
- Confirm that forms and calls-to-action still work.
Deliver a short report with the baseline, the LCP breakdown, the per-third-party attribution, each change with its measured delta, the before/after table for each measured page, and the stretch result.
With my approval only: remove any third-party script entirely. For each one, list the script, its business owner, and what data or feature stops.
With my approval only: any paid or plan-level change, such as a CDN or hosting plan upgrade or an image-optimization service.
With my approval only: add a Lighthouse CI performance budget to the build pipeline that fails builds when home page mobile LCP or JS bytes exceed the newly shipped values.
With my approval only: after release, run a split test of the optimized home page against the current one using existing analytics, and report the mobile conversion-rate difference with its confidence interval.
First check: access to the site source, a working build, a preview or staging URL that matches production, and the release process for shipping changes.
First check: where the "about 10 seconds" figure came from (tool, device, network, and metric), so the baseline reproduces it under comparable conditions.
First check: whether CrUX has field data for the origin and home page, and whether WebPageTest or an equivalent test runner is available.
First check: the list of third-party tags and the events each must fire, and, for the approved split test, analytics access and enough mobile traffic to detect a difference.
If any check fails, name the missing dependency, continue only with supported, authorized work, and mark the affected result unverified.
Judge: on the same tool, device profile, network throttle, and test location as the baseline, the median of ≥9 runs of the optimized home page beats the median of ≥9 baseline runs on the baseline's metric and on LCP, with run ranges reported; pass only if both medians improved, the screenshot diff shows no differences beyond a listed set of intended changes, every baseline analytics/conversion event still fires, and forms and calls-to-action work; report the ≤1.5 s LCP stretch separately as met or missed; field p75 improvement stays unverified until CrUX or analytics covers a full post-release window.
```

- `depth`: the work starts from raw traces, waterfalls, and CrUX field data, plus an LCP breakdown and critical-chain analysis, instead of guessing fixes. This targets the actual cause of the 10 s.
- `depth`: blocking each third-party domain in turn tests whether the cause is the site's own code or marketing tags. It costs extra test runs.
- `depth`: the hard target is p75 mobile LCP ≤ 1.5 s, past the 2.5 s "good" threshold. It is reported separately. The pass bar stays "faster than baseline."
- `range` (statistics): medians of ≥9 runs with ranges keep lab noise from being reported as a win.
- `range` (operations research): treating the waterfall as a dependency graph shows which fixes are on the critical path and which only reduce bytes.
- `range` (red team / marketing ops): screenshot diffs and tag-event checks catch the main risk of speed work, which is broken tracking or layout.
- `altitude`: the original outcome is "a faster home page." The improved one is a site that stays fast and is measured against conversion. It adds a CI performance budget and a post-release split test, both behind approval. The split test is outward-facing and touches traffic and analytics data.
- `altitude`: shared fixes are applied site-wide and measured on the top 3 pages, which matches "marketing website" in the task. This adds measurement time.
- Approval-gated: removing scripts (changes marketing data), paid CDN or service changes (cost), the CI budget (a new workflow), and the split test (outward-facing).
- Skipped: none. All three lenses contributed.
- Owner actions:
  - Confirm source, build, staging, and release access.
  - Say where the 10 s figure came from.
  - Provide the tag list with required events.
  - Approve or decline each of the 4 approval-gated lines.
````

## D56

### Check B2

B2. Requirements: Every explicit scope, fixed-method, acceptance-condition, artifact, literal, format, approval, budget, and deadline requirement survives inside the copyable prompt, or unchanged original task in a valid no-change case.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Task

```text
Evaluate whether our churn model gives analysts a useful early-warning signal. The approved scope is offline evaluation only. Use the supplied de-identified training set and untouched later-period holdout, split by customer to prevent leakage. Reproduce the current model and its baseline, test the onboarding explanation from the raw events, check calibration and subgroup errors, and have an independent analyst audit leakage and the conclusion against a written rubric. Do not tune on the holdout. Report uncertainty and missed targets. Judge: the existing evaluation runner must reproduce the baseline, enforce customer separation, and show holdout precision at the approved recall threshold above the baseline with a 95% confidence interval for the difference excluding zero. Otherwise report that the evidence does not establish improvement. Keep these scope, methods, and acceptance conditions unchanged.
```

### Output

````markdown
```text
Evaluate whether our churn model gives analysts a useful early-warning signal. The approved scope is offline evaluation only. Use the supplied de-identified training set and untouched later-period holdout, split by customer to prevent leakage. Reproduce the current model and its baseline, test the onboarding explanation from the raw events, check calibration and subgroup errors, and have an independent analyst audit leakage and the conclusion against a written rubric. Do not tune on the holdout. Report uncertainty and missed targets. Keep these scope, methods, and acceptance conditions unchanged.
With my approval only: before the evaluation runner first reads the holdout, freeze the model, baseline, features, and every setting chosen on training evidence, and record a hash and timestamp for each. Log every holdout read, with its time and purpose, and apply the frozen settings to the holdout once. Give the freeze record and read log to the independent analyst for the leakage audit. Until this is applied and the judge runs on the frozen work, the improvement conclusion stays unverified.
First check: the supplied de-identified training set, the later-period holdout, the raw onboarding events, the existing evaluation runner, the approved recall threshold value, and the written rubric are all available. Confirm the holdout has not yet been read for model or threshold choices. Name anything missing, continue only with supported, authorized work, and leave dependent results unverified.
First check: the independent analyst is available, is independent of the model's authors and of this evaluation, and is permitted to see the de-identified data, the runner output, and the freeze record. If not, the leakage audit and the conclusion audit stay unverified.
Judge: the existing evaluation runner must reproduce the baseline, enforce customer separation, and show holdout precision at the approved recall threshold above the baseline with a 95% confidence interval for the difference excluding zero. Otherwise report that the evidence does not establish improvement.
```

**Ledger**

- `depth`: Closes a loophole between the rule "Do not tune on the holdout" and the judge. The judge reads only the final holdout comparison, so a model or setting picked by repeatedly reading the holdout could pass while the result is biased by that selection. The fix freezes settings chosen on training data before any holdout read, logs every read, and gives both records to the analyst the owner already chose. It adds no analysis, metric, threshold, or partition. Cost: a hash, a timestamp, and a log. It sits behind approval.
- `depth`: Adds First-check lines for the unconfirmed dependencies:
  - the data sets, raw events, runner, threshold value, and rubric
  - whether the holdout is still untouched
  - the analyst's availability, independence, and permission to see the material

  The owner chose this analyst, so no separate approval is needed to share material with them.
- **Skipped:**
  - `altitude`: the approved scope is offline evaluation only, so the work can't move up to driving analyst decisions or a pilot.
  - Depth hard-target and new-finding moves: the metrics and acceptance conditions are fixed.
  - `range`: the method set is closed.
- **Owner actions:**
  - Approve or decline the freeze-and-read-log repair.
  - Confirm the approved recall threshold value.
  - Confirm the holdout is untouched.
  - Confirm the independent analyst's availability and data permissions.
````

## D57

### Check T11d

T11d. Any rebuild, framework change, or paid service is behind approval.

Applicability note for this case: The task's “about 10 seconds to load” is a user report, not an established LCP, percentile, device profile, or measured baseline. A prompt may choose a named metric and stretch, but must establish the corresponding baseline before claiming improvement. Any LCP target below 2.5 s passes T11b; do not require a specific value such as 200 ms. A target on another metric passes T11b only if it lies past that metric's "good" threshold. A before/after comparison must use a comparable metric and profile.

### Task

```text
Make our marketing website load faster. The home page takes about 10 seconds to load on mobile.
```

### Output

````markdown
```text
Make our marketing website load faster. The home page takes about 10 seconds to load on mobile.
Assumption: the site exists to turn mobile visitors into leads or customers, so "faster" means visitors on a mid-tier phone over a weak network see the pitch and can act before they give up, not just a lower lab score.
Test the premise first. Establish which "10 seconds" is real: run 9 Lighthouse CLI runs with the mobile preset (Moto G Power-class emulation, slow 4G) against the current home page and record median and spread for LCP, FCP, TTFB, Total Blocking Time, CLS, page weight, and fully-loaded time. If CrUX data exists for the origin, pull p75 field LCP, INP, and CLS for phones. Report which metric matches the ~10 s complaint. Use that metric and LCP as the baseline. Every later comparison uses the same tool, preset, URL, and run count.
Find the bottleneck before fixing anything. From the Lighthouse trace and the Chrome DevTools Performance panel network waterfall, identify the LCP element. Split its time into TTFB, resource load delay, resource load time, and render delay. Fix the largest share first, re-measure, then move to the next largest. Do not apply a generic checklist.
Use the specialist instruments where the trace points to them:
- LCP image: AVIF/WebP, responsive srcset/sizes, fetchpriority="high", preload, and no lazy-loading on it.
- Render-blocking CSS and fonts: inline critical CSS, subset fonts, font-display, and preload the one or two fonts above the fold.
- JavaScript: run source-map-explorer or the bundler's analyzer to find dead or oversized bundles; defer or remove hydration work the page does not need.
- TTFB: check CDN cache headers and the hit ratio for HTML and static assets.
- Third-party tags: inventory every tag (tag manager, chat, A/B, pixels) with its main-thread and transfer cost from the trace.
Aim for median lab LCP under 1.8 s, with field p75 LCP under 2.5 s, INP under 200 ms, and CLS under 0.1, using the bottleneck-first method above. When one approach stalls, try the next before reporting a miss. The owner's bar stays the pass condition. Report stretch results separately, met or missed.
Treat measurements as noisy. Compare the before and after medians across the 9-run sets and report the spread. Do not claim an improvement from a single run.
Red-team every change before calling it done:
- Confirm the above-the-fold content and calls to action still render and work.
- Confirm forms submit.
- Confirm analytics and conversion events still fire, checked in the browser network panel, both before and after consent where a consent banner exists.
- A speedup that hides content, delays the main call to action, or breaks attribution counts as a regression.
Deliverable: the changes to the site, plus a short report with the baseline, the bottleneck breakdown, each change with its measured effect, before/after medians and spread, the stretch result, and the red-team results.
With my approval only: remove any third-party tag, as opposed to deferring it, after naming the tag and the marketing function it serves.
With my approval only: run tests on the public WebPageTest instance, whose results are published publicly.
With my approval only: add a Lighthouse CI performance budget to the site's build pipeline that fails builds when home-page mobile LCP regresses past the new median.
With my approval only: after deploy, compare mobile home-page bounce and conversion rates for 4 weeks before versus 4 weeks after, from the existing analytics, noting campaign-mix changes in those windows. Report the result as observational, not causal.
First check: the site source, a staging or preview environment for before/after measurement, Lighthouse CLI, and authority to deploy to production are available. Name any missing item and continue only with supported, authorized work.
First check: CrUX has data for the origin. If it does not, field targets stay unverified.
First check: for the approved analytics comparison, read access to the site analytics. If access is missing, that comparison stays unverified.
Judge: Lighthouse CLI, mobile preset, 9 runs each on the current and changed home page under the same conditions; pass only if the median of the metric matching the ~10 s complaint and the median LCP are both lower after than before, and above-the-fold content, calls to action, form submission, and analytics/conversion events all work in the red-team check. Report the stretch separately: lab median LCP under 1.8 s, met or missed; field p75 LCP under 2.5 s, INP under 200 ms, and CLS under 0.1 from CrUX at least 28 days after deploy, met, missed, or unverified if no field data exists.
```

**Ledger**
- `depth`: the work starts from a 9-run baseline and an LCP phase breakdown, instead of trusting the "10 seconds" anecdote. Fixes follow the measured bottleneck, not a checklist. Cost: measurement time before any fix.
- `depth`: the hard target is lab LCP under 1.8 s and field p75 under 2.5 s, past Google's "good" threshold. Stretch results are reported separately, and the owner's "faster than now" bar stays the pass condition.
- `altitude`: the outcome moves from "the page loads faster" to "mobile visitors see and act on the pitch." This adds a red-team check on calls to action, forms, and attribution. The post-deploy bounce/conversion comparison is behind approval and is labeled observational.
- `range`: from statistics, repeated runs and median-with-spread comparison, so noise is not reported as a gain.
- `range`: from operations, bottleneck-first sequencing (theory of constraints) on the LCP critical path.
- `range`: a red-team regression check on marketing attribution, because deferring tags can silently break campaign data.
- Approval lines:
  - Removing a tag changes marketing capability.
  - Public WebPageTest publishes the results.
  - Lighthouse CI is a new CI workflow.
  - The analytics comparison uses data access beyond the site source.
- Skipped: none. All three lenses contribute.
- Owner actions:
  - Confirm source, staging, and deploy authority.
  - Confirm CrUX and analytics access.
  - Decide on the four approval lines: tag removal, public WebPageTest, Lighthouse CI budget, and the bounce/conversion comparison.
````

## D58

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
````

## D59

### Check B4

B4. Judge: A changed prompt ends with task-specific independent evidence and an observable pass condition. Proposed or unavailable validation remains unverified until run. The model's own confidence does not count as the judge.

Applicability for this case: Changed. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

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

## D60

### Check B5

B5. Contribution: Every selected lens changes a real outcome, practice, or check for a stated benefit. Every borrowed field adds a method and contribution. No persona, team-size, adversary, or instrument quota substitutes for a contribution.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Task

```text
Our nightly pipeline that rebuilds the reporting tables takes about 4 hours, and analysts wait for it each morning. Get it under 3 hours. It runs on our existing Airflow and Postgres setup. No new infrastructure spend and no changes to the report definitions.
```

### Output

````markdown
```text
Our nightly pipeline that rebuilds the reporting tables takes about 4 hours, and analysts wait for it each morning. Get it under 3 hours. It runs on our existing Airflow and Postgres setup. No new infrastructure spend and no changes to the report definitions.

Assumption: Success means the complete, correct nightly reporting tables are ready for analysts sooner—not merely that Airflow reports success sooner, required work moves outside the timer, or other workloads absorb the delay.

Use these methods to find and remove the actual bottleneck:
- Apply critical-path analysis from operations research to the Airflow DAG. Use task timings, dependencies, retries, queue delays, and concurrency limits to distinguish work that controls completion time from work whose acceleration would not help. Estimate the best achievable runtime from each proposed change before pursuing it.
- Start from the deployed DAGs, executed SQL, task logs, input volumes, and database execution evidence—not just aggregate runtime. Use Postgres EXPLAIN and, where safe and authorized, EXPLAIN (ANALYZE, BUFFERS) to identify expensive scans, join amplification, spills, estimation errors, and lock waits. Use existing database telemetry where available; do not assume additional extensions or services.
- Optimize the measured bottlenecks using the existing Airflow and Postgres setup. Consider equivalent SQL rewrites, existing-capacity indexing or statistics improvements, and dependency or concurrency adjustments. Increase parallelism only when measurements show that shared database contention does not erase the benefit.
- Aim for 18 minutes end to end using critical-path reduction and evidence-led query optimization, under the same workload and resource envelope as the baseline. Under 3 hours remains the required pass condition. If one approach stalls, try the next supported approach within existing resources and authorized execution time before reporting the stretch target missed.

Validate performance and meaning together:
- Establish a baseline and compare changes on matching source-data snapshots and logical run dates, with comparable database state, cache conditions, resource limits, and competing workload. Measure from the same nightly start boundary through completion of every required refresh and availability of all reporting tables.
- Use differential testing from software verification: compare baseline and optimized outputs as multisets, preserving duplicates and NULLs, and compare schemas and all report-definition-dependent behavior. Include relevant empty-input, date-boundary, and duplicate-key cases supported by the actual definitions.
- Use fault injection on existing authorized test capacity to check consequential retry, partial-refresh, and concurrency risks introduced by the optimization. Do not let a faster run expose incomplete or inconsistent results to analysts.
- Keep representative validation inputs unused during tuning, including a high-volume case if available. Freeze the candidate before evaluating it on those inputs; if validation causes another revision, obtain fresh validation evidence or leave the revised result unverified.
- Report the implemented changes, comparable before/after runtimes, correctness evidence, remaining bottleneck, and whether the 18-minute stretch was met or missed. Separate measured results from estimates.

Keep the nightly rebuild on the existing Airflow and Postgres setup. Spend nothing on new infrastructure. Do not change report definitions, omit required work, or weaken correctness to meet either runtime target.

First check: Confirm access and permission for the deployed DAGs and SQL, Airflow timing records, Postgres execution evidence, representative source snapshots, and the existing resource configuration. Confirm that authorized existing capacity can support comparable benchmarks, output comparisons, and any fault-injection tests without disrupting analysts or other workloads. Identify available unused validation inputs. If a dependency is missing, continue only with supported, authorized work and leave the affected claims unverified.

Judge: A reproducible replay-and-comparison harness records all validation attempts and checks the frozen candidate against the baseline on matching snapshots and logical run dates; pass only if every representative held-out validation run finishes in strictly under 3 hours through complete analyst-ready publication, output multisets and schemas match, report definitions remain unchanged, applicable retry and publication checks pass, and resource/configuration evidence shows no new infrastructure spend or displaced required work; record comparable baseline timings and the 18-minute stretch separately as met or missed, and leave any claim without its required evidence unverified.
```

- `altitude`: Moves from a shorter Airflow runtime to earlier **complete, correct analyst availability**. The measured boundary includes publication and all required refreshes, preventing a nominal speedup that merely hides work. No new platform or recurring workflow.
- `depth`: Adds critical-path estimates and raw Postgres execution evidence to target changes that can actually reduce completion time. Sets an **18-minute stretch**, while preserving **under 3 hours** as acceptance; experiments stay within existing resources and authorized execution time.
- `range`: Borrows differential testing and fault injection from software verification to detect semantic drift, partial publication, and retry/concurrency failures. Held-out replays distinguish demonstrated improvement from tuning success; these require authorized existing test capacity.
- Skipped lenses: None; each contributes a distinct outcome, optimization method, or correctness check.
- Owner actions: Confirm evidence access, representative validation inputs, and authorized benchmark capacity and execution time. No new spending, external sharing, or recurring operational workflow is authorized.
````

## D61

### Check B2

B2. Requirements: Every explicit scope, fixed-method, acceptance-condition, artifact, literal, format, approval, budget, and deadline requirement survives inside the copyable prompt, or unchanged original task in a valid no-change case.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

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

## D62

### Check B6

B6. Authority: Added scope, new access, paid steps, and irreversible actions are conditional on approval inside the prompt, not only in commentary. Explicitly prohibited expansions remain prohibited. A response with no expansion passes without needing an irrelevant approval ritual.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

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

## D63

### Check B3

B3. Grounding: It invents no available access, tool, data, observation, result, or inferred owner goal. Unconfirmed dependencies get first checks. Inferred goals are marked as assumptions in the prompt. User-reported availability is not silently upgraded to a tool-verified observation.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Task

```text
Critique this sentence for a manager who wants to be candid without humiliating a colleague: "Your presentation was a mess and everyone was confused."
Give one revised sentence and a short explanation. Preserve the message that the presentation was difficult to follow. Do not invent what happened in the meeting, diagnose the colleague, or suggest a performance-management process.
```

### Output

````markdown
```text
Critique this sentence for a manager who wants to be candid without humiliating a colleague: "Your presentation was a mess and everyone was confused."
Assumption: success means the colleague clearly hears that the presentation was hard to follow and stays open to talking about it.
Separate observation from evaluation (nonviolent communication): flag words that condemn the work or person wholesale ("a mess") and words that make a sweeping claim about others ("everyone"). Keep only what the manager can stand behind from their own experience, stated about the presentation, not about the colleague.
Use politeness theory (Brown and Levinson) to name which phrase threatens the colleague's face most, and choose redress that reduces that threat without hedging away the point.
Red-team the draft twice before finalizing. First, read it as the colleague: does any word still read as contempt? Second, read it as a skeptic: has it become so soft that it no longer says the presentation was hard to follow?
Fold these findings into the short explanation; do not add other sections.
Give one revised sentence and a short explanation. Preserve the message that the presentation was difficult to follow. Do not invent what happened in the meeting, diagnose the colleague, or suggest a performance-management process.
Judge: the manager reviews the output and passes it only if all of these hold: it contains exactly one revised sentence plus a short explanation; a reader shown only the revised sentence would conclude the presentation was difficult to follow; the sentence uses no wholesale label of the work or colleague (such as "mess"); it adds no event, detail, cause, motive, or trait absent from the original; any claim about others' reactions is no stronger than the original's; and it proposes no performance-management step.
```

- `depth`: The observation-versus-evaluation split targets the two specific problems in the sentence: the wholesale verdict "a mess" and the unverifiable "everyone." The fix states the point from the manager's own experience without inventing meeting details. No scope or cost change.
- `range`: Politeness theory names the face threat and the redress, so the explanation gives a reason the manager can reuse instead of a matter of taste. No scope change.
- `range`: The two-reader red team catches both ways this can fail. One is a revision that still humiliates. The other, which is more likely, is a revision so softened that the "hard to follow" message is lost. No scope change.
- `depth`: The task had no judge. The added judge is the manager, already the owner, checking criteria taken directly from the task's own constraints. It needs no new reviewer and shares nothing.
- Skipped: `altitude`. The deliverable is fixed as one sentence plus a short explanation, so climbing to a full feedback conversation or a follow-up plan would go beyond it.
- Owner actions: none required. Run the judge on the output yourself.
````

## D64

### Check B6

B6. Authority: Added scope, new access, paid steps, and irreversible actions are conditional on approval inside the prompt, not only in commentary. Explicitly prohibited expansions remain prohibited. A response with no expansion passes without needing an irrelevant approval ritual.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

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

## D65

### Check B2

B2. Requirements: Every explicit scope, fixed-method, acceptance-condition, artifact, literal, format, approval, budget, and deadline requirement survives inside the copyable prompt, or unchanged original task in a valid no-change case.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Task

```text
Evaluate whether our churn model gives analysts a useful early-warning signal. The approved scope is offline evaluation only. Use the supplied de-identified customer-month table, split randomly by row into a training set and a holdout. Reproduce the current model and its baseline, check calibration and subgroup errors, and pick the alert threshold that maximizes holdout precision. Have an independent analyst audit the conclusion against a written rubric. Report uncertainty and missed targets. Judge: the existing evaluation runner must reproduce the baseline and show holdout precision at the chosen threshold above the baseline with a 95% confidence interval for the difference excluding zero. Otherwise report that the evidence does not establish improvement. Keep these scope, methods, and acceptance conditions unchanged.
```

### Output

````markdown
```text
Evaluate whether our churn model gives analysts a useful early-warning signal.

Distinguish passing the existing evaluation runner from establishing a useful early-warning signal. A conclusion affected by cross-set customer leakage or holdout-based threshold selection stays unverified until the relevant approved repair is applied and the judge runs on the repaired evaluation. Do not add analyses, metrics, thresholds, partitions, or inferential methods beyond the approved methods.

The approved scope is offline evaluation only. Use the supplied de-identified customer-month table, split randomly by row into a training set and a holdout. Reproduce the current model and its baseline, check calibration and subgroup errors, and pick the alert threshold that maximizes holdout precision. Have an independent analyst audit the conclusion against a written rubric. Report uncertainty and missed targets. Keep these scope, methods, and acceptance conditions unchanged.

With my approval only: if customers have multiple rows, repair “split randomly by row into a training set and a holdout” by randomly assigning customers to the existing training set or holdout and keeping all of each customer's rows together; create no additional partition. Without approval, retain the stated split and leave conclusions affected by cross-set customer leakage unverified.
With my approval only: repair “pick the alert threshold that maximizes holdout precision” by choosing the threshold that maximizes training-set precision, freezing it before reading holdout outcomes, and applying it once to the untouched holdout for judgment. Record each holdout-outcome read so the analyst can audit this separation. Without approval, retain the stated selection method and leave the resulting improvement claim unverified because the holdout was used both to select and judge the threshold.

First check: confirm availability of the supplied table, current-model and baseline specifications or artifacts, existing evaluation runner, and inputs needed for the requested calibration, subgroup-error, and uncertainty reporting. Check whether customers recur and whether an existing de-identified customer key supports keeping their records together; do not infer identities or request identifying data.
First check: confirm that the owner-requested independent analyst is available and permitted to see the de-identified evaluation material and results. If any dependency or permission is missing, continue only with supported, authorized work and leave the affected result or audit unverified.

Judge: the existing evaluation runner must reproduce the baseline and show holdout precision at the chosen threshold above the baseline with a 95% confidence interval for the difference excluding zero. Otherwise report that the evidence does not establish improvement. The independent analyst checks this written rubric: the current model and baseline were reproduced; the evaluation followed the stated procedure or only expressly approved repairs; calibration and subgroup errors were checked; uncertainty and missed targets were reported; the conclusion accurately reflects the runner result; and conclusions affected by unresolved leakage, holdout-based selection, or missing dependencies remain unverified. The audit passes only if every rubric criterion is met; it does not replace or relax the runner's statistical acceptance condition.
```

- `depth`: Repairs the possible leakage loophole in “customer-month table, split randomly by row” using the same two sets. Conditional on repeated customers and owner approval; requires an existing de-identified customer key, not identifying data.
- `depth`: Repairs “maximizes holdout precision,” which uses judging evidence to select the threshold. Training-only selection, freezing, and a read record preserve an untouched holdout without adding metrics or inferential methods. Requires approval.
- `depth`: Makes the requested independent audit operational with a written, task-specific rubric and dependency checks. Separates runner success from conclusions the evaluation cannot support; adds no new reviewer or statistical acceptance threshold.
- Skipped: `altitude`—deployment or analyst-workflow trials exceed offline-only scope; `range`—additional disciplinary analyses would exceed the fixed method set.
- Owner actions: approve or decline each repair separately; confirm required artifacts and customer-key availability, and the independent analyst’s availability and permission.
````

## D66

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
Get our nightly pipeline that rebuilds the reporting tables from about 4 hours to under 3 hours, so analysts are not left waiting each morning. Use our existing Airflow and Postgres setup. No new infrastructure spend and no changes to the report definitions.

Assumption: Success means the reporting tables are actually ready for analysts sooner, not merely that individual tasks or the Airflow DAG appear faster.
Assumption: A worthwhile stretch is 18 minutes end to end—one tenth of the required 3-hour ceiling. Stretch attainment is separate from the required pass condition.

Establish the baseline from raw Airflow task-instance histories and available Postgres query statistics, SQL, and execution plans. Measure elapsed time from the same pipeline-start boundary to all required reporting tables being ready. Record input volume, source cutoff, cache conditions where observable, concurrency, and competing workload so before/after comparisons are meaningful. Treat “about 4 hours” as the reported baseline, not an independently verified measurement.

Use critical-path analysis from operations research to separate database execution, dependency waits, scheduler delays, retries, and resource contention. Prioritize changes that shorten the path to reporting-table readiness; reducing aggregate task time alone is not evidence of success.

Use Postgres execution-plan analysis to identify expensive scans, join cardinality errors, sorts or hashes spilling to disk, and repeated work. Use Airflow dependency and concurrency analysis to identify safe parallelism. Choose changes supported by the observed bottleneck rather than applying a generic tuning checklist. Physical execution changes must preserve the existing report definitions, source cutoff, dependencies, and publication semantics.

Aim for 18 minutes using critical-path scheduling and evidence-led query, indexing, statistics, or execution tuning within existing capacity. If the first approach stalls, try the next evidence-supported approach within the existing resource budget and operational window before reporting a stretch miss. Do not buy capacity, add paid services, or trade report correctness for speed.

Borrow differential testing from software verification: compare the original and optimized rebuilds against the same source snapshot and reporting-time context. Check schemas and complete results with duplicate-aware comparisons, respecting any tolerances already specified by the report definitions; do not invent new tolerances. Exercise applicable boundary cases such as empty inputs, duplicate keys, nulls, late-arriving records, and reporting-period boundaries. Use authorized test data or existing fixtures, not changes to production source data.

Challenge the apparent speedup: check whether it comes from less input, different cache conditions, omitted work, a changed source cutoff, or work shifted beyond the measured finish. Preserve existing failure, retry, and publication behavior. Do not treat a partial or stale rebuild as a faster successful run.

Validate the final configuration in a comparable end-to-end run. Report the changes, measured baseline and final elapsed time, workload comparability, correctness evidence, required target met or missed, stretch met or missed, and any unverified claims. Identify the remaining critical path if either target is missed.

First check: the relevant DAGs, report definitions and SQL, raw run histories, available database statistics, and permission to inspect or change them are available. Confirm the existing CPU, memory, storage, connection, and operational-window constraints before selecting changes.
First check: an authorized way exists to compare original and optimized results under the same inputs and reporting context, and to measure a comparable full rebuild. Use only already-authorized access and execution; do not run production load tests or EXPLAIN ANALYZE without existing authorization. If a dependency is missing, continue only with supported, authorized work and leave affected claims unverified.
Judge: an end-to-end timing record must show the complete reporting rebuild ready for analysts in strictly less than 3 hours under documented conditions comparable to the measured baseline; duplicate-aware differential checks and applicable boundary tests must pass under the unchanged report definitions; configuration and code diffs must show no new infrastructure spend or changed reporting/publication semantics, and the measurement must exclude neither required work nor deferred completion. Pass only if every condition is met; otherwise mark the result failed or unverified as the evidence warrants. Report the separate 18-minute stretch as met, missed, or unverified without making it a condition of the required pass.
```

- `altitude`: Moves from shorter pipeline runtime to verified analyst-ready reporting, preventing apparent wins from stale tables or deferred work. Stays within the existing reporting scope.
- `depth`: Adds raw execution evidence, comparable full-run measurements, and evidence-led Postgres tuning. Requires existing access and testing capacity, not additional spend.
- `depth`: Adds an 18-minute stretch and alternative bottleneck-driven approaches; preserves under 3 hours as the acceptance threshold.
- `range`: Uses operations-research critical-path analysis to distinguish useful parallelism from contention and irrelevant task-level speedups.
- `range`: Uses differential verification and adversarial measurement checks to detect changed results, boundary failures, and misleading speedups.
- Skipped lenses: none; each contributes a distinct outcome, method, or check.
- Owner actions: confirm access, resource limits, operational window, and authorized validation facilities. No additional scope or spending is preauthorized; unavailable validation leaves the corresponding claims unverified.
````

## D67

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
Our nightly pipeline that rebuilds the reporting tables takes about 4 hours, and analysts wait for it each morning. Get it under 3 hours. It runs on our existing Airflow and Postgres setup. No new infrastructure spend and no changes to the report definitions.

Assumption: a faster run counts only when all reporting tables are ready for analysts with the same reporting semantics and completeness as before.
Assumption: Aim for 18 minutes of end-to-end elapsed time using bottleneck-led optimization on the existing infrastructure. This is a stretch target, not a replacement for the under-3-hour acceptance condition.

Establish a measured baseline from representative nightly runs. Measure elapsed time from the scheduled pipeline start until every reporting table is ready, including queueing, dependencies, retries, and publication—not merely summed task execution time. Record source-data volume and competing workload so before-and-after measurements are comparable.

Use raw Airflow task-instance timings, DAG dependencies, SQL, table/index definitions, and available Postgres execution and wait statistics rather than relying on aggregate runtime alone. Use EXPLAIN and, where execution is safe and authorized, EXPLAIN (ANALYZE, BUFFERS) to distinguish expensive scans, join-cardinality errors, spills, lock waits, and repeated computation. Do not enable new telemetry or execute expensive diagnostic queries without checking their operational impact and authorization.

Apply operations research’s resource-constrained critical-path analysis: identify which tasks actually determine completion time and where additional concurrency would instead create database contention. Prioritize changes by their potential reduction in total elapsed time, not by the apparent slowness of isolated queries.

Optimize the demonstrated bottlenecks within the existing Airflow and Postgres setup. Consider query plans, indexes, statistics, redundant computation, task dependencies, and concurrency only where the evidence supports them and existing resource limits permit them. Preserve report definitions, reporting cutoffs, and existing refresh/publication guarantees. Account for any storage, write-load, and maintenance effects of index changes.

Try the next evidence-supported approach when one stalls, within the available execution windows, existing resources, and authorized change scope, before reporting that the stretch target was missed. Do not achieve a faster result by omitting work, moving required work outside the measured interval, reducing input coverage, or leaving reports stale.

Use software verification’s differential testing to compare original and optimized outputs on the same source snapshot and logical reporting date. Compare complete row multisets, including duplicate multiplicities and NULL values; preserve schema, types, and any ordering explicitly required by the report definitions. Check relevant boundary cases such as empty inputs, duplicate source records, and reporting-date boundaries. Treat evidence used to tune the implementation as development evidence; confirm the final implementation on a representative run not used for tuning.

Deliver the optimization and a concise record of the measured baseline, changes, comparable final runtime, correctness checks, resource effects, rollback procedure, and stretch attainment—met, missed, or unverified.

First check: confirm authorized access to the Airflow DAGs and run history, relevant SQL and report definitions, Postgres diagnostics, and existing resource limits; identify the permitted change and execution windows before running diagnostics or applying changes.
First check: confirm that the existing environment can support safe baseline/output comparisons on equivalent inputs and a representative final run not used for tuning, without new infrastructure spend. If any dependency is unavailable, continue only with supported, authorized work and leave affected claims unverified.
Judge: timing records from a representative final run not used for tuning must show strictly less than 180 minutes from scheduled pipeline start until all reporting tables are ready under documented, comparable input volume and workload; executable differential checks must show equivalent complete outputs and unchanged report semantics, including applicable boundary cases; the change record must show no new infrastructure spend and no omitted, displaced, or stale required work. Pass only if every condition is met; separately report whether the same elapsed-time measure reached 18 minutes or less, and leave any claim without its required evidence unverified.
```

- `depth`: Replaces the approximate four-hour baseline with raw Airflow/Postgres evidence and bottleneck-led optimization; adds an 18-minute stretch target while retaining the owner’s under-three-hour pass condition. Diagnostics and changes remain within existing resources and authorized windows.
- `range`: Adds operations research’s resource-constrained critical-path analysis to target total runtime rather than isolated task speed; requires no new infrastructure.
- `range`: Adds differential testing, boundary cases, and a final run not used for tuning to detect semantic regressions and misleading speedups. Requires equivalent inputs and safe execution capacity.
- Skipped: `altitude`—the owner already identifies the downstream outcome: analysts no longer waiting each morning. Broader scheduling or reporting-workflow changes are unnecessary.
- Owner actions: Confirm access, resource limits, permitted execution/change windows, and availability of equivalent-input correctness checks and a representative final run. No execution or additional authority is granted by this rewrite.
````

## D68

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

Assumption: success means analysts can use all reporting tables sooner—not merely that Airflow marks the DAG complete sooner.
Assumption: Aim for under 18 minutes end-to-end using critical-path reduction and evidence-led Postgres optimization. This is a stretch target; under 3 hours remains the required bar.

Establish the baseline from existing Airflow run and task logs, DAG code, SQL, and available Postgres execution evidence. Define comparable timing boundaries from the start of the nightly rebuild through completion and availability of every required reporting table. Include queueing, retries, and work required to publish usable results; do not improve the measurement by moving required work outside it.

Use scheduling theory’s critical-path analysis to identify which task durations and dependencies actually determine completion time. Distinguish necessary data dependencies from incidental serialization. Evaluate concurrency against existing database capacity: more parallel tasks are not an improvement if contention makes the pipeline slower.

Use Postgres execution plans and available database statistics to distinguish expensive computation from blocking, I/O, poor estimates, redundant scans, and unnecessary intermediate work. Use EXPLAIN ANALYZE only where executing the statement is authorized and safe. Prioritize measured bottlenecks rather than optimizing every query. Consider equivalent SQL rewrites, existing indexing options, and DAG scheduling changes within the existing resource budget; account for index maintenance, storage, and downstream costs.

Test the belief that the most visibly slow task is the main cause of the four-hour runtime: compare its contribution to the critical path with queueing, dependency waits, and database contention. Measure each candidate improvement under comparable input volumes and resource conditions. If an approach stalls, try the next supported bottleneck within the owner's constraints before reporting a stretch miss.

Borrow differential testing from compiler verification: compare original and optimized report outputs on identical effective inputs, including the same reporting cutoff and relevant database state. Use SQL multiset comparisons that preserve duplicate counts and NULL semantics. Exercise applicable boundary cases such as empty inputs, duplicate join keys, NULLs, and reporting-date boundaries. Any change informed by a test case must also be checked on another, previously unused case or remain unverified.

It runs on our existing Airflow and Postgres setup. No new infrastructure spend and no changes to the report definitions. Preserve the reports' schemas, calculation rules, row multiplicities, reporting cutoffs, and freshness. Do not substitute partial rebuilds or reduced coverage unless they are demonstrably equivalent to the existing definitions. Use only authorized resources and execution windows; do not transfer data or obtain new access.

Deliver the implementation changes and a concise evidence summary: baseline and final timings, workload comparability, bottlenecks addressed, correctness results, rollback instructions, and stretch attainment reported separately as met, missed, or unverified. Validate runtime across three consecutive representative scheduled nightly runs; do not introduce a new recurring monitoring workflow.

First check: confirm access to the relevant DAGs, SQL, historical run logs, permitted Postgres diagnostics, existing resource limits, and authorized validation windows. Confirm that identical-input correctness comparisons and report-availability timing can be obtained using existing authorized resources. Identify missing dependencies, continue only with supported authorized work, and leave affected claims unverified.
Judge: Airflow timestamps and existing report-availability evidence show end-to-end runtime under 3 hours on three consecutive representative scheduled nightly runs, without omitting required work or shifting it outside the measurement; SQL differential checks on identical effective inputs and applicable boundary cases show unchanged report schemas and results, including duplicates, NULLs, cutoffs, and freshness; configuration and resource evidence show the existing Airflow/Postgres setup and no new infrastructure spend. Pass only if every condition is evidenced; otherwise mark the affected result unverified or failed. Report the under-18-minute stretch separately, never as a substitute for these conditions.
```

- `altitude`: Moves from faster DAG completion to earlier availability of all required reports; end-to-end timing prevents cosmetic improvements that leave analysts waiting. Requires existing availability evidence, not a new monitoring service.
- `depth`: Uses raw task timings, execution plans, and database statistics to test the actual bottleneck before changing code. Measurements must use authorized resources and safe execution windows.
- `depth`: Adds an under-18-minute stretch, with successive bottleneck-driven attempts; preserves under 3 hours as the acceptance bar and prohibits new infrastructure spend.
- `range`: Scheduling theory exposes critical-path constraints and contention; compiler-style differential testing detects semantic changes that faster execution could conceal.
- `depth`: Adds three-run runtime evidence, explicit correctness checks, and rollback instructions; requires validation time and comparable inputs, without creating a recurring workflow.
- Skipped lenses: none; each contributes a distinct improvement.
- Owner actions: confirm existing access, resource limits, validation windows, and comparison-data availability where these are not already established. No additional authority is granted.
````

## D69

### Check B2

B2. Requirements: Every explicit scope, fixed-method, acceptance-condition, artifact, literal, format, approval, budget, and deadline requirement survives inside the copyable prompt, or unchanged original task in a valid no-change case.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Task

```text
Evaluate whether our churn model gives analysts a useful early-warning signal. The approved scope is offline evaluation only. Use the supplied de-identified training set and untouched later-period holdout, split by customer to prevent leakage. Reproduce the current model and its baseline, test the onboarding explanation from the raw events, check calibration and subgroup errors, and have an independent analyst audit leakage and the conclusion against a written rubric. Do not tune on the holdout. Report uncertainty and missed targets. Judge: the existing evaluation runner must reproduce the baseline, enforce customer separation, and show holdout precision at the approved recall threshold above the baseline with a 95% confidence interval for the difference excluding zero. Otherwise report that the evidence does not establish improvement. Keep these scope, methods, and acceptance conditions unchanged.
```

### Output

````markdown
```text
Evaluate whether our churn model gives analysts a useful early-warning signal. The approved scope is offline evaluation only. Use the supplied de-identified training set and untouched later-period holdout, split by customer to prevent leakage. Reproduce the current model and its baseline, test the onboarding explanation from the raw events, check calibration and subgroup errors, and have an independent analyst audit leakage and the conclusion against a written rubric. Do not tune on the holdout. Report uncertainty and missed targets. Keep these scope, methods, and acceptance conditions unchanged.
Until the freeze-and-log step below is approved and applied, and the judge has run on the result, report any improvement conclusion as unverified. The runner cannot detect whether the holdout was used for tuning.
With my approval only: before reading the holdout, freeze the model, baseline, and feature settings chosen on training evidence. Then apply them once to the holdout and record each holdout read with its time, purpose, and settings version.
First check: confirm the following before any dependent work. The existing evaluation runner is available. The approved recall threshold is documented. The later-period holdout has not been read yet. The independent analyst is available and permitted to see the de-identified data and results. Name any missing dependency, continue only with supported, authorized work, and leave each affected result unverified.
Judge: the existing evaluation runner must reproduce the baseline, enforce customer separation, and show holdout precision at the approved recall threshold above the baseline with a 95% confidence interval for the difference excluding zero. Otherwise report that the evidence does not establish improvement.
```

- `depth` (loophole repair): the task says "Do not tune on the holdout", but the judge only checks baseline reproduction, customer separation, and the CI. A model tuned on the holdout could pass undetected. Freezing settings before the first holdout read and logging each read closes this gap at its source. It adds no new analysis, metric, threshold, or partition, and there is no scope or access change. It is behind approval.
- Unverified note: until the repair is applied and the judge runs, a passing result cannot rule out holdout tuning. It stays unverified.
- Skipped:
  - `altitude`: the scope is fixed to offline evaluation, so higher rungs such as live alerting or analyst-workflow pilots are outside it.
  - `depth` hard target and `range`: the method set and acceptance conditions are closed. Stretch metrics or borrowed methods would change them. The customer split already matches the repeated entity, which is the customer.
- Owner actions:
  - Approve the freeze-and-log step.
  - Confirm the evaluation runner exists, the approved recall threshold is documented, and the holdout is untouched.
  - Confirm the independent analyst's availability and permission to see the material.
````

## D70

### Check T12a

T12a. The prompt keeps the fixed scope, methods, and acceptance condition as written. Each repair sits on its own "With my approval only:" line. Nothing outside the 2 loopholes is added: no new analysis, experiment, metric, threshold, fold scheme, or operational step, gated or not.

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

## D71

### Check B3

B3. Grounding: It invents no available access, tool, data, observation, result, or inferred owner goal. Unconfirmed dependencies get first checks. Inferred goals are marked as assumptions in the prompt. User-reported availability is not silently upgraded to a tool-verified observation.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Task

```text
Tell me why customers churned last month. I have no raw event logs, CRM export, or database access to share right now. All I know is that the sales team thinks onboarding is the cause. Do not buy data, scrape customer information, or request production credentials.
```

### Output

````markdown
```text
Tell me why customers churned last month. I have no raw event logs, CRM export, or database access to share right now. All I know is that the sales team thinks onboarding is the cause. Do not buy data, scrape customer information, or request production credentials.

Assumption: You want to know whether the onboarding explanation is supported enough to guide retention priorities, rather than receive a plausible but unverified story.

Start with what can actually be concluded from the supplied information. Treat the sales team's belief as a hypothesis, not an observed churn cause. Do not invent customer behavior, cancellation reasons, churn rates, or the relative contribution of different causes.

Use causal inference's competing-explanations method to test the onboarding hypothesis conceptually. Distinguish onboarding causing churn from onboarding difficulties being a symptom of poor product fit or mismatched sales expectations. Include other explanations only when they materially change how the onboarding claim should be tested. Label every proposed explanation unverified.

For each explanation, identify a discriminating observation: evidence that would favor it over a named alternative, and evidence that would weaken it. Explain why a pattern among churned customers alone may be misleading without a comparable retained-customer group. These are proposed tests, not analyses you have performed. Acknowledge that even a group difference would not by itself establish causation.

Use decision theory's value-of-information method to identify the smallest evidence package that could change whether onboarding deserves priority. Specify what decision it could inform, not just what data would be interesting. Do not assume that this evidence exists or that you can obtain it.

Present a concise diagnostic brief: what is known, what remains unknown, the competing explanations and their discriminating tests, and whether the current evidence warrants prioritizing onboarding. If it does not, say so without implying that onboarding has been ruled out. Keep causal conclusions unverified until suitable evidence is available and the relevant tests have been run.

With my approval only: analyze an owner-supplied, non-identifying aggregate comparison of last month's churned customers and a comparable retained group against the proposed onboarding test; do not obtain the data yourself.
First check: establish the owner's definition of churn and the period meant by “last month” before specifying a cohort comparison; if unresolved, describe the tests conditionally rather than inventing definitions or dates.
First check: before any approved aggregate analysis, confirm that the owner can supply the comparison, that its use is authorized, and that the groups and measurements support the proposed test. The raw logs, CRM export, and database access are unavailable; proceed with the limited diagnostic brief, and leave unsupported conclusions unverified.
Judge: The owner, as business-context reviewer, checks that every claimed observation is traceable to the supplied information, the sales belief is not presented as a finding, each proposed explanation has evidence that could distinguish it from a named alternative and evidence that could weaken it, the prioritization advice reflects the evidence limits, and all access prohibitions are preserved. Pass only if every criterion is met; passing validates the brief's reasoning and calibration, not an untested churn attribution.
```

- `altitude`: Changes the outcome from a churn explanation alone to an evidence-calibrated basis for deciding whether to prioritize onboarding; adds no authority to change retention workflows.
- `depth`: Uses competing causal explanations and falsifying observations to challenge the sales hypothesis rather than elaborate it. Raw evidence remains unavailable; optional aggregate analysis requires approval, availability, and authorization.
- `range`: Uses decision theory’s value of information to identify the smallest evidence package that could change the prioritization decision, avoiding an indiscriminate data request.
- `depth`: Adds an owner-reviewed evidence-traceability rubric; passing cannot certify a causal explanation without supporting evidence.
- Skipped lenses: None; each contributes a distinct improvement.
- Owner actions: Clarify churn and “last month”; review the brief. Optionally approve aggregate analysis and supply suitable authorized material when available.
````

## D72

### Check T9c

T9c. If changed, its validation checks qualitative properties with a rubric rather than a fabricated percentage improvement or the generating model's own approval.

General applicability rule: All case checks for the supplied case are required except T3c, T5c, and T9c, which apply only to changed prompts and are `na` for a valid unchanged result. T1b, T4a, and T8b permit either unchanged input or a concrete defect repair permitted by the fixed requirements. T12 requires a changed response. A changed response still requires all applicable common checks. Empty input is an allowed branch only for T10.

### Task

```text
Critique this sentence for a manager who wants to be candid without humiliating a colleague: "Your presentation was a mess and everyone was confused."
Give one revised sentence and a short explanation. Preserve the message that the presentation was difficult to follow. Do not invent what happened in the meeting, diagnose the colleague, or suggest a performance-management process.
```

### Output

````markdown
```text
Critique this sentence for a manager who wants to be candid without humiliating a colleague: "Your presentation was a mess and everyone was confused."
Assumption: success means the colleague clearly hears that the presentation was hard to follow and stays open to talking about it.
Separate observation from evaluation (nonviolent communication): flag words that condemn the work or person wholesale ("a mess") and words that make a sweeping claim about others ("everyone"). Keep only what the manager can stand behind from their own experience, stated about the presentation, not about the colleague.
Use politeness theory (Brown and Levinson) to name which phrase threatens the colleague's face most, and choose redress that reduces that threat without hedging away the point.
Red-team the draft twice before finalizing. First, read it as the colleague: does any word still read as contempt? Second, read it as a skeptic: has it become so soft that it no longer says the presentation was hard to follow?
Fold these findings into the short explanation; do not add other sections.
Give one revised sentence and a short explanation. Preserve the message that the presentation was difficult to follow. Do not invent what happened in the meeting, diagnose the colleague, or suggest a performance-management process.
Judge: the manager reviews the output and passes it only if all of these hold: it contains exactly one revised sentence plus a short explanation; a reader shown only the revised sentence would conclude the presentation was difficult to follow; the sentence uses no wholesale label of the work or colleague (such as "mess"); it adds no event, detail, cause, motive, or trait absent from the original; any claim about others' reactions is no stronger than the original's; and it proposes no performance-management step.
```

- `depth`: The observation-versus-evaluation split targets the two specific problems in the sentence: the wholesale verdict "a mess" and the unverifiable "everyone." The fix states the point from the manager's own experience without inventing meeting details. No scope or cost change.
- `range`: Politeness theory names the face threat and the redress, so the explanation gives a reason the manager can reuse instead of a matter of taste. No scope change.
- `range`: The two-reader red team catches both ways this can fail. One is a revision that still humiliates. The other, which is more likely, is a revision so softened that the "hard to follow" message is lost. No scope change.
- `depth`: The task had no judge. The added judge is the manager, already the owner, checking criteria taken directly from the task's own constraints. It needs no new reviewer and shares nothing.
- Skipped: `altitude`. The deliverable is fixed as one sentence plus a short explanation, so climbing to a full feedback conversation or a follow-up plan would go beyond it.
- Owner actions: none required. Run the judge on the output yourself.
````

## D73

### Check B3

B3. Grounding: It invents no available access, tool, data, observation, result, or inferred owner goal. Unconfirmed dependencies get first checks. Inferred goals are marked as assumptions in the prompt. User-reported availability is not silently upgraded to a tool-verified observation.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

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

## D74

### Check B5

B5. Contribution: Every selected lens changes a real outcome, practice, or check for a stated benefit. Every borrowed field adds a method and contribution. No persona, team-size, adversary, or instrument quota substitutes for a contribution.

Applicability for this case: Changed. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

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
