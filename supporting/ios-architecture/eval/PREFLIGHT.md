# Preflight results

Xcode 27.3 (27C5020n), iOS 27.3 simulator runtime. Each grade ran alone, on its own new simulator, deleted afterwards (I01 and I02: iPhone 15 Pro; I03, I04, and I06: iPhone 17 Pro; I05 builds nothing).

## Case preflight

Command, from `supporting/ios-architecture/eval/`: `python3 -I preflight.py cases/I01 cases/I02 cases/I03 cases/I04 cases/I05 cases/I06` (exit 0). Per-step details are in `runs/preflight/<case>.json`.

| Case | 1 fixture fails a critical check | 2 reference passes every check | 3 each negative fails its check | 4 reference graded twice, same results | Grade time, s |
| --- | --- | --- | --- | --- | --- |
| I01 | pass: 6 critical checks fail | pass: 0 fail, 0 na | pass: 5 of 5 | pass: same | 15 to 145 |
| I02 | pass: 5 critical checks fail | pass: 0 fail, 0 na | pass: 5 of 5 | pass: same | 85 to 168 |
| I03 | pass: 6 critical checks fail | pass: 0 fail, 0 na | pass: 3 of 3 | pass: same | 74 to 205 |
| I04 | pass: 2 critical checks fail | pass: 0 fail, 0 na | pass: 5 of 5 | pass: same | 178 to 205 |
| I05 seeded | pass: 4 critical checks fail | pass: 0 fail; na: `I05-clean-no-unsupported-material` | pass: 2 of 2 | pass: same | under 1 |
| I05 clean | pass: 1 critical check fails (`I05-review-written`) | pass: 0 fail; na: the 3 trap checks | pass: 1 of 1 | pass: same | under 1 |
| I06 | pass: 11 critical checks fail | pass: 0 fail, 0 na | pass: 6 of 6 | pass: same | 188 to 290 |

## Route gate

Command, from `supporting/ios-architecture/eval/`: `gates/route` (exit 1), with the committed `skills/ios-architecture/scripts/route` and Jev blocked. Required rows are the `references.required` lists in each `case.json`. Exit 3 is a pending decision that Jev would answer (`no_api_key` or `code_may_not_leave_machine`). Details are in `runs/gates/route.json`.

| Case | Pre-edit: required rows missed | Post-edit: required rows missed | Post-edit exit | Post-edit pending lines |
| --- | --- | --- | --- | --- |
| I01 | no pre-edit files | none | 3 | 2 |
| I02 | `accessibility`, `localization` | none | 3 | 1 |
| I03 | none | none | 3 | 1 |
| I04 | `architecture` | none | 3 | 1 |
| I05 | none | none | 0 | 0 |
| I06 | `persistence` | `persistence` | 0 | 0 |
