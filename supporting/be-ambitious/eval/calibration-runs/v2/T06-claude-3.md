```text
Goal: explain why customers churned last month, assumed to be September 2026 (confirm the month and whether "churn" means cancelled logos, lost revenue, or both). The explanation should support a decision about which retention problem to fix first. Assumption: the owner will use the answer to choose a retention intervention, and the sales team's onboarding theory is one candidate to test, not a conclusion to confirm.

Hard constraints: do not buy data. Do not scrape customer information. Do not request production credentials. Use only data the owner chooses to export and share, preferably aggregated or de-identified.

First, check dependencies and report each one as available, unavailable, or unknown. Right now the owner has no raw event logs, CRM export, or database access.
- List the minimum the owner could export themselves: churned and retained accounts with signup date, cancel date, plan and MRR, cancel reason codes, and voluntary vs involuntary (payment failure) flag; onboarding milestone completion; support ticket counts and text; exit survey or NPS responses; contract renewal dates.
- Also list what proxies exist without any export: cancellation-flow free text, support inbox, billing dashboard summaries, and sales call notes.
- If nothing is shared, do not name a cause. Deliver the plan below and state that the cause of churn is unverified, including the onboarding theory.

Before any data arrives, write a hypothesis register (Analysis of Competing Hypotheses).
- Candidates: onboarding/activation failure; involuntary churn from failed payments; price or plan fit; missing features or competitor switch; product reliability; support experience; annual-renewal timing or seasonality; customer-side events such as budget cuts or company closure; account mix shift from recent sales targeting.
- For each hypothesis, pre-register its observable prediction. Example: onboarding failure predicts churn concentrated in accounts under 90 days of tenure, with lower milestone completion than retained accounts from the same signup cohort. A theory that fits long-tenure churners equally well is not onboarding.
- Record which evidence would count against each hypothesis.

Once data is available:
1. Check whether last month was abnormal. Compare it to the trailing 12 months with a control chart. If it falls within normal variation, say so: the question becomes ongoing churn, not a spike.
2. Split churn into voluntary vs involuntary, and into logo vs revenue churn.
3. Run cohort and survival analysis (Kaplan-Meier curves by signup cohort, plan, and acquisition channel) to locate churn by tenure.
4. Compare churned vs retained accounts as a case-control study, matched on cohort and plan, to avoid base-rate errors. Report effect sizes with confidence intervals, not counts alone.
5. Code ticket, exit survey, and cancellation text with a written codebook. Have a second coder, or a blind second pass, code a 20% sample, and report Cohen's kappa.
6. Before analyzing, hold out a random 30% of churned accounts and text. Find patterns on the remaining 70%, then confirm them on the holdout.

Red team: the sales team has an incentive to attribute churn to post-sale stages. Score every hypothesis against the same evidence. Also run a pre-mortem: "We fixed onboarding and churn didn't move. Why?"

Only with owner approval: churned-customer switch interviews (jobs-to-be-done timeline method, 8–12 accounts, through the owner's existing customer channels). Contacting customers is outward-facing.
Only with separate owner approval: propose a measured retention pilot for the top-ranked cause, with a control group, a primary metric (e.g., 90-day retention of new cohorts), and the sample size needed to detect the target effect.

Deliverable: a one-page answer for decision-makers with the following:
- the churn causes, ranked by share of lost accounts and revenue
- the evidence grade for each: observed and confirmed on holdout, observed but unconfirmed, or proposed
- a verdict on the onboarding theory, labeled supported, contradicted, or untested
- the recommended next decision
Below the page, include the hypothesis register, the methods, and the data gaps. Keep observed evidence and proposed explanations visibly separate.

Judge: each causal claim must match a prediction registered before the data was examined and must hold on the 30% holdout. Report the effect size and confidence interval. For qualitative themes, report kappa ≥ 0.7. For the onboarding theory, report the tenure distribution of churners and the matched milestone-completion gap.
Pass condition: every listed cause carries an evidence grade, and only holdout-confirmed causes are stated as findings. If no data is supplied, the run passes only if it delivers the register, the export request list, and the analysis plan, and explicitly declines to name a cause.
```

**Ledger**
- `altitude`: The original task, "tell me why customers churned," becomes ranked causes that drive the choice of a retention fix, with an optional controlled pilot. Benefit: the answer becomes a decision. The pilot adds scope and is behind owner approval.
- `depth`: Pre-registered predictions, a voluntary vs involuntary split, an anomaly baseline, survival curves, a matched case-control design, and a 30% holdout. Benefit: the onboarding theory gets tested against raw evidence rather than repeated. Requires owner-supplied exports.
- `depth`: With no data, the run delivers a plan and states the cause is unverified instead of guessing. Benefit: no false finding reaches the people deciding on it.
- `range`: Intelligence analysis (competing hypotheses) and a red team on sales incentives. Benefit: alternative causes get scored against the same evidence.
- `range`: Epidemiology (case-control, base rates) and qualitative research (codebook, kappa, JTBD switch interviews). Benefit: it separates "common among churners" from "more common than among retained accounts," and adds a reliability check for text evidence. Interviews contact customers and are behind owner approval.
- Skipped: none. All three lenses fit, because people will act on this answer and it rests on an untested belief.
- Owner actions:
  - Confirm the churn month and definition.
  - Decide which exports you can share, ideally de-identified. No production credentials are requested.
  - Approve or decline customer interviews.
  - Approve or decline the retention pilot.
