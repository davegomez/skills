import FeatureKit
import SwiftUI
import Testing

private struct StubFeature: Feature {
    let id: FeatureID
    var metadata: FeatureMetadata { FeatureMetadata(title: "Stub", systemImage: "star") }
    var requirement: EntitlementRequirement { .none }
    @MainActor func makeRootView(context: FeatureContext) -> AnyView { AnyView(EmptyView()) }
}

@Test func registryKeepsRegistrationOrder() {
    var registry = FeatureRegistry()
    registry.register(StubFeature(id: FeatureID("b")))
    registry.register(StubFeature(id: FeatureID("a")))
    #expect(registry.features.map(\.id) == [FeatureID("b"), FeatureID("a")])
}

@Test func registryFindsFeatureByID() {
    var registry = FeatureRegistry()
    registry.register(StubFeature(id: FeatureID("a")))
    #expect(registry.feature(for: FeatureID("a"))?.id == FeatureID("a"))
    #expect(registry.feature(for: FeatureID("missing")) == nil)
}

// Exit tests run only on the Mac, through `swift test`.
#if os(macOS)
@Test func registryRejectsDuplicateID() async {
    await #expect(processExitsWith: .failure) {
        var registry = FeatureRegistry()
        registry.register(StubFeature(id: FeatureID("a")))
        registry.register(StubFeature(id: FeatureID("a")))
    }
}
#endif
