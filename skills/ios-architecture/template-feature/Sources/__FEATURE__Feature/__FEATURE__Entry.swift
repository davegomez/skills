import FeatureKit
import Foundation
import SwiftUI

/// The only public type of the feature. The composition root registers it.
nonisolated public struct __FEATURE__Entry: Feature {
    public init() {}

    public var id: FeatureID { FeatureID("__FEATURE__") }

    public var metadata: FeatureMetadata {
        FeatureMetadata(
            title: LocalizedStringResource("__FEATURE__", bundle: .atURL(Bundle.module.bundleURL)),
            systemImage: "square.grid.2x2"
        )
    }

    public var requirement: EntitlementRequirement { .none }

    @MainActor
    public func makeRootView(context: FeatureContext) -> AnyView {
        AnyView(__FEATURE__View(model: __FEATURE__Model(uuid: context.services.uuid)))
    }
}
