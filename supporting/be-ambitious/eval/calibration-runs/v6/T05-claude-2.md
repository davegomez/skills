```text
Analyze the support tickets I supply to identify the most common failure categories. Build the categories from the raw ticket text so that each one names a specific failure mode an owning team could act on.

Assumption: the result will be used to decide which failures to fix first, so a category should name one failure mechanism (for example "password reset email not delivered"), not a broad product area (for example "login issues").
Assumption: count means the number of distinct tickets in the category, and it equals the number of IDs in evidence_ids.
Assumption: each ticket belongs to exactly one category. Tickets that report no failure, such as how-to questions or feature requests, are excluded and do not appear in any row.

First checks, before any analysis:
- Confirm the ticket text has been supplied.
- Confirm every ticket carries a unique ticket ID.
- List the full set of IDs.
If tickets are missing or IDs are absent or duplicated, tell me and stop before producing the CSV.

Method (working notes only, never part of the answer):
1. Open coding. Read every ticket in full. Ignore subject lines and any existing tags. Write a short neutral code for the failure each ticket reports. Code what failed, not how upset the customer is or which feature they were using.
2. Duplicate check. Flag tickets that look like the same incident reported more than once. They still count as separate tickets, but they must not create a category on their own.
3. Codebook. Group the codes into categories. For each category write an inclusion rule, an exclusion rule, and one boundary case. Separate the symptom from the failure mechanism wherever the text supports it. Keep an "Other" category only for tickets that fit no rule.
4. Reliability check. Set aside a random 20% of tickets before you write the codebook. Re-code them blind, using only the codebook rules. Compute agreement and Cohen's kappa against your original codes. If kappa is below 0.7, revise the rules and confirm on a fresh sample of tickets you have not yet used. With fewer than 30 tickets, report reliability as unverified instead.
5. Red team. Merge the two closest categories, then split the largest category. Check whether the top-3 ranking changes. If it does, tighten the boundary rules until the ranking holds or the ambiguity is resolved in the codebook. If "Other" holds more than 10% of tickets, re-code it.

Output requirements (exclusive):
- The answer is only CSV with exactly this header: category,count,evidence_ids
- One row per category, sorted by count descending.
- evidence_ids lists that category's ticket IDs separated by semicolons.
- Category names are short noun phrases with no commas, so no field needs quoting.
- Use ticket IDs as evidence. Do not include customer names, quotes, Markdown, a preamble, or extra columns.
- Do not contact customers.

With my approval only: share a sample of tickets with a named independent human reviewer, who re-codes it with the codebook as an external reliability check.

Judge: a validation script run on the final CSV must pass every check:
- the header matches exactly;
- every row has 3 fields;
- each count equals the number of IDs in its row;
- every ID is in the supplied set;
- no ID appears in two rows;
- every supplied failure ticket appears exactly once;
- rows are sorted by count descending;
- no customer name from the tickets appears;
- no run of 5 or more consecutive words is copied from any ticket.
Reliability passes at Cohen's kappa ≥ 0.7 on held-out tickets. Otherwise the categorization stays unverified, and you tell me that outside the CSV answer.
```

- `altitude`: the original outcome was a list of frequent categories. The improved outcome is categories at actionable failure-mode granularity, ready for deciding what to fix first. This fits inside the CSV contract and costs nothing in scope.
- `depth`: open coding from the full ticket text, a codebook with inclusion and exclusion rules, and a blind re-code of held-out tickets measured by Cohen's kappa. Together these make the counts reproducible rather than impressionistic. The cost is extra analysis time only.
- `depth`: a mechanical validation script enforces the output contract and the privacy rules (header, counts matching IDs, no names or copied text).
- `range`: two borrowed methods. Qualitative research contributes thematic coding and inter-rater reliability. Epidemiology contributes case definitions and the duplicate-incident check.
- `range`: a red-team merge/split test checks whether the top-3 ranking is an artifact of where the category boundaries were drawn.
- Approval-gated: an independent human reviewer would require sharing ticket data, so it stays behind your approval.
- Skipped: the hard-target move, because the task has no quantitative metric to stretch. A companion report, because the CSV-only output contract forbids one.
- Owner actions:
  - Supply the tickets and confirm they carry unique IDs.
  - Confirm that non-failure tickets should be excluded.
  - Confirm semicolons as the evidence_ids delimiter.
  - Confirm that a ticket counts in exactly one category.
  - Decide whether to approve the human reviewer.
