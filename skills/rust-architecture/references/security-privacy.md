# Security and privacy

Forbid `unsafe` by default, gate every dependency, parse all input into typed values, and keep secrets and PII out of logs.

- **Secrets:** Load them from a secrets manager on servers, and from the OS keychain in CLI and desktop apps. Wrap them in `secrecy::SecretString` and call `expose_secret()` only at the point of use. `secrecy` uses `SecretBox<S>`. Use `zeroize` for key material that you own.
- **Unsafe:** Set `unsafe_code = "forbid"`. If FFI needs `unsafe`, isolate it in 1 `*-ffi` crate and override the lint there only. Write a `// SAFETY:` comment on every block. Run Miri on that crate. Run `cargo geiger` to report `unsafe` in dependencies.
- **Supply chain:** Run `cargo deny check`, `cargo audit`, and `cargo vet` on every pull request. Build releases with `cargo auditable build` and `--locked`. Attach CycloneDX SBOMs.

**Warning:** Give no secrets to a CI job that runs Miri and writes a cache, because the cache can keep environment variables that Miri stored in `target/`. If such a job had secrets, clear its caches and rotate those secrets.

- **Parse, don't validate:** Convert raw strings into domain types (`Sku`, `OrderId`, `Quantity`) with `TryFrom` at the trust boundary. After that, functions accept only the typed values.
- **Errors and logs:** Send generic messages to users ("Request failed. Reference: 7f3a…"). Log the details with the same reference. Log IDs, not names, emails, or tokens.
- **Randomness:** Use the OS CSPRNG (`getrandom`) for tokens and keys. Never use a seeded RNG for security values.
- **Regulated data (not legal advice):** For GDPR, collect the minimum and support export and deletion. For HIPAA, encrypt PHI and keep access audit logs. For PCI DSS, do not store card numbers; use provider tokenization. Ask a compliance professional before you ship.
