```text
Draft a weekly report about recurring checkout failures so our team can choose what to fix.
Assumption: the team will choose in one prioritization discussion, so the report leads with a ranked, evidence-backed shortlist of fix candidates and the open questions that could change that ranking.
Assumption: "recurring" means the same underlying cause appears in two or more incidents, not only the same symptom.

Method:
- Work from the full text of each redacted incident note, not from summaries. Give each note an ID and extract one record per note: date and time, checkout step affected (cart, address, shipping, payment, confirmation, other), symptom, stated or suspected cause, detection source (alert, customer report, staff), duration, stated customer impact, and mitigation. Mark any field the notes lack or redaction hides as "unknown". Do not infer or reconstruct redacted content.
- Build a short codebook of failure modes using thematic coding. Give each mode a definition and an inclusion/exclusion rule, and group notes by cause, not symptom. Derive the codebook from the earlier half of the notes by date, then freeze it. Apply it unchanged to the later half. Report how many later notes fit an existing mode, how many needed a new one, and which modes appear in both halves. A mode seen only in the half used to define it stays labeled "unconfirmed".
- Rank the modes with an FMEA-style table. Score occurrence (count of notes), severity (from stated duration and impact), and detection (how late, and by whom, the failure was caught), each 1–5, and show the scoring rule. A failure first caught by customers scores worse on detection than one caught by an alert.
- For each top mode, write a contributing-factor chain (5 whys, stopping where the notes stop). Name system conditions, not "human error", and list the candidate fixes the evidence supports.
- Red-team the top three modes. For each, state the strongest alternative explanation and whether the notes rule it out. Examples: the same symptom from different causes, one noisy incident counted several times, or uneven note-taking across teams.
- For each candidate fix, state which mode it targets, its expected effect, its confidence (high, medium, or low, with a reason), and the one unanswered question that would most change its rank.
- Label every claim as observed (cite note IDs or quote) or inferred.
- Report structure: a one-page summary with the ranked shortlist; the FMEA table; per-mode evidence and contributing factors; red-team results; the holdout result; data gaps; an appendix of extracted records.

Requirements:
- Inspect only the redacted incident notes I provide.
- Do not access production, change checkout code, create accounts, send messages, or change incident-response policy.
- If you think we should move beyond the report, make that a separate proposal needing my approval, and do not act on it.

With my approval only: a recurring week-over-week tracker that applies the frozen codebook to each new week's redacted notes, to show whether the chosen fixes reduce recurrence of their target modes. Present it only as the separate proposal and take no step toward setting it up.
First check: the redacted notes are provided. Record the note count, the date range, and which fields survived redaction. With fewer than 6 notes, say so, skip the date split, and label every mode "unconfirmed".
First check: a member of our team other than the report's author is available to review and is permitted to see these redacted notes. I will give them the notes and report, since you send nothing. If no such reviewer is available, deliver the report marked "unverified".
Judge: a member of our team other than the author, given the same redacted notes, checks that (1) every claim cites note IDs and is labeled observed or inferred; (2) every mode reported as recurring has at least 2 notes sharing a stated cause, not only a symptom; (3) recoding up to 10 randomly chosen notes (all if fewer) with the frozen codebook, without seeing the author's codes, matches the author's mode on at least 80% of them; (4) the shortlist order follows from the shown FMEA scores; (5) the holdout result is reported with counts, or its omission is explained by the note count; (6) no information beyond the redacted notes was used, redaction gaps are marked "unknown", and anything beyond the report appears only as a separate unexecuted proposal. Pass only if every criterion is met.
```

**Ledger**
- `altitude`: The original outcome was a report about failures. The improved outcome is a ranked fix shortlist with confidence levels and rank-changing questions, built for the team's actual choice. No scope change.
- `altitude`: The week-over-week tracker shows whether the chosen fixes worked. It sits behind approval as a separate proposal only, and it adds a recurring workflow if approved.
- `depth`: Records are extracted from raw note text, with redaction gaps marked "unknown" instead of guessed. This stops invented causes and adds no access.
- `depth`: The codebook is defined on earlier notes and confirmed on later ones. This tests whether "recurring" modes are real instead of artifacts of how they were found. With few notes, modes stay "unconfirmed".
- `range` (reliability engineering): The FMEA table ranks by occurrence, severity, and detection. It shows costly or customer-detected failures that a raw frequency count hides.
- `range` (safety science): Contributing-factor chains that exclude "human error" point fixes at system conditions instead of blame.
- `range` (decision analysis): Each fix gets a confidence label and the one question that would most change its rank. This tells the team what to find out before committing.
- `range` (red team): Alternative explanations for the top three modes expose miscounted or misattributed recurrences before the team acts on them.
- `range` (qualitative research): The reviewer blindly recodes a sample, which checks that the clusters are reproducible and not one author's reading. It needs a team reviewer's time.
- Skipped: the hard-target move, because this is not a quantitative improvement request and the report has no metric to stretch.
- Owner actions: provide the redacted notes; name a team reviewer, confirm they may see the notes, and pass them the material; decide whether to approve the tracker proposal.
