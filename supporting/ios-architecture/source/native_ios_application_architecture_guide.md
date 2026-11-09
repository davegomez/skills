# Native iOS Application Architecture Guide

## 1. Summary

Build every native iOS app as a SwiftUI-first, modular Swift Package workspace. Use a thin app shell, framework-free domain packages, and thin presentation packages. Put every cross-cutting service behind a protocol.

- **Shell:** The app target is the composition root. It builds live services, registers features, and owns root navigation. It contains almost no other code.
- **Domain:** Each feature has a pure `XDomain` target. It holds value types and pure functions, conforms to `Sendable`, and imports no UI framework.
- **Presentation:** Each feature has an `XFeature` target. It holds SwiftUI views and `@Observable` models that call the domain and injected services.
- **Services:** Networking, persistence, authentication, purchases, analytics, feature flags, and diagnostics live behind protocols. Each protocol has a live implementation and a fake.
- **Concurrency:** Use Swift 6 language mode everywhere. Use `MainActor` default isolation in UI targets only. Keep domain targets `nonisolated`.
- **Quality gates:** Domain coverage of 90% or more, automated accessibility audits, published Accessibility Nutrition Labels, and a complete privacy manifest before every release.

This guide applies to all app types: content, productivity, commerce, social, backend-driven, offline-first, health, and finance. Change a default only when a threshold in Section 22 applies.

**Platform baseline:** Xcode 27 or later, Swift 6.4 or later, and the iOS 27 SDK or later. Xcode 27 runs only on Apple silicon Macs with macOS Tahoe 26.6 or later.

## 2. Priority order for trade-offs

When 2 goals conflict, the higher priority wins.

1. **Security:** Protect user data, secrets, and the integrity of the app.
2. **Reliability:** Make behavior correct, deterministic, and testable.
3. **Accessibility:** Make every common task possible with assistive technologies.
4. **Maintainability:** Keep modules small, boundaries clear, and dependencies explicit.
5. **Performance:** Optimize only after you measure a problem.

Examples: Do not cache a token in `UserDefaults` to save a Keychain read. Do not draw a custom control in `Canvas` if it removes VoiceOver support.

## 3. Project setup and toolchain

Set up the project so that every build is reproducible and every environment is explicit.

**Toolchain**

- Use Xcode 27 or later. Pin the exact Xcode version in CI.
- Set Swift 6 language mode in every target.
- In the app target, set **Default Actor Isolation** to `MainActor` (`SWIFT_DEFAULT_ACTOR_ISOLATION = MainActor`).
- In the app target, set **Approachable Concurrency** to `Yes` (`SWIFT_APPROACHABLE_CONCURRENCY = YES`).
- Set the minimum deployment target from your user data. Use `#available` checks for newer APIs.
- Use Swift Package Manager for all dependencies. Do not add CocoaPods or Carthage.

**Workspace layout**

- Create an `.xcworkspace` with the app project in `App/` and local packages in `Packages/`.
- Keep the app target almost empty (see Section 6).
- Keep `Info.plist`, entitlements, and the privacy manifest under version control.

**Build configurations and environments**

- Create 1 build configuration per environment: `Debug`, `Staging`, and `Release`.
- Put configuration values in `.xcconfig` files, not in the project file.
- Give each non-production environment its own bundle identifier suffix and app icon. Testers can then install all variants side by side.
- Inject the environment (base URLs, feature flag defaults) into the composition root. Do not read it in feature code.

**Warning:** Do not put API secrets in `.xcconfig` files, `Info.plist`, or source code. Anyone can extract them from the app bundle. Keep secrets on your server (see Section 11).

**Signing and identifiers**

- Use automatic signing for development. Use App Store Connect API keys for CI signing.
- Store signing keys and API keys in the CI secrets manager.
- Register the bundle ID, App Groups, Keychain access groups, and Associated Domains before the first build. Changing them later breaks data access.

**Dependency policy**

- Add a third-party package only when it saves significant work and has active maintenance.
- Pin each package to an exact version or a tight range. Commit `Package.resolved`.
- Review the license, the privacy manifest, and the binary signature of each package before you add it.
- Wrap each third-party API behind your own protocol. Feature code must not import the vendor module.

**Code quality tools**

- Run `swift-format` or SwiftLint in CI. Fail the build on violations.
- Treat compiler warnings as errors in CI for domain and core packages.
- Record architecture decisions as short decision records in the repository.

## 4. UI framework

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
- Use `ASWebAuthenticationSession` for sign-in, not an embedded web view (see Section 9).
- Limit in-app navigation to an allowlist of HTTPS origins. Open all other links outside the app.
- Do not expose a JavaScript bridge to content that you do not control. Validate every message from the page as untrusted input.

**Design system package**

- Put shared components, typography, color tokens, spacing, and icons in a `DesignSystem` package.
- Build every component with its accessibility label, value, traits, and Dynamic Type behavior included.
- Define colors as asset catalog colors with light, dark, and increased-contrast variants.
- Provide a SwiftUI preview for each component at the largest accessibility text size.

## 5. Application architecture pattern

Use a pure domain core plus a thin presentation layer. Choose the presentation pattern by app size and team size.

| Pattern | Use when | Do not use when |
| --- | --- | --- |
| MV with `@Observable` | 1 to 8 engineers; most screens show and edit data; side effects are simple | Many features share complex, long-running effects |
| MVVM with `@Observable` view models | You need a testable seam per screen; the team already knows MVVM | View models only forward calls to a service |
| The Composable Architecture (TCA) | Large app; heavy side effects; you need exhaustive state tests | A small team that cannot absorb a third-party framework and its migrations |
| Clean architecture or VIPER | Very large teams with strict layer ownership | Small or medium apps, where the ceremony costs more than it saves |

If you adopt TCA, use its current stable major release. Do not ship a beta release of the framework in production.

**Rules for every pattern**

- Put business rules in a domain target. Import only `Foundation`, or nothing.
- Make domain types `struct` or `enum` values that conform to `Sendable` and `Equatable`.
- Write domain logic as pure functions, for example `(State, Action) -> State`.
- Keep `@Observable` models in the feature target. Make them call the domain and the injected services.
- Do not import SwiftUI, UIKit, or StoreKit into a domain target.
- Use `@Observable` for observable state. Do not use `ObservableObject` or Combine pipelines for new state.

**Pure reducer example**

```swift
public struct CartState: Equatable, Sendable {
    public var items: [LineItem] = []
}

public enum CartAction: Sendable {
    case add(LineItem)
    case remove(id: LineItem.ID)
    case clear
}

public func reduce(_ state: CartState, _ action: CartAction) -> CartState {
    var next = state
    switch action {
    case .add(let item):
        next.items.append(item)
    case .remove(let id):
        next.items.removeAll { $0.id == id }
    case .clear:
        next.items = []
    }
    return next
}
```

**Dependency injection**

- Define each external capability as a protocol or a struct of closures (a client).
- Create live implementations only in the composition root. Do not reach services through singletons or global state.
- Pass dependencies through initializers or the SwiftUI `Environment`.
- Provide a fake implementation for tests and a preview implementation for SwiftUI previews.
- Inject every source of non-determinism: clock, random numbers, UUIDs, locale, and time zone.

## 6. Modularization with local Swift packages

Use an app target that contains almost no code, plus local packages in a `Packages/` folder. Module boundaries then enforce the architecture, not convention.

Benefits:

- Xcode recompiles only the changed modules and their dependents.
- Independent packages build in parallel.
- Each package has its own tests, so you can test it in isolation.
- Access control (`internal` by default) hides implementation details.

**Package roles**

| Package | Contents | May depend on |
| --- | --- | --- |
| App shell (app target) | `@main` app, root navigation, live service construction, feature registration | All packages |
| `Core` | `FeatureKit` contract, client protocols, shared value types, `SeededGenerator`, clock and UUID clients, fakes | Nothing |
| `DesignSystem` | Accessible components, typography, color tokens | `Core` |
| `Networking`, `Persistence`, `Services` | Live implementations of the `Core` protocols | `Core` |
| `Features/X` | `XDomain` (pure) and `XFeature` (SwiftUI) | `Core`, `DesignSystem` |

A feature package must not depend on another feature package. Share code through `Core` or a new shared package.

**Feature contract and registry**

```swift
// Package: Core, target: FeatureKit (nonisolated)
import SwiftUI

public struct FeatureID: Hashable, Codable, Sendable {
    public let rawValue: String
    public init(_ rawValue: String) { self.rawValue = rawValue }
}

public struct FeatureMetadata: Sendable {
    public let title: LocalizedStringResource
    public let systemImage: String
    public init(title: LocalizedStringResource, systemImage: String) {
        self.title = title
        self.systemImage = systemImage
    }
}

public enum EntitlementRequirement: Sendable {
    case none
    case product(String)
}

public struct Services: Sendable {
    public let http: any HTTPClient
    public let store: any KeyValueStore
    public let entitlements: any EntitlementService
    public let analytics: any AnalyticsClient
    public let flags: any FeatureFlagProvider
    public let diagnostics: any DiagnosticsClient
    // Add a public memberwise init so the composition root can build it.
}

public struct FeatureContext: Sendable {
    public let services: Services
    public init(services: Services) { self.services = services }
}

public protocol Feature: Sendable {
    var id: FeatureID { get }
    var metadata: FeatureMetadata { get }
    var requirement: EntitlementRequirement { get }
    @MainActor func makeRootView(context: FeatureContext) -> AnyView
}

public struct FeatureRegistry: Sendable {
    public private(set) var features: [any Feature] = []
    public init() {}

    public mutating func register(_ feature: any Feature) {
        precondition(!features.contains { $0.id == feature.id }, "Duplicate FeatureID")
        features.append(feature)
    }

    public func feature(for id: FeatureID) -> (any Feature)? {
        features.first { $0.id == id }
    }
}
```

The composition root builds the registry once. The shell renders navigation from the registry only.

```swift
// App target: composition root
var registry = FeatureRegistry()
registry.register(CatalogEntry())
registry.register(CheckoutEntry())
registry.register(SettingsEntry())
```

To add a feature: create a package, conform 1 type to `Feature`, and add 1 `register` line. The shell does not change.

**Access control rules**

- Make domain types `public` only when the feature target needs them.
- Make only the `Feature` conformer and its metadata `public` to the shell.
- Keep view models and views `internal`.
- Reference concrete feature types only in the composition root.

**Naming rules**

- Name the package after the domain, for example `Checkout`.
- Suffix the products with `Domain` and `Feature`: `CheckoutDomain`, `CheckoutFeature`.
- Suffix the `Feature` conformer with `Entry`: `CheckoutEntry`.
- Name each test target after its target plus `Tests`.

**Directory tree**

```
MyApp.xcworkspace
App/
  MyApp.xcodeproj
  MyApp/
    MyApp.swift                 // @main, composition root
    AppShell/RootView.swift
    AppShell/AppRoute.swift
    AppShell/AppRouter.swift
    Resources/Assets.xcassets
    Resources/Localizable.xcstrings
    Resources/InfoPlist.xcstrings
    PrivacyInfo.xcprivacy
  Config/
    Debug.xcconfig
    Staging.xcconfig
    Release.xcconfig
Packages/
  Core/
    Package.swift
    Sources/FeatureKit/         // Feature, FeatureRegistry, FeatureContext
    Sources/CoreClients/        // HTTPClient, KeyValueStore, Clock, ...
    Sources/CoreTesting/        // fakes
  DesignSystem/
    Sources/DesignSystem/       // components, tokens
    Sources/DesignSystem/Resources/Localizable.xcstrings
  Networking/
    Sources/Networking/
    Tests/NetworkingTests/
  Persistence/
    Sources/Persistence/        // Keychain, file store, database
    Tests/PersistenceTests/
  Features/
    Checkout/
      Package.swift
      Sources/CheckoutDomain/   // pure: State, Action, reduce, validators
      Sources/CheckoutFeature/  // CheckoutEntry, @Observable model, views
      Sources/CheckoutFeature/Resources/Localizable.xcstrings
      Tests/CheckoutDomainTests/   // unit, property-based, golden
      Tests/CheckoutFeatureTests/  // model and snapshot tests
ci/
  test-plan.xctestplan
```

**Package manifest**

```swift
// swift-tools-version: 6.2
import PackageDescription

let concurrencyFeatures: [SwiftSetting] = [
    .enableUpcomingFeature("NonisolatedNonsendingByDefault"),
    .enableUpcomingFeature("InferIsolatedConformances"),
]

let package = Package(
    name: "Checkout",
    defaultLocalization: "en",
    platforms: [.iOS(.v26)],
    products: [
        .library(name: "CheckoutDomain", targets: ["CheckoutDomain"]),
        .library(name: "CheckoutFeature", targets: ["CheckoutFeature"]),
    ],
    dependencies: [
        .package(path: "../../Core"),
        .package(path: "../../DesignSystem"),
    ],
    targets: [
        // Pure domain: keep the nonisolated default.
        .target(name: "CheckoutDomain", swiftSettings: concurrencyFeatures),
        .target(
            name: "CheckoutFeature",
            dependencies: [
                "CheckoutDomain",
                .product(name: "FeatureKit", package: "Core"),
                .product(name: "DesignSystem", package: "DesignSystem"),
            ],
            resources: [.process("Resources")],
            swiftSettings: concurrencyFeatures + [.defaultIsolation(MainActor.self)]
        ),
        .testTarget(name: "CheckoutDomainTests", dependencies: ["CheckoutDomain"]),
        .testTarget(name: "CheckoutFeatureTests", dependencies: ["CheckoutFeature"]),
    ]
)
```

Replace `.v26` with your own minimum deployment target. Swift packages do not inherit the app target's concurrency settings, so set them in every manifest.

## 7. Navigation and deep links

Use `NavigationStack` with a typed route enum, owned by a router in the shell. Treat every incoming URL as untrusted input.

- Use `NavigationSplitView` for iPad and wide layouts.
- Keep the navigation path in an `@Observable` router that the shell owns.
- Use a typed array when all routes share 1 type. Use `NavigationPath` when routes from unrelated types share 1 stack.
- Add a coordinator layer only when you have deep links, several entry points, or flows that cross features.

```swift
enum AppRoute: Hashable, Codable {
    case feature(FeatureID)
    case detail(id: String)
}

@Observable
final class AppRouter {
    var path: [AppRoute] = []
    func open(_ route: AppRoute) { path.append(route) }
    func popToRoot() { path.removeAll() }
}
```

**Deep links and universal links**

- Support universal links with an `apple-app-site-association` file and the Associated Domains entitlement.
- Handle links with `.onOpenURL` and `.onContinueUserActivity`.
- Parse every incoming URL into an `AppRoute`. Reject unknown or invalid input.
- Do not perform an action with side effects directly from a link. Show a confirmation screen first.
- Make `AppRoute` `Codable` so that you can restore navigation state after the system stops the app.

## 8. Networking

Use 1 `URLSession`-based client behind a protocol, with typed endpoints and `Codable` models.

```swift
public protocol HTTPClient: Sendable {
    func send<Response: Decodable & Sendable>(_ endpoint: Endpoint<Response>) async throws -> Response
}
```

**Design rules**

- Use the `async` APIs of `URLSession`: `data(for:)`, `bytes(for:)`, and `upload(for:from:)`.
- Define each endpoint as a value: method, path, query, body, and expected response type.
- Decode responses into `Sendable` data transfer objects. Map them to domain types at the boundary.
- Validate every response: status code, content type, and size limit.
- Retry only idempotent requests. Use exponential backoff with jitter and a maximum attempt count.
- Respect `Task` cancellation. Check `Task.isCancelled` in long loops.
- Use `NWPathMonitor` to show offline state. Do not use it to block a request.
- Version your API. Make the client accept unknown JSON fields and unknown enum cases without a crash.
- Add a request ID header to each request. Log the ID, not the payload.

**Security rules**

- Keep App Transport Security (ATS) on. Do not add `NSAllowsArbitraryLoads`.
- Use HTTPS with TLS 1.2 or later for every endpoint.
- Store access and refresh tokens in the Keychain only.
- Do not log request bodies, tokens, or headers that contain credentials.
- Consider public-key pinning only for high-risk apps, such as finance or health.

**Warning:** A wrong pin locks every user out until they install an update. Before you pin, ship a backup key and write a key rotation plan.

**Offline behavior**

- Show cached content when the network is not available.
- Queue user writes locally and send them when the connection returns (see Section 12).
- Show the network state and the last sync time to the user.

**Real-time and other protocols**

- Use `URLSessionWebSocketTask` for WebSockets. Reconnect with backoff, and authenticate again after each reconnect.
- Read server-sent streams with `bytes(for:)` and its `lines` sequence.
- For GraphQL, generate typed operations from the schema. Send them through the same `HTTPClient` seam.
- Use push notifications to signal new data. Fetch the data itself over an authenticated request.

## 9. Authentication and identity

Put authentication behind an `AuthClient` protocol in `Core`. Prefer passkeys and Sign in with Apple over passwords.

- Use the `AuthenticationServices` framework for passkeys, Sign in with Apple, and password AutoFill.
- Use `ASWebAuthenticationSession` with OAuth 2.0 and PKCE for third-party identity providers. Do not use an embedded web view for sign-in.
- If you offer third-party sign-in, offer a login option that meets App Review Guideline 4.8.
- Store tokens in the Keychain. Refresh them in 1 place, and serialize refresh calls through an actor.
- Treat a `401` response as a signal to refresh once. If the refresh fails, sign the user out cleanly.
- Clear all user data, caches, and Keychain items on sign-out.
- If the app supports account creation, provide account deletion inside the app. App Review requires it.
- Use `LocalAuthentication` (Face ID, Touch ID) only to unlock a local secret. Do not use it as proof of identity to your server.

If the app has no accounts, still define the `AuthClient` seam with a no-op default. You can then add accounts later without changes to feature code.

## 10. Persistence

Use the simplest store that meets your query and sync needs, and put it behind a protocol. Feature code must not know the storage engine.

| Need | Use | Notes |
| --- | --- | --- |
| Small preferences and flags | `UserDefaults` | Not for secrets or large data. Declare the required reason in the privacy manifest. |
| Tokens, passwords, keys | Keychain | Use `kSecAttrAccessibleWhenUnlockedThisDeviceOnly` or stricter for sensitive items. |
| Documents, caches, small state | `Codable` files | Write atomically. Set a Data Protection class. |
| Object graph, SwiftUI-driven lists, private CloudKit sync | SwiftData | Use `VersionedSchema` and `SchemaMigrationPlan` from version 1. |
| Mature object graph, advanced fetches, shared or public CloudKit data | Core Data | `NSPersistentCloudKitContainer` supports private, shared, and public databases. |
| SQL, complex queries, joins, full control | GRDB or SQLiteData | Both are SQLite-based. SQLiteData adds observation-friendly queries and CloudKit sync. |
| Small key-value sync across devices | `NSUbiquitousKeyValueStore` | Small quota. Not for user content. |

**Rules**

- Put every store behind a protocol in `Core`, with an in-memory fake for tests.
- Run database work off the main actor. Pass `Sendable` snapshots back to the UI.
- Version your schema from the first release, whatever engine you use.
- Write a migration test for each schema version, with a fixture from the previous version.
- Choose the strictest Data Protection class that your background work allows. Use `.complete` for regulated data unless the app must read it while the device is locked.
- Exclude caches and data that you can download again from backup.
- Put data that extensions read in the App Group container.

**SwiftData migrations:** SwiftData supports `MigrationStage.lightweight` and `MigrationStage.custom(fromVersion:toVersion:willMigrate:didMigrate:)`. Use a custom stage for data changes such as deduplication or derived values.

**Sync to your own server:** Use SwiftData history (`HistoryObserver`) or Core Data persistent history to find local changes since the last sync.

**Performance:** Do not choose a store from published benchmarks alone. Measure with your own data shape and volume.

## 11. Security and privacy

Apply every control in this section to every app. If the data classification is not clear, treat the data as regulated until someone confirms otherwise.

**Controls**

- **Secrets:** Do not ship API secrets in the binary. Keep secrets on your server, and give the app short-lived tokens.
- **Keychain:** Store credentials and keys in the Keychain. Use access control flags (`.biometryCurrentSet`, `.userPresence`) for high-value items.
- **Data Protection:** Set a file protection class on every file that contains user data.
- **Transport:** Keep ATS on (see Section 8).
- **App integrity:** Use App Attest (`DCAppAttestService`) to prove to your server that requests come from a genuine copy of your app. Use DeviceCheck for per-device state, such as promotion abuse.
- **Trust boundaries:** Validate all input from the network, deep links, the pasteboard, files, extensions, and widgets. Parse it into typed domain values, and reject invalid values early.
- **Errors:** Show generic error messages to users. Put details in logs, without personal data.
- **Randomness:** Use `SystemRandomNumberGenerator` or `SecRandomCopyBytes` for tokens, nonces, and keys.
- **Screen content:** Hide sensitive screens in the app switcher snapshot. Mark sensitive text fields so that the system does not store them.
- **AI features:** Treat model output and retrieved content as untrusted input. Ask for user confirmation before an action with side effects.

**Logging**

- Use `os.Logger` with 1 subsystem per app and 1 category per module.
- Dynamic values are private by default in release logs. Mark only non-sensitive values with `privacy: .public`.
- Use `privacy: .private(mask: .hash)` to correlate events without exposing values.
- Use structured key-value messages. Do not log tokens, request bodies, or personal data.

**Privacy requirements**

- Ship `PrivacyInfo.xcprivacy` in the app. Declare collected data types, tracking domains, and a reason code for each required-reason API (file timestamps, system boot time, disk space, active keyboards, `UserDefaults`).
- Make sure every third-party SDK ships its own privacy manifest and, for binary SDKs, a valid signature.
- Keep the App Store privacy labels equal to what the app and its SDKs actually collect.
- Request App Tracking Transparency permission before you track users across apps or websites. If you do not track, do not show the prompt.
- Write a purpose string for every permission. Request each permission at the moment the user needs the feature, not at launch.
- Collect only the data that a feature needs.

**Regulated data (high-level guide, not legal advice)**

- **Health (for example, HIPAA in the US):** Store the minimum protected health information. Encrypt it at rest and in transit. Keep audit logs on the server. Sign a business associate agreement with every vendor that touches the data.
- **Payments (PCI DSS):** Do not handle raw card numbers. Use Apple Pay or a certified payment SDK so that card data does not enter your systems. Use StoreKit for digital goods, as App Review requires.
- **Personal data (GDPR and similar laws):** Document the legal basis for each data type. Support data export and deletion. Get consent before any optional collection.

Get a legal and compliance review before you release an app that handles regulated data.

## 12. Concurrency and reliability

Use Swift 6 strict concurrency everywhere, `MainActor` isolation for UI code, and `nonisolated`, `Sendable` code for the domain.

**Concurrency settings**

| Target type | Default isolation | Upcoming features |
| --- | --- | --- |
| App target | `MainActor` (build setting) | Approachable Concurrency: `Yes` |
| UI package targets (`XFeature`, `DesignSystem`) | `.defaultIsolation(MainActor.self)` | `NonisolatedNonsendingByDefault`, `InferIsolatedConformances` |
| Domain and core targets (`XDomain`, `Core`) | `nonisolated` (package default) | `NonisolatedNonsendingByDefault`, `InferIsolatedConformances` |
| Service targets (`Networking`, `Persistence`) | `nonisolated` | `NonisolatedNonsendingByDefault`, `InferIsolatedConformances` |

**Rules**

- Make domain types `Sendable` value types.
- Mark CPU-heavy functions `@concurrent` so that they run off the caller's actor.
- Do not use `Task.detached` or `DispatchQueue` to leave the main actor. Call a `@concurrent` function instead. A detached task loses priority, task-local values, and cancellation from its parent.
- Prefer structured concurrency (`async let`, task groups) over unstructured `Task { }` blocks.
- Use an `actor` for shared mutable state in services, such as a token refresher or a sync queue.
- Do not use `@unchecked Sendable` or `nonisolated(unsafe)` without a comment that explains why the code is safe.
- Do not block the main actor with synchronous I/O.

**Warning:** Generated String Catalog symbols can fail to compile in a target with `MainActor` default isolation. Before you turn on symbol generation in a UI package, build it. If the build fails, use `String(localized:bundle:)` with `#bundle` in that target.

**Error handling**

- Model expected failures as typed domain errors, for example `enum CheckoutError: Error`.
- Map domain errors to user-facing messages in the feature layer.
- Do not use `try!` or force unwraps on external data.
- Do not use `try?` to discard errors from external data. Catch the error, log it without personal data, and show a generic message.
- Give every error state that the user can see a recovery action.
- Show explicit loading, empty, error, and offline states on every screen that loads data.

**Determinism**

Inject every source of non-determinism: clock, random numbers, UUIDs, locale, and time zone. Use a seeded generator for reproducible tests and simulations.

```swift
public struct SeededGenerator: RandomNumberGenerator, Sendable {
    private var state: UInt64

    public init(seed: UInt64) { state = seed }

    // SplitMix64: fast and reproducible, not cryptographically secure.
    public mutating func next() -> UInt64 {
        state &+= 0x9E37_79B9_7F4A_7C15
        var z = state
        z = (z ^ (z >> 30)) &* 0xBF58_476D_1CE4_E5B9
        z = (z ^ (z >> 27)) &* 0x94D0_49BB_1331_11EB
        return z ^ (z >> 31)
    }
}
```

**Warning:** Do not use a seeded generator for security. Use `SystemRandomNumberGenerator` or `SecRandomCopyBytes` for tokens, nonces, and keys.

**Offline-first and sync**

- Write locally first. Sync in the background with a queue of pending changes.
- Use SwiftData or Core Data with CloudKit for private sync scoped to the user's Apple Account.
- Use SQLiteData for SQLite with CloudKit sync.
- Use your own backend when you need cross-platform sync or server-side rules.
- Define conflict rules (last writer wins, merge, or user choice) in the domain target, and test them.

**Crash and hang reporting**

- Use Xcode Organizer for crashes, hangs, energy, and disk writes from users who share analytics.
- Use MetricKit for on-device diagnostics and metrics.
- If you use a third-party crash reporter, declare its data collection in the privacy manifest and the App Store privacy labels.

## 13. App lifecycle, background work, notifications, and extensions

Drive lifecycle behavior from SwiftUI scene phases, and share data with extensions only through an App Group.

**Lifecycle**

- Use the SwiftUI `App` lifecycle. Use `@UIApplicationDelegateAdaptor` only for APIs that need an app delegate, such as push registration.
- React to `scenePhase` changes: save state on `.background`, refresh data on `.active`.
- Restore navigation and draft state after the system stops the app (see Section 7).

**Background work**

- Use `BGTaskScheduler` with `BGAppRefreshTask` for short refreshes and `BGProcessingTask` for long maintenance work.
- Use `BGContinuedProcessingTask` for user-started work that must continue after the user leaves the app.
- Use a background `URLSession` for large uploads and downloads.
- Make every background task idempotent. The system can stop it at any time.

**Push notifications**

- Put push handling behind a `NotificationClient` protocol.
- Use token-based APNs authentication. Keep the signing key in your server's secrets manager.
- Send the minimum content in the payload. Use a Notification Service Extension to fetch or decrypt sensitive content.
- Request notification permission when the user turns on a feature that needs it.

**Extensions and system integration**

- Put each extension (widgets, Live Activities, share extension, notification extension) in its own target. Make it depend on the same `Core` and domain packages as the app.
- Share data through the App Group container and a shared Keychain access group.
- Keep extensions small. They have strict memory and time limits.
- Expose main actions with App Intents. The system can then show them in Shortcuts, Siri, Spotlight, and widgets.
- Treat all data that an extension or intent receives as untrusted input.

## 14. Accessibility

Make every common task possible with each assistive technology, and publish Accessibility Nutrition Labels for every app and every update. Both are release requirements.

**Controls**

- **VoiceOver:** Give every control a label, a value, and traits. Add a hint only when the result of an action is not clear from the label. Group related elements with `.accessibilityElement(children: .combine)`. Add `.accessibilityAction` for every custom gesture.
- **Voice Control:** Make visible labels match accessibility labels. Add `.accessibilityInputLabels` for controls with long or ambiguous names.
- **Dynamic Type:** Use text styles, not fixed font sizes. Test at the largest accessibility sizes. Change the layout (for example, from `HStack` to `VStack`) when text does not fit.
- **Motion:** Read `accessibilityReduceMotion`. Replace large movement with fades.
- **Contrast and color:** Meet contrast targets in light and dark appearance. Do not use color alone to show state.
- **Media:** Provide captions for video and audio descriptions where the content needs them.
- **Focus:** Move VoiceOver focus to new content after navigation and to the first error after a failed submit.

**Accessibility Nutrition Labels (required)**

Accessibility Nutrition Labels show on the App Store product page which accessibility features the app supports.

1. Before the first release, test every common task with each feature: VoiceOver, Voice Control, Larger Text, Dark Interface, Differentiate Without Color Alone, Sufficient Contrast, Reduced Motion, Captions, and Audio Descriptions.
2. Record the result for each feature and each supported device type.
3. Declare in App Store Connect only the features that pass for all common tasks.
4. Repeat the test for every release. Update the labels before you submit.
5. Add a backlog item for each feature that does not pass.

**Warning:** Do not declare a feature that you did not test. App Review can ask you to correct misleading labels.

**Automated audits**

- Call `XCUIApplication().performAccessibilityAudit()` in UI tests on every main screen.
- Run the audits in CI. Fail the build on a new issue.

**Manual audits**

- Test each release with VoiceOver, Voice Control, and the largest text size.
- Use Accessibility Inspector for each new screen.

## 15. Localization

Use String Catalogs in the app and in each package, and load package strings from the package bundle.

- Use `Localizable.xcstrings` for UI text and `InfoPlist.xcstrings` for permission purpose strings and the display name.
- Set `defaultLocalization` in each `Package.swift` that has resources.
- In a package, load strings with `#bundle` or `.module`. Do not use `.main`, because it points to the app bundle.
- Generated String Catalog symbols are `internal`. If another package needs a string, expose a `public` API that returns `LocalizedStringResource`.
- Use plural and device variations in the catalog. Do not build plural strings in code.
- Format dates, numbers, currency, and measurements with `FormatStyle`. Do not format them by hand.
- Use leading and trailing, not left and right. Test right-to-left layout with a pseudo-language.
- Test the longest supported language at the largest text size.
- Send the catalogs to translators with comments that give context for each string.

## 16. Testing

Write domain tests first (test-driven development), then feature tests, then a small number of UI tests. Hold domain coverage at 90% or more.

| Layer | Tool | Target |
| --- | --- | --- |
| Domain | Swift Testing (`@Test`, `#expect`, `#require`) | 90% or more line coverage |
| Feature models | Swift Testing with fake clients | Main flows and every error state |
| Views | swift-snapshot-testing | Light, dark, largest Dynamic Type, right-to-left |
| Persistence | Swift Testing with fixtures | Every schema migration |
| UI flows and audits | XCTest (XCUITest) | Critical journeys and `performAccessibilityAudit()` |
| Performance | XCTest metrics and Instruments | Launch, scrolling, heavy operations |

**Techniques**

- Use parameterized tests (`@Test(arguments:)`) for tables of inputs.
- Use golden tests: store expected outputs for fixed seeds and inputs.
- Use property-based tests for invariants. Generate inputs with `SeededGenerator` in a loop, and record the seed in the failure message.
- Use replay tests: store a seed and a list of actions, then replay them through the reducer to any state.
- Test the live `Networking` client with a stub `URLProtocol`. Cover status codes, malformed bodies, timeouts, retries, and cancellation.
- Test the live persistence stores against a temporary on-disk database, not only the in-memory fake.
- Use fakes, not mocks with call counts, for services. Test results, not calls.

**XCTest and Swift Testing**

- Write all new unit tests in Swift Testing.
- Move existing XCTest unit tests to Swift Testing step by step. Both frameworks can run in the same test target.
- Keep UI tests in XCTest, because XCUITest requires it.

**CI**

- Run all tests on every pull request in Xcode Cloud or another CI service.
- Turn on code coverage in the test plan. Fail the build when domain coverage goes below 90%.
- Run tests on the oldest and newest supported iOS versions.
- Run UI tests with the largest text size and with a right-to-left language at least once per release.

## 17. Observability and performance

Measure before you optimize, and set performance budgets that CI checks.

- Add `OSSignposter` intervals around launch phases, network calls, and database work.
- Profile with Instruments: Time Profiler, SwiftUI, Hangs, Allocations, Network, and Swift Concurrency.
- Use the Swift Concurrency instrument to find actor contention and main-actor blocking.
- Collect field data with MetricKit and Xcode Organizer: launch time, hangs, scrolling, memory, and disk writes.
- Set budgets per reference device, for example time to first frame, memory peak, and app size.
- Test the budgets in CI with XCTest metrics. Fail the build when a budget is exceeded.
- Use lazy containers (`LazyVStack`, `List`) for long collections. Give each item a stable identity.
- Download and decode images off the main actor. Cache them with a size limit.

## 18. Purchases and cross-cutting seams

Put each cross-cutting concern behind a protocol with a safe default. Check entitlements in 1 place, in the shell.

| Seam | Protocol | Default |
| --- | --- | --- |
| Entitlements | `EntitlementService` | Entitled in debug builds; denied in release builds until StoreKit verifies a transaction |
| Authentication | `AuthClient` | Signed-out, no-op |
| Analytics | `AnalyticsClient` | No-op |
| Feature flags | `FeatureFlagProvider` | Compiled defaults |
| Diagnostics | `DiagnosticsClient` | `os.Logger` with privacy annotations |
| Notifications | `NotificationClient` | No-op |

The shell gates each feature through its `requirement` property. Feature and domain code never check purchases.

**StoreKit 2**

- Create 1 `@MainActor @Observable` store service in the shell.
- Start a `Transaction.updates` listener at launch, and keep it for the life of the app. Otherwise you miss renewals, refunds, Ask to Buy approvals, and purchases from other devices.
- Read `Transaction.currentEntitlements` at launch to build the entitlement state.
- Use only `.verified` transactions. StoreKit 2 verifies the JWS signature for you.
- Call `transaction.finish()` after you deliver the content.
- Provide a Restore Purchases action. App Review requires it for restorable purchases.
- Use `SubscriptionStoreView` and `ProductView` for standard paywalls.
- Use `AppTransaction` to check the original purchase of a paid app.
- Test purchases with a StoreKit configuration file locally and in the sandbox before release.
- Share entitlement state with extensions through the App Group.

**When you need a server**

Add App Store Server Notifications V2 and the App Store Server API when 1 of these conditions applies:

- Users have accounts that work on other platforms.
- Content comes from your server and must be protected.
- You must handle fraud, refunds, or revocations on the server.
- More than 1 app shares entitlements.

On-device StoreKit 2 is sufficient when content unlocks only on Apple devices.

**Analytics and feature flags**

- Define analytics events as a typed enum in `Core`. Do not pass free-form strings.
- Do not put personal data in events.
- Use remote feature flags as a kill switch for risky features. Make the compiled default the safe value.

## 19. Release engineering and App Store compliance

Automate every build and release step, and plan for the fact that you cannot roll back an installed version.

**Build and versioning**

- Build release candidates only in CI, with the pinned Xcode version.
- Use semantic versioning for the marketing version. Let CI set a build number that always increases.
- Upload debug symbols (dSYMs) for every build so that crash reports are readable.
- Build with the SDK version that App Store Connect currently requires.

**Distribution**

- Send every build to internal TestFlight testers first, then to external testers.
- Use phased release for updates. Pause it when crash or hang rates increase.
- Give App Review a demo account and notes for every feature that needs setup.

**Recovery without rollback**

- Use remote feature flags as kill switches for risky features (see Section 18).
- Add a minimum-supported-version check that asks users to update when a version is unsafe.
- Keep server APIs compatible with every app version that is still in use.

**App Store Connect requirements for each release**

- [ ] Privacy manifest complete, including third-party SDKs
- [ ] App privacy labels match actual data collection
- [ ] Accessibility Nutrition Labels tested and updated
- [ ] Age rating questionnaire answered
- [ ] Export compliance declared (`ITSAppUsesNonExemptEncryption` in `Info.plist`)
- [ ] Privacy policy URL current
- [ ] Trader status set for distribution in the European Union
- [ ] Account deletion available, if the app has accounts
- [ ] Restore Purchases available, if the app sells restorable purchases
- [ ] Screenshots and descriptions localized for every supported language

## 20. Migrating an existing app

Migrate step by step behind the running app, and keep every identifier that user data depends on. Do not rewrite the whole app in 1 release.

**Warning:** Do not change the bundle ID, team ID, App Group IDs, Keychain access groups, iCloud container IDs, Associated Domains, or in-app purchase product IDs. A change makes users lose data, purchases, or updates.

**Phase 1: Baseline**

1. List every feature, screen, data store, Keychain item, entitlement, deep link format, and push payload format.
2. Record the current crash rate, hang rate, launch time, and app size.
3. Write characterization tests for current behavior before you change code.
4. Collect data fixtures from each app version that users still run.

**Phase 2: Toolchain and dependencies**

1. Build the app with Xcode 27 and the current SDK. Fix all errors.
2. Adopt the `UIScene` lifecycle if the app does not use it. Apps built with the current SDK do not launch without it.
3. Move all CocoaPods and Carthage dependencies to Swift Package Manager.
4. Remove dependencies that have no maintenance, or wrap them behind a protocol and plan a replacement.

**Warning:** The CocoaPods trunk becomes read-only on December 2, 2026. After that date, pods get no new versions, including security fixes.

**Phase 3: Structure**

1. Create `Packages/` beside the existing code.
2. Move code from the bottom up: `Core` protocols and models first, then services, then features.
3. Move 1 feature at a time into an `XDomain` and `XFeature` pair. Keep the old code path until the new one passes its tests.
4. Register each moved feature in the composition root.

**Phase 4: Swift 6 and concurrency**

1. Start with leaf modules that have no dependents.
2. In each module, set strict concurrency checking to `Complete` in Swift 5 mode. Fix all warnings.
3. Switch that module to Swift 6 language mode.
4. Add the default isolation and upcoming-feature settings from Section 12.
5. Replace `ObservableObject` with `@Observable`, 1 model at a time.

**Phase 5: UI**

1. Build new screens in SwiftUI. Host them in UIKit navigation with `UIHostingController`.
2. Replace existing UIKit screens 1 at a time, starting with the screens that change most often.
3. Move the root navigation to SwiftUI last.

**Phase 6: Data**

1. Keep the existing store readable until the new store is verified.
2. Write each data migration so that it is idempotent and can resume after interruption.
3. Test each migration with the fixtures from Phase 1.
4. Read existing Keychain items with the same service, account, and access group. Do not delete an old item before you verify the new copy.
5. Migrate `.strings` and `.stringsdict` files to String Catalogs.

**Porting from another technology**

If the existing app uses a cross-platform framework, the native app is an update to the same App Store record.

1. Find every location where the previous runtime stored data: key-value stores, database files, file caches, and Keychain items with their service names.
2. Read and migrate that data on the first launch of the native version.
3. Keep deep link formats, push payload formats, and analytics event names compatible.
4. Reimplement business rules as pure domain code, guided by the characterization tests.
5. Reuse assets, translations, and server contracts. Do not reuse the UI component structure.

**Phase 7: Release**

1. Ship each migrated part behind a feature flag.
2. Use phased release, and compare metrics with the baseline from Phase 1.
3. Remove the old code path after the metrics stay stable for 1 full release.

## 21. New project checklist

Complete these steps in order before you build the first feature.

**Foundation**

- [ ] Create the workspace with `App/` and `Packages/`
- [ ] Set Swift 6 language mode in every target
- [ ] Set `MainActor` default isolation and Approachable Concurrency in the app target
- [ ] Add the concurrency settings from Section 12 to every package manifest
- [ ] Create `Debug`, `Staging`, and `Release` configurations with `.xcconfig` files
- [ ] Register the bundle ID, App Groups, Keychain access groups, and Associated Domains
- [ ] Add `PrivacyInfo.xcprivacy` and `ITSAppUsesNonExemptEncryption`

**Core packages**

- [ ] Create `Core` with `FeatureKit`, client protocols, `SeededGenerator`, and fakes
- [ ] Create `DesignSystem` with 1 accessible component, tested with VoiceOver and the largest text size
- [ ] Create `Networking` and `Persistence` with live implementations and tests
- [ ] Add the seams from Section 18 with safe defaults
- [ ] Build the shell: composition root, `FeatureRegistry`, `AppRouter`

**Quality gates**

- [ ] Set up CI that runs all tests on every pull request
- [ ] Fail CI when domain coverage goes below 90%
- [ ] Add a `performAccessibilityAudit()` UI test
- [ ] Add `swift-format` or SwiftLint to CI

**First feature**

- [ ] Write the `XDomain` target test-first, with 90% or more coverage, 1 property-based invariant, and 1 golden test
- [ ] Write the `XFeature` target with model tests and snapshot tests
- [ ] Register the feature in the composition root

**First release**

- [ ] Test and declare Accessibility Nutrition Labels
- [ ] Complete the App Store Connect checklist in Section 19

## 22. Trade-offs and thresholds

The defaults in this guide win on security, reliability, and accessibility. Change a default only when its threshold applies.

**Default decisions**

| Decision | Default | Main reason |
| --- | --- | --- |
| SwiftUI or custom renderer | SwiftUI | Accessibility, maintainability |
| Pure domain split or 1 layer | Split | Reliability (testability) |
| MV with `@Observable` or TCA | MV plus pure reducers | Maintainability; no third-party framework migrations |
| Files, SwiftData, Core Data, or GRDB | Simplest store that fits, behind a protocol | Reliability; you can change the engine later |
| Build purchases now or add a seam | Seam with a safe default | Security, maintainability |
| Modular packages or 1 target | Modular packages | Maintainability, build speed |
| Bundled String Catalogs or remote strings | String Catalogs | Reliability, security |

**Thresholds that change a default**

| Condition | Change |
| --- | --- |
| Custom drawing or animation that SwiftUI controls cannot show | Use `Canvas` or Metal in that feature only, with explicit accessibility elements |
| 3D or spatial content | Use RealityKit in that feature only |
| More than about 8 engineers, or many shared effects | Consider TCA or strict MVVM with a shared effects layer |
| Queries outgrow flat files (filters, joins, more than a few thousand records) | Move to SwiftData, Core Data, or GRDB behind the same protocol |
| Cross-device sync | Use CloudKit (SwiftData, Core Data, or SQLiteData) or your own backend |
| Accounts or purchases that work on other platforms | Add a server with App Store Server Notifications V2 |
| Regulated data | Add Data Protection `.complete`, App Attest, key pinning, server-side audit logs, and a compliance review |
