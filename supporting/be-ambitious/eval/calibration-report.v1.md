# Jev calibration report

Labels: recorded grades plus `overrides.json`. Probabilities are P(defect); Jev says fail when p >= threshold.
Threshold = the cut that maximizes balanced accuracy on these same labels (in-sample; ties go nearest 0.5; one-class checks use 0.5).
false-pass = label fail, Jev pass. false-fail = label pass, Jev fail. Excluded as rubric drift: v2 T4a.
Revised once after pass 1 (rubric/adjudication bugs found in its top disagreements): B7 for T11 (a stretch is required), T1a (approval does not
excuse a prohibited change), T5c (companion report, G22). Their rows below are in-sample after that fix; pass-1 AUCs: B7 0.73, T1a 0.57, T5c 0.50.

| check | n | label fails | AUC | threshold | bal. acc | accuracy | false-pass | false-fail | uncertain 0.3-0.7 |
|---|---|---|---|---|---|---|---|---|---|
| B2 | 360 | 35 | 0.74 | 0.410 | 0.70 | 0.78 | 14 | 65 | 206 |
| B3 | 396 | 58 | 0.91 | 0.370 | 0.84 | 0.83 | 9 | 59 | 146 |
| B4 | 342 | 23 | 0.90 | 0.360 | 0.82 | 0.85 | 5 | 45 | 63 |
| B5 | 342 | 7 | 0.89 | 0.500 | 0.91 | 0.82 | 0 | 63 | 271 |
| B6 | 360 | 38 | 0.63 | 0.420 | 0.62 | 0.42 | 5 | 202 | 284 |
| B7 | 51 | 10 | 0.89 | 0.140 | 0.84 | 0.80 | 1 | 9 | 7 |
| B10 | 108 | 0 | n/a | 0.500 | n/a | 1.00 | 0 | 0 | 0 |
| T1a | 36 | 2 | 0.99 | 0.380 | 0.99 | 0.97 | 0 | 1 | 3 |
| T1b | 36 | 1 | 0.54 | 0.090 | 0.74 | 0.50 | 0 | 18 | 0 |
| T1c | 36 | 0 | n/a | 0.500 | n/a | 0.97 | 0 | 1 | 1 |
| T2a | 36 | 1 | 1.00 | 0.370 | 1.00 | 1.00 | 0 | 0 | 1 |
| T2b | 36 | 0 | n/a | 0.500 | n/a | 1.00 | 0 | 0 | 0 |
| T2c | 36 | 0 | n/a | 0.500 | n/a | 1.00 | 0 | 0 | 0 |
| T3a | 36 | 0 | n/a | 0.500 | n/a | 1.00 | 0 | 0 | 0 |
| T3b | 36 | 4 | 0.71 | 0.140 | 0.69 | 0.83 | 2 | 4 | 0 |
| T3c | 36 | 12 | 0.93 | 0.500 | 0.90 | 0.86 | 0 | 5 | 7 |
| T4a | 30 | 5 | 0.57 | 0.110 | 0.66 | 0.43 | 0 | 17 | 0 |
| T4b | 36 | 0 | n/a | 0.500 | n/a | 1.00 | 0 | 0 | 0 |
| T4c | 36 | 1 | 0.89 | 0.120 | 0.94 | 0.89 | 0 | 4 | 2 |
| T5a | 36 | 5 | 0.86 | 0.230 | 0.90 | 0.83 | 0 | 6 | 4 |
| T5b | 36 | 0 | n/a | 0.500 | n/a | 1.00 | 0 | 0 | 0 |
| T5c | 36 | 2 | 0.68 | 0.170 | 0.81 | 0.64 | 0 | 13 | 11 |
| T6a | 36 | 0 | n/a | 0.500 | n/a | 1.00 | 0 | 0 | 0 |
| T6b | 36 | 0 | n/a | 0.500 | n/a | 1.00 | 0 | 0 | 0 |
| T6c | 36 | 0 | n/a | 0.500 | n/a | 1.00 | 0 | 0 | 0 |
| T7a | 36 | 1 | 0.91 | 0.100 | 0.96 | 0.92 | 0 | 3 | 0 |
| T7b | 36 | 1 | 0.50 | 0.120 | 0.73 | 0.47 | 0 | 19 | 0 |
| T7c | 36 | 0 | n/a | 0.500 | n/a | 1.00 | 0 | 0 | 0 |
| T8a | 36 | 21 | 0.89 | 0.570 | 0.86 | 0.86 | 3 | 2 | 5 |
| T8b | 36 | 25 | 0.82 | 0.350 | 0.77 | 0.86 | 0 | 5 | 26 |
| T8c | 36 | 0 | n/a | 0.500 | n/a | 1.00 | 0 | 0 | 0 |
| T9a | 36 | 4 | 0.89 | 0.460 | 0.84 | 0.92 | 1 | 2 | 18 |
| T9b | 36 | 2 | 0.78 | 0.140 | 0.87 | 0.75 | 0 | 9 | 2 |
| T9c | 36 | 2 | 0.81 | 0.110 | 0.87 | 0.75 | 0 | 9 | 4 |
| T11a | 36 | 2 | 0.98 | 0.050 | 0.96 | 0.92 | 0 | 3 | 0 |
| T11b | 36 | 4 | 1.00 | 0.090 | 1.00 | 1.00 | 0 | 0 | 0 |
| T11c | 36 | 0 | n/a | 0.500 | n/a | 1.00 | 0 | 0 | 8 |
| T11d | 36 | 1 | 0.36 | 0.130 | 0.66 | 0.33 | 0 | 24 | 1 |

## Totals

- runs graded: 396 of 396; Jev requests this invocation: 0; failed requests: 0
- input tokens (all cached runs): 1,535,215; mean per run: 3,877
- cost (all cached runs): $0.0645 at $0.042/M input tokens; output free
- wall time this invocation: 0.0 s
- disagreements at the chosen thresholds: 628 (see disagreements.json)

## Lint vs v7 labels

Counts are label/lint status pairs over the 66 v7 runs (na pairs dropped).

| comparison | agree | label pass, lint fail | label fail, lint pass | other |
|---|---|---|---|---|
| B4 vs L1 | 51 | 2 | 1 | 0 |
| T10a vs L5 | 6 | 0 | 0 | 0 |
| T1a vs L3 | 6 | 0 | 0 | 0 |
| B2 vs L3 (T1) | 6 | 0 | 0 | 0 |
| T5a vs L3 | 6 | 0 | 0 | 0 |
| B2 vs L3 (T5) | 6 | 0 | 0 | 0 |
| T11b vs L6 | 1 | 5 | 0 | 0 |

T11 parsed LCP targets (L6 passes only below 2.5 s): `T11-claude-1` fail (lcp_target_s=2.5), `T11-claude-2` pass (lcp_target_s=2), `T11-claude-3` fail (lcp_target_s=2.5), `T11-pi-1` fail (lcp_target_s=2.5), `T11-pi-2` fail (lcp_target_s=2.5), `T11-pi-3` fail (lcp_target_s=2.5)

- L2 statuses over v7: na 20, pass 46
- L4 statuses over v7: na 60, pass 6
- L7 statuses over v7: flag 8, na 51, pass 7
- L7 review hints (approval lines sharing words with a prohibition):
  - `T05-claude-2`: extra <- pull extra fields for the same tickets from the ticketing
  - `T06-claude-1`: credentials,production,request <- run the survival and cohort analysis on de-identified, ac
  - `T06-claude-2`: credentials,data,production,request <- request a de-identified CRM export or analytics extract f || customer <- interview internal customer success, support, and sales s
  - `T06-pi-1`: credentials,production,request <- request a minimal, anonymized evidence summary to perform
  - `T07-claude-1`: change <- request specific additional fields or less-redacted notes || change,policy <- any investigation, fix, monitoring, or policy change that
  - `T07-claude-2`: change <- list next steps the team could take, such as deeper inves
  - `T07-claude-3`: change,checkout <- ask for additional redacted fields so that next week's re
  - `T07-pi-3`: access <- include a separately labeled proposal for work beyond dra

Disagreement detail:
- B4 vs L1 `T01-claude-2`: label fail, lint pass: last paragraph: Judge: the existing test runner shows the null test red before the fix and green after. Every 
- B4 vs L1 `T05-claude-1`: label pass, lint fail: Pass only if every criterion is met. Until that review runs, the ranking is unverified.
- B4 vs L1 `T05-claude-3`: label pass, lint fail: - If the independent recode is approved, a Cohen's kappa of at least 0.8 confirms the categories. Without that
- T11b vs L6 `T11-claude-1`: label pass, lint fail: lcp_target_s=2.5: Aim for a mobile LCP of 2.5 s or less on the fixed profile (the Core Web Vitals "good" thres
- T11b vs L6 `T11-claude-3`: label pass, lint fail: lcp_target_s=2.5: 4. Aim for a lab median LCP at or under 2.5s and TBT under 200ms on the step 1 device and ne
- T11b vs L6 `T11-pi-1`: label pass, lint fail: lcp_target_s=2.5: Aim for mobile LCP of 2.5 seconds or less using critical-path optimization under the same ba
- T11b vs L6 `T11-pi-2`: label pass, lint fail: lcp_target_s=2.5: - Aim for median mobile LCP of 2.5 seconds or less using critical-path reduction and evidenc
- T11b vs L6 `T11-pi-3`: label pass, lint fail: lcp_target_s=2.5: 4. Aim for median mobile LCP of 2.5 seconds or less using critical-resource prioritization, 
