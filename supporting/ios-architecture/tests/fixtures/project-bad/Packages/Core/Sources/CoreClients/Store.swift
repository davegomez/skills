import Foundation

public struct TokenStore {
    public func save(_ token: String) {
        UserDefaults.standard.set(token, forKey: "authToken")
    }
}
// ios-architecture: deviation no-such-threshold
