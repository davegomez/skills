```text
In README.md replace the single exact string "npm instal" with "npm install". Change no other byte.
Assumption: the target is the misspelled occurrence. Every correct "npm install" also contains "npm instal", so the target is the occurrence of "npm instal" not immediately followed by "l". Leave every existing "npm install" untouched; a plain replace-all would turn those into "npm installl".
Before editing, save the original bytes to a temporary location outside the project, so the result can be checked byte for byte. Delete that copy after verification. Make the edit as one insertion of "l" directly after the target occurrence, with no editor reflow, line-ending or encoding conversion, or trailing-newline change.
Verify that the diff contains exactly that one replacement.
Do not add a test file, run an install, or reformat the document.
First check: README.md exists, and it contains exactly one occurrence of "npm instal" not immediately followed by "l". If the count is zero or more than one, stop before editing and report the count and the line numbers.
Judge: build the expected file from the saved original by inserting one "l" directly after the single "npm instal" not followed by "l". Pass only if `cmp` reports the edited README.md identical to that expected file, its size is exactly 1 byte larger than the original, the diff shows only that one line changed from "npm instal" to "npm install", and no file other than README.md was modified or added in the project.
```

- `depth`: the target is narrowed to the occurrence not followed by "l". This is because "npm install" contains "npm instal" as a substring, so the literal instruction would corrupt any correct occurrences already in the file. No scope or cost change.
- `depth`: a byte-for-byte `cmp` against an expected file built from the original is added alongside the owner's diff check. A line diff can hide changes to line endings, encoding, or the trailing newline, which "change no other byte" forbids. The cost is a temporary copy kept outside the project and deleted afterward. No file is added to the project.
- Skipped: `altitude`, because the owner fixed the scope to one replacement and fixing other typos would break "change no other byte". Also skipped: `range`, because no other field's method improves a one-byte edit and its exact check.
- Owner actions: none required. If the first check finds zero or several misspelled occurrences, decide which one to fix.
