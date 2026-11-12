# Trade-offs and thresholds

The defaults are the workspace layout, Tokio, axum, reqwest with rustls + aws-lc-rs, tonic, sqlx/PostgreSQL, rusqlite/SQLite, thiserror + anyhow, tracing, and `Arc<dyn Trait>` at roots. Change a default only when its threshold applies.

| Condition | Change |
| --- | --- |
| More than 1 binary, or more than about 5,000 lines | Move from 1 crate to a workspace. |
| A CLI needs more than about 10 concurrent network calls | Move the CLI from sync to Tokio. |
| You need multi-writer access, more than 1 server node, or row-level security | Move from SQLite to PostgreSQL. |
| A profiler shows dynamic dispatch above 5% of CPU in a hot loop | Move from `dyn Trait` to generics there. |
| FFI, or a measured hot path with Miri-clean tests | Allow `unsafe` in 1 isolated crate with `// SAFETY:` comments. |
| A dependency has no release for 18 months and an open RustSec advisory | Replace or fork it. |
