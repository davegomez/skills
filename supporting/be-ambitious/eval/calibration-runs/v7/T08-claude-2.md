```text
Evaluate whether our churn model gives analysts a useful early-warning signal. The approved scope is offline evaluation only. Use the supplied de-identified training set and untouched later-period holdout, split by customer to prevent leakage. Reproduce the current model and its baseline, test the onboarding explanation from the raw events, check calibration and subgroup errors, and have an independent analyst audit leakage and the conclusion against a written rubric. Do not tune on the holdout. Report uncertainty and missed targets. Keep these scope, methods, and acceptance conditions unchanged.

Assumption: analysts will use the result to decide whether to trust the score when choosing which customers to act on. The question is whether the evidence supports that trust, not whether the model can be made to look good.

First checks, before any work. Record each result:
- The training set, the later-period holdout, and the raw event logs with timestamps are present and readable.
- The holdout has not been scored or inspected by anyone during model development. Record what evidence supports this, and say plainly where none exists.
- The approved recall threshold is written down, with its value and its source.
- The existing evaluation runner exists and can run. Record how it enforces customer separation and how it computes the 95% CI for the precision difference, including whether it resamples customers or rows and whether the comparison is paired on the same holdout customers.
- An independent analyst, other than the author, is available.
For each missing dependency, name it and continue only with the work the available artifacts support. Do not modify the runner.

Freeze the plan before the holdout is scored. Pre-registration is the standard way to keep an untouched holdout untouched. Using the training set only, write down and date these items:
- the reproduced model and baseline specifications;
- the subgroup definitions to report;
- the calibration binning;
- the onboarding explanation stated as a testable claim, with the raw-event measure that would support or contradict it;
- the written rubric for the independent analyst.
Changing any of these after the holdout results are seen counts as tuning on the holdout. If a change is unavoidable, report it as a deviation together with its reason.

Test the onboarding explanation from the raw events:
- Rebuild the onboarding measure directly from the raw event logs. Do not use the model's precomputed features.
- Confirm that every event used falls before each customer's prediction time.
- Treat any pattern found while exploring the training set as development evidence. Confirm it only on the holdout, using the frozen test, or report it as unverified.

Blinded audit, borrowed from blinded outcome assessment in clinical trials:
- The independent analyst first audits leakage against the frozen rubric before seeing any holdout results. This audit covers customer overlap, post-cutoff events, target-derived features, and period overlap between training and holdout.
- The analyst then audits the conclusion against the same rubric.
- Report both verdicts and every rubric criterion that was not met.

Report:
- Uncertainty for every headline number, including calibration and each subgroup error estimate. Do not claim subgroup differences that the intervals do not support.
- The runner's CI method as recorded in the first checks.
- Missed targets.
- Every deviation from the frozen plan.

Judge: the existing evaluation runner must reproduce the baseline, enforce customer separation, and show holdout precision at the approved recall threshold above the baseline with a 95% confidence interval for the difference excluding zero. Otherwise report that the evidence does not establish improvement. The result stays unverified until the runner has run on the untouched holdout.
```

**Ledger**
- `depth`: Pre-register the analysis on the training set before scoring the holdout.
  - Source fact: the task says "do not tune on the holdout," but it leaves the subgroups, the calibration bins, the onboarding test, and the rubric unspecified.
  - Defect: if any of those are chosen after the holdout errors are seen, the holdout is tuned through the analysis choices.
  - Repair: freeze those choices first. Methods, metrics, and acceptance stay unchanged.
  - Cost: one planning pass before scoring.
- `depth`: Rebuild the onboarding measure from raw events with a point-in-time check, and confirm it only on the holdout.
  - Source fact: the task requires testing the onboarding explanation "from the raw events."
  - Defect: an explanation formed and tested on the same data, or built from post-cutoff events, confirms nothing.
  - Repair: rebuild from raw events, check event timing, and treat training-set patterns as development evidence. This uses the holdout without tuning on it.
- `range`: Blinded outcome assessment from clinical trials. The independent analyst audits leakage before seeing any holdout results.
  - Source fact: the task requires an independent audit of both leakage and the conclusion.
  - Defect: an auditor who already knows the result can be swayed by it when judging leakage.
  - Repair: sequence the existing audit. No new reviewer or access is needed.
- First checks: confirm the recall threshold value, the holdout's untouched status, and the runner's CI resampling unit and pairing.
  - Source fact: the judge depends on "the approved recall threshold" and a 95% CI, and neither is specified in the task.
  - Repair: record them before the work. The runner and the judge stay unchanged.
- Skipped:
  - `altitude`: moving toward a live pilot or contact workflow would break the fixed offline-only scope.
  - Hard target: acceptance is fixed, and this is an evaluation, not a model-improvement task.
  - Red-team field: the independent audit already covers it.
- Owner actions:
  - Supply or confirm the approved recall threshold.
  - Confirm the holdout has not been touched.
  - Confirm how the runner computes its CI. If it resamples rows rather than customers, decide whether that limitation is acceptable, since the runner itself is not to be modified.
  - Name the independent analyst.
