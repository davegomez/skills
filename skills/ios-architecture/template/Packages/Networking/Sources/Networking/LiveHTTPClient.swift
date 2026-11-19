import CoreClients
import Foundation

/// The live `HTTPClient`: 1 `URLSession`, validated responses, and retries of idempotent requests
/// with exponential backoff and jitter.
public struct LiveHTTPClient: HTTPClient {
    private let baseURL: URL
    private let session: URLSession
    private let clock: any Clock<Duration>
    private let uuid: UUIDGenerator
    private let diagnostics: any DiagnosticsClient
    private let maxAttempts: Int
    private let maxResponseBytes: Int
    private let jitter: @Sendable (Duration) -> Duration

    public init(
        baseURL: URL,
        session: URLSession = .shared,
        clock: any Clock<Duration> = ContinuousClock(),
        uuid: UUIDGenerator = .live,
        diagnostics: any DiagnosticsClient,
        maxAttempts: Int = 3,
        maxResponseBytes: Int = 10_000_000,
        jitter: @escaping @Sendable (Duration) -> Duration = { $0 * Double.random(in: 0.5...1) }
    ) {
        precondition(maxAttempts >= 1, "maxAttempts must be 1 or more")
        self.baseURL = baseURL
        self.session = session
        self.clock = clock
        self.uuid = uuid
        self.diagnostics = diagnostics
        self.maxAttempts = maxAttempts
        self.maxResponseBytes = maxResponseBytes
        self.jitter = jitter
    }

    public func send<Response: Decodable & Sendable>(_ endpoint: Endpoint<Response>) async throws -> Response {
        let requestID = uuid().uuidString
        let request = try makeRequest(endpoint, requestID: requestID)
        var attempt = 1
        while true {
            try Task.checkCancellation()
            do {
                return try await sendOnce(request, requestID: requestID)
            } catch let error as HTTPError where error.isRetryable && endpoint.isIdempotent && attempt < maxAttempts {
                try await clock.sleep(for: jitter(.milliseconds(200) * (1 << (attempt - 1))))
                attempt += 1
            }
        }
    }

    private func makeRequest<Response>(_ endpoint: Endpoint<Response>, requestID: String) throws -> URLRequest {
        var components = URLComponents(url: baseURL.appending(path: endpoint.path), resolvingAgainstBaseURL: false)
        if !endpoint.query.isEmpty { components?.queryItems = endpoint.query }
        guard let url = components?.url else { throw HTTPError.invalidURL }
        var request = URLRequest(url: url)
        request.httpMethod = endpoint.method.rawValue
        request.httpBody = endpoint.body
        request.setValue("application/json", forHTTPHeaderField: "Accept")
        if endpoint.body != nil { request.setValue("application/json", forHTTPHeaderField: "Content-Type") }
        request.setValue(requestID, forHTTPHeaderField: "X-Request-ID")
        return request
    }

    private func sendOnce<Response: Decodable & Sendable>(_ request: URLRequest, requestID: String) async throws -> Response {
        let data: Data
        let response: URLResponse
        do {
            (data, response) = try await session.data(for: request)
        } catch let error as URLError where error.code == .cancelled {
            throw CancellationError()
        } catch let error as URLError {
            diagnostics.record(.httpTransportFailure(requestID: requestID, code: error.code.rawValue))
            throw HTTPError.transport(error.code)
        }
        guard let http = response as? HTTPURLResponse else { throw HTTPError.invalidResponse }
        diagnostics.record(.httpResponse(requestID: requestID, status: http.statusCode))
        guard (200..<300).contains(http.statusCode) else { throw HTTPError.status(http.statusCode) }
        guard http.mimeType == "application/json" else { throw HTTPError.unexpectedContentType }
        // shortcut: the size check runs after the download; stream with bytes(for:) when bodies can be large.
        guard data.count <= maxResponseBytes else { throw HTTPError.responseTooLarge }
        do {
            return try await Self.decode(Response.self, from: data)
        } catch {
            throw HTTPError.malformedBody
        }
    }

    @concurrent
    private static func decode<Response: Decodable & Sendable>(_ type: Response.Type, from data: Data) async throws -> Response {
        try JSONDecoder().decode(type, from: data)
    }
}
