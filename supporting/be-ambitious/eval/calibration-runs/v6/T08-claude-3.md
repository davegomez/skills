```text
Evaluate whether our churn model gives analysts a useful early-warning signal, so they can decide whether to rely on it, with every claim traceable to raw evidence and its uncertainty stated.
Assumption: analysts will use the result to decide whether to trust the model's warnings over the baseline's, so the report must state plainly what the evidence does and does not establish.

Scope and fixed requirements (unchanged):
- The approved scope is offline evaluation only.
- Use the supplied de-identified training set and the untouched later-period holdout, split by customer to prevent leakage.
- Reproduce the current model and its baseline, test the onboarding explanation from the raw events, check calibration and subgroup errors, and have an independent analyst audit leakage and the conclusion against a written rubric.
- Do not tune on the holdout. Report uncertainty and missed targets.
- Keep these scope, methods, and acceptance conditions unchanged.

First checks, before any analysis. Report each as present or missing, and continue only with work the available artifacts support:
- The existing evaluation runner exists and runs, and you know how it enforces customer separation.
- The approved recall threshold is written down with its value.
- The training set, holdout, and raw event logs are present. Customer IDs are consistent across them, and event timestamps are available.
- There is a record showing the holdout has not been used for model development.
- Subgroup definitions exist, or someone with authority can supply them.
- An independent analyst is available who did not build the model and is not running this evaluation.

Method:
1. Lock the plan before opening the holdout. Write a short analysis plan, modelled on a clinical-trial statistical analysis plan, and save it with a timestamp before computing any holdout metric. It fixes:
   - the model and baseline artifacts, by hash
   - the recall threshold
   - the subgroups
   - the calibration checks
   - the confidence-interval method
   - the onboarding hypothesis
   - the auditor's rubric
   Anything changed after the holdout is opened is labelled a deviation and reported.
2. Reproduce on training data only. Rebuild the current model and baseline from the training set. Match their reported training or cross-validation metrics within a stated tolerance, and record any mismatch and its cause. Fit and select nothing on the holdout.
3. Check customer separation and timing from the raw data, beyond what the runner reports:
   - Count customer IDs that appear in both training and holdout. The expected count is zero; report the observed count.
   - For each feature, confirm it uses only events dated before that customer's prediction date.
   - List any feature built from data at or after the churn label date.
4. Run the onboarding explanation as a test with a development stage and a confirmation stage:
   - On the training set's raw events, state the onboarding claim as a specific, testable relationship, for example "customers who do not complete step X within N days churn at rate R versus R′".
   - Write the claim into the locked plan.
   - Then check it once on the holdout's raw events and report the effect with its 95% interval.
   - Training-set evidence is development evidence only. If the holdout does not support the claim, report it as not confirmed and do not revise it.
5. Compute the headline comparison with the existing runner, using the owner's metric:
   - Metric: holdout precision at the approved recall threshold, for the model and for the baseline.
   - Compute the 95% interval for the difference with a paired bootstrap that resamples whole customers, not rows. Rows from the same customer are correlated, so row-level resampling understates uncertainty.
   - In each bootstrap replicate, recompute the score cutoff that reaches the approved recall, separately for the model and the baseline.
   - Report the bootstrap count and seed.
6. Check calibration on the holdout, as in weather-forecast verification:
   - Produce a reliability diagram with binned predicted versus observed churn rates and their intervals.
   - Report calibration-in-the-large and calibration slope, overall and for each prespecified subgroup.
7. Check subgroup errors on the holdout:
   - For each prespecified subgroup, report its size, precision and recall at the approved threshold, and 95% intervals for both the model and the baseline.
   - Flag subgroups too small for a stable estimate.
   - Do not add subgroups after seeing the results. Any exploratory split is labelled exploratory and is not used in the conclusion.
8. Independent audit with a red-team role:
   - Give the auditor the locked plan, the code, and the raw data access needed to repeat checks 3 and 5. The auditor should not have to rely on the summary tables.
   - The rubric asks:
     a. Is there any customer overlap, and is any feature computed from data on or after the prediction or label date?
     b. Was the holdout touched before the plan was locked, or is any deviation unexplained?
     c. Does the confidence interval resample by customer?
     d. Does the written conclusion claim more than the judge result and intervals support, including for the onboarding explanation and the subgroups?
   - The auditor returns pass or fail on each item, with evidence, and an overall verdict: "conclusion supported" or "conclusion not supported".

Report:
- the reproduction results
- the separation and timing checks
- the headline difference with its 95% interval
- the onboarding test, labelled confirmed or not confirmed
- calibration and subgroup tables with their intervals
- the auditor's verdict for each rubric item
- a list of every missed target, failed check, deviation, and unverified result
State plainly what an analyst can and cannot rely on.

Judge: the existing evaluation runner must reproduce the baseline, enforce customer separation, and show holdout precision at the approved recall threshold above the baseline with a 95% confidence interval for the difference excluding zero. Otherwise report that the evidence does not establish improvement.
Report the auditor's verdict next to the judge result. If the audit finds leakage, say so and state that the judge result rests on leaky data.
```

**Ledger**
- `depth`: Lock a written analysis plan, with artifact hashes, before opening the holdout. This makes "do not tune on the holdout" checkable rather than asserted. Adds no scope.
- `depth`: Use a customer-level paired bootstrap, and recompute the cutoff that reaches the approved recall in every replicate for both models. Row-level resampling would give a falsely narrow interval. This specifies how to compute the owner's interval and does not change the judge.
- `depth`: Check customer overlap and feature timing from raw data, independent of the runner. This catches leakage the runner might not enforce.
- `depth`: Turn the onboarding explanation into a specific claim built from training events and checked once on the holdout, labelled confirmed or not confirmed. This separates development evidence from confirmation.
- `range`: Clinical-trial practice (locked analysis plan, prespecified subgroups, labelled deviations) guards against choosing results after seeing them.
- `range`: Forecast verification (reliability diagrams, calibration-in-the-large and slope by subgroup) shows whether warning probabilities mean what analysts will read them to mean. These are the instruments of the owner's calibration check, not new metrics.
- `range`: The red-team audit gives the auditor raw-data access to repeat the leakage and interval checks, plus a four-item rubric with a pass verdict. This makes the owner's audit an independent test rather than a read-through. It uses the analyst the owner already specified.
- Skipped: `altitude`. The next step up, a live or parallel trial with analysts, would change the offline-only scope that the owner asked to keep unchanged. The hard-target move is also skipped: this is an evaluation, and there is nothing to optimise without tuning.
- Owner actions:
  - Confirm the runner, the recall threshold value, the subgroup definitions, raw event access, the holdout's untouched status, and the independent analyst's availability.
  - Decide whether a leakage finding from the audit should block a pass, beyond being reported alongside the judge result.
  - Note that I did not obtain a workspace listing: my directory checks returned no output. Every target-specific fact above comes from your task text, not from inspected artifacts.
