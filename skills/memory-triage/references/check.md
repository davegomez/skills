# Check

How to examine each flag on a `check` or `alert` row. A row can carry several flags: examine each one.

## Results and evidence

Propose 1 result per note:

- **keep**: the note holds as written.
- **edit**: the exact old text and the exact new text.
- **merge into `<note>`**: the exact text to add to the other note. The merged note is then dropped.
- **drop**: delete the note and its index line.

Each result needs **evidence**: 1 fact the owner can verify in a minute. Evidence is a commit (short hash and subject), a file path with a line number, a timestamp from the origin extract, or the other note of a pair. When you find no evidence, propose keep and write what you could not verify.

## Sources

- **The repository**: its files and `git log`.
- **The origin extract**: `python3 scripts/triage.py --origin <note>` prints the last messages the owner typed before the session first wrote the note, and the time of each write. This command is your only way into a transcript: one transcript line can hold megabytes, and the extract leaves out tool results and credential-like values. `origin: unknown` means the transcript is gone; rely on the repository.
- **The use count**: `uses=N` is the number of sessions, other than the one that wrote the note, that named the note in a tool call. It is a lower limit: `uses=0` means no recorded use. `unknown` means the transcripts could not be read.

## Flags

### credential-like value

The value stays out of everything you write: the table, the report, and every command cite the file, the line, and the kind of match only. Propose 1 of these:

- Remove the flagged lines by their numbers, every flagged line of 1 note in 1 command, because each removal shifts the numbers below it: `perl -i -ne 'print unless $. == <a> || $. == <b>' <note>`. When a line also holds a fact worth keeping, add that fact back with an edit whose text holds no value.
- A `private-key` match flags only the BEGIN line of a block of several lines. Find its END line with `grep -nF 'PRIVATE KEY-----' <note> | cut -d: -f1`, which prints line numbers only: the END line is the first number after the BEGIN line. Remove the block as a range in the same command as the other flagged lines: `perl -i -ne 'print unless ($. >= <begin> && $. <= <end>) || $. == <a>' <note>`. When no number follows the BEGIN line, drop the note.
- Drop the note, when nothing else in it is worth keeping.

In the same row, tell the owner to rotate the credential: it sat in a plain file and can also sit in transcripts. When you judge the match false, say so in the evidence, in words that do not repeat the value, and let the owner exclude the row.

### dated file name

The note records 1 event: a day, a release. Ask whether it holds a lesson that outlives the event. Keep it, or edit it to state the lesson alone. Drop it when only the event is left; cite the age, the use count, and the commit or file that shows the event is over.

### project note N days old

Project notes record work in progress, and work ends. Test each claim against the repository now: `git log --oneline --since=<modified date> -- <paths the note names>` and the files. Keep it when the claim still holds, edit it when the claim changed, and drop it when the work is done or abandoned. Cite the commit or file.

### relative date

A word like "yesterday" loses its meaning a day later. Edit it to the absolute date: the date of the typed message in the origin extract, else the `modified` date of the note. Cite that timestamp.

### dead path

Find what happened to the path: `git log --oneline --name-status -1 -- <path>` shows the commit that renamed or deleted it. Edit the note to the new path, or drop the note when it was only about the deleted file. For a `~` or absolute path outside the repository, search near the old location; when nothing turns up, propose keep and ask the owner where it went.

### near duplicate of `<note>`

Read both notes. When they state the same fact, merge into the more complete note, or into the one the index names; cite the overlapping text. When they state different facts, keep both and cite the difference.

### unreadable

The entry is a symlink out of the memory folder, a folder, a binary file, or a file the script could not read. Leave its target unopened. Propose to drop the entry (for a symlink, the link only), or to keep it when the owner placed it there on purpose; ask in the evidence column.
