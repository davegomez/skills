```text
In README.md, replace the single exact string "npm instal" with "npm install". Change no other byte. Do not add a test file, run an install, or reformat the document.

First checks, before editing:
- README.md exists in the working directory. The directory is not a git repository, so `git diff` is unavailable. Save a byte-exact copy of the original outside the project directory, e.g. `cp -p README.md /tmp/README.md.orig`, so you can diff against it. Delete the copy once the judge passes.
- Count the occurrences of "npm instal" that are NOT followed by "l", e.g. `grep -o 'npm instal[^l]\|npm instal$' README.md | wc -l`. Correct "npm install" already contains "npm instal" as a prefix, so a naive replace-all would corrupt it into "npm installl".
- Proceed only if exactly one such typo occurrence exists. If there are zero or more than one, stop and report the count and line numbers without editing.
- Note the file's line endings (LF vs CRLF), its trailing-newline state, and its byte size (`wc -c`). The edit must preserve all three apart from the +1 byte.

Edit: insert one "l" after that single "npm instal" occurrence only. Use an edit that does not re-save the file through a formatter or normalize whitespace, encoding, or line endings.

Judge (all must hold; report each result):
1. `diff /tmp/README.md.orig README.md` shows exactly one hunk with one line removed and one line added.
2. The removed and added lines are identical except that "npm instal" became "npm install".
3. `wc -c README.md` equals the original size + 1.
4. Line endings and trailing-newline state match the original (`file README.md` before and after; `tail -c 1 | xxd`).
5. The count of correct "npm install" occurrences rose by exactly 1. The count of standalone "npm instal" typos is now 0.
6. No new files remain in the project directory.
Pass condition: checks 1–6 all hold. If any fails, restore from the saved copy and report the failing check with its output.
```

- `depth`: the main risk is a naive replace hitting existing correct "npm install" strings, because the typo is a prefix of the fix. The prompt requires a standalone-occurrence count first and a stop when there is not exactly one. Edit cost is unchanged.
- `depth`: the directory is not a git repo, so a byte-exact snapshot stands in for git diff. The judge checks size +1, a single-hunk diff, and preserved line endings and trailing newline, which catches silent editor normalization. The temporary copy lives outside the project and is deleted after the judge passes, so no file is added.
- Skipped: `altitude`, because the owner pinned the change to one byte. Next rungs like fixing other typos or adding a docs spell-check would change other bytes or add files, both prohibited. `range` is skipped because no other field's method improves a one-byte edit beyond the byte-level verification above.
- Owner actions: none required. If the occurrence check finds zero or multiple typos, decide which one (if any) to fix.
