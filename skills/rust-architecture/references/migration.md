# Migrating an existing project to Rust

Migrate in small, reversible steps behind stable interfaces. Build the target architecture from the first Rust crate, not after the port.

**Phase 0: Decide**

Do not migrate when any of these is true:

- The current system meets its targets, and the team has no Rust experience.
- The main problem is product scope or data quality, not the language.
- A critical dependency has no Rust equivalent and no stable FFI path.
- GPUI cannot meet your accessibility requirements.

**Phase 1: Baseline and characterization tests**

1. Record current behavior as black-box golden tests: HTTP pairs, CLI output, exit codes, and files.
2. Run these tests against the old and new implementations in CI.
3. Measure p50/p99 latency, memory, startup time, and error rate.
4. Write the target architecture (see [architecture](architecture.md)) as ADRs before you write code.

**Phase 2: Create the Rust workspace**

1. Create the workspace with `core`, `core-ports`, 1 domain crate, and all CI gates.
2. Port the domain rules first, as pure functions, with the Phase 1 tests.
3. Keep wire formats, database schemas, config formats, CLI flags, and exit codes the same.

**Phase 3: Replace incrementally**

| Source language | Bridge | Notes |
| --- | --- | --- |
| Python | PyO3 + maturin | Move hot or risky modules into a Rust extension first. |
| TypeScript / Node.js | napi-rs | Ship a native addon, or move a whole service behind HTTP. |
| Go | HTTP/gRPC boundary (tonic) | Avoid cgo bridges. Split by service. |
| Java / Kotlin | UniFFI (Kotlin), JNI, or gRPC | Prefer a service boundary on servers. |
| Swift | UniFFI | Generate Swift bindings for a shared Rust core. |
| C | cbindgen, bindgen | Isolate all `unsafe` in 1 `*-ffi` crate. |
| C++ | cxx, autocxx | Use cxx for a narrow, typed bridge. |
| Any (browser or plugin) | WebAssembly (`wasm-bindgen`, WASI) | Use for sandboxed plugins or shared validation. |

- **Servers:** Use the strangler-fig pattern. Put a proxy in front and route 1 endpoint at a time to Rust. Compare responses in shadow mode before you switch.
- **CLIs:** Replace 1 subcommand at a time. The old CLI can call the new binary until all commands move.
- **Desktop:** Move the core into Rust first and call it through UniFFI or FFI. Replace the UI last.

**Phase 4: Data migration**

- Keep the old schema until the Rust service owns all writes.
- Use expand-and-contract migrations. Run dual writes only with a reconciliation job.
- Verify row counts and checksums after every backfill.

**Porting idioms and team ramp-up**

- Replace exceptions with `Result<T, E>` and `thiserror` enums. Replace `null` with `Option<T>`.
- Replace inheritance with traits. Replace global singletons with values built in the composition root.
- Replace implicit async or goroutines with explicit Tokio tasks, `JoinSet`, and cancellation.
- Give each developer 2 weeks with _The Rust Programming Language_ and small domain tasks. Pair them with experienced reviewers for the first 3 months.
