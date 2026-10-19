```text
In README.md, replace the single exact string "npm instal" with "npm install". Change no other byte. Do not add a test file, run an install, or reformat the document.

"npm instal" is a prefix of "npm install", so a plain find-and-replace can match correct text and produce "npm installl". Before editing:
- Copy the original README.md to a scratch location outside the repository for comparison. Delete the copy when done.
- Count occurrences of "npm instal" that are NOT followed by "l". Proceed only if that count is exactly 1. If it is 0 or more than 1, stop and report each match with its line number and byte offset, without editing.
- Record the byte offset of that occurrence, the file size, and any properties an editor could silently change: line endings (LF or CRLF), presence of a final newline, a UTF-8 BOM, and file mode.

Edit: insert the single byte "l" immediately after the matched "npm instal", using a byte-exact method that does not re-encode, re-wrap, or normalize whitespace or line endings.

Judge (all must pass; report each result):
1. New file size = original size + 1 byte.
2. `cmp -l` of original vs new shows the first difference exactly at the recorded offset + 10 (1-based: offset + 11).
3. Deleting the byte at that position from the new file yields a file byte-identical to the original (`cmp` exits 0).
4. A line diff (`diff original README.md`) shows exactly one changed line, and on that line the only change is "npm instal" → "npm install".
5. Line endings, final newline, BOM, and file mode match what was recorded.
Pass condition: checks 1–5 all pass. If any fails, restore the original from the scratch copy and report which check failed.
```

- `depth`: Fixes a concrete defect. "npm instal" also matches inside the correct "npm install", so a naive replace can corrupt correct text and still look plausible in a diff. The prompt now requires exactly one typo occurrence before any edit. No scope change.
- `depth`: Replaces "verify the diff" with a byte-level judge: size +1, first-difference offset, round-trip back to the original, and a single-line diff. It also adds checks for the silent changes editors make (line endings, final newline, BOM, file mode). This enforces "change no other byte". It costs a temporary scratch copy, which is deleted afterward.
- `depth`: A failed check now triggers a restore from the scratch copy, so a bad edit never stays in place. No scope change.
- Skipped: `altitude`, because the owner fixed the scope at one byte, and fixing other typos or docs would break "change no other byte". Skipped: `range`, because no other field's method improves a one-byte edit beyond the byte-level verification above.
- Owner actions: none required. If the pre-check finds 0 or more than 1 typo occurrences, decide which one to fix.
