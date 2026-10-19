```text
Fix `formatLabel` in its existing file. It currently reads:
  function formatLabel(value: string | null) { return value.trim(); }
It throws for null. Make it return the literal em dash "—" (U+2014) for null, and keep the current trimming for every non-null string. Keep the public signature exactly: same name, one parameter typed `string | null`, inferred return type, no overloads, no new parameters. Add no dependencies. Change only this helper and its tests. Do not edit callers, configs, package.json, or the lockfile.

First checks (report each result before writing code):
- Find the test runner the project already uses (jest, vitest, node:test, or another) and the Node/TS versions it runs under. Use only what is installed.
- Check whether fast-check or another property-testing library is already a devDependency. Use it only if it is already there. Otherwise, write plain generated cases.
- Read every call site of formatLabel without changing any of them. List any caller that relies on the null throw: a try/catch around it, error-boundary behavior, or a test expecting a TypeError. List any caller that already guards null before calling. Report these callers. Do not modify them.

Implementation constraints:
- Use a strict `value === null` check. Leave `undefined` behavior unchanged from today: it throws at runtime and is outside the declared type. See the owner question in the ledger.
- Do not use `||`, `??`, or a truthiness check on the trimmed result. "" and whitespace-only strings must still return "", not "—".
- Write the dash in source as "\u2014" or as a verified U+2014 character. It must not be U+2013 (en dash), U+2015 (horizontal bar), U+2212 (minus), or "-".

Tests (in the helper's existing test file, or a new sibling test file if none exists):
1. Red/green: before changing the helper, add `formatLabel(null) === "\u2014"`. Run it, confirm it fails with the current TypeError, and record that output. Then implement the fix and confirm it passes. Also assert the result has length 1 and code point 0x2014.
2. Golden table with hand-written expected values (not computed with .trim()): "", " ", "\t\n", "a", " a ", "a b", "  a  b  ", "\u00A0a\u3000", "\uFEFFa", "\u2028a\u2029", "null", "—", " — ".
3. Characterization oracle: freeze the original implementation in the test as `const original = (s: string) => s.trim();`. Aim for zero divergences between formatLabel and `original` over every code point from U+0000 to U+10FFFF, including lone surrogates via String.fromCodePoint. Check each code point in five positions: alone, leading ("x"+"a"), trailing ("a"+"x"), interior ("a"+"x"+"a"), and wrapped in spaces. That is about 5.6M calls. Keep it to a few seconds of runtime; if it is slower, batch the checks instead of sampling. If one approach is too slow or flaky, try the next before reporting a miss.
4. Unicode cross-check: compare the runtime's trimmed set against the ECMAScript WhiteSpace + LineTerminator set: U+0009, 000A, 000B, 000C, 000D, 0020, 00A0, 1680, 2000–200A, 2028, 2029, 202F, 205F, 3000, FEFF. Assert that these lookalikes are NOT trimmed: U+0085 (NEL), U+180E, U+200B, U+200C, U+200D, U+2060. If the runtime disagrees with the spec table, keep matching the runtime, because the requirement is "preserve current trimming". Report the disagreement as a finding. Do not change behavior because of it.
5. Red-team mutants: apply each wrong implementation below by hand, run the suite, confirm at least one test fails, then revert:
   (a) `return value?.trim() || "—"`
   (b) `return (value ?? "—").trim()` (passes null but must be checked against the dash and every string case)
   (c) `if (value == null) return "—"` (changes undefined behavior)
   (d) `return value === null ? "—" : value` (no trim)
   (e) `.trimStart()` and (f) `.trimEnd()` in place of `.trim()`
   (g) `"–"` (U+2013) in place of "—"
   If any mutant survives, add a test that kills it. Note that (c) can only be killed by a runtime test that passes `undefined as any` and expects a throw; add that test only if the owner confirms undefined should keep throwing.

Judge and pass condition:
- The null test is red before the fix (TypeError output recorded) and green after.
- The golden table passes, and the full suite passes on the project's runner and supported Node version.
- The characterization check reports 0 divergences over all 1,114,112 code points × 5 positions. Report the count checked, the divergence count, and the runtime. Report spec-table disagreements, if any, separately.
- Every listed mutant is killed. Report mutant → killing test, or "survived".
- `tsc --noEmit` passes. If the project emits declarations, formatLabel's emitted declaration is byte-identical to before.
- The diff touches only the helper file and its test file. package.json and the lockfile are unchanged.
- Report the caller audit: callers relying on the throw, and callers with redundant null guards. These are findings only; nothing outside the helper changes.
```

- `depth`: a red/green null test, a hand-written golden table, and a frozen-original oracle that checks every code point in five positions. Together they prove "preserve current trimming" rather than sampling it, and the stretch result is reported separately as a count. Cost: a few seconds of test runtime; no new dependencies.
- `depth`: a read-only audit of call sites for code that relies on the old throw. It shows where the fix changes observable behavior without touching anything outside the helper.
- `range`: borrows Unicode text engineering. It checks the ECMAScript whitespace table and lookalikes (NEL, U+180E, zero-width characters), and it asserts the dash by code point so U+2013, U+2015, and U+2212 can't slip in. This catches bugs that look correct on screen.
- `range`: borrows red-team mutation analysis, run by hand so no Stryker dependency is needed. It runs the tempting wrong fixes (`||`, `??`, `== null`, no trim, one-sided trim) and confirms the suite catches each one.
- Skipped: `altitude`. Every rung above the fix, such as cleaning up caller null guards or hardening sibling helpers, requires changes outside this helper, and the owner prohibited that.
- Owner actions: decide whether `undefined` should keep throwing (the prompt preserves it, but a test pinning it is added only on your confirmation). Confirm the test runner, and whether fast-check is already installed. Review the caller-audit findings, since any caller relying on the throw changes behavior with this fix.
