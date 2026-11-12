# Rust Application Architecture Guide

## 1. Summary

Use 1 architecture for all 3 app types. Only the shell and the adapters change between the server, the CLI, and the desktop app.

- **Shell (composition root):** Each binary crate builds the object graph, reads config, and starts the runtime. It holds no business rules.
- **Pure domain:** Domain crates hold types, rules, and reducers. They do no I/O, read no clock, and use no global state.
- **Thin presentation and adapters:** HTTP handlers, CLI commands, and GPUI views translate input into domain commands. Then they render the results.
- **Services behind traits:** Every side effect (database, network, clock, RNG, UUIDs, keychain) sits behind a port trait with live and fake adapters.
- **Concurrency model:** The server uses Tokio. The CLI stays synchronous unless it needs many concurrent network calls. The desktop app uses the GPUI executors plus 1 dedicated Tokio runtime.
- **Quality gates:** CI runs rustfmt, clippy with warnings denied, nextest, a 90% domain coverage gate, cargo-deny, cargo-audit, cargo-vet, and SBOM generation.

**Platform baseline (November 2026):**

| Item                                  | Version or policy                                                                       | Status note                                                                                                                                                     |
| ------------------------------------- | --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Rust stable                           | 1.99.1 (2026-10-15)\[1\]                                                                | Rust 1.100.0 is scheduled for 2026-11-12.\[2\] Pin it only after you read its release notes.                                                                    |
| Edition                               | 2024                                                                                    | Latest stable edition. No next edition is announced.                                                                                                            |
| MSRV policy                           | `rust-version` = pinned toolchain for apps                                              | No project-wide MSRV policy exists. Each crate sets its own.                                                                                                    |
| Tokio                                 | 1.54.1 (2026-10-21), MSRV 1.85\[3\]                                                     | LTS line: 1.53.x until September 2027.\[4\]                                                                                                                     |
| axum                                  | 0.8.9 (2026-04-14)                                                                      | 0.9 is in progress.\[6\]\[7\] `main` has breaking changes.\[8\]                                                                                                 |
| reqwest                               | 0.13.5 (2026-09-08)                                                                     | rustls is the default TLS backend.\[9\] aws-lc-rs is the default provider.\[10\]                                                                                |
| rustls                                | 0.23.x                                                                                  | 0.24 is in development and changes how you select providers.\[11\]                                                                                              |
| tonic                                 | 0.14.x                                                                                  | Now in `grpc/grpc-rust`. Codegen moved to `tonic-prost-build`.\[12\]                                                                                            |
| sqlx                                  | 0.9.0 (2026-05-21)                                                                      | `sqlx-core` needs Rust 1.94.\[13\]\[14\]                                                                                                                        |
| rusqlite                              | 0.41.1 (2026-10-28)                                                                     | Bundles SQLite 3.54. 0.41.0 fixed RUSTSEC-2026-0459, a `libsqlite3-sys` advisory.\[15\] 0.42.0 came out on 2026-11-11. Let the cooldown pass before you use it. |
| clap / ratatui                        | 4.6.7 / 0.30.2\[16\]\[17\]                                                              | Stable.                                                                                                                                                         |
| thiserror / anyhow                    | 2.0.21 / 1.0.104\[18\]\[19\]                                                            | Stable.                                                                                                                                                         |
| tracing / tracing-subscriber          | 0.1.44 / 0.3.23\[20\]\[21\]                                                             | Stable.                                                                                                                                                         |
| opentelemetry / tracing-opentelemetry | 0.33 / 0.34.0\[22\]                                                                     | Pre-1.0. Keep all `opentelemetry*` crates on the same minor version.\[23\]                                                                                      |
| GPUI                                  | Zed tag `v1.28.1` (2026-11-11), as git dependencies on `gpui` and `gpui_platform`\[73\] | The crates.io release `gpui` 0.2.2 is stale (2025-10-22).\[26\]                                                                                                 |
| Supply chain                          | cargo-deny 0.20.2, cargo-audit 0.23.0, cargo-vet 0.10.3, cargo-cyclonedx 0.5.10         | Active.\[27\]\[28\]\[38\]\[39\] cargo-audit 0.23.0 came out on 2026-11-10.                                                                                      |

## 2. Priority order for trade-offs

Apply this order to every decision: 1. Security, 2. Reliability, 3. Accessibility, 4. Maintainability, 5. Performance. Optimize performance only after you measure it.

| Conflict                                           | Decision                                                                            | Reason                                            |
| -------------------------------------------------- | ----------------------------------------------------------------------------------- | ------------------------------------------------- |
| A new crate version fixes a bug but is 1 day old   | Wait for the cooldown. For an urgent security fix, use the override in section 3.3. | Security comes before speed of adoption.          |
| `unsafe` gives a 15% speed-up in a parser          | Keep safe code                                                                      | Security and reliability come before performance. |
| A spinner looks good, but screen readers repeat it | Print 1 status line per state change                                                | Accessibility comes before animation.             |

## 3. Project setup and toolchain

Pin the toolchain, commit `Cargo.lock`, and gate CI on lint, test, and supply-chain checks from the first commit.

### 3.1 Toolchain

1. Install Rust with `rustup`.
2. Add `rust-toolchain.toml` at the workspace root.
3. Set `rust-version` in `[workspace.package]` to the same version.
4. Update the pin in a separate pull request.

```toml
# rust-toolchain.toml
[toolchain]
channel = "1.99.1"
components = ["rustfmt", "clippy", "llvm-tools-preview"]
profile = "minimal"
```

**Warning:** Do not move to 1.100.0 on its release day. Read the final release notes first.\[30\] The draft notes list these compatibility changes: the never type `!` becomes stable, `Infallible` becomes an alias for `!`, and the never type fallback changes to `!` on all editions.\[30\]\[31\] These changes can cause new type inference errors. In Cargo, the `build-dir` layout changes to version 2, and `cargo install` uses the packaged lockfile by default.\[30\]

- Rust 1.100 stops shipping host tools (`rustc`, `cargo`) for `i686-pc-windows-msvc` and `i686-pc-windows-gnu`. The standard library still ships, so you can build 32-bit Windows binaries from a 64-bit host.\[32\]
- Rust 1.97 lets Cargo control warnings directly.\[33\] Use `CARGO_BUILD_WARNINGS=deny` in CI instead of `RUSTFLAGS=-Dwarnings`. This keeps the build cache valid. It applies to `cargo clippy` too.

### 3.2 Edition, resolver, and MSRV

- Use edition 2024 for all crates.
- Set `resolver = "3"` in the virtual workspace manifest, because a virtual manifest has no edition.
- For apps, set `rust-version` equal to the pinned toolchain. For published libraries, support at least the previous 2 stable versions.
- Check dependency MSRVs before you upgrade.\[30\] For example, `sqlx-core` 0.9.0 needs 1.94\[14\] and Tokio 1.54 needs 1.85.\[3\]\[5\]

### 3.3 Config and dependency policy

- Load config in this order: defaults, config file, environment variables, CLI flags. Parse it into typed structs at startup. Stop if it is not valid.
- Commit `Cargo.lock` for every application workspace.
- Add a dependency only after you check maintenance activity, RustSec history, license, and transitive dependency count.
- Turn on the Cargo dependency cooldown when you move to Rust 1.100, which makes it stable. The default is 0, so an upgrade alone does not protect you.\[34\]\[35\]\[36\]

```toml
# .cargo/config.toml (needs Cargo 1.100+)
[registry]
global-min-publish-age = "7 days"
```

- Cargo keeps versions that are already in `Cargo.lock`. The cooldown does not apply to `cargo install`.\[34\] Git and path dependencies have no publish time, so the cooldown does not apply to them.\[36\]
- For 1 registry only, set `registries.<name>.min-publish-age`.\[34\]
- For urgent security fixes, override it for 1 command with `CARGO_RESOLVER_INCOMPATIBLE_PUBLISH_AGE=allow`.\[34\]

On August 20, 2026, an attacker used 1 hijacked maintainer account to publish malicious releases of `arrayref` 0.3.10, `internment` 0.8.7, and `append-only-vec` 0.1.9.\[67\] Each release added a direct dependency, `proc-macro1`, with a malicious build script. These releases stayed on crates.io for 86 to 107 minutes before removal. RUSTSEC-2026-0260 records 2,285 downloads of the `arrayref` release in its 86 minutes.\[37\] A 7-day cooldown keeps such a release out of your build. On September 17, 2026, the Rust blog post "Be alert: targeted attacks on prominent Rustaceans" warned of fake job or contract video calls. These calls try to make maintainers install "a purportedly missing audio codec."\[68\]

### 3.4 Supply-chain tools

| Tool            | Version             | Purpose                                                                      |
| --------------- | ------------------- | ---------------------------------------------------------------------------- |
| cargo-deny      | 0.20.2              | Checks licenses, bans, duplicates, sources, and advisories.\[27\]            |
| cargo-audit     | 0.23.0 (2026-11-10) | Checks `Cargo.lock` and binaries (`cargo audit bin`) against RustSec.\[38\]  |
| cargo-vet       | 0.10.3              | Records human audits. Imports audits from Mozilla, Google, and others.\[39\] |
| cargo-auditable | current             | Embeds the dependency list in the binary.\[29\]                              |
| cargo-cyclonedx | 0.5.10 (2026-11-06) | Generates CycloneDX SBOMs.\[28\]                                             |

Use cargo-vet as the trust tool.

### 3.5 Lints, formatting, and decision records

- Define lints once in `[workspace.lints]`. Add `[lints] workspace = true` to every member.
- Rust 1.100 makes Cargo's own lint table (`[lints.cargo]`) stable.\[30\]\[40\] Its `unused_dependencies` lint warns by default.\[70\] Set it to `"deny"` in `[workspace.lints.cargo]` after you upgrade.
- Store Architecture Decision Records in `docs/adr/NNNN-title.md`. Write 1 record for each choice in section 22.

## 4. UI framework

Use clap for every CLI, ratatui for full-screen TUIs, and GPUI for desktop apps. Section 4.1 gives the stability and accessibility gaps of GPUI.

### 4.1 Desktop: GPUI status

GPUI is a hybrid immediate-mode and retained-mode, GPU-accelerated UI framework from Zed Industries.\[41\]\[65\] The "GPUI 2" rewrite has run Zed since January 2024.\[42\] It works well for Zed. It is not a stable general-purpose framework.

The Zed repository is the official GPUI project and the source of truth: the `crates/gpui` crate in `zed-industries/zed`, its README, and gpui.rs.\[65\]\[41\] Take each fact about the API from the source at the tag that you pin. Where gpui.rs and the source at the tag do not agree, the source is correct.

| Package                              | Version                       | Maintainer     | Use                                                                                                                                                                                  |
| ------------------------------------ | ----------------------------- | -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `gpui` and `gpui_platform` from git  | Zed tag `v1.28.1`\[73\]       | Zed Industries | Always. Pin the tag in the workspace manifest (section 6.4).                                                                                                                         |
| `gpui` on crates.io                  | 0.2.2, 2025-10-22             | Zed Industries | Do not use. It is stale, and crates.io has no `gpui_platform` crate. Zed closed the release request (issue #66275) on 2026-10-30 and said that automated releases are in work.\[26\] |
| `gpui-pre` and GPUI Kit on crates.io | 0.3.12 and 0.9.1 (2026-11-09) | Longbridge     | Reference only. `gpui-pre` is a copy of Zed `main`.\[24\] GPUI Kit depends on `gpui-pre =0.3.12`, not on Zed's `gpui`, so it does not work with the git dependency.\[25\]            |

- A Zed Discord message of 2025-12-12 said: "We gotta focus on some business relevant work in 2026." A Hacker News comment of 2026-02-13 (item 47003569) quotes the message.\[43\]
- The GPUI README says it is "pre-1.0" with "often" breaking changes, and it needs the latest stable Rust.\[65\]
- **Platforms:** macOS (Metal), Linux (wgpu, on X11 and Wayland), and Windows (Direct3D 11). Zed `main` also has `gpui_web` (WebAssembly) and `gpui_ios` crates. This guide does not cover them.
- **Components:** The `gpui` crate has elements such as `div`, `img`, `svg`, `canvas`, `list`, `uniform_list`, and text.\[74\] It has no ready button, text input, or checkbox. Write these components on the GPUI elements. GPUI Kit has ready components, but only for `gpui-pre`.\[44\]

**Accessibility status (top priority):**

- Zed merged AccessKit support into GPUI on 2026-05-27 (zed-industries/zed PR #56065).\[71\] AccessKit maps to UI Automation (Windows), NSAccessibility (macOS), and AT-SPI (Linux).
- Screen readers see an element only if the app gives it an `id` and a `role`.\[58\] A text child gives the node no name. Set the name with `.aria_label(...)`.\[72\]
- Open bugs exist. On macOS, the app reports the window as the focused element instead of the focused control (issue #66691). Elements clipped out of view are reported as visible (issue #66730).\[46\]\[47\]
- Zed's own "accessible mode" is still "experimental and incomplete" (Zed docs, November 2026).\[45\]
- The AccessKit README says its adapters do not yet support rich text or hypertext.\[66\]
- **Conclusion:** GPUI accessibility is new, opt-in per element, and not yet proven in production. Budget for manual screen-reader testing on all 3 platforms.

### 4.2 CLI and terminal UX

- Use `clap` 4.6 with the derive API.
- Use `ratatui` 0.30 only for interactive full-screen tools. Always give a non-interactive subcommand for the same task.
- If `NO_COLOR` is set and not empty, print no ANSI color.
- Disable color and animation when stdout is not a terminal.
- Give `--json` output for every command that prints data.

## 5. Application architecture pattern

Use functional core / imperative shell inside a hexagonal (ports-and-adapters) layout. Put rules in pure reducers. Put effects in adapters behind traits.

| Pattern                                    | Use when                                                      | Do not use when                            |
| ------------------------------------------ | ------------------------------------------------------------- | ------------------------------------------ |
| Functional core / imperative shell         | Always. This is the default.                                  | Never skip it.                             |
| Hexagonal (ports and adapters)             | The app has 2 or more I/O systems, or more than 1 binary.     | You have a 200-line script.                |
| Reducer (state, action) → (state, effects) | You have a UI state machine, a workflow, or CLI wizard state. | You have a stateless CRUD path.            |
| Actor (task + channel)                     | You need long-lived state shared across tasks.                | A `Mutex` around a small struct is enough. |
| CQRS / event sourcing                      | Audit or replay is a hard requirement.                        | You only want it because it looks clean.   |

### 5.1 Rules for pure domain crates

- Do no I/O, no `async`, no `SystemTime::now()`, no random numbers, and no logging.
- Depend only on `std`, `thiserror`, and small value crates.
- Make illegal states unrepresentable with newtypes and enums. Parse raw input into types such as `Sku` with `TryFrom<&str>` at the edge.
- Return `Result` with domain error enums. Never panic on input.

### 5.2 Pure reducer example

```rust
// crates/orders-domain/src/reducer.rs
use app_core::{OrderId, Quantity, Sku}; // `OrderId` is a `Copy` newtype

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum OrderState {
    Draft { lines: Vec<(Sku, Quantity)> },
    Submitted { id: OrderId, lines: Vec<(Sku, Quantity)> },
    Cancelled { id: OrderId },
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Action {
    AddLine(Sku, Quantity),
    Submit { new_id: OrderId },
    Cancel,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Effect {
    PersistOrder(OrderId),
    NotifySubmitted(OrderId),
}

#[derive(Debug, thiserror::Error, PartialEq, Eq)]
pub enum OrderError {
    #[error("order has no lines")]
    Empty,
    #[error("action is not allowed in the current state")]
    InvalidTransition,
}

/// Pure: same input, same output. The caller supplies ids, so no hidden randomness.
///
/// # Errors
///
/// Returns `OrderError` when the action is not valid for the current state.
pub fn reduce(state: OrderState, action: Action) -> Result<(OrderState, Vec<Effect>), OrderError> {
    match (state, action) {
        (OrderState::Draft { mut lines }, Action::AddLine(sku, qty)) => {
            lines.push((sku, qty));
            Ok((OrderState::Draft { lines }, vec![]))
        }
        (OrderState::Draft { lines }, Action::Submit { .. }) if lines.is_empty() => {
            Err(OrderError::Empty)
        }
        (OrderState::Draft { lines }, Action::Submit { new_id }) => Ok((
            OrderState::Submitted { id: new_id, lines },
            vec![Effect::PersistOrder(new_id), Effect::NotifySubmitted(new_id)],
        )),
        (OrderState::Submitted { id, .. }, Action::Cancel) => {
            Ok((OrderState::Cancelled { id }, vec![Effect::PersistOrder(id)]))
        }
        _ => Err(OrderError::InvalidTransition),
    }
}
```

### 5.3 Dependency injection with traits

- Use **generics** (`impl<R: OrderRepo>`) inside libraries and hot paths for static dispatch.
- Use **`Arc<dyn Trait>`** in composition roots and app state for simpler types and faster builds.
- `async fn` in traits is stable, but such traits are not dyn-compatible. For `dyn` ports with async methods, return `Pin<Box<dyn Future + Send>>`, as `BoxFut` does in section 10.
- Put `Send + Sync` bounds on ports that the server or GPUI background tasks use.

### 5.4 Inject the clock, RNG, and UUIDs (live and fake adapters)

```rust
// crates/core-ports/src/lib.rs
pub mod orders; // section 10
pub mod random; // section 12

use std::time::SystemTime;

pub trait Clock: Send + Sync {
    fn now(&self) -> SystemTime;
}

pub trait IdGenerator: Send + Sync {
    fn new_id(&self) -> uuid::Uuid;
}

pub trait Random: Send {
    fn next_u64(&mut self) -> u64;
}

pub struct SystemClock;
impl Clock for SystemClock {
    fn now(&self) -> SystemTime { SystemTime::now() }
}

pub struct V7Ids;
impl IdGenerator for V7Ids {
    fn new_id(&self) -> uuid::Uuid { uuid::Uuid::now_v7() }
}

pub struct FixedClock(pub SystemTime);
impl Clock for FixedClock {
    fn now(&self) -> SystemTime { self.0 }
}
```

## 6. Modularization with a Cargo workspace

Use 1 virtual workspace. Binaries are composition roots. Domain crates depend only on `core`. Adapters depend on ports, and ports never depend on adapters.

### 6.1 Crate roles

| Crate                              | Role                                                  | May depend on              | Must not depend on                  |
| ---------------------------------- | ----------------------------------------------------- | -------------------------- | ----------------------------------- |
| `apps/server`                      | Composition root for HTTP/gRPC                        | all except UI crates       | `gpui*`                             |
| `apps/cli`                         | Composition root for the CLI                          | all except UI crates       | `gpui*`                             |
| `apps/desktop`                     | Composition root for GPUI                             | all except server crates   | `axum`, `tonic`, `feature-contract` |
| `crates/core` (package `app-core`) | Shared value types and errors                         | std, thiserror             | any adapter                         |
| `crates/core-ports`                | Port traits (Clock, Random, repos)                    | core                       | any adapter                         |
| `crates/feature-contract`          | Feature trait and registry for the server and the CLI | core-ports, `axum`, `clap` | adapters, `gpui*`                   |
| `crates/<feature>-domain`          | Pure rules and reducers                               | core                       | I/O crates, async runtimes          |
| `crates/<feature>-app`             | Use cases that orchestrate ports                      | domain, core-ports         | concrete adapters                   |
| `crates/adapter-*`                 | Postgres, SQLite, HTTP client implementations         | core-ports                 | other adapters                      |
| `crates/ui-desktop-<feature>`      | GPUI views for 1 feature                              | feature-app                | adapters                            |
| `crates/testing`                   | Fakes and fixtures (dev-only)                         | core-ports                 | —                                   |

### 6.2 Dependency rules

- Dependencies point inward only. Binaries → UI crates → `*-app` → `*-domain` → `core`. Binaries → adapters → `core-ports` → `core`. The `*-app` crates also use `core-ports`. Enforce this in CI with `cargo deny check bans`.
- Give the shared crate the package name `app-core`, not `core`. A dependency with the name `core` hides the built-in `core` crate. Derive macros such as `thiserror::Error` then fail with "cannot find `fmt` in `core`".
- Keep items `pub(crate)` by default. Export only the minimal API from each `lib.rs`.
- Name crates `<area>-<role>`, for example `orders-domain`, `orders-app`, or `adapter-postgres`.
- All 3 binaries share `orders-app` and `orders-domain`. Build each one alone with `cargo build -p server` or `cargo build -p desktop`.

### 6.3 Directory tree

```text
.
├── Cargo.toml                # virtual workspace
├── Cargo.lock
├── rust-toolchain.toml
├── deny.toml
├── .cargo/config.toml
├── supply-chain/             # cargo-vet
├── docs/adr/
├── apps/{server,cli,desktop}/src/main.rs
└── crates/
    ├── core/  core-ports/  feature-contract/  testing/
    ├── orders-domain/  orders-app/
    ├── adapter-postgres/  adapter-sqlite/
    └── ui-desktop-orders/
```

### 6.4 Workspace `Cargo.toml`

```toml
[workspace]
resolver = "3"
members = ["apps/*", "crates/*"]

[workspace.package]
edition = "2024"
rust-version = "1.99.1"
license = "Apache-2.0"
publish = false

[workspace.dependencies]
app-core = { path = "crates/core" }
core-ports = { path = "crates/core-ports" }
feature-contract = { path = "crates/feature-contract" }
orders-domain = { path = "crates/orders-domain" }
orders-app = { path = "crates/orders-app" }

tokio = { version = "1.54", features = ["rt-multi-thread", "macros", "signal", "net", "time"] }
tokio-util = { version = "0.7.20", features = ["rt"] }
axum = "0.8.9"
tower-http = { version = "0.7", features = ["trace", "request-id", "timeout"] }
reqwest = { version = "0.13.5", default-features = false, features = ["rustls", "json"] }
tonic = "0.14"
sqlx = { version = "0.9.0", default-features = false, features = ["runtime-tokio", "tls-rustls-aws-lc-rs", "postgres", "migrate", "macros"] }
rusqlite = { version = "0.41.1", features = ["bundled"] }
thiserror = "2.0.21"
anyhow = "1.0.104"
tracing = "0.1.44"
tracing-subscriber = { version = "0.3.23", features = ["json", "env-filter"] }
clap = { version = "4.6.7", features = ["derive"] }
uuid = { version = "1", features = ["v7"] }
secrecy = "0.10"
gpui = { git = "https://github.com/zed-industries/zed", tag = "v1.28.1" }   # read section 4.1 first
gpui_platform = { git = "https://github.com/zed-industries/zed", tag = "v1.28.1", features = ["font-kit", "wayland", "x11"] }

[workspace.lints.rust]
unsafe_code = "forbid"
unreachable_pub = "warn"

[workspace.lints.clippy]
unwrap_used = "deny"
expect_used = "warn"
panic = "deny"
dbg_macro = "deny"
todo = "deny"
pedantic = { level = "warn", priority = -1 }
```

### 6.5 Member `Cargo.toml`

```toml
# crates/orders-domain/Cargo.toml
[package]
name = "orders-domain"
version = "0.1.0"
edition.workspace = true
rust-version.workspace = true
license.workspace = true
publish.workspace = true

[dependencies]
app-core.workspace = true
thiserror.workspace = true
uuid = { workspace = true, default-features = false }

[dev-dependencies]
proptest = "1.12"

[lints]
workspace = true
```

### 6.6 Feature contract and registry

Each feature registers its routes and commands through 1 contract. The composition root decides which features to load. The contract has its own crate, because it names `axum` and `clap` types. `core-ports` and the desktop binary do not depend on it.

```rust
// crates/feature-contract/src/lib.rs
use std::sync::Arc;

pub struct FeatureContext {
    pub clock: Arc<dyn core_ports::Clock>,
    pub ids: Arc<dyn core_ports::IdGenerator>,
}

pub trait Feature: Send + Sync {
    /// Stable, unique key. Used in config and feature flags.
    fn key(&self) -> &'static str;
    fn http_routes(&self, _ctx: &FeatureContext) -> Option<axum::Router> { None }
    fn cli_command(&self) -> Option<clap::Command> { None }
}

#[derive(Default)]
pub struct FeatureRegistry {
    features: Vec<Box<dyn Feature>>,
}

impl FeatureRegistry {
    /// # Panics
    ///
    /// Panics on a duplicate key. That is a wiring bug, not user input.
    #[must_use]
    pub fn register(mut self, f: Box<dyn Feature>) -> Self {
        assert!(
            self.features.iter().all(|x| x.key() != f.key()),
            "duplicate feature key: {}", f.key()
        );
        self.features.push(f);
        self
    }

    pub fn router(&self, ctx: &FeatureContext) -> axum::Router {
        self.features
            .iter()
            .filter_map(|f| f.http_routes(ctx))
            .fold(axum::Router::new(), axum::Router::merge)
    }
}
```

In large workspaces, split the contract into 1 crate per surface (`feature-http`, `feature-cli`), so the CLI does not link `axum`.

## 7. Routing, navigation, and input

Treat every URL, header, argument, environment variable, and file as untrusted. Parse input into domain types at the edge, then route typed commands.

- **Server (axum 0.8):** Use `{param}` path syntax, for example `/orders/{id}`. Group routes per feature and merge them in the root. Extract typed values (`Path<OrderId>`, `Json<CreateOrder>`). Set body size limits on all routes.
- **CLI:** Use the `noun verb` form: `app orders list`. Add new flags, but never rename old flags. Read secrets from stdin or the keychain, never from a flag, because flags show up in process lists and shell history.
- **Desktop (GPUI):** Hold navigation state in 1 root view entity as an enum (`Screen::OrderList`, `Screen::OrderDetail(OrderId)`). Change screens through actions, so keyboard shortcuts and menus use the same path. Validate dropped and opened files like network input.

## 8. Networking

Use axum on Tower and hyper for HTTP servers, reqwest with rustls for clients, and tonic for gRPC. Put timeouts on every network call.

| Framework  | Status (Nov 2026)                           | Use when                                      |
| ---------- | ------------------------------------------- | --------------------------------------------- |
| axum 0.8.9 | Maintained by tokio-rs. 0.9 is in progress. | Every HTTP server. Native Tower middleware.   |
| tonic 0.14 | Maintained in `grpc/grpc-rust`              | You need gRPC. You can mount it next to axum. |

**Warning:** Do not copy examples from the axum `main` branch. It has unreleased 0.9 breaking changes. Read the docs and examples on the `v0.8.x` branch.\[8\]

- **Middleware:** Use `tower-http` for tracing, request IDs, timeouts, compression, and CORS. Assign the request ID before the tracing layer.
- **HTTP client:** Use reqwest 0.13. It defaults to rustls with aws-lc-rs and `rustls-platform-verifier`, which uses OS trust stores.\[9\]
- **Crypto provider:** Use aws-lc-rs. It has a FIPS 140-3 mode.\[48\] The default build needs only a C compiler, and on Windows it can also need NASM. The FIPS build also needs CMake and Go.\[49\]

**Warning:** rustls 0.24 is in development. From 0.24, you must pass a crypto provider explicitly, and the providers move to separate crates (`rustls-aws-lc-rs`).\[11\] Do not mix rustls 0.23 and 0.24 in 1 binary without a plan.

- **gRPC:** Add `tonic`, `tonic-prost`, and `prost` 0.14. Use `tonic-prost-build` in `build.rs`.\[50\] Map generated types to domain types in an adapter crate.
- **Timeouts and retries:** Set connect, request, and total timeouts. Retry only idempotent calls, with exponential backoff, full jitter, and a maximum attempt count.
- **Correlation and cancellation:** Propagate `x-request-id` and `traceparent`. Use `CancellationToken` from `tokio-util` to stop work on disconnect or shutdown.

## 9. Authentication and identity

Use server-side sessions for browser clients, and short-lived tokens for CLI, desktop, and API clients. Use the OAuth device flow for CLIs, and OS credential stores for CLI and desktop secrets.

- **Server sessions:** For browser clients, use opaque session IDs stored server-side. Set cookies with `Secure`, `HttpOnly`, and `SameSite=Lax` or `Strict`.
- **JWT:** Pin the algorithm, check `exp`, `nbf`, `aud`, and `iss`, and keep lifetimes short. Never accept `alg: none`. Use the `oauth2` and `openidconnect` crates for OAuth 2.0 and OIDC.
- **Passwords:** Hash with `argon2` (Argon2id).

**Warning:** argon2 0.6.0 has breaking changes. The `rand` feature is now `getrandom`, the `simple` feature is now `password-hash`, and `PasswordHash` and `SaltString` moved to `password_hash::phc`. Before you upgrade, test that hashes from 0.5.x still verify.\[51\]

- **CLI:** Use the OAuth 2.0 device authorization grant. Store refresh tokens in the OS keychain.
- **Desktop:** Use the same keychain crates. Use the system browser with authorization code + PKCE. Do not embed a login webview.

**Warning:** keyring v4 split its API. The core API moved to `keyring-core` v1, and each platform store is a separate crate. The old feature names (`apple-native`, `linux-native`) are gone.\[52\] Depend on `keyring-core` v1 and the platform store crates: `apple-native-keyring-store`, `windows-native-keyring-store`, and `zbus-secret-service-keyring-store` (Linux).\[53\]

## 10. Persistence

Put every store behind a repository trait. Use SQLite for local data and PostgreSQL for shared server data.

| Need                            | Choice                    | Notes                                        |
| ------------------------------- | ------------------------- | -------------------------------------------- |
| User config                     | TOML file through `serde` | Store under the OS config directory.         |
| Local relational (CLI, desktop) | `rusqlite` 0.41.1 (sync)  | Use `bundled`. 0.41 fixes RUSTSEC-2026-0459. |
| Server relational               | `sqlx` 0.9 PostgreSQL     | Compile-time checked queries and migrations. |

- **sqlx 0.9:** `query*()` functions take a type that implements `SqlSafeStr`, which makes SQL injection harder.\[13\] The old `runtime-tokio-rustls` feature is gone. Use `runtime-tokio` plus the `tls-rustls-aws-lc-rs` feature.\[54\]
- **sqlx-cli:** `cargo install --locked sqlx-cli` no longer works with 0.9.0, because the project removed its `Cargo.lock`.\[13\] In CI, pin the version with `cargo install sqlx-cli --version 0.9.0`. For a reproducible build, the announcement tells you to keep your own lockfile.
- **rusqlite and tokio-rusqlite:** `tokio-rusqlite` 0.8.0 requires rusqlite 0.40, and its bundled SQLite has RUSTSEC-2026-0459. `tokio-rusqlite` 0.9.0 (2026-11-11) requires rusqlite 0.42. `FromSql` for `u64` has needed the `fallible_uint` feature since rusqlite 0.38.\[55\]
- Run server migrations as a separate, explicit step. Test every migration against production-shaped data in CI.
- Use pools with a maximum size and an acquire timeout. Encrypt data at rest. Use SQLCipher if a local file holds regulated data. With rusqlite 0.41.x, the `bundled-sqlcipher` feature still builds a SQLite that RUSTSEC-2026-0459 affects.\[15\] Read the advisory before you ship it.

```rust
// crates/core-ports/src/orders.rs
use std::{future::Future, pin::Pin};
use app_core::{Order, OrderId};

pub type BoxFut<'a, T> = Pin<Box<dyn Future<Output = T> + Send + 'a>>;

#[derive(Debug, thiserror::Error)]
pub enum RepoError {
    #[error("not found")]
    NotFound,
    #[error("storage unavailable")]
    Unavailable(#[source] Box<dyn std::error::Error + Send + Sync>),
}

pub trait OrderRepo: Send + Sync {
    fn get(&self, id: OrderId) -> BoxFut<'_, Result<Order, RepoError>>;
    fn save(&self, order: &Order) -> BoxFut<'_, Result<(), RepoError>>;
}
```

```rust
// crates/testing/src/fake_orders.rs
use std::{collections::HashMap, sync::{Mutex, PoisonError}};
use core_ports::orders::{BoxFut, OrderRepo, RepoError};
use app_core::{Order, OrderId};

#[derive(Default)]
pub struct FakeOrderRepo {
    rows: Mutex<HashMap<OrderId, Order>>,
}

impl OrderRepo for FakeOrderRepo {
    fn get(&self, id: OrderId) -> BoxFut<'_, Result<Order, RepoError>> {
        // A poisoned lock still holds valid rows, so the fake does not panic.
        let found = self.rows.lock().unwrap_or_else(PoisonError::into_inner).get(&id).cloned();
        Box::pin(async move { found.ok_or(RepoError::NotFound) })
    }
    fn save(&self, order: &Order) -> BoxFut<'_, Result<(), RepoError>> {
        self.rows.lock().unwrap_or_else(PoisonError::into_inner).insert(order.id, order.clone());
        Box::pin(async { Ok(()) })
    }
}
```

The live `PgOrderRepo` in `adapter-postgres` implements the same trait with `sqlx::query_as(...).bind(id).fetch_optional(&pool)`. It maps `sqlx::Error` to `RepoError::Unavailable`.

## 11. Security and privacy

Forbid `unsafe` by default, gate every dependency, parse all input into typed values, and keep secrets and PII out of logs.

- **Secrets:** Load them from a secrets manager on servers, and from the OS keychain in CLI and desktop apps. Wrap them in `secrecy::SecretString` and call `expose_secret()` only at the point of use. `secrecy` 0.10 uses `SecretBox<S>`.\[56\] The old `Secret<T>` type is gone. Use `zeroize` for key material that you own.
- **Unsafe:** Set `unsafe_code = "forbid"`. If FFI needs `unsafe`, isolate it in 1 `*-ffi` crate and override the lint there only. Write a `// SAFETY:` comment on every block. Run Miri on that crate. Run `cargo geiger` (0.14.0) to report `unsafe` in dependencies.
- **Supply chain:** Run `cargo deny check`, `cargo audit`, and `cargo vet` on every pull request. Build releases with `cargo auditable build` and `--locked`. Attach CycloneDX SBOMs.

**Warning:** Do not give secrets to a CI job that runs Miri and writes a cache. On September 21, 2026, the Rust blog reported: "Miri stores all environment variables to target/, allowing secrets to persist in caches."\[69\] The post names the 2026-09-22 nightly for the fix. Use a newer nightly, clear the old caches, and rotate the secrets that such a job used.

- **Parse, don't validate:** Convert raw strings into domain types (`Sku`, `OrderId`, `Quantity`) with `TryFrom` at the trust boundary. After that, functions accept only the typed values.
- **Errors and logs:** Send generic messages to users ("Request failed. Reference: 7f3a…"). Log the details with the same reference. Log IDs, not names, emails, or tokens.
- **Randomness:** Use the OS CSPRNG (`getrandom`) for tokens and keys. Never use a seeded RNG for security values.
- **Regulated data (not legal advice):** For GDPR, collect the minimum and support export and deletion. For HIPAA, encrypt PHI and keep access audit logs. For PCI DSS, do not store card numbers; use provider tokenization. Ask a compliance professional before you ship.

## 12. Concurrency and reliability

Use Tokio for servers, synchronous code for most CLIs, and the GPUI executors for desktop UI work. Never block an async thread and never hold a lock across `.await`.

- **Runtime:** Tokio 1.54.1 is the default and needs Rust 1.85.\[3\]\[5\] For a fixed minor version, use the LTS line 1.53.x (until September 2027). The 1.47.x LTS line ended in September 2026.\[4\] async-std is discontinued (RUSTSEC-2025-0052).
- **Locks:** Use `std::sync::Mutex` for short, non-async critical sections. Prefer a message-passing task over `tokio::sync::Mutex`.
- **Blocking work:** Move CPU-heavy or blocking work to `spawn_blocking`.
- **Structured concurrency:** Use `JoinSet` for task groups. Use `TaskTracker` with `CancellationToken` for graceful shutdown. Never detach a `tokio::spawn` without a tracker.
- **GPUI and Tokio:** GPUI has its own foreground and background executors and does not run Tokio. Tokio-based crates (reqwest, sqlx, tonic) need a runtime. Start 1 Tokio runtime at startup, store its `Handle`, spawn network work on it, and await the result in a GPUI task through a `tokio::sync::oneshot` channel. Zed's internal `gpui_tokio` bridge is not a stable public API.
- **Errors:** Use `thiserror` 2 in libraries and domain crates (see `OrderError` and `RepoError`). Use `anyhow` only in binaries, with `.context(...)`.\[57\] Never `unwrap()` external data. Keep `panic = "unwind"` on servers and catch panics at the task boundary.

```rust
// crates/core-ports/src/random.rs — deterministic RNG for tests and simulations
use crate::Random;

/// `SplitMix64`: tiny, fast, deterministic. Not for secrets.
pub struct SeededRandom { state: u64 }

impl SeededRandom {
    #[must_use]
    pub fn new(seed: u64) -> Self { Self { state: seed } }
}

impl Random for SeededRandom {
    fn next_u64(&mut self) -> u64 {
        self.state = self.state.wrapping_add(0x9E37_79B9_7F4A_7C15);
        let mut z = self.state;
        z = (z ^ (z >> 30)).wrapping_mul(0xBF58_476D_1CE4_E5B9);
        z = (z ^ (z >> 27)).wrapping_mul(0x94D0_49BB_1331_11EB);
        z ^ (z >> 31)
    }
}
```

## 13. Process lifecycle, background work, and platform integration

Every binary must start cleanly, report health, stop cleanly on a signal, and exit with a meaningful code.

### 13.1 Server composition root

```rust
// apps/server/src/main.rs
use std::sync::Arc;
use axum::{routing::get, Router};
use secrecy::ExposeSecret;
use tokio_util::{sync::CancellationToken, task::TaskTracker};

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    tracing_subscriber::fmt().json().with_env_filter("info").init();

    let cfg = config::Server::load()?; // typed; fails fast
    let pool = sqlx::PgPool::connect(cfg.database_url.expose_secret()).await?;

    let ctx = feature_contract::FeatureContext {
        clock: Arc::new(core_ports::SystemClock),
        ids: Arc::new(core_ports::V7Ids),
    };
    let registry = feature_contract::FeatureRegistry::default()
        .register(Box::new(orders_http::OrdersFeature::new(
            Arc::new(adapter_postgres::PgOrderRepo::new(pool.clone())),
        )));

    let app = Router::new()
        .route("/healthz", get(|| async { "ok" }))
        .merge(registry.router(&ctx))
        .layer(tower_http::trace::TraceLayer::new_for_http());

    let shutdown = CancellationToken::new();
    let tracker = TaskTracker::new();
    tracker.spawn(workers::outbox(pool.clone(), shutdown.child_token()));

    let listener = tokio::net::TcpListener::bind(cfg.listen_addr).await?;
    let token = shutdown.clone();
    axum::serve(listener, app)
        .with_graceful_shutdown(async move {
            shutdown_signal().await;
            token.cancel();
        })
        .await?;

    tracker.close();
    tracker.wait().await;
    Ok(())
}

/// Resolves on Ctrl+C, and on SIGTERM on Unix. Containers send SIGTERM.
async fn shutdown_signal() {
    #[cfg(unix)]
    {
        use tokio::signal::unix::{signal, SignalKind};
        if let Ok(mut term) = signal(SignalKind::terminate()) {
            tokio::select! {
                _ = tokio::signal::ctrl_c() => {}
                _ = term.recv() => {}
            }
            return;
        }
    }
    let _ = tokio::signal::ctrl_c().await;
}
```

- `/healthz` reports that the process is alive. Add `/readyz` to report that dependencies are reachable.
- In containers, run as a non-root user and use a read-only root filesystem.

### 13.2 CLI composition root

```rust
// apps/cli/src/main.rs
use std::process::ExitCode;
use clap::{Parser, Subcommand};

#[derive(Parser)]
#[command(version, about = "Manage orders")]
struct Cli {
    /// Print machine-readable JSON.
    #[arg(long, global = true)]
    json: bool,
    #[command(subcommand)]
    cmd: Cmd,
}

#[derive(Subcommand)]
enum Cmd {
    /// List orders.
    List,
    /// Submit a draft order.
    Submit { id: String },
}

enum AppExit { Usage(String), Failure }

fn main() -> ExitCode {
    let cli = Cli::parse();
    let deps = match cli_deps::Live::from_env() {
        Ok(d) => d,
        Err(e) => {
            eprintln!("error: could not load configuration");
            tracing::debug!(error = ?e, "config load failed");
            return ExitCode::from(78); // EX_CONFIG
        }
    };
    match commands::run(cli, &deps) {
        Ok(()) => ExitCode::SUCCESS,
        Err(AppExit::Usage(msg)) => { eprintln!("error: {msg}"); ExitCode::from(2) }
        Err(AppExit::Failure) => ExitCode::FAILURE,
    }
}
```

- Use exit code 0 for success, 1 for failure, 2 for usage errors, and 130 after SIGINT.
- Write data to stdout and diagnostics to stderr.
- Find config paths with `etcetera`. Generate completions with `clap_complete` and man pages with `clap_mangen`.

### 13.3 Desktop composition root and minimal GPUI view

The example uses Zed's `gpui` and `gpui_platform` crates at tag `v1.28.1`.

```rust
// apps/desktop/src/main.rs
use gpui::{App, Context, Role, Window, WindowOptions, div, prelude::*};

struct OrdersView {
    count: usize,
}

impl Render for OrdersView {
    fn render(&mut self, _window: &mut Window, _cx: &mut Context<Self>) -> impl IntoElement {
        let summary = format!("{} open orders", self.count);
        div()
            .id("orders-root")
            .role(Role::Document)
            .size_full()
            .p_4()
            .child(
                div()
                    .id("orders-count")
                    .role(Role::Label)
                    .aria_label(summary.clone()) // the name that a screen reader speaks
                    .child(summary),
            )
    }
}

fn main() -> std::io::Result<()> {
    let tokio_rt = tokio::runtime::Runtime::new()?;
    let _tokio_handle = tokio_rt.handle().clone(); // store in app state for network adapters

    gpui_platform::application().run(|cx: &mut App| {
        let opened = cx.open_window(WindowOptions::default(), |_, cx| {
            cx.new(|_| OrdersView { count: 0 })
        });
        if let Err(error) = opened {
            eprintln!("error: could not open the main window: {error}");
            cx.quit();
        }
    });
    Ok(())
}
```

- `gpui_platform::application()` selects the window and text backends for the host OS.\[65\] The example on gpui.rs starts with `Application::new()`.\[41\] That function is not in the source at this tag.\[75\] Do not copy it.
- `.id(...).role(Role::...)` is the GPUI accessibility API. Without both, screen readers see nothing.\[58\] `.aria_label(...)` gives the node its name. A text child does not.\[72\]

**Warning:** On macOS, the `gpui_platform` build compiles the Metal shaders. Without the Metal toolchain of Xcode, the build stops with "missing Metal Toolchain". Install it with `xcodebuild -downloadComponent MetalToolchain`.

## 14. Accessibility

Make every surface usable without sight, without a mouse, and without color. For GPUI, assume nothing is accessible until you add IDs and roles and test with a screen reader.

| Need                       | GPUI status (Nov 2026)                                                                                                        | Action                                                                                                                   |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| Screen readers             | AccessKit since 2026-05-27. Opt-in per element.\[58\] Known bugs.                                                             | Add `id`, `role`, and a label to every element. Test with VoiceOver, NVDA, and Orca.                                     |
| Keyboard navigation        | Elements have `tab_index` and `tab_stop`. `Window` has `focus_next` and `focus_prev`. GPUI binds no Tab key by default.\[72\] | Bind Tab and Shift+Tab to `focus_next` and `focus_prev`, as the `a11y.rs` example does. Test every flow without a mouse. |
| Focus                      | macOS reports the window, not the control, as focused (#66691).\[46\]                                                         | Draw a visible focus ring. Re-test after each GPUI update.                                                               |
| Contrast and high contrast | No automatic OS high-contrast theme.                                                                                          | Ship a high-contrast theme. Check 4.5:1 text contrast.                                                                   |
| Reduced motion             | `App` has a `reduce_motion` flag. The animation and image elements obey it. No GPUI crate sets it from the OS setting.\[75\]  | Read the OS setting. Call `cx.set_reduce_motion(true)` when it is set.                                                   |
| Text scaling               | Not automatic.                                                                                                                | Scale the theme's rem size from a user setting.                                                                          |

**Warning:** Do not ship a GPUI app to screen-reader users without a manual test on every target OS.

- **CLI:** Never use color as the only signal. Respect `NO_COLOR`. Print progress as discrete lines when `TERM=dumb` or stdout is not a terminal. Give `--json` and `--quiet` on every command.
- **Server:** Return errors as RFC 9457 problem details (`application/problem+json`) with a clear `title` and `detail`. Publish API docs as accessible HTML.

## 15. Localization

Use Fluent (`fluent-bundle` 0.16) for user-facing messages in desktop apps and CLIs, and ICU4X (`icu` 2.4) for numbers, dates, and plural rules.

- **Desktop and CLI:** Load Fluent `.ftl` files per locale. Keep `--json` output locale-neutral (ISO 8601, `.` decimal).
- **Server:** Return error codes plus English text. Let clients localize.
- Keep message IDs stable. Never build sentences by joining fragments.

## 16. Testing

Write tests first for domain rules, prefer fakes over mocks, and gate CI on coverage and mutation results for domain crates.

| Layer                | Tool                                             | Gate                                               |
| -------------------- | ------------------------------------------------ | -------------------------------------------------- |
| Domain unit          | built-in `#[test]`, run with cargo-nextest 0.9.x | 90%+ line coverage (cargo-llvm-cov)                |
| Domain properties    | proptest 1.12.0\[59\]                            | Required for parsers and reducers                  |
| Mutation             | cargo-mutants 27.1.0\[60\]                       | No surviving mutants in domain crates (weekly)     |
| Snapshots            | insta                                            | Review snapshot diffs in the pull request          |
| CLI                  | `assert_cmd` + `trycmd`                          | Golden tests for help, exit codes, and `--json`    |
| HTTP                 | `tower::ServiceExt::oneshot` on the `Router`     | Every route: success, 400, 401, 404                |
| Database             | `testcontainers` (PostgreSQL), temp-file SQLite  | Every migration on a clean database                |
| GPUI                 | `#[gpui::test]` with the `test-support` feature  | View logic only. Accessibility needs manual tests. |
| Fuzzing              | cargo-fuzz                                       | Every parser of external input, nightly CI         |
| Unsafe / concurrency | Miri / loom                                      | Every `unsafe` crate / custom sync primitives      |
| Benchmarks           | criterion 0.8.2\[61\]                            | Track regressions (section 17)                     |

- criterion moved to the `criterion-rs` organization and needs Rust 1.86.\[61\]\[62\]
- CI matrix: Linux x86_64 and aarch64, macOS aarch64, Windows x86_64. Build the GPUI binary on all 3 desktop OSes.

## 17. Observability and performance

Instrument with `tracing`, export with OpenTelemetry, redact PII at the source, and measure before you optimize.

- Use `tracing` 0.1.44 with `tracing-subscriber` 0.3.23. Use JSON output for servers and human output for CLIs.
- Export traces with `tracing-opentelemetry` 0.34.0 and `opentelemetry` 0.33.
- Mark sensitive fields with `skip`, for example `#[tracing::instrument(skip(password))]`. Never log request bodies by default.

**Warning:** The OpenTelemetry Rust crates are pre-1.0. Upgrade all `opentelemetry*` crates and `tracing-opentelemetry` together in 1 pull request.\[23\]

- Profile CPU with `cargo flamegraph`. Inspect async tasks with `tokio-console` in development builds only, because it needs `tokio_unstable`.

## 18. Cross-cutting seams

Put each cross-cutting concern behind 1 trait with a safe default. Check it in 1 place.

| Seam                     | Trait           | Safe default         | Checked in                                     |
| ------------------------ | --------------- | -------------------- | ---------------------------------------------- |
| Authentication           | `Authenticator` | Deny all             | Server middleware; CLI/desktop session service |
| Authorization            | `Policy`        | Deny all             | Use-case layer (`*-app` crates)                |
| Analytics / telemetry    | `Telemetry`     | No-op, opt-in only   | Composition root; domain never calls it        |
| Feature flags            | `Flags`         | All new features off | Feature registry at startup                    |
| Diagnostics              | `Diagnostics`   | Logs only, no upload | Crash and error handlers                       |
| Entitlements / licensing | `Entitlements`  | Free tier            | Use-case layer, before a paid action           |
| Notifications            | `Notifier`      | Log and drop         | Effect handler after the reducer               |

## 19. Release engineering and distribution

Version with SemVer, build reproducibly in CI, sign everything, and ship SBOMs with every artifact.

- Use `release-plz` for release pull requests and changelogs.\[63\]
- Use `dist` (cargo-dist) 0.34.0 (2026-11-02) to build installers and GitHub releases for CLI and desktop binaries.\[64\] It is maintained, with a minor release about each 3 months.
- Cross-compile with `cargo-zigbuild`. Build server images on a distroless base.
- Attach SBOMs and SLSA provenance attestations to every release.
- **macOS:** Sign with a Developer ID certificate, enable the hardened runtime, notarize with `notarytool`, and staple the ticket.
- **Windows:** Sign with an Authenticode certificate through a cloud HSM or signing service. Timestamp every signature.
- **Server rollback:** Keep the previous image tag. Make migrations backward-compatible for 1 release (expand, then contract).
- **Desktop rollback:** You cannot recall installed binaries. Fix forward through the updater, with staged rollouts (5%, 25%, 100%) and a remote kill switch.

## 20. Migrating an existing project to Rust

Migrate in small, reversible steps behind stable interfaces. Build the target architecture from the first Rust crate, not after the port.

### 20.1 Phase 0: Decide

Do not migrate when any of these is true:

- The current system meets its targets, and the team has no Rust experience.
- The main problem is product scope or data quality, not the language.
- A critical dependency has no Rust equivalent and no stable FFI path.
- GPUI cannot meet your accessibility requirements.

### 20.2 Phase 1: Baseline and characterization tests

1. Record current behavior as black-box golden tests: HTTP pairs, CLI output, exit codes, and files.
2. Run these tests against the old and new implementations in CI.
3. Measure p50/p99 latency, memory, startup time, and error rate.
4. Write the target architecture (sections 5 and 6) as ADRs before you write code.

### 20.3 Phase 2: Create the Rust workspace

1. Create the workspace with `core`, `core-ports`, 1 domain crate, and all CI gates.
2. Port the domain rules first, as pure functions, with the Phase 1 tests.
3. Keep wire formats, database schemas, config formats, CLI flags, and exit codes the same.

### 20.4 Phase 3: Replace incrementally

| Source language         | Bridge                             | Notes                                                     |
| ----------------------- | ---------------------------------- | --------------------------------------------------------- |
| Python                  | PyO3 + maturin                     | Move hot or risky modules into a Rust extension first.    |
| TypeScript / Node.js    | napi-rs                            | Ship a native addon, or move a whole service behind HTTP. |
| Go                      | HTTP/gRPC boundary (tonic)         | Avoid cgo bridges. Split by service.                      |
| Java / Kotlin           | UniFFI (Kotlin), JNI, or gRPC      | Prefer a service boundary on servers.                     |
| Swift                   | UniFFI                             | Generate Swift bindings for a shared Rust core.           |
| C                       | cbindgen, bindgen                  | Isolate all `unsafe` in 1 `*-ffi` crate.                  |
| C++                     | cxx, autocxx                       | Use cxx for a narrow, typed bridge.                       |
| Any (browser or plugin) | WebAssembly (`wasm-bindgen`, WASI) | Use for sandboxed plugins or shared validation.           |

- **Servers:** Use the strangler-fig pattern. Put a proxy in front and route 1 endpoint at a time to Rust. Compare responses in shadow mode before you switch.
- **CLIs:** Replace 1 subcommand at a time. The old CLI can call the new binary until all commands move.
- **Desktop:** Move the core into Rust first and call it through UniFFI or FFI. Replace the UI last.

### 20.5 Phase 4: Data migration

- Keep the old schema until the Rust service owns all writes.
- Use expand-and-contract migrations. Run dual writes only with a reconciliation job.
- Verify row counts and checksums after every backfill.

### 20.6 Porting idioms and team ramp-up

- Replace exceptions with `Result<T, E>` and `thiserror` enums. Replace `null` with `Option<T>`.
- Replace inheritance with traits. Replace global singletons with values built in the composition root.
- Replace implicit async or goroutines with explicit Tokio tasks, `JoinSet`, and cancellation.
- Give each developer 2 weeks with _The Rust Programming Language_ and small domain tasks. Pair them with experienced reviewers for the first 3 months.

## 21. New project checklist

**Foundation**

- [ ] Create a virtual workspace with `resolver = "3"` and edition 2024.
- [ ] Pin the toolchain to 1.99.1 (or 1.100.x after review).
- [ ] Add `[workspace.lints]` with `unsafe_code = "forbid"` and `clippy::unwrap_used = "deny"`.
- [ ] Commit `Cargo.lock`. Set `global-min-publish-age` once you use Cargo 1.100+.
- [ ] Add `deny.toml`, initialize `cargo vet`, and add `docs/adr/`.

**Core crates**

- [ ] Create `core` and `core-ports` with `Clock`, `IdGenerator`, and `Random`.
- [ ] Create the first `<feature>-domain` crate with a pure reducer, and `crates/testing` with fakes.

**Quality gates**

- [ ] CI runs `cargo fmt --check` and clippy with `CARGO_BUILD_WARNINGS=deny`.
- [ ] CI runs `cargo nextest run` and `cargo llvm-cov` with a 90% domain gate.
- [ ] CI runs `cargo deny check`, `cargo audit`, and `cargo vet` on Linux, macOS, and Windows.

**First feature**

- [ ] Parse all input into domain types at the edge.
- [ ] Add a repository trait, a fake, and 1 live adapter.
- [ ] Add 1 HTTP route, 1 CLI subcommand, or 1 GPUI view with `id`, `role`, and a label.
- [ ] Test accessibility: `NO_COLOR` and `--json` (CLI), screen reader and keyboard (desktop).

**First release**

- [ ] Build with `cargo auditable`. Generate a CycloneDX SBOM.
- [ ] Sign and notarize desktop builds. Write a rollback runbook.
- [ ] Tag with SemVer and publish a changelog.

## 22. Trade-offs and thresholds

The default decisions are the versions in the section 1 baseline: workspace layout, Tokio, axum, reqwest with rustls + aws-lc-rs, tonic, sqlx/PostgreSQL, rusqlite/SQLite, thiserror + anyhow, tracing, and `Arc<dyn Trait>` at roots. Change a default only when a condition below is true.

| Condition                                                                    | Change                                                         |
| ---------------------------------------------------------------------------- | -------------------------------------------------------------- |
| More than 1 binary, or more than about 5,000 lines                           | Move from 1 crate to a workspace.                              |
| A CLI needs more than about 10 concurrent network calls                      | Move the CLI from sync to Tokio.                               |
| You need multi-writer access, more than 1 server node, or row-level security | Move from SQLite to PostgreSQL.                                |
| A profiler shows dynamic dispatch above 5% of CPU in a hot loop              | Move from `dyn Trait` to generics there.                       |
| FFI, or a measured hot path with Miri-clean tests                            | Allow `unsafe` in 1 isolated crate with `// SAFETY:` comments. |
| A dependency has no release for 18 months and an open RustSec advisory       | Replace or fork it.                                            |

## 23. When a tool in this guide does not cover a need

This guide gives 1 tool or pattern for each need. If one does not cover your need, find the solution yourself.

1. Read the current documentation of the tool. Make sure that the gap is real.
2. Try to solve the problem with the tools and patterns in this guide.
3. If that is not possible, find another solution. Put it behind a port (section 5.3), so that the domain core does not change.
4. Apply the priority order in section 2 and the dependency policy in section 3.3 to the new solution.

## Caveats

- Rust 1.100.0 is scheduled for November 12, 2026.\[2\]\[35\] Facts about 1.100 come from the draft release notes and may change.\[30\]
- The Cargo cooldown does not apply to a git dependency, so the pinned tag is the only control for GPUI.\[36\] Zed published tag `v1.28.1` on 2026-11-11.\[73\] Compile the examples against the exact tag that you pin.
- The versions and dates in this guide are from crates.io and from each project's repository on 2026-11-11. On that date, `insta` was 1.49.0 and `release-plz` was 0.4.3.
- On 2026-11-11, these releases were younger than a 7-day cooldown: rusqlite 0.42.0, tokio-rusqlite 0.9.0, cargo-audit 0.23.0, and cargo-cyclonedx 0.5.10.
- The Rust examples in sections 5, 6, 10, 12, and 13 compile on Rust 1.99.1, and they pass clippy with the section 6.4 lint table and `CARGO_BUILD_WARNINGS=deny`. The desktop example compiles at Zed tag `v1.28.1` on macOS. The server and CLI examples need stubs for the modules that they do not show. The examples have no run test, and the desktop example has no screen-reader test.

## Sources

1. [Announcing Rust 1.99.1](https://blog.rust-lang.org/2026/10/15/Rust-1.99.1/)
2. [Rust 1.100.0 pre-release testing - announcements - Rust Internals](https://internals.rust-lang.org/t/rust-1-100-0-pre-release-testing/24802)
3. [Releases · tokio-rs/tokio · GitHub](https://github.com/tokio-rs/tokio/releases)
4. [tokio/README.md, "LTS releases" · tokio-rs/tokio · GitHub](https://github.com/tokio-rs/tokio/blob/master/README.md)
5. [tokio/tokio/Cargo.toml at tokio-1.54.1, `rust-version = "1.85"` · tokio-rs/tokio · GitHub](https://github.com/tokio-rs/tokio/blob/tokio-1.54.1/tokio/Cargo.toml)
6. [axum/axum/CHANGELOG.md at main, "Unreleased" · tokio-rs/axum · GitHub](https://github.com/tokio-rs/axum/blob/main/axum/CHANGELOG.md)
7. [tokio-rs/axum · Discussions · GitHub](https://github.com/tokio-rs/axum/discussions)
8. [axum/axum/README.md at main, "Breaking changes" · tokio-rs/axum · GitHub](https://github.com/tokio-rs/axum/blob/main/axum/README.md)
9. [reqwest/CHANGELOG.md at master, v0.13.0 to v0.13.5 · seanmonstar/reqwest · GitHub](https://github.com/seanmonstar/reqwest/blob/master/CHANGELOG.md)
10. [Release v0.13.0 (2025-12-30) · seanmonstar/reqwest · GitHub](https://github.com/seanmonstar/reqwest/releases/tag/v0.13.0)
11. [rustls - Rust](https://rustls.dev/docs/rustls/index.html)
12. [Release v0.14.0 (2025-07-28) · grpc/grpc-rust · GitHub](https://github.com/grpc/grpc-rust/releases/tag/v0.14.0)
13. [SQLx 0.9.0 Released! · transact-rs/sqlx · Discussion #4271 · GitHub](https://github.com/transact-rs/sqlx/discussions/4271)
14. [sqlx-core - crates.io: Rust Package Registry](https://crates.io/crates/sqlx-core)
15. [RUSTSEC-2026-0459: `libsqlite3-sys` via C SQLite CVE-2026-119375 · rustsec/advisory-db · GitHub](https://github.com/rustsec/advisory-db/blob/main/crates/libsqlite3-sys/RUSTSEC-2026-0459.md)
16. [clap 4.6.7 - Docs.rs](https://docs.rs/crate/clap/latest)
17. [ratatui - crates.io: Rust Package Registry](https://crates.io/crates/ratatui)
18. [thiserror 2.0.21 - Docs.rs](https://docs.rs/crate/thiserror/latest)
19. [anyhow 1.0.104 - Docs.rs](https://docs.rs/crate/anyhow/latest)
20. [tracing-subscriber - crates.io: Rust Package Registry](https://crates.io/crates/tracing-subscriber)
21. [tracing 0.1.44 - Docs.rs](https://docs.rs/crate/tracing/latest)
22. [tracing-opentelemetry 0.34.0 - Docs.rs](https://docs.rs/crate/tracing-opentelemetry/latest)
23. [opentelemetry-otlp 0.33.1 dependencies - crates.io: Rust Package Registry](https://crates.io/crates/opentelemetry-otlp/0.33.1/dependencies)
24. [gpui-pre - crates.io: Rust Package Registry](https://crates.io/crates/gpui-pre)
25. [gpui-kit/Cargo.toml at main, the `gpui-pre` pin · longbridge/gpui-kit · GitHub](https://github.com/longbridge/gpui-kit/blob/main/Cargo.toml)
26. [gpui: publish a new crates.io release (0.2.2 predates PinchEvent) · Issue #66275 · zed-industries/zed · GitHub](https://github.com/zed-industries/zed/issues/66275)
27. [cargo-deny/README.md at main · EmbarkStudios/cargo-deny · GitHub](https://github.com/EmbarkStudios/cargo-deny/blob/main/README.md)
28. [cargo-cyclonedx - crates.io: Rust Package Registry](https://crates.io/crates/cargo-cyclonedx)
29. [cargo-auditable/README.md at master · rust-secure-code/cargo-auditable · GitHub](https://github.com/rust-secure-code/cargo-auditable/blob/master/README.md)
30. [Draft release notes for 1.100.0 · Issue #163811 · rust-lang/rust · GitHub](https://github.com/rust-lang/rust/issues/163811)
31. [Announcing Rust 1.100.0 by cuviper · Pull Request #2001 · rust-lang/blog.rust-lang.org · GitHub](https://github.com/rust-lang/blog.rust-lang.org/pull/2001)
32. [Demoting i686 Windows targets to std-only](https://blog.rust-lang.org/2026/10/02/demoting-i686-windows-targets-to-std-only/)
33. [Announcing Rust 1.97.0](https://blog.rust-lang.org/2026/07/09/Rust-1.97.0/)
34. [Configuration - The Cargo Book (beta): `registry.global-min-publish-age`, `resolver.incompatible-publish-age`](https://doc.rust-lang.org/beta/cargo/reference/config.html)
35. [rust/RELEASES.md at main, "Version 1.100.0 (2026-11-12)" · rust-lang/rust · GitHub](https://github.com/rust-lang/rust/blob/main/RELEASES.md)
36. [feat(resolver): Stabilize min-publish-age · Pull Request #17335 · rust-lang/cargo · GitHub](https://github.com/rust-lang/cargo/pull/17335)
37. [RUSTSEC-2026-0260: `arrayref` 0.3.10 was removed from crates.io due to a malicious dependency · rustsec/advisory-db · GitHub](https://github.com/rustsec/advisory-db/blob/main/crates/arrayref/RUSTSEC-2026-0260.md)
38. [rustsec/cargo-audit/README.md at main · rustsec/rustsec · GitHub](https://github.com/rustsec/rustsec/blob/main/cargo-audit/README.md)
39. [Importing Audits - Cargo Vet](https://mozilla.github.io/cargo-vet/importing-audits.html)
40. [Announcing a Maintainer in Residence: Scott Schafer for the Cargo team](https://blog.rust-lang.org/2026/09/22/announcing-a-maintainer-in-residence-scott-schafer-for-the-cargo-team/)
41. [GPUI](https://gpui.rs/)
42. [GPUI 2 is now in production (2024-01-03) - Zed Blog](https://zed.dev/blog/gpui-2-on-preview)
43. [Hacker News comment 47003569 (2026-02-13), which quotes and links the Zed Discord message](https://news.ycombinator.com/item?id=47003569)
44. [gpui\_kit - Rust](https://docs.rs/gpui-kit/latest/gpui_kit/)
45. [All Settings, "Accessible Mode" - Zed Docs](https://zed.dev/docs/reference/all-settings#accessible-mode)
46. [gpui\_macos: the app reports the window as the focused accessibility element, because AccessKit subclasses the content view instead of the first responder · Issue #66691 · zed-industries/zed · GitHub](https://github.com/zed-industries/zed/issues/66691)
47. [gpui: elements clipped out of view get accessibility nodes reported as visible · Issue #66730 · zed-industries/zed · GitHub](https://github.com/zed-industries/zed/issues/66730)
48. [rustls - Rust](https://docs.rs/rustls)
49. [Requirements - AWS-LC for Rust book · aws/aws-lc-rs · GitHub](https://github.com/aws/aws-lc-rs/blob/main/book/src/requirements/README.md)
50. [grpc-rust/examples/helloworld-tutorial.md at master · grpc/grpc-rust · GitHub](https://github.com/grpc/grpc-rust/blob/master/examples/helloworld-tutorial.md)
51. [password-hash CHANGELOG, 0.6.0 · RustCrypto/traits · GitHub](https://github.com/RustCrypto/traits/blob/master/password-hash/CHANGELOG.md)
52. [keyring-rs/README.md at main · open-source-cooperative/keyring-rs · GitHub](https://github.com/open-source-cooperative/keyring-rs/blob/main/README.md)
53. [Search results for "keyring credential store" - crates.io: Rust Package Registry](https://crates.io/search?q=keyring%20credential%20store)
54. [sqlx/CHANGELOG.md at main, 0.9.0 · transact-rs/sqlx · GitHub](https://github.com/transact-rs/sqlx/blob/main/CHANGELOG.md)
55. [rusqlite v0.38.0 release notes (2025-12-20) · rusqlite/rusqlite · GitHub](https://github.com/rusqlite/rusqlite/releases/tag/v0.38.0)
56. [secrecy - Rust](https://docs.rs/secrecy/latest/secrecy/)
57. [anyhow/README.md at master, "Comparison to thiserror" · dtolnay/anyhow · GitHub](https://github.com/dtolnay/anyhow/blob/master/README.md#comparison-to-thiserror)
58. [zed/crates/gpui/src/\_accessibility.rs at main · zed-industries/zed · GitHub](https://github.com/zed-industries/zed/blob/main/crates/gpui/src/_accessibility.rs)
59. [proptest 1.12.0 - Docs.rs](https://docs.rs/crate/proptest/latest)
60. [cargo-mutants - crates.io: Rust Package Registry](https://crates.io/crates/cargo-mutants)
61. [criterion 0.8.2 - Docs.rs](https://docs.rs/crate/criterion/latest)
62. [criterion 0.8.2 - Docs.rs](https://docs.rs/crate/criterion/latest/source/CHANGELOG.md)
63. [Introduction - release-plz](https://release-plz.dev/docs)
64. [Releases · axodotdev/cargo-dist · GitHub](https://github.com/axodotdev/cargo-dist/releases)
65. [zed/crates/gpui/README.md at main · zed-industries/zed · GitHub](https://github.com/zed-industries/zed/blob/main/crates/gpui/README.md)
66. [accesskit/README.md at main · AccessKit/accesskit · GitHub](https://github.com/AccessKit/accesskit/blob/main/README.md)
67. [Supply chain attack on arrayref - Rust Blog](https://blog.rust-lang.org/2026/08/20/supply-chain-attack-on-arrayref/)
68. [Be alert: targeted attacks on prominent Rustaceans - Rust Blog](https://blog.rust-lang.org/2026/09/17/targeted-attacks/)
69. [GitHub Actions leaking secrets when Miri output is cached - Rust Blog](https://blog.rust-lang.org/2026/09/21/github-actions-leaking-secrets-when-miri-output-is-cached/)
70. [Lints - The Cargo Book (beta)](https://doc.rust-lang.org/beta/cargo/reference/lints.html)
71. [gpui: Accesskit support · Pull Request #56065 · zed-industries/zed · GitHub](https://github.com/zed-industries/zed/pull/56065)
72. [zed/crates/gpui/examples/a11y.rs at main · zed-industries/zed · GitHub](https://github.com/zed-industries/zed/blob/main/crates/gpui/examples/a11y.rs)
73. [Release v1.28.1 (2026-11-11) · zed-industries/zed · GitHub](https://github.com/zed-industries/zed/releases/tag/v1.28.1)
74. [zed/crates/gpui/src/elements at v1.28.1 · zed-industries/zed · GitHub](https://github.com/zed-industries/zed/tree/v1.28.1/crates/gpui/src/elements)
75. [zed/crates/gpui/src/app.rs at v1.28.1 · zed-industries/zed · GitHub](https://github.com/zed-industries/zed/blob/v1.28.1/crates/gpui/src/app.rs)
