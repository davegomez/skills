```text
Goal: Draft this week's report on recurring checkout failures. The report should let the team choose what to fix in one meeting. Assumption (please confirm): fix capacity is limited, so the report should rank a short list of fix candidates and state what each would likely prevent, not just summarize incidents.

Requirements (unchanged):
- Inspect only the redacted incident notes I provide.
- Do not access production, change checkout code, create accounts, send messages, or change incident-response policy.
- The deliverable is a draft weekly report.
- Anything beyond the report goes in a separate proposal, marked as needing my approval. Do not act on it.

First checks (report these before the analysis):
- List the notes received: count, date range, and which fields appear (time, duration, symptom, checkout stage, suspected cause, resolution, detection source, customer impact).
- Name fields that are missing or redacted, and say which conclusions each gap prevents.
- Say whether the notes span enough earlier weeks for the held-out check in the Judge section. If they don't, mark recurrence claims as unverified and continue.

Method:
1. Incident table from raw notes. Build one row per incident from the note text itself, not from summaries inside the notes. Columns: note ID, date, duration, symptom, checkout stage, suspected cause, resolution, detection source, stated impact. Mark each cell as stated or inferred.
2. Codebook before coding (qualitative research). Write a case definition for "checkout failure" and a definition for each failure-mode and cause category. Code every incident against the codebook. Log any change to the codebook and recode affected rows.
3. Test recurrence instead of assuming it:
   - Label each cluster as "shared cause (evidenced)", "shared symptom only", or "unclear", citing note IDs.
   - Plot occurrences per week (an epidemic curve). Use it to separate steady recurrence from a one-week spike or a change in how incidents were logged.
4. Rank clusters with an FMEA-style breakdown:
   - severity: impact as stated in the notes
   - occurrence: count and weekly rate
   - detectability: how it was found, e.g. customer report vs alert
   Show each component, not only a combined score. Where the notes lack impact or effort data, say so rather than estimating.
5. Red-team the top pick with a pre-mortem. Assume fixing it did not reduce checkout failures and list the likeliest reasons, such as wrong cluster boundaries, detection bias toward loud failures, or redaction hiding the true cause. For each reason, cite what in the notes supports or weakens it.

Report format:
- One-page decision summary first: 3–5 ranked fix candidates. For each, give what it would likely prevent, the evidence strength (evidenced / symptom-only / unclear), the key note IDs, and the open question that would most change the ranking.
- Then the epidemic curve, the cluster table, the codebook, and the pre-mortem.
- Every factual claim cites note IDs. Proposed explanations are labeled as proposals, kept apart from observed evidence.

Separate proposal (needs my approval, do not act on it): list next steps the notes could not settle, e.g. data that would confirm a cause, or note fields that would make next week's coding reliable. For each, state the expected benefit and what access or policy owner it would involve.

With my approval only: turn this into a recurring weekly workflow (template, schedule, or automation).
With my approval only: obtain data beyond the redacted notes (unredacted fields, telemetry, deploy history) to confirm causes the notes cannot.
With my approval only: share the incident table or a sample with a second coder to measure coding agreement (Cohen's kappa).

Judge:
- Traceability (mechanical):
  - Every incident-table row maps to a note ID that exists in the supplied notes.
  - Every claim in the decision summary cites at least one note ID.
  - Pass = zero untraced rows or claims.
- Held-out check:
  - Build the codebook, clusters, and ranking using only notes before the most recent week. Then apply them to the most recent week.
  - Report what share of that week's incidents the codebook covers without new categories, and whether the top-ranked clusters recur.
  - Then fold that week into the final report, and label which findings came from development data and which were confirmed on the held-out week.
  - Too little history leaves recurrence claims unverified.
- Independent review (qualitative): I will hand the draft to a reviewer I choose. They score it 1–5 on each of:
  - Can the team pick a fix from the summary in 30 minutes?
  - Are evidence and inference clearly separated?
  - Does the top pick's evidence survive the pre-mortem?
  - Pass = every item ≥ 4.
  - Until the review happens, the report is an unreviewed draft.
```

- `altitude`: The original outcome was a weekly report on failures. The improved outcome is a decision-ready ranking of fix candidates for one meeting. Same deliverable and scope; it adds an assumption you need to confirm.
- `depth`: An incident-level table built from the raw notes, plus FMEA-style ranking, replaces summarizing. The ranking shows its components, so the team can see why something ranks high. No new access.
- `depth`: The prompt tests whether the failures really recur from a shared cause, using a held-out recent week. This guards against fixing a symptom cluster. It needs enough note history, so it is checked first.
- `range`: A codebook from qualitative research makes the coding consistent and auditable. A second coder is behind approval because it means sharing the data.
- `range`: An epidemic curve from epidemiology separates steady recurrence from spikes and from changes in how incidents were logged.
- `range`: A red-team pre-mortem exposes decision risk on the top pick, including detection bias and blind spots from redaction.
- Skipped lenses: none.
- Owner actions:
  - Confirm the limited-capacity assumption.
  - Provide notes covering several weeks if possible.
  - Pick the independent reviewer and pass them the draft.
  - Decide on the three approval lines and on the separate proposal once it exists.
