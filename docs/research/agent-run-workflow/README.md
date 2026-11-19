# Agent run workflow: the measurements

The data behind the effort to turn a way of running large coding tasks with agents into a framework for any project, model, and harness. The issue of that effort has the workflow, the open questions, and the draft of the framework.

The runs were made in a private project repository (a Rust core and server with native apps), with Claude Code as the harness. The numbers are from the session logs of 1 machine.

| File | What it has |
| --- | --- |
| [`report.md`](report.md) | The first audit, 2026-11-16: where the tokens of 7 days went, 11 findings, 11 proposed changes, the targets, and the tracking method. |
| [`a13-addendum.md`](a13-addendum.md) | The verdict on run A13, which applied most of the changes: what worked, what did not, and what to change next. |
| [`a13-addendum-data.md`](a13-addendum-data.md) | Each number of the addendum with its method, for the runs A10 to A13. |
| [`runs.csv`](runs.csv) | 1 row for each run. |
| `scan.py`, `report.py`, `report2.py` | Read the Claude Code session logs of the last N days and print the tables of the audit. |
| `a13_addendum.py` | Made the data file. It has paths of the machine and of the project that it ran on. |

To run the scripts: `python3 -I scan.py <days>`, then `python3 -I report.py` and `python3 -I report2.py`, then remove `data.pkl`. The file `data.pkl` holds counts and descriptions from the logs: do not commit it.

A weighted unit is the cost measure of these files: 1 input token = 1, a cache read = 0.1, a cache write = 1.25 or 2, 1 output token = 5. It is not money.
