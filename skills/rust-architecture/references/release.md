# Release engineering and distribution

Version with SemVer, build reproducibly in CI, sign everything, and ship SBOMs with every artifact.

- Use `release-plz` for release pull requests and changelogs.
- Use `dist` (cargo-dist) to build installers and GitHub releases for CLI and desktop binaries.
- Cross-compile with `cargo-zigbuild`. Build server images on a distroless base.
- Attach SBOMs and SLSA provenance attestations to every release.
- **macOS:** Sign with a Developer ID certificate, enable the hardened runtime, notarize with `notarytool`, and staple the ticket.
- **Windows:** Sign with an Authenticode certificate through a cloud HSM or signing service. Timestamp every signature.
- **Server rollback:** Keep the previous image tag. Make migrations backward-compatible for 1 release (expand, then contract).
- **Desktop rollback:** You cannot recall installed binaries. Fix forward through the updater, with staged rollouts (5%, 25%, 100%) and a remote kill switch.
