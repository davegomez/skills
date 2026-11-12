# Testing

Write tests first for domain rules, prefer fakes over mocks, and gate CI on coverage and mutation results for domain crates.

| Layer | Tool | Gate |
| --- | --- | --- |
| Domain unit | built-in `#[test]`, run with cargo-nextest | 90%+ line coverage (cargo-llvm-cov) |
| Domain properties | proptest | Required for parsers and reducers |
| Mutation | cargo-mutants | No surviving mutants in domain crates (weekly) |
| Snapshots | insta | Review snapshot diffs in the pull request |
| CLI | `assert_cmd` + `trycmd` | Golden tests for help, exit codes, and `--json` |
| HTTP | `tower::ServiceExt::oneshot` on the `Router` | Every route: success, 400, 401, 404 |
| Database | `testcontainers` (PostgreSQL), temp-file SQLite | Every migration on a clean database |
| GPUI | `#[gpui::test]` with the `test-support` feature | View logic only. Accessibility needs manual tests. |
| Fuzzing | cargo-fuzz | Every parser of external input, nightly CI |
| Unsafe / concurrency | Miri / loom | Every `unsafe` crate / custom sync primitives |
| Benchmarks | criterion | Track regressions (see [observability and performance](observability-performance.md)) |

- criterion is maintained in the `criterion-rs` organization.
- CI matrix: Linux x86_64 and aarch64, macOS aarch64, Windows x86_64. Build the GPUI binary on all 3 desktop OSes.
