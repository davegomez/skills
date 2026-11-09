# Persistence

Use the simplest store that meets your query and sync needs, and put it behind a protocol. Feature code must not know the storage engine.

| Need | Use | Notes |
| --- | --- | --- |
| Small preferences and flags | `UserDefaults` | Not for secrets or large data. Declare the required reason in the privacy manifest. |
| Tokens, passwords, keys | Keychain | Use `kSecAttrAccessibleWhenUnlockedThisDeviceOnly` or stricter for sensitive items. |
| Documents, caches, small state | `Codable` files | Write atomically. Set a Data Protection class. |
| Object graph, SwiftUI-driven lists, private CloudKit sync | SwiftData | Use `VersionedSchema` and `SchemaMigrationPlan` from version 1. |
| Mature object graph, advanced fetches, shared or public CloudKit data | Core Data | `NSPersistentCloudKitContainer` supports private, shared, and public databases. |
| SQL, complex queries, joins, full control | GRDB or SQLiteData | Both are SQLite-based. SQLiteData adds observation-friendly queries and CloudKit sync. |
| Small key-value sync across devices | `NSUbiquitousKeyValueStore` | Small quota. Not for user content. |

**Rules**

- Put every store behind a protocol in `Core`, with an in-memory fake for tests.
- Run database work off the main actor. Pass `Sendable` snapshots back to the UI.
- Version your schema from the first release, whatever engine you use.
- Write a migration test for each schema version, with a fixture from the previous version.
- Choose the strictest Data Protection class that your background work allows. Use `.complete` for regulated data unless the app must read it while the device is locked.
- Exclude caches and data that you can download again from backup.
- Put data that extensions read in the App Group container.

**SwiftData migrations:** SwiftData supports `MigrationStage.lightweight` and `MigrationStage.custom(fromVersion:toVersion:willMigrate:didMigrate:)`. Use a custom stage for data changes such as deduplication or derived values.

**Sync to your own server:** Use SwiftData history (`HistoryObserver`) or Core Data persistent history to find local changes since the last sync.

**Performance:** Do not choose a store from published benchmarks alone. Measure with your own data shape and volume.
