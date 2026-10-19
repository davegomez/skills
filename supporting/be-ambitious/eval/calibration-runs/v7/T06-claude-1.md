```text
Goal: explain why customers churned last month well enough to decide where retention effort should go next, and state plainly how much of that explanation the available evidence supports.
Assumption: the result will drive a decision about whether to invest in onboarding or elsewhere, and sales, product, and leadership will discuss it.
Assumption: "churned" means cancelled or did not renew. Confirm the definition before analysis: voluntary vs. involuntary (failed payment), and logo count vs. revenue.

Constraints: Do not buy data, scrape customer information, or request production credentials. I have no raw event logs, CRM export, or database access to share right now.

First, before any analysis:
1. List the evidence you can use without those prohibited steps: anything I supply in this conversation, files in the working directory, and documents I point you to. Examples: a count of churned accounts, cancellation reasons, support-ticket themes, sales or CS notes, billing summaries, and dates of onboarding, pricing, or product changes. Ask me for these by name. Do not ask for credentials.
2. State which questions below that evidence can answer and which it cannot. Continue only with work the available evidence supports. Mark everything else as a proposed test, not a finding.

Work:
- Treat "onboarding caused it" as the sales team's hypothesis, not a finding. Use Analysis of Competing Hypotheses. List onboarding alongside rivals:
  - involuntary churn (failed payments)
  - a pricing or packaging change
  - a product reliability or quality incident
  - a competitor
  - contract-renewal timing or seasonality
  - a shift in which customers were acquired
  - loss of a champion at the account
  For each, write the observable signature that would distinguish it from the others before looking at any data. Rank the hypotheses by how much evidence is inconsistent with each, not by how much fits.
- Onboarding's signature: churn concentrated in early tenure (for example, the first 30–90 days) and in accounts that never reached activation milestones, with churn among long-tenured accounts flat. Churn spread across tenures, or concentrated at renewal dates, points away from onboarding.
- Use outbreak-investigation discipline:
  - a written case definition of a churned account
  - a line list when data allows: one row per churned account, with tenure, plan, segment, acquisition channel, cancellation date, and stated reason
  - a breakdown by time, segment, and tenure, compared against prior months as the baseline
- Once account-level data is available, use survival analysis to test whether churn risk is concentrated where onboarding would put it:
  - Kaplan–Meier curves by signup cohort
  - a Cox model with tenure, plan, segment, and onboarding path as covariates
  - if onboarding changed on a known date, a before/after cohort comparison using difference-in-differences against an unaffected segment
- Treat stated cancellation reasons and sales/CS notes as reports, not causes. Code them with an explicit codebook. Note where sales attribution could be biased, since sales owns the acquisition and onboarding-handoff narratives.
- Red-team the leading explanation: write the strongest case that it is wrong, and say what evidence would settle it.
- Label every claim as observed (cites a specific supplied artifact) or proposed (a hypothesis plus the test that would confirm it). A pattern found while exploring is development evidence. Confirm it on evidence not used to find it, such as a different month or a held-out set of accounts, or leave it unverified.

With my approval only: contact churned customers for consented exit or switch interviews (jobs-to-be-done format), through a channel and script I approve.
With my approval only: run the survival and cohort analysis on de-identified, account-level exports that I or another authorized owner provide. This is not a request for production credentials.

Deliverable: a short memo answering "why did customers churn last month?" It contains:
- the churn definition used
- the ranked hypotheses, each with its distinguishing signature and current verdict (supported / not supported / untested)
- which claims are observed and which are proposed
- a direct assessment of the onboarding hypothesis
- the decision the evidence points to, and what would change it
- the smallest set of data requests, in priority order, that would resolve the remaining uncertainty without any prohibited step

Judge: an analyst or data lead who is neither the author nor on the sales team checks five criteria:
1. Every claim labeled observed cites a supplied artifact.
2. Every hypothesis has a distinguishing prediction written before the evidence was examined.
3. The onboarding verdict follows from that evidence, or is marked untested.
4. No step bought data, scraped customer information, or requested production credentials.
5. Every finding from exploration is confirmed on held-out evidence or marked unverified.
Pass only if every criterion is met. Until account-level data has been analyzed, the cause of last month's churn stays unverified.
```

- `altitude`: The original outcome was an answer to why customers churned. The improved outcome is a decision on where retention effort goes, with stated confidence and the next data requests. This is no new scope. It also avoids presenting an unsupported cause as fact.
- `depth`: The prompt tests the sales team's belief against a tenure-concentration signature it writes in advance. Onboarding becomes falsifiable instead of assumed.
- `depth`: Survival analysis and difference-in-differences replace summary tables once account-level data exists. That data depends on de-identified exports, which require approval and involve data sharing.
- `depth`: Every claim is labeled observed or proposed, and findings must be confirmed on held-out evidence. This prevents a plausible story from passing as a verified finding.
- `range`: Intelligence analysis contributes Analysis of Competing Hypotheses and a red team against the leading explanation. These surface alternatives like involuntary churn or renewal timing that the obvious approach misses.
- `range`: Epidemiology contributes a case definition, a line list, and a comparison with prior months as the baseline. These show whether last month is actually abnormal and which segment is affected.
- `range`: Qualitative research contributes a coding scheme for stated reasons and approval-gated switch interviews. These separate reported reasons from causes. Interviews are outward-facing contact with customers, which raises consent and reputational risk.
- Skipped: none. All three lenses add a distinct, permitted change.
- Owner actions:
  - confirm the churn definition
  - supply whatever permitted artifacts exist (counts, cancellation reasons, ticket themes, change dates)
  - decide on the interview and de-identified-export approvals
  - name an independent reviewer outside the sales team
