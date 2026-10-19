# Native UI Patterns: direct-observation catalog

This is the main entry point for a bounded catalog of native UI patterns observed on one **iOS 27.0 Simulator** and one **Android 17 Emulator**. The catalogs keep platform facts separate. A shared UX problem in the comparison does **not** mean that the observed presentations or components are equivalent.

A second capture set, taken on 2026-09-08, adds Settings screens only, from one signed-in physical iPhone 17 Pro on iOS 27.0 in Light appearance and one signed-in Pixel 10 in the dark theme; see the [2026-09-08 capture note](../research/notes/captures-2026-09-08.md).

## How to read the evidence

- **[Observed]** records something directly seen in the inspected state.
- **[Inferred]** records a bounded design interpretation of observed evidence.
- **[Unconfirmed]** records a state or behavior that was unavailable or not tested.
- Each pattern page links to at least one retained screenshot. Android also retains matching UI Automator dumps; iOS automation results are recorded in its observation log.
- **Applicability** is an **[Inferred]** field on a catalog entry. It has one of three values. `system control`: the appearance matches a standard platform component. `general idiom`: a list, card, header, or data convention used across applications. `settings idiom`: a convention seen mostly in Settings. The separate "Applications observed" field records provenance only; it is not a scope limit.
- Findings apply only to the named simulator/emulator, app versions, data, account, permission, and captured states. Start with [limitations](../research/limitations.md) before generalizing.

## Browse by platform and category

| Platform | Navigation and presentation | Forms and controls | Lists, content, and feedback | Interaction and accessibility | Observation record |
| --- | --- | --- | --- | --- | --- |
| iOS 27.0 Simulator | [Catalog](ios/navigation-and-presentation.md) | [Catalog](ios/forms-and-controls.md) | [Catalog](ios/lists-content-feedback.md) | [Catalog](ios/interactions-and-accessibility.md) | [Log](../research/notes/ios/direct-observation-log.md) · [error-feedback pass](../research/notes/ios/error-feedback-pass.md) · [app inventory](../research/notes/ios/application-inventory.md) |
| Android 17 Emulator | [Catalog](android/navigation-and-presentation.md) | [Catalog](android/forms-and-controls.md) | [Catalog](android/lists-content-feedback.md) | [Catalog](android/interactions-and-accessibility.md) | [Log](../research/notes/android/direct-observation-log.md) · [error-feedback pass](../research/notes/android/error-feedback-pass.md) · [app inventory](../research/notes/android/application-inventory.md) · [UI dumps](../research/notes/android/ui-dumps/) |

## Searchable pattern index

Search this table by **platform**, **category**, **UX problem**, **application**, or **pattern name**. Application-specific entries remain explicitly marked; their presence here does not promote them to platform-wide patterns.

| Platform | Category | UX problem | Applications observed | Pattern name |
| --- | --- | --- | --- | --- |
| iOS | Navigation | Preserve orientation in a hierarchy | Settings; Files; Shortcuts | [Large-title hierarchy](ios/navigation-and-presentation.md#large-title-hierarchy) |
| iOS | Primary navigation | Move among peer destinations | Files; Photos | [Floating bottom navigation dock](ios/navigation-and-presentation.md#floating-bottom-navigation-dock) |
| iOS | Presentation | Focus a creation or editing task | Calendar; Contacts | [Full-screen task surface](ios/navigation-and-presentation.md#full-screen-task-surface) |
| iOS | Forms | Scan and edit related values | Contacts; Calendar | [Grouped form rows](ios/forms-and-controls.md#grouped-form-rows) |
| iOS | Input control | Find content with text or dictation | Settings; Files; Messages; Shortcuts | [Search field with dictation affordance](ios/forms-and-controls.md#search-field-with-dictation-affordance) |
| iOS | Permission control | Make a protected-capability choice | Maps; Wallet; Calendar; Photos | [System permission alert](ios/forms-and-controls.md#system-permission-alert) |
| iOS | Editing control | Add or remove repeatable values | Contacts | [Add and remove rows — application-specific](ios/forms-and-controls.md#add-and-remove-rows-application-specific) |
| iOS | Form and composer feedback | Prevent an empty event or message from being committed | Calendar; Messages | [Content-gated commit control](ios/forms-and-controls.md#content-gated-commit-control) |
| iOS | Controls | Change a binary setting in place | Settings | [Switch row](ios/forms-and-controls.md#switch-row) |
| iOS | Value selection | Set a continuous value in place | Settings | [Inline slider row](ios/forms-and-controls.md#inline-slider-row) |
| iOS | Value selection | Choose between rendered previews | Settings | [Visual option picker](ios/forms-and-controls.md#visual-option-picker) |
| iOS | Forms and controls | Offer a command or an additive action as a text-only row | Settings | [Link-style action row](ios/forms-and-controls.md#link-style-action-row) |
| iOS | Forms and controls | Isolate an irreversible action and state its consequence | Settings | [Destructive action row](ios/forms-and-controls.md#destructive-action-row) |
| iOS | Lists | Scan people and conversations | Contacts; Messages | [Identity-led list row](ios/lists-content-feedback.md#identity-led-list-row) |
| iOS | Lists | Scan destinations by icon and read their current value | Settings | [Icon-led settings row](ios/lists-content-feedback.md#icon-led-settings-row) |
| iOS | Lists | Present read-only facts about one object | Settings | [Label/value information rows](ios/lists-content-feedback.md#labelvalue-information-rows) |
| iOS | Feedback | Explain an empty collection or zero-match result | Files; Shortcuts; Settings | [Centered empty state](ios/lists-content-feedback.md#centered-empty-state) |
| iOS | Onboarding and feedback | Introduce a feature before entry | Calendar; Photos; Reminders; Health | [Feature-introduction surface](ios/lists-content-feedback.md#feature-introduction-surface) |
| iOS | Media content | Scan a photo library visually | Photos | [Photo thumbnail grid — application-specific](ios/lists-content-feedback.md#photo-thumbnail-grid-application-specific) |
| iOS | Temporal content | Relate date, events, and current time | Calendar | [Time-grid day view — application-specific](ios/lists-content-feedback.md#time-grid-day-view-application-specific) |
| iOS | Selection | Enter and leave bulk-action mode | Shortcuts | [Explicit selection mode — application-specific](ios/interactions-and-accessibility.md#explicit-selection-mode-application-specific) |
| iOS | Menu | Expose infrequent destination actions | Files | [Anchored overflow menu — application-specific](ios/interactions-and-accessibility.md#anchored-overflow-menu-application-specific) |
| iOS | Keyboard and focus | Begin the primary text-entry task | Messages; Calendar | [Immediate keyboard focus](ios/interactions-and-accessibility.md#immediate-keyboard-focus) |
| iOS | Accessibility and automation | Give visible controls programmatic names | Settings; Contacts; Files; Shortcuts; Calendar; Photos; Reminders; Wallet | [Accessibility-labeled visible controls](ios/interactions-and-accessibility.md#accessibility-labeled-visible-controls) |
| Android | Primary navigation | Move among peer destinations | Clock; Phone; Maps; Contacts; Photos shell | [Bottom navigation with selected destination](android/navigation-and-presentation.md#bottom-navigation-with-selected-destination) |
| Android | Navigation and discovery | Find content or settings | Settings; Phone; Maps; Contacts; Chrome; Messages; Files | [Search-led top surface](android/navigation-and-presentation.md#search-led-top-surface) |
| Android | Secondary navigation | Expose infrequent actions with context retained | Chrome; Messages | [Contextual overlay menu](android/navigation-and-presentation.md#contextual-overlay-menu) |
| Android | Hierarchical navigation | Reach storage categories and roots | Files | [Navigation drawer — application-specific](android/navigation-and-presentation.md#navigation-drawer) |
| Android | Spatial presentation | Balance map and place content | Maps | [Draggable map content sheet — application-specific](android/navigation-and-presentation.md#draggable-map-content-sheet) |
| Android | Controls | Show and change an on/off value | Settings; Clock | [Trailing switch in a settings or list row](android/forms-and-controls.md#trailing-switch-in-a-settings-or-list-row) |
| Android | Filtering controls | Present labeled category or status controls | Phone; Maps; Files | [Labeled chip or compact filter control](android/forms-and-controls.md#labeled-chip-or-compact-filter-control) |
| Android | Forms and editing | Enter structured contact data | Contacts | [Structured create-contact form — application-specific](android/forms-and-controls.md#structured-create-contact-form) |
| Android | Forms and editing | Choose a recipient before composing | Messages | [Recipient-first composition form — application-specific](android/forms-and-controls.md#recipient-first-composition-form) |
| Android | Value selection | Choose a valid time without saving immediately | Clock | [Modal time picker — application-specific](android/forms-and-controls.md#modal-time-picker) |
| Android | Safe destructive confirmation | Avoid losing unsaved form edits | Contacts | [Unsaved-change confirmation — application-specific](android/forms-and-controls.md#unsaved-change-confirmation) |
| Android | Keyboard and focus | Search with a visible exit path | Settings; Messages | [Search focus mode with explicit exit](android/interactions-and-accessibility.md#search-focus-mode-with-explicit-exit) |
| Android | Accessibility semantics | Name icon-only controls programmatically | Settings; Messages; Clock; Maps; Phone | [Semantic labels for icon-only actions](android/interactions-and-accessibility.md#semantic-labels-for-icon-only-actions) |
| Android | Accessibility status | Publish selected and checked state | Maps; Clock; Settings | [Semantic selected and checked state](android/interactions-and-accessibility.md#semantic-selected-and-checked-state) |
| Android | Back navigation and cancellation | Leave transient UI without committing | Clock; Messages; Settings | [System Back as non-committing exit](android/interactions-and-accessibility.md#system-back-as-non-committing-exit) |
| Android | Gestures and transitions | Change map-sheet position while retaining context | Maps | [Drag gesture changes sheet position — application-specific](android/interactions-and-accessibility.md#drag-gesture-changes-sheet-position) |
| Android | Permission and security interaction | Decide whether to grant protected access | Contacts; Maps; YouTube Music | [Permission prompt boundary](android/interactions-and-accessibility.md#permission-prompt-boundary) |
| Android | Lists and content | Scan grouped settings or scheduled items | Settings; Clock | [Grouped card list](android/lists-content-feedback.md#grouped-card-list) |
| Android | Empty-state feedback | Explain absent content and offer a safe next step | Messages; Contacts; Files | [Illustrated empty state](android/lists-content-feedback.md#illustrated-empty-state) |
| Android | Search feedback | Explain a zero-match result and offer query recovery | Settings | [Query-specific no-results recovery — application-specific](android/lists-content-feedback.md#query-specific-no-results-recovery) |
| Android | Primary action feedback | Keep the main creation action reachable | Messages; Clock; Contacts | [Floating primary action](android/lists-content-feedback.md#floating-primary-action) |
| Android | Onboarding and blocked-state feedback | Explain sign-in or permission-dependent progression | Photos; Maps; Chrome; YouTube Music; Play Store; Drive | [Sign-in or permission primer](android/lists-content-feedback.md#sign-in-or-permission-primer) |
| Android | Status feedback | Distinguish current selections and unchecked/off values | Maps; Clock; Phone; Settings | [Visible selected and unchecked states](android/lists-content-feedback.md#visible-selected-and-unchecked-states) |

## Cross-platform view

The [observed-patterns comparison](comparison/observed-patterns.md) is organized by shared UX problem and links back to separate iOS and Android evidence. It does not claim component equivalence or behavior beyond the captured states.

## Research status and audit trail

- [Coverage: inspected, limited, and unavailable applications](../research/coverage.md)
- [Limitations and curator checks](../research/limitations.md)
- [Uncertain and untested findings](../research/uncertain-findings.md)
- [iOS screenshot assets](../../../skills/native-ui-patterns/assets/ios/)
- [Android screenshot assets](../../../skills/native-ui-patterns/assets/android/)
