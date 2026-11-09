# Authentication and identity

Put authentication behind an `AuthClient` protocol in `Core`. Prefer passkeys and Sign in with Apple over passwords.

- Use the `AuthenticationServices` framework for passkeys, Sign in with Apple, and password AutoFill.
- Use `ASWebAuthenticationSession` with OAuth 2.0 and PKCE for third-party identity providers. Do not use an embedded web view for sign-in.
- If you offer third-party sign-in, offer a login option that meets App Review Guideline 4.8.
- Store tokens in the Keychain. Refresh them in 1 place, and serialize refresh calls through an actor.
- Treat a `401` response as a signal to refresh once. If the refresh fails, sign the user out cleanly.
- Clear all user data, caches, and Keychain items on sign-out.
- If the app supports account creation, provide account deletion inside the app. App Review requires it.
- Use `LocalAuthentication` (Face ID, Touch ID) only to unlock a local secret. Do not use it as proof of identity to your server.

If the app has no accounts, still define the `AuthClient` seam with a no-op default. You can then add accounts later without changes to feature code.
