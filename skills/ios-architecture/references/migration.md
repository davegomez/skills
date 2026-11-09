# Migrating an existing app

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
4. Add the default isolation and upcoming-feature settings from [Concurrency and reliability](concurrency.md).
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
