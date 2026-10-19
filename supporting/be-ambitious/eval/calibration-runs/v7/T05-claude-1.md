```text
Analyze the support tickets I supply to identify the most common failure categories, so the team can see which underlying failures generate the most tickets and decide what to fix first.

First checks, before any analysis:
- Confirm the ticket text has been supplied. If not, ask me for it and wait.
- Confirm every ticket has an ID and that no ID repeats. If any ticket lacks an ID or an ID repeats, ask me how to handle it before continuing. Do not invent IDs.

Method:
1. Read the full text of every ticket, not just subject lines. Decide whether each ticket reports a failure. A failure means something did not work as the customer expected. Exclude how-to questions, feature requests, and billing inquiries that report no malfunction. Exclude them from all rows.
2. Build a codebook from a random half of the failure tickets (open coding, as in grounded-theory qualitative research). Each category gets a one-line definition plus inclusion and exclusion rules.
3. Code the underlying failure, not the symptom the customer describes. This follows the clinical-coding "underlying cause" rule and SRE postmortem practice, which separate cause from symptom. For example, "can't log in" may really be an expired session, an SSO misconfiguration, or an outage. Assign each ticket exactly one primary category so the counts are mutually exclusive.
4. Apply the codebook unchanged to the held-out half. If more than about 10% of held-out failure tickets fit no category, the codebook is incomplete. Revise it, then recode all tickets. Treat categories you created after seeing held-out tickets as development evidence: keep them only if they hold across both halves.
5. Red-team the ranking:
   - Check whether each of the top categories is really two distinct causes that should be split.
   - Check whether any two categories are the same cause that should be merged.
   - Adjust the categories and recount where a split or merge is warranted.
6. Put failure tickets that fit no category in a final row named other.
Assumption: counts are ticket counts. Repeat reports from the same customer each count as separate tickets.
Assumption: tickets that report no failure do not appear in the output.

Output requirements, which are exclusive:
- The eventual answer must be only CSV, with exactly this header: category,count,evidence_ids
- One row per category, sorted by count descending, with other last.
- Category names are short, neutral, snake_case labels of the failure (for example, payment_webhook_timeout). Names contain no commas, customer names, or ticket wording.
- evidence_ids lists that category's ticket IDs, separated by semicolons, with no spaces.
- count equals the number of IDs in that row.
- Use ticket IDs as evidence.
- Do not include customer names, quotes, Markdown, a preamble, or extra columns.
- Do not include the codebook or any notes in the answer.
- Do not contact customers.

Judge, mechanical (run before emitting the CSV; regenerate until it passes):
- The header matches exactly.
- Every row has 3 fields.
- Every ID exists in the supplied tickets.
- No ID appears in more than one row.
- count equals the ID count in each row.
- No customer name or run of 5+ consecutive words from any ticket appears in the output.
- Nothing appears outside the CSV.

Judge, qualitative: a support lead or analyst I designate, not the author, reads 3 randomly chosen evidence tickets from each of the top 3 categories. They check that:
(a) each ticket fits its category's label;
(b) the label names an underlying failure rather than a symptom;
(c) no two of the top 3 categories describe the same cause.
Pass only if every criterion is met. Until that review runs, the ranking is unverified.
```

- `altitude`: The original outcome was a list of common categories. The improved outcome is a cause-level ranking ordered by count, so it can directly drive the decision about what to fix first. The output stays within the fixed three columns.
- `depth`: Coding from the full ticket text, a codebook with inclusion and exclusion rules, and a single primary category per ticket make the counts mutually exclusive and reproducible.
- `depth`: Building the codebook on one half and validating it on the held-out half tests whether the categories generalize, with no change to the output.
- `range`: The clinical-coding and SRE "underlying cause, not symptom" rule stops one root cause from splitting across symptom categories.
- `range`: The split/merge red-team checks the consequential claim of which category is most common, since lumping and splitting can flip the ranking.
- `depth`: Mechanical checks enforce the exact header, valid IDs, counts that match the ID lists, and no names or quotes. They add no output.
- Format: Semicolon-separated IDs within the field and an `other` row are assumptions. Change them if you want different conventions.
- Skipped: No "With my approval only" lines were needed, because every change fits inside the existing scope. A severity or impact ranking was skipped because it would need extra columns, which you prohibited.
- Owner actions:
  - Supply the ticket text with unique IDs.
  - Say how to handle any tickets without IDs.
  - Designate the reviewer for the qualitative judge.
