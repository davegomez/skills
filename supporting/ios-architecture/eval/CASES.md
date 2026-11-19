# Case format

Each case is a folder `cases/I0N/`. The harness reads only these files. Nothing in a case folder may enter the builder's work tree except `fixture/`, `task.md`, and a review case's variant diff.

| Path | Contents |
| --- | --- |
| `case.json` | `id`, `title`, `priorities` (subset of security, reliability, accessibility, maintainability, performance), `references` (gold route rows: `required` and `optional` lists of reference names such as `navigation`), `pre_edit_files` (existing files a pre-edit route must receive), `traps` (seeded issues: `id`, `file`, `line`, `severity` critical/major/minor, `description`), `variants` (review case only, see below). Optional: `toolchain.simulator_device_type` (the simulator device type for grading; default in the harness config). Other keys are for the case's own grader; the harness ignores them. |
| `task.md` | The exact user prompt for the builder. The same text for every arm. No mention of the skill, the scripts, or Jev. |
| `fixture/` | The starting tree. The harness copies it to a fresh folder, runs `git init`, and makes 1 commit. A missing or empty `fixture/` (git keeps no empty folder) is a new project: the work folder starts empty, and the git repository is in its parent folder, so `scaffold` can run in the work folder. |
| `reference.patch` | A known-good solution, as a patch against the fixture commit (`git apply`, paths relative to the work folder). Not used by a review case. |
| `negative/*.patch` | Deficient solutions. Each must fail at least 1 hidden check; the file name (without `.patch`) is the id of the check it must fail. Not used by a review case. |
| `hidden/grade.sh <work-dir> <out.json>` | The hidden grader. Runs outside the builder's tree, on a copy of the result, from a folder that is not the case folder. Builds with `CODE_SIGNING_ALLOWED=NO`, runs hidden tests on the simulator `$EVAL_SIM` (a UDID), and writes the result. Exit 0 when it wrote a result, also when checks fail; non-zero only for an infrastructure failure. |
| `hidden/` (other files) | Hidden tests and assets that `grade.sh` copies into the copy of the result. |
| `rubric.md` | Check ids for the blind reviewer, each with a priority, a severity, and a pass condition. Only checks that an executable test cannot settle. |

Check ids in the grader result and in `rubric.md` start with the case id and a hyphen, for example `I03-link-needs-confirmation`.

## Grader environment

| Variable | Value |
| --- | --- |
| `EVAL_SIM` | UDID of a simulator created for this 1 grading run and deleted after it. The harness runs 1 grading at a time on the machine, so a grader may boot, install on, and test on it freely. |
| `EVAL_FINAL_TEXT` | Path of a file with the builder's final message (empty in preflight unless the delivery is a `.md` file). |
| `EVAL_VARIANT` | Review case only: `seeded` or `clean`. |

## Review case

A review case has `variants` with exactly `seeded` and `clean`. Each is an object:

| Key | Contents |
| --- | --- |
| `diff` | Path of the diff under review, relative to the case folder. The harness applies it to the fixture commit as uncommitted changes. |
| `reference` | Path of the variant's known-good delivery. |
| `negatives` | Paths of the variant's deficient deliveries; each file name (without its extension) is the id of the check it must fail. |
| other keys | For the case's own grader (for example `traps` and `lookalikes`); the harness ignores them. |

A reference or negative ending in `.patch` is applied on top of the variant diff (a review written to a file, such as `REVIEW.md`). One ending in `.md` is the builder's final message, given as `EVAL_FINAL_TEXT`. The grader decides whether the builder left the tree as the task allows: it must fail a critical check when the builder changed anything other than its delivery.

Result JSON of `grade.sh`:

```json
{
  "case": "I03",
  "checks": [
    {"id": "I03-link-needs-confirmation", "priority": "security", "critical": true, "result": "pass", "evidence": "XCUITest testLinkAloneDoesNotArchive passed"}
  ]
}
```

`result` is `pass`, `fail`, or `na`. A build failure makes every check that needs the build `fail`, not `na`. Other top-level keys (for example `metrics`) are allowed.

## Preflight (required before a case is frozen)

`python3 -I preflight.py cases/<id>` runs these steps through the harness. A review case runs each step on each variant, with that variant's reference and negatives.

1. The fixture alone fails at least 1 critical check (the task is not already done).
2. The fixture plus the reference passes every check (`na` allowed).
3. Each negative fails the check its file name names.
4. Grading the reference 2 times in a row gives the same results (no flaky check).
