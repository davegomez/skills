```text
Fix the TypeScript helper `formatLabel(value: string | null)`, which currently is `return value.trim();` and throws for null. For null it must return the literal em dash "—" (U+2014). For every non-null string it must return exactly what `value.trim()` returns today. Keep the public signature `formatLabel(value: string | null)` and its inferred `string` return type. Add no new dependencies. Change nothing outside this helper and its tests.

Assumption: the goal is for callers to render a placeholder instead of crashing, with no other change in behavior. Test against the edge cases where a plausible fix silently changes non-null output.

First checks:
- Locate the helper and any existing test file for it.
- Confirm which test runner and type checker the project already uses. Use only those.
- If no test setup exists, name that gap and stop before adding tooling.

Method:
1. Read-only, change nothing: find every call site of `formatLabel`. Note any caller that relies on the throw (a try/catch around it, or an error path). Note any caller that may pass `undefined` at runtime, such as from JS, `any`, or an optional field. Report these findings. Keep the null check strict (`value === null`), so `undefined` behavior is unchanged and outside this task.
2. Write the tests before the fix, so they run red against the current code:
   - `formatLabel(null)` returns a string that equals "—". Also assert its length is 1 and its code point is 0x2014, so a hyphen, en dash, or "--" fails.
   - Equivalence table. For each input, `formatLabel(s)` equals `s.trim()`. Inputs:
     - `""`, which must stay `""` and not become "—"
     - whitespace-only `"   "`, `"\t\n"`, which must become `""` and not "—"
     - `"a"`, `"  a  "`, `"a  b"` (interior space kept)
     - NBSP `"\u00A0a\u00A0"`, BOM `"\uFEFFa"`, line/paragraph separators `"\u2028a\u2029"`, ideographic space `"\u3000a"`
     - a string with a surrogate pair or emoji at its edges
     - a long string
   - A small seeded loop with no library. It builds random strings from a pool of whitespace and non-whitespace code points and asserts `formatLabel(s) === s.trim()`.
3. Implement the smallest fix: return "—" when `value === null`, else `value.trim()`.
4. Red-team the tests with hand-made mutants, applied one at a time and then reverted. Each must make at least one test fail:
   - `value || "—"` (wrong for `""`)
   - `value?.trim() || "—"` (wrong for whitespace-only)
   - `value?.trim() ?? "-"` (wrong dash)
   - `(value ?? "").trim()` (null returns `""`)
   If a mutant survives, add the missing case. Leave no mutant in the final code.
5. Run the existing type checker to confirm the signature and callers still compile.

Judge:
- The new tests fail on the original code and pass on the fix.
- Every listed mutant is killed.
- The type check passes with the public signature unchanged.
- No files outside the helper and its tests are modified, and there are no new dependencies.
Report:
- the red and green test output
- the mutant list, each marked killed or survived
- the type-check result
- the read-only call-site findings
If the runner or type checker could not run, mark that result unverified.
```

- `depth`: the edge-case table, the U+2014 code-point check, and the seeded equivalence loop against `s.trim()` turn "preserve current trimming for every non-null string" into a tested property. This catches the two likely regressions, `""` and whitespace-only becoming "—". No dependencies, test files only.
- `range`: hand-made mutation analysis from software-testing research checks the tests themselves, without a mutation-testing tool. It costs a few minutes and nothing persists.
- `altitude`: the outcome moves from "the helper doesn't throw" to "callers get the placeholder and no caller depended on the throw." This is backed by a read-only call-site audit that edits nothing. `undefined` handling is reported, not changed.
- Skipped: a hard target. This isn't a quantitative request, and the judge (red/green tests plus killed mutants) is already binary.
- Owner actions:
  - Confirm the existing test runner and type checker, or accept a stop if none exists.
  - Decide separately whether runtime `undefined` should also map to "—". That would be a behavior change outside this task.
