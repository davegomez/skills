```text
In README.md replace the single exact string "npm instal" with "npm install". Change no other byte. Do not add a test file, run an install, or reformat the document.

Before editing, check the dependencies:
- Confirm README.md exists.
- Confirm you have a pristine baseline to diff against: either version control showing README.md unmodified, or a copy written outside the project directory and deleted afterward.

Locate the target safely. "npm instal" is a prefix of the correct "npm install", so a plain substring search also counts every correct occurrence, and a replace-all would turn each one into "npm installl".
- Count only occurrences of "npm instal" that are not followed by "l".
- Record the byte offset of each occurrence.
- If the count is not exactly 1, stop and report the count and offsets without editing.

Make the change as a single insertion of the byte "l" immediately after the matched "npm instal". Use an edit method that does not touch line endings (LF/CRLF), trailing whitespace, the final newline, encoding, or a BOM.

Verify the change:
- The diff contains exactly one replacement, "npm instal" → "npm install".
- The new file is exactly 1 byte longer than the baseline.
- Deleting the byte at the recorded insertion offset from the new file reproduces the baseline byte-for-byte (cmp exits 0).
- A recount finds zero occurrences of "npm instal" not followed by "l".
- The count of "npm installl" is unchanged from the baseline.

Judge: report the diff, the before/after byte sizes, the cmp exit status after removing the inserted byte, and the recounts. Pass only if the diff shows exactly that one replacement, the size grows by exactly 1, cmp exits 0, and both recounts hold.
```

- `depth`: the task's own literals show a defect, because the search string is a prefix of the replacement. A naive count or replace-all would misjudge "single" or corrupt correct lines, so the prompt counts only occurrences not followed by "l" and stops unless there is exactly one. No scope change.
- `depth`: the judge goes from reading the diff to a byte-level check (size +1, then cmp after removing the inserted byte). This enforces "change no other byte" against invisible changes a diff view can hide, such as line endings, final newline, or BOM. The cost is one temporary baseline copy kept outside the project and deleted afterward, which avoids adding a file.
- Skipped: `altitude`, because the owner fixed the scope to one replacement with no downstream decision to climb toward, and fixing other typos is prohibited. `range`, because no other field's method improves a single-byte edit beyond the checks above.
- Owner actions: none are required. If README.md isn't under version control, the run creates and removes a temporary baseline copy outside the project directory. Say so if you'd rather it didn't.
