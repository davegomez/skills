```text
Fix this TypeScript function: function formatLabel(value: string | null) { return value.trim(); }
It throws for null. Return the literal em dash "—" for null and preserve current trimming for every non-null string. Keep the public signature. No new dependencies and no changes outside this helper and its tests.

First checks, before editing:
- Locate the helper, its existing tests, and the project's existing test runner and command. Use only what is already installed. If no test setup exists, stop and report that, since adding one would mean new dependencies or changes outside this helper and its tests.
- Run the existing tests once and record the baseline result.

Write the tests first:
- Add a null case asserting the result is exactly "—". Also assert it is one character with code point U+2014, so an en dash (U+2013), a hyphen, or a mis-encoded source file fails the test.
- Run the suite and confirm the null case fails (red) on the current code.

Implement:
- Guard on strict `value === null` and return "—". Otherwise return `value.trim()` unchanged.
- Assumption: "preserve current trimming for every non-null string" means the output must equal `value.trim()` exactly for every string. So "" and whitespace-only strings return "", not "—".
- Assumption: runtime `undefined` is outside the request. It keeps its current behavior (it throws), so do not use `== null`, `??`, or optional chaining, because each of these would also map undefined to "—".
- Keep the public signature `formatLabel(value: string | null)` exactly. Do not add an explicit return type unless the current declaration has one.

Equivalence tests for non-null strings. These use no new dependencies:
- Table cases: "", " ", "\t\n", "  a  ", "a b", "—", " — ", and strings containing U+00A0, U+FEFF, U+2028, U+3000, U+200B, U+180E, and lone surrogates. For each case, assert `formatLabel(s) === s.trim()`. The engine's own `trim()` is the oracle. Do not hard-code expected outputs for Unicode whitespace.
- Differential test: a seeded, deterministic loop with a small inline PRNG in the test file. It generates at least 1,000 strings from an alphabet that is heavy in whitespace and edge characters, and asserts `formatLabel(s) === s.trim()` for each. On failure, print the seed and the input.

Mutation check (manual, not committed). Temporarily apply each mutant below, run the suite, confirm at least one test fails, then revert:
  (a) `if (!value) return "—"`
  (b) `return value?.trim() || "—"`
  (c) returning "-" or "–" for null
  (d) `value.trimStart()` in place of `value.trim()`
Mutants that `undefined` would distinguish (`== null`, `??`) are not required to fail, because undefined is outside the signature. Note them as equivalent under the type.

With my approval only: run a read-only search of formatLabel's call sites and list any callers that catch its exception or pre-guard null and so may depend on the old throwing behavior. Do not edit any call site.

Judge: the project's existing test runner. Pass only if all of the following hold:
- The new null test fails before the fix and passes after.
- Every table and differential case passes.
- Mutants (a) through (d) are each killed by at least one test.
- The full suite passes with no new failures against the recorded baseline.
- `git diff` (or an equivalent file comparison) shows changes only to the helper and its test file, with no lockfile or package.json changes.
Report each item as observed output. Any item that was not run is unverified.
```

- `depth`: the red-then-green null test and the U+2014 code-point assertion turn "it works" into evidence and catch a look-alike dash. No scope or cost effect.
- `depth`: the strict `=== null` guard plus explicit assumptions for `""`, whitespace-only strings, and `undefined` stop a plausible fix (`||`, `??`, `== null`) from changing behavior beyond what was asked.
- `range`: from compiler testing, differential testing against the engine's own `trim()` oracle, with a seeded inline generator, checks "every non-null string" without adding a property-testing dependency.
- `range`: from test-adequacy research, a manual mutation check acts as the red team for the tests themselves. It proves they would catch the likely wrong fixes. It adds a few minutes and nothing is committed.
- `altitude`: the original outcome is a helper that no longer throws. The improved outcome also tells the owner which callers might depend on the old throw. This is a read-only addition behind approval because the task doesn't permit a companion report.
- Skipped: none.
- Owner actions: confirm that a test runner exists in the project; decide whether `undefined` should keep throwing (the assumption here) or also return "—"; approve or decline the read-only call-site audit.
