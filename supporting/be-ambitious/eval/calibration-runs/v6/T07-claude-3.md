```text
Draft this week's report on recurring checkout failures so the team can choose, in one meeting, which failure to fix first and why.

Assumption: the readers are the engineers and lead who set fix priority. They need a ranked shortlist with evidence and confidence, not a story of each incident.
Assumption: "recurring" means the same failure mode appears in more than one incident. Test that from the notes rather than taking it as given.

Fixed limits:
- Inspect only the redacted incident notes I provide.
- Do not access production, change checkout code, create accounts, send messages, or change incident-response policy.
- Do not try to recover redacted content. Where redaction blocks a conclusion, say so.
- The report is a draft for me. It is not sent anywhere.

First checks:
- Confirm the notes are present. Record their count, date range, and available fields (timestamps, symptoms, error text, checkout step, duration, impact, mitigation, links to earlier incidents). If no notes are provided, stop and ask for them.
- Check whether notes from earlier weeks are included. Without them, report only repeats within this week and make no trend claim.
- List what redaction removed and which analyses it limits.

Method:
1. Work from the notes themselves, not from any summary. Turn each note into one structured row keyed by its note ID: time, checkout step, symptom, error signature, cause as written, customer impact as written, duration, mitigation, and any linked earlier incident. Leave unknown fields blank and never infer them.
2. Write a case definition for each failure mode (from epidemiology). Each definition gives explicit inclusion criteria, so every note is counted once and counted consistently.
   - Assign every note to exactly one mode or to "unclassified".
   - Separate symptoms from causes. Group two notes as the same mode only when the notes give evidence of a shared cause. Otherwise label them "same symptom, cause unconfirmed".
3. Test the taxonomy on notes not used to build it.
   - With 20 or more notes, build the case definitions from the earlier half by date. Then classify the later half without editing the definitions.
   - Report how many held-out notes fit, how many needed a new mode, and how many were ambiguous.
   - With fewer than 20 notes, state that the taxonomy is unvalidated.
4. Draw a timeline of incidents per mode (an epi curve). It shows clustering in time, such as after a deploy or at peak load. Cite only what the notes record.
5. Score each mode in FMEA style (from reliability engineering), each on a stated 1–5 scale with reasons:
   - Severity: customer impact.
   - Occurrence: count in the notes.
   - Detection: how the failure was found (alert, customer report, or unknown).
   Rank the modes with a Pareto view of occurrence × severity. Show the scores, not just the rank.
6. For the top three modes, run a short Analysis of Competing Hypotheses (from intelligence analysis).
   - List at least two candidate causes.
   - Mark which notes support or contradict each cause.
   - Give a confidence label (high, medium, or low) with its reason.
7. For each ranked mode, state what a fix would need to address. Also state the single piece of missing evidence that would most change its rank (value of information, from decision analysis). Do not design code changes.
8. Red-team the ranking.
   - Write the strongest case that the #2 mode, or an unclassified group, should come first.
   - Run a pre-mortem: "We fixed #1 and checkout failures did not drop. Why?"
   - If either case holds, revise the ranking and say so.

Report contents:
- A one-paragraph decision summary: the recommended first fix, the runner-up, and the confidence in each.
- A ranked table with these columns: mode, case definition, note IDs, count, severity/occurrence/detection scores, leading hypothesis and confidence, and the evidence that would change the rank.
- The lists of unclassified notes and "same symptom, cause unconfirmed" notes.
- Data limits: redaction gaps, missing weeks, and the taxonomy validation result.
- An appendix with the structured rows.
Every count and claim cites note IDs. Label each statement as either observed in the notes or inferred.

If you think we should move beyond the report, write that as a separate proposal, kept apart from the report and needing my approval. It may include:
With my approval only: produce this report each week from that week's provided notes, comparing failure modes week over week.
With my approval only: after the team ships a fix, apply that mode's case definition to later weeks' provided notes and report recurrence counts before and after the fix.
With my approval only: other steps beyond the report, each stating its benefit, cost, and the access it would need. None of them may include the prohibited actions above.

Judge:
- Mechanical:
  - Every note ID appears exactly once across the modes and the unclassified list.
  - Mode counts sum to the total number of notes.
  - Every claim in the summary and table cites at least one note ID.
- Taxonomy: report the held-out fit rate. With 20 or more notes, this passes when at least 80% of held-out notes fit an existing mode without edits. With fewer notes, mark the taxonomy unverified.
- Independent review: a team member who did not draft the report, ideally one who will choose the fix, scores it with this rubric:
  (a) They can name the first fix and why within 10 minutes.
  (b) They can find the supporting note for any claim.
  (c) No claim is stronger than its evidence.
  (d) They know what evidence would change the top pick.
  The report passes when all four are yes. Until that review happens, it remains an unverified draft.
```

**Ledger**

- `altitude`: The outcome moves from "a weekly report about failures" to "a decision-ready ranking the team can act on in one meeting." It adds a recommended fix, a runner-up, confidence, and what would change the pick. There is no scope change.
- `altitude`: Weekly repetition and checking a fix against later notes go in a separate proposal behind approval lines. Both use only notes you provide, so no new access is needed.
- `depth`: Each note becomes a structured row with blank unknowns and labels separating observed facts from inferences. This keeps summaries and guesses from passing as evidence.
- `depth`: The taxonomy is built on earlier notes and tested on later ones. This checks whether "recurring" modes are real. The 20-note and 80% thresholds are my defaults, so adjust them if you like.
- `range` (epidemiology): Case definitions and an epi curve give consistent counts and show clustering in time.
- `range` (reliability engineering): FMEA and Pareto scoring make the ranking transparent and open to argument.
- `range` (intelligence analysis): ACH with confidence labels keeps the team from settling on one cause too early.
- `range` (decision analysis): Value of information names the evidence that would flip the ranking.
- `range` (red team): The case for #2 and a pre-mortem expose the risk of fixing a symptom instead of a cause. The added cost is modest; there is no new access or risk.
- Skipped: the hard-target move, since this is not a quantitative improvement request and no metric was set. Anything involving production telemetry or incident-policy changes is also left out because you prohibited it.
- Owner actions:
  - Provide the redacted notes, plus earlier weeks' notes if you want trend claims.
  - Name the independent reviewer.
  - Confirm or adjust the 20-note and 80% thresholds and the 10-minute rubric.
  - Approve or decline the proposal lines.
