# Purchases and cross-cutting seams

Put each cross-cutting concern behind a protocol with a safe default. Check entitlements in 1 place, in the shell.

| Seam | Protocol | Default |
| --- | --- | --- |
| Entitlements | `EntitlementService` | Entitled in debug builds; denied in release builds until StoreKit verifies a transaction |
| Authentication | `AuthClient` | Signed-out, no-op |
| Analytics | `AnalyticsClient` | No-op |
| Feature flags | `FeatureFlagProvider` | Compiled defaults |
| Diagnostics | `DiagnosticsClient` | `os.Logger` with privacy annotations |
| Notifications | `NotificationClient` | No-op |

The shell gates each feature through its `requirement` property. Feature and domain code never check purchases.

**StoreKit 2**

- Create 1 `@MainActor @Observable` store service in the shell.
- Start a `Transaction.updates` listener at launch, and keep it for the life of the app. Otherwise you miss renewals, refunds, Ask to Buy approvals, and purchases from other devices.
- Read `Transaction.currentEntitlements` at launch to build the entitlement state.
- Use only `.verified` transactions. StoreKit 2 verifies the JWS signature for you.
- Call `transaction.finish()` after you deliver the content.
- Provide a Restore Purchases action that calls `AppStore.sync()`. App Review requires it for restorable purchases. Call `sync()` only from a user action, because it shows an App Store sign-in prompt.
- Use `SubscriptionStoreView` and `ProductView` for standard paywalls.
- Use `AppTransaction` to check the original purchase of a paid app.
- Test purchases with a StoreKit configuration file locally and in the sandbox before release.
- Share entitlement state with extensions through the App Group.

**When you need a server**

Add App Store Server Notifications V2 and the App Store Server API when 1 of these conditions applies:

- Users have accounts that work on other platforms.
- Content comes from your server and must be protected.
- You must handle fraud, refunds, or revocations on the server.
- More than 1 app shares entitlements.

On-device StoreKit 2 is sufficient when content unlocks only on Apple devices.

**Analytics and feature flags**

- Define analytics events as a typed enum in `Core`. Do not pass free-form strings.
- Do not put personal data in events.
- Use remote feature flags as a kill switch for risky features. Make the compiled default the safe value.
