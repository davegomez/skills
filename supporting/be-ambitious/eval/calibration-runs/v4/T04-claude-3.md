```text
In README.md, replace the single exact string "npm instal" with "npm install". Change no other byte. Do not add a test file, run an install, or reformat the document.

First checks, before editing:
- "npm instal" is also a prefix of "npm install". Count matches of "npm instal" that are NOT followed by "l" (for example, grep -o 'npm instal[^l]\|npm instal$'). Proceed only if the count is exactly 1. If it is 0 or more than 1, stop and report the count and line numbers. Do not guess which match to change, and never turn an existing "npm install" into "npm installl".
- This directory is not a git repository, so `git diff` is unavailable. Before editing, copy README.md to a snapshot outside the project directory (for example, under $TMPDIR). Do not create any file in the project.
- Record the file's byte size, line-ending style (LF or CRLF), presence of a BOM, and whether it ends with a newline. The edit must preserve all four. Use an exact-string edit, not a whole-file rewrite or formatter.

Make the one replacement at the confirmed match.

Judge:
(1) `diff <snapshot> README.md` shows exactly one changed line, and that line differs only by the inserted "l".
(2) The new byte size equals the old size plus 1.
(3) `cmp` reports that applying the one replacement to the snapshot gives a result byte-identical to the new README.md (for example, python3 -I -c that reads the snapshot bytes, applies .replace(b"npm instal", b"npm install", 1) at the confirmed offset, and compares the result to README.md).
(4) A fresh count of "npm instal" not followed by "l" returns 0.
Pass condition: all four checks hold. Report each command and its output. If any check fails, restore README.md from the snapshot and report the failure.
```

- `depth`: Guards against the substring trap. "npm instal" also matches every correct "npm install", so a naive replace could produce "npm installl". This adds no scope.
- `depth`: Replaces the unavailable `git diff` (this directory is not a repo) with a snapshot kept outside the project. The new judge checks byte size, does a byte-exact `cmp` against the expected result, and recounts matches. Together these prove "no other byte" mechanically instead of by eye. Cost: one temporary file outside the project.
- `depth`: Explicitly preserves line endings, BOM, and the final newline. Editors often change these silently.
- Skipped: `altitude`. The owner fenced the scope to one byte, so any higher rung, such as fixing other doc typos, would contradict "change no other byte." `range`: no other field's method improves a single-byte edit beyond the byte-level checks above.
- Owner actions: none required. If the first check finds 0 or more than 1 match, decide which occurrence is meant.
