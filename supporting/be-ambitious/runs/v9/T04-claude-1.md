```text
In README.md, replace the single exact string "npm instal" with "npm install". Change no other byte.
Target the typo, not the substring: "npm instal" is also a prefix of the correct "npm install", so plain substring matching would also hit correct occurrences. Before editing, count the occurrences of "npm instal" that are not immediately followed by "l" (for example, `grep -n 'npm instal\([^l]\|$\)' README.md`), and separately count the existing "npm install" occurrences. Edit only if exactly one typo occurrence exists. If there are zero or more than one, stop and report the line numbers without editing.
Make the edit as a single insertion of "l" at that location. Use an edit that preserves line endings (LF/CRLF), encoding, BOM, trailing whitespace, and the final-newline state. Do not use an editor or tool that rewraps or normalizes the file.
Verify that the diff contains exactly that one replacement.
Do not add a test file, run an install, or reformat the document.
First check: README.md exists and is under version control, so `git diff` can show the change. If it is not, save a copy of the original outside the project tree before editing, diff against that copy, and delete the copy afterward.
Judge: `git diff --stat` (or `diff` against the original copy) shows exactly 1 file and 1 changed line; `cmp -l` / byte sizes show the new file is exactly 1 byte longer, differing only by an inserted "l" right after the one "npm instal" occurrence; no "npm instal" occurrence not followed by "l" remains; the "npm install" count rose by exactly 1. Pass only if all four hold.
```

- `depth`: Added a check that matches the typo but not correct "npm install", because the search string is a prefix of the replacement. Without it, a naive replace-all could produce "npm installl", and a naive occurrence count would give the wrong answer. No scope change.
- `depth`: Added a zero-or-many stop condition. "Single exact string" becomes a precondition the executor checks before editing instead of assuming it. No scope change.
- `depth`: The Judge now checks bytes: +1 byte, one inserted "l", line endings and final newline preserved, and before/after counts. This catches silent normalization that a line diff can miss. It costs nothing and changes no scope.
- Skipped: `altitude`, because fixing other typos or improving the README would break "Change no other byte". `range`, because no other field's method adds anything beyond the byte-level check.
- Owner actions: confirm README.md is version-controlled, or accept a temporary original copy outside the project tree for diffing. Decide what to do if the stop condition fires (zero or several occurrences).
