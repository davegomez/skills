```text
Goal: Explain why customers churned last month well enough to decide which retention fix to fund first. The sales team believes onboarding is the cause. Treat that belief as one hypothesis to test, not as the answer.

Assumption (inferred, unconfirmed): the owner wants to choose and fund a retention intervention. A list of reasons alone is not the goal.

Constraints (all preserved):
- No raw event logs, CRM export, or database access is available right now.
- Do not buy data.
- Do not scrape customer information.
- Do not request production credentials.
- Keep "last month" as the period. Do not substitute dates.

Current evidence: the only evidence is the sales team's belief. Say so plainly. Name no cause as established until data tests it.

Part A: deliverable now, without data

1. Churn taxonomy. Split churn into types before explaining it, because each type has different causes and fixes:
   - Involuntary: failed payments, expired cards.
   - Contract-end non-renewal.
   - Active cancellation.
   - Downgrade.
   - Account consolidation or acquisition.
   Many churn reports miss involuntary churn. Size each type first.

2. Competing-hypotheses register. Use Analysis of Competing Hypotheses (Heuer), a method from intelligence analysis. List at least six rival explanations alongside onboarding:
   - Onboarding
   - Pricing or renewal shock
   - Product gaps or reliability incidents
   - Competitor switch
   - Champion turnover at the customer
   - Poor-fit customers sold into the product
   - Payment failure
   - Seasonality or contract-cycle timing
   For each, give its predicted signature in the data and the evidence that would rule it out. Rank hypotheses by how much evidence contradicts them, not by how much supports them.

3. Falsifiable predictions for the onboarding hypothesis, written before any data is seen. Sales has an incentive to locate churn after the sale, so these predictions matter:
   a. Churn concentrates in early tenure, within the onboarding window.
   b. Churned accounts show worse onboarding completion or longer time-to-first-value than retained accounts from the same signup cohorts.
   c. Exit reasons and support tickets cite setup or adoption problems more often than the base rate.
   d. Accounts that completed onboarding churn at a lower rate.
   If churners were mostly long-tenured, or if they onboarded as well as retained accounts, onboarding is unlikely to be the main cause.

4. Analysis plan, for each data type:
   - Case-control comparison from epidemiology: churned accounts as cases, retained accounts from matched cohorts as controls. This guards against the error of describing churners without comparing them to anyone.
   - Kaplan–Meier survival curves split by onboarding completion, to show whether onboarding status changes the shape of retention over tenure.
   - Cox proportional-hazards model with segment, plan, tenure, and onboarding variables, to separate onboarding from confounders such as customer size.
   - Jobs-to-be-Done switch interviews with forces-of-progress coding, to reach the reasons customers give in their own words.
   - Exit-reason coding by two independent coders, with inter-rater agreement (Cohen's kappa) reported.
   - Hold-out discipline: develop explanations on half of the churned accounts, confirm them on the other half. Claims shaped by the development half stay unverified until they hold on the held-out half.

5. Minimum data specification. List the smallest pseudonymized, aggregate-friendly fields each analysis needs, so no raw PII is required:
   - Account ID hash
   - Signup and churn dates
   - Plan and MRR band
   - Churn type
   - Onboarding milestones and dates
   - Coded exit reason
   - Support ticket counts by category

6. Red team:
   - Pre-mortem: assume the team funds an onboarding fix and churn does not move. Write the most likely reasons why.
   - Steelman the strongest rival hypothesis.
   - Flag the decision risk if the onboarding belief goes untested.

Part B: run only when approved data arrives

7. Run the pre-stated predictions and report each one as pass, fail, or untestable, with its numbers.
8. Run the case-control comparison, survival analysis, and hazard model.
9. Rank causes by estimated share of last month's churned accounts and of churned MRR. Give confidence ranges.
10. Recommend the first intervention, with the expected effect size and how to measure it.

With my approval only: analyze internal artifacts I later choose to share, such as a pseudonymized churn list, billing or payment-failure records, onboarding milestone data, exit surveys, support tickets, or CS notes.
With my approval only: interview sales and CS staff, asking for specific churned-account examples rather than general impressions.
With my approval only: contact churned customers for switch interviews or exit surveys. This is outward-facing, so I approve the wording, list, and consent before any contact.
With my approval only: run the recommended intervention as a measured pilot against a holdout group, with a pre-stated success metric and duration.

First checks:
- Confirm which internal artifacts exist and who owns them. Exit surveys, cancellation-reason fields, payment-failure reports, and support ticket categories may exist even without CRM or database access.
- Confirm the churn definition and the count of churned accounts for last month, if the owner can state them.
- Name each missing dependency. Deliver Part A in full now. Mark every Part B result as pending data, not as a finding.

Judge:
- Part A passes when an independent reviewer outside sales (for example finance, CS, or data) confirms against a rubric that:
  (1) every claim is labeled as observed evidence or hypothesis;
  (2) the onboarding hypothesis has at least four falsifiable predictions written before data;
  (3) at least six rival hypotheses each have a disconfirming test;
  (4) the analysis plan uses comparison groups, not churners alone;
  (5) the data spec needs no production credentials, purchased data, or scraped customer information.
- Part B passes when each pre-stated prediction is reported as pass, fail, or untestable with its numbers, and when every causal claim holds on the held-out half of churned accounts.
- Until Part B runs, the cause of last month's churn stays unverified, including onboarding.
```

**Ledger**

- `altitude`: Moves the outcome from "a stated reason for churn" to "a ranked, evidence-tested cause that decides which retention fix to fund." An approval-gated holdout pilot measures the fix. Pilots and interviews cost time; nothing runs without approval.
- `depth`: Tests the sales team's belief against falsifiable predictions written before data, instead of accepting it. This reduces the risk of funding the wrong fix. No new access is needed for Part A.
- `depth`: Adds a churn-type taxonomy that sizes involuntary and payment-failure churn first. This catches a frequently missed cause with a cheap fix.
- `depth`: Adds a case-control comparison, Kaplan–Meier curves, a Cox hazard model, and development and held-out halves of churned accounts. These replace a description of churners with comparisons against retained customers that can show cause. They require data you approve sharing later.
- `depth`: Adds a minimum pseudonymized data spec. It keeps analysis inside your no-scrape, no-credentials, no-purchase limits and reduces PII exposure.
- `range`: Analysis of Competing Hypotheses, from intelligence analysis, ranks rivals by disconfirming evidence. This counters anchoring on the belief sales already holds.
- `range`: Epidemiology's case-control design and survival analysis expose the base-rate error of studying churners without a comparison group.
- `range`: JTBD switch interviews and double-coded exit reasons with Cohen's kappa surface reasons that don't appear in internal data. Customer contact is outward-facing and gated behind approval.
- `range`: A red-team pre-mortem and steelman of the strongest rival hypothesis expose the decision risk of acting on an untested belief.
- Skipped lenses: none. All three lenses add a method or check the original task lacked.
- Unresolved owner actions:
  - Confirm which internal artifacts exist (exit surveys, payment-failure reports, ticket categories) and whether you'll share pseudonymized versions.
  - Confirm last month's churn definition and count.
  - Name an independent reviewer outside sales.
  - Decide on staff interviews, customer outreach, and an intervention pilot.
