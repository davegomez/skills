# Rewritten prompt: churn model evaluation

**Intended result:** a defensible verdict on whether the churn model gives analysts a useful early-warning signal. Analysts act on it, and the model's owners decide whether to keep or retire it.

**Assumptions:**
- "Useful early warning" means an alert fires early enough for an analyst to act, at a volume analysts can work through.
- The decision this evaluation drives is whether analysts should use the alerts, and at what volume.

**Lenses:**
- **Altitude: fit.** The verdict drives an adoption decision that can be checked offline by replaying the holdout timeline.
- **Depth: fit.** A leakage-prone evaluation with a hard statistical bar should be done to a high standard.
- **Range: fit.** The conclusion has to survive skeptics and support a decision under uncertainty.

```text
Evaluate whether our churn model gives analysts a useful early-warning signal. The approved scope is offline evaluation only. Use the supplied de-identified training set and untouched later-period holdout, split by customer to prevent leakage. Reproduce the current model and its baseline, test the onboarding explanation from the raw events, check calibration and subgroup errors, and have an independent analyst audit leakage and the conclusion against a written rubric. Do not tune on the holdout. Report uncertainty and missed targets. Keep these scope, methods, and acceptance conditions unchanged.

Goal (ASSUMPTION, inferred and not stated by the owner): this evaluation informs whether analysts should act on the model's alerts, and at what alert volume. "Useful early warning" is assumed to mean that an alert fires early enough for an analyst to act, at a volume analysts can work through. The secondary analyses below inform that decision. They never replace the judge.

0. First checks. Before any modelling, confirm and record each of the following:
   - The training set, holdout, raw event logs, current model code or artifact, baseline definition, and existing evaluation runner are present and readable.
   - The approved recall threshold value is known, along with where it is documented.
   - The holdout is untouched: there is an access log or file hashes, and the holdout period starts after the training period ends.
   - Raw events carry timestamps that allow features to be rebuilt as of a given scoring date.
   - An independent analyst is named, and a written rubric exists. If no rubric exists, draft one and stop for owner approval before the audit.
   - The subgroup fields available in the de-identified data are identified. Use only those fields. Do not join outside data or attempt re-identification.
   Report each missing item as a dependency. Continue only with work the available artifacts support, and label any result that depends on a missing item as unverified.

1. Lock the plan before opening the holdout (pre-registration, from clinical-trial practice). Write and timestamp an analysis plan that fixes:
   - the model and baseline artifacts, frozen by hash;
   - the operating threshold that meets the approved recall, chosen on training-period data with customer-grouped cross-validation;
   - the subgroups;
   - the lead-time horizons;
   - the metrics;
   - the multiple-comparison correction.
   Score the holdout once against this plan. Label anything decided after seeing holdout results as exploratory.

2. Reproduce. Use the existing evaluation runner to reproduce the current model and its baseline from the training set. Report any discrepancy from the recorded figures before going further. Test the runner's customer-separation check by feeding it a deliberately leaky split (shared customer IDs) built from training data only, and confirm that it rejects the split. Do not modify the runner.

3. Leakage from raw events. Customer overlap is not the only leak to rule out; also check for temporal leakage. Trace each model feature to its raw events and confirm that every event used precedes both the scoring date and the churn-label window. Flag features that encode churn already in progress, such as cancellation-page visits, downgrades, or billing events after notice. Report holdout precision with and without the flagged features as a sensitivity analysis.

4. Early-warning test. This tests the belief the task rests on: that the model warns early. Rebuild features point-in-time from raw events at pre-registered horizons before churn (for example 90, 60, and 30 days).
   - Report holdout precision at the approved recall for both the model and the baseline at each horizon. This is a lead-time skill curve, from forecast verification.
   - Report the weekly alert volume at the approved recall.
   - Add decision-curve analysis: net benefit against "flag everyone" and "flag no one" across thresholds.
   Analyst capacity is an owner input. If it is unknown, report alert volume without judging whether analysts can handle it. Do not retrain or re-threshold per horizon on the holdout.

5. Onboarding explanation from raw events.
   - State the explanation as a testable hypothesis.
   - Measure it directly from raw onboarding events, not from model attributions.
   - Explore on training data only, then confirm on the holdout once, as the locked plan specifies.
   - Draw a short causal diagram. Control for the confounders it names (tenure, signup cohort, plan, acquisition channel) by stratification or adjustment.
   - Run a negative control, such as onboarding timestamps permuted within each cohort.
   - Run an ablation: refit on training data without the onboarding features and compare.
   Report the result as an association unless the design supports a stronger claim, because this is observational evidence.

6. Calibration and subgroup errors. On the holdout, report:
   - a reliability diagram, the Brier score, and the Brier skill score against the baseline;
   - calibration slope and intercept, each with a bootstrap CI resampled by customer;
   - for each pre-registered subgroup: precision, recall, false-positive rate, false-negative rate, and calibration, with CIs and a Holm (or Benjamini–Hochberg) correction.
   Flag subgroups with too few churners to estimate reliably.

7. Uncertainty. Report the runner's 95% CI for the precision difference. If the runner does not resample by customer, add a customer-cluster bootstrap as a sensitivity analysis and report both. The runner's result remains the judge.

8. Independent audit (red team).
   - Give the analyst the locked plan, code, holdout access log, and raw results before showing them your conclusion.
   - The rubric must cover at least: customer separation, temporal leakage, label definition, threshold selection made without the holdout, deviations from the locked plan, and whether the conclusion follows from the evidence.
   - Ask the analyst for a written case for the opposite conclusion.
   - Record the analyst's findings verbatim, with your responses. Do not settle disagreements by re-running on the holdout.

9. WITH OWNER APPROVAL ONLY: draft, as a document, a design for a measured live pilot (for example, a parallel trial of analyst outreach on model alerts versus baseline alerts). Running any pilot is outside the approved scope.

Deliverable: a report that keeps observed results separate from proposed interpretations. It lists every missed target, every failed check, every deviation from the locked plan, every unverified dependency, and the audit outcome.

Judge: the existing evaluation runner must reproduce the baseline, enforce customer separation, and show holdout precision at the approved recall threshold above the baseline with a 95% confidence interval for the difference excluding zero. Otherwise report that the evidence does not establish improvement. The secondary analyses (lead time, calibration, subgroups, onboarding, sensitivity CIs) are reported with their uncertainty and do not change this pass condition.
```

## Ledger

**Altitude**
- The original question was whether the model beats the baseline. The rewritten goal is whether analysts should act on its alerts and at what volume. The lead-time curve, weekly alert volume, and decision-curve analysis answer that question on the holdout. This stays offline, but it adds feature rebuilds at several horizons.

**Depth**
- **Locked plan before the holdout:** makes "do not tune on the holdout" auditable and separates confirmatory results from exploratory ones. Cost: one planning document.
- **Leaky-split test of the runner:** shows that the separation check actually catches leaks. It uses training data only and does not modify the runner.
- **Temporal-leakage trace from raw events:** catches feature-to-label time leaks that a split by customer alone would miss.
- **Lead-time test:** tests the belief the task rests on, that the model warns *early*, rather than just predicting churn that is already underway.
- **Cluster bootstrap as a sensitivity analysis:** gives honest uncertainty when customers contribute many rows. The runner's CI remains the judge.

**Range**
- **Clinical trials:** pre-registration, which protects against choosing analyses after seeing results.
- **Forecast verification:** reliability diagrams, Brier skill score, and lead-time skill, which measure how good and how early a warning is.
- **Epidemiology:** a causal diagram, confounder control, and a negative control, which test whether the onboarding explanation survives confounding by tenure and cohort.
- **Decision analysis:** decision-curve analysis, which reports net benefit against "flag everyone" and "flag no one".
- **Red team:** the auditor receives the raw results before the conclusion and writes the case for the opposite conclusion. This tests the claim most likely to be wrong.

**Proposed only:** a live pilot design, written as a document. It is behind owner approval, and running a pilot stays out of scope.

**Skipped lenses:** none.

## Owner actions
- Confirm the approved recall threshold value.
- Name the independent analyst and supply or approve the written rubric.
- Confirm that the holdout access log or hashes exist.
- Confirm that the raw events carry usable timestamps.
- Provide analyst capacity if you want alert volume judged against it.
- Decide whether to approve the pilot-design document.
