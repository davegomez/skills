```text
Goal: Identify the most common failure categories in the support tickets I will supply, so that the counts can be used directly to decide which failures to fix first. Assumption (inferred): the CSV feeds engineering and support prioritization, so each category should name a failure mechanism a team could fix, not a symptom or a customer mood.

First checks, before any analysis:
- Confirm the ticket text has been supplied and that every ticket has a unique ID. If no ticket text exists, ask me for it and stop. If some tickets lack IDs or IDs repeat, ask me how to handle them before producing the CSV. A ticket without an ID cannot serve as evidence.
- Do not contact customers. Do not send ticket text to any external service. Do all work locally.

Method:
1. Read the raw ticket text, not any summaries or titles alone. Split the tickets by ID into two halves: a development half and a held-out half.
2. Build the codebook on the development half with qualitative open coding, then axial coding. Tag each ticket with the observed failure. Merge tags into categories. For each category, write a case definition with inclusion and exclusion rules.
3. Separate the failure mode from its effect, as in FMEA. "Can't log in" is an effect. "SSO token expiry not refreshed" is a mode. Name categories at the mode level whenever the ticket text supports it. If the text shows only the effect, name the category at the effect level and do not guess a cause.
4. Assign each ticket exactly one primary category, so the counts sum to the number of tickets classified. Put tickets that fit no definition in a single catch-all category, such as "unclassified". Do not force them into other categories.
5. Check the codebook against the held-out half. Apply it unchanged. If the held-out tickets need a new category, the codebook is incomplete: revise it and re-code all tickets.
6. Check for clusters, using the epidemiology idea of a single outbreak. Look for many tickets reporting one incident, such as the same outage window or error. Keep them in their mechanism category. Record the cluster in your working notes so that a spike is not mistaken for a chronic failure.
7. Red-team the ranking. Take the 10% of tickets that were hardest to place and try to argue each one into its next-best category. Note whether the order of the top 3 categories would change. If it would, tighten those case definitions and re-code.
8. Aim for reliability: Cohen's kappa of at least 0.8 between your first coding and a second blind pass that uses only the written codebook. If kappa falls short, find the confused category pairs, sharpen their definitions, and re-code. Try at least two revisions before accepting a lower value.

Output requirements, unchanged:
- The eventual answer must be only CSV, with exactly this header: category,count,evidence_ids
- Use ticket IDs as evidence.
- Do not include customer names, quotes, Markdown, a preamble, or extra columns.
- Format assumptions (I may override them): one row per category, sorted by count from highest to lowest. List the IDs within a row separated by semicolons. Enclose a field in double quotes if it contains a comma, a quote, or a semicolon, per RFC 4180. Category names are short plain-English labels and must contain no customer-identifying text.
- The codebook, kappa, clusters, and red-team notes are working material. They must not appear in the answer. With my approval only, you may also produce a separate validation note covering kappa, held-out results, clusters, and ranking stability. That note must contain no customer names or quotes.

Judge (run before answering; give the answer only when every check passes):
- The header matches "category,count,evidence_ids" byte for byte, and every row has exactly 3 fields when parsed as CSV.
- In every row, count equals the number of IDs in evidence_ids.
- Every evidence ID appears in the supplied tickets, no ID appears in two rows, and the sum of the counts equals the number of tickets with valid IDs.
- The output contains no customer names, no text copied from the tickets beyond IDs, and no Markdown.
- The held-out half was coded without adding a category, or the codebook was revised and all tickets were re-coded.
- Kappa is at least 0.8, or two revisions were attempted. Report the measured value in the approved validation note, or state it on request. Do not put it in the CSV.
Pass condition: all structural checks pass. Kappa and stability are the stretch target. If they are missed, the CSV can still be given, but the reliability is unverified until reported.
```

- `altitude`: The original task asked for the most common failure categories. The chosen outcome is categories cut at the fixable-mechanism level, so the counts can drive prioritization directly. The CSV-only constraint blocks recommendations, so the lift happens inside the category definitions.
- `depth`: Coding from raw tickets, a codebook with case definitions, and one primary category per ticket make the counts sum correctly and stay comparable. There is no scope or access effect.
- `depth`: A development/held-out split plus a second blind coding pass with a kappa ≥ 0.8 target turns "these categories feel right" into a measured result. This costs extra analysis time only.
- `depth`: The structural judge (header, field count, count matches IDs, IDs exist, no ID in two rows, sum matches) catches the most likely errors in a CSV-only answer.
- `range`: Reliability engineering (FMEA) separates the failure mode from its effect, so categories point at causes rather than symptoms.
- `range`: Epidemiology case definitions and cluster detection stop one outage from looking like a chronic top failure.
- `range` (red team): Re-arguing the ambiguous tickets tests whether the top-3 ranking holds before anyone acts on it.
- Skipped: none. All three lenses fit, because the output drives prioritization decisions and depends on judgment calls that can be measured.
- Owner actions:
  - Supply the ticket text with unique IDs.
  - Confirm or override the format assumptions: semicolon-separated IDs, sort order, and the single "unclassified" row.
  - Decide whether to approve a separate validation note. Without it, the kappa and stability results stay internal and are not visible in the CSV-only answer.
