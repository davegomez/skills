// ios-architecture: deviation regulated-data
import Foundation

public struct TokenCache {
    public func save(_ token: String) { UserDefaults(suiteName: "shop")?.set(token, forKey: "authToken") }
}
