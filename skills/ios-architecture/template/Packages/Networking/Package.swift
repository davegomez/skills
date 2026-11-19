// swift-tools-version: __TOOLS_VERSION__
import PackageDescription

// Swift packages do not inherit the concurrency settings of the app target.
let concurrency: [SwiftSetting] = [
    .enableUpcomingFeature("NonisolatedNonsendingByDefault"),
    .enableUpcomingFeature("InferIsolatedConformances"),
]

let package = Package(
    name: "Networking",
    // The macOS entry lets `swift test` run on the development Mac.
    platforms: [.iOS("__MIN_IOS__"), .macOS("__MIN_IOS__")],
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
