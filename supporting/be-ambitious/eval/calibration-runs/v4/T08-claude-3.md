```text
Goal: decide, from offline evidence only, whether the current churn model gives analysts a useful early-warning signal. "Useful" means it beats the baseline under the judge below. As an assumption to confirm with me, it also means flagging at-risk customers early enough, and in volumes small enough, for analysts to act.

Fixed requirements (unchanged):
- Offline evaluation only.
- Use the supplied de-identified training set and the untouched later-period holdout, split by customer to prevent leakage.
- Reproduce the current model and its baseline.
- Test the onboarding explanation from the raw events.
- Check calibration and subgroup errors.
- Have an independent analyst audit leakage and the conclusion against a written rubric.
- Do not tune on the holdout.
- Report uncertainty and missed targets.
- If any judge condition fails, report that the evidence does not establish improvement.

First checks. Name any that fail, then continue only with work the available artifacts support.
1. Confirm the training set, holdout, and raw event logs are present, including event timestamps and churn dates. Confirm the holdout is from the later period and has not been used in development. Record file hashes and row and customer counts.
2. Confirm the existing evaluation runner executes. Document three things about it:
   - how it sets the operating point for the approved recall threshold;
   - how it enforces customer separation;
   - how it computes the 95% CI for the precision difference, including whether it resamples by customer.
3. Confirm the approved recall threshold value is documented.
4. Confirm the independent analyst is available and the written rubric exists. If the rubric is not finished, finalize it before any holdout result is seen.
5. List which subgroup fields the de-identified data actually contains. Do not join external data or attempt re-identification.

Method:
1. Pre-register before touching the holdout. Write a dated analysis plan and freeze it. It covers:
   - model and baseline specifications and features;
   - a supplementary operating threshold fixed on training data;
   - the primary metric (the judge) and secondary metrics;
   - subgroups, with minimum cell sizes;
   - the onboarding hypotheses in step 4.
   List any later deviation from the plan in the report.
2. Develop on training data only.
   - Use customer-grouped cross-validation (e.g., GroupKFold on customer ID) so no customer spans folds.
   - Add a time-ordered split inside the training period (fit on earlier, validate on later) to preview drift before the holdout.
3. Audit leakage from raw events.
   - For each feature, confirm from raw event timestamps that it was computable as of the prediction cutoff (point-in-time correctness).
   - Confirm that no label-derived or post-churn event feeds any feature.
   - Run adversarial validation: train a classifier on features alone to tell training rows from holdout rows. This measures drift without using holdout labels.
   - Red-team the judge with a mutation test. On a scratch copy built only from training data, inject customers on both sides of a split and confirm the runner rejects it. Then confirm it accepts the clean split.
4. Test the onboarding explanation as a hypothesis, not a premise.
   - Rebuild the onboarding features from raw events.
   - Test whether they add signal beyond tenure, plan, and signup cohort, using two methods: an ablation (model with versus without onboarding features) and grouped permutation importance across CV folds.
   - Verify that onboarding events precede the prediction cutoff.
   - Include a negative control, such as a shuffled or time-shifted onboarding feature, that should show no effect.
   - Training-data results are development evidence only. Confirm the pre-registered onboarding claim once on the holdout, or report it as unverified.
5. Measure early-warning usefulness. These results are supplementary and do not affect the judge. On the holdout, at the training-fixed threshold, report for both model and baseline:
   - realized recall and precision, and alerts per period;
   - lead time, meaning time from the prediction cutoff (or first alert, if the model scores repeatedly) to churn, summarized with Kaplan–Meier so customers whose outcome falls past the observation window are censored, not dropped;
   - customer-level bootstrap intervals for each comparison;
   - decision curve analysis: net benefit across thresholds, compared with "flag all" and "flag none", to show where the model is worth acting on.
   If I supply an analyst capacity figure, report whether alert volume fits it. Otherwise report volume and leave fit unassessed.
6. Check calibration. On the holdout, for both model and baseline, report:
   - a reliability diagram;
   - the Brier score with its Murphy decomposition (reliability, resolution, uncertainty), to separate miscalibration from weak discrimination;
   - calibration intercept and slope.
   Fit any recalibration on training data only and report it as a separate variant. Never select it on the holdout.
7. Check subgroup errors. For each pre-registered subgroup, report precision, recall, false-positive and false-negative rates, and calibration-in-the-large, each with a customer-bootstrap 95% interval.
   - Mark undersized cells as inconclusive; do not drop them.
   - Treat subgroup differences that were not pre-registered as exploratory, and note multiplicity.
8. Run the judge once on the holdout with the frozen plan.
9. Get the independent audit. Give the analyst the plan, code, leakage findings, results, and draft conclusion. The analyst scores leakage, and whether the conclusion follows from the evidence, against the written rubric. Include their findings and any disagreements verbatim.

Report, in this order:
1. The judge result: met or not, with the precision difference and its 95% CI.
2. Calibration and subgroup errors.
3. The onboarding verdict: confirmed, refuted, or unverified.
4. Early-warning metrics.
5. The auditor's findings.
6. All uncertainty, every missed target, and every deviation from the plan.
Follow TRIPOD reporting items where they apply.

With my approval only: modify the existing evaluation runner. Supplementary analyses go in separate scripts that read the same splits.
With my approval only: live scoring, analyst outreach, or a randomized retention trial to test whether alerts reduce churn.

Judge: the existing evaluation runner must reproduce the baseline, enforce customer separation, and show holdout precision at the approved recall threshold above the baseline with a 95% confidence interval for the difference excluding zero. Otherwise report that the evidence does not establish improvement. Customer separation counts as verified only if the mutation test fails on the injected-overlap copy and passes on the clean split. The onboarding verdict, lead time, decision-curve, and capacity results are reported separately and do not change this pass condition.
```

**Ledger**

- `altitude`: The original outcome was whether the model beats the baseline on precision at the approved recall. The improved outcome is whether its alerts arrive early enough, and in workable volume, for analysts to act. This is checked on the holdout with lead time, alert volume, and decision curves. The meaning of "useful" here is my assumption. It requires churn dates in the data and, optionally, an analyst capacity figure. Scope stays offline.
- `depth`: A dated, frozen pre-registration and a single holdout run turn "do not tune on the holdout" into something that can be checked. Deviations become visible.
- `depth`: A point-in-time feature audit from raw timestamps, plus adversarial validation, finds leakage and drift without using holdout labels.
- `depth`: The onboarding explanation is tested with an ablation, grouped permutation importance, and a negative control. Training results stay development evidence until the pre-registered claim is confirmed once on the holdout.
- `depth`: A training-fixed operating threshold shows how the model would actually perform when deployed. This is reported alongside the runner's metric and does not replace it.
- `range`: Survival analysis from epidemiology (Kaplan–Meier) handles lead time when churn falls past the observation window.
- `range`: Decision curve analysis from clinical prediction shows the threshold range where acting on alerts beats flagging everyone or no one.
- `range`: The Brier/Murphy decomposition from forecast verification separates miscalibration from weak discrimination.
- `range`: A mutation test, borrowed from software testing, red-teams the judge's customer-separation check. It runs on a scratch copy of training data only, so the holdout is untouched.
- `range`: TRIPOD reporting items make the report auditable by the independent analyst.
- Skipped lenses: none.
- Owner actions:
  - confirm that raw events, churn dates, and the approved recall value exist;
  - confirm the analyst's availability and the rubric;
  - supply an analyst capacity figure, or accept volume reported without a fit assessment;
  - confirm or reject the assumed meaning of "useful";
  - decide on the two approval-only lines (runner changes; live scoring or an outreach trial).
