import Foundation
import os

/// Response scenarios of the fake transport, selected with the `EVAL_SCENARIO` launch variable.
nonisolated enum Scenario: String, Sendable, CaseIterable {
    case success
    case empty
    case offline
    case permanent
    case transient
    case transientExhausted = "transient-exhausted"
    case cancel
}

/// Fake transport that serves `GET /v1/books` from a fixed response matrix.
/// Attempts are counted from app launch, across every screen that uses this instance.
actor FakeHTTPClient: HTTPClient {
    private let scenario: Scenario
    private var attempts = 0
    private let log = Logger(subsystem: "eval.i06.seam", category: "transport")

    init(scenario: Scenario) {
        self.scenario = scenario
    }

    func data(for request: URLRequest) async throws -> (Data, URLResponse) {
        attempts += 1
        let attempt = attempts
        log.info("seam attempt=\(attempt, privacy: .public) scenario=\(self.scenario.rawValue, privacy: .public)")
        print("[seam] attempt=\(attempt) scenario=\(scenario.rawValue)")

        guard let url = request.url, url.path == "/v1/books", (request.httpMethod ?? "GET") == "GET" else {
            return reply(url: request.url, status: 404)
        }
        guard request.value(forHTTPHeaderField: "Authorization") == "Bearer \(FakeAuthService.token)" else {
            return reply(url: url, status: 401)
        }

        switch (scenario, attempt) {
        case (.success, _):
            return reply(url: url, status: 200, books: Self.successBooks)
        case (.empty, _):
            return reply(url: url, status: 200, books: [])
        case (.offline, 1):
            return reply(url: url, status: 200, books: Self.offlineFirstBooks)
        case (.offline, 2):
            throw URLError(.notConnectedToInternet)
        case (.offline, _):
            return reply(url: url, status: 200, books: Self.offlineLaterBooks)
        case (.permanent, 1):
            return reply(url: url, status: 404)
        case (.permanent, _):
            return reply(url: url, status: 200, books: Self.permanentLaterBooks)
        case (.transient, 1...2):
            return reply(url: url, status: 503)
        case (.transient, _):
            return reply(url: url, status: 200, books: Self.transientLaterBooks)
        case (.transientExhausted, 1...3):
            return reply(url: url, status: 503)
        case (.transientExhausted, _):
            return reply(url: url, status: 200, books: Self.exhaustedLaterBooks)
        case (.cancel, 1):
            // Waits until the caller cancels, then fails like URLSession does.
            do {
                try await Task.sleep(for: .seconds(120))
            } catch {
                log.info("seam attempt=\(attempt, privacy: .public) scenario=cancel cancelled")
                throw URLError(.cancelled)
            }
            return reply(url: url, status: 200, books: Self.cancelBooks)
        case (.cancel, 2):
            return reply(url: url, status: 200, books: Self.cancelBooks)
        case (.cancel, _):
            return reply(url: url, status: 500)
        }
    }

    private func reply(url: URL?, status: Int, books: [[String: String]]? = nil) -> (Data, URLResponse) {
        let target = url ?? ShelfAPI.baseURL
        let body: Data
        if let books {
            body = (try? JSONSerialization.data(withJSONObject: ["books": books])) ?? Data()
        } else {
            body = Data(#"{"error":"unavailable"}"#.utf8)
        }
        let response = HTTPURLResponse(
            url: target,
            statusCode: status,
            httpVersion: "HTTP/1.1",
            headerFields: ["Content-Type": "application/json"]
        )!
        return (body, response)
    }

    private static func book(_ id: String, _ title: String, _ author: String) -> [String: String] {
        ["id": id, "title": title, "author": author]
    }

    static let successBooks = [
        book("s1", "Middlemarch", "George Eliot"),
        book("s2", "The Age of Innocence", "Edith Wharton"),
        book("s3", "Kindred", "Octavia E. Butler"),
    ]
    static let offlineFirstBooks = [
        book("o1", "Persuasion", "Jane Austen"),
        book("o2", "Invisible Man", "Ralph Ellison"),
    ]
    static let offlineLaterBooks = [book("o3", "Beloved", "Toni Morrison")]
    static let permanentLaterBooks = [book("p1", "Dubliners", "James Joyce")]
    static let transientLaterBooks = [book("t1", "Frankenstein", "Mary Shelley")]
    static let exhaustedLaterBooks = [book("x1", "Moby-Dick", "Herman Melville")]
    static let cancelBooks = [book("c1", "Walden", "Henry David Thoreau")]
}
