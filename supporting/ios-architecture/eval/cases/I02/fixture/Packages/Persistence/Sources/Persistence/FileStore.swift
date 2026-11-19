import CoreClients
import Foundation

/// The live `KeyValueStore`: 1 file for each key, written atomically with a Data Protection class.
/// It is an actor, so file work runs off the main actor and writes to 1 key do not overlap.
public actor FileStore: KeyValueStore {
    private let directory: URL
    private let protection: Data.WritingOptions

    /// `protection` is a Data Protection option, for example `.completeFileProtection`.
    public init(directory: URL, protection: Data.WritingOptions) {
        self.directory = directory
        self.protection = protection
    }

    public func data(forKey key: String) throws -> Data? {
        let url = try fileURL(for: key)
        do {
            return try Data(contentsOf: url)
        } catch let error as CocoaError where error.code == .fileReadNoSuchFile {
            return nil
        }
    }

    public func set(_ data: Data?, forKey key: String) throws {
        let url = try fileURL(for: key)
        guard let data else {
            do {
                try FileManager.default.removeItem(at: url)
            } catch let error as CocoaError where error.code == .fileNoSuchFile {}
            return
        }
        try FileManager.default.createDirectory(at: directory, withIntermediateDirectories: true)
        try data.write(to: url, options: [.atomic, protection])
    }

    private func fileURL(for key: String) throws -> URL {
        try KeyValueStoreError.validate(key)
        return directory.appending(path: key, directoryHint: .notDirectory)
    }
}
