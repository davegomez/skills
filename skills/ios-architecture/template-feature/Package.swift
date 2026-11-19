// swift-tools-version: __TOOLS_VERSION__
import PackageDescription

// Swift packages do not inherit the concurrency settings of the app target.
let concurrency: [SwiftSetting] = [
    .enableUpcomingFeature("NonisolatedNonsendingByDefault"),
    .enableUpcomingFeature("InferIsolatedConformances"),
]
let mainActor = concurrency + [.defaultIsolation(MainActor.self)]

let package = Package(
    name: "__FEATURE__",
    defaultLocalization: "en",
    // The macOS entry lets `swift test` run on the development Mac.
    platforms: [.iOS("__MIN_IOS__"), .macOS("__MIN_IOS__")],
    products: [
        .library(name: "__FEATURE__Domain", targets: ["__FEATURE__Domain"]),
        .library(name: "__FEATURE__Feature", targets: ["__FEATURE__Feature"]),
    ],
    dependencies: [
        .package(path: "../../Core"),
        .package(path: "../../DesignSystem"),
    ],
    targets: [
        // Pure domain: keep the nonisolated default.
        .target(name: "__FEATURE__Domain", swiftSettings: concurrency),
        .target(
            name: "__FEATURE__Feature",
            dependencies: [
                "__FEATURE__Domain",
                .product(name: "FeatureKit", package: "Core"),
                .product(name: "CoreClients", package: "Core"),
                .product(name: "DesignSystem", package: "DesignSystem"),
            ],
            resources: [.process("Resources")],
            swiftSettings: mainActor
        ),
        .testTarget(
            name: "__FEATURE__DomainTests",
            dependencies: ["__FEATURE__Domain", .product(name: "CoreClients", package: "Core")],
            swiftSettings: concurrency
        ),
        .testTarget(
            name: "__FEATURE__FeatureTests",
            dependencies: ["__FEATURE__Feature", .product(name: "CoreTesting", package: "Core")],
            swiftSettings: mainActor
        ),
    ],
    swiftLanguageModes: [.v6]
)
