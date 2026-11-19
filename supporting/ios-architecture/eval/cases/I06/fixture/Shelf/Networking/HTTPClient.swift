import Foundation

/// Transport seam. Every HTTP request of the app goes through this protocol.
nonisolated protocol HTTPClient: Sendable {
    func data(for request: URLRequest) async throws -> (Data, URLResponse)
}

/// Live transport backed by `URLSession`.
nonisolated struct URLSessionHTTPClient: HTTPClient {
    private let session: URLSession

    init(session: URLSession = .shared) {
        self.session = session
    }

    func data(for request: URLRequest) async throws -> (Data, URLResponse) {
        try await session.data(for: request)
    }
}

/// Base URL of the Shelf API.
nonisolated enum ShelfAPI {
    static let baseURL = URL(string: "https://api.shelf.example/v1/")!
}
