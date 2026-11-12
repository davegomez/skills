# Security and privacy

Apply every control in this section to every app. If the data classification is not clear, treat the data as regulated until someone confirms otherwise.

**Controls**

- **Secrets:** Do not ship API secrets in the binary. Keep secrets on your server, and give the app short-lived tokens.
- **Keychain:** Store credentials and keys in the Keychain. Use access control flags (`.biometryCurrentSet`, `.userPresence`) for high-value items.
- **Data Protection:** Set a file protection class on every file that contains user data.
- **Transport:** Keep ATS on (see [Networking](networking.md)).
- **App integrity:** Use App Attest (`DCAppAttestService`) to prove to your server that requests come from a genuine copy of your app. Use DeviceCheck for per-device state, such as promotion abuse.
- **Trust boundaries:** Validate all input from the network, deep links, the pasteboard, files, extensions, and widgets. Parse it into typed domain values, and reject invalid values early.
- **Errors:** Show generic error messages to users. Put details in logs, without personal data.
- **Randomness:** Use `SystemRandomNumberGenerator` or `SecRandomCopyBytes` for tokens, nonces, and keys.
- **Screen content:** Hide sensitive screens in the app switcher snapshot. Mark sensitive text fields so that the system does not store them.
- **AI features:** Treat model output and retrieved content as untrusted input. Ask for user confirmation before an action with side effects.

**Logging**

- Use `os.Logger` with 1 subsystem per app and 1 category per module.
- The system redacts dynamic strings and objects by default. It does not redact integer, floating-point, and Boolean values, so mark a sensitive number `privacy: .private`.
- Mark only non-sensitive values with `privacy: .public`.
- Use `privacy: .private(mask: .hash)` to correlate events without exposing values.
- Use structured key-value messages. Do not log tokens, request bodies, or personal data.

**Privacy requirements**

- Ship `PrivacyInfo.xcprivacy` in the app. Declare collected data types, tracking domains, and a reason code for each required-reason API (file timestamps, system boot time, disk space, active keyboards, `UserDefaults`).
- Make sure each third-party SDK that collects data, uses a required-reason API, or contacts tracking domains ships its own privacy manifest.
- Apple requires a privacy manifest for each SDK on its list of commonly used SDKs, and a signature when a listed SDK is a binary dependency.
- Keep the App Store privacy labels equal to what the app and its SDKs actually collect.
- Request App Tracking Transparency permission before you track users across apps or websites. If you do not track, do not show the prompt.
- Write a purpose string for every permission. Request each permission at the moment the user needs the feature, not at launch.
- Collect only the data that a feature needs.

**Regulated data (high-level guide, not legal advice)**

- **Health (for example, HIPAA in the US):** Store the minimum protected health information. Encrypt it at rest and in transit. Keep audit logs on the server. Sign a business associate agreement with every vendor that touches the data.
- **Payments (PCI DSS):** Do not handle raw card numbers. Use Apple Pay or a certified payment SDK so that card data does not enter your systems. Use in-app purchase through StoreKit for digital goods, unless an exception in App Review Guideline 3.1 applies.
- **Personal data (GDPR and similar laws):** Document the legal basis for each data type. Support data export and deletion. Get consent before any optional collection.

Get a legal and compliance review before you release an app that handles regulated data.
