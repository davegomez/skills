```text
Explain why customers churned last month, so the team can decide where to spend retention effort. Treat the sales team's view that onboarding is the cause as one hypothesis to test, not as the answer.

Constraints (all binding):
- I have no raw event logs, CRM export, or database access to share right now.
- Do not buy data, scrape customer information, or request production credentials.
- Keep "last month" as I wrote it. Ask me for the exact date range; do not infer it.

First checks, before any analysis:
1. Ask me which of these I can supply without production credentials, and in what form (for example, an anonymized spreadsheet I already have): the list of churned and retained accounts, signup date, plan or segment, onboarding milestones completed, product usage summaries, support tickets, cancellation reasons or survey answers, pricing or billing changes, and notes from sales or customer success.
2. Ask me how our onboarding is defined: its steps and the time window it covers.
3. Ask me what else changed last month: releases, pricing, competitors, staffing, seasonality.
Name every missing dependency. Continue only with work the available material supports, and label every claim as observed evidence, inference, or unverified.

Method:
- Build a competing-hypotheses list, at minimum: onboarding, product fit or value, pricing or budget, product reliability or a specific release, support experience, competitor switch, involuntary churn (failed payment), and customer-side events such as layoffs or projects ending. Use Analysis of Competing Hypotheses: a matrix scoring each piece of evidence against every hypothesis, so evidence that fits all of them carries no weight.
- Before looking at any data, write falsifiable predictions for each hypothesis. Example for onboarding: churned accounts are concentrated inside the onboarding window, and among accounts of similar tenure, churned accounts completed fewer onboarding milestones than retained accounts. Write down what result would refute each hypothesis.
- Compare churned accounts with retained accounts (case-control), never churned accounts alone. A problem that is just as common among retained customers does not explain churn.
- If account-level data arrives:
  - Run a survival analysis, using a Kaplan-Meier churn curve by tenure and segment, to show whether last month's churn is early-life or late-life.
  - If there are enough accounts, fit a Cox proportional hazards model to estimate each factor's association with churn while holding the others constant.
  - Report effect sizes with confidence intervals and account counts.
  - Say which findings are only correlational.
- If only qualitative material arrives (cancellation reasons, call notes), code it with a written codebook. Report the share of churned accounts per code and separate stated reasons from observed behavior.
- Find patterns on one portion of the data. Confirm them on a portion not used to find them, such as a held-out half of accounts or an earlier month's churn. Anything not confirmed stays a lead, not a finding.

Deliverable: a brief answering "why did customers churn last month" with the following parts.
(a) Each hypothesis marked supported, refuted, or unverified, with the evidence behind it.
(b) A direct verdict on the onboarding hypothesis.
(c) The retention actions the evidence supports, ranked by how much churn they could address. For each, state the leading indicator to watch.
(d) The minimum additional data that would settle what remains unverified.
If no data can be supplied, deliver the hypothesis matrix, the pre-registered predictions, and the data specification, with every causal claim marked unverified.

With my approval only: contact churned customers for exit or switch interviews (Jobs-to-be-Done "switch" interviews: what triggered the search, and what they moved to).
With my approval only: interview internal sales, customer success, or support staff, or request exports from other teams.
With my approval only: design a measured pilot of the top-ranked retention action against a comparison group, to test whether it lowers churn.

Judge: the pre-registered predictions, evaluated on data not used to form them. Pass condition: the brief states, for every hypothesis including onboarding, whether its predictions held or failed on the confirmation data, with the comparison against retained accounts, effect sizes, and counts. Any hypothesis whose predictions were not tested is reported as unverified, not as a cause. If a qualified analyst outside this work, such as a data or retention lead, is available, they review the hypothesis matrix and conclusions against this rubric: competing causes considered, retained-account comparison present, claims traced to evidence. Their review is reported separately from the analysis.
```

- `altitude`: The original outcome was a stated reason for churn. The improved outcome is a ranked set of retention actions with leading indicators, plus an approval-gated pilot to test the top one. The pilot needs a comparison group and time to measure.
- `depth`: The sales team's onboarding belief becomes one falsifiable hypothesis, with predictions written before any data is seen. This prevents confirmation of the default story.
- `depth`: The prompt asks for account-level records instead of summaries. It specifies Kaplan-Meier survival curves and Cox hazards models, and confirms findings on held-out data. This turns a narrative into checkable claims.
- `range`: Two fields contribute methods.
  - Epidemiology contributes the case-control comparison against retained accounts, which exposes problems that are common to everyone and so explain nothing.
  - Qualitative research contributes codebook coding and Jobs-to-be-Done switch interviews, which reveal triggers that usage data misses.
- `range` (red team): Analysis of Competing Hypotheses tests the consequential onboarding claim against at least seven alternatives. Involuntary churn from failed payments is one alternative that an onboarding fix would never touch.
- `depth` (defect fix): The original task cannot be answered from the evidence given. The rewrite adds a defined no-data output in which every causal claim is marked unverified, so the result can no longer be an unsupported verdict.
- Scope, cost, and risk:
  - Customer interviews are outward-facing.
  - Staff interviews and exports from other teams are new access.
  - The pilot is a new workflow.
  - All three sit behind approval lines. Nothing buys data, scrapes, or uses production credentials.
- Skipped: The hard-target move was not used, because there is no baseline metric to stretch against without data.
- Owner actions:
  - Confirm the date range for "last month".
  - Say what account data you can share, in anonymized form if needed, and define your onboarding steps and window.
  - List what else changed last month.
  - Decide on churned-customer interviews, staff interviews, and the pilot.
  - Name an independent reviewer if one is available.
