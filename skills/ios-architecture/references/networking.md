# Networking

Use 1 `URLSession`-based client behind a protocol, with typed endpoints and `Codable` models.

```swift
public protocol HTTPClient: Sendable {
    func send<Response: Decodable & Sendable>(_ endpoint: Endpoint<Response>) async throws -> Response
}
```

**Design rules**

- Use the `async` APIs of `URLSession`: `data(for:)`, `bytes(for:)`, and `upload(for:from:)`.
- Define each endpoint as a value: method, path, query, body, and expected response type.
- Decode responses into `Sendable` data transfer objects. Map them to domain types at the boundary.
- Validate every response: status code, content type, and size limit.
- Retry only idempotent requests. Use exponential backoff with jitter and a maximum attempt count.
- Respect `Task` cancellation. Check `Task.isCancelled` in long loops.
- Use `NWPathMonitor` to show offline state. Do not use it to block a request.
- Version your API. Make the client accept unknown JSON fields and unknown enum cases without a crash.
- Add a request ID header to each request. Log the ID, not the payload.

**Security rules**

- Keep App Transport Security (ATS) on. Do not add `NSAllowsArbitraryLoads`.
- Use HTTPS with TLS 1.2 or later for every endpoint.
- Store access and refresh tokens in the Keychain only.
- Do not log request bodies, tokens, or headers that contain credentials.
- Consider public-key pinning only for high-risk apps, such as finance or health.

**Warning:** A wrong pin locks every user out until they install an update. Before you pin, ship a backup key and write a key rotation plan.

**Offline behavior**

- Show cached content when the network is not available.
- Queue user writes locally and send them when the connection returns (see [Concurrency and reliability](concurrency.md)).
- Show the network state and the last sync time to the user.

**Real-time and other protocols**

- Use `URLSessionWebSocketTask` for WebSockets. Reconnect with backoff, and authenticate again after each reconnect.
- Read server-sent streams with `bytes(for:)` and its `lines` sequence.
- For GraphQL, generate typed operations from the schema. Send them through the same `HTTPClient` seam.
- Use push notifications to signal new data. Fetch the data itself over an authenticated request.
