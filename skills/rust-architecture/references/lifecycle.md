# Process lifecycle, background work, and platform integration

Every binary must start cleanly, report health, stop cleanly on a signal, and exit with a meaningful code.

**Server composition root**

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
        .route("/health/live", get(|| async { "ok" }))
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

- `/health/live` reports that the process is alive. Add `/health/ready` to report that dependencies are reachable. Name each health route with a path that does not end in `z`: Cloud Run reserves some paths that end in `z`, and a request to `/healthz` there gets the 404 page of the platform and never reaches the container.
- In containers, run as a non-root user and use a read-only root filesystem.

**CLI composition root**

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

**Desktop composition root and minimal GPUI view**

The example uses Zed's `gpui` and `gpui_platform` crates at the tag in the workspace manifest.

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

- Start the app with `gpui_platform::application()`. It selects the window and text backends for the host OS.
- The example on gpui.rs starts with `Application::new()`. Copy startup code only after you find it in the source at the pinned tag.
- `.id(...).role(Role::...)` is the GPUI accessibility API. Without both, screen readers see nothing. `.aria_label(...)` gives the node its name. A text child does not.

**Warning:** On macOS, the `gpui_platform` build compiles the Metal shaders. Without the Metal toolchain of Xcode, the build stops with "missing Metal Toolchain". Install it with `xcodebuild -downloadComponent MetalToolchain`.
