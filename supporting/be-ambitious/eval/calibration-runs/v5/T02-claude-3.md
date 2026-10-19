```text
Prepare the quarterly business review deck for our leadership meeting in two weeks. The deck exists so leaders can decide whether to invest in retention or acquisition. Build it to make that decision clear: the recommendation, the evidence behind it, how confident we are, and what result would reverse it. The deck is required and has at most 12 slides. Count every slide, including any appendix, toward the 12.

Assumption: leaders need to compare the expected return of the next increment of investment in each option, not the historical average return of each.
Assumption: some apparent retention problems may come from acquisition, because certain customers churn more by channel or segment. The analysis should test this rather than assume either option is independent of the other.

First checks, before any analysis:
- Get the raw customer and revenue exports from me. They have not been shared yet. Record the fields, the date range, the row counts, and the revenue totals.
- Check whether the exports hold the inputs each side of the decision needs: customer start and end dates, revenue by customer by period, acquisition channel or segment, and acquisition spend by channel and period.
- Name every missing input and which slide or claim it blocks. Continue only with the analyses the available data supports, and mark the blocked claims unverified in the deck.
With my approval only: obtain acquisition spend by channel and period from existing systems if the exports do not contain it.

Method, using existing staff and tools only:
1. Start from the raw exports, not from existing dashboards. Tie the deck's revenue and customer totals back to the export totals. Record any difference and its cause.
2. Build retention cohorts by acquisition period and by channel or segment. Compute logo retention, gross revenue retention, and net revenue retention. Estimate customer lifetime with survival analysis (Kaplan-Meier curves), which handles customers who have not churned yet, instead of averaging only the customers who have.
3. Test what drives churn. Fit a hazard model (Cox regression) on the available customer attributes. Check whether channel or segment predicts churn after the other attributes are controlled for. This tells leaders whether "retention" and "acquisition" are really one problem.
4. Estimate the marginal return of each option. For acquisition, use cost per acquired customer by channel against the lifetime revenue of that channel's cohort, wherever spend data exists. For retention, use the revenue a given reduction in churn would preserve. Show uncertainty ranges, not point estimates.
5. Hold out the most recent quarter. Fit the cohort and lifetime estimates on earlier data, predict the held-out quarter's retained and new revenue, and report the prediction error. If the analysis is revised after looking at the held-out quarter, call that quarter development evidence and mark the revised claim unverified.
6. Decision analysis. Before seeing the final estimates, state the decision rule, for example "favor whichever option has the higher lower-bound marginal return." Then run a sensitivity analysis (tornado chart) over the key inputs. Report the break-even value: how much each input would need to change to flip the recommendation. Name the single fact that would most change the decision if leaders knew it.
7. Red team. Have one person from existing staff who did not build the analysis write the strongest case for the option the deck does not recommend. Then run a pre-mortem: assume the recommendation failed a year from now and list why. Address the strongest points in the deck.
8. Structure the deck answer-first (pyramid principle). Slide titles should state conclusions, so that reading the titles alone gives the recommendation and its reasons. Use small multiples for the cohort comparisons. Keep working detail in the analysis files, not in extra slides.

With my approval only: add a short readout to the next scheduled quarterly review that compares the chosen option's leading indicators with this deck's predictions. Use the existing meeting; do not add a new one.

Constraints: do not change our operating cadence. Do not contact customers. Use existing staff and tools only. Distinguish observed figures from estimates and assumptions on every slide.

Judge and pass conditions:
- Mechanical: the deck has 12 slides or fewer. The deck's totals reconcile to the raw exports, or every difference is explained in writing. The held-out-quarter prediction error is reported, along with whether any revision used it.
- Independent review: a qualified reviewer from existing staff who did not build the analysis scores the deck against this rubric:
  (a) the recommendation can be stated from the slide titles alone;
  (b) every number traces to the exports or to a labeled estimate;
  (c) uncertainty and break-even values are shown;
  (d) the red-team case is answered;
  (e) blocked or unverified claims are labeled.
- Pass when every mechanical check holds and the reviewer marks all five rubric items met.
- Any claim that depends on missing data or on a check that has not run stays labeled unverified.
```

- `altitude`: The outcome moves from "a QBR deck" to "a deck that makes the retention-vs-acquisition decision clear," with a decision rule, break-even values, and the fact that would reverse it. This adds no scope beyond the analysis. The next-QBR readout sits behind approval and uses the existing cadence.
- `depth`: The analysis starts from the raw exports with a reconciliation, then uses survival curves, a churn hazard model, marginal (not average) return, and a held-out-quarter backtest. This replaces dashboard summaries with testable estimates. The cost is analyst time from existing staff.
- `depth`: The deck tests the belief the task rests on, that retention and acquisition are separable, by checking whether channel predicts churn. This can reframe the decision itself.
- `range`: Decision analysis (sensitivity analysis, break-even values, which unknown fact matters most) shows leaders how fragile the call is.
- `range`: The red-team case and the pre-mortem expose decision risk before the meeting. This needs one staff reviewer.
- `range`: Answer-first structure and small multiples make the recommendation clear within the 12-slide limit.
- Skipped: none.
- Owner actions:
  - Share the customer and revenue exports.
  - Approve, or decline, sourcing acquisition spend data if the exports lack it.
  - Name the red-team staff member and the independent reviewer.
  - Approve or decline the next-QBR readout.
  - Confirm that appendix slides count toward the 12.
