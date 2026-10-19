```text
Analyze the support tickets I supply to identify the most common failure categories. Define each category so it points to one fixable failure mechanism, and make every count traceable to ticket IDs.

Assumption: the result will drive decisions about which failures to fix first. Categories therefore name what broke, not the customer's symptom wording, the trigger, or the channel.
Assumption: each failure ticket gets exactly one primary category. A ticket ID appears in one row only, and count equals the number of IDs in that row.
Assumption: tickets that report no failure (how-to questions, feature requests, inquiries with no defect) are excluded from all rows.
Assumption: rows cover every category and are ordered by count descending, then by category name. Within evidence_ids, IDs are separated by semicolons with no spaces. Category names contain no commas or quote characters.

First checks:
- Confirm the ticket text has arrived and that every ticket carries a unique ID. If text is missing, or any ticket lacks an ID or shares one, ask me before producing the answer. That question is not the eventual answer.
- Confirm whether you can run a local script to validate the CSV. If you cannot, do the same checks by hand and treat them as weaker evidence.

Method:
1. Read each ticket's full body and thread, not just the subject line or tags. Treat subject lines and customer-applied tags as claims to check against the body.
2. Split the failure tickets by a fixed rule (alternate tickets in ID order) into a development half and a held-out half. If there are fewer than 20 failure tickets, use all of them for development and treat the codebook's generality as unverified.
3. On the development half, open-code each failure. Then group the codes into a codebook. For each category, write a one-line definition, an inclusion rule, an exclusion rule, and the neighboring category it must be distinguished from. Following FMEA practice, separate failure mode (what broke) from symptom (what the customer saw) and from trigger (what they were doing), and categorize by failure mode.
4. Freeze the codebook and apply it to the held-out half without editing it. Any held-out ticket that fits no category counts as a miss. If more than 15% of held-out failure tickets are misses, revise the codebook and recode all tickets. The revised codebook's generality then stays unverified.
5. Red-team the categories:
   - Test whether the largest category lumps together mechanisms that need different fixes. Split it if its tickets divide cleanly under distinct inclusion rules.
   - Test whether each 1–2-ticket category is really a variant of a neighbor. Merge it if the neighbor's inclusion rule covers it.
   - Check whether any category's count comes from repeat tickets about one incident. Keep counting tickets, but make sure the category definition describes the mechanism, not the incident.
   - Put single-ticket failures that fit no category into a row named other.
6. Write category names as neutral paraphrases. Do not include customer names, company or account names, or quoted or near-verbatim ticket text.
7. Before answering, validate the CSV and fix and recheck any failure. Do not report these checks in the answer.
   - The header is exact.
   - Every row has 3 fields.
   - Each count equals the number of IDs in its row.
   - Every ID exists in the supplied tickets.
   - No ID appears in two rows.
   - The counts sum to the number of failure tickets.
   - No field contains any customer name from the tickets or any run of 5 or more consecutive words from a ticket.
   - Rows are in the required order.

Do not contact customers.

With my approval only: give the frozen codebook and a random sample of up to 30 failure tickets (IDs and text, without your assigned labels) to an independent reviewer subagent, which recodes them for the reliability judge below.

Output: the eventual answer is only CSV. Its first line is exactly category,count,evidence_ids. Use ticket IDs as evidence. Include no preamble, Markdown, code fences, extra columns, customer names, or quotes.

Judge (none of these results appear in the CSV):
- Mechanical: I can rerun the step 7 validator on the final CSV against the supplied tickets. Pass means every check passes.
- Generality: no more than 15% of held-out failure tickets are misses under the frozen codebook. If the threshold is exceeded or the set is too small for a split, generality is unverified.
- Reliability: the reviewer is a support-operations analyst who did not build the codebook. The reviewer assigns one codebook category to each sampled ticket without seeing the assigned labels. Agreement with the CSV's assignments is measured with Cohen's kappa. Pass means kappa ≥ 0.7. Without approval or a reviewer, category reliability is unverified.
```

- `altitude`: The original outcome was a list of frequent failure categories. The improved outcome is a set of mutually exclusive categories by failure mechanism, each mapping to a fix, so the CSV can decide fix order. Scope and format are unchanged.
- `depth`: The prompt codes from full ticket bodies, not subjects or tags. It uses a codebook with inclusion and exclusion rules, applies it frozen to a held-out half to test whether the categories generalize, and checks inter-rater reliability with Cohen's kappa. The cost is one extra coding pass. The reviewer step needs your approval.
- `depth`: A step 7 validator checks the counts, the IDs, uniqueness, and the privacy rules. This makes the format and redaction requirements checkable. It adds no output.
- `range`: From reliability engineering, FMEA separates failure mode from symptom and trigger, so categories point at fixes. A red-team pass splits lumped categories, merges slivers, and catches single-incident inflation. Neither adds scope.
- `range`: The qualitative-research codebook method is credited under the first depth line.
- Skipped: the hard-target move. This is a classification task with no quantitative improvement bar to stretch, so held-out confirmation fits better.
- Owner actions:
  - Supply the tickets with unique IDs.
  - Confirm or correct the four Assumption lines, especially single-label counting and the semicolon delimiter.
  - Approve or decline the reviewer subagent.
  - The CSV-only contract means the verification results are never reported. Rerun the validator yourself, or allow a separate report if you want to see them.
