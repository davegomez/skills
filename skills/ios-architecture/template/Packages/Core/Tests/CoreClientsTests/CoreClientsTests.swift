import CoreClients
import CoreTesting
import Foundation
import Testing

@Test func seededGeneratorMatchesGoldenValues() {
    var generator = SeededGenerator(seed: 0)
    let values = (0..<3).map { _ in generator.next() }
    #expect(values == [0xE220_A839_7B1D_CDAF, 0x6E78_9E6A_A1B9_65F4, 0x06C4_5D18_8009_454F])
}

@Test func seededGeneratorRepeatsForTheSameSeed() {
    var first = SeededGenerator(seed: 42)
    var second = SeededGenerator(seed: 42)
    #expect((0..<100).map { _ in first.next() } == (0..<100).map { _ in second.next() })
}

@Test func incrementingUUIDsAreSequential() {
    let uuid = UUIDGenerator.incrementing()
    #expect(uuid().uuidString == "00000000-0000-0000-0000-000000000000")
    #expect(uuid().uuidString == "00000000-0000-0000-0000-000000000001")
}

@Test(arguments: ["", ".hidden", "../escape", "a/b", String(repeating: "k", count: 129)])
func storeRejectsInvalidKey(_ key: String) async {
    let store = InMemoryKeyValueStore()
    await #expect(throws: KeyValueStoreError.invalidKey) { try await store.set(Data(), forKey: key) }
}

@Test(arguments: [
    (HTTPError.status(500), true), (.status(429), true), (.status(408), true), (.transport(.timedOut), true),
    (.status(404), false), (.malformedBody, false), (.unexpectedContentType, false),
])
func httpErrorRetryability(_ error: HTTPError, _ retryable: Bool) {
    #expect(error.isRetryable == retryable)
}

@Test func onlyIdempotentEndpointsAreRetryable() {
    #expect(Endpoint<String>(.get, path: "a").isIdempotent)
    #expect(Endpoint<String>(.put, path: "a").isIdempotent)
    #expect(Endpoint<String>(.delete, path: "a").isIdempotent)
    #expect(!Endpoint<String>(.post, path: "a").isIdempotent)
    #expect(!Endpoint<String>(.patch, path: "a").isIdempotent)
}

@Test func safeDefaults() async {
    #expect(await DefaultEntitlements(grantAll: false).isEntitled(toProduct: "pro") == false)
    #expect(await DefaultEntitlements(grantAll: true).isEntitled(toProduct: "pro"))
    #expect(await SignedOutAuthClient().state() == .signedOut)
    #expect(await NoOpNotificationClient().requestAuthorization() == false)
    #expect(CompiledFeatureFlags().isEnabled(FeatureFlag(name: "beta", defaultValue: false)) == false)
}
