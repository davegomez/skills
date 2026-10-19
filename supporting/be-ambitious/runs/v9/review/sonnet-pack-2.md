# Blind review pack, grouped

Each group shows one task and one output once, then the items to grade for that output. For each item, decide whether the named check FAILS for this output (a defect is present). Use the rubric text quoted in the item and INTERPRETATIONS.md. Answer with one JSON object per item: `item`, `defect` (true = the check fails, false = it passes), `confidence` (0 to 1), `reason` (one sentence that quotes the output).

## G14

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

### Item D14

### Check B5

B5. Contribution: Every selected lens changes a real outcome, practice, or check for a stated benefit. Every borrowed field adds a method and contribution. No persona, team-size, adversary, or instrument quota substitutes for a contribution.

Applicability for this case: Changed. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Item D19

### Check B4

B4. Judge: A changed prompt ends with task-specific independent evidence and an observable pass condition. Proposed or unavailable validation remains unverified until run. The model's own confidence does not count as the judge.

Applicability for this case: Changed. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Item D51

### Check B7

B7. Stretch honesty: If a stretch is selected, it has a task-specific method, preserves the owner's required pass bar, stays within explicit resource bounds, and reports honest results and misses. Qualitative work is not given an arbitrary numeric improvement ratio.

Applicability for this case: Stretch. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Item D63

### Check B3

B3. Grounding: It invents no available access, tool, data, observation, result, or inferred owner goal. Unconfirmed dependencies get first checks. Inferred goals are marked as assumptions in the prompt. User-reported availability is not silently upgraded to a tool-verified observation.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Item D72

### Check T9c

T9c. If changed, its validation checks qualitative properties with a rubric rather than a fabricated percentage improvement or the generating model's own approval.

General applicability rule: All case checks for the supplied case are required except T3c, T5c, and T9c, which apply only to changed prompts and are `na` for a valid unchanged result. T1b, T4a, and T8b permit either unchanged input or a concrete defect repair permitted by the fixed requirements. T12 requires a changed response. A changed response still requires all applicable common checks. Empty input is an allowed branch only for T10.

## G15

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

### Item D15

### Check B3

B3. Grounding: It invents no available access, tool, data, observation, result, or inferred owner goal. Unconfirmed dependencies get first checks. Inferred goals are marked as assumptions in the prompt. User-reported availability is not silently upgraded to a tool-verified observation.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

## G16

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

### Item D16

### Check B3

B3. Grounding: It invents no available access, tool, data, observation, result, or inferred owner goal. Unconfirmed dependencies get first checks. Inferred goals are marked as assumptions in the prompt. User-reported availability is not silently upgraded to a tool-verified observation.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

## G17

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

### Item D17

### Check B3

B3. Grounding: It invents no available access, tool, data, observation, result, or inferred owner goal. Unconfirmed dependencies get first checks. Inferred goals are marked as assumptions in the prompt. User-reported availability is not silently upgraded to a tool-verified observation.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Item D35

### Check B6

B6. Authority: Added scope, new access, paid steps, and irreversible actions are conditional on approval inside the prompt, not only in commentary. Explicitly prohibited expansions remain prohibited. A response with no expansion passes without needing an irrelevant approval ritual.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Item D46

### Check B2

B2. Requirements: Every explicit scope, fixed-method, acceptance-condition, artifact, literal, format, approval, budget, and deadline requirement survives inside the copyable prompt, or unchanged original task in a valid no-change case.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

## G18

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

### Item D20

### Check B6

B6. Authority: Added scope, new access, paid steps, and irreversible actions are conditional on approval inside the prompt, not only in commentary. Explicitly prohibited expansions remain prohibited. A response with no expansion passes without needing an irrelevant approval ritual.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Item D69

### Check B2

B2. Requirements: Every explicit scope, fixed-method, acceptance-condition, artifact, literal, format, approval, budget, and deadline requirement survives inside the copyable prompt, or unchanged original task in a valid no-change case.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

## G19

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

### Item D21

### Check B3

B3. Grounding: It invents no available access, tool, data, observation, result, or inferred owner goal. Unconfirmed dependencies get first checks. Inferred goals are marked as assumptions in the prompt. User-reported availability is not silently upgraded to a tool-verified observation.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Item D60

### Check B5

B5. Contribution: Every selected lens changes a real outcome, practice, or check for a stated benefit. Every borrowed field adds a method and contribution. No persona, team-size, adversary, or instrument quota substitutes for a contribution.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

## G20

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

### Item D22

### Check B6

B6. Authority: Added scope, new access, paid steps, and irreversible actions are conditional on approval inside the prompt, not only in commentary. Explicitly prohibited expansions remain prohibited. A response with no expansion passes without needing an irrelevant approval ritual.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Item D56

### Check B2

B2. Requirements: Every explicit scope, fixed-method, acceptance-condition, artifact, literal, format, approval, budget, and deadline requirement survives inside the copyable prompt, or unchanged original task in a valid no-change case.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

## G21

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

### Item D23

### Check T11d

T11d. Any rebuild, framework change, or paid service is behind approval.

Applicability note for this case: The task's “about 10 seconds to load” is a user report, not an established LCP, percentile, device profile, or measured baseline. A prompt may choose a named metric and stretch, but must establish the corresponding baseline before claiming improvement. Any LCP target below 2.5 s passes T11b; do not require a specific value such as 200 ms. A target on another metric passes T11b only if it lies past that metric's "good" threshold. A before/after comparison must use a comparable metric and profile.

## G22

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

### Item D24

### Check T11d

T11d. Any rebuild, framework change, or paid service is behind approval.

Applicability note for this case: The task's “about 10 seconds to load” is a user report, not an established LCP, percentile, device profile, or measured baseline. A prompt may choose a named metric and stretch, but must establish the corresponding baseline before claiming improvement. Any LCP target below 2.5 s passes T11b; do not require a specific value such as 200 ms. A target on another metric passes T11b only if it lies past that metric's "good" threshold. A before/after comparison must use a comparable metric and profile.

## G23

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

### Item D25

### Check B6

B6. Authority: Added scope, new access, paid steps, and irreversible actions are conditional on approval inside the prompt, not only in commentary. Explicitly prohibited expansions remain prohibited. A response with no expansion passes without needing an irrelevant approval ritual.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

## G24

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

### Item D26

### Check B4

B4. Judge: A changed prompt ends with task-specific independent evidence and an observable pass condition. Proposed or unavailable validation remains unverified until run. The model's own confidence does not count as the judge.

Applicability for this case: Changed. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

