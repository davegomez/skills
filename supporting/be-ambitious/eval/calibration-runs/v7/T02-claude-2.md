```text
Prepare the quarterly business review deck for our leadership meeting in two weeks. The deck is required and must be at most 12 slides. Its purpose is to help leaders decide whether to invest in retention or acquisition, so build it around that decision, not around a recap of the quarter.

Assumption: leaders need a recommendation they can act on in the meeting. That means a clear option, the expected return of each option over the same horizon, the assumptions that drive the answer, and what evidence would reverse it.
Assumption: the decision is about where the next marginal dollar goes, not whether retention or acquisition matters more in general.

First checks, before any analysis:
- Confirm I have shared the raw customer and revenue exports. Until I do, stop and list exactly what you need.
- Inventory what the exports contain: customer IDs, start/end or cancel dates, plan or segment, and revenue by customer by period. Check whether acquisition spend or CAC data is included.
- Reconcile the export revenue totals to the quarter's reported revenue. Report any gap before you build on the data.
- Confirm which existing analysis tools and which existing staff reviewer are available.
- Name every missing dependency. Continue only with the work the available data supports, and label each slide claim as observed (computed from the exports) or proposed (assumption or estimate).

Method (existing staff and tools only):
1. Work from the raw exports, not from summary dashboards. Every figure in the deck must come from a reproducible query or script that reads the exports.
2. Retention side:
   - Build monthly or quarterly customer cohorts.
   - Compute gross and net revenue retention and logo churn by cohort and segment.
   - Fit Kaplan–Meier survival curves so customers who are still active (censored) don't bias churn estimates.
   - Identify which segments drive revenue loss.
3. Acquisition side:
   - Compute new-customer counts, first-period revenue, and early survival of recent cohorts.
   - If spend data exists, compute CAC, payback period, and LTV:CAC by segment.
   - If spend data is missing, say so on the slide and state the CAC range at which acquisition beats retention.
4. Decision analysis:
   - Model the expected incremental revenue of a comparable investment in each option, over the same horizon and on the same metric.
   - Show a sensitivity (tornado) analysis of the inputs that most move the answer.
   - State the break-even assumption: the value at which the recommendation flips.
5. Test the premise:
   - Fit the retention and new-customer projections on earlier periods only.
   - Check them against the most recent held-out quarter, and report the error.
   - Check whether the data supports a split or segment-specific answer, not just a binary choice. If it does, show it as an option alongside the two leaders asked about.
6. Red team:
   - Run a pre-mortem: "it is two quarters later and this recommendation failed; why?"
   - Run an Analysis of Competing Hypotheses on the main driver of revenue change, e.g. churn vs. contraction vs. weak new-customer quality vs. seasonality.
   - Put the strongest surviving counter-case on a slide.
7. Story structure:
   - Lead with the answer, using the Minto pyramid: recommendation, then the supporting reasons, then the evidence.
   - Use one message per slide, stated in the slide title.
   - Use small multiples for cohort curves.
   - Put method details and the data lineage for each figure in speaker notes, not in extra slides.

Constraints: at most 12 slides. Use existing staff and tools. Do not change our operating cadence. Do not contact customers.

With my approval only: if the exports lack acquisition spend, request spend/CAC data from the team that owns it.

Judge:
(a) Reconciliation: every number in the deck traces to a script or query over the exports, and revenue totals reconcile to the export within rounding. Any unreconciled gap is disclosed on the relevant slide.
(b) Backtest: report the held-out-quarter error of each projection. If the held-out quarter isn't available, mark the projections unverified on the slides.
(c) Review: an existing staff reviewer other than the author, such as a finance lead, checks each of these criteria:
   - The deck has at most 12 slides, with the recommendation on slide 1 or 2.
   - Both options are compared on the same metric and horizon.
   - Observed and proposed claims are labeled.
   - The sensitivity analysis and break-even assumption are shown.
   - The strongest counter-case is presented.
   - No customer contact or cadence change was used.
Pass only if (a) and (c) pass on every criterion and (b) is either reported or disclosed as unverified. Until the judge runs, treat the deck's conclusions as unverified.
```

- `altitude`: the original outcome is a QBR deck. The improved outcome is a deck built to produce the retention-vs-acquisition decision: a recommendation, a comparable return estimate for each option, and the break-even point. There is no added scope. Rung 3 (running a live retention or acquisition test) was rejected because it would mean contacting customers or changing cadence.
- `depth`: raw exports, reproducible queries, cohort NRR/GRR, Kaplan–Meier survival, and CAC/payback replace summary-level reporting. This costs analyst time with existing tools.
- `depth`: projections are backtested on a held-out quarter, and the premise is tested by checking whether a segment-specific split beats the binary choice. This guards against confident but wrong forecasts.
- `range`: decision analysis (expected value, tornado chart, break-even) turns the data into a choice under uncertainty.
- `range`: intelligence-analysis red teaming (pre-mortem, Analysis of Competing Hypotheses) exposes alternative explanations for revenue change before leaders commit.
- `range`: information design (Minto pyramid, small multiples, speaker-note lineage) keeps the argument within 12 slides without losing traceability.
- Scope/access: requesting spend data is gated behind your approval. The reviewer must be existing staff.
- Skipped: the hard-target move, because this is not a quantitative improvement request.
- Owner actions:
  - Share the raw customer and revenue exports.
  - Confirm whether acquisition spend data exists.
  - Name the reviewer.
  - Approve or decline the spend-data request.
