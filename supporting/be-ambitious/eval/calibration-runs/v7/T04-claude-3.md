```text
In README.md replace the single exact string "npm instal" with "npm install". Change no other byte. Do not add a test file, run an install, or reformat the document.

First checks, before editing:
- Note that the target "npm instal" is a prefix of the replacement "npm install". Any correctly spelled "npm install" (or "npm installation") already in the file contains the target, so a plain find-and-replace can turn it into "npm installl".
- Count occurrences of "npm instal" at the byte level. Split them into (a) those followed by "l", which are already correct and must stay untouched, and (b) those not followed by "l", which are the typo. Record the byte offset of each (b) occurrence.
- Proceed only if there is exactly one (b) occurrence. If there are zero or more than one, stop without editing and report the counts, offsets, and surrounding lines.
- Before editing, snapshot the original bytes to a temporary path outside the project directory. Do not put the snapshot in the repo. The snapshot is the baseline for the diff, because the directory is not under version control.

Edit:
- Insert the single byte "l" immediately after the recorded (b) occurrence, using a byte-preserving method. Do not let any tool re-save the file in a way that normalizes line endings (CRLF/LF), the BOM, encoding, trailing whitespace, or the final newline.

Judge: all of the following must hold.
1. `diff <snapshot> README.md` shows exactly one changed line. The only difference on that line is "npm instal" → "npm install" at the recorded position.
2. The edited file is byte-identical to the original with "l" inserted at the recorded offset. Check with `cmp` against a reconstruction built from the snapshot. The file size is exactly 1 byte larger.
3. The count of (a) occurrences is unchanged plus one, the count of (b) occurrences is zero, and "npm installl" does not appear.

Pass only if all three hold. Report the offset, the diff output, and the before/after byte sizes. Then delete the temporary snapshot.
```

- `depth`: a prefix-collision pre-check. Because "npm instal" ⊂ "npm install", a naive replace can corrupt correct occurrences. Counting typo versus already-correct matches, and refusing to edit unless exactly one typo exists, prevents that. There is no scope change.
- `depth`: a byte-exact judge. The directory isn't a git repo, so "the diff" needs a baseline. A temporary snapshot outside the project, plus `diff`, `cmp` against a reconstruction, and a +1 byte size check, proves "change no other byte". That includes line endings, BOM, and the final newline, which a text diff can hide. Effect: one temporary file is created outside the project and then deleted. It is not a test file.
- Skipped: `altitude`, because the owner fixed the scope to one byte and other fixes are prohibited. Also skipped: `range`, because no other field's method improves a one-byte edit beyond the byte-level checks above.
- Owner actions: if the pre-check finds zero or multiple typo occurrences, decide which (if any) to change.
