```text
Draft this week's report on recurring checkout failures so our team can choose what to fix. Build it from the redacted incident notes I provide. Shape it around that choice: a ranked shortlist of fix candidates, each with its evidence, its estimated impact, and how confident we can be.

Assumption: the team will choose in one meeting, so it needs to compare candidates side by side without reading every incident.
Assumption: "recurring" means the same failure mode or contributing factor appears in more than one incident. Test this for each cluster; don't take it as given.

Scope and limits (unchanged):
- Inspect only the redacted incident notes I provide.
- Do not access production, change checkout code, create accounts, send messages, or change incident-response policy.
- If you think we should move beyond the report, put that in a separate proposal that needs my approval. Keep it out of the report.
- Do not try to recover redacted content. When redaction hides something a ranking needs, log it as a data gap.

First checks:
- Confirm the notes are present. Record the note count, the date range, and which fields the notes consistently contain (timestamps, failing checkout step, error codes, duration, stated impact, mitigation). Name what is missing, and continue only with analysis the notes support.
- Check whether the notes cover earlier weeks as well as this week. If they don't, say that recurrence and trend claims rest on this week alone.

Method:
1. Incident table. Turn each note into one row: note ID, start/detect/resolve times, checkout step, symptom, error codes, contributing factors, mitigation, and stated customer impact. Leave a cell blank rather than guess. Every later number must trace to rows by note ID.
2. Failure taxonomy (qualitative coding). Open-code the earliest subset of notes to draft failure-mode categories. Give each category a one-line definition and an inclusion rule. Then freeze the codebook and apply it to the remaining notes. Record triggers and contributing factors separately, since one incident may have several.
3. Recurrence test. For each cluster, list its incidents, their dates, and the shared factor. Flag any cluster that may be one incident logged twice or an artifact of labeling. Report counts with exact Poisson intervals, so the team can see when an apparent spike is within noise at counts this small. Compare with prior weeks only if the notes include them.
4. Prioritize (FMEA-style). Score each cluster on three dimensions:
   - severity, from stated impact and duration;
   - occurrence, from the counts;
   - detection, from how the failure was noticed and how late, using the timestamps.
   Show all three scores and their inputs rather than only a product. Mark low-confidence scores.
5. Red-team the top three clusters. For each, write the strongest alternative explanation, state which evidence in the notes would distinguish the two, and say whether the notes settle it. Then run a short pre-mortem: "We fixed this and checkout failures didn't drop. Why?"
6. Holdout check. Patterns found while building the codebook in step 2 are development evidence. Confirm each one on notes you did not use to find it, or label it unverified.

Report format:
- Top: a one-paragraph decision summary, then the ranked shortlist table. Columns: cluster, incidents by note ID, count with interval, severity/occurrence/detection scores, confidence, and the open question that would change the ranking.
- Then: evidence for each cluster, red-team findings, data gaps from redaction or missing fields, and the codebook as an appendix.
- Keep proposed causes visibly separate from observed evidence.

Separate proposal (its own document, drafted only, not sent):
With my approval only: run this analysis as a recurring weekly workflow, reusing the frozen codebook so counts are comparable from week to week.
With my approval only: ask me for additional redacted records, or fields that already exist in incident records, wherever the data-gap log shows a ranking depends on them.

Judge:
- Mechanical: every number and claim in the report traces to note IDs in the incident table. Recomputing cluster counts from the table reproduces the report's counts. Nothing outside the provided notes is cited.
- Coding reliability: a second coder I choose applies the codebook to a sample of at least 10 notes, or to all notes if there are fewer. Report Cohen's kappa. If kappa is below 0.6, revise the definitions and mark the clusters provisional.
- Independent review: I give the draft to a team member who did not write it, ideally someone who has been on call for checkout. Rubric:
  (a) the reviewer can name the top candidate and the reason for it within five minutes;
  (b) each ranking cites evidence the reviewer can check in the notes;
  (c) uncertainty and data gaps are stated wherever they affect the ranking;
  (d) the red-team alternatives are fair.
  Pass: yes on all four, and the reviewer would use the shortlist to choose a fix in the team meeting.
- Until the second coding and the review have run, mark the ranking unverified.
```

**Ledger**

- `altitude`: The original outcome is a report about failures. The improved outcome is a ranked, evidence-linked shortlist built for the team's fix decision. Scope is unchanged, with no new access.
- `altitude`: The weekly recurring workflow and the request for more redacted data go into a separate proposal behind "With my approval only:", as you asked. Each adds a new workflow or new data sharing if you approve it.
- `depth`: The analysis starts from an incident table built from the raw notes, with note-ID traceability. This replaces a narrative summary and makes every claim checkable. It costs some extra drafting time.
- `depth`: Recurrence is tested rather than assumed, using duplicate and artifact checks and exact Poisson intervals. This keeps the team from chasing noise at small counts.
- `depth`: The codebook is frozen on early notes and patterns are confirmed on held-out notes. This separates what was discovered from what was confirmed. With few notes, more results will be labeled unverified.
- `range`: Qualitative-research coding with inter-coder agreement (kappa) shows whether the categories are stable or just one person's reading. It needs a second coder that you arrange.
- `range`: FMEA scoring from reliability engineering, on severity, occurrence, and detection, can surface rare but severe or late-detected failures that frequency alone would hide.
- `range`: A red-team pass and a pre-mortem on the top three expose alternative causes before the team commits fix effort.
- Skipped lenses: the hard-target move, because this is a decision report and not a quantitative improvement request. Reducing failure rates directly is also skipped, because it needs code or production changes you prohibited.
- Owner actions: provide the notes and confirm whether they include prior weeks; choose the second coder and the independent reviewer and hand them the materials, since I can't send messages; decide on the two approval-only proposal items.
