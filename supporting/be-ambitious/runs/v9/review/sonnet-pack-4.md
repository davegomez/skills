# Blind review pack, grouped

Each group shows one task and one output once, then the items to grade for that output. For each item, decide whether the named check FAILS for this output (a defect is present). Use the rubric text quoted in the item and INTERPRETATIONS.md. Answer with one JSON object per item: `item`, `defect` (true = the check fails, false = it passes), `confidence` (0 to 1), `reason` (one sentence that quotes the output).

## G35

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

### Item D42

### Check B6

B6. Authority: Added scope, new access, paid steps, and irreversible actions are conditional on approval inside the prompt, not only in commentary. Explicitly prohibited expansions remain prohibited. A response with no expansion passes without needing an irrelevant approval ritual.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

## G36

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

### Item D47

### Check T11d

T11d. Any rebuild, framework change, or paid service is behind approval.

Applicability note for this case: The task's “about 10 seconds to load” is a user report, not an established LCP, percentile, device profile, or measured baseline. A prompt may choose a named metric and stretch, but must establish the corresponding baseline before claiming improvement. Any LCP target below 2.5 s passes T11b; do not require a specific value such as 200 ms. A target on another metric passes T11b only if it lies past that metric's "good" threshold. A before/after comparison must use a comparable metric and profile.

## G37

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

### Item D48

### Check B3

B3. Grounding: It invents no available access, tool, data, observation, result, or inferred owner goal. Unconfirmed dependencies get first checks. Inferred goals are marked as assumptions in the prompt. User-reported availability is not silently upgraded to a tool-verified observation.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

## G38

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

### Item D49

### Check B4

B4. Judge: A changed prompt ends with task-specific independent evidence and an observable pass condition. Proposed or unavailable validation remains unverified until run. The model's own confidence does not count as the judge.

Applicability for this case: Changed. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

## G39

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

### Item D50

### Check B6

B6. Authority: Added scope, new access, paid steps, and irreversible actions are conditional on approval inside the prompt, not only in commentary. Explicitly prohibited expansions remain prohibited. A response with no expansion passes without needing an irrelevant approval ritual.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Item D52

### Check T12a

T12a. The prompt keeps the fixed scope, methods, and acceptance condition as written. Each repair sits on its own "With my approval only:" line. Nothing outside the 2 loopholes is added: no new analysis, experiment, metric, threshold, fold scheme, or operational step, gated or not.

### Item D54

### Check B2

B2. Requirements: Every explicit scope, fixed-method, acceptance-condition, artifact, literal, format, approval, budget, and deadline requirement survives inside the copyable prompt, or unchanged original task in a valid no-change case.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

## G40

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

### Item D53

### Check T11d

T11d. Any rebuild, framework change, or paid service is behind approval.

Applicability note for this case: The task's “about 10 seconds to load” is a user report, not an established LCP, percentile, device profile, or measured baseline. A prompt may choose a named metric and stretch, but must establish the corresponding baseline before claiming improvement. Any LCP target below 2.5 s passes T11b; do not require a specific value such as 200 ms. A target on another metric passes T11b only if it lies past that metric's "good" threshold. A before/after comparison must use a comparable metric and profile.

## G41

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

### Item D55

### Check T11d

T11d. Any rebuild, framework change, or paid service is behind approval.

Applicability note for this case: The task's “about 10 seconds to load” is a user report, not an established LCP, percentile, device profile, or measured baseline. A prompt may choose a named metric and stretch, but must establish the corresponding baseline before claiming improvement. Any LCP target below 2.5 s passes T11b; do not require a specific value such as 200 ms. A target on another metric passes T11b only if it lies past that metric's "good" threshold. A before/after comparison must use a comparable metric and profile.

## G42

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

### Item D57

### Check T11d

T11d. Any rebuild, framework change, or paid service is behind approval.

Applicability note for this case: The task's “about 10 seconds to load” is a user report, not an established LCP, percentile, device profile, or measured baseline. A prompt may choose a named metric and stretch, but must establish the corresponding baseline before claiming improvement. Any LCP target below 2.5 s passes T11b; do not require a specific value such as 200 ms. A target on another metric passes T11b only if it lies past that metric's "good" threshold. A before/after comparison must use a comparable metric and profile.

## G43

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

### Item D66

### Check B3

B3. Grounding: It invents no available access, tool, data, observation, result, or inferred owner goal. Unconfirmed dependencies get first checks. Inferred goals are marked as assumptions in the prompt. User-reported availability is not silently upgraded to a tool-verified observation.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

