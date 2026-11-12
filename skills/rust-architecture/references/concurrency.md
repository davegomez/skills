# Concurrency and reliability

Use Tokio for servers, synchronous code for most CLIs, and the GPUI executors for desktop UI work. Never block an async thread and never hold a lock across `.await`.

- **Runtime:** Tokio is the default. For a fixed minor version, use a Tokio LTS line that is still in support. async-std is discontinued; use Tokio.
- **Locks:** Use `std::sync::Mutex` for short, non-async critical sections. Prefer a message-passing task over `tokio::sync::Mutex`.
- **Blocking work:** Move CPU-heavy or blocking work to `spawn_blocking`.
- **Structured concurrency:** Use `JoinSet` for task groups. Use `TaskTracker` with `CancellationToken` for graceful shutdown. Never detach a `tokio::spawn` without a tracker.
- **GPUI and Tokio:** GPUI has its own foreground and background executors and does not run Tokio. Tokio-based crates (reqwest, sqlx, tonic) need a runtime. Start 1 Tokio runtime at startup, store its `Handle`, spawn network work on it, and await the result in a GPUI task through a `tokio::sync::oneshot` channel. Zed's internal `gpui_tokio` bridge is not a stable public API.
- **Errors:** Use `thiserror` in libraries and domain crates (see `OrderError` in [architecture](architecture.md) and `RepoError` in [persistence](persistence.md)). Use `anyhow` only in binaries, with `.context(...)`. Never `unwrap()` external data. Keep `panic = "unwind"` on servers and catch panics at the task boundary.

**Deterministic RNG**

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
