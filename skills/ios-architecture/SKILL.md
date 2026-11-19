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

## Scripts

The scripts are in the `scripts/` folder of this skill's base directory. Run each one as `<skill-dir>/scripts/<name>`, where `<skill-dir>` is that base directory. Each script has `--help`. A script result wins over your own judgment.

**Escalation.** `route`, `check`, and `migration-sort` print 1 `pending:` line for each open decision. A pending decision is open work, as a violation is, also when the script exits 1. Do the `next:` action of each `pending:` line:

- **`escalate=fallback`:** start a subagent on the smallest model of your own model family for `tier=small`, or on the mid-size model of your family for `tier=medium`. Give it only the `request` object, and require the answer in the same labels. The subagent answers, not the main context.
- **`escalate=orchestrator`:** the orchestrator decides with the `request`, its thresholds, and its actions.
- **Record.** Record only the answer that the fallback subagent or the orchestrator gave, with the `scripts/decide --resolve` command of the line (`scripts/decide --help` gives the `--answer` form). The record goes to `.ios-architecture/resolutions.jsonl`; keep that file in the change. `check` prints each recorded answer that it applies as a `resolved:` line.
- Reach the TypeSafe API only through `scripts/decide`, and keep each file in `decisions/` as it is. Never call the API directly, and never change a decision file to get a different answer.

## Process

1. **Gate.** Load this skill in every agent and subagent before it reads or edits iOS code. When you delegate iOS work, make this the first line of the subagent prompt: `Invoke the ios-architecture skill before you read or edit code.` The gate is complete when the skill is loaded in each context that edits code.
2. **Profile.** The _project profile_ is `ios-architecture.json` in the project folder. When the profile is missing, ask the user for its fields, and write the answers to the profile. For a new project, ask for each field of `scripts/scaffold --help`. For an existing project, ask only whether code can leave the machine, and write `{"code_may_leave_machine": <answer>}`: the scripts for an existing project read only this field. Write `true` only when the user answers yes; else write `false`. The step is complete when the project folder holds the profile.
3. **Scaffold.** For a new project, run `scripts/scaffold <project-dir>` on the folder that holds only the profile. For a new feature, run `scripts/new-feature <project-dir> <Name>`. These scripts write the project and feature files; you do not write them by hand.
4. **Route.** Before you edit, run `scripts/route <project-dir> <file>...` with each existing file the change touches and each planned new path. After you edit, run `scripts/route <project-dir>` with no files, and read each new reference it prints. List each concern the change touches that the output does not cover, and match it to a row of the route table. For a concern with no row, run `scripts/decide out-of-bounds <concern>`: use the row it answers, or mark the concern _out of bounds_ when it answers `none`. The step is complete when each concern has a row or is marked _out of bounds_, the last `route` run prints no `pending:` line, and you read each reference that this run prints.
5. **Read.** Read each reference that `route` prints or a row matches, in full, and only those references.
6. **Apply.** Write or review the change against the rules of each matched reference. Change a default only when a _threshold_ in [deviations](references/deviations.md) applies, and name that threshold in the reply. A default change with no matching threshold is _out of bounds_.
7. **Out of bounds.** For each out-of-bounds concern, research the industry standard in primary sources: Apple developer documentation, the Human Interface Guidelines, Swift Evolution proposals, and WWDC sessions. Choose the pattern that keeps the invariants and follows the priority order. Write a short _decision record_ in the repository's decision record folder, for example `docs/adr/`. Record the problem, the pattern, the sources, and the priority the pattern serves. The step is complete when each out-of-bounds concern has a decision record with sources, named in the reply.
8. **Check.** Before you report done, run `scripts/check <project-dir>`, do the `next:` action of each `pending:` line, and run `check` again. Check the diff against each rule of each matched reference that the script does not examine (`scripts/check --rules` lists the rules it examines). The work is complete when the last line of `check` starts with `check: 0 violations, 0 pending decisions`, and each other rule is met or the reply names the rule and why it does not apply.

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
| An existing app, legacy code, CocoaPods, Swift 5, UIKit screens, a port from another technology | [migration](references/migration.md); run `scripts/migration-sort <project-dir>` first |
| A change to a default, a choice between patterns or stores | [deviations](references/deviations.md) |
| Screen layout, platform UI conventions, flow design | the `native-ui-patterns` skill |
