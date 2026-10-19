```text
Explain why customers churned last month, in a form that decides where the next retention effort goes, and test the sales team's belief that onboarding is the cause instead of assuming it.

Assumption: the result will be used to choose and fund a retention fix, so for each candidate cause it must state how much of last month's churn it accounts for and what evidence supports it.
Assumption: "last month" means the most recent full calendar month. Confirm this with me before analysis.

Current constraints: I have no raw event logs, CRM export, or database access to share right now. Do not buy data, scrape customer information, or request production credentials.

First checks, before any analysis:
1. List the evidence I can share without new access: cancellation-reason fields or exit surveys, support-ticket summaries, billing or dunning reports, onboarding checklists, account-manager notes, and the sales team's specific claims (which accounts, which onboarding steps).
2. For each source, record what it covers, its time range, and whether it includes retained customers as well as churned ones.
3. Name the missing dependencies. Continue only with work the available evidence supports, and label everything else a proposed finding, not an observed one.

Method:
- Start from per-account timelines rather than summary dashboards: signup date, onboarding milestones reached, usage trend, support contacts, billing events, cancellation date, and stated reason.
- Split churn into involuntary (failed payment, card expiry) and voluntary before attributing any cause. Involuntary churn says nothing about onboarding.
- Check whether last month was unusual. Compare its churn count and rate with the prior 6 to 12 months. If it was not abnormal, say so, and explain baseline churn rather than a spike.
- Treat "onboarding is the cause" as a testable hypothesis and pre-register what would support or refute it before looking at the data:
  - Supports: churn hazard concentrated in early tenure (Kaplan–Meier curves by signup cohort), churned accounts reaching key onboarding milestones at a clearly lower rate than retained accounts from the same cohorts, and stated reasons coded as setup or time-to-value problems.
  - Refutes: churned accounts were long-tenured, completed onboarding at the same rate as retained accounts, or gave reasons such as price, a competitor, budget cuts, a missing feature, or a champion leaving.
- Use case-control logic from epidemiology. Compare churned accounts with retained accounts from the same signup cohorts and segments. A problem that retained customers also had does not explain churn.
- Code stated reasons with a written codebook. Where two people can code, report their agreement (Cohen's kappa) and resolve disagreements before counting.
- Red team with Analysis of Competing Hypotheses (from intelligence analysis). Lay out onboarding, pricing, product gaps, competitor moves, support quality, customer-side events, and involuntary churn as a matrix against each piece of evidence. Rank causes by how little evidence contradicts them, not by how much seems to fit.
- To claim a new pattern, develop it on a random half of churned accounts and confirm it on the held-out half. A pattern seen only in the development half stays unverified.

With my approval only: send a request to the data owner for a de-identified, account-level extract of the fields above for last month's churned accounts and a matched set of retained accounts. This is a request for data, not credentials.
With my approval only: conduct switch interviews (Jobs-to-be-Done) with up to 8 churned customers through existing account contacts, using an interview guide I review first.
With my approval only: design a measured pilot of the top-ranked fix (for example, an onboarding change for one signup cohort against a concurrent control cohort), with its success metric and duration set before launch.

Deliverable: a decision memo containing:
- A ranked list of causes with the estimated share of last month's churn each explains and the evidence behind each estimate.
- An explicit verdict on the onboarding hypothesis: supported, refuted, or unverified, with the reason.
- The recommended next retention action.
- A list of the data still needed to verify each unverified claim.

Judge: the onboarding hypothesis is tested against its pre-registered criteria using churned-versus-retained comparison data. Every cause in the ranking cites observed evidence, or is labeled proposed or unverified. Any new pattern holds on the held-out half.
An independent reviewer outside the sales team (for example, a data analyst or customer-success lead) scores the memo against this rubric:
(a) involuntary churn separated out;
(b) a baseline comparison for last month;
(c) retained-customer comparison present for every causal claim;
(d) competing hypotheses considered;
(e) the recommendation follows from the evidence.
Pass condition: the reviewer marks all five as met. If the comparison data is never provided, the memo passes only as a test plan, and the cause of churn is reported as unverified.
```

- `altitude`: The original outcome was a stated reason for churn. The improved outcome is a ranked, quantified cause list plus a recommended retention action, with an optional measured pilot behind approval. This lets the result drive a funding decision. The pilot adds cost and time.
- `depth`: The prompt tests the sales team's onboarding belief against pre-registered criteria. It does this with per-account timelines, an involuntary/voluntary split, a baseline check, cohort survival curves, and a churned-versus-retained comparison. This prevents confirming a popular story from churned accounts alone. No new access is needed beyond what you choose to share.
- `depth`: Any new pattern must be confirmed on a held-out half of churned accounts, which guards against overfitting a small sample.
- `range`: Case-control comparison (epidemiology) exposes problems shared by retained customers. Codebook coding with kappa (qualitative research) makes stated reasons countable. Both improve rigor at no scope cost.
- `range`, red team: Analysis of Competing Hypotheses (intelligence analysis) forces pricing, competitor, product, support, and customer-side causes to be weighed against onboarding, which reduces the risk of misdirected investment.
- `range`: Jobs-to-be-Done switch interviews reveal causes that CRM fields miss. These involve contacting customers, so they sit behind approval.
- Skipped: none. All three lenses add a distinct, permitted change.
- Owner actions:
  - Confirm what "last month" covers.
  - List the evidence you can share now.
  - Approve or decline the de-identified data request, the customer interviews, and the pilot.
  - Name an independent reviewer outside the sales team.
