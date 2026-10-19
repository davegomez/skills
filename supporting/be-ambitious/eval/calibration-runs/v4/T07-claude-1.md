```text
Draft this week's report on recurring checkout failures so the team can choose what to fix. Build it from the raw redacted incident notes I provide, not from summaries of them. The report should end in a fix decision the team can make in one meeting: a ranked shortlist, a recommended first fix, a runner-up, and the evidence that would change that call.

Boundaries (all hold throughout):
- Inspect only the redacted incident notes I provide. Do not try to recover redacted content or infer identities. Where redaction hides something the ranking depends on, say so.
- Do not access production, change checkout code, create accounts, send messages, or change incident-response policy.
- The deliverable is a draft report for me. Anything beyond the report goes in a separate proposal that needs my approval.

First checks, before analysis:
- Count the notes and record the date range they cover.
- Check whether the notes span more than one week. Note-level held-out confirmation and week-over-week comparison need earlier weeks; if the notes cover only this week, mark both as unavailable.
- List the fields the notes reliably contain: timestamp, symptom, affected step, payment method or region if unredacted, duration, customer impact, suspected cause, and remediation.
- Name any missing dependency and continue only with the work the notes support.

Method:
1. Build a coding table with one row per note. Cite each note by its ID. Write a short codebook that defines each code: symptom, checkout step, failure mode, suspected cause, and impact. Start from an epidemiology-style case definition of what counts as one "checkout failure," so counts are comparable.
2. Test the belief the task rests on: that these failures are recurring problems with shared causes. Group notes by mechanism, not by symptom. For each cluster, state whether the notes show a shared cause (observed), suggest one (proposed), or only share a symptom. Split clusters that merely look alike.
3. If earlier weeks are available, find clusters on the earlier notes. Then confirm each cluster on this week's notes, which were not used to define it. A cluster that does not hold on the held-out notes is labeled unconfirmed.
4. Separate signal from noise in the weekly counts. Use a c-chart or a Poisson rate comparison against prior weeks to flag which clusters are rising, which are steady background, and which are one-offs. With only one week of notes, report counts and say no trend can be judged.
5. Rank the clusters with an FMEA-style score: severity × occurrence × detectability. Score each factor only from what the notes show, and show the inputs. Add rough fix effort as a separate column. Label effort and impact as estimates, since there is no production data.
6. Decision analysis:
   - Recommend a first fix and a runner-up.
   - Run a sensitivity check: which score change would swap their order?
   - List the value-of-information gaps: what one fact, if learned, would most change the ranking?
7. Red team: write a short pre-mortem ("we fixed #1 and failures didn't drop — why?"). Make the strongest case for the runner-up. Note any bias that redaction or note-taking habits could introduce. For example, incidents that get written up more often look more frequent.

Report contents:
- One-paragraph summary with the recommendation.
- Ranked cluster table with note-ID citations, codes, score inputs, effort estimates, and observed/proposed labels.
- Trend notes, or a statement that trend data is unavailable.
- Sensitivity check and information gaps.
- Pre-mortem and the case for the runner-up.
- Appendix: codebook and full coding table.

Separate proposal (a different document, nothing run):
With my approval only: obtain read-only production checkout metrics so cluster impact can be measured instead of estimated.
With my approval only: after the team ships the chosen fix, track same-cause recurrence in later weeks' notes against this week's baseline, using the same case definition.
With my approval only: suggest structured fields for future incident notes that would make clustering more reliable, for whoever owns incident-response practice to consider. Do not draft policy changes.

Judge and pass condition:
- Traceability (mechanical): every count, cluster, and ranking claim cites note IDs. Recomputing the counts from the coding table reproduces the report's numbers exactly.
- Coding reliability (independent): a teammate I name recodes a random sample of at least 10 notes blind to the codebook's results, or all notes if there are fewer than 10. The draft passes if agreement on failure-mode codes reaches Cohen's kappa ≥ 0.7. Until the recode runs, label coding reliability unverified.
- Held-out confirmation: each cluster called recurring is confirmed on notes not used to define it, or labeled unconfirmed.
- Decision readiness: the report names a first fix, a runner-up, and what would swap them.
The draft passes when traceability holds, every cluster is labeled confirmed or unconfirmed, and the decision section is complete. Report the kappa result once the recode runs.
```

**Ledger**
- `altitude`: The outcome rises from "a weekly report about recurring failures" to "a fix decision the team can make in one meeting" (recommendation, runner-up, flip conditions). Same deliverable and scope. Fewer actual failures remains behind approval in the separate proposal.
- `depth`: Raw notes are coded with a codebook and cited by note ID. This makes counts reproducible, at the cost of more drafting time.
- `depth`: The "recurring" premise is tested by mechanism rather than symptom, and confirmed on held-out notes. This needs notes from more than one week; otherwise clusters are labeled unconfirmed.
- `range`: Epidemiology contributes a case definition, so counts compare like with like.
- `range`: Statistical process control (c-chart or Poisson comparison) separates rising clusters from background noise. It needs prior weeks.
- `range`: Reliability engineering contributes FMEA scoring, which makes the ranking's inputs explicit and debatable.
- `range`: Decision analysis contributes the sensitivity check and value-of-information gaps, which show how firm the recommendation is.
- `range`: Red teaming contributes the pre-mortem, the case for the runner-up, and the redaction/reporting-bias check. These expose decision risk.
- `depth`/judge: A blind recode by a teammate checks coding reliability. You arrange it; I send no messages.
- Proposal items (approval only): read-only production metrics (new access), post-fix recurrence tracking (new recurring workflow), and suggested note fields for the incident-practice owner (no policy edits).
- Skipped: none. The hard-target move was skipped because the report has no baseline metric to stretch against without production data.
- Owner actions:
  - Provide the redacted notes and their date range, including prior weeks if you want trend and held-out checks.
  - Name a teammate for the blind recode.
  - Decide on each proposal item.
