```text
In README.md, replace the single exact string "npm instal" with "npm install". Change no other byte. Do not add a test file, run an install, or reformat the document.

First checks, before editing:
- Confirm README.md exists. If it doesn't, stop and report.
- "npm instal" is a prefix of "npm install", so a naive search also matches every correct "npm install" and a replace-all would turn them into "npm installl". Count occurrences of "npm instal" that are NOT followed by "l". Expect exactly one. If you find zero or more than one, stop and report each byte offset and line without editing.
- Record the file's byte size, whether it has a UTF-8 BOM, its line endings (LF or CRLF), and whether it ends with a newline. Edit tools can silently normalize these, so they are part of "no other byte."
- Copy the original README.md to a system temp directory outside the project, for the comparison below. Delete the copy afterward. Create nothing inside the project.

Edit: insert a single "l" immediately after the matched "npm instal". Use an edit that preserves the BOM, line endings, and trailing newline exactly.

Judge: byte-level comparison of the original copy with the edited README.md. All of the following must hold:
1. The new size equals the original size + 1.
2. Let N be the offset just past the matched "npm instal". The first N bytes of both files are identical.
3. Byte N of the new file is "l".
4. The original bytes from N to the end equal the new bytes from N+1 to the end.
5. `diff` shows exactly one hunk. That hunk changes one line, and the only difference within it is "npm instal" → "npm install".
Report each check as pass or fail with the command output. If any check fails, restore the original from the temp copy and report.
```

- `depth`: guards against the prefix trap, where "npm instal" also matches the correct "npm install". The edit becomes a negative-lookahead match plus a one-byte insertion, so correct occurrences cannot become "installl". No scope or cost change.
- `depth`: "change no other byte" is now checked byte for byte. This covers size +1, identical prefix and suffix around the insertion point, and preserved BOM, line endings, and trailing newline, in addition to a line diff. Benefit: it catches silent normalization by edit tools that a line diff can miss.
- `depth`: the directory is not a git repo, so there is no `git diff` to compare against. A temporary copy outside the project serves as the baseline and is deleted afterward. Risk: minimal. Nothing is added to the project.
- Skipped: `altitude`, because every higher rung (fixing other typos or other install docs) needs edits the owner prohibited with "change no other byte." `range`, because no other field's method improves a one-byte replacement beyond the byte-exact check above.
- Owner actions: none required. If the first check finds zero or more than one occurrence, decide which one to fix.
