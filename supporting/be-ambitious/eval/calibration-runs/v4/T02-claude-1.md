```text
Prepare the quarterly business review deck for our leadership meeting in two weeks. The deck exists so leaders can decide whether to invest in retention or acquisition. Build it so they can make that decision in the meeting: state which lever returns more per next dollar invested, by how much, how confident we are, and what result would reverse the call.

Constraints (all binding):
- The deck is required and must be at most 12 slides. Count every slide, including appendix or backup slides.
- Work only from the raw customer and revenue exports I will provide. Use existing staff and tools. Keep customer data inside those tools.
- Do not change our operating cadence. Do not contact customers.

First checks, before any analysis:
1. Confirm that you have received the customer and revenue exports. List their fields, date range, grain (customer, invoice, or month), and row counts.
2. Confirm that each customer can be joined to its revenue over time and that start and churn dates can be derived.
3. Check whether acquisition spend or CAC by channel and period exists in the exports or with existing staff. The acquisition side of the comparison depends on it.
4. Confirm which existing staff member can serve as the independent reviewer, preferably from finance.
For any missing item, name the gap and its effect on the decision, then continue with what the data supports. If spend data is missing, report the breakeven CAC at which acquisition would match retention, and leave the actual comparison unverified.

Analysis (start from raw rows, not pre-built summaries):
- Revenue bridge: decompose the quarter's revenue change into new, expansion, contraction, and churned revenue. Reconcile the bridge to total revenue in the export.
- Cohorts: group customers by acquisition month or quarter. Build gross and net revenue retention curves. Use survival analysis (Kaplan-Meier curves, plus a Cox model or shifted-beta-geometric fit if the data supports it) to estimate churn hazard by tenure and segment.
- Unit economics: compute discounted customer lifetime value and CAC payback by segment.
- Compare at the margin. Estimate the return on the next dollar for each lever (retained revenue saved per dollar vs. new-customer LTV per dollar of CAC), not average historical returns.
- Check segments for Simpson's paradox: confirm that the aggregate answer holds within the main segments, or show where it flips.
- Treat retention-program effects as associations unless the data contains a comparison group. Retained customers may differ from churned ones for reasons unrelated to any program. State this caveat where it affects the recommendation.

Test the belief the recommendation rests on, using held-out data:
- Fit the churn and retention model on all periods except the most recent full quarter.
- Forecast that quarter's retained revenue, then compare the forecast to actuals.
- Report the error alongside a naive baseline (last quarter's churn rate carried forward).
- If the model does not beat the baseline, base the recommendation on the baseline and say so in the deck.

Decision framing (decision analysis):
- Express each option as an expected return with a range.
- Show a tornado or breakeven sensitivity on the 3 assumptions that most move the answer, such as churn rate, CAC, and expansion rate.
- Name the single uncertainty most worth resolving. Name the evidence threshold that would reverse the recommendation.
- Include a "mixed allocation" option if the marginal returns cross within the plausible range.

Red team:
- Before finalizing, run a pre-mortem: "Six months after the decision, the chosen lever underperformed. Why?"
- Run an Analysis of Competing Hypotheses on the main driver of churn. Use the data to discriminate among the explanations, not to support only one.
- Show the surviving risks on one slide.

Deck design:
- Answer first (Minto pyramid): slide 1 states the recommendation, the number behind it, and the confidence.
- Use assertion-evidence slides: each title is a claim, and the body is the chart that proves it.
- Every number must trace to a named query or calculation in the supporting workbook in an existing tool. Keep methods detail in that workbook and in speaker notes, not in extra slides.

With my approval only: add a slide recording the forecast this decision relies on, so the next regular QBR can score it against actuals, within our existing cadence.

Judge and pass condition:
- Mechanical: the deck has 12 slides or fewer. The revenue bridge reconciles to export totals within 0.5%, or every difference is itemized. Every headline number traces to the workbook. The held-out quarter's forecast error and baseline error are reported in the deck.
- Independent review: the reviewer recomputes the 3 headline numbers from the raw exports and must match them. Then, using this rubric, the reviewer must state from the deck alone: the recommendation, the number that drives it, the breakeven or reversal condition, and the biggest remaining uncertainty.
- Pass when all mechanical checks hold and the reviewer matches all 3 numbers and all 4 rubric items. Report any failure as-is.
- Until the exports arrive and these checks run, every finding is unverified.
```

**Ledger**

- `altitude`: The outcome moves from "a QBR deck" to "a deck that lets leaders decide retention vs. acquisition in the meeting": a marginal-return comparison, a confidence level, and a reversal condition. Same deliverable, same 12-slide limit, no new scope.
- `altitude`: The proposed forecast-scoring slide checks next quarter whether the decision was right. It stays within your existing QBR cadence, but it's behind approval because it commits a future slide.
- `depth`: Working from the raw exports enables a revenue bridge, cohort survival analysis, discounted LTV/payback, and marginal rather than average returns. These measure what a summary table only describes. It costs analyst time but adds no new tools.
- `depth`: Validating on a held-out quarter against a naive baseline tests the forecast the recommendation rests on, instead of trusting a fit made on the same data.
- `depth`: The Simpson's-paradox segment check and the association-vs-cause caveat prevent a misleading aggregate answer.
- `range`: Decision analysis (expected value ranges, tornado/breakeven, the uncertainty most worth resolving) turns the numbers into a choice leaders can make under uncertainty.
- `range`: A pre-mortem plus Analysis of Competing Hypotheses (from intelligence analysis) is the red team. It exposes risks in the decision and alternative explanations for churn.
- `range`: Minto pyramid plus assertion-evidence slides (information design) fit a decision into 12 slides for busy readers. Methods move to the workbook and speaker notes.
- Skipped: none. All three lenses are fit. A live retention pilot or holdout was excluded because it would contact customers or change operations.
- Owner actions:
  - Share the customer and revenue exports.
  - Confirm whether acquisition spend/CAC data exists.
  - Name the independent reviewer from existing staff.
  - Approve or decline the forecast-scoring slide.
  - Confirm that appendix slides count toward the 12-slide limit.
