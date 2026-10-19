# Rewritten prompt

```text
Goal: Determine whether the current churn model gives analysts a useful early-warning signal. The aim is a decision analysts can act on: whether its flags, within the attention analysts can actually give, catch churners early enough to act, better than the baseline. This framing is an assumption about what "useful" means. The primary judge below is unchanged and decides the headline.

Scope and fixed requirements (do not change):
- Approved scope is offline evaluation only. No deployment, live scoring, outreach, or intervention.
- Use the supplied de-identified training set and the untouched later-period holdout, split by customer to prevent leakage.
- Reproduce the current model and its baseline.
- Test the onboarding explanation from the raw events.
- Check calibration and subgroup errors.
- Have an independent analyst audit leakage and the conclusion against a written rubric.
- Do not tune on the holdout.
- Report uncertainty and missed targets.

0. First checks. Report each as confirmed, missing, or unverified, and continue only with work the available artifacts support:
   - The training set, the holdout, and the raw events exist and are readable. Each has a stable pseudonymous customer ID and event timestamps.
   - The raw events are covered by the same de-identification clearance as the training set. If they are not confirmed, stop before reading them and ask the owner.
   - The holdout is untouched: no prior reads in logs or notebooks. Its label window has fully matured, meaning every holdout customer has had the full follow-up period needed to observe churn.
   - The existing evaluation runner runs, and its definitions of the baseline, the current model, the churn label, and "precision at recall" are documented.
   - The approved recall threshold value is written down.
   - An independent analyst is named who did not build the model.
   - Owner inputs exist for analyst capacity (flags per period) and minimum actionable lead time. If they are missing, label them assumptions and report results across a stated range.

1. Pre-register before touching the holdout. Write a frozen analysis plan and record its hash, as clinical trials freeze a statistical analysis plan before unblinding. The plan contains:
   - The primary metric and judge, unchanged.
   - Every secondary analysis below, with its metric, subgroups, and CI method.
   - The onboarding hypothesis, with its predicted direction and size.
   - All model, feature, and threshold choices, fixed using training data only, with customer-grouped cross-validation.
   Score the holdout once. Log every holdout access. Secondary analyses are descriptive and cannot rescue a failed primary result.

2. Reproduce and audit leakage on the training data.
   - Rebuild the baseline and the current model through the existing runner. Compare the results to their recorded metrics within a tolerance you state in advance.
   - Reconstruct features point-in-time from the raw events with as-of joins. Flag any feature whose source event is timestamped at or after the prediction time or the churn date.
   - Scan for single features with suspiciously high predictive power on their own.
   - Run adversarial validation: train a classifier to tell training rows from holdout rows, to expose drift or shortcuts.
   - Confirm zero customer-ID overlap between training and holdout, and check for near-duplicate customers.

3. Test the onboarding explanation as a pre-registered hypothesis.
   - Derive onboarding features independently from the raw events.
   - On training data, use customer-grouped cross-validation to:
     - compare the model with and without the onboarding features (ablation);
     - measure grouped permutation importance;
     - check whether the onboarding effect holds within strata of signup cohort, tenure, and plan, because onboarding may only proxy for these;
     - include a negative-control feature that should carry no signal.
   - State the prediction, then test it once on the holdout. Report whether it held, with CIs.

4. Calibration, subgroup errors, and the early-warning replay. All of these are pre-specified and fitted on training data only.
   - Calibration: reliability diagram, Brier score, calibration slope and intercept. If recalibration is warranted, fit it on training CV folds only.
   - Subgroups: precision, recall, and calibration per pre-specified segment, with customer-bootstrap CIs. Flag small segments, and adjust for multiple comparisons.
   - Early-warning replay on the holdout, treated as survival-style data with as-of prediction dates and censoring handled explicitly. Report:
     - lead time from flag to churn for flagged churners;
     - churners caught with at least the minimum actionable lead time at analyst capacity, versus the baseline;
     - precision and recall when the score cutoff is fixed from training data. This is the operational view, which differs from the runner's holdout-set recall threshold.
   - Decision curve analysis: net benefit of acting on the model, on the baseline, on everyone, and on no one, across a stated range of intervention cost-to-benefit ratios. This shows whether the model is worth acting on at plausible thresholds.

5. Uncertainty. Use a paired bootstrap that resamples customers, not rows, for every difference between the current model and the baseline. Report point estimates, 95% CIs, the number of holdout customers, and the number of churners.

6. Independent audit. Write a rubric before the auditor sees the results. The rubric covers:
   - temporal and customer leakage;
   - label definition and maturity;
   - fidelity of the baseline reproduction;
   - adherence to the pre-registration and holdout-access log;
   - the CI method;
   - subgroup harms;
   - whether the conclusion follows from the evidence;
   - the strongest alternative explanation for any gain.
   The auditor works from the artifacts and the rubric, attempts to find leakage, and records findings per rubric item before reading the author's conclusion. Report disagreements unresolved rather than averaged away.

Deliverable:
- A short analyst-facing verdict: use, don't rely on, or inconclusive, with the reasons.
- The primary result.
- Secondary results, labeled descriptive.
- The onboarding finding.
- Calibration and subgroup tables.
- The replay and decision-curve results, with the assumptions they used.
- The audit report.
- A list of every missed target and unverified item.
Distinguish observed evidence from proposed interpretation throughout.

Judge: the existing evaluation runner must reproduce the baseline, enforce customer separation, and show holdout precision at the approved recall threshold above the baseline with a 95% confidence interval for the difference excluding zero. Otherwise report that the evidence does not establish improvement.
```

# Ledger

- `altitude`: The original task asks whether the model beats the baseline on precision at recall. The chosen outcome is whether analysts acting on its flags, within their capacity, catch churners early enough to act. It is tested by an offline replay on the holdout plus decision curve analysis. This stays within offline scope, but it needs owner inputs for capacity and actionable lead time; without them, results are reported across a range.
- `depth`: A frozen, hashed analysis plan and a single scoring of the holdout make "do not tune on the holdout" auditable. It adds no scope and costs a short write-up before evaluation.
- `depth`: Point-in-time feature reconstruction, a scan for suspiciously strong single features, adversarial validation, and ID/near-duplicate checks catch temporal leakage, which customer splitting alone misses. This needs the raw events with timestamps.
- `depth`: The onboarding explanation becomes a pre-registered hypothesis tested with ablation, grouped permutation importance, cohort/tenure/plan stratification, and a negative control, then confirmed once on the holdout. This separates a real effect from a proxy for those variables.
- `depth`: A paired bootstrap that resamples customers gives honest CIs when customers contribute multiple rows. It is a compute cost only.
- `range`: Biostatistics contributes survival-style handling of lead time and censoring. It exposes immature labels and whether the warnings come early enough to act on.
- `range`: Clinical prediction research contributes decision curve analysis and calibration slope/intercept. These show whether acting on the model beats acting on everyone or no one at plausible costs. The cost ratios are assumptions, reported as a range.
- `range`: A red-team audit has the independent analyst write rubric findings before reading the conclusion and name the strongest alternative explanation. This reduces anchoring on the author's verdict.
- Skipped lenses: none. Rung 3 of altitude, a live intervention or uplift trial, would exceed the offline-only scope you asked to keep unchanged, so it is not in the prompt.

**Owner actions:**
- Confirm the raw events are covered by the de-identification clearance.
- Confirm the holdout is untouched and its label window has matured.
- Supply the approved recall threshold value, analyst capacity, and minimum actionable lead time.
- Name the independent analyst.
