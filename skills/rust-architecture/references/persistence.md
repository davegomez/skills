# Persistence

Put every store behind a repository trait. Select the store from the _store profile_ of the project, and use the simplest store that meets it.

## Store profile

Write these 6 facts before you select a store or a host. Take each fact from the project, not from a forecast.

- **Writers:** how many processes and nodes write at the same time, also during a deploy.
- **Disk:** whether the host keeps a local disk after a restart, a deploy, and a scale-in.
- **Unit of work:** whether a write reads rows, computes in the program, and then writes as 1 atomic unit, and whether the units of different tenants run at the same time.
- **Idle hours:** the hours each day with no request to the store. A poll and a health check are requests.
- **Guarantees:** the recovery point, the uptime agreement, the network isolation, and the audit that the project must have.
- **Budget:** the monthly cost that the project accepts while it has few users.

The profile is complete when each fact has a value and its source. Write the profile and each selection in a decision record.

## Select the store

| Profile | Use | Notes |
| --- | --- | --- |
| User config | TOML file through `serde` | Store under the OS config directory. |
| Data of 1 process on its own machine: CLI, desktop, mobile library | SQLite through `rusqlite` (sync) | Use the `bundled` feature. |
| Server data on 1 node with a durable disk and 1 writer process | SQLite through `rusqlite`, replicated to object storage with Litestream | Litestream replicates asynchronously, so a crash can lose the last second of writes. Exactly 1 process replicates. |
| Server data with more than 1 writer, more than 1 node, or a host with no durable disk | PostgreSQL through `sqlx` | Compile-time checked queries and migrations. |

A profile with no row is _out of bounds_, for example writes in more than 1 region, 1 database for each tenant, or a store that the platform prescribes.

## Select the PostgreSQL host

| Profile | Host class |
| --- | --- |
| Idle most of the day, a budget near zero, and a first request after an idle time that can wait | A host that scales to zero and bills for use |
| Requests most of the day, or a guarantee that needs an uptime agreement, a private network path, or database audit | A managed instance in the cloud and the region of the server |

- Count the idle hours from the real request pattern. A client that polls keeps the store awake while 1 user is active.
- Compare the 2 classes at the same size. A host that bills for use costs more than an always-on instance when it is awake all day.
- Read what the vendor says about its smallest tier. Use a tier that the vendor excludes from production for tests only.
- Use the same host class for staging and production.
- Select the host again when a threshold in [deviations](deviations.md) applies.

## Keep the exit open

With these rules, a move to a different host is a restore and a change of configuration.

- Use standard PostgreSQL only: the `sqlx` driver, a standard connection string, and TLS that verifies the server. Keep vendor extensions, vendor drivers, and vendor APIs out of the request path.
- Use a major version that the 2 host classes offer.
- Lock at transaction level: `SELECT ... FOR UPDATE` or `pg_advisory_xact_lock`. A pooler in transaction mode drops a session-level lock.
- Write a `pg_dump` to storage that you own on a schedule. Restore it to a scratch database on a schedule, and record the time.
- Move with a dump and a restore when the recorded time is less than the downtime that the project accepts. Move with logical replication when it is more.

## Rules

- **Unit of work:** Take the lock of the tenant in the first statement of the transaction. PostgreSQL uses Read Committed by default, so 2 reads in 1 transaction can see different data.
- **sqlx:** `query*()` functions take a type that implements `SqlSafeStr`, which makes SQL injection harder. Use the `runtime-tokio` feature plus the `tls-rustls-aws-lc-rs` feature.
- **sqlx behind a pooler:** `sqlx` always uses prepared statements. Behind PgBouncer in transaction mode, set `max_prepared_statements` above 0, or connect directly, or set `.persistent(false)` on each query.
- **sqlx-cli:** Install it with `cargo install --locked sqlx-cli@<the sqlx version>`. The crate on crates.io carries the `Cargo.lock` that Cargo wrote at publish time, and `--locked` uses it. The project does not maintain that file, so read the warnings of the install: on 2026-11-19 the lockfile of 0.9.0 pinned 4 yanked packages.
- **SQLite files:** Keep a SQLite file on a local disk. On a network file system or an object storage mount, the file locks are not reliable and the file can corrupt.
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
