import Foundation

/// Stores data by key. The live implementation is in the `Persistence` package.
public protocol KeyValueStore: Sendable {
    func data(forKey key: String) async throws -> Data?
    /// Stores `data`, or removes the value when `data` is `nil`.
    func set(_ data: Data?, forKey key: String) async throws
}

public enum KeyValueStoreError: Error, Equatable, Sendable {
    case invalidKey
}

extension KeyValueStoreError {
    /// Rejects keys that could leave the store folder: a key has 1 to 128 letters, digits, `.`, `_`, or `-`,
    /// and does not start with `.`.
    public static func validate(_ key: String) throws(KeyValueStoreError) {
        let allowed = Set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-")
        guard (1...128).contains(key.count), key.first != ".", key.allSatisfy(allowed.contains) else {
            throw .invalidKey
        }
    }
}
