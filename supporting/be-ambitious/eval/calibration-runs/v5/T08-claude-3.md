```text
Goal: decide, on offline evidence alone, whether analysts should rely on our churn model as an early-warning signal. Produce a verdict that analysts can act on and an independent analyst has checked. The verdict says whether the model beats the baseline, at what operating point, how far its probabilities can be trusted, and where it fails.
Assumption: analysts will use the result to decide whether, and for which customers, to act on model flags instead of the baseline. The report should state what a flag means in practice.

Scope and fixed requirements (unchanged):
- Offline evaluation only. Use the supplied de-identified training set and the untouched later-period holdout. Split by customer to prevent leakage.
- Reproduce the current model and its baseline. Test the onboarding explanation from the raw events. Check calibration and subgroup errors. Have an independent analyst audit leakage and the conclusion against a written rubric.
- Do not tune on the holdout. Report uncertainty and missed targets.
- Use only these analyses and the acceptance metric below. Add no new models, features, or metrics.

First checks (name anything missing and continue only with work the available artifacts support):
1. The existing evaluation runner exists and runs. Record its version or commit, its environment, and its seeds.
2. The approved recall threshold value. Find out how the runner sets the operating point: fixed in advance, or computed on the evaluated data. Find out how it computes the 95% CI for the precision difference. Note whether it resamples at the customer level and pairs both models on the same customers.
3. The recorded baseline result that reproduction must match, with its tolerance.
4. The training set and holdout are present, with customer IDs in both. Find any record showing the holdout has not been opened. If no record exists, say so.
5. The raw onboarding events are available with timestamps, along with each customer's prediction date.
6. Which subgroup attributes exist in the de-identified data.
7. An independent analyst is named, has access to these artifacts under existing approvals, and has a written rubric. If the rubric does not yet exist, have it written and frozen before results are shared.

Method:
- Pre-specify before opening the holdout. Write and date an analysis plan covering:
  - the operating-point rule
  - the CI method
  - the calibration checks
  - the subgroup definitions and minimum cell size
  - the onboarding test
  Do all development on the training set using customer-grouped cross-validation, with no customer in more than one fold. Run the holdout once under the frozen plan. Label any later deviation as post hoc.
- Reproduction: rerun the current model and the baseline through the existing runner with pinned versions and seeds. Report reproduced against recorded metrics. If the baseline does not reproduce within tolerance, stop the comparison and report why.
- Customer separation and leakage pre-check:
  - Confirm zero customer-ID overlap between training and holdout, and between CV folds.
  - Confirm every feature, including onboarding features, is built only from events timestamped before each customer's prediction date.
  - List any feature whose lineage you cannot trace to raw events.
- Onboarding explanation:
  - Rebuild onboarding indicators directly from the raw event logs. Check that they match the model's onboarding features.
  - On the training set, compare churn by onboarding status within strata of tenure, plan, and signup cohort, where those attributes exist. This tests whether the association survives the obvious confounders.
  - Check whether the model's precision gain over the baseline concentrates in customers with weak or incomplete onboarding.
  - Treat training-set results as development evidence. Then confirm on the holdout under the pre-specified test, or leave the explanation unverified.
  - State the result as association, not cause.
- Calibration on the holdout, without recalibrating:
  - a reliability diagram
  - calibration-in-the-large (mean predicted vs observed churn)
  - calibration slope and intercept
  Report each with uncertainty.
- Subgroup errors:
  - For each pre-specified subgroup, report count, base rate, precision and recall at the operating point, and calibration-in-the-large, all with CIs.
  - Flag cells below the minimum size as uninformative.
  - Note that many subgroups raise the chance of a spurious gap.
- Uncertainty: if the runner's CI does not resample by customer, or does not recompute the operating point within each resample when that point is set on the evaluated data, report this as a limitation. Do not change the runner's acceptance logic.
- Decision translation: using the measured precision, recall, and holdout base rate, state what a flag means. For example: of every 100 customers flagged at the approved recall, about how many churn under the model versus the baseline, with the CI. Include known failure subgroups and calibration limits.

Independent audit:
- Give the analyst the frozen plan, the runner outputs, the raw-event lineage, and the draft conclusion.
- The analyst independently reproduces the headline precision difference from the runner outputs.
- The analyst actively hunts for leakage: customer overlap, post-prediction-date events, target-derived features, and holdout touches before the frozen run.
- The analyst grades whether the conclusion and its decision translation follow from the evidence, scoring against the written rubric.
- Report the analyst's findings verbatim alongside yours. Resolve or disclose every disagreement.

Report: the verdict, reproduction results, separation and leakage checks, onboarding findings (confirmed or unverified), calibration, subgroup errors, all uncertainty, every missed target, every post hoc deviation, and the audit.

Judge: the existing evaluation runner must reproduce the baseline, enforce customer separation, and show holdout precision at the approved recall threshold above the baseline, with a 95% confidence interval for the difference excluding zero. Otherwise, report that the evidence does not establish improvement. For the leakage audit and the conclusion, the independent analyst's rubric scores and verbatim findings are the judge. Any rubric failure is reported, and the conclusion is labelled not independently confirmed.
```

- `altitude`: the outcome moves from an evaluation verdict (does the model beat the baseline) to an analyst-ready decision. That means what a flag means in churners per 100 flagged, the operating point, failure subgroups, and calibration limits, all checked by the auditor's rubric. These are derived from existing metrics, so there is no scope change.
- `depth`: a frozen, dated analysis plan and a single holdout run make "do not tune on the holdout" checkable, and post hoc changes become visible.
- `depth`: onboarding features are rebuilt from raw event logs with lineage and timestamp checks. This tests the explanation and catches leakage at its source.
- `depth`: customer-grouped CV, explicit overlap checks, and a check that the runner's CI resamples by customer with paired predictions. This makes the uncertainty trustworthy without altering the runner.
- `range`: two clinical-prediction-modelling tools. Pre-registration guards the holdout. Calibration slope and intercept with reliability diagrams show whether probabilities can be read as risk, not just ranked.
- `range`: epidemiology's stratification by tenure, plan, and cohort tests whether the onboarding association survives obvious confounders. It is framed as association, not cause.
- `range`: red-team audit. The independent analyst reproduces the headline number and actively hunts for leakage, and the rubric is frozen before results are shared. The analyst needs access to these artifacts under existing approvals, so no new data sharing.
- Skipped: the hard-target move. This is an evaluation of the current model, and new models, tuning, or metrics would break the closed method set. Live pilots and lead-time analysis were also left out because the scope is offline-only with fixed methods.
- Owner actions:
  - Confirm the runner, the approved recall threshold, the operating-point rule, and the CI method.
  - Provide the recorded baseline result and tolerance, and any record that the holdout is untouched.
  - Name the independent analyst, confirm their access, and supply or approve the written rubric before results are shared.
