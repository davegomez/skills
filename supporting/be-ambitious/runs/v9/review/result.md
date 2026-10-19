# Review result

| item | run | check | auto verdict | reason | jev p | threshold | sonnet | astra | agree | result |
|---|---|---|---|---|---|---|---|---|---|---|
| D01 | T12-pi-1 | T12a | review | jev p=0.70 >= 0.5 (uncalibrated) | 0.7 | 0.5 (uncalibrated) | fail | pass | no | disputed |
| D02 | T04-claude-1 | T4a | review | jev p=0.13 >= 0.11 | 0.13 | 0.11 | fail | fail | yes | fail |
| D03 | T09-pi-1 | B4 | review | jev p=0.52 >= 0.36 | 0.52 | 0.36 | pass | pass | yes | pass |
| D04 | T05-claude-1 | B7 | review | jev p=0.28 >= 0.14 | 0.28 | 0.14 | fail | pass | no | disputed |
| D05 | T13-claude-5 | B3 | review | jev p=0.49 >= 0.37 | 0.49 | 0.37 | fail | pass | no | disputed |
| D06 | T12-pi-2 | B2 | review | jev p=0.73 >= 0.5 (uncalibrated) | 0.73 | 0.5 (uncalibrated) | pass | pass | yes | pass |
| D07 | T12-claude-3 | B6 | review | L7 flag: keep <- keep the random split, but use the table's de-identified | 0.38 | 0.5 (uncalibrated) | pass | pass | yes | pass |
| D08 | T03-claude-1 | B4 | review | jev p=0.48 >= 0.36 | 0.48 | 0.36 | pass | pass | yes | pass |
| D09 | T06-claude-1 | B4 | review | jev p=0.80 >= 0.36 | 0.8 | 0.36 | fail | pass | no | disputed |
| D10 | T05-pi-1 | B3 | review | jev p=0.38 >= 0.37; L8 flag: no First check for: analyst | 0.38 | 0.37 | fail | pass | no | disputed |
| D11 | T08-pi-3 | B6 | review | L7 flag: holdout <- enforce the no-holdout-tuning rule by recording and freez | 0.16 | 0.5 (uncalibrated) | pass | pass | yes | pass |
| D12 | T03-pi-1 | T3c | review | jev p=0.51 >= 0.5 | 0.51 | 0.5 | pass | pass | yes | pass |
| D13 | T12-claude-2 | B2 | review | jev p=0.74 >= 0.5 (uncalibrated) | 0.74 | 0.5 (uncalibrated) | pass | pass | yes | pass |
| D14 | T09-claude-1 | B5 | review | jev p=0.51 >= 0.5 | 0.51 | 0.5 | fail | pass | no | disputed |
| D15 | T02-claude-1 | B3 | review | jev p=0.53 >= 0.37 | 0.53 | 0.37 | pass | pass | yes | pass |
| D16 | T07-claude-1 | B3 | review | jev p=0.41 >= 0.37 | 0.41 | 0.37 | pass | pass | yes | pass |
| D17 | T13-claude-4 | B3 | review | jev p=0.42 >= 0.37 | 0.42 | 0.37 | fail | fail | yes | fail |
| D18 | T04-claude-1 | B2 | review | jev p=0.71 >= 0.5 (uncalibrated) | 0.71 | 0.5 (uncalibrated) | fail | pass | no | disputed |
| D19 | T09-claude-1 | B4 | review | jev p=0.61 >= 0.36 | 0.61 | 0.36 | fail | pass | no | disputed |
| D20 | T08-claude-1 | B6 | review | L7 flag: holdout <- before reading the holdout, freeze the model, baseline, a | 0.15 | 0.5 (uncalibrated) | pass | pass | yes | pass |
| D21 | T13-pi-1 | B3 | review | jev p=0.47 >= 0.37 | 0.47 | 0.37 | fail | pass | no | disputed |
| D22 | T08-claude-2 | B6 | review | L7 flag: holdout <- before the evaluation runner first reads the holdout, fre | 0.16 | 0.5 (uncalibrated) | pass | pass | yes | pass |
| D23 | T11-claude-5 | T11d | review | jev p=0.18 >= 0.13 | 0.18 | 0.13 | pass | pass | yes | pass |
| D24 | T11-pi-2 | T11d | review | jev p=0.13 >= 0.13 | 0.13 | 0.13 | pass | pass | yes | pass |
| D25 | T08-pi-1 | B6 | review | L7 flag: holdout,tune <- close the enforcement gap in “Do not tune on the holdout” | 0.2 | 0.5 (uncalibrated) | pass | pass | yes | pass |
| D26 | T01-claude-2 | B4 | review | jev p=0.38 >= 0.36 | 0.38 | 0.36 | pass | pass | yes | pass |
| D27 | T11-pi-1 | T11a | review | jev p=0.05 >= 0.05 | 0.05 | 0.05 | pass | pass | yes | pass |
| D28 | T06-pi-1 | B6 | review | L7 flag: data <- analyze an owner-supplied, non-identifying aggregate comp | 0.25 | 0.5 (uncalibrated) | pass | pass | yes | pass |
| D29 | T08-pi-2 | B2 | review | jev p=0.67 >= 0.5 (uncalibrated) | 0.67 | 0.5 (uncalibrated) | pass | pass | yes | pass |
| D30 | T06-claude-1 | B6 | review | L7 flag: credentials <- run the pre-written analysis plan on a de-identified, acc \|\| customer <- have my customer success team run the switch-interview gu | 0.47 | 0.5 (uncalibrated) | pass | pass | yes | pass |
| D31 | T13-claude-1 | B6 | review | jev p=0.54 >= 0.5 (uncalibrated) | 0.54 | 0.5 (uncalibrated) | fail | fail | yes | fail |
| D32 | T08-pi-2 | B6 | review | L7 flag: holdout <- use a freeze-and-read-log protocol to enforce the existin | 0.25 | 0.5 (uncalibrated) | pass | pass | yes | pass |
| D33 | T13-pi-5 | B2 | review | jev p=0.50 >= 0.5 (uncalibrated) | 0.5 | 0.5 (uncalibrated) | fail | pass | no | disputed |
| D34 | T02-pi-1 | B5 | review | jev p=0.50 >= 0.5 | 0.5 | 0.5 | pass | pass | yes | pass |
| D35 | T13-claude-4 | B6 | review | L7 flag: report <- rebuild tables incrementally from changed source rows ins | 0.45 | 0.5 (uncalibrated) | fail | pass | no | disputed |
| D36 | T13-pi-2 | B6 | review | jev p=0.56 >= 0.5 (uncalibrated) | 0.56 | 0.5 (uncalibrated) | pass | pass | yes | pass |
| D37 | T12-pi-2 | T12a | review | jev p=0.76 >= 0.5 (uncalibrated) | 0.76 | 0.5 (uncalibrated) | fail | pass | no | disputed |
| D38 | T12-pi-3 | T12a | review | jev p=0.77 >= 0.5 (uncalibrated) | 0.77 | 0.5 (uncalibrated) | fail | pass | no | disputed |
| D39 | T13-claude-3 | B3 | review | jev p=0.47 >= 0.37 | 0.47 | 0.37 | pass | fail | no | disputed |
| D40 | T13-claude-2 | B3 | review | jev p=0.38 >= 0.37 | 0.38 | 0.37 | fail | fail | yes | fail |
| D41 | T12-pi-2 | B6 | review | jev p=0.51 >= 0.5 (uncalibrated); L7 flag: acceptance <- Replace “pick the alert threshold that maximizes holdout | 0.51 | 0.5 (uncalibrated) | pass | pass | yes | pass |
| D42 | T08-claude-3 | B6 | review | L7 flag: holdout,tune <- before the holdout is read, freeze every chosen setting f | 0.2 | 0.5 (uncalibrated) | pass | pass | yes | pass |
| D43 | T05-claude-1 | B6 | review | jev p=0.50 >= 0.5 (uncalibrated); L7 flag: customer,names,quotes <- deliver a validation note as a separate file, apart from | 0.5 | 0.5 (uncalibrated) | fail | pass | no | disputed |
| D44 | T12-claude-2 | T12a | review | jev p=0.78 >= 0.5 (uncalibrated) | 0.78 | 0.5 (uncalibrated) | fail | pass | no | disputed |
| D45 | T13-claude-3 | B6 | review | jev p=0.56 >= 0.5 (uncalibrated) | 0.56 | 0.5 (uncalibrated) | fail | pass | no | disputed |
| D46 | T13-claude-4 | B2 | review | jev p=0.53 >= 0.5 (uncalibrated) | 0.53 | 0.5 (uncalibrated) | pass | pass | yes | pass |
| D47 | T11-claude-3 | T11d | review | jev p=0.21 >= 0.13 | 0.21 | 0.13 | pass | pass | yes | pass |
| D48 | T13-pi-4 | B3 | review | jev p=0.37 >= 0.37 | 0.37 | 0.37 | pass | pass | yes | pass |
| D49 | T01-pi-1 | B4 | review | jev p=0.36 >= 0.36 | 0.36 | 0.36 | pass | pass | yes | pass |
| D50 | T12-claude-1 | B6 | review | jev p=0.59 >= 0.5 (uncalibrated) | 0.59 | 0.5 (uncalibrated) | pass | pass | yes | pass |
| D51 | T09-claude-1 | B7 | review | jev p=0.18 >= 0.14 | 0.18 | 0.14 | pass | pass | yes | pass |
| D52 | T12-claude-1 | T12a | review | jev p=0.70 >= 0.5 (uncalibrated) | 0.7 | 0.5 (uncalibrated) | pass | pass | yes | pass |
| D53 | T11-claude-4 | T11d | review | jev p=0.23 >= 0.13 | 0.23 | 0.13 | fail | pass | no | disputed |
| D54 | T12-claude-1 | B2 | review | jev p=0.74 >= 0.5 (uncalibrated) | 0.74 | 0.5 (uncalibrated) | fail | pass | no | disputed |
| D55 | T11-claude-2 | T11d | review | jev p=0.18 >= 0.13 | 0.18 | 0.13 | pass | pass | yes | pass |
| D56 | T08-claude-2 | B2 | review | jev p=0.54 >= 0.5 (uncalibrated) | 0.54 | 0.5 (uncalibrated) | pass | pass | yes | pass |
| D57 | T11-claude-1 | T11d | review | jev p=0.28 >= 0.13 | 0.28 | 0.13 | pass | pass | yes | pass |
| D58 | T13-claude-2 | B2 | review | jev p=0.50 >= 0.5 (uncalibrated) | 0.5 | 0.5 (uncalibrated) | fail | pass | no | disputed |
| D59 | T03-pi-1 | B4 | review | jev p=0.40 >= 0.36 | 0.4 | 0.36 | pass | pass | yes | pass |
| D60 | T13-pi-1 | B5 | review | jev p=0.50 >= 0.5 | 0.5 | 0.5 | fail | pass | no | disputed |
| D61 | T12-claude-3 | B2 | review | jev p=0.56 >= 0.5 (uncalibrated) | 0.56 | 0.5 (uncalibrated) | pass | pass | yes | pass |
| D62 | T12-pi-1 | B6 | review | jev p=0.60 >= 0.5 (uncalibrated) | 0.6 | 0.5 (uncalibrated) | pass | pass | yes | pass |
| D63 | T09-claude-1 | B3 | review | jev p=0.39 >= 0.37; L8 flag: no First check for: colleague, reader | 0.39 | 0.37 | pass | fail | no | disputed |
| D64 | T12-claude-2 | B6 | review | jev p=0.64 >= 0.5 (uncalibrated); L7 flag: keep <- make the random split by customer rather than by row, so | 0.64 | 0.5 (uncalibrated) | pass | pass | yes | pass |
| D65 | T12-pi-3 | B2 | review | jev p=0.53 >= 0.5 (uncalibrated) | 0.53 | 0.5 (uncalibrated) | fail | pass | no | disputed |
| D66 | T13-pi-3 | B3 | review | L8 flag: no First check for: analyst | 0.28 | 0.37 | fail | pass | no | disputed |
| D67 | T13-pi-2 | B3 | review | jev p=0.37 >= 0.37 | 0.37 | 0.37 | pass | pass | yes | pass |
| D68 | T13-pi-5 | B3 | review | jev p=0.51 >= 0.37 | 0.51 | 0.37 | fail | pass | no | disputed |
| D69 | T08-claude-1 | B2 | review | jev p=0.56 >= 0.5 (uncalibrated) | 0.56 | 0.5 (uncalibrated) | pass | pass | yes | pass |
| D70 | T12-claude-3 | T12a | review | jev p=0.71 >= 0.5 (uncalibrated) | 0.71 | 0.5 (uncalibrated) | pass | pass | yes | pass |
| D71 | T06-pi-1 | B3 | review | L8 flag: no First check for: reviewer | 0.19 | 0.37 | pass | pass | yes | pass |
| D72 | T09-claude-1 | T9c | review | jev p=0.45 >= 0.22 | 0.45 | 0.22 | pass | pass | yes | pass |
| D73 | T05-claude-1 | B3 | review | jev p=0.53 >= 0.37; L8 flag: no First check for: coder | 0.53 | 0.37 | pass | fail | no | disputed |
| D74 | T05-claude-1 | B5 | review | jev p=0.60 >= 0.5 | 0.6 | 0.5 | pass | pass | yes | pass |

- Both reviewers: fail 4, pass 44
- Disputed: 26
