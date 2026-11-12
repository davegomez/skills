# Architecture and crates

## Application architecture pattern

Use functional core / imperative shell inside a hexagonal (ports-and-adapters) layout. Put rules in pure reducers. Put effects in adapters behind traits.

| Pattern | Use when | Do not use when |
| --- | --- | --- |
| Functional core / imperative shell | Always. This is the default. | Never skip it. |
| Hexagonal (ports and adapters) | The app has 2 or more I/O systems, or more than 1 binary. | You have a 200-line script. |
| Reducer (state, action) → (state, effects) | You have a UI state machine, a workflow, or CLI wizard state. | You have a stateless CRUD path. |
| Actor (task + channel) | You need long-lived state shared across tasks. | A `Mutex` around a small struct is enough. |
| CQRS / event sourcing | Audit or replay is a hard requirement. | You only want it because it looks clean. |

**Rules for pure domain crates**

- Do no I/O, no `async`, no `SystemTime::now()`, no random numbers, and no logging.
- Depend only on `std`, `thiserror`, and small value crates.
- Make illegal states unrepresentable with newtypes and enums. Parse raw input into types such as `Sku` with `TryFrom<&str>` at the edge.
- Return `Result` with domain error enums. Never panic on input.

**Pure reducer example**

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

**Dependency injection with traits**

- Use **generics** (`impl<R: OrderRepo>`) inside libraries and hot paths for static dispatch.
- Use **`Arc<dyn Trait>`** in composition roots and app state for simpler types and faster builds.
- `async fn` in traits is stable, but such traits are not dyn-compatible. For `dyn` ports with async methods, return `Pin<Box<dyn Future + Send>>`, as `BoxFut` does in [persistence](persistence.md).
- Put `Send + Sync` bounds on ports that the server or GPUI background tasks use.

**Inject the clock, RNG, and UUIDs (live and fake adapters)**

```rust
// crates/core-ports/src/lib.rs
pub mod orders; // persistence.md
pub mod random; // concurrency.md

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

## Modularization with a Cargo workspace

Use 1 virtual workspace. Binaries are composition roots. Domain crates depend only on `core`. Adapters depend on ports, and ports never depend on adapters.

**Crate roles**

| Crate | Role | May depend on | Must not depend on |
| --- | --- | --- | --- |
| `apps/server` | Composition root for HTTP/gRPC | all except UI crates | `gpui*` |
| `apps/cli` | Composition root for the CLI | all except UI crates | `gpui*` |
| `apps/desktop` | Composition root for GPUI | all except server crates | `axum`, `tonic`, `feature-contract` |
| `crates/core` (package `app-core`) | Shared value types and errors | std, thiserror | any adapter |
| `crates/core-ports` | Port traits (Clock, Random, repos) | core | any adapter |
| `crates/feature-contract` | Feature trait and registry for the server and the CLI | core-ports, `axum`, `clap` | adapters, `gpui*` |
| `crates/<feature>-domain` | Pure rules and reducers | core | I/O crates, async runtimes |
| `crates/<feature>-app` | Use cases that orchestrate ports | domain, core-ports | concrete adapters |
| `crates/adapter-*` | Postgres, SQLite, HTTP client implementations | core-ports | other adapters |
| `crates/ui-desktop-<feature>` | GPUI views for 1 feature | feature-app | adapters |
| `crates/testing` | Fakes and fixtures (dev-only) | core-ports | — |

**Dependency rules**

- Dependencies point inward only. Binaries → UI crates → `*-app` → `*-domain` → `core`. Binaries → adapters → `core-ports` → `core`. The `*-app` crates also use `core-ports`. Enforce this in CI with `cargo deny check bans`.
- Give the shared crate the package name `app-core`, not `core`. A dependency with the name `core` hides the built-in `core` crate. Derive macros such as `thiserror::Error` then fail with "cannot find `fmt` in `core`".
- Keep items `pub(crate)` by default. Export only the minimal API from each `lib.rs`.
- Name crates `<area>-<role>`, for example `orders-domain`, `orders-app`, or `adapter-postgres`.
- All 3 binaries share `orders-app` and `orders-domain`. Build each one alone with `cargo build -p server` or `cargo build -p desktop`.

**Directory tree**

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

**Workspace `Cargo.toml`**

The versions and the GPUI tag in this manifest show the format. Select each version with the platform baseline in [the skill](../SKILL.md).

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
gpui = { git = "https://github.com/zed-industries/zed", tag = "v1.28.1" }   # read ui-framework.md first
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

**Member `Cargo.toml`**

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

**Feature contract and registry**

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
