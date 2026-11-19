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

**Pure reducer example:** the domain target of the [feature template](../template-feature/Sources/__FEATURE__Domain/__FEATURE__Domain.swift).

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

The `FeatureKit` target of [`Core`](../template/Packages/Core/Sources/FeatureKit/Feature.swift) holds the contract: `FeatureID`, `FeatureMetadata`, `EntitlementRequirement`, `Services`, `FeatureContext`, `Feature`, and `FeatureRegistry`.

The [composition root](../template/App/__APP__/__APP__.swift) builds the registry once. The shell renders navigation from the registry only.

To add a feature, run [`scripts/new-feature`](../scripts/new-feature) `<project-dir> <Name>`. The script makes the package from the feature template, links it to the app, and adds 1 `register` line at the marker comment in the composition root. The shell does not change.

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

The [project template](../template/) is the directory tree of a new project. The [feature template](../template-feature/) is the tree of 1 package in `Packages/Features/`. In path names and file contents, `__APP__` is the app name and `__FEATURE__` is the feature name.

**Package manifest**

The [feature manifest](../template-feature/Package.swift) is the reference manifest: a pure domain target that keeps the `nonisolated` default, and a UI target with `MainActor` default isolation.

- Write the platform version in the string form, for example `.iOS("<minimum>")`. The manifest then does not depend on the enum case of 1 tools version.
- Add the same version for macOS, so that `swift test` runs on the development Mac.
- Swift packages do not inherit the app target's concurrency settings, so set them in every manifest.
