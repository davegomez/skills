```text
Fix formatLabel in TypeScript. Today it is:
  function formatLabel(value: string | null) { return value.trim(); }
It throws for null.

Requirements (all must hold):
- For null, return the literal em dash "—" (U+2014). Do not use a hyphen or an en dash.
- For every non-null string, return exactly what value.trim() returns today. This includes "" for empty and whitespace-only strings.
- Keep the public signature: same name, same parameter type (string | null), same string return type, same export form.
- Add no new dependencies. Change nothing outside this helper and its tests.

First checks:
- Find the helper, its existing tests, the test runner, and the typecheck command already in the repo. If there is no test runner, use only built-in tooling (e.g. node:test or plain assertions under the existing TS setup) and say so. If none of that runs, report it and do not install anything.
- Read every call site of formatLabel without editing any. Report any caller that relies on the current throw, such as a try/catch around it, or that checks the result against "" or another placeholder. Report them only; changing callers is out of scope unless I approve it.

Method:
1. Write characterization tests before touching the code. They pin today's trim behavior for non-null input: "", "   ", "a", "  a  ", "\t\n a \r\n", internal whitespace kept ("a  b"), and the full ECMAScript trim whitespace set (U+00A0, U+FEFF, U+1680, U+2000–U+200A, U+2028, U+2029, U+202F, U+205F, U+3000). Also include characters trim does NOT strip (U+200B zero-width space, U+180E) and a non-BMP string ("  😀  "). For each case, assert the result equals input.trim(). These tests must pass on the unchanged code.
2. Write a null test that asserts the result is "—" and that its code point is 0x2014. It must fail on the unchanged code.
3. Make the smallest fix that passes both: an explicit null check, then value.trim(). Do not use value?.trim() || "—". That maps whitespace-only strings to "—" and breaks the preservation requirement.
4. Mutation check, applied temporarily and then reverted: run the suite against these wrong versions and confirm each one fails at least one test.
   (a) value?.trim() || "—"
   (b) returning "-" or "–" for null
   (c) value.trimStart() for non-null
   Report which test caught each one.
5. Run the repo's typecheck in its existing strict settings and confirm the signature is unchanged.

Assumptions (inferred, not stated by owner): undefined is outside the contract, so its runtime behavior is left as is (it still throws). The em dash is for display, so no localization is needed.

Judge, with pass condition:
- The null test fails before the fix and passes after. Show both runs.
- All characterization tests pass both before and after.
- Each of the 3 mutants is caught by at least one test.
- The typecheck passes, and the diff touches only the helper and its test file.
Report the commands run and their actual output. List the read-only caller findings separately as observations, not changes.
```

- `depth`: characterization tests written before the fix, over the full ECMAScript trim whitespace set. These turn "preserve current trimming for every non-null string" into evidence instead of an assertion. No scope change.
- `depth`: the red-then-green null test checks the U+2014 code point, which catches lookalike dashes.
- `depth`: hand-made mutants, including the tempting `?.trim() || "—"`, test whether the suite actually guards the requirements. They are temporary and reverted, so there is no scope effect.
- `depth`: a read-only audit of call sites for code that depends on the throw. This exposes behavior-change risk without editing outside the helper. Any caller changes need owner approval.
- Skipped: `altitude`, because the owner explicitly confined changes to the helper and its tests, and a narrow fix has no higher rung worth climbing. `range`, because this is a narrow fix with one right answer and no other field's method adds anything.
- Owner actions: confirm that undefined staying out of the contract is acceptable. Decide whether any callers flagged by the audit should be changed in separate work.
