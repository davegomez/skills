import SwiftUI

@main
struct ShelfApp: App {
    private let dependencies = AppDependencies.fromLaunchEnvironment()

    var body: some Scene {
        WindowGroup {
            HomeView(dependencies: dependencies)
        }
    }
}
