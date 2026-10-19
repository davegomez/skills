```text
Evaluate whether our churn model gives analysts a useful early-warning signal, and deliver a decision memo they can act on. The memo states the verdict and what an alert at the approved recall threshold means: holdout precision, meaning the share of alerts that are true churners, with its 95% interval. It also states whether scores can be read as churn probabilities, the subgroups where the signal is weaker or fails, and whether the onboarding explanation held up.
Assumption: the memo's readers are the analysts who would act on alerts and whoever decides whether they should rely on the model.

Fixed requirements (unchanged):
- Scope is offline evaluation only.
- Use the supplied de-identified training set and the untouched later-period holdout, split by customer to prevent leakage.
- Do not tune on the holdout.
- Methods are closed: reproduce the current model and its baseline; test the onboarding explanation from the raw events; check calibration and subgroup errors; have an independent analyst audit leakage and the conclusion against a written rubric. Add no other analyses, experiments, or metrics.
- Report uncertainty and missed targets.
- Keep these scope, methods, and acceptance conditions unchanged.

First checks (name anything missing, then continue only with work the available artifacts support):
- Locate the existing evaluation runner. Record how it enforces customer separation, how it sets the threshold for the approved recall, and how it computes the 95% CI for the precision difference. Check whether it resamples customers, pairs both models on the same resamples, and recomputes thresholds per resample. If it does not, report that as a limitation. Do not change the judge.
- Confirm the documented value of the approved recall threshold.
- Confirm that raw events exist for both the training and holdout periods.
- Confirm the prediction cutoff and the label window definitions.
- Confirm who the independent analyst is.
- Confirm the subgroup fields present in the supplied data.

Before anyone opens the holdout:
- Write the analysis plan. Freeze the model artifact, the baseline, the feature code, the threshold rule, the subgroup definitions, the onboarding predictions below, and random seeds. Record their hashes and the time.
- Draft the written rubric and get the owner's sign-off on it before any holdout result exists. All model and explanation work up to this point uses the training set only, with customer-grouped cross-validation. Treat it as development evidence.
- Log every holdout run. One confirmatory run is the plan. Report any additional runs and the reason for each.

Reproduce:
- Retrain or reload the current model and the baseline from the supplied training set using the runner.
- Show that the baseline's training-CV and holdout numbers match its documented values, or report the gap and its likely cause.
- Confirm that customer IDs in the training and holdout sets are disjoint.
- Confirm that no feature uses events after the prediction cutoff.

Onboarding explanation (test the belief from raw evidence):
1. Rebuild the onboarding features directly from the raw event logs. Show that they match the engineered features, and report the mismatch rate.
2. Write down falsifiable predictions on training CV before the holdout run:
   (a) Permuting the onboarding features across customers lowers precision at the approved recall.
   (b) The onboarding association with churn holds within tenure or signup-cohort strata, if those fields exist, rather than only across them. This guards against onboarding being a proxy for account age or cohort.
3. Test the predictions once on the holdout with the frozen code. Patterns first seen on the holdout are reported as unconfirmed. Do not use them to revise the explanation.

Calibration:
- On training CV and on the holdout, plot a reliability curve of binned predicted versus observed churn, and report calibration-in-the-large. Compare the two periods to show whether calibration drifted.
- Do not recalibrate. Report whether analysts can read scores as probabilities.

Subgroup errors:
- For each pre-declared subgroup, report holdout precision and recall at the approved threshold, the customer count, and customer-resampled 95% intervals.
- Label subgroup results as descriptive, because there are many comparisons and no correction.
- Flag subgroups too small to support any estimate.

Independent audit:
- The analyst works from the frozen artifacts and the holdout run log, and scores the work against the signed-off rubric.
- Rubric leakage items:
  - Customer IDs are disjoint across the split.
  - Feature timestamps fall at or before the prediction cutoff.
  - The label window starts after the cutoff.
  - No features are derived from label-adjacent events, such as cancellation-flow activity.
  - The model and the baseline are scored on identical customers.
  - The holdout access count matches the log.
- Rubric conclusion items:
  - The verdict follows the judge.
  - Uncertainty is stated.
  - Missed targets are listed.
  - The onboarding claim matches the confirmatory evidence.
  - Subgroup caveats are present.
- The analyst also tries to break the conclusion by proposing the strongest alternative explanation for any measured lift. The memo records whether the evidence rules that explanation out.

Report:
- Decision memo as described above.
- Holdout precision for the model and the baseline at the approved recall, the difference and its 95% CI, and the judge verdict.
- Calibration, subgroup, and onboarding results, each marked confirmed (holdout), development-only (training CV), or unverified.
- The audit's rubric scores and findings.
- Every missed target and every runner limitation found in the first checks.

Judge: the existing evaluation runner must reproduce the baseline, enforce customer separation, and show holdout precision at the approved recall threshold above the baseline, with a 95% confidence interval for the difference excluding zero. Otherwise report that the evidence does not establish improvement. The independent analyst's rubric audit is reported alongside the verdict. Any failed leakage item is stated in the verdict line.
```

- `altitude`: The original outcome was a pass/fail on holdout precision. The improved outcome is a decision memo that tells analysts whether to act on an alert and where not to trust it, built only from the approved analyses and checked by the rubric's conclusion items. There is no scope or access change.
- `depth`: The plan is frozen and hashed before the holdout opens, and access is logged. This makes "do not tune on the holdout" auditable. It costs a short planning step before any results.
- `depth`: The prompt checks whether the runner's CI resamples customers, pairs both models, and recomputes thresholds per resample. This exposes a CI that is too narrow without altering the judge.
- `depth`: The onboarding test rebuilds the features from raw events and checks pre-written permutation and within-cohort predictions. They are developed on training CV and confirmed once on the holdout. The test hinges on tenure or cohort fields existing in the data.
- `range`: From forecast verification, it adds reliability curves and drift between periods, which shows whether scores read as probabilities. From clinical trials, it adds pre-registration and rubric sign-off before results, which prevents moving the goalposts.
- `range`: From epidemiology, it adds stratifying by cohort to test whether onboarding is confounded with account age. From statistics, it labels subgroup results as descriptive, which prevents false subgroup alarms.
- `range`: Red-team: the analyst must propose and test the strongest alternative explanation for any lift. This protects the consequential "improves" claim. It adds some analyst time.
- Skipped: none. No stretch target was added, because the task evaluates a fixed model and tuning to beat a target would change it. No "With my approval only" lines, because every addition stays inside the offline scope and the closed method set.
- Owner actions:
  - Confirm the runner's location and how it computes the CI.
  - Confirm the approved recall threshold, the prediction cutoff, and the label window definitions.
  - Name the independent analyst.
  - Sign off on the rubric before the holdout run.
  - Decide what to do if the runner's CI turns out not to resample by customer.
