import Foundation

/// Makes UUIDs. Inject it, so that tests get known values.
public struct UUIDGenerator: Sendable {
    private let make: @Sendable () -> UUID
    public init(_ make: @escaping @Sendable () -> UUID) { self.make = make }
    public func callAsFunction() -> UUID { make() }
    public static let live = UUIDGenerator { UUID() }
}

/// Reproducible random numbers for tests and simulations.
/// Do not use it for security: use `SystemRandomNumberGenerator` or `SecRandomCopyBytes` for tokens, nonces, and keys.
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
