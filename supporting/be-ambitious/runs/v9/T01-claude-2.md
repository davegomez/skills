```text
Fix this TypeScript function: function formatLabel(value: string | null) { return value.trim(); }
It throws for null. Return the literal em dash "—" for null and preserve current trimming for every non-null string. Keep the public signature. No new dependencies and no changes outside this helper and its tests.
```
Unchanged: this is one small, clearly bounded change with a stated result, and the task text shows no targeting or verification defect. The obvious tests (null returns "—", and non-null strings including whitespace-only ones still match `value.trim()`) are ones the executor would write anyway, and a property-based library would break the no-new-dependencies rule.
