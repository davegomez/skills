# Architecture and modules

## Application architecture pattern

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

## Modularization with local Swift packages

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
