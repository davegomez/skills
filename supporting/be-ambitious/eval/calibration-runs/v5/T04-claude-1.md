```text
In README.md, replace the single exact string "npm instal" with "npm install". Change no other byte. Do not add a test file, run an install, or reformat the document.

First check the belief the task rests on, using the raw bytes of README.md. "npm instal" is also a substring of the correct "npm install", so a plain search over-counts. Count the occurrences of "npm instal" that are not followed by "l", for example with `grep -o 'npm instal[^l]\|npm instal$'`, and also count the existing "npm install" occurrences.
- Proceed only if exactly one misspelled occurrence exists.
- If there are zero or more than one, stop and report the counts and line numbers without editing.

Before editing, record the file's byte size and SHA-256. Save a pristine copy to a new temp directory outside the project, so the diff has a baseline. The project is not a git repository. Delete that copy after verification.

Make the edit as a single-byte insertion: add one "l" after that occurrence. Use a method that cannot alter line endings, encoding, BOM, trailing whitespace, or the final newline. For example, use an exact-string edit tool and not an editor or formatter that rewrites the file.

Verify that the diff contains exactly that one replacement:
- `diff` of the pristine copy against README.md shows one changed line, and the only difference on it is "npm instal" → "npm install".
- The new size equals the old size + 1 byte.
- `cmp -l` against the pristine copy diverges first at the expected offset, right after the occurrence. Every byte after that offset matches the original shifted by one.
- The re-count shows zero misspelled occurrences and one more "npm install" than before.

Judge: report the pre-edit counts, the old and new size and SHA-256, the `diff` output, and the `cmp` offset.
Pass: exactly one misspelled occurrence before the edit, zero after, a one-line diff showing only the added "l", and size +1. Any other difference fails the check; report it as found rather than repairing it silently.
```

- `depth`: a pre-edit count that excludes the "npm install" substring match. It catches the case where a naive search-and-replace yields "npm installl" or finds a "single" occurrence that is actually ambiguous, and it stops before editing if the premise is false. No scope effect.
- `depth`: byte-level verification (size +1, `cmp` offset, SHA-256) on top of the line diff. A line diff can hide line-ending, BOM, or final-newline changes that "change no other byte" forbids. The cost is a temporary copy outside the project, which is deleted afterward. It is not a test file.
- Skipped: `altitude`, because the owner prohibited every change beyond this one byte, so fixing other typos or docs is out even with approval. `range`, because no other field's method adds to a byte-level diff check on a one-character edit.
- Owner actions: none required. Confirm that a temporary baseline copy outside the project is acceptable; without it, the diff needs another baseline, since the directory is not a git repo.
