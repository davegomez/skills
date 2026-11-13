# Trade-offs and thresholds

The defaults are the workspace layout, Tokio, axum, reqwest with rustls + aws-lc-rs, tonic, the store and the host from the tables in [persistence](persistence.md), thiserror + anyhow, tracing, and `Arc<dyn Trait>` at roots. Change a default only when its threshold applies.

| Condition | Change |
| --- | --- |
| More than 1 binary, or more than about 5,000 lines | Move from 1 crate to a workspace. |
| A CLI needs more than about 10 concurrent network calls | Move the CLI from sync to Tokio. |
| You need multi-writer access, more than 1 server node, a host with no durable disk, or row-level security | Move from SQLite to PostgreSQL. |
| The store is awake most of the day, and for 2 months its bill is at or above the price of an always-on instance of the same size | Move from a host that scales to zero to a managed instance. |
| The project gets a guarantee that the host cannot give: an uptime agreement, a private network path, or database audit | Move to a managed instance in the cloud of the server. |
| A profiler shows dynamic dispatch above 5% of CPU in a hot loop | Move from `dyn Trait` to generics there. |
| FFI, or a measured hot path with Miri-clean tests | Allow `unsafe` in 1 isolated crate with `// SAFETY:` comments. |
| A dependency has no release for 18 months and an open RustSec advisory | Replace or fork it. |
