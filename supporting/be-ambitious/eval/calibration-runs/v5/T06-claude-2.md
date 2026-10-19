```text
Goal: explain why customers churned last month well enough to decide what to fix first, and test the sales team's belief that onboarding is the cause instead of assuming it.

Assumption: the result will drive a retention decision, such as fixing onboarding versus addressing other drivers, so it must say how confident we can be and what would change the answer.
Assumption: some churn may be involuntary (failed payments, expired cards) and so unrelated to onboarding. Check this, don't presume it.

Constraints (fixed):
- Do not buy data, scrape customer information, or request production credentials.
- I have no raw event logs, CRM export, or database access to share right now. Work only from material I supply in this session.
- "Last month" means last month as I said it. Confirm the exact dates with me before analysis.

First checks, before any claim:
1. List the evidence that would bear on the question, ranked by value: the churned account list with signup and cancel dates, plan, and seat count; the same fields for retained accounts in the same period, since a comparison group is required; onboarding completion records; cancellation reasons and exit-survey text; support tickets; billing and payment-failure records; any product, pricing, or competitor changes near last month.
2. Ask me which items I can supply myself. Mark every other item as missing.
3. If nothing is supplied, do not name a cause. Deliver the hypothesis map, the pre-registered tests, and the minimum evidence request below, and state that the churn cause remains undetermined.

Method:
- Analysis of Competing Hypotheses (from intelligence analysis). List at least 5 rival explanations: onboarding failure, missing product value or fit, price or budget, competitor switch, involuntary or billing churn, support failure, and champion or org change at the customer. Score each piece of evidence for how well it separates the hypotheses, not just whether it is consistent with one. This keeps the sales view from anchoring the analysis.
- Pre-register predictions before looking at any supplied data. If onboarding is the main cause, then:
  (a) churn should concentrate in early tenure, e.g. the first 30–90 days;
  (b) accounts that did not complete onboarding should churn at a higher rate than those that did, against the retained comparison group;
  (c) cancellation reasons and tickets should cite setup, confusion, or time-to-value.
  Write the opposite predictions for each rival hypothesis.
- Survival analysis (from epidemiology and reliability engineering), if dates are supplied:
  - Kaplan–Meier curves by tenure and by onboarding completion show when churn hazard peaks.
  - A Cox model, or a simple stratified comparison if n is small, checks whether the onboarding effect survives controls for plan, size, and signup cohort.
  - Treat involuntary churn as a competing risk, not as onboarding churn.
- Case-control comparison (from epidemiology). Compare churned accounts against retained accounts from the same cohorts. Looking only at churners cannot show a cause.
- Qualitative coding (from social science research). Code any supplied cancellation text and tickets with a codebook written before reading the bulk of it. Report code frequencies with example quotes. Separate stated reasons from behavior-implied reasons.
- Red team. Write the strongest case that onboarding is NOT the main driver, and the strongest case that it is. State which evidence would settle the dispute.
- Development vs. confirmation. Any driver discovered while exploring last month's data counts as development evidence. Confirm it on evidence not used to find it, such as the prior month's churners if I supply them. Otherwise label it unverified.

With my approval only: request exports such as billing, support, or CRM data from other internal teams through normal channels, without production credentials.
With my approval only: draft and run 5–10 short switch interviews with churned customers (jobs-to-be-done "why did you leave" format) to test the top hypotheses. This involves contacting customers.
With my approval only: design a measured pilot, such as an onboarding intervention for one new-signup cohort versus a comparison cohort, with a pre-set retention metric and readout date.

Deliverable: a one-page churn explanation that people can make a decision from. It contains:
- churn split into voluntary and involuntary;
- a ranked list of drivers, each labeled observed, proposed, or unverified, with its evidence and sample size;
- a verdict on the onboarding hypothesis (supported, refuted, or undetermined) tied to the outcomes of predictions a–c;
- the single decision this supports and what evidence would reverse it;
- the minimum evidence request for anything still undetermined.

Judge:
- The pre-registered predictions are written and dated before the data is examined, and each one is reported as held, failed, or untestable with the reason.
- Every causal claim either rests on a churned-vs-retained comparison and is confirmed on held-out evidence, or is labeled unverified.
- An analyst outside the sales team scores the write-up with a rubric covering:
  - Were rival hypotheses tested?
  - Is a comparison group used?
  - Are observed and proposed findings separated?
  - Do the claims match the evidence?

Pass: all predictions reported, no unlabeled causal claims, the onboarding verdict traceable to named evidence, and the reviewer finds no claim stronger than its evidence. If no data is supplied, pass means the hypothesis map, predictions, and evidence request are complete and no cause is asserted.
```

- `altitude`: the original outcome is "a reason customers churned." The improved outcome is a ranked, evidence-labeled explanation tied to the retention decision it drives, plus an optional measured pilot behind approval. A pilot needs approval, a cohort, and time.
- `depth`: the sales belief becomes falsifiable predictions, tested with survival analysis, a churned-vs-retained comparison, and confirmation on held-out data. This guards against confirming a hunch. It depends on data you can supply.
- `depth`: involuntary churn is separated out first. It is cheap, and it often removes a large share that has nothing to do with onboarding.
- `range`: Analysis of Competing Hypotheses from intelligence analysis keeps the sales hypothesis from anchoring the work, and a two-sided red-team exposes the decision risk.
- `range`: qualitative coding with a pre-written codebook, plus switch interviews from JTBD research. The interviews require contacting customers, so they are behind approval.
- Skipped: none. All three lenses fit.
- Owner actions:
  - Confirm last month's exact dates.
  - Say which evidence you can supply yourself.
  - Approve or decline the internal export requests, customer interviews, and pilot.
  - Name a reviewer outside the sales team.
