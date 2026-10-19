```text
Prepare the quarterly business review deck for our leadership meeting in two weeks. The deck exists so leaders can decide whether to invest in retention or acquisition, and so they can see what evidence that choice rests on. The deck is required and must be at most 12 slides. Use existing staff and tools. Do not change our operating cadence or contact customers.

Assumption: the decision is about where the next unit of investment produces more durable revenue. The deck should compare the two levers on that basis, not just report last quarter.
Assumption: leaders will decide in one meeting, so the deck leads with the recommendation and the decision rule, then shows the evidence.

First checks, before any analysis:
- Confirm I have shared the raw customer and revenue exports. Until I do, build only the deck skeleton and the analysis plan, and label every number as a placeholder.
- When the exports arrive, list their fields, date range, and grain (customer, invoice, month). Reconcile total revenue per quarter in the exports against the figure leadership already uses, and record any gap.
- Check whether the exports contain acquisition spend, retention spend, or customer-success cost. If they do not, say which comparisons can't be made: CAC, CAC payback, and the cost side of LTV:CAC. Show those comparisons as revenue-side only, clearly labeled.
- Confirm an independent reviewer from existing staff is available for the judge step below.

With my approval only: request acquisition and retention spend figures from finance staff if the exports lack them.

Analysis, from the raw exports rather than existing summary tables:
- Revenue bridge for the quarter and the trailing four quarters: starting revenue, new, expansion, contraction, churn, ending revenue. Report gross and net revenue retention.
- Cohort retention by acquisition quarter, using Kaplan-Meier survival curves for logos and revenue. These show when customers leave and whether newer cohorts retain worse than older ones. Cut by the segments the exports support, such as plan, size, channel, or region.
- Unit economics per segment: LTV from the survival curves and margin, if available. Add CAC and payback only where spend data exists.
- Test the belief the request rests on, that this is an either/or choice. For each segment, estimate the revenue effect of a plausible improvement in each lever: churn reduced by X points versus new customers increased by Y%. Put both on a common cost basis where spend data allows. Show the result as a sensitivity (tornado) chart. Say whether the answer differs by segment and whether a split allocation beats either pure option.
- Decision analysis: state the expected value and range of each option, the assumptions that most change the recommendation, and a decision rule fixed before the meeting. Example: "invest in retention if segment S's 12-month revenue retention is below Z." Name what further evidence would change the answer, so leaders know the value of waiting.
- Causal caution: churned and retained customers may differ for reasons a retention program can't change. Mark which links are measured correlations and which are assumed causal effects. Do not present a correlation as a lever's effect.
- Validation: fit the retention model on cohorts and periods through the prior quarter, then predict the most recent quarter. Report predicted versus actual churn and revenue retention. Any pattern found while exploring is development evidence. Confirm it on the held-out quarter, or label it unverified in the deck.

Deck structure, at most 12 slides including any appendix:
- Open with situation, complication, question, and answer: the recommendation in one sentence, the decision rule, and the confidence level.
- Then present the evidence, the segment view, the sensitivity chart, the risks, and what would change our minds.
- Close with one slide on methods and data limits, including the backtest result and the reconciliation gap.
- Give every chart a one-line takeaway headline. Put each number's source query or export field in the slide's speaker notes.

Red team: run a pre-mortem on the recommendation. Assume it failed a year from now and list the three likeliest reasons. Build the strongest case for the opposite option using the same data, and answer it on the risks slide.

Judge:
- Mechanical checks:
  - The deck has 12 or fewer slides.
  - Every revenue figure ties to the raw exports within the reconciliation tolerance stated on the methods slide.
  - The backtest's predicted-versus-actual error is reported on the methods slide.
  - Any metric that needs missing spend data is labeled as missing, not estimated silently.
- Independent review: a reviewer from existing staff, ideally from finance or analytics, who did not build the deck, reads it cold in the time the meeting allots. Rubric:
  1. Can state the recommendation and decision rule after one read.
  2. Every claim on a slide traces to a source in the notes.
  3. Correlation and causal claims are distinguished.
  4. The strongest counter-case is presented fairly.
  5. Uncertainty is shown as ranges, not point estimates.
  6. Any claim not confirmed on the held-out quarter is labeled unverified.
- Pass: all mechanical checks pass and the reviewer marks all six rubric items met. Report any unmet item as unmet rather than resolved. Until the exports arrive and the judge runs, the deck's findings stay unverified.
```

- `altitude`: the outcome moves from a QBR deck that reports the quarter to a decision-ready deck. It gives a recommendation, a pre-committed decision rule, and per-segment marginal returns for each lever. A held-out-quarter backtest and an independent reviewer judge it. No scope, cadence, or customer-contact change.
- `depth`: work starts from the raw exports instead of summary tables. It uses a revenue bridge, Kaplan-Meier cohort survival, segment LTV, and reconciliation to leadership's figures. It tests the either/or framing, since a split by segment may beat both pure options. It costs more analyst time with existing staff and tools.
- `depth`: findings from exploration are confirmed on a held-out quarter or labeled unverified. This lowers the risk of presenting overfit patterns to leaders.
- `range`: decision analysis adds expected value, sensitivity, a decision rule, and value of information, so leaders can decide under uncertainty.
- `range`: an epidemiology-style causal caution keeps retention correlations from being sold as lever effects.
- `range`: Minto-style situation-to-answer structure fits a busy-leader read inside 12 slides.
- `range` (red team): a pre-mortem plus a steelman of the opposite option exposes the main decision risk before the meeting.
- Access effect: requesting spend data from finance is behind approval. Without it, cost-side metrics are labeled missing.
- Skipped lenses: none. The hard-target move was skipped because this is a decision request, not a quantitative improvement target. A live pilot was excluded because it would change the operating cadence or involve customers.
- Owner actions:
  - Share the raw customer and revenue exports.
  - Confirm whether spend data exists, or approve the request to finance.
  - Name an independent reviewer from existing staff.
  - Confirm leadership's reference revenue figure for reconciliation.
