# Rewritten prompt

```text
Prepare the quarterly business review deck for the leadership meeting about two weeks out (assumed on or near 2026-11-01; confirm the date and meeting length). Leaders will decide whether to invest in retention or acquisition. Build the deck so they can make that decision in the meeting and record why.

Fixed requirements (do not change):
- The deck is required and has at most 12 slides. Put supporting detail in speaker notes or a separate backup file, never in extra slides.
- Use only existing staff and tools.
- Do not change the operating cadence.
- Do not contact customers.
- The deck must be ready before the meeting date.

Assumptions (inferred, confirm with the owner):
- A1: The real goal is to put the next marginal investment where it returns the most durable revenue. "Pick a side" is not the goal.
- A2: "Retention or acquisition" may be a false binary. The evidence may support a split, or a targeted move in one segment.
- A3: Leaders want a recommendation with a decision rule, not a neutral survey.

STEP 0. Check dependencies before any analysis. Report each item as confirmed, missing, or partial.
- Raw customer and revenue exports: not yet shared. Do not start modeling until they arrive.
- Fields needed:
  - customer ID
  - start date
  - end or churn date
  - plan or segment
  - acquisition channel
  - revenue by period, including expansion and contraction
- Acquisition cost: sales and marketing spend by channel and period. Without it, CAC and payback cannot be computed. If spend is not in the exports, say so. Do not request it from Finance without owner approval.
- Tools: confirm which tools exist (spreadsheet, BI tool, SQL, Python/R). Build nothing that needs a new tool.
- Sensitive data: the exports likely contain customer PII.
  - Work on a de-identified copy.
  - Keep the data local.
  - Do not paste or upload it to any external service unless the owner clears that.
- Mark every conclusion that depends on missing data as UNVERIFIED in the deck.

STEP 1. Go back to raw evidence. Do not start from summary dashboards.
- Reconcile the exports to booked revenue for each quarter. Report the variance, and explain any gap above 1%.
- Build a revenue bridge for each quarter: starting revenue + new + expansion − contraction − churn = ending revenue. This shows which lever actually moved the number.
- Build cohort retention by acquisition quarter, channel, and segment:
  - Kaplan–Meier survival curves for logo retention.
  - Net revenue retention by cohort for dollar retention.
  - If the data supports it, a parametric survival model (e.g., shifted-beta-geometric) to project remaining customer lifetime.
- Compute unit economics by channel and segment: LTV, CAC, and payback months. Report each with an uncertainty range, not just a point estimate.

STEP 2. Test the premise. This is the core analytical move.
- Estimate the marginal return of the next $1 in retention against the next $1 in acquisition.
  - Retention: revenue at stake in the churning segments × a plausible range of churn-reduction effects. Take the effect range from internal history (past save efforts, segments that improved). Label any benchmark-derived range as an assumption.
  - Acquisition: recent-cohort LTV ÷ marginal CAC by channel. Check for diminishing returns as spend rose.
- Look for concentration. Find out whether churn or poor payback sits in specific segments or channels, because that would change the answer from "retention vs acquisition" to "fix X".
- Validate out of sample:
  - Find any segment pattern using all quarters except the most recent.
  - Then test whether it holds on the most recent quarter.
  - Present only patterns that hold out-of-sample as findings. Label everything else as a hypothesis.
- Separate correlation from cause. Churned customers may differ from retained ones for reasons retention spend cannot fix (selection effects). State this explicitly where it applies.

STEP 3. Structure the decision. Use decision analysis.
- State the options:
  - retention-weighted
  - acquisition-weighted
  - split or targeted, if the evidence supports it
- Give expected 12-month revenue impact and payback for each option, across low, base, and high scenarios.
- Add a tornado chart of the 3–5 assumptions that most swing the recommendation.
- State the decision rule as one sentence: "Choose retention if [metric] is above [threshold]; otherwise acquisition."
- State what evidence would reverse the recommendation.

STEP 4. Red-team the recommendation.
- Steelman the losing option. Write its strongest case on one slide or in notes.
- Run a key-assumptions check, as in intelligence analysis: list each load-bearing assumption, its evidence, and its confidence.
- Run a pre-mortem: "It's next QBR and this choice failed. Why?" Fold the top two risks into the deck.

STEP 5. Build the deck in at most 12 slides.
- Use answer-first structure (Minto pyramid / SCQA). Slide 1 states the recommendation, the key number, and the decision being asked for.
- Suggested flow:
  1. Decision ask and recommendation
  2. Quarter in one number and the revenue bridge
  3. Retention evidence: cohorts and NRR
  4. Acquisition evidence: LTV, CAC, payback by channel
  5. Where the problem concentrates
  6. Marginal-return comparison
  7. Scenarios and sensitivity
  8. Strongest counter-case and key risks
  9. Decision rule and what would change it
  10. Data caveats and UNVERIFIED items
  11–12. Reserve, or omit
- Every chart gets a one-line takeaway headline. Every number is traceable to its source query or sheet in the backup file.

APPROVAL GATES. Do these only with explicit owner approval:
- Requesting spend or CAC data from Finance or Marketing, or any other new data access.
- Asking existing staff for reviewer or dry-run time.
- Handing leaders a reusable model or workbook beyond the deck.
- Proposing a metric to check the decision at the next regularly scheduled QBR. This uses the existing cadence and does not change it.

JUDGE AND PASS CONDITION. Report each as passed, failed, or unverified. Include measured values even when a target is missed.
1. Reconciliation: export-derived quarterly revenue ties to booked revenue within 1%, or the gap is explained on the caveats slide.
2. Held-out backtest: fit the cohort and retention model on prior quarters, predict the most recent quarter's retained revenue, and report the error. Aim for within ±5% using the survival model; if it misses, try segment-level or parametric variants before reporting the miss. The deck passes on a stated, honest error, not on hitting 5%.
3. Out-of-sample check: each segment finding presented as a finding held on the held-out quarter. The rest are labeled hypotheses.
4. Independent review, if approved: an existing finance or analytics colleague scores the deck against this rubric:
   - numbers trace to source
   - recommendation follows from evidence
   - counter-case is fair
   - caveats are visible
5. Dry run, if approved: a colleague who did not build the deck reads it in 10 minutes. They can then state the recommendation, the key number, and what would change the decision.

The deck passes when all of the following hold:
- It has at most 12 slides and is delivered before the meeting.
- Checks 1–3 are reported.
- Every finding is labeled observed or proposed.
- The recommendation includes a decision rule and its reversal condition.
Checks 4–5 stay unverified until approved and run.
```

# Ledger

- **`altitude`**: Original task: prepare the QBR deck. Chosen outcome: leaders choose where the next investment dollar goes, using a stated decision rule and reversal condition. The deck is built as a decision instrument, not a quarterly summary. No scope change; a follow-up metric at the next existing QBR is gated.
- **`depth`**: Analysis rebuilt from the raw exports, with reconciliation to booked revenue, revenue bridge, cohort survival (Kaplan–Meier, sBG), and NRR. This replaces dashboard summaries with checkable evidence. It needs a de-identified local copy of the data.
- **`depth`**: Premise test: compare the marginal return of retention and acquisition spend, and look for concentration in segments or channels. This may turn the binary into a targeted answer. Findings must hold on a held-out quarter, which separates real patterns from overfit ones.
- **`depth`**: Stretch target: backtest error within ±5%, with fallback model variants. The honest reported error remains the pass bar.
- **`range`**: Decision analysis (scenarios, tornado chart, decision rule) lets leaders decide under uncertainty in one meeting.
- **`range`**: Epidemiology and causal reasoning flag selection effects, so churn correlates aren't sold as fixable causes.
- **`range`**: Intelligence-analysis key-assumptions check, steelman, and pre-mortem red-team the recommendation before leaders do.
- **`range`**: Minto/SCQA answer-first structure fits the 12-slide limit and busy readers.
- **Skipped:** none. All three lenses fit, because this deck drives a consequential decision and must persuade.

**Your open actions:**
1. Share the exports. I can't start modeling until they arrive.
2. Confirm whether sales and marketing spend by channel is in the exports. Without it, CAC and payback are unverified, and the acquisition side is the weaker half of the comparison.
3. Confirm the meeting date and length, and which tools are available.
4. Clear PII handling, specifically whether the data may only stay local.
5. Approve or decline the gated items:
   - requesting spend data from Finance or Marketing
   - reviewer and dry-run time from staff
   - a reusable model handoff
   - a check-in metric at the next scheduled QBR
