```text
Fix formatLabel so it no longer throws for null, without changing what it returns for any non-null string.

Current code: function formatLabel(value: string | null) { return value.trim(); }

Requirements (all fixed):
- For null, return the literal em dash "—" (U+2014 EM DASH, not a hyphen, en dash, or "--").
- For every non-null string, return exactly what value.trim() returns today.
- Keep the public signature: function formatLabel(value: string | null), with an inferred return type that is still string.
- No new dependencies. No changes outside this helper and its tests.

Assumption: callers can pass only string | null, as the signature says. Use a strict check (value === null) so behavior for undefined is unchanged, and mention this in the summary.

First checks, before editing:
- Find the file that defines formatLabel and its existing test file, if any.
- Find the project's existing test runner and the command that runs it.
- If there is no test runner, say so. Add only tests the existing tooling can run, and report what stays unverified.

Method:
1. Characterize before you change anything. Write tests that pin today's non-null behavior. Use String.prototype.trim directly as the oracle, over a fixed corpus that includes:
   - "", " ", "\t\n\r\v\f", "  a  ", "a b", and already-trimmed strings
   - Unicode whitespace that trim removes: U+00A0, U+FEFF, U+2028, U+2029, U+3000, U+1680, U+2000–U+200A
   - Characters trim keeps: U+200B zero-width space, and an emoji or surrogate pair at each edge
   - A whitespace-only string, which must still return "" and not "—"
   - The literal string "null", and a string that is already "—"
   Run these tests against the unchanged function. They must pass.
2. Write a null test that asserts formatLabel(null) === "\u2014". Run it against the unchanged function and confirm it fails because a TypeError is thrown.
3. Make the smallest fix inside formatLabel. Leave the trim path textually unchanged, so non-null behavior cannot drift.
4. Run the full test file again, then run the project's type check if one exists.

Judge: the existing test runner shows the null test red before the fix and green after. Every characterization test is green both before and after the fix. The type check, if present, passes. Report the commands you ran and their results, the U+2014 assertion, and the undefined note. Any check you could not run is reported as unverified.
With my approval only: list, without editing, any other call sites or helpers in the codebase that call .trim() on a possibly-null value. Report each with file:line.
```

- `depth`: Pin current behavior with characterization tests, using `trim` itself as the oracle on a Unicode-edge corpus. This proves "preserve current trimming for every non-null string" with evidence instead of assuming it. It adds no scope or dependencies.
- `depth`: The null test goes red, then green, and asserts the exact code point U+2014. This catches look-alike dashes and confirms the test detects the original bug.
- `depth`: Fixing the whitespace-only case at `""` and leaving the trim path untouched blocks a tempting "improvement" that would break the owner's preservation requirement.
- `altitude`: The original outcome is that this one helper stops throwing. The improved outcome also covers other null-unsafe `.trim()` call sites, but only as a read-only report behind approval. No edits outside the helper.
- Skipped: `range`. Methods from other fields (e.g., mutation testing via Stryker) would need new dependencies, and nothing else changes this small, exactly specified fix.
- Owner actions: confirm the `=== null` assumption, meaning `undefined` still throws. Decide whether to approve the call-site report. Confirm that a test runner exists.
