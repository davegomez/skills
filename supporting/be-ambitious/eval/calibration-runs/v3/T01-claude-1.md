```text
Fix the TypeScript helper `formatLabel(value: string | null)`, which currently does `return value.trim();` and throws for null.

Requirements (all must hold):
- For null, return the literal em dash "—" (U+2014). Not an en dash (U+2013), a hyphen, or "--".
- For every non-null string, return exactly what `value.trim()` returns today. That includes "" and whitespace-only input, which must still return "" and not "—".
- Keep the public signature `(value: string | null)` and the inferred `string` return type.
- No new dependencies. No changes outside this helper and its tests.

First checks:
- Locate the helper, its existing test file (if any), and the project's test runner and typecheck command.
- If no test file exists, create one next to the helper using the repo's existing test convention.
- Check whether a property-testing library such as fast-check is already a dependency. Use it only if it is. Otherwise, write a small seeded string generator inside the test file.
- Report anything you could not find.

Method:
1. Write the null test first. Run it against the original code and confirm it fails by throwing.
2. Implement the fix with an explicit `value === null` check. Do not use `||`, `??` on the trimmed result, or `== null`. Each of these would either change empty or whitespace-only output, or silently change behavior for undefined, which is out of scope.
3. Add a differential test that uses `String.prototype.trim` as the oracle. For a fixed edge-case table plus a few hundred seeded generated strings, assert `formatLabel(s) === s.trim()`. The table includes:
   - "", " ", "\t\n\r", "  a  ", and "a b"
   - Unicode whitespace that trim removes: U+00A0, U+FEFF, U+2028, U+3000
   - U+200B zero-width space, which trim keeps
   - an existing "—"
   - a lone surrogate
4. Assert the null result by code point (`"\u2014"`) so a lookalike character cannot pass.
5. Red-team the tests with mutation checks. Temporarily apply each mutant below, run the tests, and confirm at least one test fails. Then revert.
   - `value?.trim() || "—"`
   - `(value ?? "").trim() || "—"`
   - `value == null ? "—" : value.trimStart()`
   - returning "-" or "–" for null
   - Add a test for any mutant that survives.
6. Note in the report that `undefined` from untyped callers still throws, as before, and leave it as an owner decision.

With my approval only: read-only, list call sites that already guard null before calling formatLabel (e.g. `formatLabel(x ?? "")`), so I can decide whether to simplify them later. Change none of them.

Judge, with pass conditions:
- The null test fails on the original code and passes after the fix.
- The differential and edge-case tests pass on both the original code (for non-null input) and the fixed code.
- Every listed mutant is killed by at least one test.
- Typecheck passes.
- The diff touches only the helper and its test file.

Report each result with command output. Report any unrun check as unverified.
```

**Ledger**
- `depth`: The null test is written first and must go red, then green. This proves the fix addresses the reported throw. It adds no scope.
- `depth`: Differential testing against `String.prototype.trim` turns "preserve current trimming for every non-null string" into a check a tool can run. It covers generated strings, not only a few examples. fast-check is used only if it is already installed, so no new dependency is added.
- `range` (Unicode text handling): The edge-case table covers BOM, NBSP, line separator, ideographic space, zero-width space, and lone surrogates. It also checks the em dash by code point. Together these catch lookalike-dash and whitespace-coverage mistakes.
- `range` (mutation testing, done by hand with no Stryker dependency): This red-team step shows the tests would catch the likely wrong fixes. The main one is `|| "—"`, which turns "" or whitespace-only input into a dash and breaks the preservation requirement.
- `depth`: The prompt requires `=== null` and flags `undefined` as an owner decision. This keeps current behavior unchanged for untyped callers and avoids a silent widening of scope.
- `altitude`: The original outcome is a helper that no longer throws on null. The improved outcome also gives the owner a read-only map of redundant null guards at call sites. It sits behind approval and changes no files.
- Skipped: a hard stretch target. The deliverable is binary correctness, so no metric goes past the owner's bar.
- Owner actions:
  - Confirm the helper's location and the test runner.
  - Decide whether `undefined` should keep throwing.
  - Approve or decline the call-site report.
