```text
Fix the TypeScript helper `formatLabel(value: string | null)`, which currently does `return value.trim();` and throws for null.

Requirements (fixed):
- For null, return the literal em dash "—" (U+2014, one character).
- For every non-null string, return exactly what `value.trim()` returns today.
- Keep the public signature: name, parameter type `string | null`, export form, and return type `string`.
- No new dependencies. No changes outside this helper and its tests.

Assumption: the job is to remove the crash without changing any rendered non-null label. Empty and whitespace-only strings must keep returning "" and must not become "—". A falsy check such as `value?.trim() || "—"` would break this, so branch on `value === null` only.
Assumption: runtime `undefined` is outside the signature. Leave its behavior unchanged and mention it in the report rather than handling it.

First checks: find the helper, its existing tests, the test runner, and how the project type-checks (for example `tsc --noEmit`). Record the current signature and inferred return type before editing. If there is no test file for the helper, create one next to the existing test convention. If a runner or type-check is unavailable, say so and mark that part unverified.

Method:
1. Write the null test first and run it. It must fail (red) against the current code.
2. Pin the current trimming with characterization tests that compare `formatLabel(s)` against `s.trim()`, using cases built from the ECMAScript WhiteSpace and LineTerminator sets:
   - tab, VT, FF, space, NBSP U+00A0, BOM U+FEFF, Zs characters such as U+1680, U+2000–U+200A, U+202F, U+205F, U+3000, and LF, CR, U+2028, U+2029
   - non-trimmed look-alikes: U+200B zero-width space, U+180E, U+2060
   - "", whitespace-only strings, interior whitespace, lone surrogates, astral characters at the edges, and a non-null string that is itself "—"
3. Aim for exhaustive equivalence on single code units. For all 65,536 UTF-16 code units, assert that `formatLabel(c) === c.trim()`, and do the same for `c + "x" + c`. Add a seeded, dependency-free random-string loop (a fixed seed, so failures reproduce) that mixes the edge set with ordinary text and compares against `.trim()`. If the project already lists fast-check as a dependency, you may use it instead. Do not add it.
4. Make the minimal fix: an explicit `=== null` branch returning "—", otherwise `value.trim()`. Assert the null result with `=== "\u2014"` and `length === 1`, so an en dash or hyphen fails.
5. Hand-mutation check. Temporarily replace the fix with `value?.trim() || "—"`, then with `value == null ? "—" : value` (no trim). Confirm that at least one test fails for each. Revert both and confirm the fix is restored.
6. Read-only caller scan. Search the codebase for call sites that catch the old TypeError or pre-guard null before calling `formatLabel`. Report them, since their behavior or redundancy changes. Do not edit them.

Report: the diff, the test results before and after, the type-check result, the mutation-check outcomes, the exhaustive and seeded sweep counts with the seed, and the caller-scan findings.

Judge: the null test goes red before the fix and green after. All characterization, exhaustive code-unit, and seeded tests pass. Both mutants are killed. The type-check passes with the signature and return type unchanged. The diff touches only the helper and its test file.
```

- `depth`: characterization tests against `s.trim()` as the oracle, plus an exhaustive sweep of all 65,536 code units and a seeded random sweep. This turns "preserve current trimming for every non-null string" from asserted into tested. Cost: seconds of test time; no dependencies.
- `depth`: red-first null test, an exact U+2014 assertion, and hand-mutation of the two likeliest wrong fixes (`||` and dropped trim). These prove the tests can catch the `""`/whitespace-only → "—" regression. No scope effect, because the mutations are reverted.
- `range`: Unicode/ECMAScript text-processing knowledge supplies the edge corpus. That covers Zs, BOM, line separators, and the U+200B/U+180E look-alikes that a naive test set misses.
- `range`: a red-team read-only caller scan finds code that relied on the throw or guards null redundantly. It is reported without being edited, so it stays inside "no changes outside this helper."
- Skipped: `altitude`. The next rung would be fixing or simplifying callers, or how missing labels render, and that requires changes outside the helper, which you prohibited.
- Owner actions: confirm that leaving runtime `undefined` behavior unchanged is intended, and decide what to do about any callers the scan reports.
