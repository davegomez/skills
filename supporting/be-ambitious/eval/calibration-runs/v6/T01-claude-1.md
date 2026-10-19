```text
Fix formatLabel so it returns the literal em dash "—" (U+2014) for null instead of throwing, and returns exactly value.trim() for every non-null string.

Current code: function formatLabel(value: string | null) { return value.trim(); }

Requirements (unchanged from the owner):
- Return the literal em dash "—" for null.
- Preserve current trimming for every non-null string.
- Keep the public signature: function formatLabel(value: string | null), with its current inferred string return type and current export form.
- No new dependencies.
- No changes outside this helper and its tests.

Method:
- Implement with a strict null check (value === null) followed by a call to the built-in String.prototype.trim. Do not reimplement trimming with a regex, because String.prototype.trim covers the full ECMAScript WhiteSpace and LineTerminator sets and a regex can drift from them.
- Assumption: only null gets the dash. undefined is outside the declared type, so it keeps its current behavior (it throws). Flag this in the summary as an owner decision; do not widen the check to == null.
- Assumption: whitespace-only strings such as "   " are non-null, so they still return "" and not "—".
- Make the em dash test check the code point, not just the visual glyph. Assert that the result has length 1 and charCodeAt(0) === 0x2014, so an en dash (U+2013), a hyphen, or a mis-encoded character fails.
- Add a differential test that uses s => s.trim() as the oracle. Run it over a hand-written table of non-null inputs and assert that formatLabel(s) === s.trim() for each one. Include:
  - "" and "   "
  - an already-trimmed string
  - inputs with leading or trailing \t \n \r \v \f
  - U+00A0 no-break space, U+FEFF BOM, U+2028 and U+2029, U+3000 ideographic space, and U+1680
  - U+200B zero-width space and U+180E, which trim does NOT remove and which must survive
  - interior whitespace, which must be kept
  - a string that is only "—"
  - surrogate pairs and emoji at the edges
  Use only the test framework and helpers the project already has.
- Add a compile-time signature check in the test file:
  const _sig: (value: string | null) => string = formatLabel;
  Type-check it with the project's existing tsc setup.
- Red-team the change before calling it done. Write one failing-first test for null and run it against the original code to confirm it goes red (TypeError). Then apply the fix.

With my approval only: run a read-only search of formatLabel's callers and list any whose behavior changes now that null no longer throws. For example, a try/catch that falls back to another label would now get "—". Report them in the summary and do not edit them.

First checks: locate the file that defines formatLabel and its existing test file, if one exists. Identify the project's test runner and type-check command. Confirm that strictNullChecks is enabled, or note that it isn't. If there is no test runner or no type-check command, name the gap and stop before adding tooling, because that would be a new dependency.

Judge:
1. The null test fails on the original implementation and passes on the fix.
2. Every differential-table case passes, with formatLabel(s) === s.trim().
3. The em dash assertion passes on its code point (length 1, charCodeAt(0) === 0x2014).
4. The project's type-check passes with the signature assertion in place.
5. The diff touches only the helper and its test file and adds no dependencies.

Report the red run, the green run, and the type-check output. Any check that could not be run stays marked unverified.
```

**Ledger**

- `depth`: The strict `=== null` check plus the built-in `trim` keeps trimming identical. A regex rewrite could silently change behavior on Unicode whitespace. No change in scope.
- `depth`: Asserting the code point catches an en dash, a hyphen, or an encoding mix-up that a glyph comparison would miss. No change in scope.
- `depth`: The red-then-green null test shows the fix actually addresses the reported throw. No change in scope.
- `depth`: The compile-time signature assertion turns "keep the public signature" into a mechanical check. It only touches the test file.
- `range` (differential testing): Using `s.trim()` as the oracle across an edge-case table turns "preserve current trimming for every non-null string" into evidence. It uses existing tooling only and adds no dependencies.
- `range` (Unicode/i18n): The input table covers characters trim does and does not strip (U+FEFF vs U+200B and U+180E). This is where a hand-rolled fix would diverge.
- `range` (red-team): A read-only audit of callers that relied on the throw, behind approval. It exposes behavior changes at call sites without editing them, so the scope fence holds.
- **Skipped:**
  - `altitude`: the owner restricted changes to the helper and its tests, so the higher rung (fixing how callers handle null labels) is out of scope. Only the read-only audit remains, and it is approval-gated.
  - Hard-target move: the task has no quantitative metric.
- **Owner actions:**
  - Decide whether `undefined` should also return "—" (the prompt keeps it throwing).
  - Approve or decline the read-only caller audit.
  - Confirm the test runner and type-check command exist; adding them would breach the no-new-dependencies rule.
