```text
Prepare the quarterly business review deck for our leadership meeting in two weeks, so leaders can decide whether to invest in retention or acquisition.
Assumption: leaders are deciding where the next increment of budget goes. The deck must compare the marginal return of one more unit of spend on each option, not average returns, and may conclude that a targeted split beats either pure choice.
Assumption: the exports cover enough quarters to build cohorts and hold out the latest quarter. If they don't, say so and mark the dependent results unverified.
Open the deck with the recommendation and the decision asked of leaders. Give each slide a title that states its conclusion, and build the supporting slides into one cause-and-effect story.
Before reading results, write the decision rule and record it, dated, in the working files. The rule states which comparison of retention and acquisition returns favors which option, over which horizon, and what margin counts as a tie. Apply it unchanged.
Work from the raw customer and revenue exports, not summary reports. Build a revenue bridge for the quarter (starting revenue, new, expansion, contraction, churn) that reconciles to the export totals. Compute gross and net revenue retention by cohort.
Use survival analysis (Kaplan-Meier retention curves by start cohort and segment) to show when and where customers churn, and whether churn is concentrated in segments that retention spend would reach.
Estimate customer lifetime value from the observed curves and margins. Where spend data is available, compute acquisition cost and payback by channel or segment, and the cost to retain an at-risk customer.
Quantify uncertainty. Bootstrap the key figures and show ranges, not points. Run a sensitivity (tornado) analysis showing which assumption, at what value, flips the recommendation, and put that flip point on a slide.
Treat churn drivers as development findings: find them on earlier quarters, then confirm them once on the most recent quarter, which stays untouched until then. Report drivers that fail confirmation as unconfirmed. Label correlations as correlations; do not claim a retention action causes retention without evidence that it does.
Red team: include one slide that makes the strongest case for the option not recommended. Add a pre-mortem naming how the recommendation could fail and the leading indicator in our existing reports that would show it failing.
State what the exports cannot answer and what data would resolve it.
The deck is required and must be at most 12 slides, appendix included.
Use existing staff and tools. Do not change our operating cadence. Do not contact customers: no surveys or interviews.
With my approval only: obtain acquisition and retention spend data (sales, marketing, and customer-success cost by quarter and, where recorded, by channel or segment) from existing finance records.
With my approval only: deliver a separate validation note that maps each figure in the deck to its source query or calculation on the exports.
First check: I have shared the raw customer and revenue exports, and they contain customer ID, start and end or cancellation dates, revenue by period, and segment. Name any missing fields and continue only with supported work.
First check: if spend data is approved, confirm it exists and the finance records are accessible. Without it, mark acquisition cost, payback, and the marginal-return comparison unverified rather than estimating them from assumptions presented as fact.
First check: a finance or analytics staff member other than the author is available to review before the meeting and is permitted to see the customer and revenue data.
Judge: an existing finance or analytics staff member other than the author recomputes every figure in the deck from the raw exports (and approved spend data) and checks that the deck has at most 12 slides; each figure matches its recomputation within rounding; the revenue bridge reconciles to export totals; the dated decision rule predates the results and was applied as written; each comparative claim is backed by computed figures with ranges or is labeled unverified with the missing data named; every churn driver presented as confirmed held up on the held-out quarter; the flip-point assumption and the case for the other option are shown; no customer was contacted and no cadence change is proposed; pass only if every criterion is met.
```

- `altitude`: The original outcome was a QBR deck. The improved outcome is a deck that drives one allocation decision, with a pre-written decision rule, a marginal-return comparison, and the assumption that would flip the answer. There is no added scope. Post-decision tracking was left out because it would change the operating cadence.
- `depth`: The deck is built from the raw exports, with a revenue bridge, cohort net and gross retention, Kaplan-Meier curves, LTV, CAC, and payback. This replaces summary figures with reconciled, segment-level evidence. Cost: analyst time from existing staff.
- `depth`: Churn drivers must be confirmed on a held-out latest quarter, and bootstrap ranges are required. This stops leaders from acting on drivers or point estimates that don't hold. Risk: short history leaves the drivers unverified.
- `depth`: The spend data needed for acquisition ROI is behind approval. Without it, the core comparison can't be computed and is marked unverified. Access effect: the executor gets finance records that were not offered.
- `range`: Decision analysis contributes the pre-written decision rule and the tornado flip point, so leaders see what they would have to believe to choose otherwise.
- `range`: Epidemiology and causal inference contribute correlation labeling and development-versus-confirmation separation. This blocks "retained customers got X, so X causes retention."
- `range`: Red team contributes the strongest-opposing-case slide and a pre-mortem tied to existing reports. This exposes decision risk without adding a cadence.
- `range`: Consulting communication (answer first, conclusion titles) fits the decision into a 12-slide leadership read.
- Skipped: the hard-target move, because this is not a quantitative improvement request. Also skipped: any customer research or new monitoring cadence, which the owner prohibited.
- Owner actions: share the exports; approve or decline access to the spend data and the separate validation note; name a finance or analytics reviewer, other than the author, who can see the data before the meeting.
