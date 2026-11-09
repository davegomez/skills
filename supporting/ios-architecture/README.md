# iOS architecture development archive

`skills/ios-architecture` is the source of truth. [`source/native_ios_application_architecture_guide.md`](source/native_ios_application_architecture_guide.md) is the original guide, archived unchanged on 2026-11-09. Edit the skill, not the archive.

## Add the skill to an iOS project

A skill description does not make sure that an agent invokes the skill every time. Add this line to the `AGENTS.md` file of each iOS project:

```markdown
iOS architecture: invoke the `ios-architecture` skill before you read or edit iOS app code, and start every subagent prompt for iOS work with the same instruction.
```

## Section map

Sections 1 and 2 of the guide are the invariants and the priority order in `SKILL.md`. Each other section is in 1 reference file. The text is unchanged, except that each "Section N" reference is now a link to its file.

| Guide section | Reference file |
| --- | --- |
| 3. Project setup and toolchain | `project-setup.md` |
| 4. UI framework | `ui-framework.md` |
| 5. Application architecture pattern | `architecture.md` |
| 6. Modularization with local Swift packages | `architecture.md` |
| 7. Navigation and deep links | `navigation.md` |
| 8. Networking | `networking.md` |
| 9. Authentication and identity | `authentication.md` |
| 10. Persistence | `persistence.md` |
| 11. Security and privacy | `security-privacy.md` |
| 12. Concurrency and reliability | `concurrency.md` |
| 13. App lifecycle, background work, notifications, and extensions | `lifecycle-extensions.md` |
| 14. Accessibility | `accessibility.md` |
| 15. Localization | `localization.md` |
| 16. Testing | `testing.md` |
| 17. Observability and performance | `performance.md` |
| 18. Purchases and cross-cutting seams | `purchases-seams.md` |
| 19. Release engineering and App Store compliance | `release.md` |
| 20. Migrating an existing app | `migration.md` |
| 21. New project checklist | `project-setup.md` |
| 22. Trade-offs and thresholds | `deviations.md` |
