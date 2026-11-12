# Release engineering and App Store compliance

Automate every build and release step, and plan for the fact that you cannot roll back an installed version.

**Build and versioning**

- Build release candidates only in CI, with the pinned Xcode version.
- Use semantic versioning for the marketing version. Let CI set a build number that always increases.
- Upload debug symbols (dSYMs) for every build so that crash reports are readable.
- Build with the SDK version that App Store Connect currently requires.

**Distribution**

- Send every build to internal TestFlight testers first, then to external testers.
- Use phased release for updates. Pause it when crash or hang rates increase.
- Give App Review a demo account and notes for every feature that needs setup.

**Recovery without rollback**

- Use remote feature flags as kill switches for risky features (see [Purchases and cross-cutting seams](purchases-seams.md)).
- Add a minimum-supported-version check that asks users to update when a version is unsafe.
- Keep server APIs compatible with every app version that is still in use.

**App Store Connect requirements for each release**

- [ ] Privacy manifest complete, including third-party SDKs
- [ ] App privacy labels match actual data collection
- [ ] Accessibility Nutrition Labels tested and updated
- [ ] Age rating questionnaire answered
- [ ] Export compliance declared (`ITSAppUsesNonExemptEncryption` in `Info.plist`)
- [ ] Privacy policy URL current
- [ ] Trader status declared for the Digital Services Act, with or without distribution in the European Union
- [ ] Account deletion available, if the app has accounts
- [ ] Restore Purchases available, if the app sells restorable purchases
- [ ] Screenshots and descriptions localized for every supported language
