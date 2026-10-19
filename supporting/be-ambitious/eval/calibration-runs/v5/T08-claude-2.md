```text
Goal: tell analysts whether the current churn model gives them a useful early-warning signal, and whether it beats its baseline, using offline evaluation only. State the verdict in terms analysts act on.
Assumption: analysts will use the conclusion to decide whether to trust and act on the model's flags. The verdict should therefore say where the signal holds, where it fails, and how certain each statement is.

Scope and fixed requirements (unchanged):
- Offline evaluation only.
- Use the supplied de-identified training set and the untouched later-period holdout, split by customer to prevent leakage.
- Methods are closed to these: reproduce the current model and its baseline; test the onboarding explanation from the raw events; check calibration and subgroup errors; have an independent analyst audit leakage and the conclusion against a written rubric. Add no other analyses, experiments, or metrics.
- Do not tune on the holdout.
- Report uncertainty and missed targets.

First checks (record each result; name anything missing and continue only with work the available artifacts support):
1. The training set, holdout, and raw event logs are present. Each has a customer ID and event timestamps.
2. Confirm the holdout is untouched, using whatever access record exists. If none exists, say so.
3. The existing evaluation runner runs. Find how it enforces customer separation, how it computes the 95% CI for the precision difference, and how it sets the operating point for the approved recall threshold. If the operating point is chosen on holdout labels, report that as a finding. Do not change the runner or the judge.
4. Find the approved recall threshold value and its source.
5. Find the current model's code or artifact, its baseline, and their previously reported numbers.
6. Confirm the written rubric exists and an independent analyst is available. The analyst must not have built the model or this evaluation.
7. Confirm the subgroup attributes exist in the de-identified data.

Order of work. Lock everything before the holdout is opened:
1. Write a short analysis plan before any holdout run, and date it before the first holdout run. The plan names:
   - the onboarding hypothesis and its event-level definition
   - the subgroups
   - the calibration bins
   - the comparison the judge uses
2. After the holdout is opened, do not change model, features, threshold, onboarding definition, or subgroups. Mark any deviation from the plan as a deviation in the report.

Reproduce:
- Rebuild the current model and the baseline from the training set with pinned seeds and library versions.
- Compare against the previously reported numbers and state the tolerance used. Record data file hashes and environment.
- If reproduction fails, stop before the holdout and report the gap.

Onboarding explanation:
- Derive the onboarding measures directly from raw event timestamps. Do not use precomputed summary features.
- Use only events before each customer's prediction date.
- Develop and refine the explanation on the training set only, with customer-grouped folds. That is development evidence.
- Then test the frozen statement once on the holdout. That is confirmation evidence.
- Check whether the association holds within each pre-specified subgroup.
- Report the result as associational, not causal. Name the plausible confounders, such as plan tier or acquisition cohort, that the data cannot rule out.

Calibration:
- On the holdout, compare predicted churn probability to observed churn rate per pre-specified bin, with bin counts and uncertainty.
- State whether a score can be read as a probability, and where it over- or under-predicts. Do not recalibrate on the holdout.

Subgroup errors:
- For each pre-specified subgroup, report precision and recall at the approved operating point, with counts and confidence intervals.
- Flag subgroups too small to support a conclusion. Do not report them as findings.

Analyst-facing result (derived only from the runner's holdout numbers at the approved operating point):
- Per 100 customers flagged, how many churned, for model and baseline.
- Of the customers who churned, how many were caught.
- The precision difference with its 95% CI.
- Which subgroups and score ranges analysts should trust less.

Independent audit:
- The independent analyst scores leakage and the conclusion against the written rubric. Leakage covers customer overlap, features built from events after the prediction date, and any holdout use in threshold or feature choices.
- The analyst works as a red team: trace each feature to its raw event timestamps; write the strongest alternative explanation for the onboarding result; check that every sentence of the conclusion follows from the runner's output and the CIs.
- Report rubric scores and findings verbatim. Resolve or explicitly carry forward each finding.

Report:
- Reproduction status, the judge result, calibration, subgroup errors, the onboarding test (development vs confirmation evidence kept separate), the audit findings, uncertainty for every estimate, every missed target, and every unchecked dependency.
- Results that the judge or audit did not cover are labeled unverified.

Judge: the existing evaluation runner must reproduce the baseline, enforce customer separation, and show holdout precision at the approved recall threshold above the baseline with a 95% confidence interval for the difference excluding zero. Otherwise report that the evidence does not establish improvement. The independent analyst's rubric scores are the evidence for the leakage audit and for the conclusion's wording.
```

**Ledger**

- `altitude`: The original outcome is a pass/fail on precision versus baseline. The improved outcome is a verdict on whether analysts should act on the flags, in their units: churners per 100 flagged, churners caught, and where to trust less. It uses only the runner's existing holdout numbers. No scope or method change.
- `depth`:
  - The analysis plan is locked and dated before the holdout opens, so later choices cannot quietly tune on it.
  - Reproduction is pinned (seeds, versions, hashes, tolerance) and gates the holdout.
  - Onboarding measures come from raw timestamps cut at the prediction date. Development evidence is kept separate from a single holdout confirmation.
  - Calibration uses binned observed-versus-predicted rates with counts.
  - Subgroups are pre-specified, with small-n flags.
- `depth`: The first checks cover how the runner picks the recall operating point. If it picks it on holdout labels, that is hidden holdout tuning. This is reported as a finding; the judge stays unchanged.
- `range`:
  - Pre-registration from experimental science blocks forking-path analyses.
  - Epidemiology's confounding check, within the approved subgroups, keeps the onboarding claim associational.
  - The red-team audit traces features to raw timestamps and argues the best alternative explanation.
  - All of this sits inside the approved audit.
- Skipped: none. No "With my approval only" lines were needed, because every change stays inside the approved methods. The hard-target move doesn't apply, since this is an evaluation and stretching would invite tuning.
- Owner actions:
  - Confirm the approved recall threshold, the runner's operating-point and CI method, the rubric, the independent analyst, the subgroup attributes, and the holdout's untouched status.
  - Note that lead time isn't among the approved methods, so this evaluation cannot show *how early* the warning arrives. Whether to test that is a separate scope decision.
