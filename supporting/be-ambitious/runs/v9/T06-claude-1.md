```text
Tell me why customers churned last month. I have no raw event logs, CRM export, or database access to share right now. All I know is that the sales team thinks onboarding is the cause.
Assumption: the answer exists to decide which retention fix to fund and which team owns it, so it must separate causes that call for different fixes.
Assumption: until account-level evidence is analyzed, every cause, onboarding included, is a hypothesis, not a finding.
Treat "onboarding caused it" as one hypothesis among rivals: poor customer fit at the point of sale, pricing or packaging, missing product value or a product incident, a competitor, involuntary churn from failed payments, contract-renewal timing or seasonality, and no real change (last month within normal variation). Poor fit at sale also produces early churn, so early-tenure churn alone cannot confirm onboarding.
Build an Analysis of Competing Hypotheses (ACH) matrix, a method from intelligence analysis. Rows are evidence items and columns are hypotheses. Mark each cell consistent or inconsistent. Rank hypotheses by how much evidence contradicts them, not by how much supports them. Label every cell observed (with its source) or predicted.
For each hypothesis, write a discriminating prediction and the exact data that would test it:
- Survival analysis by signup cohort (Kaplan-Meier curves and hazard by tenure week) shows whether churn concentrates in the onboarding window.
- A case-control comparison, from epidemiology, of churned against retained accounts from the same cohorts shows whether missed activation milestones predict churn or are just as common among customers who stayed.
- Separating voluntary from involuntary churn removes payment failures from the analysis.
- A control chart of monthly churn against prior months shows whether last month was unusual at all.
- Comparing churned accounts' attributes at sale against the ideal customer profile separates poor fit from poor onboarding.
Write a Jobs-to-be-Done switch-interview guide for churned customers. It asks what they were trying to get done, when they first doubted the product, and what they switched to, and it does not lead them toward onboarding.
Write a premortem: assume an onboarding fix ships and churn does not fall. List the most likely reasons, and name the item in the analysis plan that would have caught each one.
Deliver:
(1) a plain statement of what can and cannot be concluded about last month from what I have supplied;
(2) the hypothesis list and the ACH matrix;
(3) the analysis plan, with predictions written before any data is seen, and a decision rule that maps each outcome to the fix it supports;
(4) the minimum de-identified, account-level data request that would decide between the leading hypotheses;
(5) the interview guide;
(6) the premortem.
Do not buy data, scrape customer information, or request production credentials.
With my approval only: run the pre-written analysis plan on a de-identified, account-level export of last month's churned accounts and comparable retained accounts that I produce and share myself, with no credentials involved, and report each prediction as confirmed, refuted, or untestable.
With my approval only: have my customer success team run the switch-interview guide with churned customers who have agreed to be contacted.
With my approval only: if the approved analysis supports onboarding, run a randomized pilot that gives half of new signups a revised onboarding and compares their early-tenure churn against the other half.
First check: ask me what the sales team's belief rests on (lost deals, customer quotes, timing) and what aggregate figures I can share now without the excluded routes. Treat anything I do not supply as absent, and leave every cause unverified.
First check: for the approved export, confirm that I can produce it de-identified and that our data policy allows sharing it. For the approved interviews, confirm that my customer success team is available and that contacting churned customers fits our consent and privacy policy. For the approved pilot, confirm who owns onboarding changes. If a check fails, continue only with the plan and leave the affected result unverified.
Judge: I (the owner) review the deliverable and pass it only if every hypothesis, including no real change, has a written discriminating prediction and a named data source; every ACH cell and every claim is labeled observed with a source or predicted; no cause is stated as a finding without observed account-level evidence; the predictions and decision rule were written before any data was analyzed; the data request needs no purchase, scraping, or production credentials; and, for any approved analysis, each prediction is reported as confirmed, refuted, or untestable.
```

- `altitude`: the original outcome is an explanation of last month's churn. The improved outcome is a decision rule tied to which fix to fund, plus an approval-gated randomized onboarding pilot that tests the fix directly. The pilot affects real signups and needs a product owner.
- `depth`: the sales team's belief becomes one falsifiable hypothesis. Its rivals include poor fit at sale, which produces the same early-churn pattern, and no real change, checked with a control chart. This prevents funding the wrong team's fix.
- `depth`: the prompt names survival analysis, a voluntary/involuntary split, and a minimum de-identified data request. These lay out the raw-evidence path without any prohibited route.
- `depth`: the analysis on an export you produce yourself is approval-gated. It is new data sharing, and it involves no purchase, scraping, or credentials.
- `range`: the ACH matrix (intelligence analysis) ranks hypotheses by the evidence against them, which counters confirmation of the sales view.
- `range`: the case-control design (epidemiology) compares churned accounts against retained ones. Looking only at churned accounts can't show whether a pattern predicts churn.
- `range`: the Jobs-to-be-Done switch-interview guide (product research) captures customers' own reasons for leaving. Running the interviews is approval-gated because it means contacting customers and must fit consent rules.
- `range`: the premortem (red team) exposes the decision risk of shipping an onboarding fix that doesn't move churn.
- Skipped: no hard target, because the task asks for a diagnosis, not a quantitative improvement.
- Owner actions:
  - Say what the sales team's belief rests on and what aggregates you can share now.
  - Decide on the three approvals: the export analysis, the interviews, and the pilot.
  - Confirm de-identification, your privacy policy, customer success availability, and who owns onboarding.
