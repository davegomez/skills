# Rewritten prompt: weekly checkout-failure report

**Intended result:** a weekly report that lets the team choose which recurring checkout failure to fix next. The team acts on it, and you approve anything beyond it.

**Explicit requirements:**
- Draft a weekly report on recurring checkout failures.
- Inspect only the redacted incident notes you provide.
- Do not access production.
- Do not change checkout code.
- Do not create accounts.
- Do not send messages.
- Do not change incident-response policy.
- Anything beyond the report goes in a separate proposal that needs your approval.

**Assumptions:**
- The team's decision is constrained by limited engineering time.
- The report will recur weekly, so its method should be repeatable from week to week.
- The notes may record dates, symptoms, suspected causes and impact, but this is unconfirmed.

**Lenses:**
- **Altitude: fit.** The report exists to drive a fix decision. The rung that reduces failures directly would need production access and code changes, so it goes into the gated proposal.
- **Depth: fit.** A ranking built from summaries can merge different causes under one symptom, which would send the team to the wrong fix.
- **Range: fit.** The report has to persuade a group to commit scarce time under uncertainty.

```text
Draft this week's report on recurring checkout failures. Its purpose is to let our team choose what to fix next, so build it around a ranked set of fix options with evidence, not a narrative of incidents. (Assumption: the team has limited engineering capacity and will pick one to three items; this report will be repeated weekly, so the method must be reusable.)

HARD LIMITS (unchanged from the owner):
- Inspect only the redacted incident notes I provide. Use no other data source.
- Do not access production, change checkout code, create accounts, send messages, or change incident-response policy.
- If you think we should move beyond the report, put that in a separate proposal marked "Needs owner approval". Do not act on it.
- Do not try to reverse or infer redacted content. Mark redaction-caused gaps as gaps.

FIRST CHECKS (report results before analysis):
1. Confirm the notes have been provided. List the files, the date range they cover, and the incident count. If none are provided, stop and ask.
2. Inventory which fields the notes actually contain: timestamps, duration, symptom, suspected or confirmed cause, affected step (cart, payment, confirmation, …), impact (failed orders, minutes, users), and remediation. For each method below that a missing field would require, mark the method as unavailable rather than estimating the field.
3. State whether "this week" means the latest 7 days in the notes or a different window, and use earlier notes only as baseline.

METHOD:
1. Raw incident table. Build one row per incident from the notes themselves, not from any summary inside them. Record the note ID and the source quote for every coded field. Save it as a local file alongside the report.
2. Codebook and case definitions (from epidemiology and qualitative research). Write explicit rules for:
   - what counts as a "checkout failure"
   - what makes two incidents "the same recurring failure"
   Cluster by underlying cause or failing component where the notes support it, not by symptom alone. Where the notes give only a symptom, label the cluster "symptom-only, cause unconfirmed". Record every judgment call.
3. Recurrence and trend (from epidemiology). For each cluster, report:
   - count this week versus the baseline weekly rate
   - an epi-curve-style timeline
   - whether this week's count is distinguishable from normal variation, using a Poisson rate comparison or an exact test, with the interval stated
   With small counts, say "not distinguishable" instead of calling it a trend.
4. Prioritization (from reliability engineering and decision analysis).
   - Rank clusters with a Pareto view of frequency × impact, using only impact fields that exist.
   - Add an FMEA-style detectability note: how each failure was noticed, and how late.
   - For each top option, state the expected benefit if fixed, the evidence strength (confirmed cause / suspected / symptom-only), and what one additional piece of information would most change its rank (value of information).
5. Red team before finalizing.
   - Run a pre-mortem on the top-ranked option: "We fixed it and failures didn't drop. Why?"
   - Check artifact explanations: changes in note-taking or reporting volume, one long incident split into many notes, and redaction hiding a shared cause.
   - State which conclusions survive.
6. Held-out check (if the notes span at least 3 weeks).
   - Freeze the codebook and the cluster ranking using only the earlier weeks.
   - Then classify the most recent week with the frozen codebook. Report how many of its incidents fall into the previously top-ranked clusters, and how many need new clusters.
   - This tests whether the ranking predicts recurrence rather than describing the past.

REPORT STRUCTURE:
1. One-paragraph decision summary: the recommended options and why.
2. Ranked options table: cluster, count this week vs baseline, impact, evidence strength, supporting note IDs, key unknown.
3. Trends, with uncertainty.
4. What changed since last week (or "first edition").
5. Red-team findings.
6. Data gaps and redaction limits.
7. Appendix: the codebook and the incident table.

Label every statement as either OBSERVED (directly in a cited note) or INFERRED (your interpretation). Proposed causes stay INFERRED unless a note confirms them.

SEPARATE PROPOSAL (optional, approval-gated, not executed). If the evidence warrants work beyond the report, write it as a separate document headed "Needs owner approval". Candidates:
- a blind second-coder check of the codebook by a team member
- structured fields added to future incident notes, so cause and impact are captured
- post-fix recurrence monitoring for whichever option the team picks
For each candidate, state the access, people, and cost it would need. Do not contact anyone or change any process.

JUDGE AND PASS CONDITIONS:
- Traceability (required): every count, rank, and OBSERVED claim in the report is reproducible from the incident table, and every row cites a note ID. Pass = 100%. Spot-check 10 random claims yourself and report the result.
- Decision-readiness (required): each ranked option has a count, impact or an "impact unavailable" flag, evidence strength, note IDs, and a key unknown. Pass = no option missing a field.
- Held-out prediction: report the share of last-week incidents covered by the frozen top clusters, and the number of new clusters. There is no threshold; report the measured result. If there are fewer than 3 weeks of notes, mark it "not run: insufficient history".
- Coding reliability: aim for at least 0.8 Cohen's kappa between your codes and a blind second coder. This needs owner approval and a reviewer the owner arranges. Until it runs, mark it UNVERIFIED and say so in the report.
```

## Ledger

- `altitude`: the original task was "a weekly report about recurring failures". The chosen outcome is a decision-ready ranking of fix options with stated evidence strength and the key unknown for each. Benefit: the team can choose a fix in one meeting. Scope is unchanged.
- `altitude`: production-dependent work (post-fix monitoring, better note fields) is moved into an approval-gated proposal, per your rule. It is not executed.
- `depth`: a raw incident table with source quotes replaces reliance on in-note summaries. Every claim becomes traceable. No new access is needed.
- `depth`: clustering by cause, with symptom-only clusters flagged, avoids fixing a symptom shared by different causes.
- `depth`: the held-out week check tests whether the ranking predicts recurrence. It needs at least 3 weeks of notes; otherwise it is reported as not run.
- `range`: from epidemiology, case definitions, an epi curve and a Poisson rate comparison keep small weekly counts from being presented as trends.
- `range`: from reliability engineering and decision analysis, a Pareto view with FMEA detectability and value of information shows each option's benefit and what would change its rank.
- `range`: from qualitative research, a written codebook makes the weekly report repeatable, and inter-rater agreement makes it checkable. The kappa target needs a second coder.
- `range`: the red-team pre-mortem and artifact check expose reporting-volume or redaction artifacts before the team commits time.
- Skipped lenses: none. All three improve the decision or its judge without changing the explicit requirements.

## Your actions

- Provide the redacted notes, ideally covering at least 3 weeks so the held-out check can run.
- Confirm what "this week" means.
- Decide whether to arrange a blind second coder. Until then, coding reliability stays unverified.
- Approve or decline anything in the separate proposal.
