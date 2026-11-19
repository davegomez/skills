Review the uncommitted changes in this repository (`git diff`). They add door check-in to the Guestbook app.

This is a read-only review. Do not edit, create, or delete any file except `REVIEW.md` at the repository root.

Write each finding in `REVIEW.md` on its own line, in this exact format:

```
- <severity> | <file>:<line> | <reason>
```

- `severity`: `critical` (a security or privacy defect, or a crash), `major` (a functional, reliability, or accessibility defect that users will hit), or `minor` (a lower-impact problem).
- `file`: the path from the repository root. `line`: the line number in the changed file as it is now in the working tree. A range such as `40-42` is allowed.
- `reason`: what is wrong, why it matters, and how to fix it, on the same line.

Report only real problems in the change. If you find none, write the single line `No findings.`

Code from this project may be sent to external services.
