```text
Evaluate whether our churn model gives analysts a useful early-warning signal. The approved scope is offline evaluation only. Use the supplied de-identified training set and untouched later-period holdout, split by customer to prevent leakage. Reproduce the current model and its baseline, test the onboarding explanation from the raw events, check calibration and subgroup errors, and have an independent analyst audit leakage and the conclusion against a written rubric. Do not tune on the holdout. Report uncertainty and missed targets. Keep these scope, methods, and acceptance conditions unchanged.

Assumption: "useful early-warning signal" is decided by the acceptance condition in the judge below. Lead time and analyst workflow are outside the approved methods and are not evaluated here.

First checks, before any work on the holdout. Name each missing or unconfirmed item, and continue only with work the available artifacts support:
- The existing evaluation runner runs. Record how it enforces customer separation, how it sets the operating point at the approved recall threshold, and how it computes the 95% confidence interval for the precision difference: paired or unpaired, and resampled by customer or by row.
- The training set, the holdout, and the raw events are present. Customer identifiers support the customer split, and holdout dates fall after training dates.
- The holdout is untouched: no earlier results, features, or thresholds derived from it are on record. If you cannot confirm this, say so in the report.
- The approved recall threshold is documented. The written rubric exists, or it is written and recorded before any holdout result is seen.
- An analyst other than you is available to do the audit.

Lock the analysis before scoring the holdout, the way a clinical trial locks its statistical analysis plan before unblinding:
- Freeze the current model, the baseline, their features, and the runner configuration. Record a version or checksum for each.
- Write the onboarding explanation as a testable claim: which onboarding events, measured over which window before the prediction date, should relate to churn, and in which direction.
- Name the subgroups for the error analysis and define the calibration check.
- Timestamp the lock. After the holdout is scored, change nothing. Report any idea the holdout prompts as a hypothesis for future data. Do not test it on this holdout.

Onboarding explanation from the raw events:
- Rebuild the onboarding measures directly from the raw event records. Use only events timestamped before each customer's prediction date, and compare the rebuilt measures with the model's derived onboarding features. Any feature that draws on later events is a leakage finding for the audit.
- Develop and probe the explanation on the customer-split training set. Then evaluate the locked claim once on the holdout. Label training-set results as development evidence and holdout results as confirmation.

Calibration and subgroup errors: report both on the holdout for the current model and the baseline. Give each estimate an uncertainty interval that resamples customers. Flag subgroups too small for a stable estimate; do not drop them.

Independent audit: give the analyst the locked plan, the rubric, the runner output, and the raw-event leakage checks. The analyst audits leakage and the conclusion against the rubric, including whether the runner's confidence interval treats the customer as the unit of resampling. Record each rubric item as met or not met, with its evidence.

Report:
- whether the baseline reproduced
- the customer-separation check
- holdout precision for both models at the approved recall threshold
- the difference between them, with its 95% confidence interval
- calibration and subgroup errors, with their uncertainty intervals
- the onboarding result, with development and confirmation evidence kept separate
- the audit findings
- every missed target
- every first check that failed or could not be confirmed

Judge: the existing evaluation runner must reproduce the baseline, enforce customer separation, and show holdout precision at the approved recall threshold above the baseline with a 95% confidence interval for the difference excluding zero. Otherwise report that the evidence does not establish improvement.
```

- `range` (clinical-trial analysis-plan lock): The task says "do not tune on the holdout" but does not say when the onboarding claim, the subgroups, the calibration check, or the rubric get fixed. If any of them is chosen after holdout results are seen, the holdout quietly becomes tuning data. The repair freezes all of them, timestamped, before scoring. No new analysis is added and the scope is unchanged.
- `depth` (raw-event leakage rebuild): The task asks to test the onboarding explanation "from the raw events" and to audit leakage. Derived onboarding features can silently include events after the prediction date. The repair rebuilds the measures under a strict timestamp cutoff and compares them with the model's features. This uses the approved methods and needs the raw events, which the task already supplies.
- `depth` (development vs. confirmation): The task does not say which data shapes the onboarding explanation. Shaping it on the holdout would violate the no-tuning rule. The repair develops it on the training split and confirms it once on the holdout, with each kind of evidence labeled.
- `depth` (customer as the unit of uncertainty): The task splits by customer and requires reported uncertainty. A row-level confidence interval would overstate certainty when customers have several rows. The repair adds a first check on how the runner computes its interval, customer-resampled intervals for calibration and subgroups, and an audit item on the interval's unit. The judge and its pass condition are unchanged.
- Skipped: `altitude`. Higher rungs, such as lead-time value, analyst workflow, or a pilot, need new metrics or live data, and the owner fixed offline-only scope and a closed method set. Also skipped: the hard-target move. This is an evaluation, and a stretch target would create pressure to tune.
- Owner actions:
  - Confirm runner access and its confidence-interval method.
  - Confirm the holdout is untouched.
  - Supply the approved recall threshold and the rubric, or decide who writes the rubric before unblinding.
  - Name the independent analyst.
  - Optionally, decide separately whether to commission a later lead-time or workflow evaluation.
