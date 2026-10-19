# Be-ambitious development archive

This directory holds what continued development of the `be-ambitious` skill needs: the test cases, the rubric, the harness, the lint, the last 3 batches, and the retired grading tools. [HISTORY.md](HISTORY.md) summarizes how candidates v1 to v11 were built and tested.

Release 1 is the runtime, [`skills/be-ambitious/SKILL.md`](../../skills/be-ambitious/SKILL.md): the first stable version of the skill, a byte-identical copy of candidate v11 (sha256 f773074d…, frozen in [`runs/v11/frozen/SKILL.md`](runs/v11/frozen/SKILL.md)). The owner chose it on 2026-10-19 (Q13), before any use or shipping. Nothing is committed or linked into an agent folder. Supporting material may depend on the runtime; the runtime never depends on supporting material.

## Layout

- [`cases/`](cases/) T01 to T13, [`rubric.md`](rubric.md) (checks B1 to B10 and the case checks), [`review2/INTERPRETATIONS.md`](review2/INTERPRETATIONS.md) (accepted rules and owner decisions).
- [`run.sh`](run.sh) generates a batch into `runs/<version>/` and freezes its inputs in `runs/<version>/frozen/`. [`validate_grade.py`](validate_grade.py) is the grade JSON contract; `eval/jev_grade.py` imports it.
- [`eval/`](eval/) lint, Jev grading, labels, and calibration, documented in [`eval/README.md`](eval/README.md). `eval/cache/` holds paid Jev answers; keep it. `eval/calibration-runs/v2` to `v7` hold the 396 cross-graded runs that the labels and the calibration use.
- [`review2/`](review2/) builds a blind review pack (`build.py`), runs the Sonnet reviewer (`run_review_sonnet.sh`), and scores 2 reviewers (`score.py`).
- [`runs/v9/`](runs/v9/), [`runs/v10/`](runs/v10/), [`runs/v11/`](runs/v11/) the last full development batch and the 2 fix checks, each with `RESULT.md`, `grades-auto.json`, `review-queue.json`, `jev/`, `review/`, and `final-status.json`.
- [`exec/`](exec/) the executor test, ORIGINAL vs REWRITE prompt on fixtures, documented in [`exec/README.md`](exec/README.md), with results in [`exec/results.md`](exec/results.md).

## Setup

`.venv/`, `exec/tools/node_modules/`, and `exec/fixtures/` are not tracked. From the repository root:

```sh
python3.15 -m venv supporting/be-ambitious/.venv
supporting/be-ambitious/.venv/bin/python -m pip install typesafe-sdk==0.7.5
(cd supporting/be-ambitious/exec/tools && npm install)
python3 -I supporting/be-ambitious/exec/build_fixtures.py
mkdir -p /tmp/ambition-runner/.claude/skills/be-ambitious /tmp/ambition-skill/be-ambitious /tmp/pi-clean-agent /tmp/ambition-review
```

`build_fixtures.py` takes no arguments and rebuilds `exec/fixtures/fixture-ts`, `fixture-readme`, and `fixture-site`, each a git repository with one commit. The files are deterministic; the commit hashes are not. `/tmp/pi-clean-agent` needs `auth.json` (a link to `~/.pi/agent/auth.json`) and a `settings.json` with the default model; it keeps `~/.pi/agent/APPEND_SYSTEM.md` out of Pi runs.

## Maintain the skill

Owner decision Q19 to Q21 (2026-10-19): release 1 is the defined version. A later change gets a small check with a hard cap of $1.00 of recorded Claude cost, not a full batch. Nothing runs without the owner's approval of the change.

1. Reason. Each change fixes 1 problem, preferably a real rewrite that went wrong in use. Save that task text as the next case file, for example `cases/T14.txt`; `eval/lint.py` accepts any case from T1 to T99.
2. Edit. One model (Claude or Pi) writes the smallest edit to a copy of the runtime, `SKILL.<version>.md` in this directory. Name versions after the release: `r1.1`, `r1.2`, and so on; v1 to v11 are taken. The other model reviews the edit once, with no co-writing rounds and no brief. Both load `writing-for-agents`.
3. Generate. Run the cases the change affects plus 2 fixed smoke cases, T01 (must return unchanged) and T13 (the hardest), 1 run per model each: `CAP_USD=1.00 RESERVE_USD=0.25 ./run.sh r1.1 T01:1 T13:1 T14:1 < /dev/null`. Pi runs on the subscription; at the v9 rate a Claude run costs about $0.12. When the cap skips a run, report it as skipped; do not raise the cap.
4. Lint, free and offline: `for f in runs/r1.1/T*.md; do c=${f:t}; .venv/bin/python -I eval/lint.py ${c%%-*} $f; done`. A lint fail is a fail.
5. Review, 1 blind reviewer on the subscription. Copy each output under a neutral name (`T13-a.md`, `T13-b.md`, model order random) into `/tmp/ambition-review/r1.1/`, and keep the name-to-run key outside that folder. Then, from `/tmp/ambition-review`, with absolute paths: `PI_CODING_AGENT_DIR=/tmp/pi-clean-agent pi -p --no-session -ne -nc -ns -np --no-tools --model openai/gpt-6-astra --thinking xhigh @<abs>/rubric.md @<abs>/review2/INTERPRETATIONS.md @<abs>/cases/T13.txt @<abs>/T13-a.md ... "Each T<NN>-<x>.md file is one output of the be-ambitious skill for the task in cases/T<NN>.txt. Grade every output against rubric.md and INTERPRETATIONS.md. Report only critical failures: B1, B2, B3, B4, B6, B7, or a case check. Return one line per output: '<file> PASS' or '<file> FAIL <check> <one sentence that quotes the output>'." < /dev/null > runs/r1.1/review.txt`.
6. Decide. The change ships when every output passes lint and the reviewer reports no critical failure. Otherwise drop the change, or make 1 more edit and repeat steps 3 to 5 inside the same $1.00 cap. With the owner's approval, copy `SKILL.<version>.md` byte-identical to `../../skills/be-ambitious/SKILL.md`. Delete the candidate file after the copy, and record the change in 1 line under "Changes after release 1" in [HISTORY.md](HISTORY.md): the version, the reason, the cost, and the result.

A full sweep (all cases, 1 run per model, cap about $3.00, the same lint and review) runs only when the owner asks for a new release after many changes.

Retired by Q19: the 66-run gate, the Jev grader (`eval/grade_run.py`, `jev_grade.py`, `calibrate.py`), the Sonnet second reviewer (`review2/run_review_sonnet.sh`, `build.py`, `score.py`), and the executor test (`exec/`). Their code and data stay here as a record; do not use them by default. The gate they enforced is in [HISTORY.md](HISTORY.md).

## Standing rules

- The owner does not grade. A model judges, blind: Astra on the Pi subscription, which never sees which model wrote an output.
- The Jev grader is retired. If it is ever used again: read the TypeSafe key only at run time with `TYPESAFE_API_KEY="$(security find-generic-password -s typesafe-api-key -a dave -w)"`, never print, log, or write it, send Jev only test tasks and skill outputs, and note that about 0.3M of its 5M input-token guard is left.
- Ask the owner before a commit, an install, a link into an agent folder, or any spend.
- Give `pi -p` and `run.sh` `< /dev/null` when started from the Bash tool; otherwise Pi hangs on the open stdin.
- Start Pi with `PI_CODING_AGENT_DIR=/tmp/pi-clean-agent`, because Pi loads `~/.pi/agent/APPEND_SYSTEM.md` despite `-nc`.

## Known gaps

- No full batch has run since candidate v9. Candidates v10 and v11 were checked only on T04 and T13.
- Claude on T13 still proposes some actions on a shared live database without an approval line ([`runs/v11/RESULT.md`](runs/v11/RESULT.md)).
- With 2 reviewers, they often failed a run for different reasons. The single reviewer of the maintenance process is less strict than the retired 2-reviewer rule.

## Validate

From the repository root. Each of these commands runs offline:

```sh
cd supporting/be-ambitious
for m in lint jev_grade labels calibrate grade_run; do .venv/bin/python -I eval/$m.py --selftest; done
.venv/bin/python -I eval/lint.py T11 eval/calibration-runs/v7/T11-claude-1.md
.venv/bin/python -I eval/calibrate.py --report-only
.venv/bin/python -I eval/grade_run.py v11 --dry-run
python3 -I review2/build.py --selftest
REVIEWERS=sonnet,astra python3 -I review2/score.py --selftest
python3 -I exec/execute.py selftest
for f in run.sh review2/run_review_sonnet.sh; do zsh -n $f; done
```

`--report-only` rebuilds `eval/calibration-report.md` and `eval/disagreements.json` from the cache. `grade_run.py --dry-run` sends nothing and needs no key. Calibration that asks Jev, `run.sh`, `run_review_sonnet.sh`, Astra, and `exec/execute.py run|batch` call paid models.
