# I01 rubric for the blind reviewer

Only checks that `hidden/grade.sh` cannot settle. Grade each check `pass`, `fail`, `na`, or `unverified`, with a file and line or a test result as evidence.

| Check id | Priority | Severity | Pass condition |
| --- | --- | --- | --- |
| I01-R-tests-cover-rules | reliability | major | The result's own tests exercise the packing-list rules: adding a valid name, rejecting an empty or blank name, toggling packed both ways, and reading back saved state. Tests that came unchanged from a generator, or that test only boilerplate, do not count. |
| I01-R-errors-reach-user | reliability | major | A failed load or save is not discarded (no bare `try?` or empty `catch` on the save or load path). The user sees a message, or the failure goes to a diagnostics seam, and the app keeps the in-memory list. |
| I01-R-save-order | reliability | minor | Two quick edits cannot leave an older list on disk than the list on screen: saves are serialized, or each save writes the latest state. |
| I01-R-rules-outside-views | maintainability | minor | The rules for adding and toggling items live in UI-free code (no SwiftUI or UIKit import), not in view bodies. |
| I01-R-storage-protection | security | minor | The list is written atomically with a Data Protection class, and not to `UserDefaults` as a large blob. |
| I01-R-privacy-manifest-complete | security | minor | The privacy manifest declares tracking as false and lists a reason for each required-reason API the code uses (for example `UserDefaults` or file timestamps), and lists none it does not use. |
| I01-R-state-not-color-only | accessibility | major | The packed state shows by more than color (a symbol shape or text), and VoiceOver reads the state as the value, not as an extra unlabelled image. |
| I01-R-dynamic-type | accessibility | minor | Text uses text styles, not fixed point sizes, and rows do not clip or truncate item names at the largest accessibility text size. |
| I01-R-localizable-text | maintainability | minor | User-visible strings are localizable (a String Catalog or equivalent), not concatenated in code. |
| I01-R-scope | maintainability | minor | No network access, permission prompts, third-party dependencies, or features the task did not ask for. |
