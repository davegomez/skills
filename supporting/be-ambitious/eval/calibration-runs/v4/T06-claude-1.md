```text
Goal: find out why customers churned last month and turn the answer into a decision about where to act first. Assumption (inferred, confirm): the result will drive a retention investment decision, so the deliverable should rank causes by how much churn each explains and name the cheapest test that would confirm each one.

Constraints (fixed): I have no raw event logs, CRM export, or database access to share right now. Do not buy data, scrape customer information, or request production credentials. Keep "last month" as the analysis window. The sales team believes onboarding is the cause. Treat this as a hypothesis to test, not a finding.

First checks, before any analysis:
1. List the evidence I can supply through channels I already have, and ask me which of these exist: billing/subscription exports with account ID, start date, cancel date, plan, MRR, and cancellation type (voluntary vs payment failure); cancellation-survey or exit-reason fields; support ticket exports; onboarding milestone or activation records; release notes or incident logs; pricing or packaging changes; the sales team's specific accounts and the reasoning behind the onboarding claim.
2. For each item, record whether it is available, its window, and its account count. Name what is missing.
3. If no account-level evidence is available, do not state causes as findings. Deliver part A only, and label every cause in it "hypothesis, unverified".

Part A: hypothesis map (always delivered)
- Separate churn into voluntary and involuntary (payment failure), and into logo churn and revenue churn. These have different causes, and onboarding cannot explain involuntary churn.
- Build an Analysis of Competing Hypotheses matrix. Rows: onboarding failure, involuntary/payment churn, price or packaging change, product quality or incidents, missing capability or competitor switch, customer-side change (budget cuts, the account's champion leaving, the account being acquired), seasonality or contract-renewal timing, and a sales-fit mismatch (customers sold a product they didn't need). Columns: evidence items. For each hypothesis, write the prediction that would distinguish it from the others. Example: if onboarding is the cause, churn concentrates in early tenure (the first 30–90 days) and among accounts that missed activation milestones, compared with retained accounts from the same signup cohorts. Late-tenure churn would contradict it.
- Write these predictions down before looking at outcome data. They are the pre-registered tests for part B.

Part B: evidence analysis (only on evidence I supply)
- Survival analysis: Kaplan-Meier retention curves by signup cohort, and the churn hazard by tenure. This shows whether risk peaks early, which onboarding would predict, or later. If enough accounts exist, fit a Cox model with onboarding completion, plan, and segment as covariates.
- Case-control comparison: compare last month's churned accounts with retained accounts matched on cohort and plan, so a trait isn't mistaken for a cause just because it is common.
- Base-rate check: compare last month with the prior months available. Was churn actually abnormal, or within normal variation? If it was abnormal, what changed that month?
- Exit reasons: code free-text cancellation reasons and support tickets with a fixed codebook. Report agreement if two coders are available. State that stated reasons can differ from actual causes.
- Red team: write the strongest case against the onboarding hypothesis and against your own top-ranked cause, then report which predictions held and which failed.
- Development and confirmation: any cause you add or revise after looking at the data is development evidence. Confirm it on evidence not yet used, such as a held-out cohort or a different month. Otherwise label it unverified.

Deliverable: a 1–2 page memo with these sections:
- Churn breakdown (voluntary/involuntary, logo/revenue)
- Ranked causes, with the share of churned accounts or revenue each explains and a confidence level
- The onboarding verdict: supported, contradicted, or untestable with the current evidence, with the specific test behind it
- The ACH matrix
- Recommended first action
- A data-request list for whatever remains untested

Mark each claim "observed in [source]" or "hypothesis".

With my approval only: contact churned customers for switch interviews (Jobs-to-be-Done "switch interview" method) to learn what pushed them away and what they switched to.
With my approval only: request exports from other internal teams, or share account-level data with anyone beyond me.
With my approval only: have an analyst outside sales review the memo against the rubric below.
With my approval only: run a retention pilot on the top-ranked cause, such as an onboarding intervention or dunning fixes, with a holdout group.

Judge:
- Every causal claim cites a supplied source, or is labeled "hypothesis, unverified".
- The onboarding hypothesis has a written prediction stated before analysis, and a reported result: supported, contradicted, or untestable.
- Ranked causes report their share of churn on the stated denominator.
- Any revised claim is confirmed on evidence not used to form it, or marked unverified.

Pass condition: all four judge checks hold, and someone who did not do the analysis can trace each ranked cause to its evidence row in the ACH matrix. If I approve the independent review, it passes when the reviewer finds no cause stated as a finding without evidence. If no evidence was supplied, the pass condition is a complete part A with discriminating predictions and a prioritized data-request list, and no causal findings.
```

- `altitude`: the original outcome was an explanation of last month's churn. The rewrite targets a ranked, quantified set of causes plus a recommended first action and the cheapest confirming test for each. The retention pilot sits behind approval because it costs time and touches customers.
- `depth`: the sales team's onboarding belief becomes a pre-registered, falsifiable prediction (early-tenure hazard concentration plus a milestone gap against matched retained accounts) instead of a premise. This reduces the risk of funding the wrong fix. There is no scope change.
- `depth`: the work starts from raw account-level exports where they exist, using Kaplan-Meier/Cox survival analysis, a voluntary/involuntary split, and a base-rate check against prior months. It needs only data you can supply. If none is supplied, the deliverable degrades honestly to hypotheses.
- `depth`: anything revised after seeing the data must be confirmed on held-out evidence or labeled unverified. This prevents a story fitted to the data from becoming the finding.
- `range`: intelligence analysis contributes Heuer's ACH matrix, which weighs evidence by how well it separates competing causes, not by how well it fits the favored one.
- `range`: epidemiology contributes the case-control design and base rates, which keep common traits of churned accounts from being mistaken for causes.
- `range`: qualitative research contributes a codebook for exit reasons and JTBD switch interviews. The interviews are approval-only because they mean outward contact with customers.
- `range`: a red-team step attacks both the onboarding claim and the analyst's own top cause.
- Skipped: none. All three lenses contributed.
- Owner actions:
  - Say which exports you can supply (billing/subscription, exit reasons, support tickets, onboarding milestones, incident and pricing history).
  - Get the sales team's specific accounts and reasoning.
  - Confirm the inferred goal (a retention investment decision).
  - Decide on the four approval-only items: switch interviews, cross-team data requests or sharing, independent review, and the retention pilot.
