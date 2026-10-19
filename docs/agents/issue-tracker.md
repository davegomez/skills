# Issue tracker: GitHub

Issues and specs live in GitHub Issues for `davegomez/skills`.
Use the `gh` CLI. Pass `--repo davegomez/skills` on every issue or PR command.

## Operations

Commands below require the repository flag above.

- Create: `gh issue create --title "..." --body-file -`.
  Supply multiline bodies through a quoted heredoc.
- Read: `gh issue view <number> --json number,title,body,labels,comments`.
- List: `gh issue list --state open --json number,title,body,labels,comments`.
  Add label and state filters as needed.
- Comment: `gh issue comment <number> --body-file -`.
- Apply labels: `gh issue edit <number> --add-label "..."`.
- Remove labels: `gh issue edit <number> --remove-label "..."`.
- Close: `gh issue close <number> --comment "..."`.

“Publish to the issue tracker” means create a GitHub issue.
“Fetch the relevant ticket” means read the issue, including labels and comments.

## Pull requests as a triage surface

PRs as a request surface: no.

GitHub shares issue and PR numbers. For an ambiguous reference,
resolve whether it is an issue or PR before acting.
