```text
Fix the TypeScript helper `function formatLabel(value: string | null) { return value.trim(); }`, which throws for null.

Requirements (all binding):
- Return the literal em dash "—" (U+2014) for null.
- Preserve the current trimming for every non-null string, including "" and whitespace-only strings, which must still return "" and not "—".
- Keep the public signature `formatLabel(value: string | null)` and its inferred `string` return type.
- No new dependencies. No changes outside this helper and its tests.

First checks, before editing:
- Locate the helper and its existing test file.
- Identify the project's existing test runner and type checker.
- If there is no test runner, or the tests cannot run without a new dependency, stop and report that. Do not add one.

Method:
- Branch on `value === null` only. A falsy check (`!value`, `value || "—"`) would turn "" into "—" and break the trimming requirement.
- Assumption: runtime `undefined` from untyped callers is out of scope. Leave its current behavior unchanged and do not widen the signature.
- Characterization test: before editing, copy the original body into the test file as a reference oracle (`const original = (v: string) => v.trim()`). Assert that `formatLabel(s) === original(s)` across a table-driven corpus with no new libraries. The corpus covers:
  - ordinary strings, "", and internal whitespace (which must be kept)
  - every code point `String.prototype.trim` strips: tab, LF, VT, FF, CR, space, U+00A0, U+1680, U+2000–U+200A, U+2028, U+2029, U+202F, U+205F, U+3000, U+FEFF
  - near-misses trim must NOT strip: U+200B, U+180E, U+2060
  - each of these leading only, trailing only, both, and whitespace-only
  - surrogate-pair and combining-mark strings
- Null test: assert `formatLabel(null) === "\u2014"` by escaped code point, so an en dash, hyphen, or wrong normalization fails.
- Red/green: run the null test against the original function and confirm it fails (throws). Then apply the fix and confirm it passes.
- Hand-made mutant check, with no tooling added: temporarily change the guard to `!value`, then to `value == null`. Confirm the suite fails for `!value` (the "" case) and record the result for `== null`. Revert both.

Judge: the project's existing test runner shows the null test red before the fix and green after. The characterization corpus passes against the fixed function. The `!value` mutant makes the suite fail. The existing type checker reports no errors, and the exported signature is unchanged. The diff touches only the helper and its test file. Pass only if all of these hold. Report each result with the command output.
```

- `depth`: a characterization test uses the original `trim()` as the oracle over the full ECMAScript whitespace set and its near-misses. This turns "preserve current trimming" from an assumption into checked evidence. No scope or dependency effect.
- `depth`: the null branch is checked by escaped code point, which catches a look-alike dash that a visual review would miss.
- `depth`: the red/green run and the hand-made `!value` mutant show the suite actually guards against the most likely regression (empty string becoming "—"). There is no tooling cost, and the mutant is reverted afterward.
- `depth`: the `undefined` behavior is stated as an explicit assumption rather than silently changed, which protects the "keep the public signature" requirement.
- Skipped: `altitude`, because the owner limited changes to this helper and its tests, so a caller audit or downstream rollout would add scope without a need the task shows. `range`, because no other field's method beats differential and characterization testing for a one-line pure function.
- Owner actions: confirm the existing test runner can run without new dependencies, and confirm that leaving runtime `undefined` behavior unchanged is intended.
