---
name: memory-triage
description: Triage the Claude Code auto memory of a repository. A script sorts each note, Claude examines only the doubtful ones, and the owner approves every change from 1 table.
disable-model-invocation: true
---

# Memory triage

Review the auto memory store of a repository for the cost of a script run plus the notes that need judgment. `scripts/triage.py` gives each note 1 class. You examine only the `check` and `alert` notes, and the owner approves every change from 1 table. The store stays unchanged until the owner answers.

| Class | The note has | Your work |
| --- | --- | --- |
| `alert` | a credential-like value | examine with [check](references/check.md) |
| `drop` | an empty body, the same body as another note, or a dated file name on a project note that is 30 days old or more and that no other session used | propose drop: the flags are the evidence |
| `check` | a sign that it can be stale or wrong | examine with [check](references/check.md) |
| `fix` | a frontmatter defect, or no line in the index | propose the repair |
| `keep` | no flag | count only |

A note takes the highest class of its flags, and its row lists every flag. Resolve each flag, not only the one that set the class: a `check` note can also carry a `fix` flag. Rows on `MEMORY.md` are defects of the index itself.

## Steps

1. **Scan.** In the repository, run `python3 scripts/triage.py` (the path is in this skill's folder). It finds the memory folder from the repository. When the owner names another store, add `--memory-dir DIR`. On a non-zero exit, give the owner the message and stop. The step is complete when the output ends with a `summary:` line.
2. **Examine.** For each `check` and `alert` row, follow the section of [check](references/check.md) for each of its flags. For each `fix` flag, write the repair:
   - A frontmatter flag: the missing field, taken from the note's own body. Choose `type` from the 4 kinds: `user` (the owner's role and preferences), `feedback` (corrections and confirmed approaches), `project` (ongoing work and decisions), `reference` (where to find information outside the repository). A note without frontmatter gets the whole block in the shape the other notes use.
   - `not in the index`: 1 index line in the form the index already uses, under 150 characters.
   - An index row: shorten the long line, remove the pointer to the missing file, or merge and drop entries until the index is under its limits.

   The step is complete when each row outside `keep` has 1 proposed result (keep, edit, merge, or drop) and its evidence.
3. **Propose.** Show 1 table with the columns code, class, note, proposed action, and evidence, numbered from 1. Give an edit as its exact old and new text. Give the `keep` notes as a count under the table. An `alert` row cites the file, the line, and the kind of match only.

   **Caution: a dropped note is deleted for good.** This skill makes no backup, because a copy doubles any credential in the store. Put this caution above the table.

   Ask the owner to answer `apply`, or `apply` with the codes to exclude. On any other answer, revise the table and ask again. The step is complete when the owner answers `apply`.
4. **Apply.** Apply each approved row and only those. Change a note in place, by exact-string edits or by the line removal in [check](references/check.md), never by writing the whole file again: a tool can mask parts of the text it shows you. For a merge, add the text to the other note, then drop the merged note. For each drop, delete the file and remove its line from `MEMORY.md`. For a symlink, delete the link and leave its target alone. The step is complete when each approved row is applied.
5. **Verify.** Run `python3 scripts/triage.py` again. The work is complete when its summary shows `alert 0` and `fix 0` among the flags, and the report gives each note outside `keep` with its result and evidence. Name each flag that remains because the owner excluded its row.
