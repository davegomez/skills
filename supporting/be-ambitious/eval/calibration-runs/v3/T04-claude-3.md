```text
In README.md, replace the single exact string "npm instal" with "npm install". Change no other byte. Do not add a test file, run an install, or reformat the document.

Before editing:
- Keep a byte-for-byte copy of the original README.md outside the working tree for comparison (e.g., in a temp directory), and record its byte size.
- Count matches of "npm instal" that are NOT already followed by "l". "npm instal" is a prefix of "npm install", so a plain find-and-replace would also hit correct occurrences and produce "npm installl". Use a match that excludes a following "l" (e.g., the regex `npm instal(?!l)`).
- Proceed only if there is exactly one such match. If there are zero or more than one, change nothing and report the count, each line number, and the surrounding text.

Edit:
- Insert only the single "l" at that match. Use a method that preserves encoding, line endings (LF/CRLF), trailing whitespace, and the presence or absence of a final newline. Do not use an editor or tool that rewrites the whole file with normalization.

Judge (all must pass; report each result):
1. The new file is exactly 1 byte larger than the original.
2. Deleting the one byte at the insertion offset from the new file gives a file byte-identical to the saved original (`cmp` reports no differences).
3. A unified diff of original vs. new shows exactly one changed line, and that line differs only by "npm instal" → "npm install".
4. A search for `npm instal(?!l)` in the new file returns zero matches, and the count of "npm install" went up by exactly one.
If any check fails, restore the saved original and report which check failed and its output.
```

- `depth`: a negative-lookahead match prevents the prefix trap where "npm instal" also matches correct "npm install" text and turns it into "npm installl". It costs nothing extra and stays within scope.
- `depth`: the edit runs only when there is exactly one match. On zero or several matches it stops and reports instead of guessing, which honors "single exact string."
- `depth`: the vague "verify the diff" becomes a byte-level judge (size +1, remove-the-byte `cmp` round trip, one-line diff, match counts). This catches line-ending, encoding, or final-newline changes that a line diff can hide. A failed check rolls back to the original.
- Skipped: `altitude`. The higher rungs (fixing other typos or docs) conflict with the owner's explicit "change no other byte." `range`: no other field's method improves a single-byte edit beyond the byte-level verification already added.
- Owner actions: none required. If the pre-edit count is not exactly one, decide which occurrence to fix.
