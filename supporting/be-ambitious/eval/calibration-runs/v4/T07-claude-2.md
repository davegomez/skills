```text
Goal: draft a weekly report on recurring checkout failures so our team can choose what to fix. Assumption: the report's purpose is to let the team make that choice in one meeting, so it should lead with ranked, evidence-backed fix candidates. The report remains the deliverable.

Fixed limits:
- Inspect only the redacted incident notes I provide. Do not access production, change checkout code, create accounts, send messages, or change incident-response policy.
- Do not try to recover or guess redacted details. Note where redaction limits a conclusion.
- If you think we should go beyond the report, put it in a separate proposal that needs my approval. Do not act on it.

First checks, before analysis:
- List the notes received: how many, the date range, and which fields are present (incident ID, start and end time, symptom, stated cause, component or dependency, detection method, mitigation, links to earlier incidents). If IDs or timestamps are missing, the steps below are limited. Name each limit and continue with what the notes support.
- Ask me whether a report format is required. If one is, keep it and put the extra material in an appendix.
- Ask me who will be the independent reviewer named in the judge. I will arrange the review. Do not contact anyone.

Method:
1. Build an incident table from the raw notes, one row per note. Columns: ID, time window, duration if stated, symptom, stated cause, contributing factors, component or dependency, detection (alert or customer report), mitigation, and recurrence links. Mark each cell as stated, inferred (quote the text it rests on), or unknown.
2. Write a case definition. It says what counts as a checkout failure and when two notes describe one episode rather than two incidents. Use it to remove duplicates. List every note as included or excluded, with a reason.
3. Code failure modes using a written codebook. Group notes by underlying cause, not by symptom. Put the codebook in the appendix so later reports can reuse it.
4. Test whether the failures actually recur. Sort the notes by time. Form clusters using only the earlier portion, freeze the codebook, and then count how many later notes fall into a cluster already seen. Report the hit and miss counts. Clusters formed from all the notes are only development evidence; mark any cluster this test does not confirm as "recurrence unconfirmed". If the notes are too few or undated to split, say so.
5. For each recurring cluster, run an Analysis of Competing Hypotheses. List the plausible causes, mark which note evidence supports or contradicts each one, and name the evidence that would tell them apart. This shows where the notes do not settle the cause.
6. Draw a timeline of incidents for each cluster. It shows whether failures bunch together (for example, near changes the notes mention) or arrive steadily.
7. Rank fix candidates in an FMEA-style table with three scores, each citing note IDs:
   - Severity, as the notes state it.
   - Occurrence, as a count of notes.
   - Detectability, based on how each failure was found.
   Leave fix effort blank for the team. Do not estimate it.
8. Run a pre-mortem on the top-ranked candidate. Assume fixing it did not reduce failures. List the likeliest reasons, drawn from the notes, and what the team should check before committing.

Report contents:
- One-page decision summary: 3 to 5 fix candidates. For each, give the failure mode, incident IDs, count, impact evidence, confidence, main unknown, and the decision the team needs to make.
- The ranking table, the timelines, the competing-hypotheses notes, and the pre-mortem.
- Limits: redaction gaps, missing fields, and small counts. State that counts are not failure rates, because checkout volume is not in the notes.
- Appendix: the incident table, case definition, codebook, and inclusion/exclusion list.
- Every claim cites the note IDs it rests on. Keep observed facts (quoted from notes) separate from inferences.

Separate proposal, drafted only:
With my approval only: make this a recurring weekly workflow that reuses the codebook and tracks whether the failure modes the team fixes stop appearing in later notes.
With my approval only: get checkout volume or less-redacted notes, so that counts become failure rates.
With my approval only: draft suggested structured fields for incident notes (cause, component, recurrence link) for the owner of incident-response policy to consider. Do not change any policy.

Judge:
- Coverage (mechanical): 100% of the notes received appear in the table as included or excluded with a reason. Every claim in the summary and the ranking cites at least one note ID.
- Citation check (independent reviewer): the reviewer checks 10 randomly chosen citations, or all of them if there are fewer. Pass: no claim is unsupported by the note it cites.
- Coding agreement (independent reviewer): the reviewer codes 10 notes, or all notes if there are fewer, using only the codebook. Report Cohen's kappa. Pass: kappa ≥ 0.6. Below that, revise the codebook and mark the affected clusters unverified.
- Recurrence: report the hit and miss counts from step 4, or state that recurrence is unverified.
- Decision usefulness (independent reviewer): a team member who did not write the report reads only the summary. They then state the choice it asks for and the evidence for each candidate. Pass: both match the report.
Until the reviewer checks are done, label the coding and the ranking "unverified".
```

- `altitude`: the outcome moves from "a report about failures" to "a report the team can decide from in one meeting" (ranked candidates, confidence, unknowns, a blank effort column). It stays within report scope.
- `altitude`: a recurring workflow that tracks whether fixes work, rates based on checkout volume, and suggested note fields. All three are in the separate proposal behind approval because they add workflow, new data access, or policy input.
- `depth`: a structured incident table with stated/inferred/unknown marks, a case definition, and deduplication. Analysis uses raw notes instead of summaries. No added access is needed.
- `depth`: a time-split test of whether failures really recur. It tests the belief the report rests on, using notes not used to form the clusters. It may come back "unverified" if the notes are few or undated.
- `range`: from epidemiology, a case definition and per-cluster timelines, which separate bursts from steady recurrence. From safety engineering, an FMEA-style ranking, which makes priorities traceable to evidence. From qualitative research, a codebook plus an agreement score, which checks that the clusters can be reproduced.
- `range`: Analysis of Competing Hypotheses and a pre-mortem act as the red team. They show where the cause is unsettled and what could make the top pick fail.
- Skipped: none. No hard target was set, because a count of failures in redacted notes has no comparable baseline.
- Owner actions: confirm whether a report format is required. Provide an independent reviewer and run their checks, since the agent cannot message anyone. Share the report with the team. Decide on the three proposal items.
