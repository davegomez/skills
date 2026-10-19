```text
Prepare the quarterly business review deck for our leadership meeting in two weeks so leaders can decide whether to invest in retention or acquisition. The deck is required and must be at most 12 slides, counting any appendix. Use existing staff and tools. Do not change our operating cadence or contact customers.

Goal: leaders leave the meeting with a retention-vs-acquisition decision based on the marginal return of the next dollar in each, the uncertainty around it, and what would change their minds.
Assumption: the decision is about where the next increment of spend goes, so marginal returns matter more than historical averages.
Assumption: leaders will revisit the decision after the meeting, so the deck should name the result that would confirm or reverse it, using a metric already reported in the existing cadence.

First checks, before any analysis:
- Confirm receipt of the raw customer and revenue exports. Until they arrive, build only the analysis plan and the slide skeleton, with no numbers.
- Inventory what the exports contain: customer IDs, start and end dates, revenue by period, plan or segment, acquisition channel, and acquisition and retention spend. Name each missing field and the analyses it blocks. Label any estimate that stands in for missing data as an assumption.
- Confirm which existing tools support reproducible analysis (for example a SQL database, notebook, or versioned spreadsheet).
- Confirm which existing staff member will act as the judge below, and whether they already have access to the exports.

Method:
1. Work from the raw exports, not existing dashboards or summaries. Write the analysis as a re-runnable script or query set so every number on a slide traces to its source.
2. Reconcile first: compare total revenue in the exports with the quarter's reported revenue and show any gap.
3. Cohort analysis: group customers into acquisition cohorts and report gross and net revenue retention, logo churn, and expansion for each cohort. This shows whether retention is improving or decaying across cohorts.
4. Survival analysis (actuarial method):
   - Estimate Kaplan-Meier retention curves by segment and channel to show when in the customer lifetime churn happens and where it concentrates.
   - Fit a Cox proportional-hazards model on the available fields to rank churn drivers.
   - Fit on earlier cohorts. Confirm each reported driver on the most recent cohorts, which are held out from fitting.
   - Label drivers that fail the holdout as unconfirmed, or drop them.
5. Unit economics (finance method):
   - Compute lifetime value from the survival curves and margin.
   - If spend data exists, compute acquisition cost and payback period by channel.
   - Estimate marginal acquisition returns: how cost per new customer moves with spend across periods and channels.
   - Estimate marginal retention returns: revenue preserved per point of churn reduction in the at-risk segments the survival model identifies.
6. Test the belief the question rests on. Check from the data whether retention and acquisition are really separate choices. For example, if some channels bring customers who churn faster, then channel mix is a retention lever. Also check whether the decision is binary or a reallocation. Report what you find, even if it reframes the question.
7. Causal caution (epidemiology method): describe each driver as an association unless the data supports more. Name the likely confounders (segment, plan, tenure, channel) and control for them where the data allows.
8. Decision analysis:
   - Compare the expected value of each option: all-retention, all-acquisition, and any split the data supports.
   - Add a tornado chart showing which assumptions swing the answer, and the break-even value of each.
   - State what extra information would change the decision, and whether existing data can supply it before the meeting.
9. Red team, on one slide:
   - Run a pre-mortem on the recommended option: "A year from now this investment failed. Why?"
   - Write the strongest case for the other option.
10. Write the deck answer-first (pyramid principle):
    - Slides 1–2: the recommendation and the decision asked of leaders.
    - Middle slides: the supporting evidence.
    - Near the end: risks, and the result that would reverse the decision.
    - Methods, definitions, and data caveats go in speaker notes or on one appendix slide, within the 12-slide limit.
11. Name the metric leadership should watch to confirm or reverse the decision, chosen from metrics already reported in the existing cadence, and the threshold that triggers a revisit. Do not propose new recurring reports, reviews, or meetings.

Do not contact customers for surveys, interviews, or validation. Use only the exports and existing internal data.

With my approval only: share the raw exports with the judge if they do not already have access.

Judge: before the meeting, an existing finance or analytics staff member other than the author reruns the analysis from the raw exports and checks that:
(a) every number on the slides reproduces, and revenue reconciles to the quarter's reported figure or the gap is shown;
(b) each reported churn driver held on the held-out cohorts, or is labeled unconfirmed;
(c) the recommendation follows from the expected-value comparison, and the sensitivity analysis shows what would flip it;
(d) the strongest case for the other option is stated fairly;
(e) the deck has at most 12 slides, states the decision asked of leaders on slides 1–2, and names the existing-cadence metric and the threshold for revisiting.
Pass only if every criterion is met. Until the judge runs, mark the deck's findings as unverified.
```

- `altitude`: The original outcome was a QBR deck that informs the choice. The improved outcome is a decision made in the room, framed by marginal returns, break-even values, and a named reversal trigger. The trigger uses only metrics already reported, so the operating cadence does not change.
- `depth`: Working from the raw exports, with a reconciliation step and a re-runnable script, makes every number traceable and reproducible by the judge. It needs an existing analysis tool.
- `depth`: Cohort NRR/GRR plus Kaplan-Meier and Cox survival analysis, confirmed on held-out recent cohorts, separates real churn drivers from patterns that only fit the data they were found in.
- `depth`: Testing the core belief checks whether "retention vs acquisition" is a real binary choice, for example whether channel mix drives churn. This may reframe the decision leaders are asked to make.
- `range`: Finance unit economics (LTV, payback, marginal cost per customer) compares the next dollar in each option, not historical averages. It depends on spend data being in the exports.
- `range`: Decision analysis (expected value, tornado chart, value of information) shows leaders which assumptions the answer hinges on.
- `range`: Epidemiology's confounder control stops the deck from presenting correlated churn drivers as causes.
- `range`: The red team (pre-mortem plus a steelman of the other option) exposes decision risk before leaders commit.
- `range`: The pyramid principle puts the ask on slides 1–2 for a time-limited audience. Counting the appendix within 12 slides is the stricter reading of the limit.
- `judge`: An independent rerun by existing finance or analytics staff, against a five-part rubric, replaces the author's own verdict. Sharing the exports with that person is behind approval if they lack access.
- Skipped: none. All three lenses fit. A hard numeric stretch target was not used because this is a decision task, not a metric-improvement request.
- Owner actions:
  - Share the raw customer and revenue exports.
  - Confirm whether they include acquisition and retention spend.
  - Name the existing staff member who will serve as judge.
  - Approve sharing the exports with that person if they don't already have access.
