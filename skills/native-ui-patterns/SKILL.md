---
name: native-ui-patterns
description: Native UI patterns. Use when designing iOS or Android screens, reviewing platform fit, or adapting a flow between platforms.
metadata:
  internal: true
---

# Native UI patterns

## Process

1. Establish the target platform, version, and device class (iPhone or iPad), then name the UX problem rather than a component. This step is complete when each is explicit; record an unknown version as a gap.
2. Select the operation row below and read only the matching platform file. For cross-platform work, read the matching operation file in each platform column; combine rows only when the request spans operations. Selection is complete when each supported operation has one matching reference and each unsupported operation is an explicit gap.
3. Decide whether appearance is in scope. For text-only behavioral requests, skip screenshots. Before implementing or reviewing visual appearance, open the matched screenshots. A matching state capture itself counts as the overview; open extra surrounding, entry, return, or reset context only when the task requests it or it is necessary to interpret the state. Inspect and record layout, alignment, spacing, control placement, and surrounding content before writing code or a visual review. If no matched capture exists, state the visual-evidence gap instead of inventing a specification.
4. Apply or review the guidance while separating captured source from product adaptation. Treat recommendations as options, not platform mandates, and keep single-app examples application-specific; Kit evidence is system-wide. Use the target viewport and framework to validate the translation. This step is complete when each material choice names its source and adaptation.
5. Apply the operation file's review section and record gaps. Verify API or SDK mapping against the target project and current platform documentation rather than deriving it from captures. The work is complete when applicable states are addressed or listed as gaps.

## Route by operation

| Operation | iOS | Android |
| --- | --- | --- |
| Hierarchy, peer navigation, toolbars, sidebars, windows | [iOS navigation](references/ios/navigation.md) | [Android navigation](references/android/navigation.md) |
| Sheets, alerts, action and share sheets, menus, popovers | [iOS presentation](references/ios/presentation.md) | [Android navigation](references/android/navigation.md) |
| Search entry, focus, results, no results, clear/reset, Back/exit | [iOS search](references/ios/search.md) | [Android search](references/android/search.md) |
| Forms, editing, input, keyboards, commit/cancel | [iOS editing](references/ios/editing.md) | [Android editing](references/android/editing.md) |
| Buttons, switches, sliders, pickers, filters, value controls | [iOS controls](references/ios/controls.md) | [Android editing](references/android/editing.md) |
| Lists, selection, empty/content states, primary actions | [iOS content states](references/ios/content-states.md) | [Android content states](references/android/content-states.md) |
| Onboarding and protected capabilities | [iOS onboarding and permissions](references/ios/onboarding-permissions.md) | [Android onboarding and permissions](references/android/onboarding-permissions.md) |
| Focused accessibility review | [iOS accessibility](references/ios/accessibility.md) | [Android accessibility](references/android/accessibility.md) |
| Widgets, Lock Screen, notifications, Control Center, app icons, system bars | [iOS system surfaces](references/ios/system-surfaces.md) | Gap |
| Color, text styles, Dynamic Type, materials, Liquid Glass | [iOS foundations](references/ios/foundations.md) | Gap |

## Evidence boundary and capture metadata

- **Observed** = behavior or settled state directly captured. **Kit** = anatomy and variants from Apple's design kit: placeholder content, no behavior. **Inferred** = bounded interpretation. **Unconfirmed** = unavailable or untested.
- Kit set: Figma "iOS and iPadOS 27", exported 2026-10-28; kit images live in `assets/ios/kit/`.
- Captures: iOS from an iPhone 17 Pro on iOS 27.0 in Light appearance, Simulator without an account plus a signed-in device for Settings; Android from an Android 17 emulator without an account plus a signed-in Pixel 10 in the dark theme for Settings. Black rounded boxes in Settings captures are redaction marks over personal data, not interface elements.
- Capture scale, display density, safe-area/system-bar insets, and font metrics are unknown. Pixel measurements are estimates from a raster image, never iOS points, Android dp, or target-device dimensions. State geometry only after measuring the opened capture, labelled in pixels.
- A screenshot establishes visible settled appearance, not motion, gesture thresholds, focus order, spoken output, hit targets, or assistive-technology usability. Hierarchy/automation data establishes only limited programmatic exposure.
