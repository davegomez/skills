# App lifecycle, background work, notifications, and extensions

Drive lifecycle behavior from SwiftUI scene phases, and share data with extensions only through an App Group.

**Lifecycle**

- Use the SwiftUI `App` lifecycle. Use `@UIApplicationDelegateAdaptor` only for APIs that need an app delegate, such as push registration.
- React to `scenePhase` changes: save state on `.background`, refresh data on `.active`.
- Restore navigation and draft state after the system stops the app (see [Navigation and deep links](navigation.md)).

**Background work**

- Use `BGTaskScheduler` with `BGAppRefreshTask` for short refreshes and `BGProcessingTask` for long maintenance work.
- Use `BGContinuedProcessingTask` for user-started work that must continue after the user leaves the app.
- Use a background `URLSession` for large uploads and downloads.
- Make every background task idempotent. The system can stop it at any time.

**Push notifications**

- Put push handling behind a `NotificationClient` protocol.
- Use token-based APNs authentication. Keep the signing key in your server's secrets manager.
- Send the minimum content in the payload. Use a Notification Service Extension to fetch or decrypt sensitive content.
- Request notification permission when the user turns on a feature that needs it.

**Extensions and system integration**

- Put each extension (widgets, Live Activities, share extension, notification extension) in its own target. Make it depend on the same `Core` and domain packages as the app.
- Share data through the App Group container and a shared Keychain access group.
- Keep extensions small. They have strict memory and time limits.
- Expose main actions with App Intents. The system can then show them in Shortcuts, Siri, Spotlight, and widgets.
- Treat all data that an extension or intent receives as untrusted input.
