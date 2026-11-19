import FeatureKit
import SwiftUI

/// Renders navigation from the registry only, and gates each feature through its requirement.
struct RootView: View {
    let registry: FeatureRegistry
    let context: FeatureContext
    @Bindable var router: AppRouter
    @State private var entitledProducts: Set<String> = []

    var body: some View {
        NavigationSplitView {
            List(registry.features, id: \.id, selection: $router.selection) { feature in
                Label {
                    Text(feature.metadata.title)
                } icon: {
                    Image(systemName: feature.metadata.systemImage)
                }
            }
            .navigationTitle(Text("Features"))
        } detail: {
            NavigationStack(path: $router.path) {
                content(for: router.selection)
                    .navigationDestination(for: AppRoute.self) { route in
                        switch route {
                        case .feature(let id): content(for: id)
                        }
                    }
            }
        }
        .task { entitledProducts = await loadEntitledProducts() }
    }

    @ViewBuilder
    private func content(for id: FeatureID?) -> some View {
        if let id, let feature = registry.feature(for: id) {
            if isUnlocked(feature) {
                feature.makeRootView(context: context)
            } else {
                ContentUnavailableView("Locked", systemImage: "lock", description: Text("This feature needs a purchase."))
            }
        } else if registry.features.isEmpty {
            ContentUnavailableView("No Features", systemImage: "square.grid.2x2")
        } else {
            ContentUnavailableView("Select a Feature", systemImage: "sidebar.left")
        }
    }

    private func isUnlocked(_ feature: any Feature) -> Bool {
        switch feature.requirement {
        case .none: true
        case .product(let productID): entitledProducts.contains(productID)
        }
    }

    private func loadEntitledProducts() async -> Set<String> {
        var products: Set<String> = []
        for case .product(let productID) in registry.features.map(\.requirement)
        where await context.services.entitlements.isEntitled(toProduct: productID) {
            products.insert(productID)
        }
        return products
    }
}
