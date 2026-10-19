```text
Draft this week's report on recurring checkout failures so the team can choose what to fix. Assumed goal, to confirm: the team leaves one meeting having picked fixes, each backed by evidence and an expected payoff, and next week's report can show whether recurrence dropped.

Boundaries (unchanged):
- Inspect only the redacted incident notes I provide.
- Do not access production, change checkout code, create accounts, send messages, or change incident-response policy.
- Anything beyond the report goes in a separate proposal, clearly labeled as needing my approval, never in the report body.

First checks, before analysis:
- List the notes provided, the date range they cover, and the fields redaction removed.
- Say whether there are enough incidents across enough time to call anything "recurring".
- Note any gaps that limit a conclusion (missing timestamps, impact, or mitigation) and carry them into the report as stated limits.
- Do not fill gaps with guesses.

Method:
1. Work from the raw notes, not summaries. Turn each note into one row of an incident table, keyed by note ID. Columns: time, checkout step affected, symptom and error class, how it was detected (alert, staff, customer), mitigation, duration, and stated customer impact. Mark each field as observed in the note, inferred, or unknown.
2. Write a written case definition of "checkout failure incident" and apply it to every note. Next week's counts then mean the same thing as this week's.
3. Group incidents into failure modes using a codebook. Each code gets a definition and inclusion/exclusion rules. Use contributing factors, not a single root cause.
4. Test whether the failures really recur, before ranking anything:
   - Build the codebook on the earlier half of the notes by time.
   - Code the later half without changing the codebook.
   - Report how many later incidents fit existing modes and how many need new ones. Modes that hold up on the later half are confirmed. Modes seen only in the half used to build them are labeled unconfirmed.
5. Rank failure modes in the style of an FMEA (failure mode and effects analysis), scoring each from the notes:
   - Severity: customer impact.
   - Occurrence: count, and the interval between recurrences.
   - Detectability: share of incidents found by customers rather than by alerts.
   With small counts, report raw counts and ranges, not rates or percentages that imply precision.
6. For each of the top modes, give fix options rather than a single recommendation. For each option, state:
   - what it would prevent, citing note IDs;
   - its relative effort as a team estimate to fill in, not a fact;
   - the cost of waiting one more week, based on observed frequency and impact.
   State which unknown, if resolved, would most change the ranking.
7. Red-team the top-ranked mode. Write the strongest alternative explanation and say what in the notes supports or weakens it. Alternatives include reporting bias (only customer-visible failures get notes), redaction hiding a shared cause, or one bad week inflating the count.

Report structure, in this order:
1. Decision summary: top modes, options, and the open questions the team must answer. One page.
2. Evidence per mode: incidents cited by note ID, separating observed facts from inferences.
3. Recurrence baseline per mode, for next week's comparison.
4. Limits from redaction and data gaps.
5. Appendix: incident table, case definition, and codebook.

With my approval only: a separate proposal for any step beyond the report, such as fixes, monitoring or alerting changes, automating this weekly report, or policy suggestions.
With my approval only: request less-redacted notes or additional data sources, if the first checks show the provided notes cannot support a ranking.

Judge:
- Traceability check (run it yourself and report results): every factual claim in sections 1–3 cites one or more note IDs. Each cited ID exists, and each cited note supports the claim. Pass = zero uncited or unsupported claims.
- Recurrence test: report the number of later-half incidents that fit and do not fit the codebook. Label every mode as confirmed or unconfirmed.
- Independent review (pending; I arrange it, you do not contact anyone): a team member who did not write the draft codes a random sample of at least 10 notes using only the codebook. Report agreement with your coding. Pass = at least 80% agreement on failure mode. Until that review happens, label the clustering as unverified by independent review.
- Owner's bar: in the review meeting, the team can choose what to fix without needing information the report lacks. Record any such requests as gaps for next week.
```

**Ledger**

- **`altitude`:** Moves the outcome from "a report the team reads" to "a report built to drive one fix decision, plus a recurrence baseline so next week can check whether the chosen fixes worked." It stays within the report; nothing outside it is acted on.
- **`depth`:** An incident table keyed by note ID, with observed/inferred/unknown labels, replaces a prose summary. This makes every claim auditable, at no added scope.
- **`depth`:** The earlier/later split tests the belief the task rests on, that these failures recur, using evidence not used to build the categories. This guards against clusters that are artifacts of how they were drawn.
- **`depth`:** Counts and ranges instead of rates. This avoids false precision from small samples.
- **`range`:**
  - Epidemiology's case definition keeps week-over-week counts comparable.
  - Qualitative research's codebook and inter-coder agreement make the clustering checkable by someone other than the author.
  - Reliability engineering's FMEA ranks by severity, occurrence, and detectability. It surfaces failures that customers find before alerts do.
  - Decision analysis frames fixes as options with cost of delay and value of information. This shows what to learn before committing.
  - A red-team step on the top mode exposes reporting bias or redaction effects that could misdirect the fix.
- **`range` scope:** Any recommendation beyond the report goes in a separate proposal behind approval, as the owner required. Requests for more data are also behind approval.
- **Skipped:** None of the three lenses. A hard stretch target was not chosen, because the report has no numeric bar to exceed; the recurrence baseline enables one next week.
- **Owner actions:**
  - Provide the redacted notes and say what period they cover.
  - Arrange an independent reviewer to code a sample of at least 10 notes.
  - Confirm the assumed goal (a fix decision in one meeting, plus a baseline for next week).
  - Decide on any separate proposal or request for less-redacted data.
