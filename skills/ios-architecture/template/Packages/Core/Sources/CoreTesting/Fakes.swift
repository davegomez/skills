import CoreClients
import FeatureKit
import Foundation
import os

/// A clock that does not wait. `sleep` returns at once, or throws when the task is cancelled.
public struct ImmediateClock: Clock {
    public struct Instant: InstantProtocol {
        public let offset: Duration
        public init(offset: Duration = .zero) { self.offset = offset }
        public func advanced(by duration: Duration) -> Instant { Instant(offset: offset + duration) }
        public func duration(to other: Instant) -> Duration { other.offset - offset }
        public static func < (lhs: Instant, rhs: Instant) -> Bool { lhs.offset < rhs.offset }
    }

    public init() {}
    public var now: Instant { Instant() }
    public var minimumResolution: Duration { .zero }
    public func sleep(until deadline: Instant, tolerance: Duration?) async throws {
        try Task.checkCancellation()
    }
}

extension UUIDGenerator {
    /// Makes 00000000-0000-0000-0000-000000000000, then ...0001, and so on.
    public static func incrementing() -> UUIDGenerator {
        let counter = OSAllocatedUnfairLock(initialState: 0)
        return UUIDGenerator {
            let value = counter.withLock { count in
                defer { count += 1 }
                return count
            }
            var bytes = [UInt8](repeating: 0, count: 16)
            withUnsafeBytes(of: UInt64(value).bigEndian) { bytes.replaceSubrange(8..<16, with: $0) }
            return bytes.withUnsafeBytes { UUID(uuid: $0.load(as: uuid_t.self)) }
        }
    }
}

/// Answers each path from a fixed table of JSON bodies. Unknown paths fail with status 404.
public struct FakeHTTPClient: HTTPClient {
    private let responses: [String: Data]
    public init(responses: [String: Data] = [:]) { self.responses = responses }

    public func send<Response: Decodable & Sendable>(_ endpoint: Endpoint<Response>) async throws -> Response {
        guard let body = responses[endpoint.path] else { throw HTTPError.status(404) }
        do {
            return try JSONDecoder().decode(Response.self, from: body)
        } catch {
            throw HTTPError.malformedBody
        }
    }
}

/// Keeps values in memory, with the same key rules as the live store.
public actor InMemoryKeyValueStore: KeyValueStore {
    private var values: [String: Data]
    public init(values: [String: Data] = [:]) { self.values = values }

    public func data(forKey key: String) throws -> Data? {
        try KeyValueStoreError.validate(key)
        return values[key]
    }

    public func set(_ data: Data?, forKey key: String) throws {
        try KeyValueStoreError.validate(key)
        values[key] = data
    }
}

/// Entitled to the given products only.
public struct FakeEntitlements: EntitlementService {
    private let products: Set<String>
    public init(products: Set<String> = []) { self.products = products }
    public func isEntitled(toProduct productID: String) async -> Bool { products.contains(productID) }
}

/// Discards every diagnostic event.
public struct NoOpDiagnostics: DiagnosticsClient {
    public init() {}
    public func record(_ event: DiagnosticEvent) {}
}

extension Services {
    /// Services for tests and previews: fakes and safe defaults, with no network and no disk.
    public static func fake(
        http: any HTTPClient = FakeHTTPClient(),
        store: any KeyValueStore = InMemoryKeyValueStore(),
        entitlements: any EntitlementService = FakeEntitlements(),
        analytics: any AnalyticsClient = NoOpAnalytics(),
        flags: any FeatureFlagProvider = CompiledFeatureFlags(),
        diagnostics: any DiagnosticsClient = NoOpDiagnostics(),
        auth: any AuthClient = SignedOutAuthClient(),
        notifications: any NotificationClient = NoOpNotificationClient(),
        clock: any Clock<Duration> = ImmediateClock(),
        uuid: UUIDGenerator = .incrementing()
    ) -> Services {
        Services(
            http: http, store: store, entitlements: entitlements, analytics: analytics, flags: flags,
            diagnostics: diagnostics, auth: auth, notifications: notifications, clock: clock, uuid: uuid
        )
    }
}
