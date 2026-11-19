# I02 rubric for the blind reviewer

Only checks that `hidden/grade.sh` cannot settle. Grade each check `pass`, `fail`, `na`, or `unverified`, with a file and line or a test result as evidence.

| Check id | Priority | Severity | Pass condition |
| --- | --- | --- | --- |
| I02-R-exact-money | reliability | critical | Amounts are computed in exact units (integer cents or `Decimal`), not `Double` or `Float`, and the half-up rounding is explicit in code, not left to a formatter's default. |
| I02-R-tests-cover-rules | reliability | major | The new tests cover line totals, the subtotal, a tax value that lands on exactly half a cent, the total, the empty order, and a load failure. |
| I02-R-service-injected | maintainability | major | The feature reaches orders only through an injected protocol or client. Only the composition root picks the fake and reads `ORDER_SCENARIO`; feature and domain code do not read the process environment. |
| I02-R-rules-outside-views | maintainability | major | The amount rules live in UI-free code (no SwiftUI or UIKit import), not in view bodies or view models. |
| I02-R-error-not-swallowed | reliability | major | A load failure becomes the error state; it is not discarded (`try?`, empty `catch`) or shown as an empty order. Cancellation is not shown as an error. |
| I02-R-retry-safe | reliability | minor | "Try again" cannot start overlapping loads that leave an older result on screen. |
| I02-R-voiceover-lines | accessibility | minor | VoiceOver reads each order line as 1 element with name, quantity, and amount, and each total with its title. |
| I02-R-dynamic-type | accessibility | minor | Amounts and names do not clip or truncate at the largest accessibility text size; the layout reflows. |
| I02-R-currency-format | maintainability | minor | Amounts use a currency format style with code USD, not string concatenation of "$". User-visible strings are localizable. |
| I02-R-scope | maintainability | minor | Only the new feature and the wiring it needs changed; no unrelated edits to the shell, project settings, or other features. |
