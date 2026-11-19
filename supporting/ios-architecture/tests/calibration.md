# Decision calibration

The labeled fixtures are in [`fixtures/calibration/`](fixtures/calibration/), with the labels in `labels.tsv`. [`calibrate.sh`](calibrate.sh) runs them with real Jev calls. The model ID `jev-1.14.0` answered every request through the `jev-latest` alias. Thresholds apply to that model. When the alias moves to a new model, run `calibrate.sh` again and compare.

`p` is the Noul probability of yes, or the Choice probability of the selected option.

## Threshold rules

| Answer | Rule | Decisions |
| --- | --- | --- |
| Add work: a route row or a check flag | Noul `p >= 0.3` | `route`, every `check-*` |
| Clear the log check | Noul `p <= 0.25`. Between 0.25 and 0.3, escalate to the orchestrator. | `check-personal-data-in-log` |
| Clear the trust-boundary check | Noul `p <= 0.05`. Between 0.05 and 0.3, escalate to the orchestrator. | `check-trust-boundary-input` |
| Clear another check, or skip a route row | Noul `p < 0.3`. No band. | `route`, `check-business-rules-in-view`, `check-swallowed-error`, `check-control-accessibility` |
| Select a layer | Choice `p >= 0.7` | `migration-layer` |
| Select a route row, or confirm out of bounds | Noul `row_applies` `p <= 0.4`: `none`. Noul `p >= 0.7` and Choice `p >= 0.6`: that row. Otherwise, escalate to the orchestrator. | `out-of-bounds` |

## Results with the chosen thresholds

### check-personal-data-in-log

Jev gets only the os.Logger and os_log lines. The rule `print-log` covers print, NSLog, and debugPrint without Jev. Code enforces the Logger redaction rule, so Jev answers only about values marked `.public` and numbers with no privacy argument.

| Fixture | Label | `public_value_sensitive` | `number_sensitive` | Outcome |
| --- | --- | --- | --- | --- |
| `log/email-public.swift` | public value | 0.97 | 0.02 | violation |
| `log/body-public.swift` | public value | 0.96 | 0.01 | violation |
| `log/age-number.swift` | number | 0.09 | 0.99 | violation |
| `log/redacted.swift` | none | 0.09 | 0.24 | clear |
| `log/safe-public.swift` | none | 0.11 | 0.04 | clear |
| `log/token-print.swift` | none | script | script | no Jev call |

All 3 violations are flagged. 2 of 2 clean files clear: they score 0.04 to 0.24, at or below the 0.25 clear threshold. No file goes to the orchestrator. At a 0.05 clear threshold, 0 of 2 clean files clear.

### check-trust-boundary-input

| Fixture | Label | `unvalidated_input` | `link_side_effect` | Outcome |
| --- | --- | --- | --- | --- |
| `trust/raw-deeplink.swift` | unvalidated | 0.96 | 0.05 | violation |
| `trust/pasteboard-raw.swift` | unvalidated | 0.96 | 0.40 | violation; false `link_side_effect` flag |
| `trust/delete-link.swift` | side effect | 0.08 | 0.98 | violation; `unvalidated_input` to the orchestrator |
| `trust/parsed-deeplink.swift` | none | 0.07 | 0.05 | orchestrator |
| `trust/confirm-link.swift` | none | 0.10 | 0.02 | orchestrator |

All 3 violations are flagged. 1 false flag at 0.40. Clean files score 0.07 to 0.10 and go to the orchestrator.

### check-business-rules-in-view, check-swallowed-error, check-control-accessibility

| Fixture | Label | `p` | Outcome |
| --- | --- | --- | --- |
| `rules/view-discount.swift` | rule | 0.99 | violation |
| `rules/model-eligibility.swift` | rule | 0.98 | violation |
| `rules/view-validation.swift` | rule | 0.98 | violation |
| `rules/view-display.swift` | none | 0.03 | clear |
| `rules/model-forward.swift` | none | 0.11 | clear |
| `errors/decode.swift` | discarded | 0.96 | violation |
| `errors/file-force.swift` | discarded | 0.98 | violation |
| `errors/sleep.swift` | none | 0.02 | clear |
| `errors/constant.swift` | none | 0.11 | clear |
| `a11y/tap-image.swift` | missing | 0.96 | violation |
| `a11y/canvas-chart.swift` | missing | 0.98 | violation |
| `a11y/tap-labeled.swift` | none | 0.12 | clear |
| `a11y/drag-adjustable.swift` | none | 0.20 | clear |

13 of 13 are correct. Violations score 0.96 or more. Clean files score 0.20 or less.

### route

5 files, 18 Nouls each.

| Measure | Result |
| --- | --- |
| Labeled rows at `p >= 0.3` | 16 of 18. The 2 misses: `ui-framework` for a widget timeline provider with no view (0.14), `architecture` for a legacy view model (0.15). |
| Unlabeled rows at `p >= 0.3` (extra reads) | 7 of 72: `concurrency` 0.91, `security-privacy` 0.83, `migration` 0.62, `localization` 0.56, `security-privacy` 0.44, `localization` 0.41, `security-privacy` 0.32. |
| Labeled rows, lowest `p` | 0.84 |

### migration-layer

| Fixture | Label | Answer | `p` |
| --- | --- | --- | --- |
| `layer/Money.swift` | domain | domain | 1.00 |
| `layer/OrdersViewController.swift` | feature | feature | 1.00 |
| `layer/APIClient.swift` | service | service | 1.00 |
| `layer/AppDelegate.swift` | shell | shell | 0.99 |
| `layer/CartTotalsTests.swift` | test | test | 1.00 |
| `layer/Colors.generated.swift` | none | none | 0.97 |
| `layer/CheckoutViewController.swift` | feature | feature | 0.98 |

7 of 7 are correct and decided.

### out-of-bounds

The Choice `row` and the Noul `row_applies` go to Jev in 1 request. The Choice has no `none` option.

| Concern | Label | `row_applies` | Choice | Choice `p` | Outcome |
| --- | --- | --- | --- | --- | --- |
| Send a reminder at 9 in the morning every day | lifecycle-extensions | 0.81 | lifecycle-extensions | 1.00 | lifecycle-extensions |
| Show prices in the currency of the user | localization | 0.95 | localization | 1.00 | localization |
| Make button text readable for people who use large text sizes | accessibility | 0.91 | accessibility | 0.97 | accessibility |
| Let the user export all of their data as 1 file | security-privacy | 0.64 | security-privacy | 0.57 | orchestrator |
| Show the step count from the Health app on the dashboard | security-privacy | 0.76 | lifecycle-extensions | 0.54 | orchestrator |
| Connect to a heart-rate strap over Bluetooth | none | 0.29 | architecture | 0.55 | none |
| Print a receipt with AirPrint | none | 0.32 | ui-framework | 0.36 | none |
| Cast a product video to an Apple TV with AirPlay | none | 0.28 | networking | 0.33 | none |
| Read NFC tags on product packaging | none | 0.31 | architecture | 0.68 | none |
| Play music with spatial audio on AirPods | none | 0.31 | architecture | 0.71 | none |
| Add an Apple Wallet pass for each event ticket | none | 0.57 | lifecycle-extensions | 0.52 | orchestrator |
| Support a game controller in the mini game | none | 0.59 | ui-framework | 0.64 | orchestrator |
| Add haptic feedback when the user completes an order | none | 0.64 | ui-framework | 0.57 | orchestrator |

8 of 13 are decided, all correct: 3 rows and 5 `none`. 5 go to the orchestrator: 2 with a row label and 3 with no row. `row_applies` is 0.64 to 0.95 for concerns with a row, and 0.28 to 0.64 for concerns with no row. Without `row_applies`, the Choice selects `architecture` at 0.68 and 0.71 for 2 concerns with no row.
