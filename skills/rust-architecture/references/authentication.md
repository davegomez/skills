# Authentication and identity

Use server-side sessions for browser clients, and short-lived tokens for CLI, desktop, and API clients. Use the OAuth device flow for CLIs, and OS credential stores for CLI and desktop secrets.

- **Server sessions:** For browser clients, use opaque session IDs stored server-side. Set cookies with `Secure`, `HttpOnly`, and `SameSite=Lax` or `Strict`.
- **JWT:** Pin the algorithm, check `exp`, `nbf`, `aud`, and `iss`, and keep lifetimes short. Never accept `alg: none`. Use the `oauth2` and `openidconnect` crates for OAuth 2.0 and OIDC.
- **Passwords:** Hash with `argon2` (Argon2id).

**Warning:** Before you upgrade `argon2` across a breaking release, test that hashes from the current release still verify.

- **CLI:** Use the OAuth 2.0 device authorization grant. Store refresh tokens in the OS keychain.
- **Desktop:** Use the same keychain crates. Use the system browser with authorization code + PKCE. Do not embed a login webview.
- **Keychain crates:** Depend on `keyring-core` and the platform store crates: `apple-native-keyring-store`, `windows-native-keyring-store`, and `zbus-secret-service-keyring-store` (Linux).
