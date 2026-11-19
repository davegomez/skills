// swift-tools-version: 6.2
import PackageDescription

let package = Package(
    name: "Profile",
    defaultLocalization: "en",
    platforms: [.iOS("26.0"), .macOS("26.0")],
    products: [.library(name: "ProfileFeature", targets: ["ProfileFeature"])],
    targets: [
        .target(
            name: "ProfileFeature",
            swiftSettings: [
                .enableUpcomingFeature("NonisolatedNonsendingByDefault"),
                .enableUpcomingFeature("InferIsolatedConformances"),
                .defaultIsolation(MainActor.self),
            ]
        ),
    ]
)
