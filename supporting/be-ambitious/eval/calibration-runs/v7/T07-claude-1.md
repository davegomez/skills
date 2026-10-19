```text
Draft this week's report on recurring checkout failures so our team can choose what to fix. Build the report from the redacted incident notes I provide. Make it a decision document: it ranks fix candidates and shows, for each one, which failures it would address, the evidence for that, and what remains unknown.

Assumption: the team will discuss the report in a short meeting and pick one or two fixes, so the top of the report must support that choice on its own.
Assumption: "recurring" means the same underlying cause appears more than once. Failures that only share a symptom do not count as recurring until the evidence supports a shared cause.

Constraints (all mandatory):
- Inspect only the redacted incident notes I provide. Do not try to recover redacted content, and do not use any other source.
- Do not access production, change checkout code, create accounts, send messages, or change incident-response policy.
- The deliverable is a draft report. Anything beyond the report goes in a separate proposal section that needs my approval. Do not act on anything in that proposal.

First checks, before any analysis:
- List the notes received. Record each note's date range and which fields it contains: timestamps, symptom or error text, impact (orders, duration, users), detection method, mitigation, suspected cause.
- Note where redaction removes information needed to tell incidents apart or to judge impact.
- Say whether the notes cover this week, and whether any earlier notes exist that could show recurrence across weeks.
- For any gap, name what is missing. Then continue only with conclusions the notes support, and mark each affected conclusion as limited by that gap.

Method:
1. Work from the raw notes, not from their titles or summaries. For each incident, record a structured row with these fields:
   - note ID
   - start and end times, if present
   - symptom
   - checkout stage (cart, payment, confirmation, etc.)
   - impact
   - how it was detected
   - how it was mitigated
   - contributing factors as stated in the note
   - your proposed cause, marked as either "stated in note" or "inferred"
   Keep this table as an appendix. Every count in the report must be reproducible from it.
2. Code incidents with a written codebook that defines each symptom and cause category, including what is excluded from each. If there are enough notes, draft the codebook on the earlier half, then code the later half without changing the codebook. Report how many later-half notes did not fit any category. If the codebook had to change to fit them, treat the clusters as provisional.
3. Test whether the failures are really recurring. For each candidate cluster:
   - Separate "same symptom" from "same cause."
   - Cite the note evidence that links the cases.
   - Give the strongest alternative explanation for why they might be unrelated.
   - Flag any case where redaction could be merging distinct incidents.
4. Rank the clusters with an FMEA-style score: severity (impact per occurrence), occurrence (count and spacing), and detectability (how the failures were noticed and how long that took, from note timestamps where present).
   - Show the three components separately, not just the product.
   - Write counts as counts. With small numbers, do not claim trends or rates beyond what the counts show.
5. For each top-ranked cluster, describe one or more fix options. For each option, give:
   - which incidents it would have prevented or shortened, by note ID
   - what it would not address
   - what the team would need to estimate before choosing it, such as effort and risk
   Do not estimate engineering effort or production behavior that the notes do not document. Mark those as inputs the team must supply.
6. Pre-mortem: assume the team picks the top option and checkout failures continue. Write the most likely reason, drawn from evidence in the notes. Put it next to the recommendation.

Report structure:
1. A one-page decision summary: the ranked options, the evidence for each, its confidence, and the open questions.
2. The cluster analysis with note citations.
3. Limits, including the redaction gaps and coverage gaps from the first checks.
4. Appendices: the incident table and the codebook.
5. A separate section titled "Proposal (needs approval)." It contains only the "With my approval only" items below that the evidence supports, each with its rationale and expected benefit.

With my approval only: make this report a recurring weekly workflow, using a standard incident-note template so that recurrence can be tracked across weeks.
With my approval only: request specific additional fields or less-redacted notes, named in the report's limits section, where the analysis shows they would change a ranking.
With my approval only: any investigation, fix, monitoring, or policy change that follows from the ranked options.

Judge: a checkout engineer or incident lead on the team who did not draft the report reviews it against the criteria below. Pass only if every criterion is met.
(a) Each count in the report matches the incident table.
(b) Each claim about a cluster or its cause cites note IDs, and "stated in note" versus "inferred" is labeled correctly on a spot-check of at least five rows, or all rows if there are fewer than five.
(c) Every recurring cluster shows evidence of a shared cause, and its alternative explanation is addressed.
(d) Reading only the decision summary, the reviewer can name the top options, what each would and would not fix, and what remains unknown.
(e) No content draws on sources other than the provided notes, and the proposal section contains only approval-gated items.
Report the result of the held-out codebook check. Until the reviewer has run this check, the report is an unverified draft.
```

- `altitude`: The original outcome was a weekly report. The improved outcome is a decision document that ranks fix options, lists what each option would and would not fix, and names the inputs the team still has to supply. This targets the choice the report exists to drive. It adds no scope or access.
- `depth`: The report builds a structured table from the raw notes, so every count can be checked by recomputing it. This adds a modest amount of effort and no new access.
- `depth`: The report tests the task's own premise by separating "same symptom" from "same cause." This keeps the team from funding a fix for a shared symptom that has several unrelated causes.
- `depth`: The report checks whether its clusters are real. It drafts the codebook on the earlier half of the notes and codes the later half without changes, which shows whether the categories hold up on notes that did not shape them. With very few notes, this check is weak, and the report says so.
- `range`: Qualitative research contributes the codebook with explicit inclusions and exclusions. Without it, category labels tend to drift to fit whichever notes were read first.
- `range`: Reliability engineering contributes FMEA scoring, which keeps severity, occurrence, and detectability separate. A single count would hide a rare but costly failure, or one that is slow to detect, behind frequent minor ones.
- `range`: The pre-mortem and the requirement to state alternative explanations act as a red team on the top recommendation. They expose decision risk before the team commits engineering time.
- Approval-gated: The prompt lists three items for the proposal section. They are a recurring workflow with a note template, requests for more fields or less-redacted notes, and any follow-on fix, monitoring, or policy work. The prompt only describes them; none happen unless you approve.
- Skipped: The hard-target move doesn't fit, because this isn't a quantitative improvement request and the report has no metric to stretch. A decision-analysis cost model doesn't fit either, because fix costs aren't in the notes. Those costs are left as team inputs.
- Owner actions:
  - Provide the redacted notes, and say whether earlier weeks' notes are in scope for judging recurrence.
  - Name the reviewer who will act as the judge.
  - Decide on any items in the proposal section after the report is drafted.
