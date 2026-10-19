```text
Explain why customers churned last month, and turn that explanation into a ranked, evidence-backed recommendation on where retention effort should go. Treat the sales team's belief that onboarding is the cause as one hypothesis to test, not a conclusion to confirm.

Assumption: the result will be used to decide which retention fix to fund. Onboarding is one candidate; product changes, pricing, sales-to-customer fit, and other causes are others.
Assumption: no target-specific data is available yet. Until data arrives, do not state any cause of last month's churn as a finding. Label everything as a hypothesis, a prediction, or a method.

Hard limits: do not buy data, scrape customer information, or request production credentials. Use only what I supply directly.

Phase 1, which needs no data. Produce a pre-registered diagnosis plan:
- List competing churn hypotheses:
  - H1: onboarding failure
  - H2: involuntary churn, such as failed payments or expired cards
  - H3: price or plan change
  - H4: product gap or reliability problem
  - H5: poor sales fit or overselling
  - H6: contract or renewal timing, or seasonality
  - H7: competitor switch
  - H8: champion or budget loss at the customer
- Use Analysis of Competing Hypotheses, the intelligence-analysis method. For each hypothesis, write the evidence signature that would support it and the signature that would rule it out. Rank evidence by how well it separates hypotheses, not by how well it fits one. Example: onboarding churn should cluster in the first weeks or months after signup and track incomplete activation milestones. Renewal-driven churn should cluster at contract end dates regardless of tenure.
- Specify the analyses, each with what it reveals:
  - Tenure-at-churn distribution and Kaplan-Meier survival curves by signup cohort. These show whether churn is concentrated early in tenure, which fits onboarding, or spread across tenure.
  - A case-control comparison, the epidemiology method: churned accounts against retained accounts from the same cohorts. It tests whether onboarding gaps are actually more common among churners, or equally common among customers who stayed.
  - Separating voluntary churn from involuntary churn before any cause analysis.
  - Comparing last month's churn rate and mix with prior months, to tell a real change from normal variation.
  - Thematic coding of any cancellation reasons or exit-survey text, the qualitative-research method. Two coders work independently, inter-rater agreement is reported, and stated reasons are kept separate from behavioral evidence.
- Write the minimum data request I can fulfill myself without production credentials. Make it a de-identified table, one row per account, covering last month's churned accounts plus a comparison set of retained accounts, with these fields:
  - account ID hash
  - signup date
  - churn date, or none
  - plan and price, and any change to them
  - contract end date
  - onboarding or activation milestones reached, with dates
  - payment-failure flag
  - cancellation reason, if recorded
  - segment or size
  - acquiring sales rep or channel, hashed
  - Mark each field as essential or helpful.
- Pre-register a holdout. Choose a random subset of accounts, or a prior month, that will not be looked at while hypotheses are being shaped.

Phase 2, only once I supply the data. Run the plan:
- Rank the hypotheses by the estimated share of last month's churned accounts each explains, with uncertainty. Report what the evidence rules out as well as what it supports.
- Confirm any hypothesis revised during analysis on the untouched holdout. Leave claims that were not confirmed there marked unverified.
- Red-team the leading conclusion:
  - Run a pre-mortem: "it is three months later and the fix we chose did not reduce churn — why?"
  - Write the strongest case for the best non-onboarding explanation.
- End with a recommendation. State which fix to prioritize, the expected reduction in churn it implies, and the decision risk if the diagnosis is wrong.

With my approval only: use a de-identified export or aggregate report that I provide from the CRM, billing system, or product analytics.
With my approval only: interview customers who churned or are at risk of churning, using switch interviews in the Jobs-to-be-Done style about what pushed them away and what pulled them elsewhere. Contacting customers is outward-facing, and I will approve the recruitment list and the script.
With my approval only: design a measured pilot of the top-ranked fix against a comparison group, to test whether addressing the diagnosed cause actually reduces churn.

First checks:
- Ask me which of these exist and can be shared by me directly, without production credentials:
  - billing or churn reports
  - cancellation reasons or exit surveys
  - onboarding completion records
  - support-ticket summaries
  - the specific reasons the sales team believes onboarding is the cause
- Name each missing dependency. Deliver Phase 1 fully, and run Phase 2 only on what is actually supplied.

Judge:
- Phase 1 passes when an analyst outside sales and outside the onboarding team reviews it with this rubric and confirms all of the following:
  - every hypothesis has both a supporting and a disconfirming evidence signature
  - the data request is fulfillable without production credentials and contains no data that would identify customers
  - the holdout is defined before any analysis
- Phase 2 passes only when all of the following are true:
  - the ranked attribution is reported with uncertainty
  - the leading hypothesis is confirmed on the holdout, or is explicitly reported as unconfirmed
  - the onboarding hypothesis is stated as supported, refuted, or undetermined, with the specific evidence for that verdict
- Without supplied data, the cause of last month's churn remains unverified, and the reply must say so.
```

- `altitude`: The original outcome was an explanation of why customers churned. The improved outcome is a ranked attribution of churn causes plus a funded-fix recommendation stating the decision risk. A pilot of the fix is offered only behind approval. Effect on scope: this adds a recommendation step and an optional pilot.
- `depth`: Instead of asserting a cause, the prompt tests the sales team's onboarding belief directly. It uses tenure-at-churn analysis, Kaplan-Meier cohort survival, separation of voluntary and involuntary churn, and a comparison with prior months, followed by holdout confirmation. Benefit: this prevents a confident but wrong onboarding fix. Cost: it needs a de-identified table that you supply yourself.
- `range`: Three methods come from outside customer analytics:
  - Analysis of Competing Hypotheses, from intelligence analysis, ranks evidence by how well it separates hypotheses.
  - Case-control comparison, from epidemiology, checks whether onboarding gaps also appear in customers who stayed.
  - Double-coded thematic analysis, from qualitative research, keeps stated reasons separate from behavior.
  
  The red-team pre-mortem and the steelmanned non-onboarding case expose the risk of funding the wrong fix. Approval-gated switch interviews add customer contact, which is outward-facing.
- Skipped lenses: none.
- Owner actions:
  - Confirm which reports exist and can be shared without production credentials.
  - Approve and supply the de-identified data table.
  - Arrange an independent reviewer for the Phase 1 rubric.
  - Optionally approve customer interviews and the pilot.
