```text
In README.md, replace the single exact string "npm instal" with "npm install". Change no other byte. Do not add a test file, run an install, or reformat the document.

Before editing:
- Count matches of "npm instal" that are NOT already followed by "l". "npm install" contains "npm instal" as a substring, so a naive replace could turn a correct "npm install" into "npm installl". Proceed only if exactly one bare "npm instal" exists. If there are zero or several, stop and report the line numbers without editing.
- This directory is not a git repository, so `git diff` has no baseline. Copy README.md to a scratch location outside the repo (for example $TMPDIR/README.md.orig) to diff against.
- Record the original file's byte size, line-ending style (LF or CRLF), and whether it ends with a trailing newline.

Edit:
- Insert the single "l" at that one occurrence with an exact-string edit. Do not rewrite or re-save the file through any tool that could normalize line endings, encoding, BOM, trailing whitespace, or the final newline.

Judge, reported with its output:
1. `diff "$TMPDIR/README.md.orig" README.md` shows exactly one changed line, and that line differs only by "npm instal" becoming "npm install".
2. `cmp -l "$TMPDIR/README.md.orig" README.md` (or an equivalent byte-level check) shows the new file is exactly 1 byte larger. Every byte before the insertion point is identical, and every byte after it is identical once shifted by one.
3. Line-ending style and trailing-newline state match the original.
4. The bare "npm instal" count is now 0, and the "npm installl" count is 0.
Pass when all four hold. Afterward, delete the scratch copy, and confirm that no new files remain in the repo.
```

- `depth`: adds a precondition that guards against the substring trap. "npm instal" also matches inside every correct "npm install", so only a bare occurrence counts, and it must be unique. This prevents a silent "installl" corruption. No scope change.
- `depth`: replaces the unspecified diff check with a stronger judge. The text diff is paired with a byte-level check (+1 byte, all other bytes identical), and line endings and the final newline are confirmed preserved. This catches invisible normalization that a line diff can miss. Cost: one temporary copy outside the repo, removed afterward.
- `depth`: because the directory is not a git repo, the prompt makes a baseline copy so the required diff can actually be produced.
- Skipped: `altitude` would mean fixing other typos or doc quality, which "change no other byte" explicitly forbids. `range` was skipped because no other field's method improves a one-character edit beyond the byte-level verification already added.
- Owner actions: none required. If the precondition finds zero or several bare matches, decide which occurrence is intended.
