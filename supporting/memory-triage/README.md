# memory-triage development

`skills/memory-triage` is the skill. This folder holds its tests; an install does not copy it.

## Tests

`tests/test_triage.py` tests `scripts/triage.py` with the standard library `unittest`. It builds a synthetic store in a temporary folder: 1 note for each class rule, a symlink out of the folder, a folder and a binary file named `.md`, an index with a dead pointer and a long line, and 3 transcripts with blob lines, bad JSON, and bad UTF-8. The planted credentials are built at run time. The tests check:

- the class of each planted note, the flags and fields of each row, and the summary counts;
- each detector on its own: frontmatter, file names, relative dates, dead paths, credentials, duplicates, the index;
- the use count and the bounded `--origin` extract;
- the exit codes and the error messages;
- that no planted credential reaches the output of either mode, and that a run leaves the fixture byte-identical.

Run them from the repository root, with no install, on the current and on the macOS system Python:

```sh
python3 -m unittest discover -s supporting/memory-triage/tests
/usr/bin/python3 -m unittest discover -s supporting/memory-triage/tests
```

Measure line coverage with a tool that stays out of the repository:

```sh
uvx coverage run --data-file=/tmp/memory-triage.coverage -m unittest discover -s supporting/memory-triage/tests
uvx coverage report --data-file=/tmp/memory-triage.coverage -m --include='*/memory-triage/scripts/triage.py'
```

Validate the skill against the Agent Skills specification. The PyPI package `skills-ref` names its command `agentskills`:

```sh
uvx --from skills-ref agentskills validate skills/memory-triage
```

It reports 1 error, `Unexpected fields in frontmatter: disable-model-invocation`: the specification does not know this Claude Code field, which keeps the skill user-invoked. `skills/be-ambitious` fails the same way.
