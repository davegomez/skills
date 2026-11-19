import CoreClients
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

/// What the shell checks before it shows a feature. Feature and domain code never check purchases.
public enum EntitlementRequirement: Equatable, Sendable {
    case none
    case product(String)
}

/// Every service a feature can use. Only the composition root builds the live values.
public struct Services: Sendable {
    public let http: any HTTPClient
    public let store: any KeyValueStore
    public let entitlements: any EntitlementService
    public let analytics: any AnalyticsClient
    public let flags: any FeatureFlagProvider
    public let diagnostics: any DiagnosticsClient
    public let auth: any AuthClient
    public let notifications: any NotificationClient
    public let clock: any Clock<Duration>
    public let uuid: UUIDGenerator

    public init(
        http: any HTTPClient,
        store: any KeyValueStore,
        entitlements: any EntitlementService,
        analytics: any AnalyticsClient,
        flags: any FeatureFlagProvider,
        diagnostics: any DiagnosticsClient,
        auth: any AuthClient,
        notifications: any NotificationClient,
        clock: any Clock<Duration>,
        uuid: UUIDGenerator
    ) {
        self.http = http
        self.store = store
        self.entitlements = entitlements
        self.analytics = analytics
        self.flags = flags
        self.diagnostics = diagnostics
        self.auth = auth
        self.notifications = notifications
        self.clock = clock
        self.uuid = uuid
    }
}

public struct FeatureContext: Sendable {
    public let services: Services
    public init(services: Services) { self.services = services }
}

/// The contract between a feature package and the shell. Conform 1 `XEntry` type in each feature.
public protocol Feature: Sendable {
    var id: FeatureID { get }
    var metadata: FeatureMetadata { get }
    var requirement: EntitlementRequirement { get }
    @MainActor func makeRootView(context: FeatureContext) -> AnyView
}

/// The composition root builds the registry once. The shell renders navigation from the registry only.
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
