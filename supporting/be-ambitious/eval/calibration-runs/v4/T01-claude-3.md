```text
Fix formatLabel so it no longer throws for null:

  function formatLabel(value: string | null) { return value.trim(); }

Requirements (all mandatory):
- For null, return the literal em dash "—" (U+2014). Not an en dash (U+2013), hyphen, or minus.
- For every non-null string, return exactly what value.trim() returns today, including "" and whitespace-only inputs, which become "" and not the dash.
- Keep the public signature: name, the single parameter typed string | null, and the inferred string return type.
- No new dependencies. No changes outside this helper and its tests.

Method:
1. Write the tests first and run them against the original function. The null case must fail by throwing. The non-null cases must pass, because they record current behavior.
2. Check null with a strict equality test (value === null). Assumption: undefined is outside the declared type, so keep its current runtime behavior (it throws) and do not widen to == null. Record this choice in a test comment and in the report, without guessing at callers' intent.
3. Test the em dash by code point: assert result === "\u2014", result.length === 1 and result.codePointAt(0) === 0x2014. This avoids relying on a visual comparison.
4. Differential oracle: treat String.prototype.trim as the reference and assert formatLabel(s) === s.trim() for:
   - every BMP code point c, on its own and wrapped as c + "x" + c (65,536 cases, plain loops, no fast-check);
   - named edge cases: "", " ", "\t\n\r\v\f", "\u00A0", "\uFEFF", "\u2028", "\u2029", "\u3000", "\u200B" (zero-width space, which is not trimmed), interior whitespace "a  b", and a lone surrogate "\uD800".
5. Mutation check by hand (no tooling dependency): apply each mutation below to the fixed helper, confirm at least one test fails, then revert. Report each mutation as killed or survived.
   (a) "—" changed to "-"
   (b) "—" changed to "–"
   (c) .trim() removed
   (d) .trim() changed to .trimStart()
   (e) === null changed to !value, so "" would return the dash
   Strengthen the tests until all five are killed.
6. Read-only: list other helpers in the codebase that call .trim() or similar methods on a value typed string | null. Do not edit them.

With my approval only: fix any same-pattern helpers found in step 6.

First checks: find the helper's file and its existing test file, the test runner and its command, and whether tsconfig enables strictNullChecks. If there is no test runner, stop and report. Do not add one.

Judge and pass condition:
- The null test fails (throws) on the original and passes after the fix.
- All characterization and differential tests pass both before and after the fix, which shows non-null behavior is unchanged.
- tsc reports no new errors.
- All five mutations are killed.
- The diff touches only the helper and its tests.
Report the test command output and the mutation results. Any check that was not run stays unverified.
```

- `depth`: tests written first and run against the original show the null crash is real (red) and pin down current non-null behavior. The code-point assertion keeps a look-alike dash from passing. Scope and cost are unchanged.
- `depth`: the exhaustive differential oracle against `String.prototype.trim` covers all BMP code points without new dependencies. It shows "preserve current trimming" holds for every char, not just hand-picked samples, and also covers `""` and whitespace-only inputs that must not become the dash. The run cost is negligible.
- `depth`: the `=== null` choice, with undefined behavior left as is, is stated as an assumption so it doesn't silently change behavior for untyped JS callers.
- `range` (software-testing research, mutation analysis): five hand-applied mutations show the tests would actually catch a regression, with no Stryker dependency.
- `altitude`: the outcome goes from one fixed helper to a read-only inventory of helpers with the same null-trim crash. Fixing them needs approval because those changes would be outside the stated scope.
- Skipped: none.
- Owner actions: confirm the test runner exists and how to run it. Confirm that keeping undefined → throw is acceptable. Decide whether to approve fixes to same-pattern helpers.
