```text
Goal: prepare the quarterly business review deck for our leadership meeting in two weeks, built so leaders can decide whether to invest in retention or acquisition. Assumption (inferred, confirm with me): the decision is about where the next marginal dollar or headcount earns the most durable revenue, and the deck should make that comparison explicit rather than only report the quarter.

Fixed requirements:
- The deck is required and must be at most 12 slides, appendix included. Anything that does not fit goes in a separate analysis workbook, not in extra slides.
- Use existing staff and tools only.
- Do not change our operating cadence. Do not contact customers.
- Source data: the raw customer and revenue exports I will provide.

First checks, before any analysis:
1. Confirm you have received the customer and revenue exports. Until they arrive, draft only the deck skeleton and the analysis plan, and label every number as pending.
2. Inventory each export: date range, grain (customer, invoice, or subscription line), fields, and how customers join to revenue. You need at least 4 quarters of history for cohort curves and one held-out quarter (see Method 5). Report what the history supports.
3. Check whether the exports include acquisition cost: sales and marketing spend, by period and ideally by channel. Without it, retention and acquisition cannot be compared per dollar. If it is missing, ask me for it. Until it arrives, mark every acquisition-return figure as unverified and do not present a recommendation that depends on it as settled.
4. Reconcile the export revenue totals for the quarter against the figure leadership already treats as reported revenue. I will tell you that figure or where it lives. Explain any gap before using the data.

Method:
1. Revenue waterfall from the raw rows, not from summaries: starting revenue, new, expansion, contraction, and churn for each quarter. Compute gross revenue retention, net revenue retention, and logo churn. Keep the calculations in a reproducible script or workbook so every deck number traces back to an export row.
2. Cohort and survival analysis. Build acquisition cohorts by quarter and plot revenue-retention curves. Use Kaplan–Meier survival to handle customers too new to have churned yet (censored customers), so recent cohorts are not overstated.
3. Unit economics. Calculate customer lifetime value from the observed retention curves, discounted at a rate I approve. Calculate CAC and CAC payback from the spend data. Express both levers in one unit: expected revenue (or gross margin) per extra dollar spent on retention versus on acquisition.
4. Test the either/or framing from raw evidence. Break each metric down by segment (for example plan, size, channel, or region, whichever the exports support). Check whether the better lever differs by segment. If it does, the recommendation may be a split rather than a single choice. Keep correlation separate from causation. The exports show which customers retained, not what an intervention would change. State the size of any assumed retention-program effect as an assumption and show its range.
5. Held-out confirmation. Find segment patterns and churn signals on all quarters except the most recent complete one. Then test whether they hold on that held-out quarter. Report each finding as "confirmed on held-out data", "not confirmed", or "unverified (insufficient history)".
6. Decision analysis. Calculate expected value for retention-heavy, acquisition-heavy, and split allocations. Add a tornado sensitivity chart showing which assumption (churn reduction achievable, CAC, discount rate, expansion rate) would flip the answer. Add a value-of-information note on which missing number is most worth getting before committing.
7. Narrative. Lead with the answer (pyramid principle): the recommendation and its conditions on slide 1 or 2. Then show the evidence behind it, then the risks. Include one slide proposing how the chosen investment will be measured using existing reports at the existing cadence.
8. Red team. Write the strongest case for the opposite recommendation from the same data, and run a pre-mortem ("it's a year later and this choice failed; why?"). Put the surviving objections on the risks slide.

With my approval only: share the exports and draft deck with a finance reviewer and a red-team colleague from existing staff, whom I will name.
With my approval only: pull data beyond the two exports, such as spend by channel or support or usage data, from systems you do not already have access to.

Judge:
- Mechanical checks, run by you and reported in the workbook:
  - Export revenue reconciles to the reported quarter figure, or any gap is explained.
  - The waterfall components sum to the change in revenue for every quarter.
  - Every deck number regenerates from the script.
  - Held-out results are stated for each finding.
  - The deck has 12 slides or fewer.
- Qualitative check, by the named finance reviewer (pending my approval). The reviewer applies this rubric:
  - Does the recommendation follow from the numbers?
  - Are the assumptions stated, with their ranges?
  - Is causation overclaimed anywhere?
  - Would the red-team case change the answer?
- Pass condition: a deck of 12 slides or fewer, ready before the leadership meeting, containing a recommendation, its supporting evidence, and its risks. Every number must reconcile and trace to the exports. Acquisition-return figures are either backed by spend data or labeled unverified. Each finding carries its held-out status.
- Reviewer sign-off: report it separately as obtained or pending. Your own review does not substitute for it.
```

**Ledger**
- `altitude`: original outcome was a QBR deck that reports the quarter. Improved outcome is a deck that settles the retention-vs-acquisition decision in return per dollar, with a measurement plan that uses existing cadence. Adds analysis effort only, no scope change.
- `depth`: the waterfall, cohort and Kaplan–Meier curves, LTV, and CAC payback are all built from raw export rows in a reproducible script. This replaces summary tables and lets every number be traced back to its source.
- `depth`: checking first for acquisition spend data. The comparison cannot work without it; if it is missing, the acquisition side is labeled unverified.
- `depth`: a segment-level test of the either/or belief, confirmed on a held-out quarter. This can reveal a split answer and guards against patterns found by chance. It needs at least 4 quarters of history.
- `range`: decision analysis (expected value, tornado chart, value of information) shows leaders which assumption would flip the decision.
- `range`: the pyramid principle puts the answer first, which fits busy leaders and the 12-slide cap.
- `range`: a red-team case and pre-mortem test the recommendation before the meeting. This uses staff time and needs data sharing, so it requires approval.
- `range`: a causal-inference caveat keeps observed retention separate from the effect of an intervention, so program impact is not overclaimed.
- Skipped: a stretch target, because the 12-slide deck has no room to report one and the decision matters more than a metric target. Customer research and pilots, because contacting customers is prohibited. Recurring tracking dashboards, because the operating cadence is fixed.
- Owner actions:
  - Share both exports.
  - Provide acquisition spend data, or confirm it is in the exports.
  - Name the reported revenue figure to reconcile against.
  - Approve a discount rate.
  - Confirm the inferred decision framing.
  - Name and approve the finance reviewer and red-team colleague.
  - Approve any additional data pulls.
