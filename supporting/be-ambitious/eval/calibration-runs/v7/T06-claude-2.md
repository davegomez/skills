```text
Goal: explain why customers churned last month well enough to decide which retention fix to fund first, and say plainly what the current evidence can and cannot support.
Assumption: the result will be used to choose and prioritize a retention intervention, so the answer must rank causes by evidence and say what would change the ranking.
Assumption: "churned" means cancelled or did not renew last month. State the definition you use and flag it for confirmation.

Constraints (fixed):
- No raw event logs, CRM export, or database access is available right now. Do not invent figures, cohorts, or customer quotes. Label every statement as observed evidence (with its source) or hypothesis.
- Do not buy data, scrape customer information, or request production credentials.

First checks, before any analysis:
1. List what evidence actually exists in this conversation and workspace: the sales team's belief that onboarding is the cause, and anything else I have supplied.
2. Ask me once for any aggregate facts I can share without new access, such as churned-account count, prior months' churn for a baseline, a tenure-at-churn breakdown, plan mix, or how the sales team formed its view. Proceed with whatever I give you. Name each gap that remains.
3. Continue only with work the available evidence supports. Where evidence is missing, produce the test design, not a conclusion.

Method:
- Treat "onboarding caused it" as one hypothesis to test, not a premise. Use Analysis of Competing Hypotheses (from intelligence analysis). Build a matrix with onboarding failure and at least these rivals:
  - poor customer fit at sale (mis-sold or wrong segment)
  - product gaps or reliability problems
  - price or budget
  - a competitor
  - support experience
  - involuntary churn (failed payments)
  - seasonality or contract-renewal timing
  For each hypothesis, write the observable predictions that distinguish it from the others. For example, if onboarding is the cause, churn should be concentrated in early-tenure accounts and in accounts that did not finish onboarding, with less churn among long-tenure accounts. Rank the evidence by how well it discriminates between hypotheses, not by how much of it agrees with one.
- Separate voluntary churn from involuntary churn before attributing any cause.
- Name the confounding risk, using the case-control framing from epidemiology. Accounts that skip onboarding may be the poor-fit or low-intent accounts, so an onboarding gap can be a symptom of a bad sale rather than the cause of churn. State which comparison would separate the two, for example onboarding completion compared within the same segment and deal source.
- Red-team the leading hypothesis with a pre-mortem: assume the onboarding fix ships and churn does not move. List the most likely reasons, then check which of those reasons the current evidence can rule out.
- For every hypothesis that stays open, write a ready-to-run analysis spec covering:
  - the data needed, at the most raw level available (events and account records, not dashboard summaries)
  - the method: last-month churners compared with retained accounts as a cohort or case-control comparison, Kaplan–Meier retention curves split by onboarding completion, and Cox regression controlling for segment, plan, and deal source
  - the result that would confirm or refute the hypothesis
  Fix each hypothesis and its prediction before looking at any data. Confirm any pattern on data not used to find it, such as a held-out random half of accounts or a prior month. Otherwise mark the pattern unverified.
- If the evidence supports it, recommend the first intervention and a measured pilot to test it: target segment, control group, primary metric, duration, and the effect size that would justify a rollout.

With my approval only: request a de-identified CRM export or analytics extract from an internal data owner (not production credentials), and run the analysis specs on it.
With my approval only: interview internal customer success, support, and sales staff about specific churned accounts. Use a structured guide and log each answer against the hypothesis matrix.
With my approval only: contact churned customers for exit or switch interviews (jobs-to-be-done style: what triggered leaving, what they moved to).

Deliverable: a written answer to "why did customers churn last month?" containing:
- a one-paragraph bottom line stating how confident it is
- the competing-hypotheses matrix
- what is known versus what is assumed
- the analysis specs for the open hypotheses
- the recommended next step

Judge: a retention, customer-success, or analytics lead other than the author reviews the answer against these criteria:
(a) every claim is labeled observed or hypothesis, and observed claims cite a source;
(b) onboarding is tested against at least the listed rivals, with predictions that distinguish them;
(c) involuntary churn and the fit-versus-onboarding confound are addressed;
(d) no conclusion goes further than the evidence;
(e) each open hypothesis has a spec naming its data, method, and confirm/refute result;
(f) any quantitative pattern is confirmed on held-out data or marked unverified.
Pass only if every criterion is met. Until real churn data is analyzed, the root cause stays unverified.
```

- `altitude`: The original outcome was a stated reason for churn. The improved outcome is a ranked, evidence-labeled diagnosis tied to which retention fix to fund, plus a pilot design for that fix. The pilot spec adds no cost; running a pilot would be a separate decision.
- `depth`: The sales team's onboarding belief becomes a hypothesis tested against rivals, with predictions that tell them apart. This guards against confirmation bias and costs nothing.
- `depth`: Analysis specs that start from raw data (cohort and case-control comparisons, Kaplan–Meier curves, Cox regression), with predictions fixed in advance and held-out confirmation. The owner can run them as soon as data exists. Until then, conclusions stay unverified.
- `depth`: Voluntary and involuntary churn are separated before attributing cause. This keeps payment failures from being misread as onboarding failures.
- `range`: Analysis of Competing Hypotheses, from intelligence analysis, organizes thin evidence by how much it discriminates between causes.
- `range`: Case-control thinking and confounding, from epidemiology, expose the risk that skipped onboarding is a symptom of a bad sale rather than the cause of churn.
- `range`: The pre-mortem (red team) tests the onboarding fix before money is spent on it.
- `range`: Switch interviews, from jobs-to-be-done research, capture what triggered customers to leave. These sit behind approval because they mean contacting customers.
- Access effects: CRM or analytics extracts, staff interviews, and customer contact each sit on their own approval line. Buying data, scraping, and production credentials are excluded entirely.
- Skipped: none. All three lenses fit, because the task rests on an untested belief and has no data yet.
- Owner actions:
  - Confirm the churn definition.
  - Supply any aggregates you can share.
  - Decide whether to approve the data extract, staff interviews, and customer interviews.
  - Name the reviewer who will act as judge.
