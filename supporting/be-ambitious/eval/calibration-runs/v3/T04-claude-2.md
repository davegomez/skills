```text
In README.md, replace the single exact string "npm instal" with "npm install". Change no other byte. Do not add a test file, run an install, or reformat the document.

First check the target: count occurrences of "npm instal" that are NOT already followed by "l" (i.e. the typo, not a correct "npm install"). Correct "npm install" occurrences contain "npm instal" as a substring and must stay untouched. If the typo count is not exactly 1, stop and report the count and line numbers instead of editing.

Before editing, save a byte-exact copy of README.md outside the repository (e.g. a temp file). Make the edit as a targeted single-occurrence replacement, not a whole-file rewrite, so line endings (LF/CRLF), trailing newline, encoding, BOM, tabs, and trailing whitespace are preserved.

Judge, all must hold:
1. `cmp -l <copy> README.md` reports differences starting at exactly the byte offset of the inserted "l", and the new file is exactly 1 byte longer than the copy (`wc -c`).
2. The original with that one "l" inserted at that offset is byte-identical to the new file (e.g. reconstruct with head/printf/tail and `cmp`, which reports no output).
3. `diff <copy> README.md` shows one changed line whose only difference is "npm instal" -> "npm install".
Report the three results. If any check fails, restore README.md from the copy and report the failure.
```

- `depth`: byte-level judge (`cmp` offset + size delta + reconstruction) replaces a line diff, which can hide line-ending, trailing-newline, or encoding changes that violate "change no other byte". No scope or access change.
- `depth`: pre-edit occurrence count excluding correct "npm install" guards the substring trap (a naive replace turns "npm install" into "npm installl"), and stops on 0 or 2+ matches instead of guessing. No scope change.
- `depth`: byte-exact backup with restore-on-failure keeps the edit reversible without relying on git. Temp file only, nothing added to the repo.
- Skipped: `altitude`, since the owner fixed scope to one byte and forbade other changes, so fixing other typos would contradict an explicit requirement. `range`, since no other field's method improves a single-byte edit beyond the byte-level check.
- Owner actions: none required. If the occurrence count is not 1, decide which occurrence to fix.
