# Research limitations and curator checks

## Direct-evidence policy

Only the local [iOS observation log](notes/ios/direct-observation-log.md), [iOS error-feedback pass](notes/ios/error-feedback-pass.md), [Android observation log](notes/android/direct-observation-log.md), [Android error-feedback pass](notes/android/error-feedback-pass.md), application inventories, retained screenshots, and Android UI dumps support this catalog. No web source or platform memory is evidence. **Observed**, **Inferred**, and **Unconfirmed** labels retain their meanings; summaries do not upgrade inferred, unconfirmed, or application-specific entries.

## Environment and application scope

- iOS evidence comes from one iPhone 17 Pro Simulator on iOS 27.0 build `24A5423a`, in Light appearance and Large content size at the end of inspection. Twelve of 23 requested apps were available and launched; 11 were absent. See [iOS inventory](notes/ios/application-inventory.md).
- Android evidence comes from one `pixel_a17` AVD on Android 17/API 37 without a signed-in Google account. Fourteen of 18 requested apps launched; four requested Google apps were absent. Several launched apps were account-, permission-, onboarding-, or empty-data-limited. See [Android inventory](notes/android/application-inventory.md) and [unavailable-app notes](notes/android/unavailable-apps.md).
- These are properties of the inspected images, versions, account state, permissions, and sample data—not claims about all iOS or Android devices.

The 2026-09-08 capture set is a separate environment. See the [2026-09-08 capture note](notes/captures-2026-09-08.md) for the full record.

- Its iOS evidence comes from one signed-in physical iPhone 17 Pro on iOS 27.0, in Light appearance. The build number and the content size setting are unknown.
- Its Android evidence comes from one signed-in physical Pixel 10 in the dark theme. The Android version, the build, and the capture order are unknown.
- Both platforms cover the Settings application only. No other application appears, no interaction was exercised, and both devices held populated account data.
- Solid black rounded boxes and one blurred photograph are redaction marks added on 2026-09-09; treat a box as a text value of the covered width; the marks do not establish text length, alignment inside the box, or color of the covered value.

## Screenshot and raw-evidence boundary

- The retained set contains 36 iOS screenshots and 57 Android screenshots. The Android run also retained 57 same-basename UI Automator XML dumps. Counts come from the inspection and error-feedback logs and were verified against the local files during curation.
- All 40 cataloged pattern sections link to at least one existing screenshot. Unavailable requested apps have no screenshot; [coverage](coverage.md) explicitly records why no screenshot was possible.
- No byte-identical screenshot files were found. Similar before/after states were retained when they support different interaction states, such as Files' closed/open menu, Shortcuts' normal/selection modes, and Maps' lower/expanded sheet.
- Screenshots establish settled visible states only. They do not establish animation timing, easing, gesture thresholds, spoken output, focus order, hit targets, or behavior not directly exercised.
- Android hierarchy attributes support only the cataloged semantic-name and selected/checked-state observations. XCTest label activation supports iOS programmatic discoverability, not a complete assistive-technology audit.
- The 2026-09-08 set is retained as 20 raw Android JPEG files under [`notes/android/captures-2026-09-08/`](notes/android/captures-2026-09-08/), plus a SHA256 record of all 64 originals in the [capture note](notes/captures-2026-09-08.md). Runtime imports happen per batch; a capture is evidence in the runtime only after its batch imports it.

## Missing interaction and content states

- Neither run exercised a purchase, sign-in, completed send, call, saved contact, saved event/reminder/alarm, created folder, route, upload/download, persistent deletion, or permission grant.
- [Observed] The iOS pass retained focused Settings search and safe pre-commit states in Calendar, Contacts, and Messages. [Unconfirmed] Submit-time validation, send/delivery failures, search failures, edge-swipe back, destructive confirmation, Dynamic Type variants, VoiceOver, contrast variants, and landscape behavior remain unavailable. The Safari label query failed and a coordinate attempt hung before capture.
- [Observed] The Android pass retained safe pre-commit attempts in Contacts, Messages, Clock, and Files plus Settings no-results recovery. [Unconfirmed] Save/OK/candidate-selection validation, delivery failures, folder-creation errors, selection mode on a populated list, persistent-item deletion confirmation, TalkBack, font scaling, contrast instrumentation, rotation, split screen, external-keyboard traversal, and measured transitions remain unavailable.
- [Unconfirmed] Account- and network-backed populated, loading, empty, and failure states were generally unavailable. Android Calendar's startup “Checking info…” capture is one observed setup state, not broad loading-pattern evidence. Query-specific zero results in Settings is application feedback, not a network or indexing failure.
- [Unconfirmed] Populated and empty counterparts were not both available for most applications, so the catalog does not infer missing variants.

## Classification and terminology audit

- Platform catalogs remain separate. The [cross-platform comparison](../docs/comparison/observed-patterns.md) aligns shared UX problems and explicitly preserves different presentations; it does not call the components equivalent.
- Overlapping entries were not deduplicated when they document different evidence layers: Android search surface versus focused-search interaction; Maps sheet presentation versus the drag that changes position; visible selection versus UI-hierarchy state; iOS full-screen task presentation versus grouped form structure.
- The iOS Settings no-results state remains a variation of the existing cross-application [centered empty state](../docs/ios/lists-content-feedback.md#centered-empty-state). Android's Settings-only [query-specific no-results recovery](../docs/android/lists-content-feedback.md#query-specific-no-results-recovery) remains distinct because its observed Tips & Support suggestion is not represented by the generic empty-state entry.
- Application-specific entries remain labeled as such in the catalogs and README index. A similar UX problem on the other platform does not make either entry platform-wide.
- The iOS [content-gated commit control](../docs/ios/forms-and-controls.md#content-gated-commit-control) documents directly observed pre-commit availability; it is not evidence of submit-time validation or a platform-wide error component. Silent retention or rejection in Android's safe input attempts was not promoted to an error-feedback pattern.
- Application-level zero-match and pre-commit feedback remain separate from system permission prompts and Contacts' unsaved-change confirmation. The confirmation warns about abandoning edits; it does not establish invalid-input feedback or persistent-item deletion protection.
- Clock alarm terminology in the curated catalog uses [“unchecked”](../docs/android/lists-content-feedback.md#visible-selected-and-unchecked-states), matching the retained hierarchy's `checked="false"`, `enabled="true"`, and `clickable="true"` attributes. The raw observation log remains unchanged as the original evidence record.
- The Android [sign-in or permission primer](../docs/android/lists-content-feedback.md#sign-in-or-permission-primer) intentionally groups several blocked/progression surfaces, but curated comparison text keeps account walls, in-app primers, and system permission dialogs distinct.

## Link and deliverable validation

- During error-pass curation, every local Markdown inline link and image target under the project was resolved from its source file; no broken local target was found, so no catalog link correction was required.
- Required entry points now resolve: [README](../docs/README.md), [comparison](../docs/comparison/observed-patterns.md), [coverage](coverage.md), this limitations record, and [uncertain findings](uncertain-findings.md).
- Directory links are intentionally used for screenshot collections and Android UI dumps. A Markdown renderer or static-site generator may choose a directory listing behavior; individual evidence links remain available in catalogs, inventories, and coverage.

## Generalization boundary

Design-guidance and purpose fields are explicitly **Inferred**. They are interpretations of the named evidence, not platform requirements. Recurrence across two or more inspected applications means only recurrence in this bounded sample. Anything not directly supported remains in [uncertain findings](uncertain-findings.md) or the untested boundaries above.

The Applicability line on a catalog entry is **Inferred** as well; it interprets appearance and recurrence, and platform documentation is not evidence for it. Provenance from Settings is not by itself a scope limit, so a Settings-only entry can still carry the value `system control` or `general idiom`.
