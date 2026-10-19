```text
Analyze the support tickets I supply to identify the most common failure categories, as a ranked list a team can use to decide which failure to fix first.

Requirements (fixed):
- The final answer is only CSV with exactly this header: category,count,evidence_ids
- Use ticket IDs as evidence. No customer names, no quotes, no Markdown, no preamble, no extra columns.
- Do not contact customers.

First checks:
- Wait for the ticket text. Confirm that every ticket has a visible, unique ID. Never invent or infer an ID. Leave out any ticket without an ID, and do not mention it in the answer.
- Assumption: evidence_ids holds semicolon-separated IDs with no spaces, and count equals the number of IDs in that row. If any ID contains a comma or semicolon, quote the field per RFC 4180.
- Assumption: each ticket gets one primary category, so no ID appears in two rows. If many tickets clearly report two separate failures, put each ID under its dominant failure and keep the rule consistent.

Method:
1. Case definition (from epidemiology). Before you code anything, write an inclusion rule for what counts as a failure: something broke, errored, was lost, or did not do what it promised. Leave out how-to questions, feature requests, billing preferences, and praise. Apply the rule to every ticket before categorizing.
2. Failure-mode categories (from reliability engineering / FMEA). Name each category by the failure mode, the thing that went wrong and could have one owner and one fix, for example "password reset email not delivered". Do not use a product area ("login issues") or a customer emotion. Keep category names short and descriptive. They must not contain customer wording.
3. Codebook with a development/confirmation split (from qualitative content analysis).
   - Shuffle the failure tickets by ID and set aside about one third as a confirmation set.
   - Use open coding on the remaining two thirds to draft categories. For each category, write a one-line inclusion rule and a one-line exclusion rule that separates it from its nearest neighbor.
   - Apply the frozen codebook to the confirmation set. If confirmation tickets need a new category, or more than about 1 in 10 fit poorly, revise the codebook, recode all tickets, and treat the result as development evidence only.
   - Assumption: put failure tickets that fit no category with at least 2 tickets into one row named "other".
4. Red-team the ranking. Try the most plausible merges and splits of neighboring categories. If the top 3 order changes under a merge or split you cannot rule out with the codebook rules, tighten the rules and recode until the ranking holds.
5. Sort rows by count descending. Break ties by category name.

With my approval only: have an independent second coder blind-code a sample of tickets with the codebook. That coder can be a separate agent or a person, and the step shares ticket text with them. Compute Cohen's kappa against your coding.

Judge (run before emitting; none of this appears in the answer):
- Mechanical validator. If code execution is available, use a CSV parser script; otherwise check line by line. Pass when all of these hold:
  - The first line is exactly category,count,evidence_ids.
  - Every row has exactly 3 fields.
  - count is an integer equal to the number of IDs in its row.
  - Every ID exists in the supplied tickets, and no ID repeats across rows.
  - No customer name from the tickets appears in the output.
  - No run of 5 or more consecutive words from any ticket appears in the output.
  - The output has no text outside the CSV.
- Confirmation check. Pass when the frozen codebook covers the confirmation set without new categories. A revised codebook leaves category accuracy unverified.
- Approved reviewer only. Pass at kappa ≥ 0.7. Without the reviewer, the category assignments rest on your own coding and stay unverified.

Output: emit only the CSV.
```

- `altitude`: The original outcome is a list of common categories. The improved outcome is a ranked list of fixable failure modes, sorted by count, that directly supports "what do we fix first". It keeps the same three columns and no extra output.
- `depth`: The method changes are an explicit codebook with inclusion and exclusion rules, one primary code per ticket, and a development/confirmation split. Together they make the counts reproducible and test whether the categories hold beyond the tickets that shaped them. There is no scope or access change.
- `depth`: The mechanical validator checks the header, field count, count against IDs, that IDs exist and don't repeat, names, quotes, and stray text. It enforces every format and privacy requirement before emitting. It runs locally, and its results stay out of the CSV.
- `range`: An epidemiology-style case definition keeps non-failures such as questions and feature requests out of the counts.
- `range`: FMEA failure-mode naming yields categories that one team could own.
- `range`: A red-team merge/split sensitivity test catches a top-3 ranking that comes from arbitrary category boundaries.
- `range`: An independent second coder with kappa ≥ 0.7 is the only qualitative judge of category accuracy. It requires approval because it means delegation and sharing ticket text.
- Skipped lenses: none.
- Owner actions:
  - Supply the ticket text with IDs.
  - Confirm or override the assumptions: semicolon-separated IDs, one category per ticket, and an "other" row.
  - Approve or decline the second coder.
  - Note that the fixed CSV format has no channel for reporting validation results. Without the reviewer, category accuracy stays unverified.
