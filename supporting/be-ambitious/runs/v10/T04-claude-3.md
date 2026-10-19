```text
In README.md replace the single exact string "npm instal" with "npm install". Change no other byte.
Locate the target before editing. "npm instal" is a prefix of "npm install", so a plain search or replace-all also matches text that is already correct. Count only occurrences of "npm instal" that are not immediately followed by "l". If that count is not exactly 1, stop without editing and report each match's line and byte offset.
Make the change as a single insertion of "l" directly after the one identified occurrence, not as a replace-all. Keep the original bytes in memory for comparison, and add no file to the project.
Do not add a test file, run an install, or reformat the document.
First check: README.md exists and is readable and writable. If it is not, report that and stop.
Judge: build the expected bytes from the original README.md by inserting the single byte "l" at offset (match offset + 10) of the one identified occurrence, then compare them with the edited file. Pass only if all of these hold: the comparison is byte-for-byte identical, including encoding, line endings, BOM, and final newline; the file grew by exactly 1 byte; the diff shows exactly one changed line, differing only by that inserted "l"; no test file was added and no install was run. A match count other than 1 leaves the result unverified.
```

- `depth`: the prompt now guards against the prefix collision. "npm instal" also matches inside the correct "npm install", so a naive count or replace-all could miscount, or turn correct text into "npm installl". The prompt counts only occurrences not followed by "l" and stops if the count is not exactly 1. No scope, cost, or access effect.
- `depth`: the judge now compares the whole file against the expected bytes, built from the original plus only the specified insertion. A line diff alone can miss changes to line endings, the BOM, the final newline, or encoding that an editor might make silently. This enforces "Change no other byte" directly and keeps the owner's diff check. It adds no file.
- Skipped: `altitude`, because this is a one-string typo fix with stated boundaries and nothing worth climbing toward. `range`, because no other field's method improves an exact single-byte edit.
- Owner actions: none required. If the executor reports zero or several misspelled occurrences, decide which one, if any, to fix.
