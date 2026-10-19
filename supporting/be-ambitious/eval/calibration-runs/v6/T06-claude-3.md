```text
Tell me why customers churned last month. The decision this serves is which retention action to take, so the answer should rank candidate causes by evidence and say what each implies.

Assumption: the result goes to leadership and the sales team, who will choose a retention fix from it. An unsupported "onboarding" verdict would send that effort to the wrong place.
Assumption: no customer data is available yet, so this run produces a falsifiable diagnosis plan plus findings from whatever I supply. Label every cause "proposed" until evidence supports it.

Constraints: do not buy data, scrape customer information, or request production credentials. I have no raw event logs, CRM export, or database access to share right now.

First checks:
- List the artifacts that would answer this without production credentials. Examples: aggregate churn counts by month, cancellation reasons from the billing or subscription tool, exit-survey responses, support-ticket themes, signup dates of churned accounts, onboarding-completion flags, and any pricing, product, or staffing changes last month.
- Ask me which of these I can share. Continue only with what I supply, and name each gap and what it blocks.

Method:
1. Is last month abnormal? Compare last month's churn rate with prior months on a control chart (statistical process control). If it sits within normal variation, say so: then the question becomes the baseline churn rate, not a spike.
2. Classify churn as voluntary vs. involuntary (failed payments, expired cards). Involuntary churn is often a large share and is unrelated to onboarding.
3. Test the onboarding belief directly. If onboarding is the cause, churners should cluster early in tenure (roughly the first 30–90 days) and among accounts that did not complete onboarding. Use the tenure-at-churn distribution and a survival curve (Kaplan-Meier) by signup cohort and onboarding status. If churners are mostly long-tenured, onboarding is unlikely to be the main cause.
4. Build competing hypotheses with Analysis of Competing Hypotheses (ACH, from intelligence analysis). Candidates: onboarding, pricing or renewal changes, product gaps or reliability, competitor moves, segment or acquisition-channel mix, support quality, involuntary payment failure. For each, state the evidence that would refute it, and rank by least refuted, not most supported.
5. If account-level data arrives, separate confounders (plan, segment, channel, cohort size) from cause. Draw a causal diagram, as in epidemiology, and fit a Cox or logistic model on it. Do not read raw cross-tabs as causes.
6. If free-text reasons arrive (exit surveys, tickets), code them into themes with a written codebook. Report theme frequencies with example quotes.
7. Validate new findings. A pattern found on one slice of data is development evidence: confirm it on data not used to find it, such as a held-out random half or an earlier month's churners, or mark it unverified.

With my approval only: contact churned customers for exit interviews or surveys.
With my approval only: get read-only access to any additional internal system or export beyond what I hand over.
With my approval only: design a measured pilot of the top-ranked fix, with a holdout group, to confirm the cause by intervention.

Deliverable: a ranked list of candidate causes. For each cause, give the evidence for and against, its status (observed, proposed, or refuted), and the retention action it implies. Then give the data gaps and the next analysis each gap blocks.

Judge: an analyst independent of the sales team reviews the result against this rubric:
(a) every cause claim cites a supplied artifact or is labeled proposed;
(b) the onboarding hypothesis has an explicit refutation test, with its result or "untested — needs X";
(c) at least three competing hypotheses are weighed;
(d) any validated pattern was confirmed on held-out data.
Pass: the reviewer confirms (a)–(c), and (d) wherever a pattern is claimed as validated. With no data supplied, the run passes only as a plan, and every cause stays unverified.
```

- `altitude`: the outcome moves from "a reason customers churned" to "a ranked, evidenced cause list that picks a retention action." A holdout pilot that confirms the cause by intervention is available behind approval.
- `depth`: the onboarding belief is tested directly with tenure-at-churn and survival curves, involuntary churn is split out, confounders are modeled, and findings are confirmed on held-out data. This prevents the incumbent belief from being rubber-stamped. Scope is unchanged, and nothing runs without supplied data.
- `range`: statistical process control checks whether last month is a real spike. ACH from intelligence analysis red-teams the onboarding belief against rivals. Epidemiology's causal diagrams separate confounders from causes. Qualitative coding turns exit reasons into countable themes.
- Skipped: none. All three lenses fit, though data scarcity means this run produces a plan, not findings.
- Owner actions:
  - Say which listed artifacts you can share.
  - Name an independent reviewer.
  - Decide on customer outreach, additional access, and the pilot (each listed as "With my approval only").
