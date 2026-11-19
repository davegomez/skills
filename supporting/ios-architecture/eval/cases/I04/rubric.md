# I04 rubric

Checks for the blind reviewer. The hidden checks already settle the build, the legacy totals, loading the old cache, the cache keys and bundle identifier, a truncated cache and repeated reloads, navigation, a linked local package, no UI import in the totals target, and 4 unchanged legacy files. Grade each check `pass`, `fail`, `na`, or `unverified`, with file and line evidence.

| Check | Priority | Severity | Pass condition |
| --- | --- | --- | --- |
| I04-R1-seam-injected | maintainability | major | The screen reaches loading and saving only through a protocol or an injected value, with the live implementation built outside the view controller. The view controller no longer calls `URLSession`, `FileManager`, or JSON coders directly. |
| I04-R2-totals-pure | maintainability | major | The totals logic is a pure function or value type in the package: no I/O, no formatting, no UI types, and `Sendable` where it crosses concurrency domains. |
| I04-R3-characterization-tests | reliability | major | The package has tests for the totals (the discount threshold, half-up rounding, and quantities of 0 or less) and for the cache (bytes in the old format, a truncated file, and a failed load that keeps the saved data). |
| I04-R4-error-policy | reliability | minor | A failed load or save neither crashes nor deletes the saved orders. Errors are not silently swallowed where the old code reported them. No new `try!` or force unwrap on loaded data. |
| I04-R5-load-ordering | reliability | minor | Overlapping loads cannot show an older result over a newer one, or the reviewer can show that they cannot overlap. UI updates run on the main actor. |
| I04-R6-incremental-scope | maintainability | minor | Only the Orders screen's totals and loading moved. Navigation, other screens, generated code, and the app's build settings are unchanged, except what linking the package needs. |
