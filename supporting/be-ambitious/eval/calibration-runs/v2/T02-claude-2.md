```text
Prepare the quarterly business review deck for the leadership meeting on or about 2026-11-01. The deck is required and must be at most 12 slides. Its purpose is to help leaders decide whether to invest in retention or acquisition. Build it so that leaders leave with a decision, the evidence for it, and the condition that would reverse it.

Constraints (unchanged from the owner):
- At most 12 slides. The deck is required.
- Use existing staff and tools only.
- Do not change the operating cadence. Add no new recurring meetings, reports, or processes.
- Do not contact customers. That rules out surveys, interviews, and outreach. Do not run any intervention.

Assumptions (inferred, not confirmed by the owner):
- A1: Leaders want a recommendation with a stated confidence level, not just a description of the quarter.
- A2: "Retention vs. acquisition" assumes the two are separable substitutes. The deck should test this assumption rather than adopt it.
- A3: The meeting has a fixed time slot. Assume about 30 minutes unless told otherwise.

STEP 0: Check dependencies before any analysis.
1. Confirm receipt of the raw customer export and the raw revenue export. For each, record the row count, date range, fields, and customer ID join key. Stop and report if either is missing.
2. Check whether the exports contain acquisition spend or CAC by channel. If they do not, the acquisition side cannot be costed. Ask the owner for spend data from an existing source. Additional data sources need owner approval. Until then, label every acquisition economics figure "unverified".
3. Customer data may contain personal information. Before analysis, confirm with the owner how it may be handled. Work only in existing approved tools. Aggregate before anything goes on a slide. Send no raw data to external services.
4. Get finance's reported quarterly revenue figures for reconciliation. Ask the owner for one existing staff member (for example, a finance or analytics lead) to act as the independent reviewer around 2026-10-28.

STEP 1: Analyze from raw data, not summaries.
- Reconcile export revenue to finance's reported figures within 0.5%. Explain any gap before going further.
- Growth accounting: break quarterly revenue into new, expansion, contraction, and churn, so that each lever's contribution is visible.
- Cohort analysis: build retention triangles by acquisition quarter (actuarial run-off style) and net and gross revenue retention by cohort. Use Kaplan-Meier survival curves, cut by segment and acquisition channel. Where tenure data supports it, use a Cox model to show which factors move churn hazard.
- Unit economics: LTV, CAC, and payback by channel and segment, using marginal rather than average CAC where spend data allows. Use the marginal figures because the decision concerns the next dollar, not the average one.
- Test A2 directly. Check whether churn concentrates in customers from specific channels or segments. If it does, acquisition quality drives retention, and the real decision may be "acquire differently". Show the evidence either way.
- New-finding discipline: identify churn or expansion drivers using cohorts up to the prior quarter. Then confirm them on the most recent quarter, which was held out. Call a driver an observed finding only if it holds on the held-out data. Otherwise label it a hypothesis.

STEP 2: Frame the decision (decision analysis).
- Define options as discrete investment levels for retention, acquisition, and any mix the data suggests. Do not leave it as an abstract either/or.
- For each option, estimate expected revenue impact with ranges, based on the cohort and unit-economics models.
- Run a sensitivity (tornado) analysis to find the two or three assumptions that most change the answer. State the threshold value at which the recommendation flips.
- Apply value-of-information reasoning: name what further evidence would most reduce uncertainty. Leaders may choose to gather that evidence later. Any such test would be a proposal for leaders to decide on, and it must respect the no-customer-contact and cadence constraints. It is not to be run.

STEP 3: Red-team the recommendation.
- Analysis of Competing Hypotheses: list rival explanations for the main pattern (for example, seasonality, pricing changes, a single large account, mix shift) and record which evidence rules each in or out.
- Check for Simpson's paradox (the pooled trend reversing within segments) and survivorship bias (older cohorts looking healthier only because churned customers dropped out).
- Pre-mortem: assume the recommended investment failed a year from now. Write the most likely reasons. Each reason must either be addressed in the deck or named as a key risk.
- Write the strongest one-slide case for the option not recommended. Keep it in the working notes so the presenter can answer it.

STEP 4: Build the deck (at most 12 slides).
- Pyramid structure: slide 1 states the decision being asked for, the recommendation, confidence, and the flip condition.
- Suggested flow:
  1. Decision and recommendation
  2. Quarter at a glance (growth accounting)
  3–4. Retention evidence (cohorts and survival)
  5–6. Acquisition evidence (unit economics by channel)
  7. Test of whether retention and acquisition are independent
  8. Options with expected impact
  9. Sensitivity and flip point
  10. Risks and rival explanations
  11. Proposed next evidence
  12. The ask
- Every chart must state its takeaway in the title. Use small multiples for cohort comparisons. Each number must be labeled "observed", "modeled", or "unverified".
- Supporting analysis stays in working files. A backup document beyond the 12 slides may be created only with owner approval.

JUDGE: all of the following must pass.
1. Reconciliation: export revenue matches finance's reported figures within 0.5%, or the gap is explained and shown.
2. Back-test: models fit on earlier quarters predict the most recent quarter's churned revenue and new revenue. Report the error for each, even if it is large. A model with error above 15% may appear only as directional and must be labeled that way.
3. Held-out confirmation: every driver presented as a finding holds on the held-out quarter. Drivers that do not hold are labeled hypotheses.
4. Independent review: the owner-assigned reviewer reads the deck cold. From slide 1 alone, they should be able to state the decision, the recommendation, and the flip condition. They then score the deck against this rubric: each claim has visible evidence; observed vs. modeled is clear; constraints are respected; at most 12 slides. Record their findings and how each was resolved.

Pass condition: the deck has at most 12 slides, judge checks 1 to 4 are reported with their results, and no constraint has been violated. If spend data or reviewer access never arrives, report the affected checks as unverified. Do not claim they passed.
```

**Ledger**
- `altitude`: the task moves from "prepare the QBR deck" to "get leaders to a decision with an explicit flip condition". The benefit is a meeting that ends in a decision rather than a status review. Scope stays at 12 slides and adds no cadence change.
- `depth`: the work starts from raw exports, reconciled to finance figures, rather than digested summaries. This catches data errors before they reach leaders.
- `depth`: growth accounting, cohort triangles, Kaplan-Meier and Cox models, and marginal LTV/CAC show how each lever works, not just totals. This needs spend data, which may be a new source requiring approval.
- `depth`: the deck tests the retention-vs-acquisition framing (A2) itself. If channel quality drives churn, it may reveal a better third option.
- `depth`: findings must be confirmed on a held-out quarter, which separates observed findings from hypotheses.
- `range`: decision analysis (options, tornado chart, flip point, value of information) shows leaders which assumption to argue about.
- `range`: intelligence analysis (competing hypotheses) and a red team (Simpson's paradox and survivorship checks, a pre-mortem, a steelman of the other option) test the main claim before leaders see it.
- `range`: Pyramid Principle and Tufte-style small multiples make the story readable in about 30 minutes.
- Skipped lenses: none. All three fit, because this deck drives a high-stakes investment decision and must persuade busy leaders.

**Owner actions**
- Share both raw exports and confirm how customer personal data may be handled and in which tools.
- Provide or approve a source for acquisition spend by channel. Without it, acquisition economics stay unverified.
- Provide finance's reported quarterly revenue for reconciliation.
- Assign an existing staff reviewer around 2026-10-28 and confirm the meeting's length.
- Decide whether to allow a backup document beyond the 12 slides.
