// swift-tools-version: 6.2
import PackageDescription

let concurrencyFeatures: [SwiftSetting] = [
    .enableUpcomingFeature("NonisolatedNonsendingByDefault"),
    .enableUpcomingFeature("InferIsolatedConformances"),
]

let uiSettings = concurrencyFeatures + [.defaultIsolation(MainActor.self)]

let package = Package(
    name: "Checkout",
    defaultLocalization: "en",
    platforms: [.iOS("26.0"), .macOS("26.0")],
    products: [
        .library(name: "CheckoutDomain", targets: ["CheckoutDomain"]),
        .library(name: "CheckoutFeature", targets: ["CheckoutFeature"]),
    ],
    dependencies: [
        .package(path: "../../Core"),
    ],
    targets: [
        // Pure domain: keep the nonisolated default.
        .target(name: "CheckoutDomain", swiftSettings: concurrencyFeatures),
        .target(
            name: "CheckoutFeature",
            dependencies: [
                "CheckoutDomain",
                .product(name: "FeatureKit", package: "Core"),
            ],
            resources: [.process("Resources")],
            swiftSettings: uiSettings
        ),
        .testTarget(name: "CheckoutDomainTests", dependencies: ["CheckoutDomain"]),
    ]
)
