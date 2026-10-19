```text
Explain why customers churned last month, and test the sales team's belief that onboarding is the cause. Do not treat that belief as the answer.

Assumption: the explanation exists to decide where retention effort goes next, for example an onboarding fix, product gaps, pricing, support, or billing recovery. Frame the result as that decision. For each candidate cause, give its estimated share of churn, the evidence strength, and the cheapest action that would confirm or refute it.
Assumption: "churned" can mean lost accounts or lost revenue, and voluntary cancellation or failed payment. Report each meaning separately when the data allows. If the company's definition is unknown, state the one you used.

Current constraints: no raw event logs, CRM export, or database access is available. Do not buy data, scrape customer information, or request production credentials. Keep "last month" as written and confirm its exact dates with me.

First checks, before any analysis:
1. List the data I can supply without production credentials, such as a subscription or billing export, cancellation reasons, support tickets, onboarding milestone records, sales or account notes, and plan, size, and tenure fields. List which of these exist.
2. Get the count of churned accounts and the count of retained accounts for the same period.
3. Get the sales team's specific claim: which accounts, which onboarding failure, and how they know.
If no data arrives, deliver only these: a competing-hypotheses map, the analysis plan below, a minimal ranked data request, and the predictions each hypothesis makes. Label all of it as hypotheses. State no causes as findings.

Method, once data is available:
- Base rates, borrowed from epidemiology (case-control design). Compare churned accounts with retained accounts from the same signup cohorts. An onboarding problem among churners proves nothing unless it is rarer among customers who stayed. Stratify by plan, company size, acquisition channel, and sales owner. Small accounts may both skip onboarding and churn for unrelated reasons.
- Tenure hazard, borrowed from reliability engineering (Kaplan-Meier curves, plus a Cox model if the counts allow). Plot churn by account age. Onboarding-driven churn should concentrate early in the account's life. Churn among long-tenured accounts points elsewhere, for example price, a competitor, a champion leaving, or a product regression.
- Analysis of Competing Hypotheses, borrowed from intelligence analysis. Build a matrix with these hypotheses as rows: onboarding, product fit or missing features, price or budget, competitor, support quality, reliability incidents, involuntary payment failure, and loss of a champion. Use each evidence item as a column. Rank hypotheses by how much evidence contradicts them, not by how much supports them.
- Thematic coding of free text, borrowed from qualitative research (switch-interview framing: push, pull, anxiety, habit). Code cancellation reasons, tickets, and notes. Have a second coder, or a blind second pass, code a sample, and report agreement.
- Pre-register the onboarding test before looking at outcomes. If onboarding drives churn, three things should hold: accounts that missed activation milestones churn at a higher rate than comparable accounts that hit them; churn concentrates in the first tenure months; and churn reasons cite setup or time-to-value. Report each prediction as held, failed, or untestable.
- New findings: split the churned accounts and text into a development half and a held-out half. Form hypotheses on the development half and confirm them on the held-out half. Label any claim that has not been confirmed as unverified.
- Report counts with uncertainty intervals. When the number of churned accounts is too small for a statistical claim, say so.
- Handle customer data minimally. Use de-identified exports, and quote no individual customer in the report.

With my approval only: I share de-identified exports of billing, subscription, support, and onboarding data for this analysis.
With my approval only: interview or survey churned customers, using a switch-interview guide, to collect new cancellation evidence.
With my approval only: design a measured pilot of the top-ranked fix, for example an onboarding change for a randomized share of new accounts with a held-out control. Name its success metric and run length.

Deliverable: a short written explanation of why customers churned last month. Include the churn definition and counts, the ranked causes with their share and evidence strength, the verdict on the onboarding hypothesis, the recommended next decision, and a list of claims still unverified along with the data that would settle each one.

Judge: an independent reviewer outside the sales team, such as a data analyst or customer-success lead, scores the report against this rubric:
(a) Churn is defined, and its counts reconcile to billing totals for the period.
(b) Every causal claim cites its source and is labeled observed or hypothesized.
(c) Every comparison uses a retained-customer baseline.
(d) The onboarding hypothesis has pre-registered predictions and a verdict.
(e) Involuntary churn is separated out.
(f) Confirmed findings held on the held-out half.
Pass condition: the reviewer can trace every causal claim to cited evidence and finds no claim stronger than its evidence. If the data never arrives, the deliverable passes only as a plan and hypothesis map, and every cause is labeled unverified.
```

- `altitude`: Original outcome: a list of churn reasons. Improved outcome: a ranked, evidence-weighted basis for deciding where to spend retention effort. A pilot of the top fix sits behind approval. No added scope without approval.
- `depth`: Turns sales' belief into pre-registered, falsifiable predictions. This guards against confirmation bias, which matters because the only current input is a prior.
- `depth`: Requires a defined churn metric reconciled to billing, a split between voluntary and involuntary churn, and counts with intervals. Failed-payment churn is often mistaken for dissatisfaction.
- `depth`: Includes a no-data fallback with no fabricated causes, which matches today's actual inputs.
- `depth`: Confirms findings on a held-out half, so patterns found while exploring aren't reported as proven.
- `range`: The epidemiology case-control design exposes base-rate and confounding errors, such as "churners skipped onboarding, but so did retained customers."
- `range`: Reliability-style tenure hazard curves separate early-life churn from later churn, a direct test of the onboarding hypothesis.
- `range`: Analysis of Competing Hypotheses from intelligence analysis acts as the red team. It ranks causes by disconfirming evidence and forces alternatives onto the table.
- `range`: Qualitative coding with a second coder turns free-text reasons into evidence whose reliability can be checked.
- Access and risk effects: sharing data and contacting customers are both gated on approval. Customer contact is outward-facing and carries privacy and relationship risk. The pilot changes the product experience for real accounts.
- Skipped lenses: none.
- Owner actions: confirm the dates of "last month" and the company's churn definition. Find out which de-identified exports you can share, and approve sharing them. Get the sales team's specific claim and account list. Name an independent reviewer. Decide on customer interviews and the pilot.
