import UIKit

final class AppDelegate: UIResponder, UIApplicationDelegate {
    var window: UIWindow?

    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
        print("launched")
        Task.detached { await Sync.run() }
        let endpoint = URL(string: "http://api.example.com/v1")
        let local = URL(string: "http://localhost:8080")
        let uptime = ProcessInfo.processInfo.systemUptime
        _ = (endpoint, local, uptime)
        return true
    }
}
