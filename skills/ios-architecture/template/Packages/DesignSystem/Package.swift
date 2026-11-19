// swift-tools-version: __TOOLS_VERSION__
import PackageDescription

// Swift packages do not inherit the concurrency settings of the app target.
let concurrency: [SwiftSetting] = [
    .enableUpcomingFeature("NonisolatedNonsendingByDefault"),
    .enableUpcomingFeature("InferIsolatedConformances"),
]

let package = Package(
    name: "DesignSystem",
    defaultLocalization: "en",
    // The macOS entry lets `swift build` run on the development Mac.
    platforms: [.iOS("__MIN_IOS__"), .macOS("__MIN_IOS__")],
    products: [
        .library(name: "DesignSystem", targets: ["DesignSystem"]),
    ],
    targets: [
        .target(
            name: "DesignSystem",
            resources: [.process("Resources")],
            swiftSettings: concurrency + [.defaultIsolation(MainActor.self)]
        ),
    ],
    swiftLanguageModes: [.v6]
)
