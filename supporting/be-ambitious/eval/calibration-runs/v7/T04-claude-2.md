```text
In README.md, replace the single exact string "npm instal" with "npm install". Change no other byte. Do not add a test file, run an install, or reformat the document.

"npm instal" is a prefix of "npm install", so a plain substring search also matches any correct "npm install" already in the file. Editing one of those would produce "npm installl".

First, before editing:
- Confirm README.md exists.
- Record its byte size and a SHA-256 hash.
- Count occurrences of "npm instal" not followed by "l" (for example, `grep -o 'npm instal\($\|[^l]\)'`). Also count all "npm install" occurrences.
- If the misspelled count is not exactly 1, stop and report both counts without editing.

Edit only that one occurrence with an exact, single-occurrence string replacement. Use no editor or tool that rewrites line endings, trailing newline, encoding, BOM, or whitespace.

Judge: the edit passes only if all of these hold:
(a) `diff` against the original shows exactly one changed line, and the only difference on it is "npm instal" → "npm install";
(b) the new file is exactly 1 byte larger than the original;
(c) `cmp` reports the first difference at the expected offset, and the bytes after it match the original shifted by one;
(d) a re-count finds 0 misspelled occurrences, and the "npm install" count is one higher than before.
Report the before and after counts, sizes, hashes, and the diff.
```

- `depth`: the target string is a prefix of its replacement, so a naive find-replace could change a correct "npm install". The rewrite requires a not-followed-by-"l" match and exactly one hit before editing, and stops otherwise. No scope change.
- `depth`: the judge now uses byte-level checks: a +1 byte size delta, a `cmp` offset, and before/after counts and hashes. A line diff alone would miss changes to line endings, encoding, or the trailing newline. This stays within "change no other byte" and the required diff check.
- Skipped: `altitude`, because fixing other typos or doc issues is a change the owner prohibited. `range`, because no other field's methods add anything to a one-byte edit.
- Owner actions: none required. If the pre-check finds zero or several misspelled occurrences, decide which one, if any, to change.
