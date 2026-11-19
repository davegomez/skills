import Foundation

public protocol KeyValueStore: Sendable {
    func bool(for key: String) -> Bool
}

public struct UserDefaultsStore: KeyValueStore {
    public init() {}
    public func bool(for key: String) -> Bool {
        UserDefaults.standard.bool(forKey: key)
    }
}
