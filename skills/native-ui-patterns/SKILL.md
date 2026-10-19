---
name: native-ui-patterns
description: Native UI patterns. Use when designing iOS or Android screens, reviewing platform fit, or adapting a flow between platforms.
metadata:
  internal: true
---

# Native UI patterns

## Process

1. Establish the target platform and version, then name the UX problem rather than a component. This step is complete when both are explicit; record an unknown version as a gap.
2. Select the operation row below and read only the matching platform file. For cross-platform work, read the matching operation file in each platform column; combine rows only when the request spans operations. Selection is complete when each supported operation has one matching reference and each unsupported operation is an explicit gap.
3. Decide whether appearance is in scope. For text-only behavioral requests, skip screenshots. Before implementing or reviewing visual appearance, open the matched screenshots. In the operation file, choose the exact visual question and open only its named state or explicit comparison pair. A matching state capture itself counts as the overview; open extra surrounding, entry, return, or reset context only when the task requests it or it is necessary to interpret the state. Inspect and record layout, alignment, spacing, control placement, and surrounding content before writing code or a visual review. If no matched capture exists, state the visual-evidence gap instead of inventing a specification.
4. Apply or review the guidance while separating captured source from product adaptation. Treat recommendations as options, not platform mandates, and keep single-app examples application-specific unless the entry's Applicability line names a system control or a general idiom. Use the target viewport and framework to validate the translation; do not blindly copy pixels. This step is complete when each material choice names its source and adaptation.
5. Check the states relevant to the flow—resting, focused, empty, selected, disabled, permission-deferred, cancel, and error as applicable—and record gaps. Verify API or SDK mapping against the target project and current platform documentation rather than deriving it from captures. The work is complete when applicable states are addressed or listed as gaps.

## Route by operation

| Operation | iOS | Android |
| --- | --- | --- |
| Hierarchy, peer navigation, menus, sheets | [iOS navigation](references/ios/navigation.md) | [Android navigation](references/android/navigation.md) |
| Search entry, focus, results, no results, clear/reset, Back/exit | [iOS search](references/ios/search.md) | [Android search](references/android/search.md) |
| Forms, editing, input, commit/cancel | [iOS editing](references/ios/editing.md) | [Android editing](references/android/editing.md) |
| Switches, filters, and value controls | [iOS editing](references/ios/editing.md) | [Android editing](references/android/editing.md) |
| Lists, selection, empty/content states, primary actions | [iOS content states](references/ios/content-states.md) | [Android content states](references/android/content-states.md) |
| Onboarding and protected capabilities | [iOS onboarding and permissions](references/ios/onboarding-permissions.md) | [Android onboarding and permissions](references/android/onboarding-permissions.md) |
| Focused accessibility review | [iOS accessibility](references/ios/accessibility.md) | [Android accessibility](references/android/accessibility.md) |

## Evidence boundary and capture metadata

- **Observed** = behavior or settled state directly captured. **Inferred** = bounded interpretation. **Unconfirmed** = unavailable or untested.
- Two capture sets. Original set: 36 iOS PNGs at 1206×2622 from one iPhone 17 Pro Simulator on iOS 27.0 build `24A5423a`, Light appearance and Large content size recorded at the end of inspection, not verified per frame; 57 Android PNGs at 1280×2856 from one Android 17/API 37 `pixel_a17` emulator with no signed-in Google account. 2026-09-08 set, Settings only: iOS PNGs at 1206×2622 from one signed-in physical iPhone 17 Pro on iOS 27.0 in Light appearance; Android PNGs at 1000×2244 converted from JPEG, from one signed-in Pixel 10 in the dark theme, Android version unknown. Black rounded boxes in that set are redaction marks over personal data, not interface elements.
- Dimensions above are PNG pixel dimensions measured from file headers. Capture scale, display density, safe-area/system-bar insets, and font metrics are unknown. Pixel measurements are estimates from a raster image, never iOS points, Android dp, or target-device dimensions. State geometry only after opening and measuring the capture, label it in pixels, and validate the translation in the target viewport/framework.
- A screenshot establishes visible settled appearance, not motion, gesture thresholds, focus order, spoken output, hit targets, or assistive-technology usability. Hierarchy/automation data establishes only limited programmatic exposure. Full screenshot availability does not broaden those claims.
