**Task:** fix one typo in README.md for whoever reads the install instructions. Requirements: replace exactly `npm instal` → `npm install`; change no other byte; verify the diff shows only that replacement; no test file, no install, no reformatting.

**Lenses**
- **Altitude: skipped.** This is a one-byte typo fix, and the owner explicitly fenced the scope.
- **Depth: fit.** `npm instal` is a prefix of `npm install`. A naive replace-all would turn any correct `npm install` into `npm installl`. A line-based diff can also hide line-ending, BOM, or trailing-newline changes. A byte-level check closes both gaps.
- **Range: skipped.** A narrow fix with one right answer.

```text
In README.md, replace the single exact string "npm instal" with "npm install". Change no other byte. Do not add a test file, run an install, or reformat the document.

Before editing:
1. Copy README.md to a temp location outside the repo as the baseline.
2. Count occurrences of "npm instal" that are NOT followed by "l" (e.g. `grep -o 'npm instal\($\|[^l]\)'` or equivalent). "npm instal" is a prefix of "npm install", so a plain replace-all would corrupt correct occurrences into "npm installl".
   - Exactly 1 match: proceed.
   - 0 or more than 1: stop and report the matches with line numbers; do not edit.
3. Note the file's line endings (LF/CRLF), any BOM, and whether it ends with a newline. The edit must preserve all three.

Edit: insert a single "l" at that one occurrence, using an exact-string edit, not a regex replace-all and not a rewrite of the file.

Judge, all must hold:
- `cmp -l baseline README.md` shows the files diverge exactly at the byte after "npm instal". The new file is exactly 1 byte longer (compare `wc -c`).
- `diff baseline README.md` shows one changed line whose only difference is "npm instal" → "npm install".
- The count from step 2 is now 0. The count of "npm installl" is 0.
- No other files were created or modified in the repo.
Report the observed outputs of these commands, not a summary. If any check fails, restore the baseline and report the failure.
```

**Ledger**
- `depth`: a pre-edit occurrence count that excludes `npm install` prevents corrupting correct instances and stops on ambiguity. No scope or cost change.
- `depth`: byte-level judge (`cmp -l`, a +1 byte count, preserved line endings, BOM, and final newline) proves "change no other byte" literally, where a line diff could miss invisible changes. No scope change.
- `depth`: the baseline copy is kept outside the repo and restored on failure, which keeps the edit reversible without leaving a file behind.
- Skipped: `altitude` (the owner fenced the scope to one typo) and `range` (no other field's method is needed for a single-byte fix).
- Owner actions: none. The repo isn't under git, so the prompt uses a temp baseline instead of `git diff`.
