The task is a one-answer typo fix, so altitude and range don't apply. Depth fits only to sharpen the judge, for two reasons:

- **Substring trap.** "npm install" itself contains "npm instal". A naive count or replace-all would match correct occurrences too, or would add a second "l" to them.
- **No git.** The directory isn't a git repository, so there's no `git diff` to verify against. The original file has to be copied somewhere before the edit.

```text
In README.md replace the single exact string "npm instal" with "npm install". Change no other byte. Verify that the diff contains exactly that one replacement. Do not add a test file, run an install, or reformat the document.

Before editing:
- Locate the target precisely. "npm install" contains "npm instal" as a substring, so count only occurrences of "npm instal" NOT followed by "l" (e.g. `grep -c 'npm instal\([^l]\|$\)' README.md`, or an equivalent byte search).
- If that count is not exactly 1, stop and report every match with its line number. Do not edit.
- This directory is not a git repository, so snapshot the original first: `cp README.md /tmp/README.md.orig`. Keep the copy outside the project so no file is added to it.

Edit only that one occurrence, inserting the single byte "l". Do not use a replace-all or any tool that rewrites line endings, encoding, trailing whitespace, or the final newline.

Judge: run `diff /tmp/README.md.orig README.md` and `cmp -l /tmp/README.md.orig README.md | head`, and report both outputs.
Pass when all of these hold:
- the diff shows exactly one changed line, differing only by "npm instal" → "npm install";
- the new file is exactly 1 byte longer (`wc -c` on both files);
- a re-run of the count above returns 0.
Then delete /tmp/README.md.orig and report the results as observed, including any failure.
```

**Ledger**
- `depth`: the target count excludes existing "npm install" text, so the edit can't hit a correct occurrence or miss an ambiguous one. No scope change.
- `depth`: a snapshot outside the project replaces the missing `git diff`, which makes "verify the diff" executable without adding a file to the repo.
- `depth`: the judge checks the diff, a 1-byte length increase, and a zero count after the edit. Together these prove "change no other byte" rather than just asserting it.
- Skipped: `altitude`, because the fix is its own outcome. `range`, because it's a narrow fix with one right answer.
- Owner actions: none. The prompt stops and reports if the count isn't exactly 1.
