```text
Goal: determine, with evidence, whether our churn model gives analysts a useful early-warning signal. "Useful" here means it flags at-risk customers early enough, accurately enough, and in volumes analysts can act on.
Assumption: analysts use the flags to decide which customers to contact. Confirm this with the owner. If it is wrong, adjust the secondary analyses only, never the acceptance test.

Scope, methods, and acceptance conditions (keep unchanged):
- Offline evaluation only.
- Use the supplied de-identified training set and the untouched later-period holdout, split by customer to prevent leakage.
- Reproduce the current model and its baseline.
- Test the onboarding explanation from the raw events.
- Check calibration and subgroup errors.
- Have an independent analyst audit leakage and the conclusion against a written rubric.
- Do not tune on the holdout.
- Report uncertainty and missed targets.

First checks. Before any analysis, report each item as available, missing, or unverified:
- Inputs: training set, holdout, raw events, current model code and artifacts, baseline definition, existing evaluation runner, the approved recall threshold value, and a written statement of the onboarding explanation.
- Subgroup attributes: which ones survive de-identification.
- Holdout label maturity: whether every holdout customer has a complete churn outcome window.
- Analyst: whether an independent analyst is available.
- Holdout status: what evidence shows it is untouched (access logs, file hashes, a list of who has opened it). If you cannot confirm it, say so.
- Runner behavior: how it sets the operating point at the approved recall threshold, and which CI method it uses. Record both without changing them.
Name every missing dependency. Continue only with work the available artifacts support.

Phase 1: freeze everything before the holdout is opened (training set only; all results here are development evidence)
1. Reproduce. Run the existing runner on the training set with customer-grouped cross-validation to reproduce the model and the baseline. Record versions, seeds, and data hashes. Any gap from previously reported numbers is a finding.
2. Point-in-time audit from raw events. The customer split blocks identity leakage but not temporal leakage, so check these:
   - Every feature can be computed from events timestamped before the prediction cutoff.
   - The churn label window starts after the feature window ends.
   - No feature is a proxy for the outcome, such as cancellation-flow or billing-stop events.
3. Validate the judge. On a copy of the training data (never the holdout):
   - Plant one customer on both sides of the split. The runner's separation check must fail. On the clean split it must pass.
   - Train on permuted labels in grouped CV. Precision at the approved recall threshold should fall to roughly the churn base rate. If it does not, the pipeline leaks.
4. Test the onboarding explanation.
   - Rebuild the onboarding features directly from raw events and compare them with the engineered features.
   - Test the explanation with a grouped-CV ablation: the model with versus without the onboarding features.
   - Stratify by the signup cohort, tenure, acquisition channel, and plan attributes that are available. This shows whether the onboarding signal holds within strata or only stands in for cohort or tenure.
   - Before the holdout is opened, write down the explanation's specific, falsifiable prediction for the holdout, including the minimum effect that would count as support.
   - Describe all results as predictive association, not causal effect.
5. Hunt for errors. Use the CV folds to find the segments where errors concentrate (subgroup, tenure, plan, activity level). Turn the strongest into a short list of hypotheses, each with a predicted direction.
6. Freeze the plan. Write an analysis plan and freeze it together with the model. It must contain:
   - the primary test (the judge below)
   - the secondary metrics
   - the subgroup list, with a minimum sample size for each
   - the hypotheses from step 5
   - the onboarding prediction from step 4
   - the analyst's rubric. The rubric must cover temporal and identity leakage, holdout access, reproduction gaps, uncertainty reporting, and whether the conclusion follows from the evidence.
   Record a hash and timestamp for the frozen plan and model. Give the rubric to the analyst before any holdout result exists.

Phase 2: score the holdout once
7. Run the existing evaluation runner on the holdout with the frozen model and baseline. Log every holdout run, and report any rerun with its reason.
8. Primary result: holdout precision at the approved recall threshold, model versus baseline, with the runner's 95% CI for the difference.
9. Secondary results. Report these, but do not use them for acceptance:
   - Calibration: reliability diagram, calibration intercept and slope, Brier score, and Brier skill score versus the baseline.
   - Decision value: decision curve analysis, showing net benefit across a range of contact-cost thresholds, compared against "contact everyone" and "contact no one". Also report alert volume per week at the approved operating point, compared with analyst capacity if it is known.
   - Lead time: for true positives, the time from first flag to churn (distribution and median). Add Kaplan–Meier churn curves by risk decile, treating customers with incomplete outcome windows as censored.
   - Subgroups: precision, recall, and calibration for each pre-registered subgroup, with 95% CIs. Mark groups below their minimum size as uninformative rather than reporting them as findings.
   - Sensitivity: if customers have multiple rows, run a customer-level cluster bootstrap of the precision difference outside the runner, as a cross-check on the runner's CI.
   - Pre-registered items: mark each hypothesis and the onboarding prediction as confirmed, refuted, or inconclusive. Label any pattern first seen on the holdout as exploratory and unconfirmed.
10. Independent audit. The analyst audits leakage (Phase 1 steps 2–3 and the holdout access log) and whether the conclusion follows from the evidence, scoring against the pre-written rubric. Do not give them your verdict beforehand. Include their findings verbatim.

Report contents:
- the verdict under the judge
- every primary and secondary result with its uncertainty
- every missed target and missing dependency
- any reproduction gaps
- the analyst's audit
- a plain statement of what analysts should and should not do with the flags, given these results

With my approval only: link any data beyond the supplied de-identified sets, such as demographic or CRM attributes, to extend the subgroup analysis.
With my approval only: modify the existing evaluation runner, or add these checks to CI.
With my approval only: design a prospective shadow-mode run or a randomized retention pilot to measure whether acting on flags reduces churn (uplift). Offline evaluation cannot show this.

Judge: the existing evaluation runner must reproduce the baseline, enforce customer separation, and show holdout precision at the approved recall threshold above the baseline with a 95% confidence interval for the difference excluding zero. Otherwise report that the evidence does not establish improvement. Separately, the independent analyst's rubric-based audit judges leakage and whether the conclusion follows from the evidence. Your own review does not substitute for that audit. Secondary analyses inform the report but do not change the verdict.
```

- `altitude`: the original outcome was a model-vs-baseline verdict. The improved outcome also tells analysts whether to act on the flags: how far ahead they warn (lead time), whether acting on them beats contacting everyone or no one (decision curves), and how many alerts arrive per week. These are reported as secondary results, and the acceptance test is unchanged. Setup needed: event timestamps, churn dates, and analyst capacity if known.
- `depth`: freezing the analysis plan, the model, and the rubric before opening the holdout makes "do not tune on the holdout" checkable and keeps the analyst's rubric independent of the results. No scope effect.
- `depth`: the point-in-time audit from raw events catches temporal and label-proxy leakage, which a customer split does not prevent.
- `depth`: the onboarding test gains a feature rebuild from raw events, an ablation, cohort and tenure stratification, and a falsifiable prediction written before the holdout. Results are framed as association, not cause.
- `depth`: the new-finding move. Error segments are found on CV folds, pre-registered, and tested once on the holdout. Anything first seen on the holdout is labeled exploratory.
- `range` (software testing / red team): a planted cross-split customer and a permuted-label run show that the judge can actually fail. Both use a copy of the training data, so the holdout is not touched.
- `range` (clinical prediction modeling): calibration slope and intercept, decision curve analysis, and per-subgroup CIs with minimum sizes guard against reading noise in small groups as findings.
- `range` (survival analysis): lead-time distributions and Kaplan–Meier curves that handle censoring cover the "early" in early warning, which immature holdout outcome windows would otherwise bias.
- `range` (statistics): the customer-level cluster bootstrap cross-checks the runner's CI without changing the runner.
- Approval lines: linking extra data, changing the runner or CI, and a prospective or uplift pilot. Each would move the work beyond offline scope or add new data access.
- Skipped: a hard-target stretch. This task evaluates the model rather than improving it, and a performance stretch would invite tuning.
- Owner actions:
  - Confirm the analyst-use assumption.
  - Supply the approved recall threshold, the written onboarding explanation, the baseline definition, and analyst capacity.
  - Confirm an independent analyst is available and how they will get data access.
  - Provide evidence that the holdout is untouched.
  - Decide on the three approval lines.
