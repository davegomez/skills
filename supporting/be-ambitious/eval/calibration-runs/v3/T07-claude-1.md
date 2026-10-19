```text
Draft this week's report on recurring checkout failures so the team can choose what to fix. The goal behind the report (assumption: confirm or correct) is a decision the team can make in one meeting: which one to three recurring failure modes to fix first, and why. The report should show the ranked candidates, the evidence for each, and what remains uncertain.

Scope and limits (all binding):
- Inspect only the redacted incident notes I provide. Do not access production, change checkout code, create accounts, send messages, or change incident-response policy.
- Anything beyond the report goes in a separate proposal that needs my approval. Do not act on it.

First checks, done before any analysis:
- List the notes provided: count, IDs (assign stable IDs if none exist), the date span they cover, and which fields are present (timestamps, symptom, affected step, customer impact, duration, contributing factors, remediation).
- Name each field that redaction removed or that is missing, and what that prevents you from concluding. Treat these as limitations. Do not fill them with guesses.

Method:
1. Work from the raw notes, not from any summary lines inside them. Pull out timelines, symptoms, and the contributing factors each note describes.
2. Write a case definition for each candidate failure mode, the way epidemiologists define a case: which features make an incident count, and which features rule it out.
3. Build a small codebook through open coding: code name, definition, inclusion and exclusion rules, and one example note ID. If there are enough notes (roughly 15 or more), build the codebook on a random two-thirds of them. Then apply it unchanged to the remaining third and report how many held-out notes fit an existing code and how many needed a new one. Below that size, say the split is too small and code all notes.
4. Test whether each failure mode really recurs. For each cluster, separate two cases:
   - same contributing factor across incidents (true recurrence)
   - similar symptom with different or unknown causes (lookalikes)
   Report a cluster as recurring only when the notes show a shared factor. Otherwise label it "symptom-similar, cause unconfirmed."
5. Rank the candidates with a Pareto view. For each one, show the recurrence count, the impact the notes record (duration, affected step, any customer-impact detail that survived redaction), and time between recurrences. Where impact is redacted, say so instead of estimating it.
6. Use contributing-factor analysis in the style of learning-from-incidents, not a single root cause per incident. Note where the same factor shows up across different clusters, since one fix might cover several.
7. For each top candidate, give a decision-analysis view: what fixing it would plausibly prevent, according to the notes, and the single piece of missing information that would most likely change the ranking (value of information).
8. Red-team the ranking:
   - State the strongest case for the runner-up over the top pick.
   - Check whether a cluster could be an artifact of how the notes were written or redacted, such as one author's phrasing or a redacted field that merges distinct causes.
   - Check for ascertainment bias: the notes cover only incidents someone recorded.

Deliverable: the weekly report, containing:
- a one-paragraph summary with the recommended choice
- a ranked table (failure mode, recurrence status, count, recorded impact, cited note IDs, confidence, key unknown)
- case definitions and the codebook as an appendix
- the held-out coding result
- the red-team findings
- limitations from redaction
Every finding must cite the note IDs it rests on. Label each statement as observed in the notes or as inference.

Separate proposal (draft only; do not act):
- With my approval only: request less-redacted notes or checkout telemetry to validate the ranking and fill the impact gaps the report names.
- With my approval only: turn the codebook and ranking steps into a repeatable weekly process.
- With my approval only: I give an independent reviewer on the team the review packet: the codebook plus the held-out or sampled notes with your codes removed.

Judge:
- Mechanical check (run it yourself): every note ID cited in the report exists in the provided set. Every provided note is assigned to a cluster or to "unclassified." Each cluster's count matches its cited IDs. Pass means zero mismatches; report the tally.
- Held-out check: report how many held-out notes fit the codebook. This is evidence on data not used to build the codebook, but it is still your own coding.
- Independent check (pending until the reviewer runs it): the reviewer codes the packet using only the codebook. Pass means at least 80% agreement with your codes, plus a "yes" from the reviewer on each top candidate against this rubric: evidence cited, recurrence status justified, impact stated or marked redacted, key unknown named.
- Until the independent check runs, mark the ranking "unverified by independent review."
```

- `altitude`: The original outcome was a weekly report on recurring failures. The improved outcome is a ranked fix decision the team can make in one meeting, with stated uncertainty. It stays within the report scope. Going further, toward fewer recurrences, would need telemetry, so it is only in the approval-gated proposal.
- `depth`: Working from raw notes, with case definitions and a recurrence test (shared factor versus lookalike symptom), checks the belief the task rests on: that the failures really recur. Read-only, no new access.
- `depth`: Building the codebook on two-thirds of the notes and confirming it on the held-out third separates the evidence used to find clusters from the evidence used to confirm them.
- `range`: Epidemiology (case definitions, ascertainment bias) makes counts consistent and exposes gaps in what got recorded.
- `range`: Qualitative research (codebook, inter-rater agreement) gives the independent reviewer something to check.
- `range`: Decision analysis (Pareto ranking, value of information) shows which unknown would flip the choice.
- `range`: Learning-from-incidents (contributing factors) finds single fixes that cover several clusters.
- `range`: The red team (runner-up steelman, author or redaction artifacts) tests the top recommendation before the meeting.
- Skipped: none. Each lens added a method the task lacked.
- Owner actions:
  - Confirm or correct the assumed goal of one to three fixes chosen in one meeting.
  - Provide the redacted notes.
  - Pick and brief an independent reviewer, and hand over the packet, since I may not send messages.
  - Decide on the three approval-gated proposal items: less-redacted data or telemetry, a repeatable weekly process, and reviewer data sharing.
