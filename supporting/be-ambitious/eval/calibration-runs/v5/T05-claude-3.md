```text
Analyze the support tickets I supply separately and identify the most common failure categories, so the team can see where failures concentrate and which ones to fix first.

Assumption: the result will be used to prioritize fixes. Name each category as a failure mode that one owner could fix (for example, a specific sync or billing failure), not as a symptom or a product area. Sort rows by count, highest first.
Assumption: each ticket counts once, under its single primary failure. count equals the number of distinct ticket IDs in that row's evidence_ids. evidence_ids is one quoted field with IDs separated by semicolons. Tickets that fit no recurring category go in one row named other. Confirm these conventions with me if the tickets make them ambiguous.

First checks: confirm the ticket text has arrived, that every ticket has an ID, and that the IDs are unique. Merge exact duplicates and same-incident resubmissions under their earliest ID, and note which IDs you merged in your working notes. If tickets lack IDs, stop and ask me before you produce an answer. Check whether you can run a script, such as Python's csv module, to validate the output. If you cannot, do the same checks by hand and treat them as weaker.

Method, which is qualitative content analysis with a codebook:
1. Read each full ticket body, not just the subject line. Separate what the customer reports (the symptom) from the failure that caused it. Code the cause when the text supports it. Otherwise, code the most specific failure the text shows.
2. Open coding: label each ticket in your own words. Then cluster the labels into candidate categories, the way a reliability engineer separates failure mode, cause, and effect in FMEA.
3. Write a codebook entry for each category, with inclusion and exclusion rules. Use a primary-diagnosis rule borrowed from clinical coding: a multi-issue ticket goes under the failure that blocked the customer first. Use a "not elsewhere classified" rule for other.
4. Held-out check: if there are at least 20 tickets, build the codebook on a random half and freeze it. Then code the other half. If more than 10% of the held-out tickets need a new category or end up in other, revise the codebook. Treat the categories as development evidence until the revised codebook has coded those held-out tickets cleanly. With fewer than 20 tickets, skip the split and rely on step 5.
5. Red team: for every ticket, try to argue it into a different category. A category with many plausible reassignments is ill-defined. Merge it or sharpen its rules, and recode.
6. Privacy check: category names are your own neutral wording. They contain no customer names, no quoted or near-verbatim ticket text, and no details that identify a customer. Evidence is ticket IDs only.

Requirements:
- The eventual answer must be only CSV, with exactly this header: category,count,evidence_ids
- Use ticket IDs as evidence.
- Do not include customer names, quotes, Markdown, a preamble, or extra columns.
- Do not contact customers.
- Steps 1 to 5 are working notes and never appear in the answer.

With my approval only: send a separate validation note, outside the CSV answer. It would cover held-out coverage, red-team reassignment results, merged duplicate IDs, and the codebook rules.
With my approval only: have a qualified independent reviewer recode a sample of the tickets with the codebook and report agreement, such as Cohen's kappa. This shares ticket data with that reviewer.

Judge: a validation script, or a manual check if no script can run, must pass on the final CSV:
- it parses with a standard CSV parser
- the first line is exactly category,count,evidence_ids
- every row has 3 fields
- each count equals the number of distinct IDs in its row
- every ID exists in the supplied tickets and appears in only one row
- the counts sum to the number of tickets after merging duplicates
- rows are sorted by count, highest first
- no customer name or string of 5 or more consecutive words from any ticket appears in the output
Pass condition: every check passes, and the held-out step (or the red-team step for small sets) needs no further revision. Category validity stays unverified unless the approved independent review runs, and the CSV makes no claim otherwise.
```

- `altitude`: The original outcome was a list of common categories. The improved outcome is failure-mode categories that one owner can fix, ranked by count, which supports prioritization. Rows are ordered within the existing format, and no columns are added.
- `depth`: Coding full ticket bodies with a codebook that has inclusion and exclusion rules, merging duplicates, and checking the codebook on held-out tickets makes the categories hold up beyond the tickets used to build them. This adds analysis time but changes no scope.
- `depth`: A mechanical validation script checks the parts of the CSV that can be verified: header, counts against IDs, ID existence and uniqueness, sum, ordering, and absence of names and quotes. It needs a scripting tool, with a manual fallback.
- `range`: Three borrowed methods sharpen the taxonomy. From reliability engineering, FMEA's split between mode, cause, and effect keeps symptoms out of category names. From clinical coding, the primary-diagnosis and "not elsewhere classified" rules make the counts mutually exclusive and comparable. The red-team reassignment pass exposes ill-defined categories.
- `range`: A privacy check on category wording keeps names and quoted text out even of the labels, which tightens the owner's existing prohibitions.
- Behind approval: a separate validation note, which adds an artifact outside the CSV answer, and independent-reviewer recoding, which adds delegation and shares ticket data.
- Skipped: none. All three lenses contributed.
- Owner actions:
  - Supply the tickets with IDs.
  - Confirm the conventions: one primary category per ticket, semicolon-separated IDs in a quoted field, and an other row.
  - Confirm whether a scripting tool is available.
  - Decide on the validation note and the independent review.
