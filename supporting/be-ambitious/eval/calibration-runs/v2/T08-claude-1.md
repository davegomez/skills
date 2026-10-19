```text
Goal: Determine whether our churn model gives analysts a useful early-warning signal, meaning one they can act on before customers leave. Report the result whether or not it shows improvement. The people who act on it are the analysts who review flagged customers and the owner deciding whether analysts should rely on the model.

Fixed requirements (do not change):
- The approved scope is offline evaluation only. No deployment, no live data, no customer contact.
- Use the supplied de-identified training set and the untouched later-period holdout, split by customer to prevent leakage.
- Reproduce the current model and its baseline.
- Test the onboarding explanation from the raw events.
- Check calibration and subgroup errors.
- Have an independent analyst audit leakage and the conclusion against a written rubric.
- Do not tune on the holdout.
- Report uncertainty and missed targets.
- Keep these scope, methods, and acceptance conditions unchanged. Everything added below is supplementary and never changes the pass condition.

Assumptions (inferred; confirm or correct before step 2):
- A1: Analysts review a limited number of customers per period. Use the owner's capacity figure; if none is given, report results across a range of capacities.
- A2: "Early" means flagged far enough ahead to act. Use the lead-time windows the owner sets; otherwise use 30, 60, and 90 days.
- A3: The relevant subgroups are plan, tenure band, signup cohort, acquisition channel, and region, limited to those present in the data.

1. First checks, before any holdout access. Report each item as confirmed, missing, or unverified:
   - The existing evaluation runner executes. Its baseline definition, metric, and 95% CI method are documented. Record whether the CI is paired and whether it resamples rows or customers.
   - The approved recall threshold is written down, with its source.
   - Customer pseudonyms are consistent between the training set and the holdout, so the same customer has the same key in both. If they are not, customer separation cannot be verified. In that case, stop and report to the owner. Do not attempt record linkage or re-identification.
   - Raw events carry timestamps, and churn labels carry dates, so features can be rebuilt as of a prediction date.
   - The independent analyst is named, did not build the model, and is available.
   Continue only with work the available artifacts support. Anything that depends on a missing item stays unverified.

2. Freeze the analysis plan before unlocking the holdout. Write and date a plan in the style of a clinical-trial statistical analysis plan. It covers:
   - model and baseline artifacts, with hashes
   - feature definitions and prediction dates
   - the threshold rule, metrics, subgroups, and CI methods
   - every supplementary analysis below
   The independent analyst writes the audit rubric at this stage, based on the TRIPOD prediction-model checklist plus the leakage checks in step 4. Any analysis added after holdout results are seen is labeled exploratory.

3. Reproduce on training data only. Rebuild the current model and its baseline from the supplied training set. Use customer-grouped cross-validation for any fitting. Report any discrepancy from the recorded versions.

4. Red-team leakage hunt, done before scoring the holdout:
   - Confirm zero customer overlap between training and holdout, and across CV folds.
   - Rebuild features from raw events with point-in-time (as-of) joins, then diff them against the supplied features. Any feature that uses information from after the prediction date is leakage.
   - Search for label proxies, such as cancellation-flow, billing-failure, or account-closure events that feed into features.
   - Run adversarial validation: train a classifier to distinguish training rows from holdout rows. Report its AUC and top features as a drift and leakage signal.

5. Test the onboarding explanation from raw events. Treat it as a hypothesis, not a finding.
   - Rebuild the onboarding features from raw events and confirm they match the supplied ones.
   - Ablation: retrain without the onboarding features, on training data only with hyperparameters held fixed. Compare on the holdout as a pre-specified secondary result.
   - Stratify by signup cohort, plan, and channel to check whether the onboarding effect survives within strata or is confounded by them.
   - State that this is predictive evidence, not causal evidence.

6. Score the holdout once, following the frozen plan:
   - Compute the judge metric with the existing runner.
   - Calibration, without recalibrating on the holdout: reliability diagram, Brier score, calibration intercept and slope. Any recalibration is fit on training data only.
   - Subgroup errors: precision, recall, and calibration per subgroup, with counts and 95% CIs. Flag subgroups too small to judge.
   - Uncertainty sensitivity check: run a customer-level paired bootstrap of the precision difference. If it disagrees with the runner's CI, report both. The runner's result remains the judge.

7. Analyst-usefulness replay (supplementary). Replay the analyst workflow on the holdout:
   - Precision at analyst capacity: top-k customers per review period (A1).
   - Lead time: rebuild features as of each prediction date (A2). Report how many days before churn each caught churner was first flagged, and what share was flagged early enough to act on. This tests the belief the task rests on: that the signal is early, not merely accurate close to churn.
   - Decision curve analysis: net benefit of the model, the baseline, contact-all, and contact-none across plausible cost ratios of an analyst review versus a lost customer.

8. Independent audit. The analyst audits leakage and the conclusion against the written rubric, using the plan, code, and results. Each rubric item is recorded as pass or fail, with notes. Unresolved disagreements are reported as unresolved.

With owner approval only, because it is outside the approved scope: draft, but do not run, a design for a measured live pilot. The design would test whether analyst outreach to flagged customers reduces churn compared with a randomized holdback.

Report structure:
- Lead with the conclusion, then the judge result.
- Then reproduction, leakage findings, the onboarding test, calibration, subgroups, the usefulness replay, and the audit.
- Then uncertainty, missed targets, and anything left unverified.
- Keep observed results separate from interpretation.

Judge: the existing evaluation runner must reproduce the baseline, enforce customer separation, and show holdout precision at the approved recall threshold above the baseline with a 95% confidence interval for the difference excluding zero. Otherwise report that the evidence does not establish improvement. The supplementary analyses inform the analysts' decision but do not change this pass condition.
```

**Ledger**

- `altitude`: The original task asks whether the model beats the baseline. The rewrite moves up to the decision that comparison serves: whether analysts should act on the signal. It adds an offline replay of precision at analyst capacity, lead time, and decision-curve net benefit. Scope stays offline. A live pilot appears only as a design draft, behind owner approval.
- `depth`: The analysis plan is frozen and the rubric written before the holdout is unlocked. This enforces "do not tune on the holdout" by procedure and separates confirmatory results from exploratory ones. Cost is about half a day of up-front writing.
- `depth`: Features are rebuilt from raw events with as-of joins, and label proxies are searched for directly. This tests leakage from the raw evidence rather than trusting the supplied feature table.
- `depth`: The onboarding explanation gets an ablation plus stratification by cohort, plan, and channel. This tests the claim instead of describing it and guards against reading confounding as cause.
- `depth`: A customer-level paired bootstrap runs as a sensitivity check. If the runner resamples rows, its CI is too narrow. The check exposes that without changing the judge.
- `depth`: The lead-time analysis tests the "early" part of early warning. A model can win on precision while flagging churners too late to act.
- `range`: Clinical prediction research contributes three methods: a statistical analysis plan, the TRIPOD checklist as the basis for the rubric, and decision curve analysis. Together they give the auditor a standard rubric and show whether the model beats the trivial policies at real cost ratios.
- `range`: The red-team leakage hunt adds adversarial validation and a check that pseudonyms are consistent across periods. With de-identified data, customer separation is only as good as the keying. If keys differ by period, the judge cannot pass, and the prompt stops rather than attempting linkage.

Skipped lenses: none. All three fit, because the result drives an adoption decision, must be done rigorously, and has to land with analysts.

**Owner actions**
- Confirm the approved recall threshold and where it is documented.
- Confirm that customer pseudonyms are consistent across the training and holdout periods.
- Name the independent analyst and confirm they are available.
- Supply analyst review capacity (A1) and the lead-time windows (A2), or accept the defaults.
- Confirm the runner's CI method.
- Decide whether to approve drafting the live-pilot design.
