```text
Goal: Help leadership make a well-grounded choice between investing in retention and investing in acquisition at the leadership meeting in two weeks. Do this by preparing the required quarterly business review deck, at most 12 slides, built from the raw customer and revenue exports.

Assumption: "leaders" are the executive team, and the choice is about incremental budget for the coming quarter(s). Confirm with me.
Assumption: the 12-slide limit includes any appendix slides.

Requirements (unchanged):
- Deliverable: the quarterly business review deck. It is required, has at most 12 slides, and is for the leadership meeting in two weeks.
- Purpose: leaders decide whether to invest in retention or acquisition. Frame the deck around that choice.
- Use existing staff and tools only.
- Do not change our operating cadence. That means no new recurring meetings, reports, or reviews.
- Do not contact customers. That means no surveys, interviews, or outreach.

First checks, before analysis:
1. I have not yet shared the raw customer and revenue exports. Request them. Until they arrive, prepare only the method and a slide skeleton, and mark every number as pending.
2. When the exports arrive, record their fields, date range, grain (customer, invoice, or month), and row counts. Name any gap that blocks a method below, such as a missing acquisition date, channel, or contract terms.
3. Acquisition cost (sales and marketing spend by period, ideally by channel) is not in the named exports. Check whether it exists in an existing tool or finance report. If it is missing, say on the slides that the acquisition side cannot be measured per dollar. Do not estimate it silently.
4. Get finance's reported revenue for the same periods so the exports can be reconciled against it.
5. Confirm which existing analysis tools are available, such as a spreadsheet, BI tool, SQL, or Python/R. Use only those, and keep customer data inside them.
6. Confirm an independent reviewer from existing staff (see Judge).

Analysis, from raw records rather than summaries:
- Reconciliation: reconcile export revenue to finance-reported revenue for each period. Show any unexplained difference.
- Revenue bridge: split each quarter's change in recurring revenue into new, expansion, contraction, and churn. This tests the belief the decision rests on, which is which lever actually moved revenue, before choosing which one to fund.
- Cohort retention: build retention curves by acquisition cohort, for both customers and revenue, with gross and net revenue retention. Use Kaplan-Meier survival estimates so customers who are still active are counted correctly (censoring). Segment by whatever dimensions the data supports, such as plan, size, or channel, to find where churn concentrates.
- Lifetime value: estimate customer lifetime value as discounted expected margin over the survival curve, by segment. State the discount rate and where the margin figure comes from.
- Acquisition economics (only if spend data exists): CAC and CAC payback by period and by channel, and LTV:CAC.
- Marginal comparison: estimate the revenue gained per additional dollar on each lever.
  - Retention: the revenue saved if churn in the targetable segments falls by plausible amounts.
  - Acquisition: new customers at marginal CAC (not average CAC), multiplied by their lifetime value.
  - Show every assumption.
- Uncertainty: give ranges, not single points. Run a sensitivity (tornado) analysis on the assumptions that drive the comparison. State the break-even condition, that is, what would have to be true for the other option to win.
- Held-out validation: fit the retention and lifetime-value estimates on data through the quarter before last. Use them to predict last quarter's churn and retained revenue, and report the error. Any segment finding discovered on the earlier data must be confirmed on the held-out quarter, or else labeled unconfirmed.
- Red team: before finalizing, do two things.
  - Write the strongest case for the option you are not recommending.
  - Run a pre-mortem: "This recommendation failed a year from now. Why?"
  - Put the risks that survive this on the recommendation slide.
  - Treat correlations as non-causal unless the data supports a causal reading, such as a before/after comparison around a past change.

Deck design (at most 12 slides):
- Open with the decision, the recommendation, and the main reason, in situation, complication, question, answer order.
- Make each slide title a full-sentence claim that the slide's evidence supports.
- Suggested flow, adjusted to stay within 12 slides:
  1. Decision and recommendation
  2. The quarter in brief
  3. Revenue bridge
  4. Cohort retention
  5. Unit economics
  6. Marginal comparison with ranges
  7. Sensitivity and break-even
  8. Risks and the opposing case
  9. Decision requested and the signals to watch
- Keep the choice as framed. If the evidence shows the answer depends on segment, present that as part of the answer to the choice.
- Make every number on the slides traceable to a query or formula over the raw exports in the existing tool. Keep that workbook for the reviewer.

With my approval only: at the next regularly scheduled quarterly review (no new meetings), present actual retention and new-customer results against this deck's projections.
With my approval only: share the analysis workbook with attendees in addition to the deck.

Judge:
- Mechanical checks:
  - The deck has 12 slides or fewer.
  - Export revenue reconciles to finance-reported revenue, or each difference is shown.
  - Every number on the slides traces to the workbook.
  - The held-out backtest error is reported.
- Robustness: the recommendation holds across the backtest error band and the sensitivity ranges. If it flips inside them, the deck says the evidence does not separate the options and names the data that would.
- Independent review: an existing staff member who did not build the analysis (for example, someone from finance or analytics) reads the deck cold and scores it against this rubric:
  1. After a 5-minute read, they can state the recommendation and its main reason.
  2. Every claim's evidence is on the slide or traceable to the workbook.
  3. The opposing case and the key uncertainties are presented fairly.
  4. The decision requested of leaders is explicit.
  - The review passes when all four answers are yes and recorded. Schedule it early enough to allow one revision before the meeting.
  - If no reviewer is available, say so and leave the deck unreviewed.
- Until the review passes and the checks above hold, label the deck as a draft.
```

**Ledger**

- `altitude`: The original outcome was a QBR deck. The improved outcome is a deck built to make one decision, with the recommendation first, ranges, a break-even condition, and the decision requested. Scope is unchanged. It still fits within 12 slides and the existing cadence.
- `altitude` (approval): Present actual results against projections at the next scheduled QBR. This closes the loop on whether the decision worked without adding meetings. It needs your approval.
- `depth`: Working from raw records, reconciling to finance, and using Kaplan-Meier cohort retention and survival-based lifetime value replaces digested summaries with figures that can be checked. Cost is analyst time with existing tools.
- `depth`: The revenue bridge tests the belief the decision rests on, which lever actually moved revenue, before comparing investments.
- `depth`: Held-out validation of the last quarter turns segment findings into confirmed or unconfirmed claims, and it gives the error band the recommendation must survive.
- `range`: Decision analysis contributes marginal-return comparison, tornado sensitivity, and break-even. It shows whether the evidence actually separates the options.
- `range`: Biostatistics contributes survival analysis with censoring and caution about causal claims. It prevents biased churn estimates and overclaiming.
- `range`: Red-teaming contributes the opposing case and a pre-mortem. It exposes decision risks before leaders commit.
- `range`: Executive communication contributes answer-first structure and claim titles. It lets leaders grasp the decision quickly.
- `range` (approval): Sharing the workbook with attendees is new internal data sharing, so it needs your approval.
- Skipped: none. All three lenses fit.
- Owner actions:
  - Share the raw exports.
  - Point to the acquisition spend source, or confirm it doesn't exist.
  - Provide finance-reported revenue for the same periods.
  - Name an independent reviewer from existing staff.
  - Confirm the two assumptions: who the leaders are, and whether the appendix counts toward 12 slides.
  - Decide on the two approval lines.
