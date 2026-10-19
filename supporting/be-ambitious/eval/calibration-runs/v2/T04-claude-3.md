**Finding from reading `README.md`:** the file contains `npm instal` twice by substring match. The typo is on line 3. Line 11 holds a correct `npm install`, which also contains the string "npm instal". A naive replace-all would turn line 11 into `npm installl`. The rewrite pins the edit to the standalone occurrence. The file is 412 bytes of ASCII and ends with a newline.

```text
In README.md replace the single exact string "npm instal" with "npm install". Change no other byte. Do not add a test file, run an install, or reformat the document.

Target only the standalone typo: "npm instal" not immediately followed by "l". README.md currently has two substring matches. Line 3 has `npm instal` (the typo). Line 11 has `npm install`, which is already correct and must stay unchanged. A replace-all would corrupt line 11 into "npm installl".

First checks, before editing:
- Confirm that exactly one occurrence of "npm instal" is not followed by "l" (e.g. `grep -nE 'npm instal([^l]|$)' README.md`). If the count is not exactly 1, stop and report what you found instead of editing.
- Record the original byte count (expected 412), the encoding (ASCII), the line endings, and whether the file ends with a trailing newline.
- The directory is not a git repo, so save a pristine copy for diffing outside the project directory (e.g. under $TMPDIR). Delete it when done. Nothing new may remain in the project.

Make the edit with a tool that changes only that span: a single-occurrence exact-match edit of "`npm instal`" on line 3. Do not rewrite the file through anything that could normalize whitespace, line endings, or the final newline.

Judge, with observable pass conditions. All must hold, and each is reported with its command output:
1. `diff` of original vs. edited shows exactly one changed line, line 3: `npm instal` → `npm install`.
2. `cmp -l` reports exactly one-byte growth. The new size is 413 bytes and every byte before the insertion point is identical.
3. Line 11 still reads `npm install` (not `installl`). `grep -c 'npm installl' README.md` returns 0.
4. The trailing newline and line endings are unchanged, and no new files exist in the project directory.
If any check fails, restore the pristine copy and report the failure rather than retrying silently.
```

- `depth`: Added a guard so the edit hits only line 3. The literal "npm instal" also matches inside the correct `npm install` on line 11, so a plain replace would corrupt it. No scope change.
- `depth`: Strengthened the judge. The diff check now also requires exactly +1 byte (412→413), an unchanged line 11, an unchanged trailing newline and line endings, and no new files. This catches silent reformatting that a visual diff misses. Cost: one temporary copy outside the project, deleted afterward. That respects "no test file" and adds no artifacts.
- Skipped: `altitude`, because the deliverable is a one-word typo fix with no larger outcome to serve. `range`, because a narrow fix with one right answer gains nothing from other fields.
- Owner actions: none required. If you'd rather not have even a temporary copy under `$TMPDIR`, the judge can instead compare against the recorded byte count and the exact expected line content.
