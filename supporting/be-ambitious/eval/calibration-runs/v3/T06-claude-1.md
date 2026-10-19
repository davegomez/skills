```text
Tell me why customers churned last month, and what I should do about it. I have no raw event logs, CRM export, or database access to share right now. All I know is that the sales team thinks onboarding is the cause. Do not buy data, scrape customer information, or request production credentials.

Goal (assumption: the answer exists to decide which retention fix to fund): produce a ranked set of candidate churn causes, each with the evidence that would confirm or rule it out, and a decision on what to do next under each outcome. Do not present any cause as established. With no data yet, every cause is a hypothesis. Label each statement as "observed" (with its source), "reported" (e.g., the sales team's view), or "hypothesis".

First checks, before any analysis:
- Ask me what "churn" means here: logo or revenue, voluntary cancellation or failed payment/non-renewal. Ask what "last month" covers. Do not assume either.
- Ask me which artifacts I can share later through access I already have. Candidates: an account list with signup date, plan, and churn date; cancellation reasons; support tickets; billing events; onboarding completion flags. Name each missing artifact as a dependency, and continue only with work that does not need it.
- Ask what evidence sales has for the onboarding view: specific accounts, quotes, or a pattern.

Method:
1. Treat "onboarding caused it" as one hypothesis to test, not the answer. Build a hypothesis set using Analysis of Competing Hypotheses (Heuer). Candidates: onboarding failure; poor fit or overselling at the sale; pricing or packaging change; product regression or outage; competitor move; involuntary/billing churn; seasonality or contract-renewal timing; one or a few large accounts dominating the number. Then build a matrix scoring each piece of evidence by how well it tells the hypotheses apart, not by how many hypotheses it fits.
2. For each hypothesis, write its prediction and its kill condition before seeing data. Onboarding predicts three things. Churn concentrates in early-tenure accounts. Accounts that did not complete onboarding churn at a higher rate than comparable accounts that did, at the same tenure and plan. Last month's churners skew toward recent signup cohorts relative to the prior months' baseline.
3. Specify the analysis to run once data exists:
   - Compare churned with retained accounts (case-control). Churners alone cannot show a cause, since retained accounts may share the same onboarding gaps.
   - Use cohort survival curves (Kaplan-Meier) by signup month and onboarding status, so a tenure effect is not misread as an onboarding effect.
   - Split voluntary from involuntary churn.
   - Run a concentration check showing what share of lost revenue the top few accounts represent.
   - Build a reason taxonomy coded from cancellation text and tickets. Two independent coders apply it, and inter-rater agreement is reported.
4. Red team: write the strongest case that onboarding is not the main cause, and name the single observation that would most change the ranking.
5. For each plausible outcome, state the action it implies. Examples: onboarding confirmed means fix the first-30-day path; fit/overselling means change qualification; billing means fix dunning.

With my approval only: send a specific, minimal data request to me or my team for the artifacts named in the first checks, scoped to the fields the tests need, with customer identifiers removed where the test does not need them.
With my approval only: ask the sales team for the accounts and evidence behind their onboarding view.
With my approval only: run consented exit/switch interviews (jobs-to-be-done format) with a small set of churned and retained customers, through channels we already use with them.
With my approval only: set up a recurring monthly churn-reason coding and cohort report.
With my approval only: run a measured pilot of the top intervention against a comparison group before a full rollout.

Judge:
- Now, with no data: a reviewer who did not write the analysis (an analyst or ops lead) checks the output against this rubric. Every claim carries an observed/reported/hypothesis label. Every hypothesis has a prediction, a data source, and a kill condition written before data. The onboarding test compares against retained accounts and controls for tenure. Each outcome maps to an action. Pass means all four hold. Findings about actual causes stay "unverified" until data arrives.
- Once data is shared: hypotheses are kept or killed by their pre-written conditions. Any new cause found while exploring last month's data is confirmed on a period or account set not used to find it, such as the prior month, or is reported as unverified.
- If a pilot is approved: compare churn in the pilot group against the comparison group over a stated window, and report the effect and sample size, met or missed.
```

- `altitude`: the outcome moves from "explain last month's churn" to "decide which retention fix to fund, with a pilot to confirm it." The pilot needs approval.
- `depth`: the sales belief becomes a falsifiable hypothesis with kill conditions written before data. The tests compare against retained accounts with tenure controls (cohort survival curves) and split voluntary from involuntary churn. This guards against reading a pattern into churners alone. No new access is needed.
- `depth`: any new cause must hold on a held-out period or account set. Otherwise it stays unverified.
- `range`: intelligence analysis (Heuer's Analysis of Competing Hypotheses) weighs evidence by how well it separates causes, not by agreement.
- `range`: epidemiology (case-control, confounding by tenure) keeps a tenure effect from being mistaken for an onboarding effect.
- `range`: qualitative research (jobs-to-be-done interviews, dual-coder taxonomy with agreement score) gives reasons beyond what a single coder would read in. Interviews need approval and consent, which means outward contact.
- `range`: a red-team steelman of the "not onboarding" case exposes the risk of funding the wrong fix.
- Skipped: none. Each lens changed the outcome, the method, or the judge.
- Owner actions:
  - Define churn and "last month".
  - Say which artifacts you can share with access you already have.
  - Name an independent reviewer.
  - Approve or decline: the data request, asking sales, customer interviews, recurring reporting, and the pilot.
