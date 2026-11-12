# Rust architecture development archive

`skills/rust-architecture` is the source of truth. [`source/rust-application-architecture-guide.md`](source/rust-application-architecture-guide.md) is the original guide, archived on 2026-11-11. Edit the skill, not the archive.

## Add the skill to a Rust project

A skill description does not make sure that an agent invokes the skill every time. Add this line to the `AGENTS.md` file of each Rust project:

```markdown
Rust architecture: invoke the `rust-architecture` skill before you read or edit Rust code, and start every subagent prompt for Rust work with the same instruction.
```

## Section map

Sections 1, 2, and 23 of the guide are the invariants, the platform baseline, the priority order, and the out-of-bounds step in `SKILL.md`. Each other numbered section is in 1 reference file. The "Caveats" and "Sources" sections are only in the archive.

The reference text is an edit of the guide, not a copy:

- Version numbers are only in the code examples, where they show the format. The baseline line of `SKILL.md` names the latest stable releases, not version numbers. The guide's version columns are gone.
- Dated status, release news, incident reports, and open issue numbers are durable rules, or they are gone.
- Notes that Cargo, the compiler, or the supply-chain gates already report are gone, for example renamed crate features and fixed RustSec advisories.
- The citation markers are gone. Each "section N" reference is a link to its file.
- The code examples are unchanged, except that each comment that cites a section names the reference file.

| Guide section | Reference file |
| --- | --- |
| 1. Summary | `SKILL.md` |
| 2. Priority order for trade-offs | `SKILL.md` |
| 3. Project setup and toolchain | `project-setup.md` |
| 4. UI framework | `ui-framework.md` |
| 5. Application architecture pattern | `architecture.md` |
| 6. Modularization with a Cargo workspace | `architecture.md` |
| 7. Routing, navigation, and input | `routing-input.md` |
| 8. Networking | `networking.md` |
| 9. Authentication and identity | `authentication.md` |
| 10. Persistence | `persistence.md` |
| 11. Security and privacy | `security-privacy.md` |
| 12. Concurrency and reliability | `concurrency.md` |
| 13. Process lifecycle, background work, and platform integration | `lifecycle.md` |
| 14. Accessibility | `accessibility.md` |
| 15. Localization | `localization.md` |
| 16. Testing | `testing.md` |
| 17. Observability and performance | `observability-performance.md` |
| 18. Cross-cutting seams | `seams.md` |
| 19. Release engineering and distribution | `release.md` |
| 20. Migrating an existing project to Rust | `migration.md` |
| 21. New project checklist | `project-setup.md` |
| 22. Trade-offs and thresholds | `deviations.md` |
| 23. When a tool in this guide does not cover a need | `SKILL.md` |
