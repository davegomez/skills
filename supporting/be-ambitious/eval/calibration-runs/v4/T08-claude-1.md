```text
Evaluate whether our churn model gives analysts a useful early-warning signal: one that ranks the right customers, arrives early enough to act on, and is honest about its probabilities and where it fails. The approved scope is offline evaluation only. Keep the scope, methods, and acceptance conditions below unchanged.

Assumption (inferred, confirm with the owner): analysts use the score to decide which customers to contact, have limited contact capacity, and need warning some time before churn. Treat the lead-time and capacity analyses below as supplementary to the judge, not as replacements for it.

First checks. Name any missing dependency and continue only with work the available artifacts support.
- Confirm access to the existing evaluation runner, the supplied de-identified training set, the untouched later-period holdout, and the raw event data behind both.
- Confirm the holdout is untouched: check access records or provenance notes, and report whatever you find.
- Locate the documented approved recall threshold, the baseline definition, and the current model's training configuration. Do not infer any of these from the holdout.
- Read how the runner enforces customer separation and how it computes the 95% confidence interval for the precision difference. If it resamples rows rather than customers, or splits by row anywhere, report that to the owner as a finding. Do not modify the runner or the judge.
- Confirm an independent analyst is available, and confirm the written rubric exists or will be written before any holdout result is seen.
- Find any documented analyst contact capacity or action window. If none exists, state the values you assume and show sensitivity across a range.

Freeze the plan before opening the holdout. Write and date an analysis plan that fixes:
- the primary comparison (holdout precision at the approved recall threshold, model vs. baseline), which is the judge;
- the supplementary metrics and subgroups;
- the onboarding hypotheses and the direction each predicts;
- the auditor's rubric.
Analyses not in the plan are labeled exploratory in the report.

Development, on training data only:
1. Reproduce the current model and its baseline. Rebuild features from the raw events where possible and confirm they match the supplied features. Report any discrepancy.
2. Use customer-grouped cross-validation (for example, GroupKFold by customer ID) for any development choice, including thresholds and calibration mappings. Do not tune on the holdout.
3. Point-in-time leakage checks:
   - Verify that every feature is computable from events before each prediction date.
   - Look for post-outcome signals: cancellation-flow events, billing-failure codes, support tags written at churn.
   - Run a shuffled-label control. The model should fall to chance.
   - Run a probe model trained only on suspicious features. High performance flags a leak.
4. Test the onboarding explanation from raw events, not from summary features or SHAP plots alone:
   - Reconstruct onboarding steps and completion timing per customer.
   - Compare churn rates and model scores across onboarding patterns within strata of tenure, plan, and acquisition cohort.
   - Run an ablation: retrain without the onboarding features and measure the loss.
   - Add a negative-control check: an onboarding-like feature that should not predict churn.
   Treat anything found here as development evidence. Confirm only pre-registered onboarding claims on the holdout. Leave any other claim unverified.

Holdout, scored once with the frozen model, baseline, and plan:
5. Run the existing evaluation runner for the judge.
6. Calibration:
   - reliability diagram;
   - Brier score with its reliability/resolution decomposition;
   - calibration intercept and slope;
   - observed vs. predicted churn by score decile.
7. Subgroup errors, for each pre-registered subgroup (for example plan, tenure band, region, acquisition channel, onboarding pattern):
   - precision, recall, and calibration, each with customer-level bootstrap confidence intervals and the subgroup size;
   - a flag for subgroups too small to support a conclusion;
   - a correction for multiple comparisons, applied to any claimed difference.
8. Early-warning usefulness (supplementary):
   - Lead time: distribution of days between first alert and churn, treating customers who have not churned by the end of the holdout as censored. Use Kaplan–Meier or similar survival methods rather than dropping them.
   - Precision and churners caught at the stated or assumed analyst capacity (alerts per analyst per period).
   - A decision curve showing net benefit vs. the baseline and vs. contacting everyone or no one, across a range of contact-cost/benefit ratios.
   - Report each of these as observed holdout results without changing the judge.

Independent audit. The independent analyst audits leakage and the conclusion against the written rubric. The rubric covers at least:
- customer separation;
- point-in-time feature validity;
- holdout integrity;
- whether the reported conclusion follows from the judge's result;
- whether the onboarding claim is supported or only suggestive;
- whether calibration and subgroup caveats are stated.
As a red-team step, the auditor attempts to construct a leak-exploiting model or a split that inflates the result, and records what they tried and found. Report the rubric findings verbatim alongside the results.

Report:
- uncertainty for every estimate;
- every missed target, failed check, and unverified claim;
- development vs. confirmatory evidence, kept separate;
- assumptions, with sensitivity.

With my approval only: run a prospective shadow-mode trial where analysts see scores without acting, to measure real lead time and alert volume.
With my approval only: run a randomized outreach pilot to measure whether contacting flagged customers changes retention (uplift), which this offline evaluation cannot establish.
With my approval only: change the evaluation runner or its CI configuration, including adding supplementary metrics to it.

Judge: the existing evaluation runner must reproduce the baseline, enforce customer separation, and show holdout precision at the approved recall threshold above the baseline with a 95% confidence interval for the difference excluding zero. Otherwise report that the evidence does not establish improvement. Supplementary analyses (lead time, capacity, decision curve, onboarding confirmation) are reported as observed holdout results and audited against the rubric. They do not alter the pass condition. Any claim not pre-registered and confirmed on the holdout remains unverified.
```

- `altitude`: The original outcome is "the model beats the baseline at the approved recall." The improved outcome is "analysts know whether the warning arrives early enough and fits their contact capacity." This adds lead-time survival analysis, precision at capacity, and a decision curve, all offline on the same holdout. The judge is unchanged. Capacity may need an assumed value with a sensitivity range.
- `depth`: Rebuilding features from raw events, point-in-time checks, shuffled-label and probe-model controls, and an onboarding test with strata, ablation, and a negative control all test the explanation instead of describing it. Freezing the plan before the holdout separates development evidence from confirmatory evidence. This costs analyst time and adds no new access.
- `depth`: A first check on how the runner computes its CI. Row-level resampling would overstate certainty. Any problem is reported to the owner, not fixed, so the judge stays unchanged.
- `range`: Clinical prediction methods (calibration slope and intercept, decision curve analysis) show whether the scores support decisions, not just rankings.
- `range`: Survival analysis handles censored non-churners, so lead time isn't biased.
- `range`: Epidemiology-style stratification and negative controls guard against confounding in the onboarding claim.
- `range`: The red-team audit, where the auditor tries to build a leak-exploiting model, tests the most consequential failure mode.
- Skipped: no hard stretch target. The fixed acceptance condition and the lack of a stated precision figure leave no comparable target to set, and setting one risks pressure to tune toward it.
- Owner actions:
  - confirm the approved recall threshold, the baseline definition, holdout provenance, runner access, and auditor availability;
  - supply analyst capacity and action-window figures, or accept assumed ranges;
  - confirm the inferred early-warning goal;
  - decide on the three approval-only lines (shadow trial, randomized outreach pilot, runner changes).
