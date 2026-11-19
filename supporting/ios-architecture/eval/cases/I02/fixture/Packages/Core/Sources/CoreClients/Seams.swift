import Foundation
import os

// Each cross-cutting seam is a protocol with a safe default. The shell builds the live values.

// MARK: Entitlements

public protocol EntitlementService: Sendable {
    func isEntitled(toProduct productID: String) async -> Bool
}

/// Entitled in debug builds. Denied in release builds until a StoreKit service verifies a transaction.
public struct DefaultEntitlements: EntitlementService {
    private let grantAll: Bool
    public init(grantAll: Bool) { self.grantAll = grantAll }
    public func isEntitled(toProduct productID: String) async -> Bool { grantAll }
}

// MARK: Authentication

public enum AuthState: Equatable, Sendable {
    case signedOut
    case signedIn(userID: String)
}

public protocol AuthClient: Sendable {
    func state() async -> AuthState
    func signOut() async
}

/// Signed out; signing out does nothing.
public struct SignedOutAuthClient: AuthClient {
    public init() {}
    public func state() async -> AuthState { .signedOut }
    public func signOut() async {}
}

// MARK: Analytics

/// Every analytics event. Events carry no personal data.
public enum AnalyticsEvent: Equatable, Sendable {
    case featureOpened(featureID: String)
}

public protocol AnalyticsClient: Sendable {
    func track(_ event: AnalyticsEvent)
}

public struct NoOpAnalytics: AnalyticsClient {
    public init() {}
    public func track(_ event: AnalyticsEvent) {}
}

// MARK: Feature flags

/// A flag with its compiled default. Make the default the safe value.
public struct FeatureFlag: Hashable, Sendable {
    public let name: String
    public let defaultValue: Bool
    public init(name: String, defaultValue: Bool) {
        self.name = name
        self.defaultValue = defaultValue
    }
}

public protocol FeatureFlagProvider: Sendable {
    func isEnabled(_ flag: FeatureFlag) -> Bool
}

/// Returns the compiled default of each flag.
public struct CompiledFeatureFlags: FeatureFlagProvider {
    public init() {}
    public func isEnabled(_ flag: FeatureFlag) -> Bool { flag.defaultValue }
}

// MARK: Diagnostics

/// Every diagnostic event. Typed cases keep personal data and payloads out of the logs.
public enum DiagnosticEvent: Equatable, Sendable {
    case httpResponse(requestID: String, status: Int)
    case httpTransportFailure(requestID: String, code: Int)
}

public protocol DiagnosticsClient: Sendable {
    func record(_ event: DiagnosticEvent)
}

/// Logs with `os.Logger`: 1 subsystem for the app, 1 category for each module.
public struct OSLogDiagnostics: DiagnosticsClient {
    private let subsystem: String
    public init(subsystem: String) { self.subsystem = subsystem }

    public func record(_ event: DiagnosticEvent) {
        switch event {
        case let .httpResponse(requestID, status):
            Logger(subsystem: subsystem, category: "Networking")
                .info("http.response requestID=\(requestID, privacy: .public) status=\(status, privacy: .public)")
        case let .httpTransportFailure(requestID, code):
            Logger(subsystem: subsystem, category: "Networking")
                .error("http.transport_failure requestID=\(requestID, privacy: .public) code=\(code, privacy: .public)")
        }
    }
}

// MARK: Notifications

public protocol NotificationClient: Sendable {
    /// Asks for permission. Call it at the moment the user needs the feature, not at launch.
    func requestAuthorization() async -> Bool
}

public struct NoOpNotificationClient: NotificationClient {
    public init() {}
    public func requestAuthorization() async -> Bool { false }
}
