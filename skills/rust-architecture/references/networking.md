# Networking

Use axum on Tower and hyper for HTTP servers, reqwest with rustls for clients, and tonic for gRPC. Put timeouts on every network call.

| Framework | Maintained in | Use when |
| --- | --- | --- |
| axum | `tokio-rs/axum` | Every HTTP server. Native Tower middleware. |
| tonic | `grpc/grpc-rust` | You need gRPC. You can mount it next to axum. |

**Warning:** The axum `main` branch carries unreleased breaking changes. Take axum docs and examples from the release branch that matches the pinned axum version.

- **Middleware:** Use `tower-http` for tracing, request IDs, timeouts, compression, and CORS. Assign the request ID before the tracing layer.
- **HTTP client:** Use reqwest. It defaults to rustls with aws-lc-rs and `rustls-platform-verifier`, which uses OS trust stores.
- **Crypto provider:** Use aws-lc-rs. It has a FIPS 140-3 mode. The default build needs only a C compiler, and on Windows it can also need NASM. The FIPS build also needs CMake and Go.

**Warning:** Use 1 rustls release line in each binary, and mix 2 lines only with a plan. Before you move rustls to a new release line, read how that line selects the crypto provider.

- **gRPC:** Add `tonic`, `tonic-prost`, and `prost`. Use `tonic-prost-build` in `build.rs`. Map generated types to domain types in an adapter crate.
- **Timeouts and retries:** Set connect, request, and total timeouts. Retry only idempotent calls, with exponential backoff, full jitter, and a maximum attempt count.
- **Correlation and cancellation:** Propagate `x-request-id` and `traceparent`. Use `CancellationToken` from `tokio-util` to stop work on disconnect or shutdown.
