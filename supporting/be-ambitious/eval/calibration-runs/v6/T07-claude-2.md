```text
Draft this week's report on recurring checkout failures so the team can choose what to fix, and make that choice easy to defend. The report succeeds if a teammate can read it in about 30 minutes, pick a fix, and trace every claim behind that pick back to specific incident notes.

Assumption: the team has limited capacity and will fund one to three fixes this cycle, so the report should rank candidates rather than list them.
Assumption: "recurring" means the same failure mechanism occurring more than once. Similar symptoms alone (for example, "payment timeout") do not count.

Boundaries (all binding):
- Inspect only the redacted incident notes I provide. Do not access production, change checkout code, create accounts, send messages, or change incident-response policy.
- Treat redaction tokens as missing data, not as matching values. Two notes that both say [REDACTED] are not linked by that token.
- The deliverable is the weekly report. Anything beyond it goes in a separate, clearly labeled proposal that needs my approval.

First checks, before any analysis:
- Confirm the notes are present.
- Count them, state their date range, and list which fields they reliably contain: timeline, symptom, detection method, duration, customer impact, mitigation, suspected cause.
- If the notes are missing, stop and ask for them.
- If impact or duration is mostly absent, say so and rank on what the notes support.

Method:
1. Work from each note's timeline and narrative, not its title or summary line. Build a coding table with one row per incident: note ID, date, symptom, failure mechanism, contributing factors, detection (alert, customer report, or other), time to detect, time to mitigate, and impact as stated. Mark every cell as observed (quoted or directly stated) or inferred.
2. Write a short codebook that defines each failure-mechanism code by its mechanism, with one example per code. Before writing findings, re-code a sample of notes from the codebook alone and report any codes that disagree.
3. Test whether each apparent recurrence is real. For each candidate cluster, check whether the incidents share a mechanism or only a symptom, and split clusters that fail this check. Also check whether an apparent rise reflects more failures or only more or better note-taking.
4. Shape the clusters on the earlier notes in the date range. Then check whether each cluster recurs in the later notes, which were not used to define it. If too few notes exist for this split, mark the cluster "recurrence unconfirmed" instead of claiming it.
5. Analyze contributing factors per cluster. List the conditions that let each failure happen and persist (detection gaps, missing safeguards, manual steps) rather than a single root cause. Each factor cites its note IDs.
6. Rank the fix candidates by recurrence count × impact × detection gap. Show the inputs for each.
7. Run a sensitivity check: does the top pick change if each impact estimate is halved or doubled? State the result.
8. Red team the ranking. Write the strongest one-paragraph case for the second-ranked candidate. Run a short pre-mortem: "We fixed #1 and checkout failures didn't drop. Why?" Fold anything that survives into the uncertainties.

Report contents:
- A one-paragraph decision summary.
- A ranked candidate table. Each row shows: cluster, mechanism, incident count with note IDs, observed impact, detection gap, confidence, and what fixing it would and would not address.
- Uncertainties and data gaps.
- The coding table and codebook, as an appendix.
- Every claim cites note IDs and is labeled as observed or inferred.

Separate proposal (do not act on any of this):
- With my approval only: compare the report's impact ranking against an aggregate checkout failure-rate export for the same period, which I would provide.
- With my approval only: add a recurrence tracker to future weekly reports, so the team can see whether the chosen fix reduced its cluster's recurrence. Baseline and follow-up use the same case definition.
- With my approval only: draft a reproduction plan for the top-ranked failure mechanism, for an engineer to run outside production.

Judge:
- Mechanical checks:
  - Every count in the report can be rebuilt from the appendix coding table.
  - Every claim cites at least one note ID.
  - The coding disagreements and the held-out recurrence result are both reported.
  - The sensitivity result is stated.
- Independent review: a checkout engineer or incident responder who did not draft the report reviews it against this rubric:
  - (a) Can they name the fix to pick, and why, within 30 minutes?
  - (b) Spot-checking five citations, does each support its claim?
  - (c) Does each recurring cluster share a mechanism, not only a symptom?
  - (d) Are the uncertainties clear enough to decide under?
- Pass condition: all mechanical checks pass, the reviewer answers yes to (a) through (d), and no spot-checked citation fails.
- Until the review runs, label the report "draft, unreviewed."
```

**Ledger**
- `altitude`: the original outcome is a weekly report about failures. The improved outcome is a ranked, traceable fix decision the team can defend in one review. It stays within the report format, and the review is the judge.
- `depth`: coding each incident from its timeline instead of its summary, plus a codebook re-code check, makes the counts reproducible and exposes inconsistent coding.
- `depth`: testing each recurrence (same mechanism versus same symptom, more failures versus more notes) checks the belief the task rests on. Confirming clusters on later notes keeps the findings from being shaped by the same data that proves them.
- `range`: borrowed from epidemiology. A case definition plus an artifact check separates real recurrence from changes in how notes get written.
- `range`: borrowed from safety science. Contributing-factor analysis finds the conditions that let failures persist, which a single root cause misses.
- `range`: borrowed from decision analysis. The ranking formula and sensitivity check show whether the top pick holds up when impact estimates are uncertain.
- `range`: a red team step (case for the runner-up, pre-mortem) exposes risk in the decision before the team commits.
- Effect on scope and cost: no new access. The three proposal items each need your approval and would add data sharing or a new recurring workflow.

**Skipped:** none. All three lenses had a contribution the notes-only constraint allows.

**Your actions:**
- Provide the redacted notes.
- Name an independent reviewer and arrange the review, since the prompt forbids sending messages.
- Decide on each of the three proposal items.
