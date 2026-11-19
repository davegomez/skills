# Trade-offs and thresholds

The defaults in this guide win on security, reliability, and accessibility. Change a default only when its threshold applies.

**Default decisions**

| Decision | Default | Main reason |
| --- | --- | --- |
| SwiftUI or custom renderer | SwiftUI | Accessibility, maintainability |
| Pure domain split or 1 layer | Split | Reliability (testability) |
| MV with `@Observable` or TCA | MV plus pure reducers | Maintainability; no third-party framework migrations |
| Files, SwiftData, Core Data, or GRDB | Simplest store that fits, behind a protocol | Reliability; you can change the engine later |
| Build purchases now or add a seam | Seam with a safe default | Security, maintainability |
| Modular packages or 1 target | Modular packages | Maintainability, build speed |
| Bundled String Catalogs or remote strings | String Catalogs | Reliability, security |

**Thresholds that change a default**

| Id | Condition | Change |
| --- | --- | --- |
| `custom-drawing` | Custom drawing or animation that SwiftUI controls cannot show | Use `Canvas` or Metal in that feature only, with explicit accessibility elements |
| `spatial-content` | 3D or spatial content | Use RealityKit in that feature only |
| `large-team` | More than about 8 engineers, or many shared effects | Consider TCA or strict MVVM with a shared effects layer |
| `large-store` | Queries outgrow flat files (filters, joins, more than a few thousand records) | Move to SwiftData, Core Data, or GRDB behind the same protocol |
| `cross-device-sync` | Cross-device sync | Use CloudKit (SwiftData, Core Data, or SQLiteData) or your own backend |
| `cross-platform-accounts` | Accounts or purchases that work on other platforms | Add a server with App Store Server Notifications V2 |
| `regulated-data` | Regulated data | Add Data Protection `.complete`, App Attest, key pinning, server-side audit logs, and a compliance review |

**Deviation marker.** When a threshold applies to a file, write the comment `// ios-architecture: deviation <id>` in that file, with the id from the table. A marker in `Package.swift` applies to that manifest. `scripts/check` then prints each violation that `scripts/lib/deviation-rules.tsv` permits for that id in that file as a `suppressed:` line, not as a violation. A marker with an unknown id is a violation. A marker never suppresses a security or privacy rule.
