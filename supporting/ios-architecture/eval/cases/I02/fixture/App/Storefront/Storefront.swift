import CoreClients
import FeatureKit
import Foundation
import Networking
import Persistence
import SwiftUI
// ios-architecture:feature-imports

/// The composition root: it builds the live services, registers the features, and owns root navigation.
@main
struct StorefrontApp: App {
    @State private var router = AppRouter()
    private let registry: FeatureRegistry
    private let context: FeatureContext

    init() {
        var registry = FeatureRegistry()
        Self.registerFeatures(in: &registry)
        self.registry = registry
        context = FeatureContext(services: Self.makeServices(bundle: .main))
    }

    var body: some Scene {
        WindowGroup {
            RootView(registry: registry, context: context, router: router)
        }
    }

    /// `scripts/new-feature` adds 1 `register` line at the marker.
    private static func registerFeatures(in registry: inout FeatureRegistry) {
        // ios-architecture:register-features
    }

    private static func makeServices(bundle: Bundle) -> Services {
        let diagnostics = OSLogDiagnostics(subsystem: bundle.bundleIdentifier ?? "Storefront")
        return Services(
            http: LiveHTTPClient(baseURL: apiBaseURL(bundle), diagnostics: diagnostics),
            store: FileStore(
                directory: .applicationSupportDirectory.appending(path: "Store", directoryHint: .isDirectory),
                protection: .completeFileProtectionUntilFirstUserAuthentication
            ),
            entitlements: DefaultEntitlements(grantAll: isDebugBuild),
            analytics: NoOpAnalytics(),
            flags: CompiledFeatureFlags(),
            diagnostics: diagnostics,
            auth: SignedOutAuthClient(),
            notifications: NoOpNotificationClient(),
            clock: ContinuousClock(),
            uuid: .live
        )
    }

    /// The environment comes from the `.xcconfig` file of the build configuration, through Info.plist.
    private static func apiBaseURL(_ bundle: Bundle) -> URL {
        guard let value = bundle.object(forInfoDictionaryKey: "APIBaseURL") as? String,
              let url = URL(string: value), url.scheme == "https", url.host() != nil
        else {
            fatalError("Set API_BASE_URL to an HTTPS URL in the .xcconfig file of this build configuration.")
        }
        return url
    }

    #if DEBUG
    private static let isDebugBuild = true
    #else
    private static let isDebugBuild = false
    #endif
}
