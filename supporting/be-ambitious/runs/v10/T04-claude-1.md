```text
In README.md replace the single exact string "npm instal" with "npm install". Change no other byte.
Assumption: the target is the misspelled "npm instal" that is not followed by "l". The search string is a prefix of the replacement, so any correct "npm install" already in the file also contains it, and a plain replace-all would corrupt it into "npm installl".
Locate the target as "npm instal" not immediately followed by "l". Make the one edit with a byte-preserving method so that encoding, line endings, trailing newline, and whitespace stay untouched. Before editing, save a copy of the original README.md outside the project directory to use as the comparison baseline.
Verify that the diff contains exactly that one replacement.
Do not add a test file, run an install, or reformat the document.
First check: README.md exists and contains exactly one occurrence of "npm instal" not followed by "l". If it contains zero or more than one, stop before editing and report the count and line numbers.
Judge: build the expected file from the saved original by replacing only the single "npm instal" occurrence not followed by "l" with "npm install". Pass only if `cmp` reports the edited README.md byte-identical to the expected file, the size grew by exactly 1 byte, and a diff against the original shows one changed line whose only difference is the added "l".
```

- `depth`: The search string "npm instal" is a prefix of "npm install", so it also matches every correct "npm install" already in the file. Targeting the occurrence not followed by "l" prevents a replace-all from producing "npm installl". The First check stops the work if the count is anything other than one. No scope or cost change.
- `depth`: The judge now compares the whole file byte-for-byte against an expected result built from the original plus only the specified change, and checks that the size grew by exactly 1 byte. This catches line-ending, encoding, and trailing-newline drift that a line diff can hide. It needs a temporary copy kept outside the project, so no file is added to the project.
- Skipped: `altitude`, because this is a one-character typo fix and no downstream decision depends on it. `range`, because no other field's method improves a single exact substitution.
- Owner actions: none required. If the First check finds zero or several matches, decide which occurrence is meant.
