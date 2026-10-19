```text
Fix this TypeScript function: function formatLabel(value: string | null) { return value.trim(); }
It throws for null. Return the literal em dash "—" for null and preserve current trimming for every non-null string. Keep the public signature. No new dependencies and no changes outside this helper and its tests.
```
Unchanged: this is one stated change with its exact result ("—" for null, the same `trim()` for every non-null string), a fixed signature, and closed scope. It shows no targeting or verification defect, and any extra testing would be either what the executor writes anyway or blocked by the no-dependencies and helper-only limits.
