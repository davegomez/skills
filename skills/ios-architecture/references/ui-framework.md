# UI framework

Use SwiftUI as the default for all new screens. Use other frameworks only where SwiftUI has no equivalent.

- Use system SwiftUI controls first: `List`, `Form`, `Grid`, `LazyVGrid`, `NavigationStack`, and `NavigationSplitView`. They give you accessibility, Dynamic Type, and localization support with no extra work.
- Use the system design language and materials. Do not depend on compatibility keys that turn off the current system appearance.
- Use UIKit through `UIViewRepresentable`, `UIViewControllerRepresentable`, or `UIHostingController` when SwiftUI has no equivalent. Examples are advanced text editing, some camera flows, and legacy screens.
- Use the `UIScene` lifecycle in all UIKit code. Apps built with the current SDK fail to launch without it.
- Use `Canvas` and `TimelineView` for custom drawing and time-driven animation. Add `.drawingGroup()` only after you measure a rendering problem.
- Use RealityKit for 3D and spatial content.
- Use Metal directly only for custom GPU rendering or compute that no higher-level framework supports.

**Warning:** Content drawn in `Canvas` or Metal is not accessible by default. Before you choose a custom renderer, plan explicit accessibility elements, labels, values, and actions for the drawn content.

**Out of scope:** Cross-platform frameworks and engines are not part of a native architecture. They add a runtime, bypass native accessibility and Dynamic Type, and move platform updates outside your control. Choose them only through a separate product decision.

Follow the Human Interface Guidelines for layout, navigation, controls, and system behaviors.

**Web content**

- Use the SwiftUI `WebView` and `WebPage` types to show web content inside the app. Use `WKWebView` only through `UIViewRepresentable` when you need an API that `WebPage` does not have.
- Use `SFSafariViewController` or open the system browser for external pages that the app does not control.
- Use `ASWebAuthenticationSession` for sign-in, not an embedded web view (see [Authentication and identity](authentication.md)).
- Limit in-app navigation to an allowlist of HTTPS origins. Open all other links outside the app.
- Do not expose a JavaScript bridge to content that you do not control. Validate every message from the page as untrusted input.

**Design system package**

- Put shared components, typography, color tokens, spacing, and icons in a `DesignSystem` package.
- Build every component with its accessibility label, value, traits, and Dynamic Type behavior included.
- Define colors as asset catalog colors with light, dark, and increased-contrast variants.
- Provide a SwiftUI preview for each component at the largest accessibility text size.
