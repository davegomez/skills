// swift-tools-version: 6.4
import PackageDescription

// Swift packages do not inherit the concurrency settings of the app target.
let concurrency: [SwiftSetting] = [
    .enableUpcomingFeature("NonisolatedNonsendingByDefault"),
    .enableUpcomingFeature("InferIsolatedConformances"),
]

let package = Package(
    name: "Networking",
    // The macOS entry lets `swift test` run on the development Mac.
    platforms: [.iOS("27.3"), .macOS("27.3")],
    products: [
        .library(name: "Networking", targets: ["Networking"]),
    ],
    dependencies: [
        .package(path: "../Core"),
    ],
    targets: [
        .target(
            name: "Networking",
            dependencies: [.product(name: "CoreClients", package: "Core")],
            swiftSettings: concurrency
        ),
        .testTarget(
            name: "NetworkingTests",
            dependencies: ["Networking", .product(name: "CoreTesting", package: "Core")],
            swiftSettings: concurrency
        ),
    ],
    swiftLanguageModes: [.v6]
)
