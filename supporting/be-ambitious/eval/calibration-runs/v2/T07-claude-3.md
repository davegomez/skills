## Rewritten prompt

```text
Draft this week's report on recurring checkout failures so the team can choose what to fix. The report should be strong enough that the team can make that choice in one meeting, and every claim in it should trace back to a specific incident note.

HARD LIMITS (unchanged from the owner)
- Inspect only the redacted incident notes the owner provides. Use no other source.
- Do not access production, change checkout code, create accounts, send messages, or change incident-response policy.
- The deliverable is a draft report returned to the owner. Do not distribute it.
- Anything beyond the report goes in a separate "Proposals (need owner approval)" section and is not carried out.
- Do not try to reverse redactions. If a note appears to contain unredacted sensitive data, stop using that passage, keep it out of the report, and flag it to the owner by note ID.

ASSUMPTIONS (inferred, not confirmed; state them in the report)
- A1: The goal behind the report is fewer checkout failures and less customer and revenue impact. The team ranks fixes by impact, recurrence, and effort.
- A2: The notes cover at least the current week. They may also cover earlier weeks, which would allow baselines and held-out checks.
- A3: The team, not this report, supplies fix-effort estimates.

FIRST CHECKS (report results before analysis)
1. List the notes received: count, ID scheme, date range, and which fields survive redaction (timestamp, symptom, component, duration, impact, mitigation, stated cause).
2. State whether earlier weeks are present. If they are not, mark baselines, trend claims, and held-out validation as UNAVAILABLE. Do not estimate them.
3. Name fields whose loss to redaction blocks a conclusion, such as impact counts or payment provider. These are gaps, not findings.

METHOD
1. Build the incident table from the raw notes, not from any summary. Make one row per incident with fields: note ID, start/end, symptom, checkout stage (cart / payment auth / confirmation / etc.), component, trigger, detection method (alert, customer report, manual), duration, stated impact, mitigation, stated cause, and suspected cause. Keep "stated in note" separate from "my inference" in every column.
2. Write case definitions before counting, the way epidemiology does. Define each failure class by explicit inclusion criteria. Count a note in a class only if it meets them. This stops recurrence from being an artifact of loose labels.
3. Code each note into the classes with a written codebook, as qualitative research does. After the first pass, re-code a random 20% blind to the first labels and report the agreement. Revise the codebook if agreement is poor.
4. Test the belief the task rests on. For each "recurring" class, check whether the notes show a shared cause or only a shared symptom. Sort each class as SAME-CAUSE (evidence cited), SAME-SYMPTOM / CAUSE UNKNOWN, or COINCIDENTAL. Only SAME-CAUSE classes support a single fix.
5. Quantify per class: incident count, total and median duration, stated impact, time between recurrences, and detection method. Run a Pareto analysis of impact by class. If earlier weeks exist, compare this week's rate to the baseline and give the counts. Do not call a change significant on small numbers.
6. For the top 2–3 classes, run Analysis of Competing Hypotheses, a technique from intelligence analysis. List the plausible causes, mark which note evidence is consistent or inconsistent with each, and show which cause survives. State confidence in calibrated terms (likely, roughly even, unlikely) and say why.
7. Red-team the ranking with a pre-mortem. Assume the top-ranked fix ships and failures continue, then write the most plausible reasons. Check detection bias in particular: failures that never generate an incident note are invisible, so a class found by customer reports may be undercounted relative to alerted ones.
8. Forecast. For each candidate class, predict whether it recurs next week. Next week's report scores these predictions.

REPORT STRUCTURE (draft)
- Top section, readable in 5 minutes: 3–5 fix candidates ranked by evidence-backed impact. Each candidate gets its case definition, count, impact, confidence, cited note IDs, key unknowns, and an "effort: team to estimate" placeholder.
- Decision sheet: for each candidate, what fixing it would likely prevent, what the evidence cannot yet show, and what would change the ranking.
- Evidence appendix: the incident table, codebook, coding agreement, ACH matrices, pre-mortem, and redaction gaps.
- Last week's forecast scored, if a prior report exists. This week's forecast.
- Proposals (need owner approval), kept separate and not carried out. Examples: structured fields to add to incident notes, requests for specific un-redacted fields or other data sources, tracking whether a chosen fix reduces recurrence over the following weeks. Each proposal states its benefit, cost, required access, and risk.

JUDGE AND PASS CONDITION
- Traceability: sample 10 claims from the top section at random. All 10 must trace to cited note IDs, with any inference labeled.
- Coding consistency: report the blind re-code agreement on the 20% sample. If the owner names a team member to independently code the same sample using the codebook, report that agreement instead. Self-recoding alone is weaker evidence; say so.
- Held-out check, only if earlier weeks exist: derive the classes from earlier notes, then report how many of this week's notes fit them cleanly and how many need new classes.
- Forecast: this week's predictions are recorded and scored next week. Report the hit rate, including misses.
- Decision test: the owner's bar is that the team can choose what to fix. Pass when a reviewer reading only the top section and decision sheet can name the top candidates, their evidence, and their confidence, and can pick one or say which missing evidence blocks the choice.
- Mark any check that cannot run on the provided notes as UNVERIFIED, with the reason.
```

## Ledger

- `altitude`: the original task was a weekly report on recurring failures. The chosen outcome is a decision-ready ranking the team can act on in one meeting, with the higher goal of fewer failures handled only as gated proposals. The scope stays at the report, and no access is added.
- `depth`: building an incident table from the raw notes, separating stated facts from inference, and citing note IDs makes the report auditable. No added access.
- `depth`: the report tests the "recurring" premise by sorting classes into same-cause, same-symptom, or coincidental. This prevents a fix aimed at a symptom label rather than a cause.
- `depth`: Pareto analysis, recurrence intervals, and baseline rate comparison (only if earlier weeks exist) show which classes actually carry the impact.
- `range` (epidemiology): case definitions written before counting stop loose labels from inflating recurrence.
- `range` (qualitative research): a codebook plus a blind re-code gives a measurable consistency check on the classification.
- `range` (intelligence analysis): ACH and calibrated confidence language show why one cause is favored and how sure the report is.
- `range` (red team): a pre-mortem and a detection-bias check expose the risk that the top-ranked fix targets a class that is over- or under-counted.
- `depth`: next-week forecasts give the report a judge that improves week over week. Scoring them requires next week's notes from the owner.
- Skipped: none. All three lenses fit, because the team will hold a meeting to make a decision under incomplete, redacted evidence.

**Owner actions**
- Provide the redacted notes and their date range. Say whether earlier weeks are available, since this enables baselines and held-out checks.
- Optionally name a team member to independently code the 20% sample and to act as the decision-test reviewer.
- Decide on any items in the Proposals section. None are carried out without your approval.
- Distribute the report yourself. The prompt keeps it as a draft returned only to you.
