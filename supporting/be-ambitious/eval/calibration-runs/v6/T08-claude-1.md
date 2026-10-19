```text
Evaluate whether our churn model gives analysts a useful early-warning signal, and give analysts a conclusion they can act on: rely on the model's flags over the baseline's, do not, or the evidence does not establish improvement.
Assumption: analysts will use this result to decide whether to act on the model's flags instead of the baseline's. So the report also states the result in their terms: at the approved recall threshold, how many flagged customers analysts review per true churner for each model (1 / precision), with its uncertainty.

Scope and fixed requirements (unchanged):
- Offline evaluation only. Use the supplied de-identified training set and the untouched later-period holdout, split by customer to prevent leakage.
- Reproduce the current model and its baseline.
- Test the onboarding explanation from the raw events.
- Check calibration and subgroup errors.
- Have an independent analyst audit leakage and the conclusion against a written rubric.
- Do not tune on the holdout.
- Report uncertainty and missed targets.

First checks, before any modeling:
- Confirm access to the training set, the holdout, the raw events, and the existing evaluation runner.
- Confirm the approved recall threshold value, the baseline's definition, and the written onboarding explanation under test.
- Confirm that an independent analyst who did not build the model is available.
- Name any missing dependency, and continue only with work the available artifacts support.
- Run the evaluation runner's customer-separation check on the train/holdout split. Record the customer overlap count, which must be zero, and confirm that every holdout row falls in the later period.
- Record how the runner computes its confidence interval, for example whether it resamples customers or rows. Do not change the runner.

Protocol:
1. Freeze before the holdout.
   - Write a short analysis plan using the training period only. It covers the model and baseline configurations, the onboarding hypothesis and its test, the calibration checks, and the predefined subgroups.
   - Record the date and a hash of the plan and the code.
   - Open the holdout once, after the freeze, and run the frozen plan on it without revision.
   - Report any change made after seeing holdout results as exploratory, and leave its claim unverified.
2. Reproduce.
   - Retrain the current model and the baseline on the training set with their documented configurations.
   - Compare reproduced metrics with the recorded ones, and explain any gap.
   - Do all development and diagnostics with customer-grouped cross-validation inside the training period.
3. Test the onboarding explanation.
   - Rebuild the onboarding measures directly from the raw events, not from derived feature tables.
   - For each customer, check that every event used comes before the prediction point and none falls in or after the churn label window.
   - Test the stated explanation: does the rebuilt measure relate to churn the way the explanation claims, does it agree with the model's onboarding feature, and does the relationship hold within the predefined subgroups?
   - Develop the test on the training set, then confirm it once on the holdout under the frozen plan. A claim supported in training but not confirmed on the holdout is reported as unconfirmed.
4. Check calibration.
   - For both models on the holdout, report a reliability curve over binned predicted risk, the Brier score, and the calibration intercept and slope, each with customer-level bootstrap intervals.
   - State whether analysts can read predicted risk as a probability, and where each model is over- or under-confident.
5. Check subgroup errors.
   - For each predefined subgroup, report counts, plus precision and recall for both models at the approved threshold, and the difference with its interval.
   - Flag subgroups too small for a stable estimate instead of drawing conclusions from them.
   - Note that many subgroup comparisons will show some differences by chance.
6. Report uncertainty.
   - Report the runner's 95% interval for the precision difference.
   - Alongside it, report a paired bootstrap that resamples customers, as a sensitivity check that does not change the pass condition. Customers have several rows each, so resampling rows can make the interval too narrow.
   - If the two intervals disagree on whether zero is excluded, say so plainly.
7. Independent audit.
   - Give the independent analyst the frozen plan, code, runner output, and draft conclusion.
   - The analyst scores each rubric item below pass or fail, with notes:
     a. Customer IDs are disjoint across training and holdout, and the holdout is entirely later-period.
     b. Every feature, including the rebuilt onboarding measures, uses only data available at the prediction point, and each label window starts after its feature cutoff.
     c. No preprocessing step (scaling, encoding, imputation, feature selection) was fit on holdout data. The score cutoff that reaches the approved recall is computed the same way for both models, as the runner defines it.
     d. The baseline received the same data, split, and evaluation as the current model.
     e. The plan was frozen before the holdout was opened, and every post-freeze change is labeled exploratory.
     f. The conclusion follows from the judge's numbers and interval, does not overstate the subgroup or onboarding findings, and lists every missed target.
   - The analyst also tries to break the conclusion. They name the most plausible way the result could be an artifact, such as a leakage path, a shift between periods, or one subgroup dominating the result, and then check it.
   - The audit passes only if every rubric item passes. Report any failed item with the analyst's notes.

Report:
- Reproduction results and the separation check.
- Holdout precision at the approved recall for both models, the difference, and its 95% interval.
- Reviews per true churner for each model.
- Onboarding, calibration, and subgroup findings, each labeled confirmed, unconfirmed, or exploratory.
- The audit verdict, with notes.
- Every missed target.

With my approval only: measure lead time. For true churners flagged at the approved threshold, report the time from first flag to churn, compared between the two models, separately from the pass condition.

Judge: the existing evaluation runner must reproduce the baseline, enforce customer separation, and show holdout precision at the approved recall threshold above the baseline with a 95% confidence interval for the difference excluding zero. Otherwise report that the evidence does not establish improvement. Report the independent analyst's rubric verdict next to the judge's result. The pass condition stays exactly as written.
```

- `altitude`: The original outcome was an offline evaluation verdict. The improved one is a verdict analysts can act on: reviews per true churner, derived from the same precision metric. No scope change.
- `altitude`: Lead-time measurement is behind approval. It speaks directly to "early warning", which the judge's metric doesn't capture. It adds a new metric, so it needs your sign-off, since you fixed the methods.
- `depth`: The onboarding test is rebuilt from raw events, with point-in-time checks against the prediction point and the label window. It is developed on training and confirmed once on the holdout. This tests the explanation the task rests on, without tuning on the holdout.
- `depth`: Calibration is made concrete: reliability curve, Brier score, and calibration intercept and slope, with customer-level intervals. This stays within "check calibration".
- `depth`: A customer-resampled paired bootstrap runs alongside the runner's interval as a sensitivity check. It exposes a CI that is too narrow if the runner resamples rows. The pass condition is unchanged.
- `range` (clinical trials): A pre-registered, hashed analysis plan and a single holdout opening. This turns "do not tune on the holdout" into something the auditor can verify, and separates confirmed claims from exploratory ones.
- `range` (red team / audit): A written six-item rubric with pass/fail scoring and a required attempt to break the conclusion. This makes the independent audit a real judge for leakage and overclaiming.
- Skipped: a hard target, because this evaluates a fixed model under a no-holdout-tuning rule, and a stretch metric would invite tuning. Also skipped: live pilots and parallel trials, which are outside the offline-only scope.
- Owner actions:
  - Supply the approved recall threshold value, the baseline definition, and the written onboarding explanation.
  - Confirm runner and raw-event access.
  - Name the independent analyst.
  - Decide on the lead-time approval line.
