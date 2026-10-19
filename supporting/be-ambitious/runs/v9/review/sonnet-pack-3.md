# Blind review pack, grouped

Each group shows one task and one output once, then the items to grade for that output. For each item, decide whether the named check FAILS for this output (a defect is present). Use the rubric text quoted in the item and INTERPRETATIONS.md. Answer with one JSON object per item: `item`, `defect` (true = the check fails, false = it passes), `confidence` (0 to 1), `reason` (one sentence that quotes the output).

## G25

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

### Item D27

### Check T11a

T11a. Depth: the prompt names raw material a performance engineer starts from (field data or traces, a waterfall, the bundle) and instruments by name (for example a lab tool and real-user measurement), not "optimize images".

Applicability note for this case: The task's “about 10 seconds to load” is a user report, not an established LCP, percentile, device profile, or measured baseline. A prompt may choose a named metric and stretch, but must establish the corresponding baseline before claiming improvement. Any LCP target below 2.5 s passes T11b; do not require a specific value such as 200 ms. A target on another metric passes T11b only if it lies past that metric's "good" threshold. A before/after comparison must use a comparable metric and profile.

## G26

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

### Item D28

### Check B6

B6. Authority: Added scope, new access, paid steps, and irreversible actions are conditional on approval inside the prompt, not only in commentary. Explicitly prohibited expansions remain prohibited. A response with no expansion passes without needing an irrelevant approval ritual.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Item D71

### Check B3

B3. Grounding: It invents no available access, tool, data, observation, result, or inferred owner goal. Unconfirmed dependencies get first checks. Inferred goals are marked as assumptions in the prompt. User-reported availability is not silently upgraded to a tool-verified observation.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

## G27

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

### Item D29

### Check B2

B2. Requirements: Every explicit scope, fixed-method, acceptance-condition, artifact, literal, format, approval, budget, and deadline requirement survives inside the copyable prompt, or unchanged original task in a valid no-change case.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Item D32

### Check B6

B6. Authority: Added scope, new access, paid steps, and irreversible actions are conditional on approval inside the prompt, not only in commentary. Explicitly prohibited expansions remain prohibited. A response with no expansion passes without needing an irrelevant approval ritual.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

## G28

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

### Item D31

### Check B6

B6. Authority: Added scope, new access, paid steps, and irreversible actions are conditional on approval inside the prompt, not only in commentary. Explicitly prohibited expansions remain prohibited. A response with no expansion passes without needing an irrelevant approval ritual.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

## G29

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

### Item D33

### Check B2

B2. Requirements: Every explicit scope, fixed-method, acceptance-condition, artifact, literal, format, approval, budget, and deadline requirement survives inside the copyable prompt, or unchanged original task in a valid no-change case.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Item D68

### Check B3

B3. Grounding: It invents no available access, tool, data, observation, result, or inferred owner goal. Unconfirmed dependencies get first checks. Inferred goals are marked as assumptions in the prompt. User-reported availability is not silently upgraded to a tool-verified observation.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

## G30

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

### Item D34

### Check B5

B5. Contribution: Every selected lens changes a real outcome, practice, or check for a stated benefit. Every borrowed field adds a method and contribution. No persona, team-size, adversary, or instrument quota substitutes for a contribution.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

## G31

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

### Item D36

### Check B6

B6. Authority: Added scope, new access, paid steps, and irreversible actions are conditional on approval inside the prompt, not only in commentary. Explicitly prohibited expansions remain prohibited. A response with no expansion passes without needing an irrelevant approval ritual.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Item D67

### Check B3

B3. Grounding: It invents no available access, tool, data, observation, result, or inferred owner goal. Unconfirmed dependencies get first checks. Inferred goals are marked as assumptions in the prompt. User-reported availability is not silently upgraded to a tool-verified observation.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

## G32

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

### Item D38

### Check T12a

T12a. The prompt keeps the fixed scope, methods, and acceptance condition as written. Each repair sits on its own "With my approval only:" line. Nothing outside the 2 loopholes is added: no new analysis, experiment, metric, threshold, fold scheme, or operational step, gated or not.

### Item D65

### Check B2

B2. Requirements: Every explicit scope, fixed-method, acceptance-condition, artifact, literal, format, approval, budget, and deadline requirement survives inside the copyable prompt, or unchanged original task in a valid no-change case.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

## G33

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

### Item D39

### Check B3

B3. Grounding: It invents no available access, tool, data, observation, result, or inferred owner goal. Unconfirmed dependencies get first checks. Inferred goals are marked as assumptions in the prompt. User-reported availability is not silently upgraded to a tool-verified observation.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Item D45

### Check B6

B6. Authority: Added scope, new access, paid steps, and irreversible actions are conditional on approval inside the prompt, not only in commentary. Explicitly prohibited expansions remain prohibited. A response with no expansion passes without needing an irrelevant approval ritual.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

## G34

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

### Item D40

### Check B3

B3. Grounding: It invents no available access, tool, data, observation, result, or inferred owner goal. Unconfirmed dependencies get first checks. Inferred goals are marked as assumptions in the prompt. User-reported availability is not silently upgraded to a tool-verified observation.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Item D58

### Check B2

B2. Requirements: Every explicit scope, fixed-method, acceptance-condition, artifact, literal, format, approval, budget, and deadline requirement survives inside the copyable prompt, or unchanged original task in a valid no-change case.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

