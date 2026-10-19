```text
Analyze the support tickets I supply separately and identify the most common failure categories. Define each category as a failure mode that a single fix or owning team could address, so the counts can be used to decide where engineering effort goes first. (Assumption: that is the purpose of the counts.)

First checks:
- Confirm that the ticket text has been supplied, that every ticket has an ID, and that the IDs are unique.
- If the text is missing, or the IDs are missing or duplicated, say exactly what is missing and stop. Do not produce the CSV yet.
- Do not contact customers. Do not send ticket text to any external service.

Method:
1. Work from the full text of each ticket: the description, error messages, steps, and any thread. Do not work from subject lines alone.
2. Write a short internal codebook. Use qualitative-research thematic analysis: open-code a random half of the tickets (the development set) into candidate failure modes. Give each category:
   - a one-line case definition
   - inclusion rules
   - exclusion rules
3. Use the Orthogonal Defect Classification idea from software reliability engineering. Classify by underlying failure type and trigger, not by the customer's wording or the product area alone. Symptoms that share a cause belong in one category.
4. Lumping vs. splitting rule:
   - Merge categories that one fix would resolve.
   - Split a category when it needs two different fixes.
5. Assign each ticket exactly one primary category. (Assumption: one primary category per ticket, so counts are not double-counted.) Tickets that are not failures, such as how-to questions or feature requests, are excluded from the CSV. (Assumption: this matches "failure categories"; include them if I say otherwise.)
6. Apply the codebook unchanged to the held-out half. If held-out tickets need a new category or a changed definition:
   - revise the codebook
   - treat the whole set as development evidence from then on
   - consider the codebook's stability unverified
7. Red-team the ranking. Check whether the top 3 categories keep their rank under the most plausible alternative merge or split. If a rank depends on one arbitrary boundary, choose the boundary that the one-fix rule supports.

Deliverable (the eventual answer):
- It must be only CSV, with exactly this header: category,count,evidence_ids
- Use ticket IDs as evidence.
- Separate multiple IDs within evidence_ids with semicolons and no spaces, so the field never adds a column.
- Category names are short neutral labels in your own words. They contain no commas and no wording copied from tickets.
- count equals the number of IDs in that row's evidence_ids.
- Sort rows by count, descending. Break ties alphabetically by category.
- Do not include customer names, quotes, Markdown, a preamble, or extra columns.
- The codebook, held-out results, and red-team notes do not appear in the answer.

With my approval only: give me a separate validation report, outside the CSV answer. It would cover the codebook, the held-out fit, the sensitivity check, and the excluded non-failure ticket IDs.
With my approval only: share an anonymized random sample of tickets with an independent reviewer I name. The reviewer codes the sample with the codebook. Report Cohen's kappa against your labels.

Judge:
Before answering, write and run a local validator against the CSV and the supplied ticket IDs.
Pass condition: all of the following hold.
- The first line is exactly category,count,evidence_ids
- Every row parses into exactly 3 fields.
- Each count equals its number of semicolon-separated IDs.
- Every ID exists in the supplied tickets.
- No ID appears in more than one row.
- Every supplied ticket is either in the CSV or classified as a non-failure.
- No category name contains a customer name found in the tickets, or a run of 4 or more words copied verbatim from any ticket.
- The output contains no Markdown characters and no text outside the CSV.
If any check fails, fix the CSV and rerun until it passes.
The CSV has no room for qualitative validation. Held-out stability and reviewer agreement stay pending unless I approve the separate report; with reviewer agreement, the bar is kappa ≥ 0.7.
```

- `altitude`: The original outcome was common categories in whatever grouping emerges. The improved outcome is categories defined as one-fix failure modes and sorted by count, so the CSV directly ranks where to invest. Scope and format are unchanged.
- `depth`: Coding from full ticket text with a codebook (case definitions plus inclusion/exclusion rules) and one primary category per ticket makes counts reproducible and not double-counted. Two assumptions (single category per ticket, non-failures excluded) are flagged for the owner.
- `depth`: The held-out split tests whether the categories generalize beyond the tickets used to invent them. If the codebook is revised, the result is labeled unverified rather than claimed.
- `depth`: A runnable local validator acts as the mechanical judge. It checks header, field count, count/ID consistency, ID existence, no double-counting, full coverage, absence of PII and quotes, and that the output is CSV only.
- `depth` (defect fix): Comma-separated IDs inside evidence_ids would break the exact 3-column CSV. The prompt now specifies semicolon separators, and bans commas in category names.
- `range`: Software reliability engineering (Orthogonal Defect Classification) groups by failure type and trigger instead of symptom wording, which exposes shared causes.
- `range`: Qualitative research (thematic analysis, Cohen's kappa) gives a reviewer-checkable measure of whether the categories are applied consistently.
- `range` (red team): The lump/split sensitivity check tests whether the top-ranked category is real or an artifact of boundary choices.
- Skipped: a hard stretch target, because the fixed CSV has no room to report it. Deduplicating tickets into incidents was also skipped, because count must match the ticket IDs listed and incident counts would need an extra column.
- Owner actions:
  - Supply the ticket text.
  - Confirm or override the single-category and exclude-non-failures assumptions.
  - Decide on the separate validation report.
  - Decide on the independent reviewer (which shares anonymized ticket data), and name the reviewer if approved.
