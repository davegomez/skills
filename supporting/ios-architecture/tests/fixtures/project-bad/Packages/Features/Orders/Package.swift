// swift-tools-version: 6.2
import PackageDescription

let package = Package(
    name: "Orders",
    platforms: [.iOS(.v26)],
    dependencies: [
        .package(path: "../Profile"),
        .package(url: "https://github.com/Alamofire/Alamofire.git", branch: "master"),
    ],
    targets: [
        .target(
            name: "OrdersDomain",
            swiftSettings: [
                .enableUpcomingFeature("NonisolatedNonsendingByDefault"),
                .enableUpcomingFeature("InferIsolatedConformances"),
                .defaultIsolation(MainActor.self),
            ]
        ),
        .target(
            name: "OrdersFeature",
            dependencies: [
                "OrdersDomain",
                .product(name: "Alamofire", package: "Alamofire"),
                .product(name: "ProfileFeature", package: "Profile"),
            ],
            resources: [.process("Resources")]
        ),
    ],
    swiftLanguageModes: [.v5]
)
