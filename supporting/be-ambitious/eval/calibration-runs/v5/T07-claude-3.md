```text
Draft this week's report on recurring checkout failures so the team can choose what to fix. Make the report decision-ready: a short ranked list of fix candidates, each with the evidence behind it, its estimated impact, your confidence, and what would change its rank.

Scope and limits (all binding):
- Inspect only the redacted incident notes I provide. Use no other data source. Do not try to infer or reconstruct redacted content.
- Do not access production, change checkout code, create accounts, send messages, or change incident-response policy.
- Anything beyond the report goes in a separate proposal section, and each item there needs my approval.

First checks, before any analysis:
- Confirm the notes are present.
- Count them, give each a stable ID, and record the date range each covers.
- Note which fields are redacted or missing (for example time, component, duration, customer impact).
- State whether the notes span enough history to show recurrence, or only this week.
- Note whether any order-volume or traffic denominator exists. If none does, report counts, not rates, and say so.
- Name every gap and continue only with work the notes support.

Method:
1. Build an incident table from the raw note text, not from note titles. Use one row per incident, with these fields:
   - date/time
   - symptom the customer saw
   - checkout step affected
   - suspected component
   - trigger
   - how it was detected
   - duration
   - stated impact
   - mitigation
   - whether the note claims a root cause
   Mark each field as observed in the note, inferred, or absent.
2. Write a case definition for "checkout failure" and a codebook of failure modes. Each code needs an inclusion rule and an exclusion rule. Develop the codebook on about two-thirds of the notes, chosen by stable ID. Then classify the held-out third without changing the codebook. Report how many held-out notes fit a code cleanly, fit ambiguously, or fit no code.
3. Test the belief the task rests on: that these failures recur from shared causes.
   - For each cluster, check whether the notes show a shared mechanism or only a shared symptom.
   - Label each cluster as "same cause (evidenced)", "same symptom, cause unknown", or "coincidental grouping".
   - Use contributing-factor analysis, which allows several factors per incident, rather than forcing a single root cause.
4. Rank fix candidates with a Pareto view: frequency × stated impact × confidence.
   - Show recurrence intervals where dates allow.
   - For each candidate, name the cheapest piece of missing information that would most change its rank. This is a value-of-information note.
5. Check for reporting bias. Note anything in the notes that suggests changes in detection or write-up practice, rather than in failures, could explain the counts. Examples: a new alert, a new note template, or a spike in notes after one large incident.
6. Red-team the top two candidates. For each, write the strongest alternative explanation the notes allow, and say what evidence in the notes supports or weakens it.

Report contents:
- one-paragraph summary for a 30-minute triage meeting
- ranked candidate table
- cluster labels from step 3
- codebook and held-out fit results
- data gaps and bias notes
- red-team notes
Cite every count and claim by note ID. Separate observed evidence from inference throughout.

Separate proposal, after the report:
- With my approval only: make this a standing weekly template that tracks per-cluster recurrence week over week, so the team can see whether chosen fixes reduced recurrence.
- With my approval only: request additional data, such as less-redacted fields or order-volume denominators for failure rates. Name each field, the decision it would change, and who would need to grant it.

Assumption: the team's goal is to fix the failures that cost the most and recur from a shared cause, not the ones that were most recently noticed.
Assumption: someone who did not draft the report is available to review it. Confirm this before relying on the judge below.

Judge: an independent reviewer on the team, who did not draft the report, checks it against this rubric:
(a) Every count and claim traces to cited note IDs.
(b) A recount of any two clusters from the incident table matches the report.
(c) Each "same cause (evidenced)" label quotes or cites the shared mechanism in the notes.
(d) Held-out fit results are reported.

Pass condition: (a) through (d) all hold, and the reviewer can name the top fix candidate and the evidence for it from the report alone. If the reviewer is unavailable, or the held-out set has too few notes to test the codebook, mark the affected cluster claims unverified.
```

**Ledger**

- `altitude`: The original outcome is a weekly report on recurring failures. The improved outcome is a ranked, evidence-cited fix list that a triage meeting can act on. It needs no new access, and it is checked by the reviewer rubric.
- `depth`: The report is built from raw note text into a coded incident table instead of titles, using a codebook, contributing-factor analysis, and a Pareto ranking. This makes the counts reproducible and auditable. It adds analysis effort only.
- `depth` (move): The prompt tests whether "recurring" means a shared cause or only a shared symptom, and confirms the codebook on held-out notes. This protects the team from fixing a grouping that isn't real. If there are few notes, some claims may end up unverified.
- `range`: From epidemiology, it adds a case definition and a reporting-bias check. These catch count changes that come from detection or write-up practice rather than from failures.
- `range`: From decision analysis, it adds a value-of-information note per candidate. This shows which cheap fact would most change the ranking.
- `range`: A red-team step writes the strongest alternative explanation for the top two candidates. This exposes the decision risk before the team commits engineering time.
- Approval-only items (separate proposal): a standing weekly tracking template, which would be a new recurring workflow, and requests for extra data, which would be new access or data sharing.
- Skipped lenses: none.
- Owner actions:
  - Supply the redacted notes.
  - Confirm that an independent reviewer is available. I can't contact anyone, so arranging this is yours.
  - Decide on the two approval-only proposals.
