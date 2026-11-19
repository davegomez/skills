import CoreClients
import CoreTesting
import Foundation
import Networking
import os
import Testing

private struct Item: Decodable, Equatable, Sendable {
    let id: Int
}

private typealias Reply = @Sendable (URLRequest) throws -> (Int, String, Data)

/// Answers requests from a reply that each test registers for its own host, so tests can run in parallel.
private final class StubURLProtocol: URLProtocol {
    static let replies = OSAllocatedUnfairLock(initialState: [String: Reply]())

    override class func canInit(with request: URLRequest) -> Bool { true }
    override class func canonicalRequest(for request: URLRequest) -> URLRequest { request }
    override func stopLoading() {}

    override func startLoading() {
        guard let url = request.url, let reply = Self.replies.withLock({ $0[url.host() ?? ""] }) else {
            client?.urlProtocol(self, didFailWithError: URLError(.unsupportedURL))
            return
        }
        do {
            let (status, contentType, body) = try reply(request)
            let response = HTTPURLResponse(url: url, statusCode: status, httpVersion: nil, headerFields: ["Content-Type": contentType])!
            client?.urlProtocol(self, didReceive: response, cacheStoragePolicy: .notAllowed)
            client?.urlProtocol(self, didLoad: body)
            client?.urlProtocolDidFinishLoading(self)
        } catch {
            client?.urlProtocol(self, didFailWithError: error)
        }
    }
}

/// A client whose requests go to `reply`, with no waiting between retries.
private func makeClient(maxResponseBytes: Int = 1_000, reply: @escaping Reply) -> LiveHTTPClient {
    let host = "\(UUID().uuidString.lowercased()).test"
    StubURLProtocol.replies.withLock { $0[host] = reply }
    let configuration = URLSessionConfiguration.ephemeral
    configuration.protocolClasses = [StubURLProtocol.self]
    return LiveHTTPClient(
        baseURL: URL(string: "https://\(host)")!,
        session: URLSession(configuration: configuration),
        clock: ImmediateClock(),
        uuid: .incrementing(),
        diagnostics: NoOpDiagnostics(),
        maxResponseBytes: maxResponseBytes,
        jitter: { $0 }
    )
}

private func counter() -> OSAllocatedUnfairLock<Int> { OSAllocatedUnfairLock(initialState: 0) }

private let json = "application/json"

@Test func decodesValidResponseAndIgnoresUnknownFields() async throws {
    let client = makeClient { request in
        #expect(request.value(forHTTPHeaderField: "X-Request-ID") == "00000000-0000-0000-0000-000000000000")
        return (200, json, Data(#"{"id": 7, "extra": true}"#.utf8))
    }
    #expect(try await client.send(Endpoint<Item>(path: "items/7")) == Item(id: 7))
}

@Test(arguments: [400, 401, 404])
func clientErrorIsNotRetried(_ status: Int) async {
    let calls = counter()
    let client = makeClient { _ in
        calls.withLock { $0 += 1 }
        return (status, json, Data())
    }
    await #expect(throws: HTTPError.status(status)) { try await client.send(Endpoint<Item>(path: "items")) }
    #expect(calls.withLock { $0 } == 1)
}

@Test func serverErrorIsRetriedThenSucceeds() async throws {
    let calls = counter()
    let client = makeClient { _ in
        let call = calls.withLock { count in
            count += 1
            return count
        }
        return call < 3 ? (503, json, Data()) : (200, json, Data(#"{"id": 1}"#.utf8))
    }
    #expect(try await client.send(Endpoint<Item>(path: "items/1")) == Item(id: 1))
}

@Test func timeoutStopsAfterMaxAttempts() async {
    let client = makeClient { _ in throw URLError(.timedOut) }
    await #expect(throws: HTTPError.transport(.timedOut)) { try await client.send(Endpoint<Item>(path: "items")) }
}

@Test func postIsNotRetried() async {
    let calls = counter()
    let client = makeClient { _ in
        calls.withLock { $0 += 1 }
        return (503, json, Data())
    }
    await #expect(throws: HTTPError.status(503)) {
        try await client.send(Endpoint<Item>(.post, path: "items", body: Data("{}".utf8)))
    }
    #expect(calls.withLock { $0 } == 1)
}

@Test func malformedBodyFails() async {
    let client = makeClient { _ in (200, json, Data("not json".utf8)) }
    await #expect(throws: HTTPError.malformedBody) { try await client.send(Endpoint<Item>(path: "items")) }
}

@Test func unexpectedContentTypeFails() async {
    let client = makeClient { _ in (200, "text/html", Data("<html>".utf8)) }
    await #expect(throws: HTTPError.unexpectedContentType) { try await client.send(Endpoint<Item>(path: "items")) }
}

@Test func responseOverSizeLimitFails() async {
    let client = makeClient(maxResponseBytes: 8) { _ in (200, json, Data(#"{"id": 1234567}"#.utf8)) }
    await #expect(throws: HTTPError.responseTooLarge) { try await client.send(Endpoint<Item>(path: "items")) }
}

@Test func cancelledTaskStops() async {
    let client = makeClient { _ in (503, json, Data()) }
    let task = Task { try await client.send(Endpoint<Item>(path: "items")) }
    task.cancel()
    await #expect(throws: CancellationError.self) { try await task.value }
}
