The task has three gaps. It has no data, it rests on an untested belief (onboarding), and it has no definition of churn. The rewrite doesn't pretend to answer "why" without evidence. Instead, it turns the sales team's belief into tests that can prove it wrong, works out what evidence each cause would leave behind, and blocks any finding until that evidence exists.

```text
Goal: explain why customers churned in September 2026 well enough to decide which retention fix to fund first. (Assumption: "last month" means September 2026. Confirm with me before relying on it.) The sales team believes onboarding is the cause. Treat that as one hypothesis to test, not as the answer.

Hard constraints. Do not break these for any reason:
- Do not buy data, scrape customer information, or request production credentials.
- I currently have no raw event logs, CRM export, or database access to share. Do not assume any exists.
- Do not contact customers, sales, or anyone outside this conversation without my explicit approval.

Step 1: Check what evidence is available. Do this before any analysis.
Ask me which of these I can provide myself, de-identified (customer IDs hashed or removed, no names, emails, or contact details):
- billing or subscription records with start date, cancel date, plan, and MRR
- cancellation reasons or exit-survey answers
- support ticket counts or categories
- onboarding completion flags
- payment-failure records
Use only what I hand over. Write an evidence register. For each item, record what it is, where it came from, its date range, its row count, and its known gaps.
If I provide nothing, say so plainly and go to Step 2 only. In that case, every output below is a proposal or a plan, not a finding.

Step 2: Define churn and list competing hypotheses.
- Pin down the definition: logo churn vs. revenue churn, and voluntary cancellation vs. involuntary loss from failed payments. Propose a definition and ask me to confirm it.
- List at least 5 competing explanations. Onboarding is one. Others: involuntary payment failure, price or plan change, product gap or reliability, a competitor, seasonality or contract-renewal timing, and a single large account or segment skewing the count.
- Build an Analysis of Competing Hypotheses matrix. For each hypothesis, state:
  - the evidence that would discriminate it from the others
  - the data source for that evidence
  - the test you would run
  - the result that would falsify it
- For onboarding specifically, write these tests down before seeing any data:
  (a) Tenure. Onboarding-driven churn should cluster in early-tenure customers. Plot churned customers by tenure and compare the hazard in the first 90 days against later tenure.
  (b) Case-control comparison. Compare churn rates for customers who completed onboarding vs. those who didn't. Stratify by plan, segment, and signup cohort so a confounder doesn't produce the gap.
  (c) Stated reasons. Code the cancellation and exit-survey text with a codebook written before you read the responses. Report what share mentions setup or getting started.

Step 3: Analyze. Only run this step on data I have provided.
- Run the tests you pre-registered in Step 2. Use survival analysis (Kaplan-Meier curves by onboarding status, then a Cox model or a stratified rate comparison) wherever the data allows.
- Size each cause by its share of churned MRR as well as churned logos.
- Hold-out check: develop the explanation on September, then test whether it predicts churn in a month you did not use, such as August or July. If no prior month is available, say the result is unconfirmed out of sample.
- Red-team the leading explanation. Write the strongest case against it, and check whether one account, one plan, or a definitional choice is driving it.

Step 4: Deliverable.
A short decision memo for leadership and the sales team that someone can read in about 10 minutes. It contains:
- the September churn count and MRR under the confirmed definition
- each hypothesis marked supported, refuted, or untested, with the evidence behind each verdict
- an estimated share of churn per cause, with uncertainty
- a recommendation on which fix to fund first
Keep observed evidence and proposed explanations visibly separate.
If the onboarding belief fails, say so directly and show the test that refuted it.

With my approval only:
(i) Draft a consented exit-interview guide for a small number of churned customers. I or my team would run the interviews; you would not contact anyone.
(ii) Propose an ongoing churn-reason instrument, such as a required cancellation reason and early-warning signals like a stalled onboarding step or failed payments, so next month's question can be answered in days.

Judge:
- Pass condition with data: every pre-registered test has been run and reported as written, including any that contradict the sales team's view. The leading explanation is checked against a held-out month and the result is reported, hit or miss.
- Pass condition without data: every hypothesis in the matrix has a named data source, a test, and a falsification threshold. A reviewer I choose (for example, someone in finance or customer success) can tell from the memo exactly what data to pull and what result would change the decision.
- Any finding not backed by a register entry is labeled unverified.
```

**Ledger**

- `altitude`: The original task is "tell me why customers churned last month." The chosen outcome is deciding which retention fix to fund first, with causes sized by churned MRR. That gives the analysis a decision to serve. No added access is needed.
- `altitude`: The ongoing churn-reason instrument is approval-gated. It would make future churn questions answerable quickly. It adds scope beyond the original question.
- `depth`: An evidence-availability check comes first, along with an evidence register. This prevents the model from inventing a causal story when no data exists. No access is requested.
- `depth`: The churn definition must be confirmed, with voluntary churn split from involuntary. Payment failure is a common non-onboarding cause that a vague definition hides.
- `depth`: The onboarding belief is tested with falsification thresholds written in advance. The tests are tenure clustering, a stratified case-control comparison, and coded stated reasons. This tests the premise directly instead of confirming it.
- `depth`: The analysis uses survival analysis plus a held-out month as the judge. This separates a real pattern from a September coincidence. It needs a second month of data from you.
- `range`: Analysis of Competing Hypotheses, borrowed from intelligence analysis, makes all the alternative causes compete on discriminating evidence.
- `range`: Case-control comparison and stratification for confounders, borrowed from epidemiology, stop plan or cohort mix from masquerading as an onboarding effect.
- `range`: A codebook written before reading responses, borrowed from qualitative research, keeps the coding of stated reasons from being bent toward the expected answer.
- `range`: A red-team pass on the leading explanation exposes the risk of a single account or a definitional choice driving the conclusion.
- Skipped: none. Altitude fits because this result drives a funding decision. Depth fits because the premise is untested. Range fits because the conclusion has to land with a sales team holding a prior belief.
- **Owner actions:**
  - Confirm that "last month" means September 2026 and confirm the churn definition.
  - Decide which data, if any, you can provide yourself, de-identified, and get clearance for sharing it.
  - Name the reviewer.
  - Approve or decline the exit-interview guide and the ongoing instrument.
