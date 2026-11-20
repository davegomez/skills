# Engineering skills

Agent skills for Claude Code, Codex, Cursor, and other agents that the [`skills`](https://github.com/vercel-labs/skills) CLI supports.

## Skills

| Skill | What it does |
|---|---|
| [`be-ambitious`](skills/be-ambitious/SKILL.md) | Rewrites a task or prompt to aim higher in altitude, depth, and range, with an outside judge that checks the result. |
| [`memory-triage`](skills/memory-triage/SKILL.md) | Sorts the notes of a Claude Code auto memory store with a script, so that Claude examines only the doubtful notes and you approve each change from 1 table. |
| [`react-testing-library`](skills/react-testing-library/SKILL.md) | Writes and reviews React and React Native component tests with Testing Library, with every rule tied to a source. |

## Install

```sh
npx skills add davegomez/skills --skill be-ambitious
npx skills add davegomez/skills --skill memory-triage
npx skills add davegomez/skills --skill react-testing-library
```

## Use `be-ambitious`

In Claude Code, the skill runs only when you invoke it. Give it the task to rewrite:

```text
/be-ambitious fix the crash in the login screen
```

The reply has 2 parts:

- A rewritten prompt in 1 fenced block. Its last line starts with `Judge:` and names the evidence that shows the work is done.
- A ledger with 1 line for each change, and the actions that you must do.

The skill does not do the task. You read the prompt and decide what to run. Each addition outside the original scope is on a line that starts with `With my approval only:`. Each unconfirmed dependency is on a line that starts with `First check:`.

The method comes from Felix Rieseberg, [How to be more ambitious](https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/).

## Use `memory-triage`

In Claude Code, the skill runs only when you invoke it. Invoke it in the repository whose auto memory you want to review:

```text
/memory-triage
```

A script sorts each note of the memory store into 1 class. It needs Python 3.9 or later and no other package. Claude examines only the notes that the script marks as doubtful, then shows 1 table with a proposed action for each note. Nothing changes until you answer `apply`.

The skill keeps no backup. A dropped note is deleted for good.

## Development

`supporting/` holds the test cases, the eval harness, and the history of each skill. An install does not copy it. [`supporting/be-ambitious/README.md`](supporting/be-ambitious/README.md) tells how to change and check `be-ambitious`.

## License

[GNU Affero General Public License v3.0](LICENSE).
