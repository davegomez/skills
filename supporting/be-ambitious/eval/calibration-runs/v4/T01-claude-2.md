```text
Fix formatLabel so it no longer throws for null:

  function formatLabel(value: string | null) { return value.trim(); }

Requirements (all binding):
- Return the literal em dash "—" (U+2014) when value is null.
- Preserve current trimming for every non-null string: the result must equal value.trim() exactly, including "" for "" and for whitespace-only input. Do not map empty or whitespace-only strings to "—".
- Keep the public signature: name, parameter list, and parameter type `string | null`.
- No new dependencies. No changes outside this helper and its tests.

First checks, before editing:
- Locate the helper and its test file, the test runner and command, and the tsconfig (is `strict` / `strictNullChecks` on?). If no test runner is already installed, stop and report that rather than adding one.
- Record whether the return type is currently inferred or annotated, and keep the public signature unchanged either way.
- Read-only: search the codebase for formatLabel call sites. Change nothing outside the helper. Report any caller that catches the old null throw, passes `undefined` through `any`/JS, or compares the result to "". These are behavior changes callers may notice.

Method:
1. Write the null test first and watch it fail with the current TypeError. Then fix with the smallest change, e.g. `value === null ? "—" : value.trim()`. Use a strict null check, not a falsy check, so "" still trims to "".
2. Em dash identity: assert `formatLabel(null) === "\u2014"` and `formatLabel(null).length === 1`. This catches look-alikes that read the same in review: en dash U+2013, hyphen-minus U+002D, minus U+2212, horizontal bar U+2015.
3. Differential test against the original behavior. Use `s.trim()` as the oracle and assert `formatLabel(s) === s.trim()` over a hand-built table:
   - every ECMAScript WhiteSpace and LineTerminator code point (U+0009–000D, U+0020, U+00A0, U+1680, U+2000–200A, U+2028, U+2029, U+202F, U+205F, U+3000, U+FEFF) at the start, end, both ends, interior only, and alone;
   - non-trimmed look-alikes that must survive: U+200B zero-width space, U+180E;
   - "", a string of one space, mixed whitespace only, a lone surrogate "\uD800", an emoji with surrounding spaces, and the string "—" itself.
   Also add a small seeded loop that builds random strings from that alphabet plus ASCII letters, with no new dependencies, so the property is checked beyond the hand-picked cases.
4. Red-team the tests with hand mutation. Temporarily apply each mutant and confirm at least one test fails, then revert:
   (a) return "-" for null;
   (b) use `!value` instead of `=== null`;
   (c) use trimStart;
   (d) use trimEnd;
   (e) return value unchanged.
   Report which test killed each mutant. Leave no mutant in the code.
5. Run the TypeScript typecheck (the project's existing command, or `tsc --noEmit` if tsc is already installed). It must pass with no new errors and no `any` or non-null assertion in the helper.

Judge and pass condition:
- The null test goes red (TypeError) before the fix and green after.
- All em-dash identity and differential trim tests pass.
- All 5 hand mutants are killed, and the final code contains none of them.
- The typecheck is clean and the signature diff is empty.
- The diff touches only the helper and its test file.
Report the call-site findings as observations, unverified at runtime.
```

- `depth`: a differential test against `String.prototype.trim` across the full ECMAScript whitespace set proves the "preserve current trimming for every non-null string" requirement instead of sampling it. The `=== null` guard keeps `""` and whitespace-only inputs out of the em-dash branch. No scope or dependency change.
- `depth`: tests red before and green after, plus a typecheck, make the fix verifiable rather than asserted.
- `range`: from typography and Unicode, a code-point assertion catches dash look-alikes that pass visual review. From mutation testing, five hand mutants (no Stryker, so no new dependency) show the tests actually guard each requirement.
- `altitude`: the outcome moves from "no throw for null" to "no throw, and owners know which callers may notice the behavior change". This is done with a read-only caller search; no edits outside the helper.
- Skipped: none.
- Owner actions: confirm a test runner is already installed. Decide whether any reported caller (one catching the old throw, passing `undefined`, or comparing to `""`) needs follow-up work. That work is outside this task's scope.
