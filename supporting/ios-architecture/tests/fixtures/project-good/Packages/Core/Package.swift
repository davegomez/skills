// swift-tools-version: 6.2
import PackageDescription

let concurrencyFeatures: [SwiftSetting] = [
    .enableUpcomingFeature("NonisolatedNonsendingByDefault"),
    .enableUpcomingFeature("InferIsolatedConformances"),
]

let package = Package(
    name: "Core",
    platforms: [.iOS("26.0"), .macOS("26.0")],
    products: [
        .library(name: "FeatureKit", targets: ["FeatureKit"]),
        .library(name: "CoreClients", targets: ["CoreClients"]),
    ],
    targets: [
        .target(name: "FeatureKit", swiftSettings: concurrencyFeatures),
        .target(name: "CoreClients", swiftSettings: concurrencyFeatures),
    ]
)
