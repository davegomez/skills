```text
Fix formatLabel so it no longer throws for null:

  function formatLabel(value: string | null) { return value.trim(); }

Requirements (all binding):
- For null, return the literal em dash "—" (U+2014). Not an en dash (U+2013), a hyphen, or "--".
- For every non-null string, return exactly value.trim(). That includes the current results for edge cases: "" stays "", whitespace-only input becomes "", and trim's own set of Unicode whitespace is kept as is.
- Keep the public signature: the parameter stays `value: string | null`, and the return type stays `string`.
- No new dependencies. Change nothing outside this helper and its tests.
- Undefined is outside the spec. Use a strict `value === null` check. Do not widen to `== null` or `??`. Report what undefined does now; do not change it.

First checks (report any that fail, and continue only with what is available):
- Locate the helper, its existing tests, the test runner, and the TypeScript config. Confirm that `tsc --noEmit` (or the project's typecheck script) runs.
- Note whether a property-testing library (e.g. fast-check) or a mutation tool (e.g. Stryker) is ALREADY a dependency. Use one only if it is. Never add one.

Method:
1. Red first. Before you change the helper, add tests and run them against the current code:
   - The null test fails because it throws.
   - Assert `formatLabel(null) === "—"`, its length is 1, and `codePointAt(0) === 0x2014`. This catches dash look-alikes and encoding slips in the source file.
2. Differential test against the original as an oracle. In the test file, keep a copy of the old body as `reference = (s: string) => s.trim()` and assert `formatLabel(s) === reference(s)` for:
   - A fixed edge table:
     - "", " ", "\t\n\v\f\r", " a ", "a b"
     - Leading and trailing U+00A0, U+FEFF, U+1680, U+2000–U+200A, U+2028, U+2029, U+202F, U+205F, U+3000
     - Characters trim does NOT remove: U+200B, U+180E
     - Astral and combining characters: "😀", "e\u0301"
     - The string "null", and a lone "—"
   - Several thousand strings from a seeded generator written inline (a small PRNG, no library). Draw from that whitespace set plus ordinary and astral characters, and print the seed on failure.
   - If fast-check is already installed, use it for this property instead.
3. Fix the helper with the smallest change that passes. Then confirm all new and existing tests pass.
4. Type check. Add a compile-time assertion that `formatLabel(null)` and `formatLabel("x")` are `string`, using the project's existing type-test idiom or `const _: string = ...`. Run the typecheck.
5. Mutation check by hand (or with Stryker if it is already configured). Apply each mutant in turn, confirm at least one test fails, then revert:
   - (a) return "-" for null
   - (b) return "" for null
   - (c) drop .trim()
   - (d) return "—" for empty or whitespace-only strings
   - (e) use trimStart() or trimEnd() only
6. Read-only: list the call sites of formatLabel. Flag any that already guard null, catch the throw, or substitute their own placeholder. Do not edit them.

With my approval only: change any call site from step 6. That includes removing redundant null guards and unifying placeholders.
With my approval only: change undefined handling to also return "—".

Judge:
- The new null tests fail on the original code and pass after the fix.
- The differential test passes on the edge table and on the seeded run (report the seed and count).
- Every mutant in step 5 is killed (list each one with the test that caught it).
- The typecheck passes.
- All pre-existing tests pass.
- The diff touches only the helper and its test file(s).
Report each item as pass or fail with command output. Report the call-site list and the current undefined behavior as findings, not as changes.
```

- `depth`: Red-then-green null tests check for code point U+2014, not just a string that looks right. Benefit: they catch en-dash and encoding mistakes. No scope effect.
- `depth`: A differential test against the original `trim()` as an oracle, over a Unicode-whitespace edge table plus seeded random strings. Benefit: it tests "preserve current trimming for every non-null string" directly instead of by spot checks. No new dependency; it uses an inline PRNG.
- `depth`: A hand mutation check (five named mutants). Benefit: it shows the tests can tell a correct fix from plausible wrong ones, especially "—" leaking into whitespace-only input. No new dependency.
- `depth`: A compile-time return-type assertion plus the typecheck. Benefit: "keep the public signature" becomes a checkable claim.
- `range`: Differential testing from compiler and fuzzing practice, mutation analysis from test-adequacy research, and i18n handling of Unicode whitespace and dash look-alikes. Each exposes a failure that a single null test would miss.
- `altitude`: The original outcome is "no throw on null". The improved outcome adds a read-only list of call sites that already guard null or substitute their own placeholder, so you can decide on cleanup. Edits stay behind approval, and there is no scope change.
- Strict `=== null` and reporting undefined behavior keep the fix inside the spec. Widening it is behind approval.
- Skipped: a hard stretch target. For a one-line helper, the mutation and differential checks are already past what the stated bar requires.
- Owner actions: confirm the test runner and typecheck command. Decide whether to approve call-site cleanup and undefined handling.
