```text
Tell me why customers churned last month, and recommend which retention action deserves investment first.
Assumption: the answer will be used to decide whether to put retention effort into onboarding, as the sales team proposes, or into some other cause.
Assumption: no churn data is available to you right now. No cause can be observed yet, so the first deliverable is a decision-ready diagnosis plan, not a verdict.

Constraints: do not buy data, scrape customer information, or request production credentials. Label every statement as one of: observed (with its source), reported belief (with who holds it), or hypothesis.

First checks, before any analysis:
- List what I can share without production credentials. Examples: churned-account counts from billing, cancellation-reason fields, exit-survey responses, support tickets, sales or CS notes on lost accounts, onboarding-completion flags, and existing dashboards I already see.
- Name each missing dependency and what it blocks.
- Continue only with work the available material supports.

Method:
1. Treat "onboarding caused it" as a reported belief to test, not a finding.
   - Record what the sales team observed that led to it: which accounts, how many, and what they heard.
   - Note whether that evidence covers only churned accounts. If it does, it has no comparison group.
2. Build a differential diagnosis using Analysis of Competing Hypotheses, a structured method from intelligence analysis for weighing evidence against every candidate cause.
   - List rival causes next to onboarding: involuntary churn (failed payments), price or budget cuts, product gaps or fit, a competitor switch, a champion leaving the customer's company, contract-renewal timing, a recent release or outage, and a change in which customers were acquired.
   - For each cause, state the evidence that would refute it.
   - Rank causes by how little evidence contradicts them, not by how much supports them.
3. For each hypothesis, write a prediction that separates it from the others. For onboarding, two examples:
   - Churned accounts completed fewer onboarding milestones than retained accounts from the same signup period, using a case-control comparison.
   - Churn risk is concentrated in the first weeks after signup, using a Kaplan-Meier survival curve by onboarding status.
   For each prediction, name the smallest dataset that tests it, obtainable within the constraints above. Prefer aggregate or de-identified fields.
4. Split voluntary from involuntary churn before looking for any cause. Report last month's churn against the prior months' base rate, so the size of the problem is clear.
5. Draft a switch-interview guide, a Jobs-to-be-Done method that reconstructs the timeline of the decision to leave. Include questions that do not lead toward onboarding.
6. Pre-register the predictions in writing before seeing any data. Any cause proposed after seeing data stays unverified until it is confirmed on accounts or months not used to form it.
7. Give a recommendation under uncertainty:
   - The action you would fund now.
   - The cheapest evidence that would change that choice.
   - What it would cost to act on onboarding if onboarding is not the cause.

With my approval only: receive a de-identified or aggregate export of churned and retained accounts from someone already authorized to pull it.
With my approval only: contact churned customers for exit surveys or switch interviews through channels the company already uses.
With my approval only: run a holdout pilot of an onboarding change and measure early-tenure churn against the holdout.
With my approval only: set up recurring churn-reason capture and a cohort retention dashboard.

Deliverable:
- The ranked hypothesis table, with each cause's discriminating prediction, required data, and current evidence status.
- The evidence request list.
- The interview guide.
- The recommendation.
Any measured results are reported only where approved data exists.

Judge: a customer-success or analytics lead other than the author checks these criteria:
(a) Every claim is labeled observed, reported belief, or hypothesis, and no cause is stated as observed without a cited source.
(b) The onboarding hypothesis has at least one stated prediction that would refute it, plus a comparison against retained accounts.
(c) At least five rival causes are assessed, with involuntary churn separated out.
(d) Each data request is obtainable without purchase, scraping, or production credentials.
(e) The recommendation names what evidence would reverse it.
Pass only if every criterion is met. Any cause claim stays unverified until its pre-registered prediction is tested on data not used to form it.
```

- `altitude`: The original outcome was an explanation of last month's churn. The improved outcome is a decision on which retention action to fund first, with the evidence that would reverse it. It adds no scope, and the pilot and dashboard sit behind approval.
- `depth`: The sales belief becomes a hypothesis tested against retained accounts. This counters the "only looked at churned customers" bias and makes onboarding falsifiable. It costs nothing until data is shared.
- `depth`: The rewrite splits voluntary from involuntary churn and compares against a base rate. Failed payments often look like dissatisfaction, and this also shows whether last month was unusual at all.
- `depth`: Predictions are pre-registered and held out, so a cause found by browsing data is not reported as confirmed.
- `range`: From intelligence analysis, Analysis of Competing Hypotheses acts as a red team against confirmation bias toward onboarding.
- `range`: From epidemiology, the case-control design compares churned with retained accounts. From biostatistics, survival analysis shows *when* churn happens, which separates onboarding from renewal or price causes.
- `range`: From qualitative research, Jobs-to-be-Done switch interviews recover the customer's actual decision timeline. Contacting customers is outward-facing, so it sits behind approval.
- Skipped: none. All three lenses fit, because the task rests on an untested belief and has no data yet.
- Owner actions:
  - List which internal artifacts you can share without production credentials.
  - Decide on the de-identified export, customer outreach, the holdout pilot, and recurring tracking.
  - Name the reviewer who acts as judge.
