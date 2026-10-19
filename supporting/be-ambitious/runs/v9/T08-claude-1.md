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
