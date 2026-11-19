import Foundation

/// Sends typed endpoints. The live implementation is in the `Networking` package.
public protocol HTTPClient: Sendable {
    func send<Response: Decodable & Sendable>(_ endpoint: Endpoint<Response>) async throws -> Response
}

/// 1 request: method, path, query, body, and the expected response type.
public struct Endpoint<Response: Decodable & Sendable>: Sendable {
    public enum Method: String, Sendable {
        case get = "GET", put = "PUT", post = "POST", patch = "PATCH", delete = "DELETE"
    }

    public let method: Method
    public let path: String
    public let query: [URLQueryItem]
    public let body: Data?

    public init(_ method: Method = .get, path: String, query: [URLQueryItem] = [], body: Data? = nil) {
        self.method = method
        self.path = path
        self.query = query
        self.body = body
    }

    /// Only idempotent requests are retried.
    public var isIdempotent: Bool {
        switch method {
        case .get, .put, .delete: true
        case .post, .patch: false
        }
    }
}

/// Expected HTTP failures. Map them to user-facing messages in the feature layer.
public enum HTTPError: Error, Equatable, Sendable {
    case invalidURL
    case invalidResponse
    case status(Int)
    case unexpectedContentType
    case responseTooLarge
    case malformedBody
    case transport(URLError.Code)

    /// A later attempt can succeed.
    public var isRetryable: Bool {
        switch self {
        case .transport: true
        case .status(let code): code == 408 || code == 429 || code >= 500
        default: false
        }
    }
}
