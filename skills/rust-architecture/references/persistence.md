# Persistence

Put every store behind a repository trait. Use SQLite for local data and PostgreSQL for shared server data.

| Need | Choice | Notes |
| --- | --- | --- |
| User config | TOML file through `serde` | Store under the OS config directory. |
| Local relational (CLI, desktop) | `rusqlite` (sync) | Use the `bundled` feature. |
| Server relational | `sqlx` with PostgreSQL | Compile-time checked queries and migrations. |

- **sqlx:** `query*()` functions take a type that implements `SqlSafeStr`, which makes SQL injection harder. Use the `runtime-tokio` feature plus the `tls-rustls-aws-lc-rs` feature.
- **sqlx-cli:** The `sqlx-cli` package has no `Cargo.lock`, so `cargo install --locked sqlx-cli` does not work. In CI, pin the version with `cargo install sqlx-cli --version <the sqlx version>`. For a reproducible build, keep your own lockfile.
- **rusqlite:** Turn on the `fallible_uint` feature to use `FromSql` for `u64`.
- **rusqlite in async code:** `rusqlite` is synchronous. In Tokio code, call it in `spawn_blocking` (see [concurrency](concurrency.md)) or through `tokio-rusqlite`, which runs each connection on its own thread. Each `tokio-rusqlite` release requires 1 `rusqlite` release line, so select the 2 versions together.
- Run server migrations as a separate, explicit step. Test every migration against production-shaped data in CI.
- Use pools with a maximum size and an acquire timeout. Encrypt data at rest. Use SQLCipher if a local file holds regulated data.

**Warning:** The rusqlite `bundled-sqlcipher` feature builds a different SQLite from the `bundled` feature, and a release that fixes a RustSec advisory for `bundled` can still build an affected SQLCipher. Read the open `libsqlite3-sys` advisories before you ship `bundled-sqlcipher`.

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
