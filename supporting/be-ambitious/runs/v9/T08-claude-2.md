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
