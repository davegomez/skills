# Cross-cutting seams

Put each cross-cutting concern behind 1 trait with a safe default. Check it in 1 place.

| Seam | Trait | Safe default | Checked in |
| --- | --- | --- | --- |
| Authentication | `Authenticator` | Deny all | Server middleware; CLI/desktop session service |
| Authorization | `Policy` | Deny all | Use-case layer (`*-app` crates) |
| Analytics / telemetry | `Telemetry` | No-op, opt-in only | Composition root; domain never calls it |
| Feature flags | `Flags` | All new features off | Feature registry at startup |
| Diagnostics | `Diagnostics` | Logs only, no upload | Crash and error handlers |
| Entitlements / licensing | `Entitlements` | Free tier | Use-case layer, before a paid action |
| Notifications | `Notifier` | Log and drop | Effect handler after the reducer |
