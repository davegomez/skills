# Concurrency and reliability

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
