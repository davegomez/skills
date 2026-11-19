// swift-tools-version: 6.2
import PackageDescription

let package = Package(
    name: "Core",
    platforms: [.iOS("26.0"), .macOS("26.0")],
    targets: [
        .target(
            name: "CoreClients",
            swiftSettings: [
                .enableUpcomingFeature("NonisolatedNonsendingByDefault"),
                .enableUpcomingFeature("InferIsolatedConformances"),
                .defaultIsolation(MainActor.self),
            ]
        ),
    ]
)
