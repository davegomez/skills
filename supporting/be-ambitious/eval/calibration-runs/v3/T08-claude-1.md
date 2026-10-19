```text
Goal: decide, with stated uncertainty, whether our churn model gives analysts an early-warning signal they can act on. Do this as an offline evaluation only. Assumption to confirm: "useful" means alerts that arrive early enough, and in small enough volume, for analysts to act on.

Fixed requirements (unchanged):
- Offline evaluation only.
- Use the supplied de-identified training set and the untouched later-period holdout, split by customer to prevent leakage.
- Reproduce the current model and its baseline.
- Test the onboarding explanation from the raw events.
- Check calibration and subgroup errors.
- Have an independent analyst audit leakage and the conclusion against a written rubric.
- Do not tune on the holdout.
- Report uncertainty and missed targets.

First checks. Report each as available, missing, or unverified, and continue only with work the available artifacts support:
- Access to the training set, the holdout, the raw event logs, and the existing evaluation runner.
- The approved recall threshold value and the exact baseline definition.
- Evidence that the holdout is untouched, such as access logs or a prior-use record. If there is none, say so.
- Event and churn timestamps, whether customers have multiple scoring dates, and how the label window treats customers whose outcome period is incomplete (censoring).
- Which subgroup attributes the de-identified data contains.
- Whether the independent analyst is available.
- Which confidence-interval method the runner uses. If customers have multiple rows and the runner resamples rows instead of customers, report this as a judge defect. Do not change the acceptance condition.

Before any holdout run:
1. Write and date an analysis plan. It covers the primary metric and threshold from the judge, the baseline, the secondary metrics below, the pre-specified subgroups, the onboarding hypothesis and its test, and the CI method. Give the rubric to the independent analyst at this stage, before anyone sees holdout results. Treat any analysis added after the plan is locked as exploratory.
2. Test the judge itself. On a copy of the training data only, build a split where the same customer appears on both sides. Confirm the runner rejects it (red), then confirm it accepts the true customer split (green). If the runner accepts the overlap, the judge cannot enforce separation; report that and stop the acceptance claim.
3. Reproduce the model and baseline with the runner on the training data. Record the code, config, and data hashes.
4. Leakage audit from raw events. Rebuild a sample of features with a point-in-time cutoff: only events before each prediction date. Compare them to the supplied engineered features. Flag any feature that encodes churn already underway, such as cancellation-flow, downgrade, or billing-failure events near the label date. Those features make a model look predictive without giving any warning.
5. Onboarding explanation. Rebuild onboarding features from the raw events. On training data only, with customer-grouped cross-validation:
   - Ablate them and measure the drop in precision at the approved recall.
   - Stratify by signup cohort and plan, to check whether onboarding is a proxy for tenure or cohort.
   - Add a negative-control feature that has no plausible link to churn, as a comparison.
   State the resulting claim in the plan before confirming it once on the holdout.

Holdout (run once, with the locked plan):
- Primary: run the runner's acceptance comparison.
- Secondary, report only, never used to change the model or threshold. Run these in separate scripts that leave the runner unchanged:
  - Lead time: the distribution of days from first alert to churn, and skill against the baseline at each lead-time band. This is the forecast-verification view; it tests whether the warning is early.
  - Analyst workload: precision at top-k across a range of alert volumes, and net benefit across thresholds (decision-curve analysis). Analyst capacity is unknown, so report curves rather than assuming a capacity.
  - Calibration: reliability diagram, Brier score and Brier skill score against the baseline, and calibration intercept and slope.
  - Subgroups: per-subgroup precision, recall, and calibration for the pre-specified groups only. Use customer-level bootstrap CIs and flag small groups. Label any pattern noticed in the holdout as exploratory and unverified.
- Mark every finding as confirmed (pre-specified and tested once on the holdout) or development or exploratory (shaped by the data it is reported on).

Independent audit: the analyst applies the pre-written rubric to the leakage evidence, the split check, and the conclusion. Report their findings and any disagreement verbatim, separately from my own summary.

Report:
1. Lead with the judge verdict.
2. Give the secondary findings with CIs.
3. List the missed targets, the failed or unverified dependencies, and every place where uncertainty limits the conclusion.

With my approval only: modify the existing evaluation runner, including fixing any CI or separation defect found above.
With my approval only: draft a prospective shadow-mode or randomized pilot to measure whether acting on alerts changes retention. Any live scoring, outreach, or production-data access is outside the approved offline scope.
With my approval only: share data or results with anyone beyond the independent analyst.

Judge: the existing evaluation runner must reproduce the baseline, enforce customer separation, and show holdout precision at the approved recall threshold above the baseline with a 95% confidence interval for the difference excluding zero. Otherwise report that the evidence does not establish improvement. The separation check in step 2 must go red on the overlapping split and green on the customer split. If it does not, report that the judge cannot enforce separation. The lead-time, workload, calibration, subgroup, and onboarding results are reported alongside the verdict and never replace it.
```

**Ledger**
- `altitude`: from "does the model beat the baseline on holdout precision" to "can analysts act on these alerts in time and at a workable volume." It adds lead-time, top-k, and decision-curve results as report-only secondaries. There is no scope change and the acceptance condition is unchanged. The impact pilot sits behind approval because it goes past offline evaluation.
- `depth`: a dated analysis plan and a rubric fixed before any holdout run, plus a single holdout pass. This guards against implicit tuning on the holdout and makes the confirmed/exploratory split auditable.
- `depth`: the runner's customer-separation check is tested red then green on training-data copies, so the judge is shown to work rather than assumed to. Uses training data only.
- `depth` (tests the belief the task rests on): point-in-time feature rebuild and a near-label leakage scan. These catch a model that "predicts" churn already in progress, which would pass the precision bar while giving no early warning.
- `depth`: the onboarding explanation is tested with ablation, cohort stratification, and a negative control on training data, then confirmed once on the holdout. This separates a causal-looking story from a tenure proxy.
- `depth`: the runner's CI method is checked for customer-level resampling. Row-level resampling would make the interval too narrow; any fix needs approval.
- `range`: forecast verification (meteorology) contributes skill against lead time and Brier skill score, which show whether the warning is early. Clinical prediction contributes decision-curve net benefit and calibration slope and intercept, which show whether acting on alerts is worth the workload. Survival analysis contributes the censoring check, which catches label bias from incomplete outcome windows.
- `range` (red team): deliberate overlap and leakage canaries exercise the audit and the runner before the conclusion relies on them.
- Skipped: a hard target. The owner's bar is a statistical test with no numeric goal, and a stretch target on the holdout would invite tuning.
- Owner actions:
  - Confirm the recall threshold, the baseline definition, holdout integrity evidence, raw-event and timestamp access, subgroup attributes, and the independent analyst's availability.
  - Confirm the "useful = actionable in time and volume" assumption and supply analyst capacity if it is known.
  - Decide on runner fixes, the pilot design, and any wider sharing.
