```text
Fix the TypeScript helper `formatLabel(value: string | null)`, which currently calls `value.trim()` and throws when `value` is null.

Requirements (all binding):
- For `null`, return the literal em dash "—" (U+2014), one character.
- For every non-null string, return exactly what `value.trim()` returns today. Whitespace-only strings still become "", not "—". Unicode whitespace is trimmed exactly as `String.prototype.trim` trims it.
- Keep the public signature: `formatLabel(value: string | null)` with a `string` result.
- No new dependencies. Change only this helper and its tests.

First checks:
- Locate the helper and its existing test file.
- Identify the test framework and type-checker the project already uses.
- If there is no test setup, stop and report this. Do not add a framework.

Method:
1. Write the null test first and run it. Confirm it fails with the current code.
2. Make the minimal fix. Use a strict `value === null` check, not `value == null`. Today `undefined` from untyped JS callers throws, and the fix should not silently change that. State this choice in a one-line code comment only if the surrounding code uses comments like that.
3. Differential test against the original behavior.
   - Keep a copy of the original body, `(v: string) => v.trim()`, inside the test file only, as the oracle.
   - Assert `formatLabel(s) === oracle(s)` for a corpus that includes:
     - "", " ", "\t\n", leading, trailing, and inner whitespace, and already-trimmed strings
     - every ECMAScript WhiteSpace and LineTerminator code point: U+0009–U+000D, U+0020, U+00A0, U+1680, U+2000–U+200A, U+2028, U+2029, U+202F, U+205F, U+3000, U+FEFF
     - U+180E and U+200B, which are not trimmed
     - a lone surrogate, an emoji, and a string that is the em dash itself
4. Assert the null result exactly:
   - `formatLabel(null) === "\u2014"`
   - its length is 1
   - its code point is 0x2014, which rules out the en dash U+2013, the hyphen-minus, and the horizontal bar U+2015
5. Manual mutation check, with no tooling added. Apply each mutant below, confirm at least one test fails, then revert:
   - swap `===` for `==`
   - drop `.trim()`
   - return "-" instead of "—"
   - map "" to "—"
   Report each mutant and the test that killed it.
6. Run the project's existing type-check. Confirm the exported signature is unchanged.

With my approval only: search the codebase and list, without changing, the call sites that guard against null before calling formatLabel or that throw on null. These are candidates for later cleanup.

Judge: the null test goes red before the fix and green after. The full differential corpus passes against the oracle. Every listed mutant is killed. The existing type-check passes with the signature unchanged.
Stretch, reported on its own line: the corpus covers 100% of the ECMAScript whitespace and line-terminator code points listed above, met or missed.
If the test runner or type-checker is unavailable, report those checks as unverified.
```

- `depth`: The differential test uses the original `trim` as its oracle and covers every ES whitespace code point. This turns "preserve current trimming" into something a test can check, not an assumption. Scope: test file only.
- `depth`: The fix uses `=== null` rather than `== null`, so the current behavior for `undefined` from JS callers stays as it is. This is an inferred risk, not something you stated.
- `depth`: Manual mutation testing checks that the tests can actually fail, without adding a tool like Stryker. Cost: a few minutes.
- `range`: A typography/Unicode check asserts code point 0x2014 and length 1. This guards against en dash or hyphen lookalikes from editors and file encoding.
- `altitude`: The original outcome is a helper that doesn't throw on null. The improved outcome also finds callers that work around the old bug. That search is read-only and sits behind approval, since it goes beyond the helper.
- Skipped: a hard target past the owner's bar beyond corpus coverage. The behavior is fully specified, so there is nothing to push further.
- Owner actions:
  - Confirm the project has a test runner and type-checker.
  - Approve or decline the call-site audit.
  - Confirm that keeping `undefined` throwing is intended.
