```text
Prepare the quarterly business review deck for our leadership meeting in two weeks. Build it so leaders leave the meeting having decided whether to invest in retention or acquisition, with the evidence, the decision rule, and the assumptions that would change it. The deck is required and must be at most 12 slides, including any title, appendix, or backup slides. Use existing staff and tools. Do not change our operating cadence. Do not contact customers.

Assumption: the goal is a sound, defensible decision, not only a status report. The deck should answer first ("we recommend X because Y"), and every slide should support or stress-test that answer.
Assumption: leaders need to know which choice returns more per marginal dollar, how confident we are, and what would prove us wrong.

First checks (dependencies):
- I will provide the raw customer and revenue exports. Confirm they arrived, then document their fields, date coverage, grain (customer, subscription, invoice), and known gaps.
- Check whether the exports contain what each side of the comparison needs. Retention economics need customer start and end dates and revenue over time. Acquisition economics need spend or cost per acquired customer. If acquisition cost data is missing, say so on the relevant slide and present that side as a dependency. Do not estimate it from assumptions without labeling it.
- Confirm which existing analysis tools are available, such as a spreadsheet, SQL database, or notebook environment.
- Confirm which colleague can serve as the independent reviewer before the meeting.
- Name any missing dependency and continue only with work the available data supports.

Analysis (from raw exports, not existing summaries):
- Reconcile first. Rebuild quarterly revenue from the raw exports and reconcile it to the revenue figure leadership already sees. Document every difference before any analysis builds on it.
- Decompose revenue movement. Split this quarter's revenue movement into new, expansion, contraction, and churned revenue. This shows where growth was won and lost, and gives leaders the size of each lever in revenue terms.
- Build cohort retention curves. Group customers by start period and estimate customer and revenue survival with Kaplan–Meier curves. This handles customers still active, whom a simple churn rate miscounts. Break the curves out by segments present in the data, such as plan, size, or channel, to find where churn concentrates.
- Estimate customer lifetime value from the survival curves, with bootstrap confidence intervals, so the deck shows a range rather than a single number. If acquisition cost data exists, compute CAC payback and LTV:CAC by segment and cohort.
- Test the belief the task rests on. Check from the raw cohorts whether retention and acquisition are separable choices. For example, check whether recent acquisition cohorts retain worse than older ones, which would mean acquisition spend is buying low-retention customers. Also check whether churn is concentrated enough that a targeted retention effort is plausible. Report what the data shows, including if it undercuts the either/or framing.
- Validate projections out of time. Fit the retention and LTV projections on cohorts before a cutoff date. Then compare predictions with the observed retention of later cohorts and report the error. Patterns found while exploring are development evidence. Confirm any headline finding on cohorts or periods not used to find it, or label it unverified on the slide.
- Label evidence by type. Mark which claims are observed in the data and which are correlational or projected. Historical exports cannot show that retention spending causes retention, so the deck must not imply that it does.

Decision framing (decision analysis):
- Present each option's expected return per marginal dollar as a range, using the LTV and payback results.
- Show a tornado sensitivity chart: which single assumption, moved across its plausible range, flips the recommendation. This tells leaders where disagreement actually matters.
- State the decision rule in one line, for example: "Invest in retention unless [metric] exceeds [threshold]."
- Propose the metrics that would show whether the chosen investment is working. These should be reviewable inside the existing review cadence.

Stress test (red team, using existing staff):
- Run an analysis of competing hypotheses on the main revenue story. List the alternative explanations, such as seasonality, pricing changes, a single large account, or data artifacts. Show which explanations the evidence rules out and which it does not.
- Run a pre-mortem: "It's next year and this decision was wrong. Why?" Put the strongest surviving objection on a slide with our response.

Communication (information design):
- Write slide titles as full-sentence claims, so that reading only the titles tells the whole argument (pyramid principle: answer first, then supporting points).
- Use small multiples for cohort and segment comparisons, and keep one message per slide.
- Keep supporting calculations in a reproducible workbook or notebook built with existing tools. Do not add slides beyond the 12-slide limit.

With my approval only: request acquisition spend or cost data from any team or system I have not already provided, if the exports lack it.

Judge and pass conditions:
- Mechanical: the deck has 12 or fewer slides in total. Every number on a slide traces to a named query, formula, or notebook cell that runs on the raw exports and reproduces it. Reconstructed quarterly revenue matches the figure leadership already sees, or every difference is documented.
- Out-of-time backtest: report the projection error of the retention and LTV model on the held-out later cohorts. Any headline finding not confirmed on held-out data is labeled unverified on its slide.
- Independent review: before the meeting, the confirmed colleague, who did not build the deck, reads the slide titles only and then the full deck, and is scored on a rubric:
  (1) Can they state the recommendation and the decision rule?
  (2) Can they name the assumption that would flip it?
  (3) Can they tell which claims are observed and which are projected or correlational?
  (4) Did they find any number they could not trace to its source?
  Pass = yes, yes, yes, no.
- Report each result as met or missed. Any check that could not run, such as missing acquisition cost data or an unavailable reviewer, is reported as unverified, with the reason.
```

**Ledger**

- `altitude`: The original outcome was a QBR deck. The improved outcome is a deck built to produce a defensible retention-vs-acquisition decision, with a decision rule, the assumption that flips it, and success metrics that fit the current cadence. No scope or cadence change. The judge is the reviewer rubric.
- `depth`: The deck now starts from the raw exports instead of summaries. It adds revenue reconciliation, new/expansion/contraction/churn decomposition, Kaplan–Meier cohort curves, bootstrap LTV ranges, and CAC payback where data allows. This adds analyst time with existing tools.
- `depth`: Before recommending either option, the prompt tests whether retention and acquisition are separable at all, for example whether newer cohorts retain worse. It also checks whether churn is concentrated enough to target. This may undercut the either/or framing, and the deck is told to report that if so.
- `depth`: Projections are validated on held-out later cohorts, and findings from exploration are kept separate from confirmed ones. This lowers the risk of presenting a pattern found by searching as an established result.
- `range` (decision analysis): Expected value ranges, a tornado sensitivity chart, and an explicit decision rule. These focus leadership debate on the assumption that actually changes the answer.
- `range` (intelligence analysis / red team): Analysis of competing hypotheses and a pre-mortem expose alternative explanations and decision risk before leaders see the deck. This uses one existing colleague's time.
- `range` (information design): Claim-style titles, pyramid structure, and small multiples help busy readers get the argument from the titles alone. This works within the 12-slide limit.
- `approval`: Requesting acquisition cost data from teams or systems not yet provided is new data access, so it is gated behind approval.
- Skipped: the hard-target move, because this is a decision task, not a quantitative improvement request with a metric to stretch.
- Owner actions:
  - Share the customer and revenue exports.
  - Say whether acquisition spend or cost data exists and approve requesting it if needed.
  - Name an independent reviewer available before the meeting.
  - Confirm which revenue figure leadership already uses, so the reconciliation has a target.
