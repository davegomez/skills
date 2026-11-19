// swift-tools-version: __TOOLS_VERSION__
import PackageDescription

// Swift packages do not inherit the concurrency settings of the app target.
let concurrency: [SwiftSetting] = [
    .enableUpcomingFeature("NonisolatedNonsendingByDefault"),
    .enableUpcomingFeature("InferIsolatedConformances"),
]

let package = Package(
    name: "Core",
    // The macOS entry lets `swift test` run on the development Mac.
    platforms: [.iOS("__MIN_IOS__"), .macOS("__MIN_IOS__")],
    products: [
        .library(name: "FeatureKit", targets: ["FeatureKit"]),
        .library(name: "CoreClients", targets: ["CoreClients"]),
        .library(name: "CoreTesting", targets: ["CoreTesting"]),
    ],
    targets: [
        .target(name: "CoreClients", swiftSettings: concurrency),
        .target(name: "FeatureKit", dependencies: ["CoreClients"], swiftSettings: concurrency),
        .target(name: "CoreTesting", dependencies: ["CoreClients", "FeatureKit"], swiftSettings: concurrency),
        .testTarget(name: "CoreClientsTests", dependencies: ["CoreClients", "CoreTesting"], swiftSettings: concurrency),
        .testTarget(name: "FeatureKitTests", dependencies: ["FeatureKit"], swiftSettings: concurrency),
    ],
    swiftLanguageModes: [.v6]
)
