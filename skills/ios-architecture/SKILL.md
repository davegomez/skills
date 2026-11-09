---
name: ios-architecture
description: iOS app architecture. Use before writing, changing, or reviewing Swift, SwiftUI, UIKit, Xcode project, or Swift package code for an iOS app.
metadata:
  internal: true
---

# iOS app architecture

Every native iOS app is a SwiftUI-first, modular Swift Package workspace. This file holds the invariants every task needs. Each file in `references/` holds the rules for 1 concern.

## Invariants

- **Shell:** The app target is the composition root. It builds live services, registers features, and owns root navigation. It contains almost no other code.
- **Domain:** Each feature has a pure `XDomain` target. It holds value types and pure functions, conforms to `Sendable`, and imports no UI framework.
- **Presentation:** Each feature has an `XFeature` target. It holds SwiftUI views and `@Observable` models that call the domain and injected services.
- **Services:** Networking, persistence, authentication, purchases, analytics, feature flags, and diagnostics live behind protocols. Each protocol has a live implementation and a fake.
- **Concurrency:** Use Swift 6 language mode everywhere. Use `MainActor` default isolation in UI targets only. Keep domain targets `nonisolated`.
- **Quality gates:** Domain coverage of 90% or more, automated accessibility audits, published Accessibility Nutrition Labels, and a complete privacy manifest before every release.

The invariants apply to all app types: content, productivity, commerce, social, backend-driven, offline-first, health, and finance.

**Platform baseline:** Xcode 27 or later, Swift 6.4 or later, and the iOS 27 SDK or later. Xcode 27 runs only on Apple silicon Macs with macOS Tahoe 26.6 or later.

## Priority order

When 2 goals conflict, the higher priority wins.

1. **Security:** Protect user data, secrets, and the integrity of the app.
2. **Reliability:** Make behavior correct, deterministic, and testable.
3. **Accessibility:** Make every common task possible with assistive technologies.
4. **Maintainability:** Keep modules small, boundaries clear, and dependencies explicit.
5. **Performance:** Optimize only after you measure a problem.

Examples: Do not cache a token in `UserDefaults` to save a Keychain read. Do not draw a custom control in `Canvas` if it removes VoiceOver support.

## Process

1. **Gate.** Load this skill in every agent and subagent before it reads or edits iOS code. When you delegate iOS work, make this the first line of the subagent prompt: `Invoke the ios-architecture skill before you read or edit code.` The gate is complete when the skill is loaded in each context that edits code.
2. **Route.** List every concern the change touches, and match each to a row of the route table. The step is complete when each concern has a row or is marked _out of bounds_.
3. **Read.** Read each matched reference in full, and only the matched references.
4. **Apply.** Write or review the change against the rules of each matched reference. Change a default only when a _threshold_ in [deviations](references/deviations.md) applies, and name that threshold in the reply. A default change with no matching threshold is _out of bounds_.
5. **Out of bounds.** For each out-of-bounds concern, research the industry standard in primary sources: Apple developer documentation, the Human Interface Guidelines, Swift Evolution proposals, and WWDC sessions. Choose the pattern that keeps the invariants and follows the priority order. Write a short _decision record_ in the repository's decision record folder, for example `docs/adr/`. Record the problem, the pattern, the sources, and the priority the pattern serves. The step is complete when each out-of-bounds concern has a decision record with sources, named in the reply.
6. **Check.** Before you report done, check the diff against every rule of each matched reference. The work is complete when each rule is met, or the reply names the rule and why it does not apply.

## Route table

| The change touches | Read |
| --- | --- |
| A new project, build settings, `.xcconfig` files, signing, a new dependency, linting | [project setup](references/project-setup.md) |
| A feature, a package, domain or model code, dependency injection, the feature registry | [architecture](references/architecture.md) |
| SwiftUI or UIKit views, web content, custom drawing, the design system | [UI framework](references/ui-framework.md) |
| Routes, navigation stacks, deep links, universal links | [navigation](references/navigation.md) |
| HTTP calls, WebSockets, GraphQL, streams, offline display | [networking](references/networking.md) |
| Sign-in, tokens, accounts, biometrics | [authentication](references/authentication.md) |
| Stored data, schemas, migrations, caches, App Group data | [persistence](references/persistence.md) |
| Secrets, input across a trust boundary, logs, permissions, personal or regulated data, AI features | [security and privacy](references/security-privacy.md) |
| Async code, actors, `Sendable`, error handling, randomness, clocks, sync, crash reports | [concurrency](references/concurrency.md) |
| Scene phases, background tasks, push notifications, extensions, widgets, App Intents | [lifecycle and extensions](references/lifecycle-extensions.md) |
| Any view or control | [accessibility](references/accessibility.md) |
| Any text the user sees, dates, numbers, currency, measurements | [localization](references/localization.md) |
| Any code change | [testing](references/testing.md) |
| Launch time, scrolling, images, memory, performance budgets | [performance](references/performance.md) |
| Purchases, entitlements, analytics, feature flags | [purchases and seams](references/purchases-seams.md) |
| Versions, release builds, TestFlight, App Store submission | [release](references/release.md) |
| An existing app, legacy code, CocoaPods, Swift 5, UIKit screens, a port from another technology | [migration](references/migration.md) |
| A change to a default, a choice between patterns or stores | [deviations](references/deviations.md) |
| Screen layout, platform UI conventions, flow design | the `native-ui-patterns` skill |
