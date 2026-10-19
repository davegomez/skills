```text
Draft this week's report on recurring checkout failures so the team can choose what to fix. The report should end in a decision: a ranked shortlist of fix candidates, with the evidence, confidence, and trade-offs for each, that the team can act on in one meeting.

Assumption: the report's real job is to help the team pick the one to three fixes most likely to reduce repeat checkout failures. Keep that goal unless the incident notes show a different one.

Scope and limits (fixed):
- Inspect only the redacted incident notes I provide. Do not access production, change checkout code, create accounts, send messages, or change incident-response policy.
- Anything beyond the report goes in a separate proposal, clearly marked as needing my approval. Do not act on it.

First checks:
- Confirm which notes you received and which week they cover.
- List the fields the notes reliably contain, such as time, symptom, component, trigger, detection, mitigation, duration, and stated customer impact.
- Note what redaction removed.
- If a field is missing, such as order counts, revenue impact, or root cause, say so. Do not estimate it or invent it. Rank only on what the notes support, and list each gap as a limitation.

Method:
1. Work from the raw notes, not from summaries of them.
   - Build an incident table with one row per incident and a stable note ID.
   - Use only values stated in the notes. Mark inferred values as inferred.
   - Merge duplicate reports of the same event and record each merge.
2. Write a short codebook of failure modes before you count anything (qualitative content analysis).
   - For each mode, give a definition, inclusion and exclusion rules, and one example note ID.
   - Code every incident against it.
   - Keep an "unclassified" bucket instead of forcing a fit.
3. Write a case definition for "recurring" (epidemiology), for example "same failure mode at least twice in the window."
   - Test whether each candidate mode really recurs, or only looks recurring because of shared wording.
   - Flag detection and reporting bias, such as modes that only appear when one person is on call, or causes redaction may have hidden.
4. Rank the recurring modes with an FMEA-style table (reliability engineering).
   - Score severity, occurrence, and detectability, each from evidence in the notes.
   - Show the scores and the cited note IDs.
   - Mark any score set to "unknown" because the notes are silent.
5. Distinguish the kinds of cause for each mode.
   - Separate observed cause, stated suspected cause, and your own hypothesis.
   - Use contributing-factor analysis (e.g., Five Whys) only as far as the notes support, and stop where evidence ends.
6. Run a pre-mortem on the top-ranked candidate (red team). Assume the team fixes it and failures continue, then state:
   - the most likely reason this happens
   - the evidence that would reorder the ranking
7. Run a holdout check if the window has enough incidents.
   - Build the codebook on all but the most recent notes, then code the most recent ones blind.
   - Report how many fit existing modes and how many needed new ones.
   - If there are too few notes to hold any out, say the taxonomy is unvalidated.

Report contents:
- A one-paragraph summary.
- The ranked shortlist, giving for each candidate:
  - the failure mode
  - recurrence count with note IDs
  - severity and evidence
  - confidence
  - what fixing it would plausibly prevent
  - what remains unknown
- Notable non-recurring incidents.
- Data gaps and limitations.
- An appendix with the codebook, incident table, and FMEA table.

Label every claim as observed (with note IDs) or inferred.

Separate proposal, with my approval only:
- With my approval only: a recurring weekly version of this analysis that re-applies the same codebook to each new week's redacted notes. It would track whether modes the team chose to fix stop recurring.
- With my approval only: a request list for additional fields or less-redacted notes, each with the ranking question it would resolve.

Judge and pass condition:
- Mechanical: recompute every count and score in the report from the incident table. They must match exactly, and every observed claim must cite note IDs that exist.
- Holdout: report the fraction of held-out notes that fit the existing modes, or state that the holdout was not possible.
- Independent review: a qualified team member reviews the draft against this rubric:
  - Can they choose a fix from the shortlist without opening the notes?
  - Is each claim correctly labeled observed or inferred?
  - Is the pre-mortem credible?
- Pass when the recount matches, all citations resolve, the proposal is separate and marked for approval, and the reviewer confirms the rubric.
- Until the review happens, the report's decision-readiness is unverified.
```

**Ledger**
- `altitude`: The original outcome was a weekly report about failures. The improved outcome is a ranked, decision-ready fix shortlist with confidence and a pre-mortem, which serves the stated purpose of letting the team choose what to fix. Scope, access, and cost are unchanged.
- `altitude`: The recurring weekly tracking workflow sits behind "With my approval only" in the separate proposal you asked for. It is a new recurring workflow, but it uses only redacted notes.
- `depth`: The method works from the raw notes through an incident table with note IDs, dedup, and an observed/inferred split. Every number can then be traced and recounted. No scope effect.
- `depth`: The holdout test challenges the assumption that the failures really fall into stable recurring causes. It needs enough incidents and falls back to "unvalidated" if there are too few.
- `range`: Qualitative content analysis, through the codebook and the unclassified bucket, makes categories explicit and repeatable instead of impressionistic.
- `range`: An epidemiology-style case definition and a bias check stop the report from counting look-alike wording or artifacts of on-call patterns as recurrence.
- `range`: FMEA-style scoring turns the ranking into transparent, evidence-cited trade-offs. Scores stay "unknown" where the notes are silent.
- `range`: The red-team pre-mortem on the top candidate exposes the main decision risk before the team commits engineering time.
- `depth`: The data-request list in the proposal is approval-gated, because it would involve new data access.
- Skipped lenses: none. Fixing the failures themselves, or any production measurement, stays out of the prompt because production access and code changes are prohibited.
- Owner actions:
  - Provide the redacted notes and the week they cover.
  - Name a qualified team member to review the draft against the rubric. I can't contact them, since sending messages is prohibited.
  - Decide whether to approve the recurring workflow and the data-request list.
