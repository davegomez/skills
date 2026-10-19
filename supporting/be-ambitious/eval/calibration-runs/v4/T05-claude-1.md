```text
Analyze the support tickets I supply to find the most common failure categories, so the team can decide which failures to fix first.

Requirements (unchanged):
- The final answer is only CSV with exactly this header: category,count,evidence_ids
- Use ticket IDs as evidence.
- Do not include customer names, quotes, Markdown, a preamble, or extra columns.
- Do not contact customers.

First checks:
- Confirm the ticket text has arrived, and that every ticket has a unique, parseable ID. Report any tickets without an ID.
- Check whether the tickets include agent replies or resolution notes, or only the customer's first message.
- If the input lacks IDs, stop and say what is missing. Do this outside the CSV, because without IDs there is no valid answer.

Assumptions. Apply these unless I override them before you start:
- Count only tickets that describe a failure. Exclude feature requests, how-to questions, and billing questions.
- Assign each failure ticket exactly one primary category, so the counts add up to the number of failure tickets.
- When one field holds several IDs, separate them with semicolons and quote the field per RFC 4180.
- Sort rows by count, highest first. Ties break by category name.

Method:
1. Read the raw text in full, including resolution notes when present. The resolution often shows the real cause behind what the customer described.
2. Build the taxonomy using the failure-mode-and-effects distinction from reliability engineering. Separate the symptom ("can't log in"), the failure mode ("session token expires early"), and the cause. Name each category at the most specific level the text supports, so that each category is one failure that one team could own and fix. Use the cause only when several tickets show it. Otherwise use the failure mode. Never use a symptom as a category when the text reveals a mode.
3. Develop the codebook with qualitative content-analysis practice. Do open coding on a randomly chosen development portion of about 60% of the tickets. Then write a codebook that gives each category a one-line inclusion rule and an exclusion rule. Categories must be mutually exclusive. Add one "uncategorized" row for tickets that fit no rule.
4. Code the remaining held-out tickets against the frozen codebook, without adding categories. A held-out ticket that would need a new category counts as a saturation miss. If there are more than 2 misses, or more than 10% of held-out tickets miss, revise the codebook and recode everything. In that case the held-out set has become development evidence, and the codebook is unconfirmed. If there are fewer than 30 tickets, skip the split and treat the codebook as unconfirmed.
5. Aim for "uncategorized" at 5% or less of failure tickets, achieved by sharpening the rules, not by stretching categories to fit. If one approach stalls, try the next: split an overloaded category, check the resolution notes, or rewrite the exclusion rules. Only after that, accept a higher share. The "uncategorized" row in the CSV reports whether the target was met.
6. Red-team the ranking. For the top 3 categories, try the plausible merges and splits of neighboring categories. Check whether any reasonable boundary change reorders the top 3. If it does, tighten the codebook until that boundary is defined by a rule, not by your judgment call.
7. Privacy pass. Category names must be generic failure descriptions. They must not contain customer names, organization names, email addresses, or any phrase copied from ticket text.

With my approval only: after the CSV answer, send a separate short validation note covering the codebook rules, the held-out saturation result, and the red-team outcome. The CSV itself stays clean.
With my approval only: give the codebook and tickets to an independent reviewer, such as another model instance or a named colleague, to blind-recode a sample. This shares ticket data.
With my approval only: save the codebook and validation script as files for reuse on future ticket batches.

Judge:
- Mechanical check: run a script on the final CSV, kept outside the ticket directory and run with python -I. It passes only if all of the following hold:
  - The header is exactly category,count,evidence_ids.
  - Every row has 3 fields.
  - Every count equals the number of IDs in that row.
  - Every ID exists in the supplied input and appears in exactly one row.
  - The counts add up to the number of failure tickets.
  - No field contains a customer name, an email address, or any run of 5 or more consecutive words from the ticket text.
  - The output contains nothing outside the CSV.
- Saturation check: held-out misses are within the threshold in step 4. Otherwise the codebook is reported as unconfirmed.
- Pass condition: every mechanical check passes. The saturation and red-team results are unverified unless the approved validation note or independent recoding is run. Report the 5% stretch target as met or missed from the "uncategorized" row.
```

- `altitude`: The original outcome is a list of common categories. The improved outcome is a ranked list in which each category is something one team can own and fix, so the CSV directly supports deciding what to fix first. Same format and scope.
- `depth`: Coding from the raw text and resolution notes, a mutually exclusive codebook, and one primary label per ticket make the counts additive and trustworthy.
- `depth`: Confirming the codebook on held-out tickets turns the taxonomy from an untested proposal into a tested one. With small sets, it falls back to "unconfirmed".
- `depth`: The ≤5% "uncategorized" stretch target is reported inside the approved format through the "uncategorized" row.
- `depth`: The mechanical CSV/ID/privacy script is a red/green judge for the format and evidence rules the owner set.
- `range`: The reliability engineering symptom/mode/cause split stops categories from merely restating complaints.
- `range`: Red-teaming the top-3 boundaries exposes cases where the ranking depends on an arbitrary category cut.
- Approval lines: the validation note adds a message after the CSV. Independent recoding shares data. Saved files create a reusable workflow. Each needs approval.
- Skipped lenses: none.
- Owner actions:
  - Supply the tickets with IDs.
  - Confirm or override the four assumptions: failure-only scope, one primary label, semicolon ID delimiter, sorting.
  - Decide on the validation note, the independent reviewer, and saved artifacts.
