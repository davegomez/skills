```text
Draft this week's report on recurring checkout failures so our team can choose what to fix. Write it as a decision memo: a short ranked list of fix candidates, each with the evidence behind it, how sure we are, and what the team gives up by not fixing it. The supporting analysis goes underneath.
Assumption: the team will read this in one meeting and pick one to three fixes. Rank candidates by impact as the notes describe it, not by how often each failure was mentioned.
Assumption: "recurring" means the same underlying cause showing up in more than one incident. A repeated symptom is not enough. Test this rather than accept the labels in the notes.

Scope and limits:
- Inspect only the redacted incident notes I provide.
- Do not access production, change checkout code, create accounts, send messages, or change incident-response policy.
- If you think we should go beyond the report, put that in a separate proposal document that needs my approval. Keep it out of the report.

First checks, before any analysis:
1. Count the notes and state the date range they cover.
2. List which fields survived redaction: timestamps, checkout stage, error codes, payment provider, duration, customer impact, resolution, root-cause statement.
3. Say which analyses below the redactions block or weaken. Continue only with what the notes support.
4. There is no traffic or order-volume data. Report counts and durations, never failure rates.

Method:
1. Write case definitions first. Before counting anything, write a one-line definition for each failure cluster that states what qualifies and what is excluded. This is borrowed from outbreak investigation, where counts mean nothing without a fixed case definition. It keeps the counts consistent and exposes incidents that only look alike.
2. Code each note with one codebook:
   - checkout stage (cart, address, shipping, payment authorization, order confirmation, other)
   - symptom
   - stated or inferred cause
   - trigger
   - how it was detected
   - duration
   - customer impact
   - resolution
   - whether the fix was permanent or a workaround
   Cite note IDs for every coded value. Mark each value as "observed" (stated in the note) or "inferred" (your reading).
3. Test the recurrence belief. For each cluster, check from the raw note text whether the incidents share a cause or only a symptom. Split clusters that mix causes, and merge separate labels that share a cause. Report every split and merge with note IDs.
4. Do a Pareto analysis. Rank clusters by incident count and by total impact (duration and described customer effect). Show where the two rankings disagree.
5. Do a reliability-engineering risk score (FMEA style). Score each cluster from the notes on:
   - severity
   - occurrence
   - detection (did customers or monitoring find it first)
   Use a stated 1–5 scale and mark any score the notes cannot support as "unknown". Never guess a score.
6. For the top two candidates, red-team the cause.
   - Use Analysis of Competing Hypotheses: list rival explanations and mark which note evidence is consistent or inconsistent with each.
   - Run a pre-mortem: "If we fix this and the failures continue, the likeliest reason is ___."
   - State what evidence would change the ranking.
7. If notes from earlier weeks are among those provided, freeze the codebook and case definitions on the earlier notes first. Then apply them unchanged to the most recent week. Report how many recent incidents fit existing clusters and how many needed a new one. Label conclusions drawn only from development notes as such.

Report structure:
1. Decision summary (one page):
   - the ranked fix candidates
   - for each: the case definition, incident count and note IDs, impact, risk score, confidence (high/medium/low with the reason), and the cost of waiting another week as the notes describe it
2. What recurred and what didn't, including the split/merge results.
3. Evidence gaps caused by redaction or missing fields, and how each one limits the ranking.
4. Appendix: the coded note table and the codebook.

Separate proposal document, only if you recommend going beyond the report. It needs my approval, and nothing in it is acted on without that approval.
With my approval only: list next steps the team could take, such as deeper investigation of a top candidate, or additional evidence the team could choose to supply in future redacted notes. For each, give the question it would answer and which ranking it could change.
With my approval only: reuse this codebook and these case definitions for next week's report, so that week-over-week counts are comparable.

Judge: a checkout or on-call engineer on the team, other than the author, reviews the draft against this rubric:
(a) Every count, score, and claim cites note IDs.
(b) Every cluster has a written case definition, and its incidents meet it.
(c) Values are labeled observed or inferred, and no rates appear.
(d) Recurrence claims survive the reviewer's own reading of the cited notes.
(e) The ranking criteria are stated, and the top candidates include competing hypotheses and a pre-mortem.
(f) Redaction gaps are named alongside the conclusions they weaken.
(g) Any beyond-report recommendation appears only in the separate proposal.
The reviewer also re-codes 5 randomly chosen notes with the codebook and compares results with the draft.
Pass only if every criterion is met and the re-coding agrees on checkout stage and cluster for at least 4 of the 5 notes. Until the review runs, mark the report "unverified draft".
```

- `altitude`: The original outcome was a weekly report about failures. The improved outcome is a decision memo with ranked fix candidates, confidence levels, and the cost of waiting, so the meeting can choose a fix rather than re-read incidents. It stays within the report scope.
- `depth`: Coding each note against a codebook, labeling values observed vs inferred, and citing note IDs makes the report traceable to raw notes instead of summaries. Cost: more drafting time.
- `depth`: The report tests whether "recurring" incidents share a cause, not only a symptom. This guards against funding a fix that addresses only one of several causes.
- `depth`: Pareto by count and by impact shows when the most frequent failure is not the most costly one.
- `depth`: If earlier weeks' notes are provided, the codebook is frozen on them and checked on the newest week. This separates development evidence from confirmation. It depends on what notes you supply.
- `range`: Case definitions from outbreak investigation keep cluster counts consistent.
- `range`: FMEA-style severity, occurrence, and detection scores give an explicit, contestable ranking. Unknowns stay unscored.
- `range` (red-team): Competing hypotheses and a pre-mortem on the top two candidates expose ranking risk before the team commits.
- `range`: Asking "what evidence would change the ranking" feeds the separate proposal only, behind your approval.
- Judge: an engineer other than the author applies the rubric and re-codes 5 notes. This adds a small review cost to the team.
- Skipped: none. All three lenses had a permitted contribution inside the notes-only boundary.
- Owner actions:
  - Supply the redacted notes, ideally with earlier weeks included for the hold-out check.
  - Name the reviewing engineer.
  - Decide on the proposal items and on reusing the codebook week to week.
