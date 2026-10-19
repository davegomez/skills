```text
Goal: Explain why customers churned in September 2026 ("last month" as of 2026-10-18), well enough to choose the next retention action. The sales team believes onboarding is the cause. Treat that belief as one hypothesis to test, not as the answer.

Assumption (inferred, not stated): the result will be used to decide where to invest in retention, so it should rank causes by evidence strength and name the action each cause implies.

Hard limits (unchanged from the owner):
- Do not buy data.
- Do not scrape customer information.
- Do not request production credentials.
- No raw event logs, CRM export, or database access is available now. Do not assume any of them.

Step 0. Check inputs before analyzing anything.
List what the owner can supply without production credentials, and mark each item available or unavailable. Examples: a billing-dashboard summary, cancellation-reason fields or exit-survey text, support-ticket themes, onboarding-completion rates, the sales team's notes on specific lost accounts, a sanitized CSV the owner exports themself. Record whether each item is raw (per-account rows) or digested (a summary or opinion). Ask the owner to confirm that any customer-level data is cleared for this use and stripped of PII they don't want shared. Until real data arrives, label every claim as proposed, not observed.

Step 1. Define churn before counting it.
State the definitions to use:
- Logo churn vs revenue churn.
- Denominator: customers active on 2026-09-01.
- Voluntary vs involuntary churn. Separate failed payments and card expiries first, because onboarding cannot explain them.
- Contract-renewal timing. A spike may just mean many renewals fell due in September.

Step 2. Run competing hypotheses (Analysis of Competing Hypotheses).
Generate at least these rival explanations alongside onboarding:
- Involuntary or payment churn
- Renewal-cohort timing
- Price or packaging change
- A competitor move
- A product gap or reliability incident
- Poor customer fit at sale (mis-sold accounts)
- Champion or budget loss at the customer
For each, write the observable prediction that would distinguish it from the others.
- Onboarding predicts that churn concentrates in early-tenure accounts (for example, under 90 days) and in accounts that never reached activation. It also predicts a dose-response: less onboarding completed means higher churn.
- If most churners are long-tenured and were once active, onboarding is unlikely to be the main cause.
Note that the sales team's view may carry attribution bias, since mis-sold fit is a rival explanation. Test it on evidence, not on who holds it.

Step 3. Use the strongest method the available data supports.
- Only aggregates or opinions available: produce the hypothesis matrix, a pre-registered analysis plan, and a minimal data request. The request should be the smallest owner-exportable fields that would discriminate between hypotheses: tenure at churn, plan, MRR, onboarding milestones reached, last-active date, cancellation reason, and payment-failure flag.
- Per-account data available: estimate churn by tenure cohort with Kaplan-Meier curves. Compare churners against retained accounts from the same signup cohorts (case-control). Fit a Cox or logistic model of onboarding completion against churn, controlling for plan, segment, acquisition channel, and contract term. Report effect sizes with confidence intervals.
- Free-text reasons available (exit surveys, tickets, sales notes): code them into themes with a written codebook. Have a second coding pass check agreement and report Cohen's kappa. Report how often each theme appears, not anecdotes.
Weigh any causal claim against the Bradford Hill criteria: strength, dose-response, temporality, consistency, and plausibility.

Step 4. Prove it on held-out evidence.
Fix the hypotheses and the analysis plan before looking at outcome data. Form findings on one slice of the data, then test them on evidence not used to find them. Either hold out half the September churners at random, or check whether the same pattern explains August 2026 churn.

With owner approval only (outward-facing or added scope):
- Contacting churned customers, for example 5 to 8 "switch" interviews on why they left and what they moved to. Draft the outreach and wait for approval before sending anything.
- Proposing and measuring a pilot intervention, such as an onboarding fix if onboarding is supported, or dunning/payment-retry changes if involuntary churn dominates.

Deliverable: a short decision memo containing:
1. Churn definitions and September 2026 counts, or "unavailable".
2. The hypothesis matrix, with each cause marked supported, refuted, or unverified, plus the evidence and its strength.
3. A verdict on the onboarding hypothesis specifically.
4. The recommended next action and what it depends on.
5. The data request, if evidence was missing.
Keep proposed explanations visibly separate from observed findings.

Judge and pass condition:
- If data was available: every claimed cause cites per-account or coded evidence, and the leading cause holds up on the held-out slice or on August 2026. Report effect sizes, confidence intervals, sample sizes, and kappa for any coding, including results that contradict the onboarding belief.
- If no data was available: the memo passes only if every hypothesis has a falsifiable, distinguishing prediction, and the data request can be fulfilled by the owner without purchased data, scraping, or production credentials. The cause of churn is then reported as UNVERIFIED, not answered.
```

**Ledger**
- `altitude`: The original task, "tell me why customers churned last month," becomes a decision memo that ranks causes and names the retention action each implies. The action is to be confirmed by a pilot, but only with approval. Benefit: the output drives a spending decision instead of confirming a story. Scope effect: interviews and the pilot sit behind approval.
- `depth`: The memo first separates voluntary from involuntary churn and checks renewal timing. It then uses tenure-cohort survival curves, a case-control comparison, and a controlled model on raw per-account rows instead of opinion. Benefit: it tests the onboarding belief directly with a cheap test (the tenure distribution of churners). No access effect, because it only uses data the owner exports.
- `depth`: Hypotheses are fixed before analysis, and findings are validated on held-out churners or on August 2026. Benefit: this guards against fitting a narrative to the same data that produced it.
- `range`: Analysis of Competing Hypotheses, from intelligence analysis, is the red team. It forces rivals to the sales team's view and flags that view's possible attribution bias. Benefit: it exposes the risk of funding the wrong fix.
- `range`: From epidemiology, the case-control design and Bradford Hill criteria separate association from cause.
- `range`: From qualitative research, switch interviews and thematic coding with inter-rater agreement turn exit reasons into measured frequencies. The interviews are outward-facing, so they are gated.
- Skipped lenses: none. All three fit, because the result drives a retention decision, needs rigor, and must persuade a sales team that already holds a view.

**Owner actions**
- Say which non-production exports or summaries you can supply yourself, such as billing summaries, cancellation reasons, or onboarding milestones.
- Clear any customer-level data for this use and remove PII you don't want shared.
- Approve or decline outreach to churned customers.
- Approve or decline a measured pilot.

Until data arrives, this prompt will produce a plan and a data request, not an answer to why customers churned.
