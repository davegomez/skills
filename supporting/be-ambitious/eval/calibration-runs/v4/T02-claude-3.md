```text
Prepare the quarterly business review deck for our leadership meeting in two weeks. The deck exists so leaders can decide whether to invest in retention or acquisition. Build it to produce that decision: a recommendation, the evidence behind it, and the condition that would reverse it. The deck is required and must be at most 12 slides. Use existing staff and tools. Do not change our operating cadence or contact customers.

Assumption to confirm with me: "invest" means where the next marginal dollar or headcount goes, and the comparison is expected revenue (or margin) returned per unit invested over a horizon I will name.

First checks (dependencies, not yet confirmed):
- The raw customer and revenue exports have not been shared yet. On receipt, confirm they hold per-customer IDs, start and end dates, monthly revenue, plan or segment, and acquisition channel. List missing fields and continue only with analysis the data supports.
- Reconcile export revenue totals to the reported revenue for the quarter, within a tolerance I set before analysis begins. Report the gap and its cause. Do not build slides on unreconciled numbers.
- Confirm whether retention and acquisition spend by period is available inside existing tools. Without cost data, return-per-dollar comparisons are inputs I must supply. Label them as assumptions on the slide.

Analysis (work from customer-level records, not summary dashboards):
- Revenue bridge: decompose the quarter's change into new, expansion, contraction, and churned revenue. Compute gross and net revenue retention.
- Cohort analysis by start month and acquisition channel. Use survival curves (Kaplan-Meier) to show when customers leave, whether churn is concentrated early in life, and whether recent cohorts retain worse than older ones. That would mean acquisition is buying future churn.
- Unit economics per segment: lifetime value from the survival curves, CAC and payback where cost data exists.
- Test the belief the decision rests on: that retention and acquisition are separable options with comparable returns. Check whether churn is concentrated in identifiable, addressable segments, and whether acquisition volume and cohort quality move together. If the evidence says the framing is wrong, for example because the real lever is onboarding for new cohorts, say so on the recommendation slide.
- Causal caution (epidemiology): any claim that past retention efforts "worked" must address confounding. Customers who received attention may differ from those who did not. Label each claim as correlational or causal and give the basis.
- Decision analysis: model expected return for each option over the named horizon. Run a sensitivity (tornado) analysis on the key assumptions. State the single assumption whose plausible range flips the recommendation. State what the information that resolves it would be worth. A test that needs customer contact or a cadence change can appear only as a recommendation for leaders to decide, never as an action taken.
- Holdout: develop segment findings on data through the quarter before last. Confirm them on the last quarter, which was not used to find them. Mark any finding that fails, or that could not be checked, as unverified on its slide.

Red team: before the deck is final, someone from existing staff who did not do the analysis runs a pre-mortem ("leaders followed this recommendation and it failed a year later; why?"). They also run an Analysis of Competing Hypotheses against the main causal story. Address each surviving objection on a slide or in the appendix notes.

Deck structure (pyramid principle, answer first, at most 12 slides): slide 1 states the decision asked, the recommendation, and the flip condition. Each later slide carries one claim as its headline, with its supporting chart. Every number traces to a named query or calculation kept with the working files.

With my approval only: give the independent reviewer customer-level exports. Otherwise share only aggregated outputs.
With my approval only: request retention and acquisition spend data from any team or system I have not already granted access to.

Judge and pass conditions:
1. Reconciliation: export totals tie to reported revenue within my stated tolerance, or the gap is explained on the data slide.
2. Backtest: the churn and new-revenue figures modeled from data through the quarter before last are compared with actuals for the last quarter. Report the error. Holdout-confirmed findings are labeled confirmed; all others are labeled unverified.
3. Format: at most 12 slides. Every figure links to its source calculation.
4. Independent review: the red-team reviewer scores the deck on this rubric: decision stated, recommendation explicit, evidence traceable, flip condition named, causal claims labeled, objections addressed. The deck passes when every item passes or the reviewer's remaining objections are listed.
5. Cold read: a staff member who has not seen the analysis reads slide 1 and the headlines only. They can then state the decision, the recommendation, and what would reverse it.
Until checks 1 and 2 run on the shared exports, all quantitative results are unverified.
```

- `altitude`: The original outcome was a QBR deck about retention versus acquisition. The improved outcome is a deck that produces the decision: a recommendation, a flip condition, and the value of resolving the key uncertainty. It stays within 12 slides and the existing cadence. It needs my assumption about the investment unit and horizon confirmed.
- `depth`: The analysis works from customer-level exports, with reconciliation, a revenue bridge, survival-curve cohorts, LTV/CAC, and a holdout backtest. It also tests the decision's own framing. This takes more analyst time, inside existing staff and tools.
- `range`: Decision analysis (tornado sensitivity, value of information) shows which assumption actually decides the question. It adds no scope.
- `range`: Epidemiological confounding checks keep correlational retention claims from being presented as causal. No added scope.
- `range`: Intelligence-style red-teaming (pre-mortem, Analysis of Competing Hypotheses) by an uninvolved staff member exposes decision risk before the meeting. It costs that reviewer's time.
- `range`: The pyramid-principle structure puts the answer first so busy leaders can act on slide 1. No added scope.
- `approval`: Sharing raw customer data with the reviewer, and requesting spend data from new sources, are both gated behind your approval.
- Skipped: none. All three lenses had a permitted contribution.
- Owner actions:
  - Share the exports.
  - Set the reconciliation tolerance.
  - Confirm the investment unit and horizon.
  - Say whether spend data is accessible.
  - Name the independent reviewer and cold reader.
  - Decide on the two approval lines.
