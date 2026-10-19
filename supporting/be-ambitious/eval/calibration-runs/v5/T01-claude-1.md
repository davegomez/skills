```text
Fix formatLabel so it no longer throws for null, without changing anything it does for strings.

Current code: function formatLabel(value: string | null) { return value.trim(); }

Requirements (all fixed):
- For null, return the literal em dash "—" (U+2014 EM DASH, not U+2013 en dash or U+002D hyphen).
- For every non-null string, return exactly what value.trim() returns today. This includes "" → "", whitespace-only → "", and String.prototype.trim's full whitespace set (tab, LF, CR, VT, FF, space, NBSP U+00A0, U+1680, U+2000–U+200A, U+2028, U+2029, U+202F, U+205F, U+3000, BOM U+FEFF). Do not normalize, collapse inner whitespace, or map empty strings to "—".
- Keep the public signature: same name, export form, parameter name, and parameter type (string | null). Do not widen or narrow the parameter type, and do not change the inferred return type from string.
- No new dependencies. Do not change anything outside this helper and its tests.

Assumption: the goal is safe display of a missing value with zero behavioral drift for present values. Use a strict `value === null` check, so the runtime behavior for untyped callers that pass undefined stays as it is today. If you find evidence that undefined should also map to "—", report it as a question. Do not change it.

Method:
1. Find the helper, its existing tests, the test runner, and the tsconfig. Before you edit anything, check whether a property-testing library such as fast-check is already a dependency. Name any missing piece and continue with what exists.
2. Characterize before you change. Add a test that calls formatLabel(null) and expect it to fail on the current code (red). Add characterization tests that pin current trimming on the cases listed above, plus a mixed leading/trailing case, inner whitespace that must survive, surrogate pairs and emoji, a lone surrogate, and combining marks at the edges. These tests should pass on the current code.
3. Write a differential equivalence test. Run formatLabel against the reference `(s: string) => s.trim()` on:
   - every BMP code point as a 1-character string, and wrapped in the string "a…a" (inner position);
   - a seeded generated set of at least 10,000 strings built from the whitespace set plus ASCII and astral characters.
   If fast-check is already installed, use it. Otherwise use a small seeded PRNG inside the test file. Assert exact string equality (===) on every case.
4. Make the minimal fix: return "—" when value === null, otherwise value.trim(). In the test, assert the null result by code point ("\u2014" and charCodeAt(0) === 0x2014) so an encoding or lookalike-character mistake fails visibly.
5. Red-team the tests by hand-mutating the implementation and running the tests against each mutant. Revert every mutant afterward. Mutants:
   - (a) `== null` in place of `=== null`, checked with an untyped undefined call that documents current behavior;
   - (b) trimStart only;
   - (c) trimEnd only;
   - (d) returning "-" or "–" for null;
   - (e) `value?.trim() ?? "—"` without the explicit branch;
   - (f) mapping "" to "—".
   Each mutant that changes behavior must turn at least one test red. If one survives, add the missing test.
6. Run the type checker on the project's existing config.

Report: the diff, the test output before and after the fix, the mutant table (mutant → killed or survived, with the killing test), and the type-check result.

Judge: the null test goes red before the fix and green after. All characterization and differential tests pass both before and after the fix, which proves non-null output is unchanged. Every behavior-changing mutant is killed. tsc reports no new errors. The diff touches only the helper file and its test file, and adds no dependencies.
```

- `depth`: characterization tests written before the edit, plus a differential test against `s.trim()` over every BMP code point and seeded random strings. This turns "preserve current trimming" from an assumption into a checked equivalence. Cost: one larger test file, no new dependencies.
- `depth`: a strict `=== null` check keeps runtime behavior for untyped `undefined` callers unchanged and avoids silent drift. Any change there is surfaced as a question, not made.
- `range` (software QA, mutation testing done by hand without Stryker): seeded mutants show the tests actually catch the plausible wrong fixes (`== null`, one-sided trim, wrong dash, `"" → "—"`). Cost: a few minutes. Every mutant is reverted, so scope is unchanged.
- `range` (typography/Unicode): asserting U+2014 by code point catches en-dash, hyphen, and encoding mistakes that a visual check would miss.
- Skipped: `altitude`. The owner limited changes to this helper and its tests, and the next rungs (fixing callers that work around null, standardizing empty-value display) would need edits outside that boundary.
- Owner actions: confirm whether `undefined` should keep its current runtime behavior (the prompt assumes yes), and confirm the helper's test file location and test runner if they are non-standard.
