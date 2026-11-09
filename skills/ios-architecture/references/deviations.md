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

| Condition | Change |
| --- | --- |
| Custom drawing or animation that SwiftUI controls cannot show | Use `Canvas` or Metal in that feature only, with explicit accessibility elements |
| 3D or spatial content | Use RealityKit in that feature only |
| More than about 8 engineers, or many shared effects | Consider TCA or strict MVVM with a shared effects layer |
| Queries outgrow flat files (filters, joins, more than a few thousand records) | Move to SwiftData, Core Data, or GRDB behind the same protocol |
| Cross-device sync | Use CloudKit (SwiftData, Core Data, or SQLiteData) or your own backend |
| Accounts or purchases that work on other platforms | Add a server with App Store Server Notifications V2 |
| Regulated data | Add Data Protection `.complete`, App Attest, key pinning, server-side audit logs, and a compliance review |
