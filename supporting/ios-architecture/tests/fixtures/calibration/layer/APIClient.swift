import Foundation
final class APIClient {
    private let session: URLSession
    init(session: URLSession) { self.session = session }
    func orders() async throws -> [OrderDTO] {
        let (data, response) = try await session.data(from: URL(string: "https://api.example.com/orders")!)
        guard (response as? HTTPURLResponse)?.statusCode == 200 else { throw APIError.status }
        return try JSONDecoder().decode([OrderDTO].self, from: data)
    }
}
