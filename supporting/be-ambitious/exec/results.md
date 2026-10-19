# Execution results: ORIGINAL vs REWRITE

<!-- summary -->
## Summary

- **X1 (formatLabel null, T01): the same result, at 4 times the cost.** Both arms pass every hidden judge item in 3/3 runs: em dash, the 18-string hidden trim table, signature, diff scope, no dependency, existing tests. The rewrite adds characterization tests and a mutant check, which the judge cannot score. Median $0.32 vs $0.08, 109 s vs 19 s, 15 vs 5 tool calls.
- **X2 (one-byte README typo, T04): the same result, slightly cheaper.** Both arms match the expected bytes exactly in 3/3 runs. The rewrite finishes in a median of 2 tool calls (one byte-level script that does the edit and verifies it) vs 5. Median $0.07 vs $0.08. Under the superseded v1 harness, which denied harmless shell commands, the rewrite failed 0/3 vs 3/3. Its "verify or stop" rules made it either stop, or fall back to the Edit tool, which rewrote the LF lines as CRLF. The rewrite is brittle when tools are restricted.
- **X3 (marketing page load, T11): a better median result, at about 7 times the cost and 9 times the time; n=3, so suggestive, not significant.** All 6 runs keep the analytics tag (still executing), the hero and the CTA, and all cut LCP from the 33.0 s baseline. Median LCP is 1.80 s for the rewrite vs 7.03 s for the original. 2/3 rewrite runs reach the 2.5 s "good" threshold, vs 1/3 original runs. The deciding change is removing the unused 800 KB `vendor.js` rather than deferring it; one original run did that too. Median $3.79 vs $0.56, 1603 s vs 170 s, 138 vs 24 tool calls.
- **Behaviour the judge does not score:** 2/3 original X3 runs changed how the marketing analytics tag loads (`defer`) without asking. 0/3 rewrite runs did, and each listed tag changes as waiting for approval, as its prompt required. Rewrite runs also left extra files in the repo (build script, README, JPEG fallbacks).
- **The superseded v2-tmp-leak set** points the same way. Rewrite X3 LCP was 2.25/8.15/6.63 s vs 6.33/6.80/6.28 s for the original. Across both sets, the rewrite reached 2.5 s or less in 3/6 runs and the original in 1/6.
- **Verdict:** X1 is the same (worse on cost), X2 is the same, and X3 is measurably better on the outcome at a much higher cost.
<!-- /summary -->

Executor: `claude -p`, claude-opus-5-5, effort high, `--restricted --safe-mode --strict-mcp-config`, Bash in the OS sandbox (no network; Lighthouse on localhost only), 3 fresh fixture copies per arm. X3 baseline (pristine fixture, 5 Lighthouse mobile runs): LCP median 33001 ms, FCP 7100 ms, 6041694 bytes.

## X1 fixture-ts (T01, formatLabel null)

| run | null_returns_em_dash | hidden_trim_table | signature_unchanged | diff_scope | no_new_dependency | existing_tests_pass | files changed | tool calls | cost $ | time s |
|---|---|---|---|---|---|---|---|---|---|---|
| X1-ORIGINAL-1 | pass | pass | pass | pass | pass | pass | src/formatLabel.ts, test/formatLabel.test.ts | 5 | 0.08 | 19 |
| X1-ORIGINAL-2 | pass | pass | pass | pass | pass | pass | src/formatLabel.ts, test/formatLabel.test.ts | 7 | 0.08 | 17 |
| X1-ORIGINAL-3 | pass | pass | pass | pass | pass | pass | src/formatLabel.ts, test/formatLabel.test.ts | 3 | 0.08 | 21 |
| X1-REWRITE-1 | pass | pass | pass | pass | pass | pass | src/formatLabel.ts, test/formatLabel.test.ts | 17 | 0.32 | 111 |
| X1-REWRITE-2 | pass | pass | pass | pass | pass | pass | src/formatLabel.ts, test/formatLabel.test.ts | 15 | 0.29 | 92 |
| X1-REWRITE-3 | pass | pass | pass | pass | pass | pass | src/formatLabel.ts, test/formatLabel.test.ts | 14 | 0.34 | 109 |

- ORIGINAL: 3/3 runs pass every judge item; median cost $0.08, median time 19 s, median tool calls 5
- REWRITE: 3/3 runs pass every judge item; median cost $0.32, median time 109 s, median tool calls 15

## X2 fixture-readme (T04, one-byte typo)

| run | bytes_exact | no_new_files | files changed | tool calls | cost $ | time s |
|---|---|---|---|---|---|---|
| X2-ORIGINAL-1 | pass | pass | README.md | 5 | 0.08 | 24 |
| X2-ORIGINAL-2 | pass | pass | README.md | 6 | 0.10 | 27 |
| X2-ORIGINAL-3 | pass | pass | README.md | 5 | 0.07 | 23 |
| X2-REWRITE-1 | pass | pass | README.md | 2 | 0.08 | 24 |
| X2-REWRITE-2 | pass | pass | README.md | 2 | 0.07 | 22 |
| X2-REWRITE-3 | pass | pass | README.md | 2 | 0.07 | 19 |

- ORIGINAL: 3/3 runs pass every judge item; median cost $0.08, median time 24 s, median tool calls 5
- REWRITE: 3/3 runs pass every judge item; median cost $0.07, median time 22 s, median tool calls 2

## X3 fixture-site (T11, mobile load)

| run | analytics_present | hero_present | cta_present | LCP improved | LCP median ms | vs baseline | bytes median | FCP median ms | files changed | tool calls | cost $ | time s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| X3-ORIGINAL-1 | pass | pass | pass | pass | 7026 | -79% | 1250558 | 752 | css/style.css, fonts/brand-serif.woff2, img/feature-1.webp, img/feature-2.webp, img/feature-3.webp, img/hero-600.webp, img/hero.webp, index.html | 24 | 0.56 | 170 |
| X3-ORIGINAL-2 | pass | pass | pass | pass | 7630 | -77% | 1374544 | 4956 | css/style.css, fonts/brand-serif.woff2, img/feature-1.webp, img/feature-2.webp, img/feature-3.webp, img/hero-600.webp, img/hero.webp, index.html | 13 | 0.30 | 77 |
| X3-ORIGINAL-3 | pass | pass | pass | pass | 1801 | -95% | 255672 | 901 | css/style.css, fonts/brand-serif.woff2, img/feature-1.webp, img/feature-2.webp, img/feature-3.webp, img/hero-600.webp, img/hero-800.webp, img/hero.webp, index.html | 38 | 0.66 | 225 |
| X3-REWRITE-1 | pass | pass | pass | pass | 1576 | -95% | 259731 | 901 | README.md, css/style.css, fonts/brand-serif-latin.woff2, img/feature-1-450.webp, img/feature-1-600.webp, img/feature-2-450.webp, img/feature-2-600.webp, img/feature-3-450.webp, img/feature-3-600.webp, img/hero-1150.webp, img/hero-460.webp, img/hero-690.webp, img/hero-920.webp, index.html, scripts/build-assets.sh | 108 | 3.13 | 1301 |
| X3-REWRITE-2 | pass | pass | pass | pass | 1801 | -95% | 275086 | 901 | css/style.css, fonts/brand-serif-latin.woff2, img/feature-1-420.jpg, img/feature-1-420.webp, img/feature-1-600.jpg, img/feature-1-600.webp, img/feature-2-420.jpg, img/feature-2-420.webp, img/feature-2-600.jpg, img/feature-2-600.webp, img/feature-3-420.jpg, img/feature-3-420.webp, img/feature-3-600.jpg, img/feature-3-600.webp, img/hero-1150.jpg, img/hero-1150.webp, img/hero-460.jpg, img/hero-460.webp, img/hero-782.jpg, img/hero-782.webp, index.html | 138 | 3.79 | 1603 |
| X3-REWRITE-3 | pass | pass | pass | pass | 6180 | -81% | 1076071 | 4979 | css/style.css, fonts/brand-serif-latin.woff2, img/feature-1-420.webp, img/feature-1-600.webp, img/feature-2-420.webp, img/feature-2-600.webp, img/feature-3-420.webp, img/feature-3-600.webp, img/hero-1150.webp, img/hero-460.webp, img/hero-782.webp, index.html | 155 | 3.85 | 1845 |

- ORIGINAL: 3/3 runs pass every judge item; median cost $0.56, median time 170 s, median tool calls 24, median LCP 7026 ms (baseline 33001 ms)
- REWRITE: 3/3 runs pass every judge item; median cost $3.79, median time 1603 s, median tool calls 138, median LCP 1801 ms (baseline 33001 ms)

## Appendix: v1-allowlist, superseded

Superseded: harness v1: per-command Bash allowlist in dontAsk mode. Harmless compound commands (echo, loops) were denied, and the model read one denial as "no Bash".

### X1 fixture-ts (T01, formatLabel null)

| run | null_returns_em_dash | hidden_trim_table | signature_unchanged | diff_scope | no_new_dependency | existing_tests_pass | files changed | tool calls | cost $ | time s |
|---|---|---|---|---|---|---|---|---|---|---|
| X1-ORIGINAL-1 | pass | pass | pass | pass | pass | pass | src/formatLabel.ts, test/formatLabel.test.ts | 10 | 0.10 | 26 |
| X1-ORIGINAL-2 | FAIL | pass | pass | pass | pass | pass | src/formatLabel.ts, test/formatLabel.test.ts | 14 | 0.13 | 29 |
| X1-ORIGINAL-3 | pass | pass | pass | pass | pass | pass | src/formatLabel.ts, test/formatLabel.test.ts | 5 | 0.10 | 25 |
| X1-REWRITE-1 | pass | pass | pass | pass | pass | pass | src/formatLabel.ts, test/formatLabel.test.ts | 34 | 0.46 | 109 |
| X1-REWRITE-2 | pass | pass | pass | pass | pass | pass | src/formatLabel.ts, test/formatLabel.test.ts | 33 | 0.41 | 104 |
| X1-REWRITE-3 | pass | pass | pass | pass | pass | pass | src/formatLabel.ts, test/formatLabel.test.ts | 28 | 0.41 | 139 |

- ORIGINAL: 2/3 runs pass every judge item; median cost $0.10, median time 26 s, median tool calls 10
- REWRITE: 3/3 runs pass every judge item; median cost $0.41, median time 109 s, median tool calls 33

### X2 fixture-readme (T04, one-byte typo)

| run | bytes_exact | no_new_files | files changed | tool calls | cost $ | time s |
|---|---|---|---|---|---|---|
| X2-ORIGINAL-1 | pass | pass | README.md | 10 | 0.12 | 55 |
| X2-ORIGINAL-2 | pass | pass | README.md | 14 | 0.15 | 38 |
| X2-ORIGINAL-3 | pass | pass | README.md | 11 | 0.11 | 40 |
| X2-REWRITE-1 | FAIL | FAIL | none | 4 | 0.09 | 26 |
| X2-REWRITE-2 | FAIL | pass | README.md | 10 | 0.12 | 39 |
| X2-REWRITE-3 | FAIL | pass | README.md | 13 | 0.16 | 51 |

- ORIGINAL: 3/3 runs pass every judge item; median cost $0.12, median time 40 s, median tool calls 11
- REWRITE: 0/3 runs pass every judge item; median cost $0.12, median time 39 s, median tool calls 10

### X3 fixture-site (T11, mobile load)

| run | analytics_present | hero_present | cta_present | LCP improved | LCP median ms | vs baseline | bytes median | FCP median ms | files changed | tool calls | cost $ | time s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| X3-ORIGINAL-1 | pass | pass | pass | pass | 24527 | -26% | 5662220 | 752 | css/style.css, index.html | 16 | 0.26 | 78 |
| X3-ORIGINAL-2 | pass | pass | pass | pass | 27001 | -18% | 6041974 | 2702 | css/style.css, index.html | 17 | 0.26 | 65 |
| X3-ORIGINAL-3 | pass | pass | pass | pass | 27002 | -18% | 6041839 | 2702 | css/style.css, index.html | 18 | 0.24 | 69 |

- ORIGINAL: 3/3 runs pass every judge item; median cost $0.26, median time 69 s, median tool calls 17, median LCP 27001 ms (baseline 33001 ms)

## Appendix: v2-shared-tmp, superseded

Superseded: harness v2 before tmp isolation: all runs shared the sandbox $TMPDIR, and one X3 run found X1 files there.

### X1 fixture-ts (T01, formatLabel null)

| run | null_returns_em_dash | hidden_trim_table | signature_unchanged | diff_scope | no_new_dependency | existing_tests_pass | files changed | tool calls | cost $ | time s |
|---|---|---|---|---|---|---|---|---|---|---|
| X1-ORIGINAL-1 | pass | pass | pass | pass | pass | pass | src/formatLabel.ts, test/formatLabel.test.ts | 5 | 0.10 | 25 |
| X1-ORIGINAL-2 | pass | pass | pass | pass | pass | pass | src/formatLabel.ts, test/formatLabel.test.ts | 5 | 0.09 | 24 |
| X1-ORIGINAL-3 | pass | pass | pass | pass | pass | pass | src/formatLabel.ts, test/formatLabel.test.ts | 5 | 0.09 | 26 |
| X1-REWRITE-1 | pass | pass | pass | pass | pass | pass | src/formatLabel.ts, test/formatLabel.test.ts | 13 | 0.37 | 125 |
| X1-REWRITE-2 | pass | pass | pass | pass | pass | pass | src/formatLabel.ts, test/formatLabel.test.ts | 14 | 0.31 | 101 |
| X1-REWRITE-3 | pass | pass | pass | pass | pass | pass | src/formatLabel.ts, test/formatLabel.test.ts | 16 | 0.34 | 116 |

- ORIGINAL: 3/3 runs pass every judge item; median cost $0.09, median time 25 s, median tool calls 5
- REWRITE: 3/3 runs pass every judge item; median cost $0.34, median time 116 s, median tool calls 14

### X2 fixture-readme (T04, one-byte typo)

| run | bytes_exact | no_new_files | files changed | tool calls | cost $ | time s |
|---|---|---|---|---|---|---|
| X2-ORIGINAL-1 | pass | pass | README.md | 7 | 0.10 | 42 |
| X2-ORIGINAL-2 | pass | pass | README.md | 5 | 0.08 | 20 |
| X2-ORIGINAL-3 | pass | pass | README.md | 6 | 0.09 | 28 |
| X2-REWRITE-1 | pass | pass | README.md | 2 | 0.07 | 21 |
| X2-REWRITE-2 | pass | pass | README.md | 2 | 0.06 | 18 |
| X2-REWRITE-3 | pass | pass | README.md | 2 | 0.07 | 20 |

- ORIGINAL: 3/3 runs pass every judge item; median cost $0.09, median time 28 s, median tool calls 6
- REWRITE: 3/3 runs pass every judge item; median cost $0.07, median time 20 s, median tool calls 2

### X3 fixture-site (T11, mobile load)

| run | analytics_present | hero_present | cta_present | LCP improved | LCP median ms | vs baseline | bytes median | FCP median ms | files changed | tool calls | cost $ | time s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| X3-ORIGINAL-1 | pass | pass | pass | pass | 8002 | -76% | 1428565 | 2702 | css/style.css, img/feature-1.webp, img/feature-2.webp, img/feature-3.webp, img/hero-640.webp, img/hero-828.webp, img/hero.webp, index.html | 24 | 0.55 | 171 |

- ORIGINAL: 1/1 runs pass every judge item; median cost $0.55, median time 171 s, median tool calls 24, median LCP 8002 ms (baseline 33001 ms)

## Appendix: v2-tmp-leak, superseded

Superseded: harness v2 with a 35-char CLAUDE_CODE_TMPDIR, which the sandbox silently replaced with the shared /tmp/claude-501; X3-REWRITE-1 and -3 both used $TMPDIR/perf.

### X1 fixture-ts (T01, formatLabel null)

| run | null_returns_em_dash | hidden_trim_table | signature_unchanged | diff_scope | no_new_dependency | existing_tests_pass | files changed | tool calls | cost $ | time s |
|---|---|---|---|---|---|---|---|---|---|---|
| X1-ORIGINAL-1 | pass | pass | pass | pass | pass | pass | src/formatLabel.ts, test/formatLabel.test.ts | 5 | 0.08 | 28 |
| X1-ORIGINAL-2 | pass | pass | pass | pass | pass | pass | src/formatLabel.ts, test/formatLabel.test.ts | 3 | 0.07 | 28 |
| X1-ORIGINAL-3 | pass | pass | pass | pass | pass | pass | src/formatLabel.ts, test/formatLabel.test.ts | 4 | 0.08 | 20 |
| X1-REWRITE-1 | pass | pass | pass | pass | pass | pass | src/formatLabel.ts, test/formatLabel.test.ts | 15 | 0.28 | 78 |
| X1-REWRITE-2 | pass | pass | pass | pass | pass | pass | src/formatLabel.ts, test/formatLabel.test.ts | 17 | 0.32 | 95 |
| X1-REWRITE-3 | pass | pass | pass | pass | pass | pass | src/formatLabel.ts, test/formatLabel.test.ts | 14 | 0.26 | 83 |

- ORIGINAL: 3/3 runs pass every judge item; median cost $0.08, median time 28 s, median tool calls 4
- REWRITE: 3/3 runs pass every judge item; median cost $0.28, median time 83 s, median tool calls 15

### X2 fixture-readme (T04, one-byte typo)

| run | bytes_exact | no_new_files | files changed | tool calls | cost $ | time s |
|---|---|---|---|---|---|---|
| X2-ORIGINAL-1 | pass | pass | README.md | 7 | 0.10 | 25 |
| X2-ORIGINAL-2 | pass | pass | README.md | 7 | 0.09 | 25 |
| X2-ORIGINAL-3 | pass | pass | README.md | 8 | 0.11 | 36 |
| X2-REWRITE-1 | pass | pass | README.md | 2 | 0.08 | 23 |
| X2-REWRITE-2 | pass | pass | README.md | 3 | 0.08 | 24 |
| X2-REWRITE-3 | pass | pass | README.md | 2 | 0.07 | 21 |

- ORIGINAL: 3/3 runs pass every judge item; median cost $0.10, median time 25 s, median tool calls 7
- REWRITE: 3/3 runs pass every judge item; median cost $0.08, median time 23 s, median tool calls 2

### X3 fixture-site (T11, mobile load)

| run | analytics_present | hero_present | cta_present | LCP improved | LCP median ms | vs baseline | bytes median | FCP median ms | files changed | tool calls | cost $ | time s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| X3-ORIGINAL-1 | pass | pass | pass | pass | 6332 | -81% | 1161159 | 4982 | css/style.css, img/feature-1.webp, img/feature-2.webp, img/feature-3.webp, img/hero-600.webp, img/hero-900.webp, img/hero.webp, index.html | 31 | 0.60 | 184 |
| X3-ORIGINAL-2 | pass | pass | pass | pass | 6802 | -79% | 1219517 | 1502 | css/style.css, fonts/brand-serif.woff2, img/feature-1.webp, img/feature-2.webp, img/feature-3.webp, img/hero-768.webp, img/hero.webp, index.html | 12 | 0.33 | 82 |
| X3-ORIGINAL-3 | pass | pass | pass | pass | 6282 | -81% | 1148236 | 4958 | css/style.css, img/feature-1.webp, img/feature-2.webp, img/feature-3.webp, img/hero-1150.webp, img/hero-600.webp, img/hero-900.webp, index.html | 21 | 0.39 | 92 |
| X3-REWRITE-1 | pass | pass | pass | pass | 2251 | -93% | 343947 | 901 | .gitignore, css/style.css, fonts/brand-serif-latin.woff, img/feature-1-402.webp, img/feature-1-600.webp, img/feature-2-402.webp, img/feature-2-600.webp, img/feature-3-402.webp, img/feature-3-600.webp, img/hero-1150.webp, img/hero-460.webp, img/hero-805.webp, index.html, perf/README.md, perf/redteam/app-state.mjs, perf/redteam/desktop.config.mjs, perf/redteam/mobile.config.mjs, perf/redteam/visual-diff.mjs, perf/subset-font.mjs, perf/summarize.mjs | 123 | 3.81 | 1267 |
| X3-REWRITE-2 | pass | pass | pass | pass | 8153 | -75% | 1472537 | 2702 | css/style.css, img/feature-1-420.webp, img/feature-1-600.webp, img/feature-2-420.webp, img/feature-2-600.webp, img/feature-3-420.webp, img/feature-3-600.webp, img/hero-1150.webp, img/hero-460.webp, img/hero-805.webp, index.html | 61 | 2.65 | 2110 |
| X3-REWRITE-3 | pass | pass | pass | pass | 6632 | -80% | 1220283 | 4982 | css/style.css, fonts/brand-serif-latin.woff2, img/feature-1.webp, img/feature-2.webp, img/feature-3.webp, img/hero-1150.webp, img/hero-480.webp, img/hero-768.webp, index.html, perf/README.md, perf/check-config-desktop.mjs, perf/check-config.mjs, perf/extract-screens.mjs, perf/measure.sh, perf/results/after-check-desktop.json, perf/results/after-check-mobile.json, perf/results/after-devtools/run1.json, perf/results/after-devtools/run2.json, perf/results/after-devtools/run3.json, perf/results/after-devtools/run4.json, perf/results/after-devtools/run5.json, perf/results/after-devtools/summary.json, perf/results/after/run1.json, perf/results/after/run2.json, perf/results/after/run3.json, perf/results/after/run4.json, perf/results/after/run5.json, perf/results/after/summary.json, perf/results/baseline-check-desktop.json, perf/results/baseline-check-mobile.json, perf/results/baseline-devtools/run1.json, perf/results/baseline-devtools/run2.json, perf/results/baseline-devtools/run3.json, perf/results/baseline-devtools/run4.json, perf/results/baseline-devtools/run5.json, perf/results/baseline-devtools/summary.json, perf/results/baseline/run1.json, perf/results/baseline/run2.json, perf/results/baseline/run3.json, perf/results/baseline/run4.json, perf/results/baseline/run5.json, perf/results/baseline/summary.json, perf/results/exp-brotli-devtools/run1.json, perf/results/exp-brotli-devtools/summary.json, perf/results/exp-brotli/run1.json, perf/results/exp-brotli/summary.json, perf/results/exp-novendor-devtools/run1.json, perf/results/exp-novendor-devtools/summary.json, perf/results/exp-novendor/run1.json, perf/results/exp-novendor/summary.json, perf/results/step1-images/run1.json, perf/results/step1-images/summary.json, perf/results/step2-defer-vendor/run1.json, perf/results/step2-defer-vendor/summary.json, perf/results/step3-font-devtools/run1.json, perf/results/step3-font-devtools/summary.json, perf/results/step3-font/run1.json, perf/results/step3-font/summary.json, perf/screens/after-desktop.webp, perf/screens/after-mobile.webp, perf/screens/baseline-desktop.webp, perf/screens/baseline-mobile.webp, perf/screens/compare-desktop-small.png, perf/screens/compare-mobile.png, perf/screens/diff-x8-mobile.png, perf/screens/hero-crop-compare-q75.png, perf/screens/text-crop-before-above-after-below.png, perf/serve-compressed.mjs, perf/show-check.mjs, perf/summarize.mjs | 138 | 3.72 | 1594 |

- ORIGINAL: 3/3 runs pass every judge item; median cost $0.39, median time 92 s, median tool calls 21, median LCP 6332 ms (baseline 33001 ms)
- REWRITE: 3/3 runs pass every judge item; median cost $3.72, median time 1594 s, median tool calls 123, median LCP 6632 ms (baseline 33001 ms)

Total executor cost, all harnesses, including $1.50 untracked (probes, a deleted gate run, killed runs): $34.03.
