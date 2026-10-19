```text
Tell me why customers churned last month. Treat the sales team's view that onboarding is the cause as one hypothesis to test, not as the answer. The goal behind the question is assumed to be deciding which retention action to take next. Confirm or correct that assumption before you start.

Constraints (unchanged): I have no raw event logs, CRM export, or database access to share right now. Do not buy data, scrape customer information, or request production credentials. Never present an inference as an observed fact. Label every claim as observed (with its source) or proposed (unverified).

First checks, before any analysis:
1. Ask me which of these I can share without production credentials: how many accounts churned last month and how many churn in a typical month; each churned account's tenure, plan, segment, and contract or renewal date; whether each churn was voluntary (a cancellation) or involuntary (a failed payment); cancellation-reason text; support tickets or call notes from churned accounts; onboarding milestones each account reached; and any pricing, product, outage, or staffing changes around last month.
2. Ask the sales team what evidence their onboarding view rests on: specific accounts, quotes, or a pattern.
3. List what is missing. Continue only with the work the available material supports.

Method:
- Check whether last month was unusual at all. Plot monthly churn on a control chart (statistical process control). If last month falls within normal variation, say so, because the question then changes from "what broke?" to "what is our baseline churn?"
- Split churn into voluntary and involuntary before explaining it. Failed payments are a different cause with a different fix.
- Pre-register falsifiable predictions for the onboarding hypothesis before looking at the account data. If onboarding drives churn, then:
  (a) churners cluster in early tenure, which shows as an early peak on a Kaplan-Meier curve and in the hazard by tenure;
  (b) churners completed fewer onboarding milestones than retained accounts of the same tenure and segment;
  (c) cancellation reasons and tickets cite setup, activation, or time-to-value.
  Write down what result would refute each prediction.
- Compare churned accounts with retained ones, as epidemiology does in a case-control design. A trait common among churners means nothing unless it is rarer among retained accounts. Adjust for confounders such as segment, plan, and acquisition channel. If enough accounts exist, fit a Cox proportional-hazards model. Otherwise report the comparison tables and their sample sizes.
- Red-team the onboarding story. Build a competing-hypotheses table (analysis of competing hypotheses) covering pricing or packaging changes, involuntary payment failure, a product gap or outage, a competitor, a renewal-date cluster, seasonality, a single large account, and onboarding. For each, list the evidence that would separate it from the others. Then mark which evidence is present, absent, or unavailable.
- Code any cancellation text or ticket notes qualitatively. Write a codebook first, using Jobs-to-be-Done "switch" categories such as push, pull, anxiety, and habit. Report counts per code and quote verbatim. Do not paraphrase into conclusions.
- Separate development evidence from confirmation. Form hypotheses on one portion of the churned accounts, such as a random half or earlier months' churners if I can provide them. Then test them on accounts not used to form them. A claim not tested this way stays unverified.

Deliverable: a short memo for the people deciding on retention work, containing:
- whether last month was abnormal;
- the voluntary/involuntary split;
- a verdict on the onboarding hypothesis: supported, refuted, or untestable, naming the data still missing;
- the ranked competing causes, with the evidence for and against each;
- the single most decision-relevant next step.
If data is too thin for a verdict, deliver the analysis plan, the pre-registered predictions, and the exact data request instead. Do not deliver a conclusion.

With my approval only: request specific exports or summaries from internal teams (finance or billing, support, customer success). Request only aggregated or minimum-necessary fields, and never production credentials.
With my approval only: contact churned customers for exit or switch interviews, using a script I approve first.
With my approval only: design a measured pilot of the top-ranked retention action against a comparison group, with the metric, sample size, and duration fixed in advance.

Judge: the onboarding verdict and every ranked cause must rest on predictions written down before the confirming data was examined, and tested on accounts not used to form them. Report each prediction as passed, failed, or untested.
Independent review: an analyst outside the sales team, whom I name, reviews the memo against a rubric:
- Is the comparison to retained accounts present?
- Is the voluntary/involuntary split done?
- Are the alternative causes addressed?
- Is each claim labeled observed or proposed?
Pass condition: the reviewer finds no causal claim without a passed held-out prediction, and the onboarding verdict names its evidence or the missing data. Until the data arrives and the reviewer signs off, the memo is reported as unverified.
```

**Ledger**
- `altitude`: The original outcome was an explanation of why customers churned. The improved outcome is a decision on which retention action to take next, with a measured pilot behind approval. Benefit: the result drives an action that can be checked. Adds a pilot, which needs your approval.
- `depth`: Pre-registered, falsifiable predictions test the sales team's onboarding belief instead of assuming it. Benefit: the verdict can come out "refuted" as easily as "confirmed."
- `depth`: Rawer inputs (account-level tenure, milestones, cancellation text, tickets) replace sales' summary view. Survival analysis and Cox regression replace descriptive anecdotes. Benefit: tests a pattern rather than describing it. Depends on data you may not have yet.
- `depth`: Held-out confirmation of any new finding. Benefit: separates real causes from stories fit to the same data. Needs enough accounts to split.
- `range`: Statistical process control checks whether last month was abnormal at all. Benefit: avoids explaining noise.
- `range`: An epidemiology case-control comparison against retained accounts, with confounder adjustment. Benefit: exposes traits common to all customers being mistaken for causes.
- `range`: Intelligence analysis's competing-hypotheses table as a red team, plus the voluntary/involuntary split. Benefit: surfaces pricing, payment failure, outages, and renewal clusters that an onboarding focus would miss.
- `range`: Qualitative research coding with a predefined Jobs-to-be-Done codebook. Benefit: turns cancellation text into countable evidence without paraphrase bias. Optional exit interviews are behind approval, because they mean outward contact with customers.
- Skipped: none. All three lenses add a method this task lacks.
- Owner actions:
  - Tell me what data you can share without production credentials.
  - Confirm that "decide the next retention action" is the real goal.
  - Name an independent reviewer outside sales.
  - Approve or decline internal export requests, customer interviews, and the pilot.
