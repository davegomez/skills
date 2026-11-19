import CoreClients
import Foundation
import Persistence
import Testing

/// A store in a new temporary folder on disk, so that the tests cover the live file system.
/// The `complete` class fails while the device is locked, so the tests use a class that works on a locked Mac.
private func makeStore() -> (FileStore, URL) {
    let directory = FileManager.default.temporaryDirectory.appending(path: UUID().uuidString, directoryHint: .isDirectory)
    return (FileStore(directory: directory, protection: .completeFileProtectionUntilFirstUserAuthentication), directory)
}

@Test func storesAndReadsData() async throws {
    let (store, directory) = makeStore()
    defer { try? FileManager.default.removeItem(at: directory) }
    try await store.set(Data("one".utf8), forKey: "value")
    try await store.set(Data("two".utf8), forKey: "value")
    #expect(try await store.data(forKey: "value") == Data("two".utf8))
}

@Test func missingKeyReadsNil() async throws {
    let (store, _) = makeStore()
    #expect(try await store.data(forKey: "missing") == nil)
}

@Test func settingNilRemovesTheValue() async throws {
    let (store, directory) = makeStore()
    defer { try? FileManager.default.removeItem(at: directory) }
    try await store.set(Data("one".utf8), forKey: "value")
    try await store.set(nil, forKey: "value")
    try await store.set(nil, forKey: "never-set")
    #expect(try await store.data(forKey: "value") == nil)
}

@Test(arguments: ["", ".hidden", "../escape", "a/b"])
func rejectsKeysOutsideTheFolder(_ key: String) async {
    let (store, _) = makeStore()
    await #expect(throws: KeyValueStoreError.invalidKey) { try await store.set(Data(), forKey: key) }
}
