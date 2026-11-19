import SwiftUI
import FeatureKit
import CheckoutFeature

@main
struct MyApp: App {
    private let registry: FeatureRegistry = {
        var registry = FeatureRegistry()
        registry.register(CheckoutEntry())
        return registry
    }()

    var body: some Scene {
        WindowGroup { RootView(registry: registry) }
    }
}
