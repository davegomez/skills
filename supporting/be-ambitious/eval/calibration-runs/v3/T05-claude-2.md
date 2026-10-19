```text
Analyze the support tickets I supply to identify the most common failure categories, coded at the level of the underlying failure mode, so that each category points to something an owner could investigate and fix.

First checks, before any coding:
- Confirm the ticket text has been supplied and that every ticket carries a ticket ID. If tickets are missing or any lack IDs, stop and tell me which. Do not substitute quotes or names for IDs.
- Note any fields that hold customer names or signatures so the final checks can screen for them.

Method:
1. Work from the raw ticket text, not from subject lines or any pre-assigned tags. Set aside tickets that describe no failure, such as how-to questions or feature requests. Do not count them.
2. Build a codebook through qualitative content analysis. Use open coding on a development half of the tickets, then merge the codes into categories. Give each category a short neutral label, a one-sentence definition, and inclusion and exclusion rules. Separate symptom from failure mode, as in failure mode and effects analysis (FMEA): "login fails" is a symptom, while "expired SSO token not refreshed" is a failure mode. Use the most specific failure-mode level that the ticket text supports. Use the symptom level only where the text gives no cause.
3. Assign each failure ticket to exactly one category, its primary failure mode. That way the counts sum to the number of failure tickets. (Assumption: single-label coding. Switch to multi-label only if I say so.)
4. Freeze the codebook, then code the held-out half. A category that first appears in the held-out half means the codebook was not saturated. Revise it and re-code all tickets. Do this at most twice.
5. Red-team the largest category. Check whether it splits into two or more distinct failure modes with different fixes. If it does, split it. Then check whether any two small categories share one failure mode. If they do, merge them.
6. Sort the rows by count, descending.

Output requirements (unchanged):
- The eventual answer is only CSV, with exactly this header: category,count,evidence_ids
- Use ticket IDs as evidence. Separate multiple IDs within the evidence_ids field with semicolons, no spaces, unless I specify otherwise.
- No customer names, no quotes, no Markdown, no preamble, no extra columns.
- Do not contact customers.
- The codebook, the split, and the check results are working material. They stay out of the answer.

With my approval only: have an independent reviewer recode a random sample of at least 30 tickets, blind to your labels, using only the frozen codebook, and compute Cohen's kappa. This shares ticket text with another reviewer.
With my approval only: after the CSV, produce a separate prioritization of the top categories by impact. This would be a different deliverable.

Judge: before answering, run a script over the CSV, the ticket set, and the screened name fields, and fix the CSV until every check passes. Pass condition:
- The first line equals "category,count,evidence_ids" exactly.
- Every row parses as exactly 3 fields under RFC 4180.
- count is an integer equal to the number of distinct IDs in its evidence_ids.
- Every ID exists in the supplied tickets, and no ID appears in more than one row.
- Rows are sorted by count, descending.
- No category label contains a customer name or a run of 5 or more consecutive words copied from any ticket.
- The output has no text outside the CSV.
The qualitative judge is the reviewer's kappa: 0.7 or higher passes. It is not part of the CSV. It stays unverified unless I approve the review and ask for its result separately.
```

- `altitude`: Original outcome: count the common failure categories. Improved outcome: count failure-mode categories that an engineering owner can act on, with symptom and cause separated and non-failure tickets excluded. No scope or format change.
- `depth`: A codebook built through open coding, then frozen and tested for saturation on held-out tickets, turns ad hoc labels into categories that hold up on tickets not used to create them.
- `depth`: The mechanical judge (header, field count, count-to-ID match, ID existence, uniqueness, sort order) catches format and evidence errors that a CSV-only answer would otherwise hide.
- `range`: FMEA from reliability engineering separates symptom from failure mode, so categories point to fixes.
- `range`: A privacy screen checks labels against name fields and for verbatim runs of 5 or more words. This enforces the "no names, no quotes" rule mechanically instead of by eye.
- `range`: The red-team split and merge test on the largest category guards against one catch-all label inflating "most common."
- `range`: An independent blind recode with Cohen's kappa is the qualitative judge. It sits behind an approval line because it shares ticket text.
- `altitude`: An impact prioritization would follow the CSV. It sits behind an approval line because it is a separate deliverable.
- Skipped: a hard stretch target. The CSV-only deliverable has no room to report one.
- Owner actions:
  - Supply the tickets and confirm each has an ID.
  - Confirm single-label coding and semicolon-separated IDs.
  - Say whether "most common" means all categories or a top-N cutoff.
  - Approve or decline the independent recode and the impact prioritization.
