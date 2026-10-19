```text
Fix `formatLabel` in TypeScript so it no longer throws for null:

    function formatLabel(value: string | null) { return value.trim(); }

Requirements (all must hold):
- For `null`, return the literal em dash "—" (U+2014). Do not return a hyphen "-", an en dash "–", or a padded variant.
- For every non-null string, return exactly what `value.trim()` returns today.
- Keep the public signature: same name, same parameter type `string | null`, same `string` return type, same export form.
- No new dependencies. No changes outside this helper and its tests.

Method:
1. Before editing, write characterization tests that pin current trimming behavior, using `String.prototype.trim` as the oracle. Cover:
   - empty string `""` → `""` (not "—")
   - whitespace-only strings → `""` (not "—")
   - leading, trailing, and both-side ASCII whitespace: space, \t, \n, \r, \v, \f
   - Unicode whitespace that `trim` strips: U+00A0, U+FEFF, U+2028, U+2029, U+3000, U+1680, U+2000–U+200A
   - characters `trim` does not strip, which must survive: U+200B zero-width space, U+180E
   - interior whitespace kept intact (`" a  b "` → `"a  b"`)
   - non-whitespace edges unchanged, including emoji and combining marks
   - a string that is already "—" passes through unchanged
   Run these tests against the original code and confirm they pass.
2. Add a null test that asserts `formatLabel(null) === "\u2014"`. Using the escape in the test catches source-encoding drift and look-alike dashes. Run it against the original code and confirm it fails because the function throws.
3. Implement with an explicit null check, e.g. `value === null ? "—" : value.trim()`. Do not use a falsy check (`!value`), which would turn `""` into "—". Assumption to report: `undefined` is outside the declared type. Whatever the implementation does for `undefined`, state it in the report and do not widen the signature.
4. Red-team check (read-only): search callers of `formatLabel` for code that relies on the old throw, such as try/catch around it, or that already maps null to its own placeholder. Report each finding with its file:line. Do not edit callers.
5. Hand-mutation check, with no new tooling: temporarily make each of these changes and confirm at least one test fails for each, then revert:
   - the null branch returns "-"
   - the null branch returns "–"
   - the null branch returns ""
   - the null check is replaced with `!value`
   - `.trim()` is replaced with `.trimStart()`
   - `.trim()` is replaced with `.trimEnd()`

First checks: locate the helper's file and its existing test file. Identify the test runner and the TypeScript config, including whether `strictNullChecks` is on. If no test file exists, create one next to the helper, following the repo's existing test convention. If no test runner is available without adding a dependency, stop and report.

Judge:
- The null test fails on the original code and passes after the fix.
- Every characterization test passes both before and after the fix.
- The existing test suite stays green.
- The project's type check (e.g. `tsc --noEmit`) passes with the signature unchanged.
- Every hand mutation is caught by at least one test.
- The report lists the commands run, their red/green results, the diff limited to the helper and its tests, the `undefined` behavior, and any caller findings.
```

- `depth`: characterization tests using `trim` as the oracle, written before the edit, prove "preserve current trimming" instead of assuming it. They also catch the main trap, a falsy check that turns `""` into "—". Scope is unchanged; only the test file grows.
- `depth`: the red→green null test plus hand-mutation checks show the tests can actually fail, without adding Stryker or any other dependency.
- `range`: Unicode/i18n practice adds the specific whitespace code points `trim` does and doesn't strip, and checks the dash by code point to rule out look-alikes and encoding drift.
- `range`: a read-only red-team pass over callers exposes code that depended on the throw. It has no edit scope, so it doesn't break the "no changes outside" rule.
- Skipped: `altitude`. Any higher rung, such as consistent missing-value display across callers or removing redundant guards, needs edits outside the helper, which the task explicitly forbids.
- Owner actions: confirm the intended behavior for `undefined` from untyped callers; decide what to do with any caller findings the red-team pass reports.
