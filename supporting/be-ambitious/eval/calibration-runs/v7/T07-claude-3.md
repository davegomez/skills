```text
Draft this week's report on recurring checkout failures so the team can choose what to fix. Write it as a decision brief: a short ranked list of fix candidates, each with the evidence that it recurs, its impact, how confident the evidence makes us, and what remains unknown. Build every claim from the redacted incident notes the owner provides.

Assumption: the team will choose in a meeting with limited fix capacity, so the report should lead with a recommendation and its trade-offs, not a chronology.
Assumption: "recurring" means the same underlying cause or contributing factor returns, not just the same visible symptom. Test this against the notes; do not take it as given.

Scope and limits (all binding):
- Inspect only the redacted incident notes the owner provides. Use no other data source.
- Do not access production, change checkout code, create accounts, send messages, or change incident-response policy.
- The deliverable is the report. Anything beyond it goes in a separate proposal section, and every item there needs the owner's approval before anyone acts on it.

First checks, before analysis:
- Confirm the notes are present. List how many there are, the date span they cover, and which fields they reliably contain: time, symptom, detection, duration, customer impact, suspected cause, remediation, and links to earlier incidents.
- Say which questions the notes cannot answer. Examples: no order volume means failure rates are impossible and only counts are possible. Missing timestamps means time between recurrences is impossible.
- Flag places where redaction may hide whether two incidents share a cause.
- Name every missing dependency. Do only the work the notes support.

Method:
1. Incident table. Turn each note into one row: note ID, date, symptom, detection path, duration, stated impact, stated cause, contributing factors, remediation, and any recurrence link. Mark each field as stated in the note or inferred by you. Keep inference out of the stated column.
2. Cause coding, using qualitative-research practice. Write a short codebook that defines each failure class by its underlying cause or contributing factor, with inclusion and exclusion rules. Draft the codebook on part of the notes, then apply it unchanged to the rest. Report the notes that fit no class. If there are too few notes to split, say so and mark the classes as not yet checked on unseen notes.
3. Recurrence test. For each class, show the note IDs, the count, and the dates or intervals. Separate three cases:
   - Same cause recurring.
   - Same symptom with different or unknown causes.
   - Possible duplicate records of one incident.
   With small counts, report counts and spans only. Do not claim trends.
4. Contributing factors, using resilience-engineering practice. Where the notes allow, list several contributing factors per incident rather than forcing a single root cause. Note any remediation that the notes show recurring anyway.
5. Ranking, using decision-analysis practice. Rank classes on explicit criteria: frequency, stated customer impact, and evidence confidence. Give a Pareto view of which classes account for most incidents and most stated impact. Show the scoring so the team can reweight it in the meeting. Mark fix effort as unknown unless the notes state it.
6. Red team, using a pre-mortem. For the top-ranked candidate, write the strongest case that fixing it would be the wrong choice. For example: its recurrence could be a recording artifact, redaction could merge distinct causes, or a lower-ranked class could carry more hidden impact. Say what evidence would settle the question.

Report format:
- One-paragraph recommendation.
- Ranked candidates, each with evidence citing note IDs, a confidence level, and open questions.
- The scoring table.
- The red-team note.
- Data limits.
- Appendix with the incident table and codebook.

Every count must be recomputable from the appendix.

Separate proposal (for owner decision; none of this is done as part of this task):
With my approval only: repeat this analysis on later weeks' redacted notes to check whether the classes the team chose to fix actually stop recurring. Report before-and-after counts per class.
With my approval only: ask for additional redacted fields so that next week's report can give rates and timelines instead of raw counts. Examples: checkout attempt or order volume per day, incident timestamps, and deploy or change references.

Judge: a checkout-team reviewer, other than the author, whom the owner designates. The owner hands the report to the reviewer; the author does not send it.
Before reading the author's coding, the reviewer independently codes a sample of the notes (at least 5, or 20%, whichever is larger) using the codebook. The reviewer then checks:
(a) every count and claim traces to cited note IDs and recomputes from the appendix;
(b) stated and inferred facts are kept distinct;
(c) the reviewer's sample coding either matches the author's or differs in ways that do not change the top-ranked candidates;
(d) the recurrence test separates same-cause, same-symptom, and duplicate cases;
(e) the ranking criteria are explicit and can be reweighted;
(f) the red-team note is specific to the top candidate;
(g) data limits are stated;
(h) nothing in the report or the proposal crosses the stated limits.
Pass only if every criterion is met. Until the review runs, the classification and ranking are unverified.
```

- `altitude`: The original outcome was a weekly report about failures. The improved outcome is a decision brief: ranked fix candidates with adjustable criteria, so the meeting ends in a choice. Scope and cost stay the same, since it uses only the provided notes.
- `depth`: An incident table built from the raw notes, a check of whether "recurring" means the same cause, and stated-versus-inferred labels. Together these stop symptom-level grouping from sending the team to fix the wrong thing. No new access.
- `depth`: The codebook is drafted on part of the notes and applied unchanged to the rest. The judge is a blind recode by a second person. Together they give evidence beyond the author's own verdict. This costs the reviewer about an hour.
- `range`: Qualitative research (codebook, double-coding) makes the classification reproducible. Resilience engineering (contributing factors) avoids single-root-cause fixes. Decision analysis (explicit criteria, Pareto) lets the team reweight priorities live. A pre-mortem red team tests the top pick against recording artifacts and redaction.
- `altitude` (proposal, approval only): The report becomes a weekly loop that checks whether chosen fixes worked. This adds a new recurring workflow.
- `depth` (proposal, approval only): Extra redacted fields would allow rates instead of counts. This means sharing new data.
- Skipped: none. A proposal for incident-template changes was left out because it could count as incident-response policy, which you prohibited.
- Owner actions:
  - Supply the redacted notes.
  - Designate the reviewer and hand them the report.
  - Decide on the two proposal items.
