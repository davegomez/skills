```text
Fix this TypeScript function: function formatLabel(value: string | null) { return value.trim(); }
It throws for null. Return the literal em dash "—" for null and preserve current trimming for every non-null string. Keep the public signature. No new dependencies and no changes outside this helper and its tests.
```
Unchanged: this is a small, clear task with one change, an exact null result, a fixed rule for non-null strings (including empty and whitespace-only ones), and firm scope limits. The task text shows no targeting or verification defect, and the tests the executor would write anyway already cover it.
