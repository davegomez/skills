```text
Fix the TypeScript helper `formatLabel`:

    function formatLabel(value: string | null) { return value.trim(); }

It throws for null. Required behavior:
- For null, return the literal em dash "—" (U+2014).
- For every non-null string, preserve the current trimming exactly (today's behavior is `value.trim()`).
- Keep the public signature: parameter `value: string | null`, return type `string`.
- No new dependencies. No changes outside this helper and its tests.

First checks (report each result before editing):
- Locate the file that defines `formatLabel` and its existing test file, if any. If no test file exists, create one next to the helper using the project's existing test runner and conventions. If you can't identify a runner, stop and report this instead of adding one.
- Confirm the test command runs on the unchanged code. This directory is not a git repo, so record the original function body verbatim before editing. It serves as the "before" state and the reference for differential tests.

Method:
1. Write tests before changing the helper:
   a. Null case: `formatLabel(null)` returns "—". Assert the exact code point (`"—".codePointAt(0) === 0x2014`) so a hyphen (U+002D) or en dash (U+2013) fails. This test must fail on the original code with a TypeError.
   b. Characterization tests on the original code. Check that `formatLabel(s) === s.trim()` for edge cases a careless null check would break:
      - "" must stay "" and must not become "—". This guards against `!value` / `value ?? …` / `value || …` style mistakes.
      - "   " becomes "".
      - "0" and "false" are kept as they are.
      - Leading, trailing, and interior whitespace: interior whitespace is kept.
      - Every code point that `String.prototype.trim` strips: U+0009–U+000D, U+0020, U+00A0, U+1680, U+2000–U+200A, U+2028, U+2029, U+202F, U+205F, U+3000, and U+FEFF.
      - A zero-width space (U+200B), which `trim` does NOT strip.
      - Strings that already contain "—".
      - Astral characters, e.g. an emoji with surrounding whitespace.
      These must pass both before and after the fix.
   c. Differential check without new dependencies: inline a copy of the original implementation in the test file as the reference. Run a deterministic, seeded loop of a few thousand generated strings built from the whitespace set above plus ordinary characters. Assert the new `formatLabel` matches the reference on all of them.
2. Fix with an explicit `value === null` check, return "—", otherwise `value.trim()`. Keep the return type `string`. Do not widen or narrow the parameter type.
3. Assumption (not a requirement): callers passing `undefined` at runtime are out of scope. Do not add handling for it. Mention it in the report only if you find evidence of such calls inside the helper's own file or tests.

Report: the before and after function bodies, the files touched (helper and its test file only), and test output from both runs.

Judge: the test suite run before the fix and after it.
Pass condition:
- Before the fix, the null test fails (TypeError) and every characterization test passes.
- After the fix, all tests pass, including the seeded differential loop, with the iteration count and seed reported.
- No dependency manifest or other file has changed.
```

**Ledger**
- `depth`: tests are written first and the null test goes red then green, which proves the fix addresses the reported throw.
- `depth`: characterization and differential tests against the original `trim()` show trimming is unchanged across all whitespace code points `trim` strips, plus near-misses like U+200B. They also catch the common `!value` bug that would turn `""` into "—". The tests stay in scope and need no dependencies.
- `depth`: the exact code-point assertion keeps the required literal "—" from being swapped for a hyphen or en dash.
- Skipped: `altitude`, because this is a narrow bug fix with no downstream decision to serve. `range`, because there is one right answer and no other field's method adds to it.
- Owner actions: none required. If the project has no test runner, the prompt stops and asks rather than adding one.
