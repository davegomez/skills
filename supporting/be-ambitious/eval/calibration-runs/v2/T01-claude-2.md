```text
Fix the TypeScript helper `formatLabel(value: string | null)`, which currently does `return value.trim();` and throws for null.

Required behavior (these are the owner's explicit requirements; do not change them):
- For null, return the literal em dash "—" (U+2014). It is not a hyphen "-" or an en dash "–".
- For every non-null string, preserve the current trimming exactly, meaning the result of `String.prototype.trim()`.
- Keep the public signature `formatLabel(value: string | null)`, including its name, parameter, and export form.
- Add no new dependencies.
- Change only this helper and its tests.

First checks (report each result before you edit):
1. Find the file that defines `formatLabel` and its existing test file, if one exists. Confirm the test runner and the typecheck command that are already in the project. Use only those.
2. Record the original function body and the original test file so you can show a before/after diff. The working directory may not be a git repository, so do not assume `git diff` is available.
3. If there is no test runner, or the helper is defined more than once, stop and report it. Do not add tooling.

Method:
- Write characterization tests first and run them against the ORIGINAL code. They should pass before any edit, which proves they capture current behavior. Cover:
  - plain strings
  - an empty string, which stays "" and does not become "—"
  - a whitespace-only string, which becomes "" and does not become "—"
  - internal whitespace, which is kept
  - leading and trailing whitespace, built from every code point ECMAScript `trim()` removes: the WhiteSpace set (TAB, VT, FF, SP, NBSP U+00A0, ZWNBSP U+FEFF, and Unicode Zs, including U+1680, U+2000–U+200A, U+202F, U+205F, U+3000) and the LineTerminator set (LF, CR, U+2028, U+2029)
  - lookalikes that `trim()` does NOT remove, such as U+200B zero-width space and U+180E Mongolian vowel separator
  
  Aim for this exhaustive code-point table, driven from one array in the test, using only the existing test runner. If a code point behaves differently from what you expected, the original code's behavior is the truth. Record it; do not "fix" it.
- Write a null test that asserts the result is exactly "—" and checks its code point (`charCodeAt(0) === 0x2014`, length 1). Run it against the original code and confirm it fails because the original throws.
- Implement the fix with a strict `value === null` check, not `== null` and not a falsy check. This way the empty string and runtime `undefined` from untyped callers behave exactly as they did before, so nothing beyond null changes.
  - Assumption: no caller relies on `undefined` producing "—". Mention this in your report; do not act on it.

Judge and pass condition:
- The characterization tests pass on the original code AND on the fixed code (preservation proven).
- The null test fails on the original code (it throws) and passes on the fixed code (red, then green).
- The project's existing typecheck passes with the signature unchanged.
- The before/after diff touches only the helper's file and its test file, and adds no dependency or lockfile changes.

Report:
- the commands you ran
- the pass/fail output for each stage
- the final diff
- any code point whose behavior surprised you

Anything not run is reported as unverified.
```

- `depth`: Characterization tests run against the original code first. This turns "preserve current trimming" from a claim into evidence. No scope or dependency effect.
- `depth`: The test covers every whitespace and line-terminator code point from the ECMAScript spec, plus lookalikes that `trim()` does not remove. This catches a trim rewrite that silently drifts, such as switching to a regex. It costs one table-driven test.
- `depth`: The null test is red, then green, and checks the code point U+2014. This guards against substituting a hyphen or en dash.
- `depth`: The fix uses a strict `=== null` check. This keeps `""`, whitespace-only strings, and runtime `undefined` behaving as before. The `undefined` point is flagged as an assumption, not changed.
- `depth`: First checks confirm the existing runner and typecheck, and save the original code for the diff. This matters because the directory isn't a git repo. It adds no tooling.
- Skipped:
  - `altitude`: The owner scoped the work strictly to this helper and its tests, so there is no higher rung to climb without breaking that scope.
  - `range`: This is a narrow fix with one right answer, so no other field's method adds anything.
- Owner actions:
  - None required to run the prompt.
  - Optionally confirm whether any untyped caller passes `undefined`. If one does, it will still throw, as it does today.
