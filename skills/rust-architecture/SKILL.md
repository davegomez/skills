---
name: rust-architecture
description: Rust app architecture. Use before writing, changing, or reviewing Rust code, Cargo manifests, or workspace config for a server, CLI, or desktop app.
metadata:
  internal: true
---

# Rust app architecture

Every Rust server, CLI, and GPUI desktop app uses 1 architecture: a pure domain core inside an imperative shell. This file holds the invariants every task needs. Each file in `references/` holds the rules for 1 concern.

## Invariants

- **Shell:** Each binary crate is the composition root. It builds the object graph, reads config, and starts the runtime. It holds no business rules.
- **Domain:** Domain crates hold types, rules, and reducers. They do no I/O, read no clock, and use no global state.
- **Presentation and adapters:** HTTP handlers, CLI commands, and GPUI views translate input into domain commands, then render the results.
- **Services:** Every side effect (database, network, clock, RNG, UUIDs, keychain) sits behind a port trait with a live adapter and a fake adapter.
- **Concurrency:** The server uses Tokio. The CLI stays synchronous unless it needs many concurrent network calls. The desktop app uses the GPUI executors plus 1 dedicated Tokio runtime.
- **Quality gates:** CI runs rustfmt, clippy with warnings denied, nextest, a 90% domain coverage gate, cargo-deny, cargo-audit, cargo-vet, and SBOM generation.

The invariants apply to all 3 app types. Only the shell and the adapters change between the server, the CLI, and the desktop app.

**Platform baseline:** The latest stable Rust release and edition, and the latest release of each crate and tool that is older than the dependency cooldown in [project setup](references/project-setup.md). Find these versions when you do the work. The versions in the examples show the format, not the version to use.

## Priority order

Apply this order to every decision. When 2 goals conflict, the higher priority wins.

1. **Security**
2. **Reliability**
3. **Accessibility**
4. **Maintainability**
5. **Performance:** Optimize only after you measure it.

Examples: Wait for the dependency cooldown on a 1-day-old release that fixes a bug; for an urgent security fix, use the override in [project setup](references/project-setup.md). Keep safe code when `unsafe` gives a 15% speed-up in a parser. Print 1 status line per state change instead of a spinner that screen readers repeat.

## Process

1. **Gate.** Load this skill in every agent and subagent before it reads or edits Rust code. When you delegate Rust work, make this the first line of the subagent prompt: `Invoke the rust-architecture skill before you read or edit code.` The gate is complete when the skill is loaded in each context that edits code.
2. **Route.** List every concern the change touches, and match each to a row of the route table. The step is complete when each concern has a row or is marked _out of bounds_.
3. **Read.** Read each matched reference in full, and only the matched references.
4. **Apply.** Write or review the change against the rules of each matched reference. Change a default only when a _threshold_ in [deviations](references/deviations.md) applies, and name that threshold in the reply. A default change with no matching threshold is _out of bounds_.
5. **Out of bounds.** For each out-of-bounds concern, read the current documentation of the tool, and make sure the gap is real. Try the tools and patterns of this skill first. If they cannot meet the need, research a solution in primary sources: the tool's own documentation and source, the Cargo Book, the Rust Reference and release notes, and the RustSec advisory database. Put the solution behind a port, so that the domain core does not change. Apply the priority order and the dependency policy in [project setup](references/project-setup.md). Write a short _decision record_ in `docs/adr/`. Record the problem, the solution, the sources, and the priority the solution serves. The step is complete when each out-of-bounds concern has a decision record with sources, named in the reply.
6. **Check.** Before you report done, check the diff against every rule of each matched reference. The work is complete when each rule is met, or the reply names the rule and why it does not apply.

## Route table

| The change touches | Read |
| --- | --- |
| A new workspace, the toolchain pin, Cargo config, lints, a new dependency, supply-chain tools | [project setup](references/project-setup.md) |
| A crate, domain or reducer code, port traits, dependency injection, the workspace manifest, the feature registry | [architecture](references/architecture.md) |
| GPUI views or components, a TUI, CLI terminal output | [UI framework](references/ui-framework.md) |
| HTTP routes, CLI arguments and subcommands, GPUI navigation, dropped or opened files | [routing and input](references/routing-input.md) |
| HTTP servers or clients, middleware, TLS, gRPC, timeouts, retries | [networking](references/networking.md) |
| Sign-in, sessions, JWTs, passwords, stored credentials | [authentication](references/authentication.md) |
| Stored data, the selection of a store or a database host, SQL, schemas, migrations, pools, config files | [persistence](references/persistence.md) |
| Secrets, `unsafe`, FFI, input across a trust boundary, error messages, logs, randomness, regulated data | [security and privacy](references/security-privacy.md) |
| Async code, Tokio, locks, blocking work, task groups, GPUI with Tokio, error types | [concurrency](references/concurrency.md) |
| A `main` function, startup, health checks, signals, shutdown, exit codes, containers | [lifecycle](references/lifecycle.md) |
| Any GPUI view, CLI output, or API error response | [accessibility](references/accessibility.md) |
| Any text the user sees, numbers, dates, plural rules | [localization](references/localization.md) |
| Any code change | [testing](references/testing.md) |
| Logs, traces, profiling, benchmarks | [observability and performance](references/observability-performance.md) |
| Authorization, telemetry, feature flags, entitlements, notifications, diagnostics | [seams](references/seams.md) |
| Versions, release builds, installers, signing, SBOMs, rollouts, rollback | [release](references/release.md) |
| An existing project in another language, a port to Rust, FFI bridges, data migration | [migration](references/migration.md) |
| A change to a default, a choice between patterns or stores | [deviations](references/deviations.md) |
