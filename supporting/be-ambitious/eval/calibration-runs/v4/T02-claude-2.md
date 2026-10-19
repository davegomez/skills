```text
Prepare the quarterly business review deck for our leadership meeting in two weeks. The deck is required and must be at most 12 slides. Its purpose is to help leaders decide whether to invest in retention or acquisition. Assumption: leaders need a clear recommendation, how confident we are, and what would change the answer, not just a description of last quarter. Use existing staff and tools only. Do not change our operating cadence. Do not contact customers.

First checks (before analysis):
- Receive the raw customer and revenue exports. Record each export's fields, date range, row counts, and grain (customer, invoice, or month).
- Confirm the exports include, or can be joined on, the following: customer ID, start date, end or churn date, revenue by period, segment or plan, and acquisition channel.
- Confirm whether acquisition spend or CAC data exists in tools we already have. If it does not, say so on the slides and present acquisition economics as a range built from stated assumptions, not as a measured figure.
- Confirm there are enough past quarters to hold the most recent quarter out for validation.
- Confirm which existing tools are available for the analysis (spreadsheet, BI, SQL, notebook) and which existing staff can review the deck.
- Name any missing dependency and continue only with work the available data supports.

Analysis (from the raw exports, not from summary reports):
- Reconcile revenue totals to the finance-reported figures for each quarter before using them.
- Build cohort retention by start quarter: logo retention, gross revenue retention (GRR), and net revenue retention (NRR).
- Break revenue change into new, expansion, contraction, and churn. This shows which lever actually moved revenue.
- Run survival analysis (Kaplan-Meier curves by segment and by channel) to find when and where churn concentrates.
- Estimate lifetime value by segment and channel. Where spend data exists, compare it with CAC and payback period.
- Compare the two options at the margin: the expected revenue from the next unit of retention investment versus the next unit of acquisition investment, each as a range with stated assumptions. Treat a blend of the two as a legitimate answer if the data supports it.
- Holdout validation: develop segment and churn findings on earlier quarters, then check them against the most recent quarter, which was not used to find them. Label any finding that fails or cannot be tested as unverified.
- Label drivers of churn as associations, not causes, unless the data supports a causal claim. For the main churn-driver claim, use Analysis of Competing Hypotheses: list rival explanations and the evidence that separates them.

Decision framing (decision analysis):
- State the decision rule before showing the recommendation. For example: "invest in retention if the marginal NRR gain exceeds the marginal new-revenue gain from acquisition at equal spend."
- Show a sensitivity (tornado) chart of the 3–5 assumptions that most affect the answer.
- State what evidence would flip the recommendation.
- Identify the single uncertainty most worth resolving next. Propose how it could be measured later without contacting customers or changing operating cadence.

Deck construction (12 slides maximum, all included):
- Lead with the answer (Minto pyramid).
- Write each slide title as an assertion that the slide's evidence supports.
- Give one decision-relevant chart per slide.
- Keep methods detail and backup analyses in working files, outside the deck.

Red team:
- Before review, write the strongest case for the option the deck does not recommend.
- Run a pre-mortem: "the decision was wrong a year later; why?"
- Answer each serious objection on a slide, or list it as an open risk.

With my approval only: share customer-level export data with any reviewer or staff member beyond those I name.
With my approval only: pull additional data sources (marketing spend, CRM, product usage) that require new access.
With my approval only: distribute the backup working files or a methods appendix outside the deck.

Judge, with pass conditions:
1. Reconciliation: revenue in the analysis ties to finance-reported totals within a tolerance I confirm. Any gap is explained in writing.
2. Holdout: each segment or churn finding shown in the deck is reported with its development-period result and its held-out-quarter result. A finding passes if the direction holds and the size falls within the stated range. Others are marked unverified on the slide.
3. Cold read: an existing staff member who did not build the deck reads it within a fixed time limit. Without help, they must correctly state the recommendation, the two or three numbers it rests on, and what would flip it.
4. Red-team review: a second existing staff member argues the opposite option. Every objection they raise is either answered in the deck or listed as an open risk.
5. Format: the deck has 12 or fewer slides and is ready early enough before the meeting in two weeks to allow one revision after review.

Results that have not passed these checks stay marked unverified.
```

**Ledger**

- `altitude`: The original outcome was a QBR deck about last quarter. The improved outcome is a deck that drives the retention-vs-acquisition decision, with a stated decision rule, sensitivities, and the conditions that would flip it. It stays within 12 slides, existing staff, and no customer contact. The cold-read judge checks whether it works.
- `depth`: The analysis starts from raw exports and reconciles them to finance figures, then adds cohort GRR/NRR, a revenue decomposition, survival curves, and LTV/CAC compared at the margin. This replaces descriptive summaries with a comparison of where the next dollar earns most. It adds analyst time but no new tools.
- `depth`: Holdout validation on the most recent quarter means the headline findings are confirmed on data not used to find them. Findings that fail are shown as unverified, which may reduce how much the deck can confidently claim.
- `range`: Decision analysis (decision rule, tornado chart, choosing the next thing to measure) makes the uncertainty explicit, so leaders decide on ranges instead of point estimates.
- `range`: Analysis of Competing Hypotheses for churn drivers keeps associations from being presented as causes.
- `range`: Minto pyramid structure and assertion-style titles make the deck readable within a leadership meeting.
- `range` (red team): The opposite-case brief, the pre-mortem, and the red-team reviewer expose decision risk before leaders see the deck. This takes time from one or two existing staff members.
- Approval-gated: sharing customer-level data with reviewers you haven't named, new data-source access, and distributing material outside the deck.
- Skipped lenses: none.
- Unresolved owner actions:
  - Share the raw customer and revenue exports.
  - Confirm whether acquisition spend or CAC data exists.
  - Set the reconciliation tolerance.
  - Name the cold-read and red-team reviewers from existing staff, and approve their access to customer-level data if needed.
  - Decide on the three approval-gated items.
