```text
Draft this week's report on recurring checkout failures so the team can choose what to fix. The report exists to drive one decision: which failure causes to fix next. Make it decision-ready: a short ranked list of fix candidates, each with its evidence, expected impact, and confidence.

Hard limits (unchanged from the owner):
- Inspect only the redacted incident notes the owner provides. Use no other source.
- Do not access production, change checkout code, create accounts, send messages, or change incident-response policy.
- If you think the team should go beyond the report, put that in a separate proposal that needs the owner's approval. Do not act on it.
- Deliver the report as a draft to the owner. Do not send or publish it.

Assumptions (inferred, not stated by the owner):
- The readers are engineers and a lead who will pick fixes in one meeting.
- "Recurring" means the same underlying cause, not only the same symptom ("checkout failed").

First checks. Report these before analysis and treat any gap as a limitation:
1. List the notes received, their date range, and whether they cover earlier weeks as well as this one.
2. List which fields the notes contain: timestamps, duration, user or order impact, detection method, suspected cause, remediation. Analysis that needs a missing field is "unverified" for that dimension.
3. Check whether redaction has hidden details that could make different incidents look alike, such as several different services all shown as "[REDACTED]". Do not try to reconstruct redacted content. If you find content that looks unredacted and sensitive, do not quote it, and flag it to the owner by note ID.

Method:
1. Case definition. Write one explicit definition of a "checkout failure incident" and apply it to every note, so counts are comparable. Record which notes are included and excluded, and why.
2. Coding from raw notes. Code each note directly; do not rely on any summary. Separate the symptom, the trigger, contributing factors, and the detection method. Build a small codebook (cause category and definition) from the notes. Allow an "unclassified" bucket, and do not force notes into clusters.
3. Recurrence and frequency.
   - Group incidents by cause and build a Pareto table: count, total duration, and impact where known.
   - Show an epi-curve-style timeline per cause.
   - Give the time between recurrences for each cause.
   - Only call a trend "rising" if the counts support it. With small counts, show the raw numbers and say a trend cannot be concluded.
4. Prioritization (FMEA-style).
   - Score each cause cluster on severity, occurrence, and detectability, using only what the notes show. Explain each score with note IDs.
   - Rank the clusters, then add a decision table: candidate fix, which incidents it would have prevented, rough effort if the notes indicate it (otherwise "unknown"), and confidence.
5. Red team the top three causes.
   - For each one, state the strongest alternative explanation and what evidence in the notes supports or weakens it.
   - Name reporting bias: the notes cover only incidents that someone wrote up, and silent or short failures may be missing.
6. Keep observed evidence (quoted or cited by note ID) visibly separate from inference and proposals throughout.

Stretch target: aim for named cause clusters that account for at least 80% of included incidents, each backed by at least two notes. If that stalls, try the next approach before reporting a miss: split the clusters by contributing factor instead of symptom, or merge clusters whose remediation would be the same. Report the coverage you actually reached, including a miss. A forced fit is a failure; an honest unclassified bucket is not.

Report format, in this order:
- One-paragraph summary.
- Ranked fix candidates with confidence.
- Evidence tables (Pareto table and timeline).
- Red-team notes.
- Data limitations, including the first-check results.
- Codebook as an appendix.
- Every factual claim cites note IDs.

Separate proposal, only if warranted, and clearly marked "needs owner approval". Examples: a recurring weekly version of this analysis, or fields worth adding to future incident notes. Present any note-template idea as a suggestion for the owner to take to whoever owns incident-response policy, not as a policy change.

Judge and pass condition:
- Traceability. Every claim in the report cites at least one note ID, and a spot check of 10 claims (or all claims, if fewer) finds each one supported by the cited note.
- Coding reliability. Re-code a blind sample of at least 20% of the notes (minimum 5) from the codebook alone, without looking at the first coding. Report the agreement rate on cause cluster. Below 80% agreement, revise the codebook and repeat, and report both rates.
- Held-out check, if the notes span more than one week. Build the clusters and ranking from earlier weeks only, then report how many of this week's incidents fall into the predicted top clusters. If the notes cover only one week, mark this check "not possible".
- Decision readiness. Provide a 4-question rubric for the owner or a reviewer they choose:
  1. Can I name the top fix and why?
  2. Do I know how confident to be?
  3. Do I know what the evidence cannot show?
  4. Could I defend the ranking to a skeptic?
  The report passes when the reviewer answers yes to all four. Until a human applies the rubric, mark this check "unverified".
```

**Ledger**

- `altitude`: The task moves from "a weekly report about recurring failures" to "a decision-ready ranking of what to fix." This serves the owner's stated purpose, and the held-out week checks it. The scope stays the same, and anything further goes into the separate proposal.
- `depth`: Each note is coded directly from the raw text, with a case definition, a codebook, and a symptom/trigger/contributing-factor split. This avoids counting different causes as one "recurring" failure. No access change.
- `depth`: The prompt tests the belief the task rests on: that apparent recurrences share a cause rather than only a symptom.
- `depth`: The stretch target is 80% cluster coverage with two notes per cluster. An unclassified bucket is allowed, and a miss is reported. This raises rigor without inviting forced fits.
- `range`: FMEA (severity × occurrence × detectability) from reliability engineering turns frequency counts into a fix priority.
- `range`: Epidemiology's case definition and epi curve make counts comparable and stop small-number trends from being overclaimed.
- `range`: Qualitative research's blind re-coding agreement measures whether the clusters are reproducible or just one reading of the notes.
- `range`: A red-team pass on the top three causes, with alternative explanations and reporting bias, exposes the decision risk before the team commits effort.
- Skipped: none. All three lenses fit, because this report drives a team decision and has to hold up in a meeting.
- Owner actions:
  - Provide the notes and say whether earlier weeks are included. The held-out check depends on this.
  - Confirm the redaction is cleared for analysis.
  - Name a reviewer for the rubric, or apply it yourself.
  - Decide on any separate proposal.
