```text
Goal: Prepare the quarterly business review deck for our leadership meeting in two weeks so leaders can decide, in the meeting, whether to invest in retention or acquisition. The deck should show which choice returns more per dollar, how confident we are, and what evidence would change the answer.

Fixed requirements:
- The deck is required and must be at most 12 slides. Supporting analysis goes in a separate methods document or notebook, not in extra slides.
- Build every number from the raw customer and revenue exports the owner will provide, not from summary dashboards.
- Use existing staff and tools only. Keep customer data inside those tools.
- Do not change our operating cadence.
- Do not contact customers. That rules out surveys, interviews, outreach, and any test that touches customers.

Assumption: leaders want a recommendation backed by a decision rule, not only a description of the quarter.
Assumption: the decision is about where the next marginal investment goes. If the evidence supports a split, present it as a variant of the retention-or-acquisition answer, not as a replacement for the question.

First checks, before any analysis:
1. Receive the exports and list the fields present: customer ID, start and end dates, revenue by period, plan or segment, acquisition channel, downgrades and cancellations, and gross margin. Name each missing field and what its absence prevents.
2. Reconcile the export revenue totals to reported revenue for each period. Report any unexplained gap before building slides.
3. Check whether acquisition cost (sales and marketing spend by period or channel) is in the exports. If it is not, CAC and payback stay out of the deck's conclusions and appear as a named gap.
4. Confirm which existing tools support reproducible analysis (a spreadsheet with saved formulas, a BI tool, SQL, or a notebook). Confirm which existing staff can act as the independent reviewer and the red-team colleague.

Analysis:
- Revenue bridge: split each period's recurring-revenue change into new, expansion, contraction, and churn. This shows which lever actually moved revenue.
- Cohort retention: build logo and revenue retention curves by acquisition cohort, and by segment or channel if those fields exist. Report gross and net revenue retention.
- Survival analysis: draw Kaplan-Meier time-to-churn curves by segment. If the data supports it, fit a Cox proportional-hazards model to rank churn drivers. Label drivers as associations, not causes.
- Unit economics: estimate lifetime value from cohort retention, using margin if it is available and revenue otherwise. Add CAC and payback only if spend data exists.
- Marginal comparison: for the same spend, compare the revenue over a stated horizon from (a) cutting churn by a stated number of points and (b) adding customers at the observed CAC. Use a decision-analysis tornado chart on churn, CAC, expansion, and cohort quality to show which assumptions would flip the recommendation.
- Belief test: the question assumes one lever clearly returns more, so test that.
  - Fit the retention and acquisition-yield estimates on all periods except the most recent quarter, predict that quarter, and report the prediction error.
  - Treat any pattern found in the development periods (for example, churn concentrated in one cohort or channel) as a finding only if it holds on the held-out quarter. Otherwise label it unverified.
- Competing hypotheses: list rival explanations for this quarter's revenue movement, such as a churn spike, weak new cohorts, pricing, seasonality, or one large account. Score each against the evidence so the deck's story is the best-supported one, not the first one found.

Deck structure, at most 12 slides:
- Lead with the decision asked and the recommendation (answer first, pyramid principle).
- Follow with the revenue bridge, cohort retention, and the marginal-return comparison with its sensitivity.
- Show the risks and the specific evidence that would change the recommendation.
- Close with what to measure at the next regularly scheduled QBR, within the existing cadence.
- Give each slide one message and state it in the slide title.

Red team, using existing staff, before the meeting:
- A colleague who did not build the analysis argues for the opposite recommendation.
- The team runs a pre-mortem: "Two quarters from now this choice has failed. Why?"
- Record every objection. The deck either answers each of the strongest ones or names it as an open risk.

With my approval only: request acquisition spend data from finance if it is not in the exports.

Judge and pass conditions:
- Mechanical: the deck has at most 12 slides. Every figure traces to a saved formula, query, or notebook cell run on the raw exports. Export totals reconcile to reported revenue for each period, or the methods document explains each gap.
- Backtest: the held-out-quarter prediction error is reported, and any finding that failed the backtest is marked unverified in the deck.
- Independent review: a dry run timed to the meeting's allotted slot, with a reviewer from existing staff who did not build the deck. Using a written rubric, the reviewer must state unaided:
  (1) the decision asked
  (2) the recommendation
  (3) the two strongest pieces of evidence
  (4) the assumption that would flip the recommendation
  (5) the confidence level
- Pass: all five rubric items are stated correctly, and every red-team objection is answered or listed as an open risk.
- Until these checks run, present the recommendation as unverified.
```

**Ledger**

- `altitude`: The original outcome was a QBR deck. The improved outcome is a deck that settles the retention-vs-acquisition decision in the meeting, with a per-dollar comparison, a confidence level, and stated flip conditions. Scope, the slide cap, and the cadence are unchanged.
- `depth`: The analysis is built from raw exports, using a revenue bridge, cohort retention curves, Kaplan-Meier and Cox survival analysis, and LTV/CAC. Every number becomes reproducible and is reconciled to reported revenue. This needs a reproducible tool, which is checked first.
- `depth`: The belief test holds out the most recent quarter. This tests whether one lever really dominates, and it stops patterns found while exploring from being presented as findings. If history is short, the backtest may be weak.
- `range`: Decision analysis contributes the marginal comparison and tornado sensitivity. Leaders see which assumption flips the answer, not just a point estimate.
- `range`: Intelligence analysis contributes competing hypotheses. Rival explanations for the quarter, such as one large account or seasonality, are scored before the story is chosen.
- `range`: Red team and pre-mortem test the recommendation against its strongest counter-case using existing staff. This takes about one colleague-session of time.
- `range`: Communication craft contributes the answer-first pyramid, one message per slide, and a timed dry run with a rubric. The deck stays within 12 slides and is checked by someone other than its author.
- Skipped lenses: none. Customer-facing pilots and new recurring dashboards were left out entirely because you prohibited customer contact and cadence changes.
- Owner actions:
  - Share the raw customer and revenue exports.
  - Confirm the reported revenue figures to reconcile against.
  - Say whether margin and acquisition spend are in the exports, or approve the finance request.
  - Name the existing tool for the analysis.
  - Name an independent reviewer and a red-team colleague.
  - Confirm the length of the meeting slot for the dry run.
