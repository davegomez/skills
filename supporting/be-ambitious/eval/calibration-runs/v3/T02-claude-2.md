```text
Prepare the quarterly business review deck for our leadership meeting in two weeks. Its purpose is to let leaders decide whether to invest in retention or acquisition. The deck is required and has at most 12 slides, appendix included. Use existing staff and tools. Do not change our operating cadence. Do not contact customers.

Goal (assumption, confirm with me): leaders leave the meeting with a committed choice. The choice rests on a comparable estimate of what the next unit of investment returns in retention versus acquisition, and on the evidence that would reverse it.

First checks, before any analysis:
- Confirm you have received the raw customer and revenue exports. List their fields, date ranges, row counts, and gaps.
- Check whether the exports include acquisition data: spend, channel, or signup source. Without it you can measure retention economics but not acquisition economics. Name what is missing, ask me for it, and label any acquisition figure built on assumptions as an assumption.
- Check whether a reported quarterly revenue figure from finance exists to reconcile against. If none exists, reconcile only internally and say so.
- Keep customer-level data out of the deck. Show aggregates only.

Method:
1. Build everything from the raw exports with a reproducible script or workbook in our existing tools. No hand-typed numbers. Every figure in the deck must trace back to it.
2. Retention side:
   - Cohort revenue retention curves by signup quarter.
   - Gross and net revenue retention.
   - Survival analysis: Kaplan-Meier curves by segment, plus a Cox or comparable model of churn drivers. This shows when and where customers leave, which a single churn rate cannot.
   - Customer lifetime value by segment from those curves.
3. Acquisition side: payback period and lifetime value to acquisition cost by channel or segment, if the data allows.
4. Test the belief the decision rests on. The question frames retention and acquisition as competing for the same investment. Estimate the marginal return of each: what an increment of churn reduction is worth versus an increment of new customers at observed cost. Check whether the answer differs by segment. If it does, the right answer may be "retention for segment A, acquisition for segment B." Present that only if the evidence supports it.
5. Decision analysis:
   - State the expected value of each option.
   - Show a tornado sensitivity chart of the inputs that move it most.
   - Give the break-even value of each key input, meaning what would have to be true for the other option to win.
   - Note which unknown is most worth resolving before committing (value of information).
6. Analysis of competing hypotheses for any churn explanation. List the rival causes and the evidence that would separate them. Report which ones the data rules out and which it cannot.
7. Pre-mortem. Assume the recommended option fails a year from now. Write the most likely reasons and show which ones the data can already check.
8. Structure the deck answer-first:
   - Decision asked.
   - Recommendation.
   - The 2–3 numbers that decide it.
   - Evidence.
   - Risks and what would change the call.
   - The ask.
   - One slide on evidence quality: data coverage, reconciliation, and model backtest.
   Keep analysis that does not fit in 12 slides in the backing workbook, not in extra slides.

With my approval only: share the draft deck and backing workbook with a named existing staff member (e.g., someone in finance) for independent review.
With my approval only: propose a post-decision measurement plan, such as a cohort or holdout comparison. Present it in the deck as an option for leaders. Do not start any new recurring report or process.

Judge and pass conditions:
- Format: the deck has at most 12 slides.
- Reconciliation: rerunning the script from the raw exports reproduces every deck figure within rounding. Total revenue ties to the exports, and to finance's reported figure if one exists. Any unreconciled gap is shown on the evidence-quality slide.
- Backtest: fit the retention model on data through the quarter before the most recent one, then predict the most recent quarter's retention. Report the error alongside a naive baseline (last period's rate carried forward). If the model does not beat the baseline, label its forecasts directional. Report the result on the evidence-quality slide.
- Independent review (only if approved): the reviewer reads the deck cold and, without help, states:
  - the recommendation
  - the deciding numbers
  - what would reverse it
  The reviewer also flags any figure they cannot trace to the workbook. Pass means all three are stated correctly and no figure is untraced. Until the review runs, report it as pending. Your own read of the deck does not count as this check.
```

**Ledger**
- `altitude`: from "a QBR deck about retention vs acquisition" to "a committed decision based on comparable marginal returns, with explicit break-evens and reversal conditions." This adds no scope beyond the analysis. Achieving it depends on getting acquisition cost data.
- `depth`: the raw exports feed a reproducible pipeline (cohort curves, NRR/GRR, Kaplan-Meier/Cox, LTV, payback). This replaces summary tables and makes every number traceable. It costs analyst time within the two weeks.
- `depth`: the move is to test the belief that this is a single either/or choice by estimating marginal returns per segment. This may yield a split recommendation. That risk is disclosed only if the data supports it.
- `depth`: the judge is reconciliation plus a backtest on a held-out quarter against a naive baseline. The results go on one evidence-quality slide inside the 12-slide limit.
- `range`: decision analysis (expected value, tornado chart, break-even, value of information) makes uncertainty decidable in a single meeting.
- `range`: analysis of competing hypotheses from intelligence work keeps a convenient churn story from going untested.
- `range`: a pre-mortem as red team exposes how the recommended option could fail.
- `range`: answer-first structure from consulting fits busy leaders and the slide cap.
- Approval-gated: sharing data with an independent reviewer (delegation and data sharing), and a post-decision measurement plan. The plan is offered only as an option, so the operating cadence is unchanged.
- Skipped: no hard stretch target. The deliverable is a decision, not a metric to push, so a target number would add no checkable benefit.
- Owner actions:
  - Share the raw customer and revenue exports.
  - Supply acquisition spend/channel data and finance's reported quarterly revenue, if they exist.
  - Confirm the assumed goal.
  - Approve or decline the independent reviewer and name them.
  - Approve or decline including the measurement-plan option.
