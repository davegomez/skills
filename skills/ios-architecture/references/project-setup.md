# Project setup

## Project setup and toolchain

Set up the project so that every build is reproducible and every environment is explicit.

**Toolchain**

- Use the baseline Xcode version or later. Pin the exact Xcode version in CI.
- Set Swift 6 language mode in every target.
- In the app target, set **Default Actor Isolation** to `MainActor` (`SWIFT_DEFAULT_ACTOR_ISOLATION = MainActor`).
- In the app target, set **Approachable Concurrency** to `Yes` (`SWIFT_APPROACHABLE_CONCURRENCY = YES`).
- Set the minimum deployment target from your user data. Use `#available` checks for newer APIs.
- Use Swift Package Manager for all dependencies. Do not add CocoaPods or Carthage.

**Workspace layout**

- Create an `.xcworkspace` with the app project in `App/` and local packages in `Packages/`.
- Keep the app target almost empty (see [Modularization with local Swift packages](architecture.md)).
- Keep `Info.plist`, entitlements, and the privacy manifest under version control.

**Build configurations and environments**

- Create 1 build configuration per environment: `Debug`, `Staging`, and `Release`.
- Put configuration values in `.xcconfig` files, not in the project file.
- Give each non-production environment its own bundle identifier suffix and app icon. Testers can then install all variants side by side.
- Inject the environment (base URLs, feature flag defaults) into the composition root. Do not read it in feature code.

**Warning:** Do not put API secrets in `.xcconfig` files, `Info.plist`, or source code. Anyone can extract them from the app bundle. Keep secrets on your server (see [Security and privacy](security-privacy.md)).

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

## New project checklist

Complete these steps in order before you build the first feature.

**Foundation**

- [ ] Create the workspace with `App/` and `Packages/`
- [ ] Set Swift 6 language mode in every target
- [ ] Set `MainActor` default isolation and Approachable Concurrency in the app target
- [ ] Add the concurrency settings from [Concurrency and reliability](concurrency.md) to every package manifest
- [ ] Create `Debug`, `Staging`, and `Release` configurations with `.xcconfig` files
- [ ] Register the bundle ID, App Groups, Keychain access groups, and Associated Domains
- [ ] Add `PrivacyInfo.xcprivacy` and `ITSAppUsesNonExemptEncryption`

**Core packages**

- [ ] Create `Core` with `FeatureKit`, client protocols, `SeededGenerator`, and fakes
- [ ] Create `DesignSystem` with 1 accessible component, tested with VoiceOver and the largest text size
- [ ] Create `Networking` and `Persistence` with live implementations and tests
- [ ] Add the seams from [Purchases and cross-cutting seams](purchases-seams.md) with safe defaults
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
- [ ] Complete the App Store Connect checklist in [Release engineering and App Store compliance](release.md)
