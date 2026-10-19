```text
Tell me why customers churned last month. Treat "the sales team thinks onboarding is the cause" as a hypothesis to test, not the answer.

Assumption: the result will be used to decide where to spend retention effort, so the deliverable is a decision memo. It ranks candidate causes by evidence strength, states what is observed and what is only hypothesized, and names the cheapest evidence that would change the decision.

Constraints (hold throughout):
- No raw event logs, CRM export, or database access are available right now. Do not invent counts, rates, accounts, or quotes. Label every claim either "observed: <source>" or "hypothesis".
- Do not buy data, scrape customer information, or request production credentials.

First checks, before any analysis:
1. List what I can already share without new access: cancellation reasons or exit-survey text, support tickets, the sales team's per-account notes on who churned and why, billing summaries, and onboarding checklists.
2. For each item, state what it can and cannot show.
3. If nothing is available, say so plainly. Deliver the plan below with every finding marked unverified, and report "cause unknown" as the current answer.

Method:
1. Build the rival hypotheses with Analysis of Competing Hypotheses, a matrix from intelligence analysis that scores each piece of evidence by how well it separates hypotheses, not by how well it fits one. Include at least:
   - onboarding failure
   - poor fit at the point of sale (mis-sold accounts; sales has an incentive to locate the cause after the handoff)
   - product gaps
   - price or budget
   - competitor switch
   - involuntary churn (failed payments)
   - support experience
   - contract-renewal timing or seasonality
2. Pre-register falsifiable predictions for each hypothesis, written down before any data is seen. Onboarding as cause predicts three things:
   - Churn concentrates in early tenure, within the onboarding window the company defines.
   - Churned accounts completed fewer onboarding milestones than retained accounts that signed up in the same period.
   - Exit reasons cite setup, time-to-value, or adoption.
   If churned and retained accounts show similar onboarding completion, onboarding does not distinguish the churners, whatever the sales team observed.
3. Specify the analysis to run once data exists, with the minimum de-identified account-level fields each step needs (account ID hash, signup date, churn date, plan, segment, sales owner, onboarding milestones completed, voluntary/involuntary flag, exit reason):
   - Kaplan-Meier survival curves by signup cohort, to show whether churn hazard peaks during onboarding or later.
   - A case-control comparison of churned vs. retained accounts, as in epidemiology, to supply the base rate that the sales anecdote lacks.
   - A Cox proportional-hazards model with onboarding completion as a covariate, adjusted for segment, deal size, and plan, so onboarding is not credited for effects of account type.
   - A split of voluntary from involuntary churn before any cause analysis.
4. Draft a switch-interview guide, a jobs-to-be-done technique that reconstructs the timeline from first doubt to cancellation, to find causes no structured field records.
5. Red-team the result:
   - Run a pre-mortem on the leading explanation: "It is six months later and fixing this did not reduce churn. Why?"
   - Name the evidence that would overturn it.
   - Apply the same test to any explanation that replaces onboarding.
6. Treat any new explanation found while exploring the data as development evidence. Confirm it on churners from a different month that were not used to find it, or report it as unverified.

With my approval only: I provide de-identified account-level exports covering the fields listed in step 3, for the analysis.
With my approval only: contact churned customers for switch interviews or an exit survey.
With my approval only: run a measured pilot of an onboarding change with a randomized or matched holdout group, if the evidence points to onboarding, and report the churn difference against the holdout.

Deliverable: a decision memo that answers "why did customers churn last month" with the best supported answer, or "unknown" with the leading hypotheses. It contains:
- the hypothesis matrix
- the pre-registered predictions
- the observed/hypothesis label on every claim
- the data list and analysis plan
- the interview guide
- the red-team findings
- a recommendation on whether to invest in onboarding now, wait for evidence, or test with a pilot

Judge: an independent reviewer outside the sales team scores the memo against this rubric:
(a) every causal claim traces to a named observed source or is labeled hypothesis;
(b) every hypothesis has a stated prediction that would disconfirm it;
(c) churned accounts are compared with retained accounts, or the memo states that the comparison is missing;
(d) no figure appears without a source.
Pass condition: all four criteria hold. Once data arrives, the pre-registered predictions are run and reported as confirmed or disconfirmed, and any new finding is confirmed on a held-out month or left marked unverified.
```

**Ledger**

- `altitude`: The original outcome was an explanation of last month's churn. The improved outcome is a decision memo on where to spend retention effort, including the cheapest evidence that would change that decision. It is checked by the reviewer rubric. There is no added access or cost.
- `depth`: The sales belief is treated as a hypothesis with pre-registered falsifiable predictions and a churned-vs-retained base rate. Kaplan-Meier, a case-control comparison, Cox regression, and a voluntary/involuntary split are specified to run once data exists. New findings require held-out confirmation. This prevents a plausible but untested story from driving spend.
- `range`: Three fields contribute methods. Analysis of Competing Hypotheses comes from intelligence analysis and scores evidence by how well it separates explanations. Switch interviews come from jobs-to-be-done research and recover causes no structured field records. A pre-mortem red team tests the leading explanation and its replacement. Together they surface rival causes, including mis-sold accounts, which sales may be motivated to overlook.
- `altitude` (approval): The original outcome was diagnosing churn. With approval, an onboarding pilot with a holdout group would measure whether changing onboarding reduces churn. This is customer-facing and needs owner approval.
- `range` (approval): Interviewing churned customers is outward-facing contact and needs owner approval.
- Skipped: none. All three lenses contributed.
- Owner actions:
  - List any artifacts you can already share, such as exit reasons, tickets, or sales notes.
  - Decide whether to approve de-identified exports.
  - Decide whether to approve customer interviews or a survey.
  - Decide whether to approve the onboarding pilot.
  - Name an independent reviewer outside the sales team.
