```text
Prepare the quarterly business review deck for our leadership meeting in two weeks. Build it so leaders can make one decision in the meeting: whether to invest in retention or acquisition. Lead with a recommendation, then show the evidence, the size of each option, and what would change the answer. The deck is required and must be at most 12 slides, including any appendix or backup slides. Use existing staff and tools. Do not change our operating cadence. Do not contact customers.

Assumptions to confirm with me, not facts: (a) the decision is about where the next increment of spend or effort goes, not all-or-nothing; (b) the business model (recurring subscription vs. repeat purchase) determines the methods below; (c) leaders will have roughly one meeting slot to decide.

First checks, before any analysis:
1. Confirm you have received the raw customer and revenue exports. Until they arrive, prepare only the analysis plan and the slide skeleton, with no numbers.
2. Profile the exports. Confirm customer ID, start and end or cancel dates, revenue by period, plan or segment, and acquisition date and channel if present. Count how many quarters of history exist. Report missing fields, duplicates, and totals that do not reconcile.
3. Check whether acquisition cost or spend data exists in these exports. If it does not, the acquisition side cannot be costed. State that on the relevant slide rather than estimating CAC from assumptions presented as data.
4. Confirm which analysis tools existing staff already use, and run all work in those tools.
Name each missing dependency and continue only with work the available data supports.

Method:
- Start from raw rows, not dashboard summaries. Rebuild the quarter's revenue movement from customer-level records.
  - If revenue is recurring: run growth accounting. Split period-over-period change into new, expansion, contraction, churned, and reactivated revenue. Compute gross and net revenue retention.
  - If revenue is repeat-purchase: use a buy-till-you-die model (BG/NBD with Gamma-Gamma) to estimate expected future value per customer.
- Build cohort retention curves by acquisition quarter, segment, and channel. Use survival analysis: Kaplan-Meier curves so recent, still-active customers count as censored rather than retained or churned. Use a Cox model only if enough history exists to test which segments churn faster.
- Separate churn that a retention investment could plausibly address from churn it could not, using only fields in the exports (for example payment failure vs. cancellation, if recorded). Do not infer customer intent.
- Test the belief the decision rests on, that retention and acquisition are separate levers. Check whether churn is concentrated in customers from particular channels or segments. If so, part of the "retention problem" is an acquisition-quality problem, and the deck should say so.
- Size both options in the same unit, for example revenue impact over the next four quarters:
  - Retention: what a 1-point change in gross retention is worth.
  - Acquisition: what N additional customers of the current cohort quality are worth.
  - Include the cost side only where cost data exists.
- Decision analysis:
  - Compute the expected value of each option.
  - Add a tornado chart showing which input most moves the comparison.
  - Find the break-even value at which the recommendation flips.
  - Name the one uncertainty most worth resolving. This is the value of information.
- Avoid causal overreach. Correlations from historical data (for example "customers on plan X retain better") are labeled associations, not effects. Do not propose experiments that require contacting customers.
- Red team:
  - Run a pre-mortem: assume we chose the recommended option and it failed a year later, then list why.
  - Give the losing option its strongest case on one slide.
  - Run Analysis of Competing Hypotheses on the main explanation for churn. List the rival explanations and the evidence for and against each.
- Hold out the most recent complete quarter. Find patterns and fit models on earlier quarters. Then confirm any headline claim (for example "channel A cohorts churn 2x faster") on the held-out quarter. A claim that does not hold there is shown as unconfirmed or dropped.
- Slide craft:
  - Answer first, using the pyramid principle.
  - Each slide headline is a full-sentence assertion, and the body is the evidence for it.
  - Suggested arc within 12 slides: decision and recommendation; where the quarter's revenue change came from; retention curves; acquisition cohort quality; option sizing in one unit; sensitivity and break-even; the losing option's best case and the pre-mortem; what would change our mind and the leading indicators to watch within the existing cadence; the ask.
- Keep methods detail, the reconciliation log, and the holdout results in a separate working file, not in the deck, so the deck stays within 12 slides.

With my approval only: request additional data beyond the two exports, such as marketing spend, support tickets, or product usage.
With my approval only: share the exports with any person or tool that does not already have access to them.
With my approval only: ask a named staff member who did not build the deck to serve as independent reviewer.
With my approval only: build a refreshable retention and acquisition metrics view in existing tools that continues after this meeting.

Judge and pass condition:
1. Reconciliation (mechanical). Recompute every number on every slide from the raw exports with a script or workbook. Pass: every figure ties to the exports exactly, or with a documented adjustment, and quarterly revenue totals match the export totals.
2. Holdout (mechanical). Report the error of the retention model fit on earlier quarters when it predicts the held-out quarter. Report each headline claim as confirmed, unconfirmed, or dropped on that quarter.
3. Independent review (qualitative). A reviewer who did not build the deck scores it against this rubric:
   - Numbers trace to the reconciliation.
   - The recommendation is stated on slide 1.
   - Both options are sized in the same unit.
   - The break-even and the "what would change our mind" condition are explicit.
   - Associations are not presented as causes.
   The reviewer then reads the deck cold for ten minutes and states the recommendation, the main driver, and the flip condition. Pass: all rubric items are met, and the reviewer's three statements match the deck's.
   Until a reviewer is approved and has run this review, report the review as unverified.
4. Constraints. The deck has 12 or fewer slides including any appendix. No customer was contacted. The operating cadence is unchanged.
Report all four results in the working file, each as passed, failed, or unverified.
```

**Ledger**

- `altitude`: The original outcome is a QBR deck covering the quarter. The improved outcome is a decision instrument: a recommendation, both options sized in one unit, a break-even, and a "what would change our mind" condition, so leaders can decide in the meeting. The scope stays a single deck of at most 12 slides. A recurring metrics view is the next rung up, and it sits behind approval as a new recurring workflow.
- `depth`: The analysis starts from customer-level raw rows using growth accounting or BG/NBD, cohort curves, and Kaplan-Meier, instead of summary tables. This prevents recent cohorts from making churn look biased, and it shows which revenue component actually moved.
- `depth`: The prompt tests the either/or premise by checking whether churn concentrates by acquisition channel. If it does, the real lever may be acquisition quality, which reframes the decision. This uses only the existing exports.
- `depth`: Headline claims are confirmed on a held-out quarter. This separates real patterns from ones found by searching the data. It needs enough quarters of history, which is checked first.
- `range`: Decision analysis (expected value, tornado chart, break-even, value of information) shows which single uncertainty decides the question.
- `range`: Red teaming (pre-mortem, steelman of the losing option, Analysis of Competing Hypotheses on the churn explanation) exposes decision risk before leaders commit. It costs one slide.
- `range`: Epidemiology's discipline on confounding labels historical correlations as associations. This avoids recommending a fix based on a non-causal pattern, and it respects the no-customer-contact rule.
- `range`: Communication craft (pyramid principle, assertion-evidence headlines) makes the story readable in one meeting, within 12 slides.
- `judge`: Four checks: reconciliation, holdout error, independent review with a rubric and cold read, and the constraints. Results go in a separate working file because the deck has no room for them. The independent review stays unverified until a reviewer is approved.
- **Skipped:** No hard numeric stretch target. The deliverable is a decision, and the deck has no room to report a stretch metric.
- **Owner actions:**
  - Share the exports.
  - Confirm assumptions (a) to (c), especially the business model.
  - Say whether acquisition spend data exists.
  - Approve or decline the four approval lines, in particular naming an independent reviewer.
