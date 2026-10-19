```text
Prepare the quarterly business review deck for our leadership meeting in two weeks. The deck is required and must be at most 12 slides, appendix included. Its job is to let leaders decide whether to invest in retention or acquisition, and to show what evidence would change that decision.

Assumption: the decision is where to put the next increment of budget or effort, so the deck should compare the expected return per dollar of each lever at the margin, not overall averages.
Assumption: leaders will act on the deck in one meeting, so every slide title states its claim and the titles alone tell the full story.

First checks, before any analysis:
- Receive the raw customer and revenue exports. Confirm the quarters, fields, customer IDs, and how churn, expansion, and contraction can be read from them. Reconcile total revenue to the figure finance reports for the same periods.
- Confirm whether acquisition cost data exists in existing tools: sales and marketing spend by quarter, and channel if available. If it is missing, say so on the relevant slide and present acquisition economics as a range with stated assumptions, not as a point estimate.
- Confirm which existing analysis tools and staff are available, including one independent reviewer from existing staff (finance or analytics) who did not build the analysis.
List missing dependencies and continue only with the work the available data supports.

Method:
1. Growth accounting from the raw revenue export. Split each quarter's revenue change into new, expansion, contraction, and churned revenue. Report net and gross revenue retention, so leaders can see which lever has actually driven growth.
2. Cohort survival from the raw customer export. Build cohort-by-quarter retention curves with Kaplan-Meier estimates that handle censoring, so recent cohorts are not mistaken for better ones. Segment by the attributes the export supports (plan, size, channel, tenure). Find where churn concentrates and whether that is the fixable part.
3. Customer lifetime value from the observed survival curves and revenue per customer, with acquisition cost and payback period where spend data exists.
4. Decision analysis. Model 4-quarter revenue under two scenarios: a plausible reduction in churn among the concentrated segments, and a plausible increase in new customers at observed or assumed marginal acquisition cost. Show a tornado sensitivity chart of the inputs that would flip the recommendation. State the break-even point, for example "acquisition wins only if marginal CAC stays below X". Note any diminishing returns visible in the spend data.
5. Test the premise. Check from the data whether retention and acquisition really compete for the same budget, or whether one constrains the other, for example new cohorts churning faster. Report what you find, even if it reframes the choice.
6. Backtest. Fit the retention and revenue model on data through the second-most-recent quarter. Predict the most recent quarter, and report the prediction error on the slide that carries the forecast. Treat any segment finding that shaped the model as development evidence. Mark it confirmed only if it also holds on the held-out quarter; otherwise label it unverified.
7. Red team. Have one existing staff member build the strongest case for the option the deck does not recommend. Include the result as a short "case against" with the deck's response, within the 12 slides.
8. Structure. Put the answer first, using the pyramid principle: recommendation, the 2–3 findings that support it, the key uncertainty and what would resolve it, then supporting evidence. Each slide makes one claim with one chart. Every number traces to a named query or calculation on the raw exports.

Constraints: use existing staff and tools only. Do not change our operating cadence. Do not contact customers, including surveys, interviews, or experiments that reach customers. Use only the exports I provide and data already in existing internal tools.

With my approval only: a companion methods note outside the 12-slide deck documenting queries, assumptions, and backtest details.

Judge:
- Mechanical checks: 12 or fewer slides. Deck revenue totals reconcile to the raw revenue export within rounding. Every number on a slide traces to a source calculation. The backtest error is reported on the forecast slide.
- Independent review: the existing-staff reviewer who did not build the analysis scores the deck on this rubric, pass or fail per item:
  (a) the recommendation and its break-even condition are stated on slide 1 or 2;
  (b) both options are compared on the same metric, return per marginal dollar over 4 quarters;
  (c) cohort and churn claims account for censoring and segment mix;
  (d) the strongest counter-case is presented fairly;
  (e) uncertainty and the inputs that would flip the decision are visible;
  (f) reading only the slide titles, the reviewer can state the recommendation, the evidence for it, and what would change it.
- Pass condition: all mechanical checks hold and the reviewer passes every rubric item. Report any item that fails, along with the backtest error, rather than omitting it. If cost data is missing, the acquisition comparison stays labeled as assumption-based and unverified.
```

**Ledger**

- `altitude`: the outcome moves from a quarterly review deck to a deck that drives a single allocation decision, with a break-even condition and the evidence that would change it. No added scope. The deck stays within 12 slides and the existing cadence.
- `depth`: the analysis works from the raw exports, using growth accounting, Kaplan-Meier cohort survival, and LTV/CAC/payback. Leaders see what actually drove revenue, not summary averages. It needs an analyst's time from existing staff.
- `depth`: the premise test checks whether retention and acquisition really compete. It may reframe the either/or. This costs analysis time only.
- `depth`: the model is backtested on a held-out quarter, and segment findings stay unverified unless that quarter confirms them. This keeps the analysis from overfitting the story.
- `range`: from decision analysis, the deck uses marginal comparison, scenarios, a tornado chart, and a break-even point. Leaders see which input decides the choice.
- `range`: from red teaming, a staff member argues the case against the recommendation. This exposes the decision risk before the meeting. It needs one existing staff member's time.
- `range`: from information design, the deck uses answer-first pyramid structure and a titles-only test. This makes it decidable by busy people in one meeting.
- `scope`: a companion methods note is gated behind your approval, because the 12-slide limit counts every slide.
- Skipped: the hard-target move, because this isn't a quantitative improvement request. Also skipped are a pilot or holdout experiment on the outcome itself, and any post-decision tracking cadence. These would contact customers or change the operating cadence, which you prohibited.
- Owner actions:
  - Share the customer and revenue exports.
  - Confirm whether sales and marketing spend data exists in current tools.
  - Name an independent reviewer and a red-team staff member.
  - Decide on the companion methods note.
