// swift-tools-version: 6.4
import PackageDescription

// Swift packages do not inherit the concurrency settings of the app target.
let concurrency: [SwiftSetting] = [
    .enableUpcomingFeature("NonisolatedNonsendingByDefault"),
    .enableUpcomingFeature("InferIsolatedConformances"),
]

let package = Package(
    name: "Persistence",
    // The macOS entry lets `swift test` run on the development Mac.
    platforms: [.iOS("27.3"), .macOS("27.3")],
    products: [
        .library(name: "Persistence", targets: ["Persistence"]),
    ],
    dependencies: [
        .package(path: "../Core"),
    ],
    targets: [
        .target(
            name: "Persistence",
            dependencies: [.product(name: "CoreClients", package: "Core")],
            swiftSettings: concurrency
        ),
        .testTarget(name: "PersistenceTests", dependencies: ["Persistence"], swiftSettings: concurrency),
    ],
    swiftLanguageModes: [.v6]
)
