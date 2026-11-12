# Project setup

## Project setup and toolchain

Pin the toolchain, commit `Cargo.lock`, and gate CI on lint, test, and supply-chain checks from the first commit.

**Toolchain**

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

**Warning:** Move the pin to a new Rust release only after you read its final release notes. Release notes list compatibility changes, such as type inference changes, that can break the build.

- Build 32-bit Windows binaries from a 64-bit host.
- Use `CARGO_BUILD_WARNINGS=deny` in CI instead of `RUSTFLAGS=-Dwarnings`. This keeps the build cache valid. It applies to `cargo clippy` too.

**Edition, resolver, and MSRV**

- Use the latest stable edition for all crates.
- Set `resolver = "3"` in the virtual workspace manifest, because a virtual manifest has no edition.
- For apps, set `rust-version` equal to the pinned toolchain. For published libraries, support at least the previous 2 stable versions.
- Each crate sets its own MSRV. Check dependency MSRVs before you upgrade.

**Config and dependency policy**

- Load config in this order: defaults, config file, environment variables, CLI flags. Parse it into typed structs at startup. Stop if it is not valid.
- Commit `Cargo.lock` for every application workspace.
- Add a dependency only after you check maintenance activity, RustSec history, license, and transitive dependency count.
- When the pinned Cargo supports the dependency cooldown (`registry.global-min-publish-age`), turn it on. The default is 0, so a toolchain upgrade alone does not protect you.

```toml
# .cargo/config.toml (needs Cargo 1.100+)
[registry]
global-min-publish-age = "7 days"
```

- A cooldown keeps a malicious release out of your build when the registry removes it before the cooldown ends.
- Cargo keeps versions that are already in `Cargo.lock`. The cooldown does not apply to `cargo install`, or to git and path dependencies.
- For 1 registry only, set `registries.<name>.min-publish-age`.
- For urgent security fixes, override it for 1 command with `CARGO_RESOLVER_INCOMPATIBLE_PUBLISH_AGE=allow`.

**Supply-chain tools**

| Tool | Purpose |
| --- | --- |
| cargo-deny | Checks licenses, bans, duplicates, sources, and advisories. |
| cargo-audit | Checks `Cargo.lock` and binaries (`cargo audit bin`) against RustSec. |
| cargo-vet | Records human audits. Imports audits from Mozilla, Google, and others. |
| cargo-auditable | Embeds the dependency list in the binary. |
| cargo-cyclonedx | Generates CycloneDX SBOMs. |

Use cargo-vet as the trust tool.

**Lints, formatting, and decision records**

- Define lints once in `[workspace.lints]`. Add `[lints] workspace = true` to every member.
- When the pinned Cargo supports its own lint table (`[lints.cargo]`), set `unused_dependencies` to `"deny"` in `[workspace.lints.cargo]`. It warns by default.
- Store Architecture Decision Records in `docs/adr/NNNN-title.md`. Write 1 record for each choice in [deviations](deviations.md).

## New project checklist

Complete this checklist for every new workspace.

**Foundation**

- [ ] Create a virtual workspace with `resolver = "3"` and the latest stable edition
- [ ] Pin the toolchain to the latest stable Rust release, after you read its release notes
- [ ] Add `[workspace.lints]` with `unsafe_code = "forbid"` and `clippy::unwrap_used = "deny"`
- [ ] Commit `Cargo.lock`. Set `global-min-publish-age` when the pinned Cargo supports it
- [ ] Add `deny.toml`, initialize `cargo vet`, and add `docs/adr/`

**Core crates**

- [ ] Create `core` and `core-ports` with `Clock`, `IdGenerator`, and `Random`
- [ ] Create the first `<feature>-domain` crate with a pure reducer, and `crates/testing` with fakes

**Quality gates**

- [ ] CI runs `cargo fmt --check` and clippy with `CARGO_BUILD_WARNINGS=deny`
- [ ] CI runs `cargo nextest run` and `cargo llvm-cov` with a 90% domain gate
- [ ] CI runs `cargo deny check`, `cargo audit`, and `cargo vet` on Linux, macOS, and Windows

**First feature**

- [ ] Parse all input into domain types at the edge
- [ ] Add a repository trait, a fake, and 1 live adapter
- [ ] Add 1 HTTP route, 1 CLI subcommand, or 1 GPUI view with `id`, `role`, and a label
- [ ] Test accessibility: `NO_COLOR` and `--json` (CLI), screen reader and keyboard (desktop)

**First release**

- [ ] Build with `cargo auditable`. Generate a CycloneDX SBOM
- [ ] Sign and notarize desktop builds. Write a rollback runbook
- [ ] Tag with SemVer and publish a changelog
