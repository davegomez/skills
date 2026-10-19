# Engineering skills

Agent skills for Claude Code, Codex, Cursor, and other agents that the [`skills`](https://github.com/vercel-labs/skills) CLI supports.

## Skills

| Skill | What it does |
|---|---|
| [`be-ambitious`](skills/be-ambitious/SKILL.md) | Rewrites a task or prompt to aim higher in altitude, depth, and range, with an outside judge that checks the result. |

## Install

```sh
npx skills add davegomez/skills --skill be-ambitious
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

## Development

`supporting/` holds the test cases, the eval harness, and the history of each skill. An install does not copy it. [`supporting/be-ambitious/README.md`](supporting/be-ambitious/README.md) tells how to change and check `be-ambitious`.

## License

[GNU Affero General Public License v3.0](LICENSE).
