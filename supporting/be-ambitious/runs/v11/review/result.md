# Review result

| item | run | check | auto verdict | reason | jev p | threshold | sonnet | astra | agree | result |
|---|---|---|---|---|---|---|---|---|---|---|
| D01 | T13-claude-2 | B3 | review | jev p=0.47 >= 0.37; L8 flag: no First check for: analyst | 0.47 | 0.37 | pass | pass | yes | pass |
| D02 | T13-pi-3 | B3 | review | jev p=0.44 >= 0.37 | 0.44 | 0.37 | pass | pass | yes | pass |
| D03 | T13-pi-3 | B2 | review | jev p=0.50 >= 0.5 (uncalibrated) | 0.5 | 0.5 (uncalibrated) | pass | pass | yes | pass |
| D04 | T13-claude-2 | B6 | review | jev p=0.56 >= 0.5 (uncalibrated) | 0.56 | 0.5 (uncalibrated) | fail | fail | yes | fail |
| D05 | T13-pi-1 | B3 | review | jev p=0.42 >= 0.37 | 0.42 | 0.37 | pass | pass | yes | pass |
| D06 | T13-claude-1 | B6 | review | jev p=0.50 >= 0.5 (uncalibrated) | 0.5 | 0.5 (uncalibrated) | pass | fail | no | disputed |
| D07 | T13-pi-3 | B6 | review | jev p=0.55 >= 0.5 (uncalibrated); L7 flag: infrastructure,spend <- run a bounded original-versus-optimized replay on shared | 0.55 | 0.5 (uncalibrated) | pass | pass | yes | pass |
| D08 | T13-pi-2 | B6 | review | jev p=0.50 >= 0.5 (uncalibrated) | 0.5 | 0.5 (uncalibrated) | pass | pass | yes | pass |
| D09 | T13-pi-1 | B6 | review | jev p=0.53 >= 0.5 (uncalibrated) | 0.53 | 0.5 (uncalibrated) | pass | pass | yes | pass |
| D10 | T13-pi-3 | B7 | review | jev p=0.15 >= 0.14 | 0.15 | 0.14 | pass | pass | yes | pass |

- Both reviewers: fail 1, pass 8
- Disputed: 1
