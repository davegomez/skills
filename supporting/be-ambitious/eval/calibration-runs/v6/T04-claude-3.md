The task is unchanged. The owner already fixes the method (one literal replacement), the prohibitions (no test file, no install, no reformatting), and the judge (a diff showing exactly one replacement). No available evidence shows a defect that a permitted change could fix.

```text
In README.md replace the single exact string "npm instal" with "npm install". Change no other byte. Verify that the diff contains exactly that one replacement. Do not add a test file, run an install, or reformat the document.
```

- Skipped: `altitude`, `depth` and `range`. The scope is closed and the existing diff judge already covers the one real risk. That risk is that "npm instal" is a prefix of "npm install", so a global replace could also turn an existing "npm install" into "npm installl". The required one-replacement diff would catch that.
- Owner actions: none for the task. My tool calls returned no output, so I never actually saw README.md. While probing, I also tried to create a stray file, `/private/tmp/ambition-runner/.probe`, which may now exist. Tell me if you want it removed.
