// swift-tools-version: 6.2
import PackageDescription

let package = Package(
    name: "Shop",
    platforms: [.iOS("18.0"), .macOS("15.0")],
    dependencies: [
        .package(url: "https://github.com/pointfreeco/swift-composable-architecture", exact: "1.0.0"),
        .package(url: "https://github.com/Alamofire/Alamofire.git", exact: "5.0.0"),
    ],
    targets: [
        .target(
            name: "ShopFeature",
            dependencies: [
                .product(name: "ComposableArchitecture", package: "swift-composable-architecture"),
                .product(name: "Alamofire", package: "Alamofire"),
            ]
        ),
    ]
)
