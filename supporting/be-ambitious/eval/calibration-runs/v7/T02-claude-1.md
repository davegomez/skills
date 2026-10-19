```text
Prepare the quarterly business review deck for our leadership meeting in two weeks. Leaders will use it to decide whether to invest in retention or acquisition. The deck is required and must be at most 12 slides, including any appendix or backup slides. The deck is the only deliverable. Use existing staff and tools. Do not change our operating cadence. Do not contact customers.

Goal: a deck that lets leaders make the retention-versus-acquisition decision in the meeting. The page should show the evidence, the uncertainty, and what would change the answer.
Assumption: the decision is about where the next incremental investment goes, and leaders want a recommendation, not only a description of the quarter.
Assumption: the deck must still cover the standard quarterly review content, organized around the decision and kept within the 12-slide limit.

First checks, before analysis:
1. Confirm I have shared the raw customer and revenue exports. Until I do, run no analysis. Draft only the slide outline and the list of fields you need.
2. Check that the exports give, for each customer, a stable ID, start date, churn or end date, revenue by period, and any segment, plan, or acquisition-channel fields. List the gaps and which slides each gap affects.
3. Reconcile total revenue per period in the exports to the revenue figure leadership already uses. Report and explain any difference before building on the data.
4. Check whether retention and acquisition spend data (for example, cost to acquire a customer) is already available to you through existing tools. If it is not, do not request new access. Use the fallback below.
5. Confirm with me the planning horizon leaders use for investment decisions.
Name any missing dependency and continue only with work the available data supports.

Method:
- Answer first (pyramid principle). Slide 1 states the recommendation, the main reason, and the level of confidence. Each later slide supports one claim, and its headline is that claim.
- Revenue bridge: split the quarter's change in recurring revenue into new, expansion, contraction, and churned revenue. This shows which lever moved revenue, which the net total hides.
- Cohort survival: group customers by start quarter. Show logo and revenue retention over time as cohort tables or survival curves, and report gross and net revenue retention. This shows whether retention is improving or worsening across cohorts, which a single churn rate hides.
- Compute lifetime value from observed cohort survival, not from an assumed constant churn rate.
- Segment the bridge and the retention results by the segment, plan, and channel fields that exist, to find where churn and growth concentrate.
- Test the premise of the decision from the raw data. Over the confirmed planning horizon, compare the revenue added by a plausible retention improvement with the revenue added by an equal-size acquisition improvement. Show the break-even point: how much improvement in one lever matches a given improvement in the other.
- If spend data is available, express each lever as revenue per unit of spend. If it is not, present the revenue side only and state plainly that leaders must judge the cost of each unit of improvement. Do not invent cost figures.
- Decision analysis: include a sensitivity (tornado) chart showing which assumptions would flip the recommendation, and state what evidence would change it.
- Causal caution: this is observational data. Label patterns as associations and name likely confounders, such as segment mix or pricing changes. Do not claim a lever causes an outcome without evidence that supports it.
- Held-out check: develop segment findings on earlier periods, then test them on the most recent quarter, which was not used to find them. Label any finding that fails this test, or could not be tested, as unverified.
- Red team: before review, write the strongest case for the opposite recommendation and a pre-mortem ("a year from now this choice failed; why?"). Address the strongest points on a slide or in the speaker notes.
- Close with how leaders will know the decision worked: the metric to watch and its threshold, reviewed at a meeting that already exists in our cadence. Do not propose new meetings or reviews.
- Footnote every number with its source export and period.

With my approval only: request access to marketing, sales, or customer-success spend data that is not already available to you.
With my approval only: ask a colleague who did not author the deck to review the red-team case independently.

Judge: a finance or analytics lead from existing staff, other than the author and named by me, checks that:
(1) the deck has 12 or fewer slides, including the appendix;
(2) revenue totals on the slides reconcile to the raw exports and to the leadership revenue figure, and any differences are explained;
(3) slide 1 states a recommendation, its main reason, and the confidence level;
(4) both levers are compared over the same horizon in the same units, and missing cost data is stated rather than estimated;
(5) the sensitivity view names what would flip the recommendation;
(6) each segment finding is marked either confirmed on held-out data or unverified;
(7) the strongest opposing case is addressed;
(8) no customer was contacted and no cadence change is proposed.
Pass only if every criterion is met. Treat the deck as unverified until the reviewer signs off, and leave time for this review before the meeting.
```

- `altitude`: The original outcome was a QBR deck. The improved outcome is a decision made in the meeting, with a stated confidence level, the conditions that would flip it, and a success metric checked at an existing review. I did not go a rung higher (piloting either lever), because that would need cadence changes or customer contact, and you prohibited both.
- `depth`: The analysis starts from the raw exports, reconciled to the revenue figure leadership already uses. It adds a revenue bridge, cohort survival curves, survival-based lifetime value, and a segment breakdown. These show which lever actually moved revenue, which a summary churn rate hides. It needs no new tools.
- `depth`: The deck tests the premise of the decision with a break-even comparison of the two levers from the raw data. If spend data is missing, it reports revenue impact only and says so instead of inventing costs.
- `depth`: Segment findings are developed on earlier periods and confirmed on the most recent quarter, or labeled unverified. This lowers the risk of presenting a pattern that the data only appears to show.
- `range`: Decision analysis contributes the tornado sensitivity chart and the conditions that would change the answer, so leaders can decide under uncertainty.
- `range`: Epidemiology and actuarial science contribute cohort survival tables, which separate improving cohorts from worsening ones.
- `range`: Causal inference contributes labeling patterns as associations and naming confounders, which keeps observational data from being presented as proof.
- `range`: Communication practice contributes the answer-first pyramid structure, which fits the decision into a busy meeting and the 12-slide limit.
- `range`: Red teaming contributes the opposing case and a pre-mortem, which test the recommendation before leaders see it. An independent red-team reviewer needs your approval.
- Skipped: the hard-target move, because this is a decision deck rather than a request for quantitative improvement. The pilot or outcome-level rung, because it would require contacting customers or changing cadence.
- Owner actions: share the exports; name the reviewer for the judge step; confirm which revenue figure leadership uses; confirm the planning horizon; decide whether to approve spend-data access and an independent red-team reviewer.
