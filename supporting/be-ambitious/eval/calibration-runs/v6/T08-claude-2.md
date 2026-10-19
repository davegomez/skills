```text
Evaluate whether the current churn model gives analysts a useful early-warning signal, compared with its baseline. The scope is offline evaluation only.
Assumption: analysts will use the model's flags to decide which customers to act on, so the conclusion must say how far they can trust a flag at the approved recall threshold, and for which customers.

Data and separation
- Use only the supplied de-identified training set and the untouched later-period holdout. Split by customer so that no customer appears on both sides.
- Confirm the separation from the raw records as well as from the runner's split logic:
  - check customer-ID overlap between training and holdout;
  - check that every feature's source events fall before each row's prediction date;
  - check for duplicated event sequences across the split that would indicate one customer under two IDs. Use this only to detect leakage, never to re-identify anyone.

Freeze before the holdout
- Do not tune on the holdout.
- Before any holdout scoring, write and date an analysis plan. It fixes the model and baseline artifacts, the operating-point definition used by the runner, the subgroups, the calibration checks, and the audit rubric.
- Do all development on training data with customer-grouped cross-validation. Score the holdout once, under the frozen plan. Label any later change as post-hoc.

Reproduce
- Reproduce the current model and its baseline from the training data with pinned code, seeds, and environment.
- Record any mismatch with the reference results before going further.

Onboarding explanation
- Test the onboarding explanation from the raw events, not from the pipeline's derived features.
- Rebuild the onboarding features from the events and compare them with the pipeline's values.
- Check time-zero alignment, the epidemiology check for immortal-time bias: customers who churn early may never have had time to finish onboarding, which would make "incomplete onboarding predicts churn" partly an artifact of follow-up time.
- State whether the explanation holds:
  - first on training, under grouped cross-validation;
  - then confirm it once on the holdout. Treat any holdout result that differs from what training showed as unconfirmed.

Calibration
- Check calibration for both the model and the baseline on the holdout. Use:
  - a reliability diagram with customer-level bins;
  - the Brier score;
  - calibration intercept and slope.
- Do not recalibrate on the holdout.

Subgroup errors
- Check subgroup errors on the subgroups pre-specified in the plan. For each subgroup, report precision and recall at the operating point, with confidence intervals and counts.
- Flag subgroups too small to support a conclusion.
- Note that differences across many subgroups can arise by chance.

Uncertainty
- Report uncertainty for every headline number.
- Alongside the runner's interval, compute a customer-clustered paired bootstrap of the precision difference (resample customers, score model and baseline on the same draw). Label it supplementary, not the judge.
- If the runner's interval resamples rows rather than customers, say so as a limitation.

Independent audit
- Have an independent analyst who did not build the model or run this evaluation audit leakage and the conclusion against the written rubric. The rubric covers:
  - (a) customer overlap and duplicate-sequence checks;
  - (b) feature timestamps against prediction dates;
  - (c) whether anything after the frozen plan touched the holdout;
  - (d) whether the onboarding test handles time-zero alignment;
  - (e) whether the stated conclusion matches the runner's result and its uncertainty.
- The audit passes when the analyst finds no unresolved leakage path and judges the conclusion supported as written. Report the verdict and its findings. The audit does not replace or relax the judge below.

Reporting
- Report missed targets plainly: a failed reproduction, failed separation, a miscalibrated model, a weak subgroup, or an onboarding explanation that does not hold.

With my approval only: change the existing evaluation runner, including its confidence-interval method or split logic.

First checks
Confirm each of the following before any analysis:
- the training set and holdout are present, and the holdout has no prior scoring or access in its records;
- the existing evaluation runner runs and supports customer-grouped splits and a confidence interval for the precision difference;
- the approved recall threshold value and how the runner sets its operating point;
- the customer ID field and per-row prediction dates;
- raw event logs covering onboarding;
- the written source of the onboarding explanation;
- the subgroup attributes in the de-identified data;
- the name of the independent analyst.
Name each missing dependency. Continue only with work the available artifacts support.

Judge: the existing evaluation runner must reproduce the baseline, enforce customer separation, and show holdout precision at the approved recall threshold above the baseline with a 95% confidence interval for the difference excluding zero. Otherwise report that the evidence does not establish improvement. Report the independent audit's verdict alongside this result.
```

- `depth`: raw-record leakage checks (ID overlap, feature timestamps against prediction dates, duplicate sequences) back up the runner's split logic. Benefit: catches leakage the split code cannot see. Risk: duplicate matching touches de-identified data, so the prompt limits it to leakage detection.
- `depth`: a dated, frozen analysis plan and a single holdout scoring make "do not tune on the holdout" checkable by the auditor.
- `depth`: named calibration instruments (reliability diagram, Brier score, intercept and slope), plus subgroup counts, intervals and small-n flags. These sharpen the approved checks without adding metrics.
- `depth`: a supplementary customer-clustered paired bootstrap. Benefit: shows whether the runner's interval is too narrow when customers contribute several rows. The judge stays the runner.
- `range`: the epidemiology time-zero alignment (immortal-time bias) check on the onboarding explanation. It reveals whether the explanation is an artifact of short follow-up.
- `range`: the red-team audit rubric now has five concrete items and a passing verdict. It is reported beside the owner's pass condition, which is unchanged.
- Skipped: `altitude`. The higher rungs (analyst action on flags, retention outcomes) need live pilots or new metrics, and the owner fixed the scope as offline only and the methods as closed. A hard target is also skipped: raising model performance would require tuning, which is outside an evaluation.
- Owner actions:
  - confirm the approved recall threshold and how the runner defines the operating point;
  - confirm the holdout is untouched;
  - name the independent analyst;
  - supply the written onboarding explanation;
  - decide whether to approve runner changes if its interval resamples rows rather than customers.
