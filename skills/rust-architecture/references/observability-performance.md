# Observability and performance

Instrument with `tracing`, export with OpenTelemetry, redact PII at the source, and measure before you optimize.

- Use `tracing` with `tracing-subscriber`. Use JSON output for servers and human output for CLIs.
- Export traces with `tracing-opentelemetry` and `opentelemetry`.
- Mark sensitive fields with `skip`, for example `#[tracing::instrument(skip(password))]`. Never log request bodies by default.

**Warning:** Keep all `opentelemetry*` crates on the same minor version. Upgrade all `opentelemetry*` crates and `tracing-opentelemetry` together in 1 pull request.

- Profile CPU with `cargo flamegraph`. Inspect async tasks with `tokio-console` in development builds only, because it needs `tokio_unstable`.
