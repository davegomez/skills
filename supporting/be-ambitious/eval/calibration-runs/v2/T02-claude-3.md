```text
Goal: Prepare the quarterly business review deck that lets leadership decide, at the meeting in two weeks (on or near 2026-11-01), whether to invest next in retention or in acquisition. The deck should state a recommendation, the evidence for it, the main uncertainty, and the result that would reverse it.

Requirements (do not change):
- The deck is required and has at most 12 slides. Backup slides and appendices count toward the 12.
- Deliver it in time for the leadership meeting in two weeks.
- Build it from the raw customer and revenue exports the owner provides.
- Use only existing staff and tools.
- Do not change the operating cadence. Add no new recurring meetings or reports.
- Do not contact customers. No surveys, interviews, or outreach.

Assumptions to confirm with the owner:
- (A1) The business has recurring or repeat revenue, so retention and churn can be measured per customer over time.
- (A2) Leadership is choosing where the next increment of investment goes. The size of that budget is unknown; ask for it.
- (A3) Finance's reported quarterly revenue is the source of truth for reconciliation.

First checks. Report each as confirmed or missing before any analysis:
1. Exports received. They have not been shared yet. List the fields actually present: customer ID, start and end or churn dates, revenue by period, segment, plan, and acquisition channel or date.
2. Spend data. Acquisition spend (marketing and sales) and retention spend (customer success, support) are probably not in these exports. Without spend data, CAC, payback, and return per dollar cannot be computed. In that case, report them as unverified and present break-even values instead. Example: "acquisition wins if blended CAC is below $X."
3. Tools. Identify the existing analysis tools, such as the spreadsheet, BI tool, SQL warehouse, or Python. Use nothing new without owner approval.
4. Data handling. The customer exports may contain personal data. Process them only in owner-approved, existing environments. Never upload them to external services.
5. Reconciliation. Export revenue totals per quarter should match reported revenue within 1%, or within a tolerance finance sets. If they do not, explain the gap before using the data.

Analysis. Start from customer-level records, not dashboards:
- Cohort analysis by acquisition quarter: gross and net revenue retention, and logo retention. Break it out by segment and by channel where the fields exist.
- Survival analysis: Kaplan-Meier churn curves by cohort and segment. Use them to estimate customer lifetime and lifetime value from observed retention instead of an average churn rate.
- Unit economics, when spend data exists: CAC by channel, payback months, LTV:CAC. Compare marginal returns, not averages. Ask what the next dollar buys in each option.
- Test the belief the question rests on. Decide whether retention and acquisition are really separate bets. Check two things:
  (a) Is churn concentrated in identifiable segments, cohorts, or tenure windows? Concentrated churn is addressable by retention investment. Diffuse churn is weak evidence for it.
  (b) Do recent acquisition cohorts retain worse than older ones? If so, more acquisition buys leakier revenue, and the two options interact.
  Report what the evidence shows, including "no difference."
- Holdout check. Fit the retention and revenue projections on data through two quarters ago. Predict last quarter, then compare to actuals. Report the error. Treat any pattern found during exploration as a proposed finding until it holds on that held-out quarter.
- Label claims as observed (measured in the data), modeled (projected), or associational (correlated, not shown to be causal). Observational exports cannot prove that a retention action causes retention.

Decision framing. Use decision analysis and capital-allocation methods:
- Model the expected revenue impact of a given investment in each option over 12 to 24 months, with low, base, and high ranges.
- Make a sensitivity (tornado) chart showing which assumptions move the answer most. State the break-even value at which the recommendation flips.
- State what would change the recommendation. Name the leading indicators to review at the next scheduled QBR. These go into the existing cadence, not a new one.

Red team:
- Have a designated skeptic from existing staff, or a separate pass by you, build the strongest case for the option you do not recommend. Include its best point on one slide.
- Run a premortem: "It is two quarters later and this choice failed. Why?" Fold the top two risks into the risk slide.

Story and format, at most 12 slides:
- Answer first, using the pyramid principle. Slide 1 holds the decision requested, the recommendation, and the one number that matters most.
- Each slide title is a full-sentence claim, with one message per slide. Every number traces to a named query or worksheet tab.
- Suggested spine: decision and recommendation; quarter at a glance; revenue bridge (new, expansion, contraction, churn); cohort retention; churn concentration; unit economics or break-evens; the two options modeled; sensitivity and flip point; case for the other option; risks from the premortem; what we will watch at the next QBR; the ask.
- Keep supporting work as working files, not slides: queries, the workbook, and the methods note.
- With owner approval only: a 2-page written pre-read sent ahead of the meeting.

Judge. Report each item. Missing inputs leave the related claims unverified:
1. Slide count is 12 or fewer.
2. Revenue reconciles to reported figures within tolerance, or the gap is explained on the record.
3. Holdout projection error for last quarter is reported. Any finding presented as established holds on the held-out quarter.
4. The sensitivity analysis names the flip assumption and its break-even value.
5. Cold-read test. Two existing staff who did not build the deck (one from finance) read it. Each answers without help:
   (a) What decision is being asked?
   (b) What is recommended?
   (c) What is the biggest uncertainty?
   (d) What result would reverse it?
   (e) Pick any 3 numbers and trace each to its source.
Pass condition: items 1 to 4 are met or explicitly reported as unverified with the reason, and both readers answer all of (a) to (e) correctly. Report the reader answers verbatim, along with any item that failed.
```

**Ledger**

- `altitude`: Moves from "prepare the QBR deck" to "leadership makes a reasoned retention-vs-acquisition decision": recommendation, flip point, and indicators for the next QBR. Adds no scope beyond the deck and working files. A live experiment or pilot would be a higher rung, but it was excluded because it would change cadence or touch customers.
- `depth`: Uses customer-level cohort and survival analysis and marginal unit economics instead of summary tables. This gives lifetime value and payback grounded in observed retention. CAC and payback depend on spend data that may not be in the exports.
- `depth`: Tests the premise that retention and acquisition are independent options, using churn concentration and cohort-quality trends. It can reframe the decision; no added cost.
- `depth`: Revenue reconciliation, a held-out-quarter backtest, and observed/modeled/associational labels keep proposed findings separate from evidence.
- `range`: Decision analysis (scenario ranges, tornado chart, break-even) shows leaders which assumption the choice actually hinges on.
- `range`: Red team (strongest case for the other option, premortem) exposes decision risk before the meeting. It costs a few hours of one existing staff member.
- `range`: Pyramid-principle structure with claim titles, plus a cold-read test with two staff, checks that the story lands. It costs about an hour of two people's time.
- Skipped lenses: none. All three fit, because the deck exists to drive a contested investment decision that must land with busy leaders.

**Owner actions**

- Share the customer and revenue exports.
- Provide acquisition and retention spend data, or accept break-even framing instead.
- Name the approved analysis tools and environment for customer data.
- Confirm finance's reported revenue and the reconciliation tolerance.
- Confirm assumptions A1–A3, including the investment size.
- Name two cold-read reviewers and a skeptic from existing staff.
- Approve or decline the optional pre-read memo.
