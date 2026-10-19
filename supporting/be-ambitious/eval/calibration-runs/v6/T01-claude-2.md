```text
Fix `formatLabel` so it returns the literal em dash "—" for null instead of throwing, and keep every non-null result exactly as it is today.

Current code: function formatLabel(value: string | null) { return value.trim(); }

Requirements (all binding):
- For null, return the literal em dash "—" (U+2014). Do not use a hyphen "-", an en dash "–" (U+2013), or a horizontal bar "―" (U+2015).
- For every non-null string, preserve the current trimming exactly. `String.prototype.trim` strips all ECMAScript whitespace and line terminators, which includes U+00A0, U+FEFF, U+2028, U+2029, U+3000 and the U+2000–U+200A spaces. Keep calling `value.trim()` on that path rather than reimplementing it. Empty and whitespace-only strings still return "", not "—".
- Keep the public signature: same name, export form, and parameter type `string | null`. The inferred return type stays `string`.
- No new dependencies. No changes outside this helper and its tests.
- Narrow with `value === null` exactly. Do not widen to `== null` or a falsy check, because that would change behavior for "" and for untyped callers passing undefined.

First checks:
- Locate the helper and its existing test file.
- Identify the project's existing test runner and typecheck command (for example, `tsc --noEmit`). Use only what is already installed.
- If no test file exists, create one next to the helper, following the project's naming convention.
- If there is no runner or typecheck command, say so, and treat those results as unverified rather than claiming them.

Method:
1. Characterization first. Before editing the helper, add table-driven tests for non-null inputs that pin today's outputs. Cover:
   - "", "   ", "a", "  a  ", "\t\n a \r\n"
   - "\u00A0a\u00A0", "\uFEFFa", "\u2028a\u2029", "\u3000a\u3000", "\u2003a\u2009"
   - "a  b", where internal whitespace is kept
   - "\u200Ba\u200B", where the zero-width space is NOT trimmed
   - a non-BMP string such as "  😀  "
   - a combining-mark string such as " e\u0301 "

   Run them against the unmodified function. They must pass, which proves they describe current behavior.
2. Add a null test that asserts the result is "—" and that `result.codePointAt(0) === 0x2014 && result.length === 1`. Run it and confirm it fails (throws) on the current code.
3. Apply the minimal fix, then rerun the full suite and the typecheck.
4. Read-only call-site audit. Search the repo for callers of `formatLabel` that relied on the throw:
   - a try/catch around the call
   - tests elsewhere that expect an error
   - code that checks for an empty string after calling it

   List each one with `file:line` in your report. Do not modify any of them, since that is outside the approved scope.

Judge: the characterization tests pass on both the old and the new code. The null test fails before the fix and passes after. The project's typecheck reports no new errors. Report the commands run with their outputs, and the call-site audit findings (or "none found").
```

- `depth`: characterization tests pinned on the unmodified code turn "preserve current trimming" from an intention into a checked property. They cover the Unicode whitespace that `trim` actually strips, plus near-misses like U+200B that it doesn't.
- `depth`: red/green null test with a code-point assertion. This catches the common substitution of a hyphen or en dash for the em dash. Scope is unchanged and there are no new dependencies.
- `depth`: pins `=== null` over `== null` and falsy checks, so "" and untyped `undefined` behave exactly as before.
- `range` (red-team / legacy-code practice): a read-only audit for callers that depended on the throw. It exposes behavior-change risk without editing outside the helper. Cost is one repo search.
- Skipped: `altitude`. Every higher rung, such as hardening other null-unsafe helpers or updating callers, needs changes outside this helper, which you prohibited.
- Owner actions: confirm the test runner and typecheck command exist. Decide what to do about any callers the audit reports.
