```text
In README.md, replace the single exact string "npm instal" with "npm install". Change no other byte. Do not add a test file, run an install, or reformat the document.

First, before editing, inspect README.md read-only:
- Count occurrences of "npm instal" that are NOT already followed by "l" (i.e. the actual typo). "npm instal" is a prefix of "npm install", so a naive replace-all would turn any correct "npm install" into "npm installl".
- If the typo occurs zero times or more than once, stop and report the count and line numbers instead of editing; the task says "the single exact string".
- Note the file's byte length, line endings (LF vs CRLF), encoding/BOM, and whether it ends with a trailing newline, so the edit can be shown not to alter them.

Make the edit as a targeted single-occurrence replacement of the typo instance only (an exact-match edit tool, or an equivalent that does not rewrite line endings, trim whitespace, or re-encode). Keep the original bytes available for comparison without adding a file to the project (hold them in memory, or in a temp path outside the repository that you delete afterward).

Judge: compare original and edited bytes. Pass only if all of the following hold, and report each:
1. The edited file is exactly 1 byte longer than the original.
2. A unified diff shows exactly one changed line, where the only difference is "npm instal" -> "npm install".
3. A byte-level comparison (e.g. `cmp -l`) shows that every byte before the inserted "l" is identical, and every byte after it matches the original shifted by one.
4. Occurrences of "npm installl" = 0; occurrences of the typo = 0; occurrences of "npm install" = original count + 1.
5. Line endings, BOM, and trailing newline match what was recorded before the edit.
If any check fails, restore the original bytes and report the failing check with its output.
```

- `depth`: The rewrite guards against the prefix hazard, because "npm instal" also matches inside every correct "npm install". It checks the occurrence count before editing and replaces a byte-length, `cmp`, and occurrence-count check for an eyeballed diff. Benefit: it catches a silent "installl" corruption and any line-ending or encoding drift that the original "verify the diff" step could miss. There is no scope change. The original bytes stay in memory or in a temp path outside the repo, so no test file is added.
- Skipped: `altitude`. "Change no other byte" sets the deliverable, so fixing other typos or doc improvements is out of bounds. `range`: no other field's method improves a single-byte replacement beyond the byte-level checks above.
- Owner actions: none required. If the pre-edit count isn't exactly 1, decide which instance is the intended one. I haven't inspected README.md, so the occurrence count is still unverified.
