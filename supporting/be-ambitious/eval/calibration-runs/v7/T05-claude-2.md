```text
Analyze the support tickets I supply to identify the most common failure categories, so that whoever reads the result can rank fixes and assign each category to one owner.

Assumption: the categories exist to drive fix prioritization. Name each one by its failure mode, meaning what broke and where, at a level one team could fix. A broad label such as "account issues" fails this. A specific one such as "password-reset email not delivered" passes.
Assumption: each ticket gets exactly one primary category, so the counts sum to the total number of tickets supplied.
Assumption: tickets that report no failure (feature requests, how-to questions) go in one row named no_failure_reported. Tickets that fit no category go in a row named other. Both rows are counted.
Assumption: the output lists every category, sorted by count descending. evidence_ids holds every ticket ID in that category, separated by semicolons, with the field double-quoted.

First checks, before any coding:
- Confirm the ticket text has arrived.
- Confirm every ticket has an ID and that the IDs are unique.
- If IDs are missing or duplicated, use only tickets with unambiguous IDs. Leave out the rest. Do not invent IDs.

Method:
1. Read the full ticket body. Do not rely only on subject lines, tags, or the customer's own category. Code each ticket by the failure it describes.
2. Separate symptom from failure mode. "App is slow" is a symptom. "Search times out on large accounts" is a failure mode. Categorize by failure mode whenever the text supports it. Otherwise categorize by the most specific symptom.
3. If several tickets describe the same incident (same failure, close in time), still count each ticket. Keep them in the same category.
4. Build a codebook with open coding. Every category gets a one-line inclusion rule and an exclusion rule, so the categories are mutually exclusive and cover every ticket. The codebook is a working note and does not appear in the answer.
5. If there are at least 20 tickets, randomly split them in half:
   - Build the codebook on the first half.
   - Freeze it and code the second half with it.
   - If more than 10% of the second half lands in other, the codebook is incomplete. Revise it, then recode all tickets with the revised codebook.
6. Red-team the boundaries. For each pair of similar categories, try to reassign their tickets. Wherever a ticket fits both, merge the categories or tighten the rules.
7. Check the draft CSV before answering, and fix every failure:
   - The header is exactly category,count,evidence_ids.
   - There are exactly 3 columns.
   - Each count equals the number of IDs in its row.
   - Every supplied ticket ID appears exactly once.
   - The counts sum to the total number of tickets.
   - No customer names appear (check against names that appear in the tickets).
   - No text is copied from any ticket beyond the category label.

Requirements:
- The final answer is only CSV, with exactly this header: category,count,evidence_ids
- Use ticket IDs as evidence.
- Do not include customer names, quotes, Markdown, a preamble, or extra columns.
- Do not contact customers.
- Do not send ticket text to any external service.

With my approval only: pull extra fields for the same tickets from the ticketing system (product area, timestamps) to sharpen failure-mode and incident grouping.
With my approval only: share a random 20% sample of the tickets with a second coder for the reliability check below.

Judge:
- Mechanical: a script rerun by the owner on the CSV and the supplied ticket IDs passes every check in step 7.
- Qualitative: an authorized support or engineering lead, not the author, recodes a blind random sample of at least 20% of the tickets (or all of them if there are fewer than 20), working only from the category names. The lead also checks that each category maps to one fixing owner. This check requires the second-coder approval above.
- Pass only if every mechanical check passes, and the reviewer's agreement with the CSV is at least 0.8 (Cohen's kappa), and no category spans two owners.
- If no reviewer is available, the qualitative result remains unverified.
```

- `altitude`: The outcome moves from "a list of common categories" to "categories that each map to one fixable failure mode and one owner, ranked by count." This drives fix prioritization while keeping the 3-column CSV. There is no cost to scope.
- `depth`: The model codes from full ticket bodies rather than tags, separates symptom from failure mode, and builds a codebook with inclusion and exclusion rules. These make the counts reproducible.
- `depth`: The codebook is built on half the tickets and confirmed on the other half, with a threshold for the other row. This tests whether the categories generalize instead of fitting the sample. It is skipped below 20 tickets.
- `depth`: Self-checks cover the header, column count, count against ID count, each ID used once, the sum against the ticket total, and leakage of names or quotes. These enforce the exclusive output contract mechanically.
- `range`: Qualitative research contributes the codebook and the inter-rater reliability check (Cohen's kappa), which show whether the categories are someone else's categories too. Reliability engineering contributes the failure-mode versus symptom distinction, which exposes vague buckets. Incident management contributes same-incident grouping, which stops one outage from splitting across categories.
- `range`: A red-team pass on category boundaries exposes overlapping categories that would inflate or split counts.
- Scope/risk: Assumption lines settle single-label coding, a no_failure_reported row, an other row, and semicolon-separated IDs. The owner should correct any of these that don't match intent. Ticket text stays local.
- Skipped: none. All three lenses fit, though no hard numeric target was set beyond the kappa pass bar, because the owner set no quantitative goal.
- Owner actions:
  - Supply tickets with unique IDs.
  - Confirm or override the assumptions.
  - Approve or decline the ticketing-system field pull and sharing the sample with a second coder.
  - Name the reviewer for the qualitative judge.
