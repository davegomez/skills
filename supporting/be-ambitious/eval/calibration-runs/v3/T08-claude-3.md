```text
Evaluate whether our churn model gives analysts a useful early-warning signal, and give the people who decide whether analysts should rely on it a decision-ready answer: does it beat its baseline, how early do its warnings arrive, how many alerts would analysts handle at the approved recall threshold, and where does it fail. (Assumption: the result decides whether analysts use the model to prioritize outreach. Confirm or correct this.)

Fixed scope and methods. Do not change these:
- Offline evaluation only.
- Use the supplied de-identified training set and the untouched later-period holdout. Split by customer to prevent leakage.
- Reproduce the current model and its baseline.
- Test the onboarding explanation from the raw events.
- Check calibration and subgroup errors.
- Have an independent analyst audit leakage and the conclusion against a written rubric.
- Do not tune on the holdout.
- Report uncertainty and missed targets.

First checks. Report each as confirmed or missing before any analysis:
- Access to the training set, the holdout, the raw event logs, and the existing evaluation runner.
- The holdout is still untouched. Record its file hash and row and customer counts before use, and ask whether anyone has already scored it.
- The approved recall threshold value, and how the runner turns it into a score cutoff. If the cutoff is set using holdout labels, ask me before proceeding, because that may count as tuning on the holdout.
- The exact baseline definition the runner reproduces.
- Which subgroup fields exist in the de-identified data.
- That an independent analyst is available and has the access the audit needs.
For anything missing, name it, continue only with work the available artifacts support, and mark dependent results unverified.

1. Lock the analysis plan before opening the holdout (borrowed from clinical-trial statistical analysis plans). Write and timestamp a plan covering:
   - the prediction cutoff and label window
   - feature definitions
   - the baseline
   - the threshold rule
   - the CI method: a paired bootstrap that resamples customers, not rows, and repeats any threshold step inside each resample so the interval reflects threshold uncertainty
   - subgroup definitions
   - calibration metrics
   - the onboarding hypotheses
   - every secondary metric
   The written audit rubric is fixed at the same time and given to the independent analyst before results exist. All development uses the training set only, with rolling-origin temporal validation inside the training period. The holdout is scored once, by the existing runner, under the locked plan. Log any deviation from the plan in the report.

2. Reproduce the model and baseline on the training period. Record the code version, environment, seeds, and the metric deltas against the documented figures.

3. Run leakage checks before trusting any score:
   - Feature-timestamp audit from raw events. Every feature must use only events strictly before the prediction cutoff.
   - Scan for label-proxy features, such as cancellation-flow events or account-closure activity.
   - Verify that no customer ID appears in both training and holdout.
   - Time-shift test: move the cutoff later. A sharp jump in performance signals leakage.
   - Shuffled-label negative control run through the same pipeline. Its precision difference must have a CI that covers zero.
   - Adversarial validation (a classifier that tries to tell training rows from holdout rows) to measure drift between the periods.

4. Test the onboarding explanation from raw events, not from derived features:
   - Define onboarding milestones directly from the event logs.
   - Estimate their association with churn using Kaplan-Meier curves and a Cox model with time-varying covariates, adjusted for signup cohort and plan where those fields exist.
   - Check whether the model's reliance on onboarding features (permutation importance) matches the raw-event result.
   Patterns found while exploring the training data are development evidence. A claim counts as confirmed only if it was pre-registered in step 1 and holds on the holdout run. Otherwise report it as unverified. Report it as an association, not a cause.

5. Calibration and subgroup errors:
   - Calibration: reliability diagram, calibration intercept and slope, and Brier score with its decomposition, overall and by subgroup.
   - Subgroup errors: precision, recall, and false-positive rate per subgroup, each with a customer-level bootstrap CI.
   - Flag groups too small to support a conclusion instead of over-reading them.

6. Decision-useful secondary results on the holdout. These are reported for context only and do not change the pass condition:
   - Lead time: the distribution of days between the first alert and churn, for customers caught at the approved recall threshold.
   - Alert volume per period at that threshold. If I supply analyst capacity, also report precision at that capacity.
   - Decision curve analysis (net benefit across a range of outreach-cost assumptions, borrowed from clinical prediction modeling), compared against "flag nobody", "flag everybody", and the baseline.
   - Context-only comparison against a trivial heuristic such as days since last activity, so readers can see whether the model adds value beyond the obvious.

7. Independent audit. The analyst audits leakage and the conclusion against the pre-written rubric, and also red-teams the conclusion by naming the most likely way it is wrong. Include the analyst's findings unedited, along with how each was resolved.

Report: the result against the pass condition, CIs on every estimate, the negative-control result, all deviations from the plan, every missed target, and every unverified item, each with its reason. Follow TRIPOD reporting items where they apply.

With my approval only: build or tune a challenger model, using training data only.
With my approval only: use retention-intervention outcome data, or run any live or pilot test of alerts with analysts. This is outside the offline scope.
With my approval only: share data or results with anyone beyond the independent analyst.
With my approval only: change the existing evaluation runner or add its checks to CI. Until then, propose changes in writing and do not apply them.

Judge: the existing evaluation runner must reproduce the baseline, enforce customer separation, and show holdout precision at the approved recall threshold above the baseline with a 95% confidence interval for the difference excluding zero. Otherwise report that the evidence does not establish improvement. The independent analyst's rubric audit is the judge for the leakage and conclusion claims. Secondary metrics never change this verdict.
```

**Ledger**
- `altitude`: The outcome moves from "does it beat the baseline" to "should analysts rely on it." Lead time, alert volume, and decision curves are added as context only. Everything runs offline on the existing holdout, so no scope change. Analyst capacity is an optional input from you.
- `depth`: A locked analysis plan and rubric before the holdout is opened guard against forking paths and accidental holdout tuning. Cost: one up-front planning step.
- `depth`: The customer-cluster paired bootstrap, with threshold re-estimation in each resample, gives the CI the judge requires without overstating certainty from multiple rows per customer.
- `depth`: Leakage instruments (timestamp audit, label-proxy scan, time-shift test, adversarial validation) give the analyst concrete evidence to audit.
- `depth`: The onboarding belief is tested with survival models on raw events. Training-set findings stay development evidence and are confirmed only by a pre-registered holdout test (new-finding move).
- `range`: Clinical prediction modeling contributes decision curve analysis and TRIPOD reporting. These show whether the model is worth acting on at realistic outreach costs.
- `range` (red team): A shuffled-label negative control, the trivial-heuristic comparison, and the analyst's "most likely way this is wrong" test whether a pass could be an artifact.
- Skipped: a hard target, because the scope evaluates the existing model rather than improving it. A challenger model is offered behind approval instead.
- Owner actions:
  - Confirm the assumed decision.
  - Confirm the holdout is untouched and the data, raw events, runner, and analyst are accessible.
  - Confirm how the approved recall threshold becomes a cutoff, and whether holdout labels are involved.
  - Supply the baseline definition, subgroup fields, and analyst capacity (optional).
  - Decide on the four approval lines.
