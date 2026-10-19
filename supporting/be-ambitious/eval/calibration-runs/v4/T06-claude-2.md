```text
Goal: explain why customers churned last month, well enough to decide which retention fix to test first. Assumption (inferred): the result will drive a decision about where to invest, such as onboarding, product, pricing, or sales targeting. Confirm this with me.

Constraints: do not buy data, scrape customer information, or request production credentials. I have no raw event logs, CRM export, or database access to share right now. Treat the sales team's view that onboarding is the cause as a hypothesis to test, not a finding.

First checks, before any analysis:
1. Ask me which evidence I can already reach without new access. Examples: cancellation-reason fields, exit-survey responses, support tickets, billing or dunning summaries, onboarding-completion reports, and churn counts for last month and the 3–6 months before it. List what is missing.
2. Establish whether churn last month was actually higher than usual, using the same churn definition each month. If no baseline exists, say so. Without one, "why did customers churn last month" and "why do customers churn" cannot be told apart.
3. If none of this evidence is available, do not invent figures or causes. Deliver the hypothesis map, predictions, and analysis plan below, and mark every causal claim unverified.

Method:
- Separate the churn types before explaining them: voluntary cancellation, involuntary churn (failed payment or card expiry), downgrade, and non-renewal. Each has different causes and fixes.
- Build a set of competing hypotheses using Analysis of Competing Hypotheses. At minimum include:
  - onboarding failure
  - poor-fit customers acquired by sales (oversold, wrong segment or deal source)
  - a product defect or outage
  - a price or packaging change
  - a competitor move
  - involuntary payment churn
  - seasonality or contract-renewal timing
  - a few large accounts dominating the count
  For each hypothesis, write down before seeing data the evidence that would support it and the evidence that would rule it out.
- Use survival analysis to separate the hypotheses:
  - Plot churn by tenure at cancellation, with Kaplan-Meier curves by signup cohort.
  - Onboarding-caused churn should cluster in early tenure and among accounts that never activated or finished onboarding.
  - Poor-fit churn should show up regardless of onboarding completion and cluster by segment, rep, or deal source.
  - A product or pricing shock should hit all tenures together in one calendar window. This is the period-versus-cohort distinction used in epidemiology.
- Use a case-control comparison: churned versus retained accounts that were similar at signup, compared on onboarding completion, activation, and support contact.
- Weight what customers did, such as usage decline and tickets, above stated cancellation reasons. Stated reasons are often post-hoc.
- Red team: the sales team's hypothesis is convenient for the sales team. Check explicitly whether the "onboarding" pattern is really a poor-fit-acquisition pattern. Also report which result would change the decision.

Deliverable: a short decision memo with these parts:
- the churn breakdown by type
- the ranked hypotheses, each labeled observed evidence, inference, or unverified
- the evidence behind each ranking
- what remains unknown and the cheapest evidence that would resolve it
- one recommended intervention to test, with the metric it should move

With my approval only: I share aggregated or anonymized exports, such as cancellation reasons, onboarding status, and tenure, for the analysis above.
With my approval only: interview 5–10 churned customers using Jobs-to-be-Done switch interviews, to learn what they moved to and what triggered it.
With my approval only: run the recommended intervention as a measured pilot with a holdout group, and compare churn in the first 90 days of tenure against the holdout.

Judge:
- Hypotheses and their predictions are written down before any data is examined.
- Any causal finding drawn from last month's churners is confirmed on a cohort not used to form it, such as an earlier month's churners. Otherwise it is labeled unverified.
- An independent reviewer outside the sales team (for example, a CS or finance analyst) scores the memo against a rubric:
  - alternatives considered
  - evidence matched to each claim
  - unknowns stated
  - the recommendation follows from the evidence
- Pass: the reviewer confirms every causal claim either rests on cited evidence or is labeled unverified, and agrees that the onboarding hypothesis was tested against at least the poor-fit, product, pricing, and involuntary-churn alternatives.
- If no evidence was available, pass means a complete hypothesis map, pre-registered predictions, and a minimum data list, with no fabricated findings.
```

**Ledger**
- `altitude`: The outcome moves from "why customers churned" to a ranked explanation plus which retention fix to test first. A pilot with a holdout is offered behind approval. The memo stays in scope; the pilot needs approval and resources.
- `depth`: The prompt now tests the sales team's onboarding belief instead of accepting it. It does this by separating churn types, checking last month against a baseline, and using tenure-based survival analysis and a case-control comparison. It never fabricates results when data is missing. It needs no new access, but shared exports sit behind approval.
- `depth`: Findings are confirmed on a cohort they were not drawn from, which guards against fitting a story to one month. This depends on having a prior month's data.
- `range`: Intelligence analysis contributes Analysis of Competing Hypotheses, which writes down disconfirming evidence before the data is seen.
- `range`: Epidemiology contributes the period-versus-cohort distinction and the case-control design, which separate onboarding problems from product shocks.
- `range`: Customer research contributes Jobs-to-be-Done switch interviews. Contacting customers is outward-facing, so it sits behind approval.
- `range`: The red team checks whether "onboarding" is masking poor-fit customers acquired by sales. This exposes the main bias risk in the decision.
- Skipped: none. All three lenses add something the original task lacked.
- Owner actions:
  - Confirm the decision this analysis feeds.
  - List the evidence you can reach without new access.
  - Supply or confirm a churn baseline for prior months.
  - Decide on export sharing, customer interviews, and the pilot.
  - Name an independent reviewer outside the sales team.
