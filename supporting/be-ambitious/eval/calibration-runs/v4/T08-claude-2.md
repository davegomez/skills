```text
Evaluate whether our churn model gives analysts a useful early-warning signal: accounts flagged early enough, and precisely enough at the analysts' working capacity, to act on. Keep these scope, methods, and acceptance conditions unchanged:
- The approved scope is offline evaluation only.
- Use the supplied de-identified training set and the untouched later-period holdout, split by customer to prevent leakage.
- Reproduce the current model and its baseline, test the onboarding explanation from the raw events, and check calibration and subgroup errors.
- Have an independent analyst audit leakage and the conclusion against a written rubric.
- Do not tune on the holdout. Report uncertainty and missed targets.
Assumption to confirm: analysts act on a ranked alert list with limited outreach capacity, so lead time and precision at that capacity decide usefulness.

First checks. Name anything missing and continue only with work the available artifacts support:
1. Confirm the existing evaluation runner exists, runs, and reports precision at a fixed recall with a 95% CI for the paired model-minus-baseline difference.
2. Locate the documented approved recall threshold.
3. Confirm the holdout is untouched: no prior runs, and no features or thresholds fitted on it.
4. Confirm the raw event logs, churn dates, and the as-of timestamp of each prediction are available.
5. Confirm the independent analyst is available and was not involved in building the model.
6. Ask for analysts' weekly outreach capacity. If it is unknown, prespecify a small set of capacity levels from training data only.

Pre-register before touching the holdout. Write a dated analysis plan and give it to the auditor. It fixes:
- the operating point (the approved recall threshold)
- the capacity levels and lead-time windows
- the subgroups, with a minimum n
- the onboarding hypothesis and its test
- the multiple-comparison correction
- the metrics below
Then write the auditor's rubric, also before the holdout run. It covers leakage, label definition, deviations from the plan, and whether the conclusion follows from the judged result. Run each prespecified holdout analysis once. Log any unplanned analysis as exploratory.

Leakage and labels, from raw evidence:
- Rebuild features with point-in-time (as-of) joins from the raw events, and diff them against the supplied features.
- Search for post-outcome proxies: cancellation tickets, billing stops, and events dated after the prediction timestamp.
- Confirm the churn label definition and how customers still active at the holdout's end are handled (right-censoring). Exclude them or treat them explicitly, and do not count them as non-churners.
- Run adversarial validation, a classifier that tries to tell training customers from holdout customers, to expose drift or split leaks beyond customer ID overlap.

Is the warning early?
- Report precision at each prespecified capacity, the number of alerts per true churner, and the lead-time distribution (days from first alert to churn).
- Re-score after excluding customers already showing late-stage signals at prediction time (for example, near-zero recent activity, defined in the plan). This tests whether the lift comes from early warning or from relabeling visible exits.
- Run decision curve analysis: net benefit across threshold probabilities versus "contact everyone" and "contact no one". This shows the range of cost ratios where the model helps.

Onboarding explanation:
- Reconstruct onboarding behavior directly from the raw events.
- On training data only, using customer-grouped cross-validation, measure what onboarding features add over the baseline, with ablation and grouped permutation importance.
- State the hypothesis precisely, then test it once on the holdout as pre-registered.
- Anything found during training exploration is development evidence. Report it as unverified unless the pre-registered holdout test confirms it.

Calibration:
- Draw reliability diagrams with customer-level bootstrap bands.
- Report the Brier score and its Murphy decomposition (reliability, resolution, uncertainty), plus calibration slope and intercept, for the model and the baseline.

Subgroups:
- Report precision, recall, and calibration per prespecified segment with CIs, and flag any segment below the minimum n.
- Apply Holm or Benjamini–Hochberg correction across segments.
- Use only attributes present in the de-identified data. Make no attempt to re-identify customers.

Uncertainty: use a paired bootstrap resampled by customer, so the model and the baseline are scored on the same customers. Report every target the plan names as met or missed.

With my approval only: modify the existing evaluation runner, for example to add the paired customer-clustered CI if it is missing. A result computed outside the unmodified runner does not satisfy the judge.
With my approval only: draft a shadow-mode or randomized outreach pilot to test whether alerts reduce churn. This goes beyond offline evaluation.
With my approval only: share data or results with anyone beyond the independent analyst.

Report:
- the judged result
- lead time, capacity precision, decision curve, calibration, subgroup, and onboarding findings, each labeled confirmatory or exploratory
- deviations from the plan
- the auditor's rubric findings
- missed targets
The supplementary analyses inform the analysts' decision. They cannot rescue a failed judge.

Judge: the existing evaluation runner must reproduce the baseline, enforce customer separation, and show holdout precision at the approved recall threshold above the baseline with a 95% confidence interval for the difference excluding zero. Otherwise report that the evidence does not establish improvement. The independent analyst's rubric findings judge the leakage audit and the conclusion. Until the auditor signs off, those remain unverified.
```

**Ledger**

- `altitude`: The original outcome is "does the model beat the baseline." The improved outcome is "can analysts act on these alerts," measured by lead time, precision at capacity, and decision-curve net benefit. These metrics are reported alongside the unchanged pass condition and cannot override it. Needs prediction as-of timestamps, churn dates, and the capacity figure.
- `depth`: Pre-registering the plan and rubric before the holdout run enforces "do not tune on the holdout." It also makes the audit checkable against a fixed plan. No scope change.
- `depth`: Point-in-time feature rebuild, a post-outcome proxy search, and a censoring check catch temporal and label leakage that a customer split alone misses. Needs raw events with timestamps.
- `depth`: The late-signal exclusion re-score tests the belief the task rests on: that the lift is early warning rather than relabeling visible churners.
- `depth`: The onboarding hypothesis is tested with grouped CV and ablation on training data and confirmed once on the holdout. Training-only findings stay labeled unverified.
- `depth`: Paired customer-clustered bootstrap, Brier decomposition, calibration slope and intercept, and corrected subgroup CIs with a minimum n give honest uncertainty. These are within the approved calibration and subgroup work.
- `range`: Screening epidemiology contributes lead time and alerts per true churner. Clinical decision analysis contributes decision curves, showing when acting on the model beats contacting everyone or no one. Survival analysis contributes censoring handling.
- `range` (red team): Adversarial validation and a pre-written rubric try to break the leakage and conclusion claims before the auditor does.
- Approval-gated: changing the runner (it is the judge), a pilot design (outside offline scope), and any wider sharing of data or results.
- Skipped lenses: none.
- Owner actions:
  - Confirm the runner computes the paired CI, or approve changing it.
  - Supply the approved recall threshold and analyst capacity.
  - Confirm the holdout is untouched and that as-of timestamps exist.
  - Name an independent analyst.
  - Decide on the pilot and sharing lines.
