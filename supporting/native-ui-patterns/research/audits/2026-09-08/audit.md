# native-ui-patterns audit: new Settings screenshots (2026-09-08)

This audit proposes changes only. No repository file was changed.

> Archive copy (2026-09-09). This file was copied from the private audit directory after every personal string was replaced by its kind. The worker reports (`workers/`), the batch specs and notes (`batches/`), the personal-data inventory and backups (`pii/`), the redaction specs and image scratch files (`tmp/`), and the contact sheets were not archived; the private directory was deleted on 2026-09-09. A reference to one of those paths in this file is historical. `redact.py` beside this file is the redaction tool named below, and `prompt.md` is the brief that produced this audit. Pending iOS originals for B4 to B13 live in `research/notes/ios/captures-2026-09-08/`; a batch moves its file from there into the runtime. From this copy on, this file is the working record: implementation status is appended here.

## Scope and baseline

- Repository reviewed: this repository (branch `main`, clean at start).
- New screenshot directory reviewed: the owner's screenshot folder outside the repository (recursive). `screenshot-ledger.tsv` lists each file under `captures-2026-09-08/`, the original-path prefix that `screenshot-map.tsv` also uses.
- Baseline validation, run before analysis from the repository root:
  - `python3 supporting/native-ui-patterns/check_skill.py` exited 1 with one failure: `unexpected runtime path: assets/android/.DS_Store`. This is a Finder metadata file inside the runtime asset tree. It was not fixed.
  - `python3 supporting/native-ui-patterns/test_check_skill.py` exited 0 (14 tests, OK). The run created `supporting/native-ui-patterns/__pycache__/` (untracked). It was removed after the run, so the tree is clean again.
- Files discovered: 65. Images: 64. Non-image: 1 (`.DS_Store`, skipped).
- Images inspected visually: 64. Blocked or failed: 0. Unsupported format: 0.

Corpus facts, taken from the screenshots themselves:

| Set | Files | Format | Dimensions (image pixels) | Environment shown in the captures |
| --- | ---: | --- | --- | --- |
| iOS | 44 | PNG | 1206×2622 | Settings app only. Light appearance. Signed-in Apple Account with Family, subscriptions, and devices. S-I12 shows "iPhone 17 Pro" and "iOS 27.0". Sequential file names IMG_4293 to IMG_4336, times 16:58 to 17:06. |
| Android | 20 | JPEG | 1000×2244 | Settings app only. Dark theme. Signed-in Google account. S-A15 shows the device as "Pixel 10". OS version not visible (unknown). File times are identical, so capture order is unknown. |

The existing corpus came from a Simulator and an Emulator with no account and mostly empty data. The new corpus is a physical, signed-in device with populated data. That difference explains most findings: the existing catalog documents iOS Settings only as root, General, and search, and Android Settings only as root, search, and Display & touch.

## Delegation summary

14 read-only workers ran concurrently on the `sonnet` model. Each worker opened its images at full resolution, read the platform runtime references and catalog, and wrote one report under `workers/`. All 14 completed. No reassignment was needed.

| Worker | Group | Screenshots | Count |
| --- | --- | --- | ---: |
| W01 | iOS account hub | S-I01, S-I02, S-I03, S-I04 | 4 |
| W02 | iOS account detail | S-I05, S-I06, S-I07, S-I08 | 4 |
| W03 | iOS family and devices | S-I09, S-I10, S-I11, S-I12, S-I13 | 5 |
| W04 | iOS connectivity | S-I14, S-I15, S-I16, S-I18 | 4 |
| W05 | iOS device status | S-I17, S-I19, S-I20, S-I21, S-I22 | 5 |
| W06 | iOS care and cars | S-I23, S-I24, S-I25 | 3 |
| W07 | iOS general settings | S-I26, S-I27, S-I28, S-I29, S-I30 | 5 |
| W08 | iOS appearance and display | S-I31, S-I32, S-I33, S-I34, S-I35, S-I36 | 6 |
| W09 | iOS notifications and sound | S-I37, S-I38, S-I39 | 3 |
| W10 | iOS screen time and safety | S-I40, S-I41, S-I42, S-I43, S-I44 | 5 |
| W11 | Android root and network | S-A17, S-A05, S-A16, S-A18, S-A14, S-A15 | 6 |
| W12 | Android sound, modes, display | S-A01, S-A20, S-A02, S-A19, S-A09, S-A06 | 6 |
| W13 | Android wallpaper, security, location | S-A10, S-A12, S-A03, S-A11 | 4 |
| W14 | Android safety, apps, storage | S-A13, S-A07, S-A04, S-A08 | 4 |

Worker output was corrected during consolidation:

- W01 reported a stale "◀ Wallet" label on S-I01. The crop shows no such label. The note was dropped.
- W03 called the inline centered title a duplicate of the existing General capture without opening it. W01 and W08 opened `assets/ios/settings/general.png` and found no title in the bar. The orchestrator confirmed this by crop. The inline title is a variation (F014).
- W11 cited wrong file paths for S-A05, S-A14, and S-A15. The ledger paths are authoritative.
- W04 classified the Wi-Fi "Other Networks" spinner as application-specific. W06 found the same spinner on CarPlay "Other Cars". The two instances were merged into F019.
- The worker report format was followed loosely by W03, W06, and W14. Their content was normalized into the fields below.

## Candidate totals

After consolidation of 118 worker candidates:

| Classification | Count |
| --- | ---: |
| new-pattern | 31 |
| existing-pattern-variation | 6 |
| existing-pattern-improvement | 5 |
| duplicate | 8 |
| application-specific | 9 |
| uncertain | 15 |

Actionable findings: 42 (iOS 26, Android 16). Every one of the 64 screenshots supports at least one actionable finding. See `findings-ledger.tsv` and `screenshot-ledger.tsv`.

## Scope rule for this corpus

All 64 captures come from one application per platform: Settings. The existing catalog marks a pattern "application-specific" when only one application confirmed it. Applied literally, that rule would label all 42 findings and would tell an agent that a switch or a slider belongs only on a Settings screen. This audit counts recurrence across distinct Settings screens instead. Provenance goes in "Applications observed". Applicability goes in a separate Inferred line with the value `system control`, `general idiom`, or `settings idiom`. See decision D1 below and the `applicability` column in `findings-ledger.tsv`.

## Claim conventions used below

- **Observed**: visible in the named screenshot.
- **Inferred**: bounded interpretation.
- **Unconfirmed**: not established. No still image establishes activation, dismissal, gesture, animation, focus order, spoken output, hit targets, or APIs.
- Regions are named by screen third, or by image-pixel box when a worker measured one. No iOS points or Android dp are stated.

---

## Proposed new patterns

### F001 Switch row (iOS)

- **Identity**: Switch row; iOS; new-pattern; proposed category Forms and controls; runtime operation editing. This fills the iOS cell "Switches, filters, and value controls: Record a coverage gap".
- **Source**: S-I01, S-I03, S-I10, S-I14, S-I16, S-I18, S-I26, S-I28, S-I32, S-I33, S-I34, S-I35, S-I38, S-I39, S-I41, S-I43, S-I44.
- **Scope**: Settings root and 14 detail screens.
- **UX problem** (Inferred): change a binary setting in place and show its current state without a detail screen.
- **Current coverage**: absent for iOS. Android documents `Trailing switch in a settings or list row`.
- **Gap**: the iOS catalog has no toggle at all. The new corpus shows 25 switches in on and off states, in 5 placements.
- **Visual structure** (Observed): a horizontally elongated rounded track at the trailing edge of a row, vertically centered against a leading label. On state: green-filled track, white circular knob at the trailing end. Off state: light gray track, knob at the leading end. Placements: (a) sole row in its own card, often followed by a gray footer sentence outside the card (S-I18, S-I26, S-I34, S-I41, S-I43, S-I44); (b) first row of a card whose next rows are dependent label/value rows in gray (S-I26 "Set Time Zone Automatically" above "Time Zone" and "Time Zone City"); (c) a row after a divider inside a feature hero card (S-I14, S-I16, see F009); (d) an icon-led row with a switch (S-I01 Airplane Mode, VPN; S-I38 Silent Mode); (e) an identity row with a switch (S-I28 NBC Sports, see F025). Several switches with footers stack under one section header without card dividers between units (S-I43).
- **Interaction**: Unconfirmed. No toggle was exercised.
- **States**: on and off observed. Disabled not observed.
- **Variations**: as listed in placements (a) to (e).
- **Evidence**: S-I26 middle third (switch over dependent rows plus footer); S-I43 middle third (three stacked switch-plus-footer units); S-I38 top third (off switch with leading bell glyph, on switch below); S-I14 top third (switch after a divider in the Wi-Fi hero card).
- **Existing evidence checked**: `docs/ios/forms-and-controls.md#grouped-form-rows` (no switch), `references/ios/editing.md` (gating only).
- **Integration**: new heading "Switch row" in `docs/ios/forms-and-controls.md`. Route from `references/ios/editing.md` with a "Switch on versus off with footer" row (S-I26) and a "Stacked switches under one header" row (S-I43). Change the SKILL.md route cell for iOS "Switches, filters, and value controls" to `references/ios/editing.md`.
- **Confidence**: high. 25 instances, both states.
- **Priority**: highest. The most common iOS settings control is undocumented and the route table says so.

### F002 Inline slider row (iOS)

- **Identity**: Inline slider row; iOS; new-pattern; Forms and controls; editing.
- **Source**: S-I35, S-I38.
- **Scope**: Display & Brightness "Brightness" group; Sounds & Haptics "Ringtone" group.
- **UX problem** (Inferred): set a continuous value and read its current position without a dialog.
- **Current coverage**: absent. No continuous-value control exists in the iOS catalog.
- **Gap**: first slider evidence for iOS.
- **Visual structure** (Observed): the first row of a grouped card holds a thin horizontal rounded track that spans the row. A small glyph sits at the leading end and a larger glyph of the same family at the trailing end (dim sun and bright sun in S-I35; small speaker and loud speaker in S-I38). The filled part of the track, left of the thumb, is blue. The rest is light gray. The thumb is a white circle. A thin divider separates the slider row from the label/value rows below it in the same card. No text label appears on the slider row.
- **Interaction**: Unconfirmed.
- **States**: one settled thumb position per screen. No drag, minimum, maximum, or disabled state.
- **Variations**: none beyond the glyph pair.
- **Evidence**: S-I35 top third; S-I38 upper-middle third (about y 1420 to 1580 of 2622).
- **Existing evidence checked**: all four iOS catalog files. None mention a slider.
- **Integration**: new heading "Inline slider row" in `docs/ios/forms-and-controls.md`. Route from `references/ios/editing.md` with one row (S-I35).
- **Confidence**: high.
- **Priority**: high. Fills the same route gap as F001.

### F003 Visual option picker (iOS)

- **Identity**: Visual option picker; iOS; new-pattern; Forms and controls; editing.
- **Source**: S-I32, S-I33, S-I37.
- **Scope**: Appearance "Light / Dark"; Notifications "Display As".
- **UX problem** (Inferred): choose between a few mutually exclusive outcomes whose difference is visual, by comparing rendered previews.
- **Current coverage**: absent.
- **Gap**: no picker, segmented control, or preview-based selection exists in the iOS catalog.
- **Visual structure** (Observed): inside one grouped card, two or three small device-shaped preview tiles sit side by side with equal spacing, each rendering a miniature of the outcome. A caption sits below each tile. Two selection indicators were observed. In S-I32 a circular control sits below each caption: a filled blue circle with a check for the selected option, an empty outlined circle for the other. In S-I37 the selected caption sits inside a filled blue capsule, the selected tile has a blue tint, and the other captions are plain black text with no control. A divider or a gray explanatory footer follows the picker.
- **Interaction**: Unconfirmed.
- **States**: one selected option per screen.
- **Variations**: radio-style indicator below the caption (2 options) versus capsule-highlighted caption (3 options).
- **Evidence**: S-I32 top third; S-I37 top third (about y 450 to 950).
- **Existing evidence checked**: `docs/ios/forms-and-controls.md#grouped-form-rows`.
- **Integration**: new heading "Visual option picker" in `docs/ios/forms-and-controls.md` with both indicator variants. Route from `references/ios/editing.md` with an explicit comparison pair (S-I32, S-I37).
- **Confidence**: high.
- **Priority**: high.

### F005 Icon-led settings row (iOS)

- **Identity**: Icon-led settings row; iOS; new-pattern; Lists; navigation and content-states.
- **Source**: S-I01, S-I10, S-I12, S-I13, S-I31, S-I39, S-I40, S-I41, S-I44.
- **Scope**: Settings root and detail hubs (Find My, Device Info, Accessibility, Focus, Screen Time, family member detail).
- **UX problem** (Inferred): let a user scan many destinations by a color and glyph cue and read each row's current state without opening it.
- **Current coverage**: absent as a description. The existing `assets/ios/settings/root.png` shows these rows, but no catalog entry describes them. `Identity-led list row` covers avatar badges for people.
- **Gap**: the standard Settings row anatomy has no entry.
- **Visual structure** (Observed): a small colored rounded-square icon in a fixed leading slot, a label, and a trailing zone. The trailing zone holds a gray value plus chevron (S-I31 "VoiceOver Off >", S-I10 "Find My iPhone On >"), a chevron alone (S-I01 Cellular), a gray value with no chevron for a read-only fact (S-I10 "My Location  This Device"), or a switch (S-I01 Airplane Mode, see F001). A second gray subtitle line under the label appears on destination rows that need explanation (S-I40, S-I41 "Set time limits for apps"). Focus rows (S-I39) use flat colored glyphs with no square background.
- **Interaction**: Unconfirmed.
- **States**: value present, value absent, read-only value, subtitle present.
- **Variations**: rounded-square icon versus flat colored glyph; with or without subtitle.
- **Evidence**: S-I40 lower half (subtitle rows); S-I31 middle third (value rows); S-I39 upper-middle third (flat glyphs); S-I10 upper-middle third (read-only value row).
- **Existing evidence checked**: `docs/ios/lists-content-feedback.md#identity-led-list-row`; `docs/ios/forms-and-controls.md#grouped-form-rows`; `assets/ios/settings/root.png` (shows the anatomy, undocumented).
- **Integration**: new heading "Icon-led settings row" in `docs/ios/lists-content-feedback.md`. Route from `references/ios/content-states.md` (S-I40) and cross-reference the existing root capture.
- **Confidence**: high.
- **Priority**: high.

### F006 Label/value information rows (iOS)

- **Identity**: Label/value information rows; iOS; new-pattern; Lists and content; content-states.
- **Source**: S-I12, S-I22, S-I30.
- **Scope**: Device Info "Device Info" group; Music storage "App Size / Documents & Data"; Legal & Regulatory table.
- **UX problem** (Inferred): present read-only facts about one object without implying any row is tappable.
- **Current coverage**: absent. `Grouped form rows` documents editable fields and option rows with chevrons.
- **Gap**: no non-interactive spec-sheet rows exist in the catalog.
- **Visual structure** (Observed): rows in a grouped card with a plain black label at the leading edge and a gray value at the trailing edge, no icon, no chevron, no control, thin dividers between rows. Long values (serial number, IMEI) stay on one line in S-I12. In S-I30 the value column can be a multi-sentence gray paragraph, and one cell embeds small monochrome certification marks under an address. The regulatory content is application-specific (A05); the label-plus-wrapped-paragraph structure is the reusable part.
- **Interaction**: Unconfirmed. No affordance is visible.
- **States**: populated only.
- **Variations**: short value versus wrapped paragraph value versus paragraph with inline marks.
- **Evidence**: S-I12 lower half; S-I22 top card; S-I30 middle to bottom.
- **Existing evidence checked**: `docs/ios/forms-and-controls.md#grouped-form-rows`; `docs/ios/lists-content-feedback.md#identity-led-list-row`.
- **Integration**: new heading "Label/value information rows" in `docs/ios/lists-content-feedback.md`. Route from `references/ios/content-states.md` (S-I12).
- **Confidence**: high.
- **Priority**: medium.

### F007 Link-style action row (iOS)

- **Identity**: Link-style action row; iOS; new-pattern; Forms and controls; editing.
- **Source**: S-I04, S-I05, S-I22, S-I24, S-I27, S-I29, S-I33, S-I34, S-I35, S-I41, S-I44.
- **Scope**: Sign-In & Security ("Change Password", "Add Email or Phone Number"), Language & Region ("Add Language…"), Music storage ("Offload App"), AppleCare device ("Manage Subscription"), Transfer or Reset ("Reset", "Erase All Content and Settings", "Transfer to Android"), Control Center ("Reset Control Center"), Screen Time ("Lock Screen Time Settings"), Game Center ("Invite Friends", "Customize Profile"), Appearance and Display ("More in Accessibility Settings…"), Personal Information ("See how your data is managed…").
- **UX problem** (Inferred): present a command, an additive action, or a secondary link that reads as tappable without full row chrome.
- **Current coverage**: absent. `Add and remove rows (application-specific)` covers red minus and green plus icon controls only.
- **Gap**: no text-only tappable row exists in the catalog. 11 screens use one.
- **Visual structure** (Observed): a row whose only content is blue text, no leading icon, no chevron, no trailing value. Four placements: (a) last row of a data group as an add action, left-aligned, with an ellipsis (S-I27, S-I05); (b) sole row in its own card, centered or left-aligned, often with a gray footer under the card (S-I22, S-I34, S-I41); (c) a two- or three-row card of commands with dividers, left-aligned (S-I29; S-I24 pairs a blue row with a red row, see F008); (d) cardless centered blue text on the page background below the last card, as a secondary disclosure (S-I04); and a caption-attached form under a gray footer (S-I33, S-I35). Blue text-only rows are also used for consequential flows (S-I29 "Erase All Content and Settings"), not red; the confirmation flow was not captured.
- **Interaction**: Unconfirmed for all instances.
- **States**: resting only.
- **Variations**: placements (a) to (d); alignment centered versus left; footer present or absent.
- **Evidence**: S-I27 upper-middle (add row inside a group); S-I22 middle (centered "Offload App" with footer); S-I29 lower half (command groups); S-I04 bottom (cardless link); S-I24 middle (blue over red in one card).
- **Existing evidence checked**: `docs/ios/forms-and-controls.md#add-and-remove-rows-application-specific`; `#grouped-form-rows`; `docs/ios/lists-content-feedback.md#feature-introduction-surface`.
- **Integration**: new heading "Link-style action row" in `docs/ios/forms-and-controls.md`, cross-referenced with F008. Route from `references/ios/editing.md` with one comparison pair: add row inside a group (S-I27) versus standalone command card with footer (S-I22).
- **Confidence**: high.
- **Priority**: high.

### F008 Destructive action row (iOS)

- **Identity**: Destructive action row; iOS; new-pattern; Forms and controls; editing.
- **Source**: S-I13, S-I22, S-I24, S-I28, S-I41.
- **Scope**: family member detail ("Remove <member> from Sharing Group"; the member name is boxed in the redacted capture), Music storage ("Delete App"), AppleCare device ("Remove Device"), TV Provider ("Sign Out"), Screen Time ("Turn off App & Website Activity").
- **UX problem** (Inferred): isolate an irreversible or account-level action so it is not mistaken for navigation, and state its consequence before activation.
- **Current coverage**: absent. No red row exists in either the existing catalog or the runtime.
- **Gap**: first destructive treatment for iOS.
- **Visual structure** (Observed): red text on a row with no icon, chevron, or value. In S-I13, S-I22, S-I28, and S-I41 the row is alone in its own card, placed last on the screen, separated by whitespace. Text is centered in S-I13, S-I22, and S-I28, and left-aligned in S-I41. In S-I24 the red row shares one card with a blue row above it, separated by a divider. A gray footer under the card states the consequence in S-I22 ("This action can't be undone."), S-I28 (signed-in account and sync consequence), and S-I41 (the dependent features that will be disabled). S-I22 stacks a blue "Offload App" card above the red "Delete App" card, each with its own footer, so the two actions differ only by color and footer.
- **Interaction**: Unconfirmed. No confirmation dialog was captured.
- **States**: resting only.
- **Variations**: standalone card versus grouped with a link row; centered versus left-aligned; footer present or absent.
- **Evidence**: S-I22 middle (blue/red pair with footers); S-I13 bottom; S-I28 lower third; S-I41 bottom; S-I24 middle.
- **Existing evidence checked**: `docs/ios/forms-and-controls.md#add-and-remove-rows-application-specific`; `#content-gated-commit-control`.
- **Integration**: new heading "Destructive action row" in `docs/ios/forms-and-controls.md`. Route from `references/ios/editing.md` with S-I22 (reversible versus irreversible pair). Add "confirmation after activation" to the capture backlog.
- **Confidence**: high.
- **Priority**: high.

### F009 Feature hero card (iOS)

- **Identity**: Feature hero card; iOS; new-pattern; Navigation and presentation (or Lists and content); navigation and onboarding-permissions.
- **Source**: S-I11, S-I14, S-I16, S-I18, S-I23, S-I25, S-I29, S-I31, S-I43.
- **Scope**: top of Sign in with Apple, Wi-Fi, Bluetooth, Personal Hotspot, AppleCare & Warranty, CarPlay, Transfer or Reset, Accessibility, Emergency SOS.
- **UX problem** (Inferred): orient the user to what a feature does, on the screen where it is configured, without a one-time onboarding gate.
- **Current coverage**: a one-line aside in `docs/ios/navigation-and-presentation.md#large-title-hierarchy` ("Settings presents a descriptive hero card on General"). The existing `assets/ios/settings/general.png` shows the card, but no entry documents its anatomy. `Feature-introduction surface` is full-screen with a Continue button.
- **Gap**: the anatomy, the link, the embedded master switch, and the illustration variant are undocumented.
- **Visual structure** (Observed): the first card below the back control. Variant (a), icon-led: a large tinted rounded-square icon at the top-left, a bold title, a gray paragraph ending in a blue "Learn more…" link (S-I11, S-I14, S-I16, S-I18, S-I23, S-I31; also the existing General capture). Variant (b): the same card continues after a thin divider with a master switch row (S-I14 "Wi-Fi", S-I16 "Bluetooth"). Variant (c), illustration-led: a centered line-art illustration or a full-width image at the top, then a bold heading and gray body (S-I25 CarPlay, S-I43 Emergency SOS); S-I29 adds a divider and a centered blue "Get Started" link as the last card element, with a large empty area below the card. Ordinary rows follow the card on every screen. No Continue button or dismiss control appears.
- **Interaction**: Unconfirmed.
- **States**: resting only.
- **Variations**: (a), (b), (c) as above.
- **Evidence**: S-I14 top third (icon, title, description, link, divider, switch); S-I25 top third (illustration variant); S-I29 top third (compact illustration with divided link).
- **Existing evidence checked**: `docs/ios/navigation-and-presentation.md#large-title-hierarchy`; `docs/ios/lists-content-feedback.md#feature-introduction-surface`; `assets/ios/settings/general.png`.
- **Integration**: new heading "Feature hero card" in `docs/ios/navigation-and-presentation.md`. Remove the aside from Large-title hierarchy and cross-reference. Route from `references/ios/navigation.md` (S-I14) and from `references/ios/onboarding-permissions.md` as the persistent alternative to Feature-introduction surface (S-I25).
- **Confidence**: high. Nine instances plus the existing General capture.
- **Priority**: high.

### F010 Tip card with side illustration (iOS)

- **Identity**: Tip card with side illustration; iOS; new-pattern; Lists and content; content-states.
- **Source**: S-I34, S-I36.
- **Scope**: Control Center (top card); Wallpaper (below the carousel).
- **UX problem** (Inferred): explain a gesture or feature that has no on-screen control, in place, without a full-screen surface.
- **Current coverage**: absent.
- **Gap**: a two-column text-plus-illustration card is undocumented.
- **Visual structure** (Observed): a light gray rounded card. The left two-thirds hold a bold heading and two or three lines of gray body. The right third holds a small schematic illustration, vertically centered and right-aligned. No button, link, or dismiss control. The card can sit at the top of the screen (S-I34) or below another card (S-I36).
- **Interaction**: Unconfirmed.
- **States**: resting only.
- **Variations**: position on screen.
- **Evidence**: S-I34 top third; S-I36 bottom third.
- **Existing evidence checked**: `references/ios/onboarding-permissions.md`; F009 in the same corpus (stacked, not two-column).
- **Integration**: new heading "Tip card with side illustration" in `docs/ios/lists-content-feedback.md`. Route from `references/ios/content-states.md` (S-I34).
- **Confidence**: high.
- **Priority**: medium.

### F011 Inline suggestion card (iOS)

- **Identity**: Inline suggestion card; iOS; new-pattern; Lists and content; content-states.
- **Source**: S-I08, S-I20, S-I24.
- **Scope**: iCloud+ ("Get Apple Invites"), iPhone Storage ("Recommendations"), AppleCare device ("Need Help?").
- **UX problem** (Inferred): surface an optional suggestion, promotion, or recommendation inside a settings list without blocking it.
- **Current coverage**: absent. `Feature-introduction surface` is full-screen.
- **Gap**: three compositions of an inline card with a divider between its subject and its action or rationale are undocumented.
- **Visual structure** (Observed): (a) dismissible promo (S-I08): a small square icon, bold title, gray sentence, a thin divider, a blue link-style call to action alone below the divider, and a small gray X in the card's top-right corner. (b) app promo (S-I24): under a "Need Help?" header, a square app icon, bold app name, gray subtitle, then a wide light-blue capsule button with bold uppercase blue label "OPEN", and a gray caption below. (c) recommendation (S-I20): under a "Recommendations" header, a tappable-looking header row (rounded-square icon, bold title, chevron), a divider, then a gray paragraph that quantifies the benefit.
- **Interaction**: Unconfirmed, including dismissal.
- **States**: resting only.
- **Variations**: (a) to (c).
- **Evidence**: S-I08 middle (about y 904 to 1264); S-I20 upper-middle; S-I24 bottom.
- **Existing evidence checked**: `docs/ios/lists-content-feedback.md#feature-introduction-surface`; `docs/ios/forms-and-controls.md#grouped-form-rows`.
- **Integration**: new heading "Inline suggestion card" in `docs/ios/lists-content-feedback.md` with the three variants. Route from `references/ios/content-states.md` (S-I08).
- **Confidence**: medium. Each variant has one instance.
- **Priority**: medium.

### F012 Identity header (iOS)

- **Identity**: Identity header; iOS; new-pattern; Navigation and presentation; navigation and content-states.
- **Source**: S-I02, S-I03, S-I04, S-I09, S-I12, S-I13, S-I22, S-I44.
- **Scope**: Apple Account hub, Personal Information, Family, Device Info, family member detail, Music storage detail, Game Center.
- **UX problem** (Inferred): identify the subject of a detail screen (a person, a group, a device, an app) before its rows.
- **Current coverage**: absent. `Identity-led list row` is a list row, not a header.
- **Gap**: no header composition exists in the catalog.
- **Visual structure** (Observed): (a) person: a large circular photo centered below the bar, a bold centered name, a gray centered email (S-I02) or none (S-I03), and a small light-blue capsule "Change" button centered below (S-I02, S-I03). (b) group: four circular photos overlapped left to right with thin light borders, centered, above a bold centered "Family" title (S-I09). (c) member: a smaller centered photo, name with a small trailing chevron, and a gray role line (S-I13). (d) device: a small centered illustration of the device, bold name, gray subtitle (S-I12). (e) app: a card at the top with a large rounded-square app icon at the leading edge, bold name, gray publisher, then a divider and value rows (S-I22). (f) profile card with avatar, bracketed name, email, external-link arrow, and a blue "Customize Profile" row after a divider (S-I44). The iCloud+ left-aligned brand header with a circular badge (S-I08) is recorded as application-specific (A01).
- **Interaction**: Unconfirmed.
- **States**: top of scroll (S-I03) and scrolled (S-I04, see F013).
- **Variations**: (a) to (f).
- **Evidence**: S-I03 top third; S-I09 top third; S-I12 top third; S-I22 top card; S-I44 top third.
- **Existing evidence checked**: `docs/ios/lists-content-feedback.md#identity-led-list-row`; `docs/ios/navigation-and-presentation.md#large-title-hierarchy`.
- **Integration**: new heading "Identity header" in `docs/ios/navigation-and-presentation.md` with variants. Route from `references/ios/navigation.md` (S-I03 person, S-I12 device) and `references/ios/content-states.md` (S-I22 app).
- **Confidence**: high.
- **Priority**: medium.

### F013 Scrolled content under a translucent navigation bar (iOS)

- **Identity**: Scrolled content under a translucent navigation bar; iOS; new-pattern (settled scroll state); Navigation; navigation.
- **Source**: S-I03 and S-I04 (pair); S-I32 and S-I33 (pair); S-I21; S-I41.
- **Scope**: Personal Information, Appearance, iPhone Storage, Screen Time.
- **UX problem** (Inferred): keep the bar legible while showing that content continues above the visible list.
- **Current coverage**: `docs/ios/navigation-and-presentation.md#large-title-hierarchy` marks transitions Unconfirmed. No scrolled state is captured in the existing corpus.
- **Gap**: first settled scrolled states.
- **Visual structure** (Observed): in the scrolled captures, the region behind the bar shows blurred, low-contrast shapes of the content that scrolled under it (the lower arc of the avatar in S-I04; the preview tiles and radio dots in S-I33; row fragments in S-I21 and S-I41). The circular back button and the centered title remain crisp on top. Content below the bar is sharp. In S-I04 the "Change" capsule is the first fully visible element under the clipped photo, and one more row is revealed at the bottom.
- **Interaction**: Inferred from the pairs only. Gesture, speed, and animation are Unconfirmed.
- **States**: unscrolled and scrolled pairs.
- **Variations**: image header clipped (S-I04) versus picker blurred (S-I33).
- **Evidence**: S-I32 full image and S-I33 top eighth; S-I03 top third and S-I04 top.
- **Existing evidence checked**: `references/ios/navigation.md`; `docs/ios/navigation-and-presentation.md#large-title-hierarchy` Notes field.
- **Integration**: new heading "Scrolled state under a translucent bar" in `docs/ios/navigation-and-presentation.md`. Route from `references/ios/navigation.md` as an explicit comparison pair (S-I32, S-I33). Update the Large-title hierarchy Notes to point here.
- **Confidence**: medium. Settled states only.
- **Priority**: medium.

### F015 Section header with trailing utility action (iOS)

- **Identity**: Section header with trailing utility action; iOS; new-pattern; Lists; content-states and editing.
- **Source**: S-I07, S-I08, S-I20, S-I22.
- **Scope**: Subscriptions ("Active | Sort ⇅"), iCloud+ ("● Saved to iCloud | See All"), iPhone Storage ("Size ⇅" above the app list), Music storage ("MUSIC | EDIT").
- **UX problem** (Inferred): offer one list-scoped control (sort, edit, see all) without a toolbar or a nav-bar action.
- **Current coverage**: absent. `Explicit selection mode` is nav-bar level with a bottom action bar.
- **Gap**: no list-level control exists.
- **Visual structure** (Observed): one line at full content width above a grouped card. A plain gray section label sits at the leading edge. A blue text control sits at the trailing edge, vertically centered with the label: "Sort" with an up/down arrow glyph (S-I07), "See All" with no chevron (S-I08), "EDIT" in uppercase (S-I22). In S-I20 the control is "Size" with the arrow glyph, right-aligned, with no leading label. In S-I08 a small filled green dot precedes the section label.
- **Interaction**: Unconfirmed (U04).
- **States**: resting only.
- **Variations**: sort, see-all, edit; with or without a leading label; with a status dot.
- **Evidence**: S-I07 top (about y 419 to 485); S-I08 (about y 1598 to 1660); S-I20 upper-middle; S-I22 middle.
- **Existing evidence checked**: `docs/ios/lists-content-feedback.md#identity-led-list-row`; `docs/ios/interactions-and-accessibility.md#explicit-selection-mode-application-specific`.
- **Integration**: new heading "Section header with trailing utility action" in `docs/ios/lists-content-feedback.md`. Route from `references/ios/content-states.md` (S-I07).
- **Confidence**: medium.
- **Priority**: medium.

### F016 List truncation row (iOS)

- **Identity**: List truncation row; iOS; new-pattern; Lists; content-states.
- **Source**: S-I17, S-I21.
- **Scope**: Battery ("View All Battery Usage"), iPhone Storage ("Show All").
- **UX problem** (Inferred): reveal a longer collection without pre-loading it or leaving the screen.
- **Current coverage**: absent.
- **Gap**: no capped-list convention exists.
- **Visual structure** (Observed): S-I21 closes a six-row app list with centered blue "Show All" text, no chevron, inside the same card, above the card's closing edge. S-I17 closes the "App and System Activity" card with a left-aligned blue "View All Battery Usage" row plus a trailing gray chevron, on the same row grid as the rows above.
- **Interaction**: Unconfirmed (expand in place versus navigate).
- **States**: truncated only.
- **Variations**: centered without chevron versus left-aligned with chevron.
- **Evidence**: S-I21 upper portion; S-I17 bottom of the list card.
- **Existing evidence checked**: `docs/ios/lists-content-feedback.md#centered-empty-state`.
- **Integration**: new heading "List truncation row" in `docs/ios/lists-content-feedback.md`. Route from `references/ios/content-states.md` (S-I21).
- **Confidence**: medium.
- **Priority**: medium.

### F017 Comparative bar chart card (iOS)

- **Identity**: Comparative bar chart card; iOS; new-pattern; Lists and content (data summary); content-states.
- **Source**: S-I17, S-I40.
- **Scope**: Battery "Daily Usage"; Screen Time summary.
- **UX problem** (Inferred): show a headline metric, its trend or baseline, and a short history in one card, with a route to detail.
- **Current coverage**: absent. No chart exists in either platform catalog.
- **Gap**: first chart evidence.
- **Visual structure** (Observed): a white rounded card. S-I17: a status card first (very large bold "90" with a smaller "%", a bold "Last Charged to 90%:" caption with gray "20m ago", a thin dark-gray full-width bar, and a small circular "i" glyph at the top-right); then an insight sentence card; then a chart card with two large values side by side ("Average 29%" gray, "Today 13%" blue), eight two-tone vertical bars with one-letter day labels, the current day in blue, and a thin horizontal rule at the average height labeled "Average". A legend row sits under the bars. S-I40: a small gray "Daily Average" caption, a large bold "3h 15m", a circular gray badge with an up arrow and "21% from last week" to its right, a seven-column bar chart with teal bars, a dashed green "avg" line, dotted gridlines, a "6h / 0" scale at the right, then a divider and a "See All App & Website Activity" row with a chevron inside the same card. A gray "Updated today at 17:05" caption sits under the card.
- **Interaction**: Unconfirmed.
- **States**: populated only.
- **Variations**: reference line solid (S-I17) versus dashed with label (S-I40); embedded detail row (S-I40) versus separate list (S-I17).
- **Evidence**: S-I17 top and middle thirds; S-I40 top third (about y 480 to 1160).
- **Existing evidence checked**: `docs/ios/lists-content-feedback.md`; `references/ios/content-states.md`.
- **Integration**: new heading "Comparative bar chart card" in `docs/ios/lists-content-feedback.md`. Route from `references/ios/content-states.md` (S-I40).
- **Confidence**: high.
- **Priority**: high. Any usage or analytics screen needs a native reference.

### F018 Capacity and progress bars (iOS)

- **Identity**: Capacity and progress bars; iOS; new-pattern; Lists and content (data summary); content-states.
- **Source**: S-I08, S-I20.
- **Scope**: iCloud+ "Storage" row; iPhone Storage summary.
- **UX problem** (Inferred): show proportion of a total in minimal vertical space.
- **Current coverage**: absent.
- **Gap**: no proportional indicator exists.
- **Visual structure** (Observed): S-I20: under "iPhone  238.2 GB of 1.02 TB used", a thin full-width rounded bar divided into contiguous colored segments (red, orange, a thin yellow-green sliver, gray), a size label near the bar, then a wrapping legend of colored dots and category names on two lines. S-I08: a grouped row with the label "Storage", a capsule bar with a green fill over a lighter gray track between the label and the trailing "3.2 of 4 TB" text, then a chevron.
- **Interaction**: Unconfirmed.
- **States**: one fill level each. Near-full and over-quota colors Unconfirmed.
- **Variations**: segmented bar with legend versus single-fill inline row bar.
- **Evidence**: S-I20 top card; S-I08 (about y 707 to 806).
- **Existing evidence checked**: all four iOS catalog files.
- **Integration**: new heading "Capacity and progress bars" in `docs/ios/lists-content-feedback.md`. Route from `references/ios/content-states.md` (S-I20).
- **Confidence**: high.
- **Priority**: high.

### F019 Loading states: skeleton rows and inline section spinner (iOS)

- **Identity**: Loading states; iOS; new-pattern; Lists and feedback; content-states.
- **Source**: S-I28 (skeleton), S-I14 and S-I25 (spinner).
- **Scope**: TV Provider "Available Apps"; Wi-Fi "Other Networks"; CarPlay "Other Cars".
- **UX problem** (Inferred): show that a section is loading while its header and the rest of the screen stay usable.
- **Current coverage**: absent. `research/coverage.md` marks loading Unconfirmed for iOS.
- **Gap**: first loading evidence.
- **Visual structure** (Observed): skeleton (S-I28): inside one grouped card, four repeated rows with thin dividers; each row has a leading rounded-square light-gray block where an icon would be, two stacked light-gray bars in the middle (the lower one shorter), and a light-gray pill at the trailing edge. All shapes are flat light gray, lighter than the dividers. The section header above is fully rendered. Spinner (S-I14, S-I25): a small circular activity indicator immediately after the gray section header text, on the same baseline, at the header's trailing side, with rows (S-I14) or no rows (S-I25) below.
- **Interaction**: Unconfirmed. No motion or resolution evidence.
- **States**: loading only. Populated counterpart for S-I28 not captured.
- **Variations**: skeleton rows versus header spinner.
- **Evidence**: S-I28 middle third; S-I25 bottom; S-I14 lower-middle.
- **Existing evidence checked**: `references/ios/content-states.md`; `docs/ios/lists-content-feedback.md#centered-empty-state`.
- **Integration**: new heading "Loading states" in `docs/ios/lists-content-feedback.md`. Route from `references/ios/content-states.md` (S-I28, S-I25). Update `research/coverage.md` "Loading and failures" row.
- **Confidence**: high for appearance; low for behavior.
- **Priority**: high.

### F022 Authentication passcode sheet (iOS)

- **Identity**: Authentication passcode sheet; iOS; new-pattern; Presentation; onboarding-permissions and editing.
- **Source**: S-I42.
- **Scope**: sheet presented over an unknown screen between Screen Time (S-I41) and Emergency SOS (S-I43) in the capture sequence. Entry point Unconfirmed (U03).
- **UX problem** (Inferred): re-authenticate before a sensitive settings area with a focused, easily dismissed surface.
- **Current coverage**: absent. `Full-screen task surface` has a trailing commit control. `System permission alert` is a compact centered alert with choices.
- **Gap**: a dismiss-only sheet without a commit control or visible field.
- **Visual structure** (Observed): a gray strip at the top of the image, then a white sheet with rounded top corners. A circular light-gray close button with an X at the top-left. Centered: a filled blue padlock, bold "Enter your passcode", and a two-line gray sentence. More than half the sheet is empty white. No field, keypad, or commit control is visible.
- **Interaction**: Unconfirmed.
- **States**: one static state.
- **Variations**: none.
- **Evidence**: S-I42 full frame; compared by the orchestrator against S-I15 (same sheet framing, but S-I15 has a trailing checkmark).
- **Existing evidence checked**: `docs/ios/navigation-and-presentation.md#full-screen-task-surface`; `docs/ios/forms-and-controls.md#system-permission-alert`; `assets/ios/calendar/event-form.png`; `assets/ios/wallet/location-permission.png`.
- **Integration**: new heading "Authentication passcode sheet" in `docs/ios/navigation-and-presentation.md` (Applicability: system control; single capture). Route from `references/ios/onboarding-permissions.md`.
- **Confidence**: medium. Single capture; entry point and keypad state missing.
- **Priority**: medium.

### F023 Reorderable list with drag handles (iOS)

- **Identity**: Reorderable list with drag handles; iOS; new-pattern; Lists and editing; editing.
- **Source**: S-I27.
- **Scope**: Language & Region "Preferred Languages".
- **UX problem** (Inferred): change the priority order of a short ranked list in place.
- **Current coverage**: absent.
- **Gap**: first reorder affordance.
- **Visual structure** (Observed): a grouped card of five two-line rows (native language name over a gray English name or role). At the trailing edge of every row sits a stack of three short horizontal gray bars, vertically centered, with no chevron. A blue "Add Language…" row closes the card (F007). The navigation bar shows a rounded "Edit" capsule at the trailing edge (F014).
- **Interaction**: Unconfirmed. Whether handles show only after Edit is Unconfirmed (U05).
- **States**: handles visible, resting.
- **Variations**: none.
- **Evidence**: S-I27 top and upper-middle.
- **Existing evidence checked**: `docs/ios/interactions-and-accessibility.md#explicit-selection-mode-application-specific`.
- **Integration**: new heading "Reorderable list" in `docs/ios/lists-content-feedback.md`. Route from `references/ios/editing.md`.
- **Confidence**: medium.
- **Priority**: medium.

### F027 Master switch card (Android)

- **Identity**: Master switch card; Android; new-pattern; Controls; editing.
- **Source**: S-A06, S-A11, S-A16.
- **Scope**: Enhanced HDR brightness ("Use enhanced HDR brightness"), Location ("Use location"), Internet ("Use Wi-Fi").
- **UX problem** (Inferred): give the subsystem that gates everything below it one high-emphasis control, distinct from row switches.
- **Current coverage**: `docs/android/forms-and-controls.md#trailing-switch-in-a-settings-or-list-row` documents a switch as a trailing element in a labeled row with summary text.
- **Gap**: a full-width, taller, icon-free, summary-free card whose only content is a label and a switch, placed first, is undocumented.
- **Visual structure** (Observed): a full-width rounded or stadium-shaped container, taller than a standard row, with a muted dark-green-gray fill (S-A11, S-A06) or the standard card fill (S-A16). A bold label at the leading edge and a switch at the trailing edge, vertically centered. The on-state thumb contains a small check glyph. In S-A16 the card sits under a "Wi-Fi" section label and directly above the connected-network row. In S-A06 the tinted pill sits directly above the "Intensity" slider card it governs. No icon, subtitle, or divider.
- **Interaction**: Unconfirmed.
- **States**: on only.
- **Variations**: tinted fill (S-A11, S-A06) versus standard fill (S-A16).
- **Evidence**: S-A16 (about x 35 to 855, y 435 to 565); S-A11 top (about y 280 to 450); S-A06 upper-middle.
- **Existing evidence checked**: the trailing-switch entry; `references/android/editing.md`.
- **Integration**: new heading "Master switch card" in `docs/android/forms-and-controls.md`. Route from `references/android/editing.md` (S-A11).
- **Confidence**: high.
- **Priority**: high.

### F029 Inline value slider (Android)

- **Identity**: Inline value slider; Android; new-pattern; Value selection; editing.
- **Source**: S-A01, S-A06.
- **Scope**: Sound & vibration volume channels; HDR "Intensity".
- **UX problem** (Inferred): adjust a continuous value in place and read its position at a glance.
- **Current coverage**: absent. `Modal time picker` is a dialog.
- **Gap**: no inline slider exists.
- **Visual structure** (Observed): each slider sits in its own rounded card. S-A01: a bold label at the top of the card, then a wide track with a light filled segment from the left edge to a thin vertical handle line, a dark unfilled remainder, and a small trailing glyph at the right end (music note, phone, ringer-off, bell, alarm clock, waveform). Six such cards stack as peers. S-A06: one card labeled "Intensity", the same track and handle, and text end labels "Dimmer" and "Brighter" below the track ends instead of a glyph.
- **Interaction**: Unconfirmed.
- **States**: one resting position each.
- **Variations**: trailing glyph versus text end labels.
- **Evidence**: S-A01 upper-middle to lower area; S-A06 lower-middle card.
- **Existing evidence checked**: `docs/android/forms-and-controls.md#modal-time-picker`; `references/android/editing.md`.
- **Integration**: new heading "Inline value slider" in `docs/android/forms-and-controls.md`. Route from `references/android/editing.md` (S-A01).
- **Confidence**: high.
- **Priority**: high.

### F030 Credential entry form (Android)

- **Identity**: Credential entry form: outlined field with visibility toggle and required helper, expander row, Cancel/Connect pair; Android; new-pattern; Forms and editing; editing.
- **Source**: S-A14 (reached from S-A16).
- **Scope**: Wi-Fi join screen titled with a network name.
- **UX problem** (Inferred): enter one sensitive required value, reveal it on demand, reach optional fields, and commit or cancel.
- **Current coverage**: `Structured create-contact form` documents outlined fields without a visibility toggle or required helper. `Modal time picker` documents Cancel/OK in a dialog only.
- **Gap**: password field anatomy, an inline expander, and a full-screen button pair are undocumented.
- **Visual structure** (Observed): a "Password*" floating label above an active entry line with a cursor, a trailing eye-outline icon, and "*required" in small text under the line. Below: a full-width rounded row "Advanced options" with a trailing downward chevron in a small dark circle. Below that, right-aligned: an outlined pill "Cancel" and a filled pill "Connect" in a muted, lower-contrast fill. A software keyboard fills the lower half of the screen. The top bar holds a back button and the network name as the title.
- **Interaction**: Unconfirmed. The muted "Connect" fill is Inferred as disabled (U10). The expanded state is not captured (U11).
- **States**: empty, focused, collapsed, pre-commit.
- **Variations**: none.
- **Evidence**: S-A14 upper third (field), middle (expander and buttons), lower half (keyboard).
- **Existing evidence checked**: `docs/android/forms-and-controls.md#structured-create-contact-form`; `#modal-time-picker`.
- **Integration**: new heading "Credential entry form" in `docs/android/forms-and-controls.md` (Applicability: system control; single capture). Route from `references/android/editing.md` (S-A16 to S-A14 as list-to-form pair).
- **Confidence**: medium. Single capture.
- **Priority**: medium.

### F031 Detail top bar with back and title; large in-content title variant (Android)

- **Identity**: Detail top bar; Android; new-pattern; Navigation and presentation; navigation.
- **Source**: all Android detail screens (S-A01 to S-A16, S-A18 to S-A20); large-title variant S-A07; trailing actions S-A16, S-A18, S-A19.
- **Scope**: every Settings detail screen.
- **UX problem** (Inferred): show where the user is and how to leave, with at most one trailing action.
- **Current coverage**: absent as anatomy. `Semantic labels for icon-only actions` documents only the "Navigate up" content description. No entry describes the bar.
- **Gap**: the basic detail-screen bar has no entry, and one screen departs from it.
- **Visual structure** (Observed): a circular dark back button at the leading edge and a title in a single line to its right (19 screens). Optional trailing controls: a pencil edit icon (S-A18), a three-dot overflow (S-A19), an icon of unresolved function (S-A16, U15). Variant (S-A07): the back button sits alone in the bar; the title "Safety & emergency" renders as large display text lower in the content column, left-aligned to the content margin, above an outlined pill action (F035).
- **Interaction**: Unconfirmed, including scroll collapse (U14).
- **States**: resting.
- **Variations**: inline title versus large in-content title; trailing action present or absent.
- **Evidence**: S-A18 top (pencil); S-A19 top (overflow); S-A07 top third (large title).
- **Existing evidence checked**: `docs/android/navigation-and-presentation.md`; `docs/android/interactions-and-accessibility.md#semantic-labels-for-icon-only-actions`; `assets/android/settings/root.png`.
- **Integration**: new heading "Detail top bar" in `docs/android/navigation-and-presentation.md` with the large-title variant. Route from `references/android/navigation.md` as a comparison pair (S-A18, S-A07).
- **Confidence**: medium for the large-title variant (one instance); high for the bar.
- **Priority**: medium.

### F032 Centered detail header with icon action-button row (Android)

- **Identity**: Centered detail header with icon action-button row; Android; new-pattern; Navigation and presentation; navigation.
- **Source**: S-A18.
- **Scope**: Network details.
- **UX problem** (Inferred): identify one entity and expose a small set of entity-scoped actions before its attributes.
- **Current coverage**: absent.
- **Gap**: no centered header or icon-button row exists in the Android catalog.
- **Visual structure** (Observed): centered under the top bar, a large outlined Wi-Fi glyph, then the network name in large bold text, then "Connected" in lighter text. Below, three equally spaced circular buttons with muted gray fill, each with a centered glyph (trash, X, share grid) and a label beneath ("Forget", "Disconnect", "Share"). The destructive action has the same weight as the others. No container or divider separates the block from the label/value rows below (F033).
- **Interaction**: Unconfirmed, including confirmation for "Forget".
- **States**: connected only.
- **Variations**: none.
- **Evidence**: S-A18 upper third (about x 40 to 855, y 300 to 870).
- **Existing evidence checked**: `docs/android/navigation-and-presentation.md`; `docs/android/lists-content-feedback.md`.
- **Integration**: new heading in `docs/android/navigation-and-presentation.md` (Applicability: general idiom; single capture). Route from `references/android/navigation.md`.
- **Confidence**: high for anatomy.
- **Priority**: medium.

### F034 Recent-items row with relative time and See-all continuation (Android)

- **Identity**: Recent-items row with See-all continuation; Android; new-pattern; Lists and content; content-states.
- **Source**: S-A04, S-A11, S-A15.
- **Scope**: Apps "Recently opened apps"; Location "Recent access"; Connected devices "Saved devices".
- **UX problem** (Inferred): show which items were used recently and when, then offer the full list.
- **Current coverage**: absent. `Grouped card list` secondary text is a static summary.
- **Gap**: recency rows and three continuation controls are undocumented.
- **Visual structure** (Observed): rows with a circular full-color app icon on a white disc, a bold app name, and a gray relative-time line ("1 minute ago", "2 minutes ago"), ordered most recent first, with thin dividers inside one card. No trailing control. Continuation: (a) a row inside the same card with a chevron at the leading edge and "See all 102 apps" (S-A04); (b) an outlined pill "See all" with a leading three-dot icon below the card (S-A11); (c) a card row with a leading chevron and "See all" under "Saved devices" (S-A15).
- **Interaction**: Unconfirmed.
- **States**: populated only.
- **Variations**: (a) to (c).
- **Evidence**: S-A04 upper-middle; S-A11 (about y 530 to 800, pill at y 1000 to 1075); S-A15 middle.
- **Existing evidence checked**: `docs/android/lists-content-feedback.md#grouped-card-list`; `references/android/content-states.md`.
- **Integration**: new heading "Recent-items list with See-all continuation" in `docs/android/lists-content-feedback.md`. Route from `references/android/content-states.md` (S-A04).
- **Confidence**: high.
- **Priority**: medium.

### F035 Inline pill button (Android)

- **Identity**: Inline pill button (outlined or tonal); Android; new-pattern; Controls; navigation and editing.
- **Source**: S-A02, S-A03, S-A07, S-A10, S-A11, S-A12, S-A19.
- **Scope**: Modes ("+ Create your own mode"), Security & privacy ("3 More alerts"), Safety & emergency ("Open Personal Safety"), Wallpaper & style ("Wallpapers", "More wallpapers"), Location ("See all"), Digital Wellbeing ("View app activity details").
- **UX problem** (Inferred): give a secondary or creation action a compact tappable control that is neither a filter chip nor a floating action.
- **Current coverage**: `Labeled chip or compact filter control` documents peer filter sets with selection. `Floating primary action` documents filled floating controls. Neither matches.
- **Gap**: seven instances across six screens with no entry.
- **Visual structure** (Observed): a stadium-shaped container sized to its content or spanning the card width. Variants: full-width outlined with a leading plus glyph after a list (S-A02); full-width outlined with no icon inside a card (S-A19); content-sized outlined with a leading icon, left-aligned above rows (S-A07); content-sized outlined with a leading numeral badge (S-A03 "3"); content-sized outlined with a leading three-dot icon (S-A11); content-sized tonal filled with a leading image icon, centered (S-A10, S-A12). None sits in a horizontal peer row and none shows a selected state.
- **Interaction**: Unconfirmed.
- **States**: resting only.
- **Variations**: as listed.
- **Evidence**: S-A02 bottom of content; S-A03 (about y 1035 to 1110); S-A07 upper-middle; S-A10 (about y 910 to 990); S-A19 inside the top card.
- **Existing evidence checked**: both entries named above.
- **Integration**: new heading "Inline pill button" in `docs/android/forms-and-controls.md`, cross-referenced from the chip and floating action entries. Route from `references/android/editing.md` (S-A02) and `references/android/navigation.md` (S-A07).
- **Confidence**: high.
- **Priority**: high.

### F037 Status overview card with per-item status badges (Android)

- **Identity**: Status overview card with per-item status badges; Android; new-pattern; Content and state feedback; content-states and accessibility.
- **Source**: S-A03.
- **Scope**: Security & privacy.
- **UX problem** (Inferred): communicate overall health first, then the outcome of each independent check.
- **Current coverage**: absent. `Visible selected and unchecked states` covers selection and switches, not outcomes.
- **Gap**: no status banner or outcome badge exists.
- **Visual structure** (Observed): a full-width dark rounded card with a green shield glyph at the leading side, bold "Looks good", and a dim "Checking device settings…" subtitle; no control. Below, under a "Security" label, rows in one card each lead with a small solid-green circle containing a white check, then a bold title and a gray status subtitle ("Play Protect scanning is on"). No trailing control.
- **Interaction**: Unconfirmed. Whether "Checking…" is a loading state is Unconfirmed (U12).
- **States**: all-passed only. Warning and failed states not captured.
- **Variations**: none.
- **Evidence**: S-A03 top (about y 280 to 470) and lower region (y 1230 to bottom).
- **Existing evidence checked**: `docs/android/lists-content-feedback.md#grouped-card-list`; `docs/android/interactions-and-accessibility.md#semantic-selected-and-checked-state`.
- **Integration**: new heading in `docs/android/lists-content-feedback.md` (Applicability: settings idiom; single capture), with an accessibility note that a color-only badge needs a semantic state. Route from `references/android/content-states.md` and `references/android/accessibility.md`.
- **Confidence**: medium. Single screen; semantics unknown without a hierarchy dump.
- **Priority**: medium.

### F038 Inline suggestion card (Android)

- **Identity**: Inline suggestion card; Android; new-pattern; Lists, content, and feedback; content-states and onboarding-permissions.
- **Source**: S-A03, S-A08, S-A13, S-A19.
- **Scope**: Security & privacy ("Add more fingerprints"), Digital Wellbeing ("Sleep better with Bedtime mode"), Parental controls ("Get Google Family Link"), Storage ("Free up space").
- **UX problem** (Inferred): recommend an optional action inline without blocking the screen.
- **Current coverage**: `Sign-in or permission primer` covers blocking modal or full-page primers with Skip or Not now.
- **Gap**: a non-blocking card, scrollable with the list, with a dismiss X or none, is undocumented.
- **Visual structure** (Observed): (a) S-A03: a full-width dark card with a small dim eyebrow label "Device unlock" top-left, a circular X top-right, a bold title, two lines of body, and a full-width filled green stadium button "Add more". (b) S-A19: a card with a leading circular icon, a bold two-line title, a gray body, and a small X at the trailing edge aligned near the title baseline. (c) S-A13 and S-A08: a card with a lighter or more saturated tint than the rows around it, a circular white-background app icon, a bold title, two or three lines of body, and a trailing chevron (S-A13) or nothing (S-A08); no dismiss control.
- **Interaction**: Unconfirmed, including dismissal (U08).
- **States**: un-dismissed only.
- **Variations**: (a) to (c).
- **Evidence**: S-A03 (about y 480 to 1000); S-A19 lower-middle; S-A13 lower-middle; S-A08 upper-middle.
- **Existing evidence checked**: `docs/android/lists-content-feedback.md#sign-in-or-permission-primer`; `assets/android/photos/sign-in-primer.png`.
- **Integration**: new heading "Inline suggestion card" in `docs/android/lists-content-feedback.md` as a sibling of the primer entry. Route from `references/android/content-states.md` (S-A03) and cross-reference from `references/android/onboarding-permissions.md`.
- **Confidence**: high.
- **Priority**: high.

### F039 Ring chart summary card with stat tiles (Android)

- **Identity**: Ring chart summary card with stat tiles; Android; new-pattern; Data summary; content-states.
- **Source**: S-A19.
- **Scope**: Digital Wellbeing.
- **UX problem** (Inferred): show a total, its composition, and a few short numeric facts without a chart screen.
- **Current coverage**: absent.
- **Gap**: no data visualization exists in the Android catalog.
- **Visual structure** (Observed): a large rounded card with a thick ring mostly in one light color and a smaller differently colored "Other" arc labeled above it. Centered inside the ring: a small "Today" caption above a large "5 hr, 50 …" value (truncated). Below the ring a caption names the dominant app, then a full-width outlined pill "View app activity details" (F035). Below the card, two equal-width square-ish tiles side by side, each with a large numeral over a gray caption ("3 / Unlocks", "3 / Notifications"), aligned top and bottom, with a gap between.
- **Interaction**: Unconfirmed.
- **States**: populated, two segments.
- **Variations**: Unconfirmed.
- **Evidence**: S-A19 upper and middle thirds.
- **Existing evidence checked**: `docs/android/lists-content-feedback.md`; `references/android/content-states.md`.
- **Integration**: new heading in `docs/android/lists-content-feedback.md` (Applicability: general idiom; single capture). Route from `references/android/content-states.md`.
- **Confidence**: medium. Single instance.
- **Priority**: medium.

### F040 Storage numeral with capacity bar and per-row usage bars (Android)

- **Identity**: Storage numeral with capacity bar and per-row usage bars; Android; new-pattern; Data summary; content-states.
- **Source**: S-A08.
- **Scope**: Storage.
- **UX problem** (Inferred): summarize an aggregate quantity and the share of each category on one screen.
- **Current coverage**: absent. The Settings root row shows the same total as text only.
- **Gap**: no numeral or bar treatment exists.
- **Visual structure** (Observed): a large display-weight "51" beside a small stacked "GB used", with "128 GB total" right-aligned on the same line. Below, a full-width rounded bar filled from the leading edge to a proportional stop, lighter fill over a darker track, with a small dot at the trailing end. Then a promo card (F038) and category rows, each with a leading glyph, a label, a right-aligned size, and a thin per-row bar under the label filled proportionally with the same end-dot treatment.
- **Interaction**: Unconfirmed.
- **States**: populated.
- **Variations**: none.
- **Evidence**: S-A08 top region and lower half.
- **Existing evidence checked**: `docs/android/lists-content-feedback.md#grouped-card-list`; `assets/android/settings/root.png`.
- **Integration**: new heading in `docs/android/lists-content-feedback.md` (Applicability: general idiom; single capture). Route from `references/android/content-states.md`.
- **Confidence**: medium. Single instance.
- **Priority**: medium.

### F041 Screen intro paragraph and info footnote (Android)

- **Identity**: Screen intro paragraph and info footnote; Android; new-pattern; Screen framing; content-states and navigation.
- **Source**: S-A02, S-A06, S-A11, S-A13, S-A15.
- **Scope**: Modes and HDR (intro paragraph); HDR, Location, Connected devices (info footnote); Parental controls (plain footer).
- **UX problem** (Inferred): frame a screen or a control with short explanatory copy that is not a row.
- **Current coverage**: absent. Explanatory text exists only in empty-state and primer entries.
- **Gap**: uncontained copy above rows and below cards is undocumented.
- **Visual structure** (Observed): intro: directly under the title, a two- or three-line gray paragraph spanning the content width, then a gap before the first card (S-A02, S-A06). Footnote: below the last card, a small circled "i" icon above or beside a gray sentence or paragraph, left-aligned to the margin, with no card background (S-A06, S-A11, S-A15). Plain footer: the same without an icon (S-A13).
- **Interaction**: none visible.
- **States**: static.
- **Variations**: intro versus footnote versus plain footer.
- **Evidence**: S-A02 upper portion; S-A06 upper portion and lower portion; S-A15 (about y 1420 to 1520); S-A11 lower region; S-A13 bottom.
- **Existing evidence checked**: `docs/android/lists-content-feedback.md#illustrated-empty-state`; `#sign-in-or-permission-primer`.
- **Integration**: new heading "Screen intro paragraph and info footnote" in `docs/android/navigation-and-presentation.md`. Route from `references/android/content-states.md` (S-A06 shows both).
- **Confidence**: high.
- **Priority**: medium.

---

## Proposed variations

### F014 Pushed-destination bar with inline centered title and trailing action (iOS)

- **Identity**: existing-pattern-variation of `docs/ios/navigation-and-presentation.md#large-title-hierarchy`; navigation.
- **Source**: S-I02, S-I03, S-I06, S-I09, S-I14, S-I27, S-I31, S-I39 (and all other pushed screens).
- **Scope**: every pushed Settings screen in the corpus.
- **UX problem** (Inferred): show the current level and the return path on a pushed screen without a large title.
- **Current coverage**: the entry says a rounded back control replaces the large title on a pushed destination and cites General. The orchestrator confirmed by crop that `assets/ios/settings/general.png` shows the back circle with no title in the bar; the name appears only in the hero card.
- **Gap**: 43 new pushed screens show a bold centered inline title in the bar beside the back circle, with no duplicate heading below. Trailing bar actions are also undocumented: a rounded "Edit" capsule (S-I06, S-I14, S-I27), a circular "+" (S-I39), and a circular add-person icon (S-I09), each matching the back circle's size and vertical position.
- **Visual structure** (Observed): circular white back button with a chevron at the leading edge; a bold single-line centered title, smaller than a large title; an optional trailing circular or capsule control symmetric with the back button.
- **Interaction**: Unconfirmed.
- **States**: resting; scrolled (F013).
- **Variations**: bare back control with hero-card title (existing General) versus inline title (new); trailing text capsule versus icon circle.
- **Evidence**: S-I31 top (inline title, no trailing action); S-I27 top (Edit); S-I39 top (+).
- **Existing evidence checked**: `assets/ios/settings/general.png` (opened by W01, W08, and the orchestrator); `assets/ios/shortcuts/empty-library.png` (W09, floating add for contrast).
- **Integration**: amend Large-title hierarchy's Visual structure, States, and Variations. Add a route row in `references/ios/navigation.md`: "Pushed screen with inline title and trailing action" (S-I27).
- **Confidence**: high.
- **Priority**: high. The current wording implies pushed screens have no bar title.

### F020 Centered status confirmation (iOS)

- **Identity**: existing-pattern-variation of `docs/ios/lists-content-feedback.md#centered-empty-state`; content-states.
- **Source**: S-I19.
- **Scope**: Software Update.
- **UX problem** (Inferred): confirm that nothing remains to do, as distinct from an empty collection.
- **Current coverage**: the entry covers empty collections and zero results with a muted symbol, bold title, and optional sentence.
- **Gap**: the same composition is used for an affirmative state and adds a link.
- **Visual structure** (Observed): centered in open background: a filled gray circle with a white check, bold "iOS is up to date", gray "iOS 27.0", and a centered blue "More Details" link with spacing above it. Two value rows sit in a card at the top of the screen.
- **Interaction**: Unconfirmed.
- **States**: up to date only.
- **Variations**: check glyph and appended link.
- **Evidence**: S-I19 vertical center.
- **Existing evidence checked**: the centered empty state entry (text).
- **Integration**: broaden the entry's Description and Variations to cover affirmative status and an appended link. Route from `references/ios/content-states.md` (S-I19).
- **Confidence**: high.
- **Priority**: medium.

### F021 Single-field card sheet with gated commit (iOS)

- **Identity**: existing-pattern-variation of `Full-screen task surface` and `Content-gated commit control`; editing.
- **Source**: S-I14 (list) and S-I15 (sheet).
- **Scope**: Wi-Fi join sheet for an unauthenticated network.
- **UX problem** (Inferred): collect one required credential with the same dismiss/commit separation as a form, at lighter weight.
- **Current coverage**: both entries cite Calendar and Contacts forms with grouped left-aligned rows and a keyboard.
- **Gap**: the body composition differs, and the keyboard is absent despite an empty required field.
- **Visual structure** (Observed): a card sheet with rounded top and bottom corners over a dimmed gray strip at the top and bottom of the image. Leading: a white circular X button. Trailing: a gray-filled circular checkmark (dimmed). Centered: a blue Wi-Fi glyph, bold "Join “<network name>”", and a gray instruction. One full-width rounded white field with placeholder "Password", then a small gray caption. The rest of the sheet is empty. No keyboard.
- **Interaction**: Unconfirmed.
- **States**: empty, unfocused, commit disabled.
- **Variations**: centered single field versus grouped rows; no keyboard on entry versus Immediate keyboard focus.
- **Evidence**: S-I15 top third and bottom (orchestrator crops); `assets/ios/calendar/event-empty.png` for framing comparison (W04).
- **Existing evidence checked**: both entries and the Calendar asset.
- **Integration**: add a "compact single-field variant" to Full-screen task surface; add Settings as a third application under Content-gated commit control; add a caveat to Immediate keyboard focus. Route from `references/ios/editing.md` as a pair (S-I14, S-I15).
- **Confidence**: medium.
- **Priority**: medium.

### F025 Identity-led list row variations (iOS)

- **Identity**: existing-pattern-variation of `docs/ios/lists-content-feedback.md#identity-led-list-row`; content-states.
- **Source**: S-I01, S-I06, S-I07, S-I09, S-I10, S-I11, S-I20, S-I21, S-I23, S-I28, S-I37, S-I41.
- **Scope**: Settings root account and Family rows; Payment methods; Subscriptions; Family; Find My; Sign in with Apple; iPhone Storage; AppleCare; TV Provider; Notifications per-app rows.
- **UX problem** (Inferred): reuse one scan order (image, label, metadata, trailing) for people, apps, cards, and devices.
- **Current coverage**: circular initials badge, plain list with index rail, phone or date metadata (Contacts, Messages).
- **Gap**: the new rows differ in containment, leading image, secondary text, and trailing metadata.
- **Visual structure** (Observed): rows sit inside grouped cards with no index rail. Leading images: photographic circular avatars (S-I09, S-I10, S-I41); three overlapped circular thumbnails as a group cue (S-I01 "Family"); rounded-square app icons (S-I07, S-I11, S-I20, S-I28, S-I37); a wide rectangular card-art image (S-I06); a device glyph (S-I23). Secondary text: a role ("Age <n>", "Organizer"), "Last used: <date>", a comma-separated capability list ("Banners, Sounds, Announce"), or two lines (plan then "Next Billing Date"). Primary labels truncate mid-string with an ellipsis (S-I07). Trailing: a price then chevron (S-I07), a size then chevron (S-I20), a count then chevron (S-I05 "2"), or a switch (S-I28). The signed-in account row (S-I01) uses a larger photo, a bold name, and a status line where the existing root capture shows a dotted circle and a sign-in prompt.
- **Interaction**: Unconfirmed.
- **States**: populated only.
- **Variations**: as listed.
- **Evidence**: S-I07 (about y 517 to 1650); S-I06 (about y 517 to 937); S-I09 middle; S-I37 bottom edge; S-I01 top card; `assets/ios/settings/root.png` (W01 comparison).
- **Existing evidence checked**: the entry; `assets/ios/settings/root.png`.
- **Integration**: amend Visual structure, States, and Variations; add "leading image shape" and "trailing metric" fields. Route from `references/ios/content-states.md` (S-I07).
- **Confidence**: high.
- **Priority**: medium.

### F026 Pinned search field over a scrolling detail list (iOS)

- **Identity**: existing-pattern-variation of `docs/ios/forms-and-controls.md#search-field-with-dictation-affordance`; search.
- **Source**: S-I20, S-I21.
- **Scope**: iPhone Storage at two scroll offsets.
- **UX problem** (Inferred): keep search reachable on a long list without a fixed header slot.
- **Current coverage**: the entry notes that Settings root anchors Search near the bottom.
- **Gap**: on a long detail list the field stays at one screen position above the bottom edge and overlaps rows that scroll under it; placeholder reads "Applications", not "Search".
- **Visual structure** (Observed): a full-width rounded translucent field with a leading magnifier, gray placeholder "Applications", and a trailing microphone. Row content is faintly visible through it. The field cuts across the "Messages" row in S-I20 and different rows in S-I21.
- **Interaction**: Unconfirmed. Pinning is Inferred from two offsets.
- **States**: resting at two offsets.
- **Variations**: bottom-edge (root) versus pinned above the edge (detail).
- **Evidence**: S-I20 and S-I21 lower portion; `assets/ios/settings/root.png` (W05 comparison).
- **Existing evidence checked**: the entry; `references/ios/search.md`; the root asset.
- **Integration**: amend the Variations field. Route from `references/ios/search.md` (S-I21).
- **Confidence**: medium.
- **Priority**: low.

### F036 Inline creation row with leading plus (Android)

- **Identity**: existing-pattern-variation of `docs/android/lists-content-feedback.md#floating-primary-action`; content-states.
- **Source**: S-A15.
- **Scope**: Connected devices "Pair new device".
- **UX problem** (Inferred): place a creation action inline on a dense settings screen instead of floating it.
- **Current coverage**: three floating examples.
- **Gap**: a same-weight list row with a plain plus glyph and no tinted background.
- **Visual structure** (Observed): a card row with a plain plus glyph at the leading edge and bold "Pair new device", matching the "USB" row above in height and style.
- **Interaction**: Unconfirmed.
- **States**: resting.
- **Variations**: inline row versus floating control; compare the outlined pill creation control in S-A02 (F035).
- **Evidence**: S-A15 (about y 610 to 740).
- **Existing evidence checked**: the floating primary action entry.
- **Integration**: amend the entry's Variations field and cross-reference F035. Route from `references/android/content-states.md` (S-A15).
- **Confidence**: medium.
- **Priority**: low.

---

## Existing pattern improvements

### F004 Grouped rows: section header, footer caption, mixed trailing controls, read-only use (iOS)

- **Identity**: existing-pattern-improvement of `docs/ios/forms-and-controls.md#grouped-form-rows`; editing and content-states.
- **Source**: S-I01, S-I03, S-I05, S-I06, S-I10, S-I11, S-I12, S-I18, S-I19, S-I26, S-I27, S-I28, S-I31, S-I33, S-I34, S-I35, S-I37, S-I38, S-I39, S-I41, S-I43, S-I44.
- **Scope**: nearly every screen.
- **UX problem** (Inferred): frame a group with a name and a consequence, and mix control types by topic.
- **Current coverage**: the entry describes rounded white groups with separators from two edit forms. It names no section header, no footer, no mixed controls, and no read-only use.
- **Gap**: the wording is too narrow ("form rows") and the anatomy is incomplete.
- **Visual structure** (Observed): a small gray left-aligned caption above a card, outside it ("Email & Phone Numbers", "Vision", "Silent Mode", "Device Info"). A small gray left-aligned paragraph below a card, outside it, wrapping to two to four lines; it can embed one blue inline link ("Learn more…" in S-I06) or state account status (S-I28). One card can mix switch rows, value-plus-chevron rows, chevron-only rows, and link rows (S-I01, S-I05). The same container serves read-only navigable settings outside any editing task (S-I19).
- **Interaction**: none for captions.
- **States**: static.
- **Variations**: header only; header and footer; footer with inline link; mixed controls.
- **Evidence**: S-I05 (about y 480 to 520 header; y 1440 to 1620 footer); S-I06 (about y 990 to 1140 footer with link); S-I01 middle card (mixed controls); S-I26 (footers under switch groups).
- **Existing evidence checked**: the entry; `docs/ios/lists-content-feedback.md#centered-empty-state`.
- **Integration**: rename or broaden the heading to "Grouped rows" and add Section header, Footer caption, and Trailing control fields. Keep the mapping row in `supporting/native-ui-patterns/README.md` in sync. Route from `references/ios/editing.md` (S-I05).
- **Confidence**: high.
- **Priority**: high.

### F024 Row trailing accessories: info button, external-link arrow, menu caret, selected checkmark (iOS)

- **Identity**: existing-pattern-improvement of `Grouped form rows` and `Identity-led list row`; navigation and accessibility.
- **Source**: S-I03, S-I14, S-I16, S-I44.
- **Scope**: Personal Information "Share Automatically"; Wi-Fi network rows; Bluetooth device rows; Game Center rows.
- **UX problem** (Inferred): let a user tell navigation, inline choice, external destination, and an independent detail target apart before tapping.
- **Current coverage**: both entries imply only a chevron, a value, or a date at the trailing edge.
- **Gap**: four accessories are undocumented.
- **Visual structure** (Observed): (a) a circled "i" at the far trailing edge, separated by spacing from status glyphs (lock, signal in S-I14) or status text ("Not Connected" in S-I16), reading as its own target; (b) a small diagonal up-right arrow instead of a chevron on rows that leave the stack (S-I44 profile, "All Friends 3", "Friend Requests"), while "Share Friends List  On >" keeps a chevron on the same screen; (c) a stacked up/down caret pair after the value "Contacts Only" (S-I03), where sibling rows use a chevron; (d) a blue check at the leading edge of the connected network row (S-I14).
- **Interaction**: Unconfirmed (U02, U07).
- **States**: resting; one selected row.
- **Variations**: as listed.
- **Evidence**: S-I14 (about y 980 to 1020 and 1650 to 1950); S-I16 (about y 1120 to 1900); S-I44 (about y 440 to 620 and 1130 to 1330); S-I03 middle third.
- **Existing evidence checked**: both entries.
- **Integration**: add a "Trailing accessory" field to Grouped rows listing chevron, value, switch, info button, external-link arrow, menu caret, and none, plus the leading selected check. Route from `references/ios/accessibility.md` (S-I16, independent target) and `references/ios/navigation.md` (S-I44).
- **Confidence**: medium.
- **Priority**: medium.

### F028 Trailing switch: on/off thumb glyphs and multi-line description (Android)

- **Identity**: existing-pattern-improvement of `docs/android/forms-and-controls.md#trailing-switch-in-a-settings-or-list-row`; editing.
- **Source**: S-A18, S-A20.
- **Scope**: Network details ("Share network", "Allow users to edit network"); Sound & vibration "System sounds & vibrations".
- **UX problem** (Inferred): read on/off beyond color and explain a consequential setting in more than a phrase.
- **Current coverage**: the entry records only `checked="false"` examples and a short summary line.
- **Gap**: the on state and the thumb glyphs are undocumented.
- **Visual structure** (Observed): on: a light filled track with a darker circular thumb containing a thin check glyph. Off: an outlined unfilled track with a hollow thumb containing a thin X (S-A20 "Always show icon when in vibrate mode"). In S-A18 each switch row carries a two- or three-line explanatory sentence under the label; the switch stays aligned to the label line, not the text block.
- **Interaction**: Unconfirmed.
- **States**: on and off.
- **Variations**: one-line rows (S-A20) versus multi-line description rows (S-A18).
- **Evidence**: S-A20 lower half; S-A18 (about y 1340 to 1650); `assets/android/settings/display-and-touch.png` (W12, thumb too small to confirm a glyph).
- **Existing evidence checked**: the entry and the existing asset.
- **Integration**: amend States and Visual structure. Route from `references/android/editing.md` (S-A20).
- **Confidence**: high.
- **Priority**: high. Closes a gap the entry itself flags.

### F033 Grouped card list anatomy (Android)

- **Identity**: existing-pattern-improvement of `docs/android/lists-content-feedback.md#grouped-card-list`; content-states and navigation.
- **Source**: S-A02, S-A05, S-A07, S-A13, S-A15, S-A16, S-A18.
- **Scope**: Modes, Network & internet, Safety & emergency, Parental controls, Connected devices, Internet, Network details.
- **UX problem** (Inferred): keep one container legible when rows differ in icon presence, interactivity, and trailing control.
- **Current coverage**: the entry describes uniform icon, title, and summary rows that navigate.
- **Gap**: five row forms are undocumented.
- **Visual structure** (Observed): (a) informational rows with a leading icon, bold label, and value line but no trailing control (S-A18 "Signal strength / Excellent"); (b) icon-less rows at the end of an icon-led card, label indented to the text column (S-A05 "Private DNS", S-A15 "Connection preferences", S-A13 "Set up a parental controls PIN", S-A07 second card); (c) flat monochrome glyph icons on detail screens versus colored circular badges on the root (S-A07, S-A13 versus S-A17); (d) single-line rows with a leading Wi-Fi glyph and a trailing padlock glyph instead of summary text (S-A16 "Networks"); (e) a circular outlined gear icon button at the trailing edge of the connected-network row (S-A16); (f) leading circular icon, bold label, and gray status line with no chevron (S-A02 Modes).
- **Interaction**: Unconfirmed (U09).
- **States**: resting.
- **Variations**: (a) to (f).
- **Evidence**: S-A18 (about y 940 to 1310); S-A05 lower third; S-A16 (gear about x 700 to 855, y 585 to 670; list lower two-thirds); S-A02 middle.
- **Existing evidence checked**: the entry; `assets/android/settings/root.png` (W14).
- **Integration**: amend Visual structure and Variations, and add a "Trailing control" field (none, chevron, switch, icon button, status glyph). Route from `references/android/content-states.md` (S-A18) and `references/android/navigation.md` (S-A16).
- **Confidence**: high.
- **Priority**: high.

### F042 Signed-in account row and dark theme on Settings root (Android)

- **Identity**: existing-pattern-improvement of `Search-led top surface` and `Grouped card list`; navigation.
- **Source**: S-A17.
- **Scope**: Settings root.
- **UX problem** (Inferred): represent the signed-in account at the top of the root.
- **Current coverage**: `assets/android/settings/root.png` is light theme, signed out, with a generic "G" icon.
- **Gap**: no signed-in or dark-theme root exists.
- **Visual structure** (Observed): a full-width dark pill search field with a magnifier and "Search Settings". Below it, a card row with a circular photo avatar, a bold account name, and gray "Google services and preferences". Category rows follow with tinted circular icons, bold labels, and one-line summaries. Cards are dark gray on a near-black background.
- **Interaction**: Unconfirmed.
- **States**: signed in, dark.
- **Variations**: photo avatar versus icon; dark versus light.
- **Evidence**: S-A17 top third; `assets/android/settings/root.png` (W11 comparison).
- **Existing evidence checked**: both entries and the root asset.
- **Integration**: add Variations notes to both entries. Route from `references/android/navigation.md` as a comparison pair with the existing root (dark signed-in versus light signed-out). Update the SKILL.md metadata sentence that all Android captures are light and signed out.
- **Confidence**: high.
- **Priority**: medium.

---

## Duplicates

| ID | Candidate | Screenshots | Matching existing entry | Why adequate |
| --- | --- | --- | --- | --- |
| D01 | Circular back control on pushed screens | all pushed iOS screens | `docs/ios/navigation-and-presentation.md#large-title-hierarchy` | The rounded back control is documented; only the inline title and trailing action are new (F014). |
| D02 | Rounded grouped container with thin dividers | S-I05, S-I06, S-I07, S-I08, S-I23, S-I24, S-I25 | `docs/ios/forms-and-controls.md#grouped-form-rows` | Container geometry matches; anatomy additions are F004. |
| D03 | Label, trailing value, chevron row | S-I03, S-I18, S-I19, S-I21, S-I22, S-I27, S-I37, S-I38, S-I44 | `docs/ios/forms-and-controls.md#grouped-form-rows` | "Labeled option rows with trailing current values" already covers it. |
| D04 | Family member row with photo avatar | S-I41 | `docs/ios/lists-content-feedback.md#identity-led-list-row` | Same badge, label, chevron anatomy. |
| D05 | Split row with chevron, vertical divider, and switch | S-A09 | `docs/android/forms-and-controls.md#trailing-switch-in-a-settings-or-list-row` | The entry states this pairing; W12 confirmed against the existing asset. |
| D06 | Airplane mode row with off switch | S-A05 | same entry | Same anatomy and state. |
| D07 | Grouped title/summary rows and section captions | S-A09, S-A10, S-A11, S-A13, S-A17, S-A19, S-A20 | `docs/android/lists-content-feedback.md#grouped-card-list` | Baseline anatomy matches; deltas are F033. |
| D08 | Closed overflow trigger in the top bar | S-A19 | `docs/android/navigation-and-presentation.md#contextual-overlay-menu` | Closed trigger only; no new anatomy. |

## Application-specific findings

| ID | Observation | Screenshots | Why not generalized |
| --- | --- | --- | --- |
| A01 | iCloud+ brand hero header: back circle alone, left-aligned two-line header, circular "SUBSCRIBER · ICLOUD+" badge | S-I08 | Sub-brand treatment; recorded as a variant note under F012. |
| A02 | Two-column icon-tile grid inside one card with count, size, or "Off" per tile | S-I08 | One instance in one hub. Candidate for a later entry if a second instance appears. |
| A03 | Wallpaper preview carousel with peek edges, "Customize" pills, page dots, "+ Add New Wallpaper" capsule | S-I36 | One instance; comparable to the existing `Photo thumbnail grid (application-specific)`. Optional app-specific entry. |
| A04 | Coverage checklist of gray checkmark lines inside an informational card | S-I24 | AppleCare only. |
| A05 | Regulatory certification table content and marks | S-I30 | Legally mandated content; structure folded into F006. |
| A06 | Artist rows with circular album art, album count, size | S-I22 | Music storage only; variant of F025. |
| A07 | Wallpaper & style tabbed "Lock screen / Home screen" preview carousel and rows with trailing live-preview glyphs | S-A10, S-A12 | Customization surface; one app screen in two states. |
| A08 | "Standard image / HDR image" comparison card | S-A06 | Feature-specific. |
| A09 | Product copy, brand icons, personal data, Focus icon-color assignments, Emergency SOS and CarPlay illustration content | many | Content, not structure. |

## Uncertain findings

| ID | Candidate | Screenshots | What is missing |
| --- | --- | --- | --- |
| U01 | Family row destination; avatar cluster overflow treatment | S-I01, S-I09 | A tap result; a group with more or fewer members. |
| U02 | Up/down caret row opens an inline menu, a picker, or something else | S-I03 | The activated state. |
| U03 | Passcode sheet entry point and keypad state | S-I42 | The triggering row and the next frame. |
| U04 | Sort control behavior (Subscriptions "Sort", Storage "Size") | S-I07, S-I20 | The opened state. |
| U05 | Drag handles visible before Edit or only after | S-I27 | A pre-Edit capture. |
| U06 | Dependent Time Zone rows when the automatic switch is off | S-I26 | The off state. |
| U07 | External-link arrow always means leaving the stack | S-I44 | A tap result. |
| U08 | Promo and tip card dismissal persistence | S-I08, S-A03, S-A19 | The post-dismiss state. |
| U09 | Gear icon and row body as separate targets | S-A16, S-A18 | The specific tap used to reach S-A18. |
| U10 | Muted "Connect" fill is a disabled state | S-A14 | An enabled-state comparison. |
| U11 | "Advanced options" expanded content | S-A14 | The expanded state. |
| U12 | "Checking device settings…" is a loading state | S-A03 | Motion or a resolved state. |
| U13 | Tinted master toggle recurs beyond HDR | S-A06 | A second tinted instance. |
| U14 | Large in-content title collapses on scroll | S-A07 | A scrolled capture. |
| U15 | Trailing icon in the Internet top bar | S-A16 | Glyph identity and function. |

## Future capture backlog

| Platform | App or workflow | Required state | Claim it would establish |
| --- | --- | --- | --- |
| iOS | Settings, any switch row | Same row toggled to the other state | Footer text changes with state; dependent rows enable (F001, U06). |
| iOS | Settings, Music storage or TV Provider | After tapping "Delete App", "Sign Out", or "Remove Device" | Whether a confirmation alert follows a destructive row (F008). |
| iOS | Settings, Wi-Fi join sheet | Password entered; wrong password | Enabled checkmark treatment and a failure state (F021). |
| iOS | Settings, Screen Time | Row tapped before the passcode sheet; keypad visible | Entry point and implicit commit (F022, U03). |
| iOS | Settings, TV Provider | "Available Apps" after loading | Populated counterpart of the skeleton rows (F019). |
| iOS | Settings, Language & Region | Before tapping Edit; mid-drag | Handle visibility rule and drag feedback (F023, U05). |
| iOS | Settings, Subscriptions and Storage | Sort control opened | Menu versus toggle (F015, U04). |
| iOS | Settings, iCloud+ | Storage near capacity; card after dismiss | Fill color change; dismissal persistence (F018, F011). |
| iOS | Settings, Software Update | Update available | Alternate status composition with an action (F020). |
| iOS | Settings, Appearance | Mid-scroll frame | Blur progression (F013). |
| Android | Settings, Wi-Fi join | Text entered, eye toggled; Advanced options expanded; Connect enabled | Visibility toggle, expander, and disabled-state claims (F030, U10, U11). |
| Android | Settings, Network details | "Forget" tapped | Whether a confirmation follows a destructive icon button (F032). |
| Android | Settings, Internet | An open network row; gear tapped alone | Status-glyph rule; separate targets (F033, U09). |
| Android | Settings, Location and Digital Wellbeing | Master switch off; ring chart with three segments or zero usage; tip card dismissed | Off-state treatment; chart scaling; dismissal (F027, F039, U08). |
| Android | Settings, Safety & emergency | Scrolled | Large-title collapse (F031, U14). |
| Android | Settings, Security & privacy | A failed check; "3 More alerts" expanded | Non-green badge state; count pill result (F037, F035). |
| Android | any detail screen | UI Automator dump | Semantic state for status badges, switches, and master switch cards (F037, F027). |

## Decisions (resolved 2026-09-09)

- **D1 Applicability versus provenance. Resolved.** No heading suffix and no "Settings only" label. The "Applications observed" field records provenance only, for example "Settings, 17 screens". Each new or amended entry gets an "Applicability" line, labeled Inferred, with one of three values. `system control`: the appearance matches a standard platform component (switch, slider, sheet, navigation or top bar, text field, pill button, progress bar, reorder control, detail-disclosure button). `general idiom`: a list, card, header, or data convention used across applications. `settings idiom`: a convention seen mostly in Settings. The values per finding are in `findings-ledger.tsv` (column `applicability`): 15 system control, 23 general idiom, 4 settings idiom (F003, F009, F027, F037). SKILL.md step 4 currently says "keep single-app examples application-specific"; refine it to "keep single-app examples application-specific unless the entry's Applicability line names a system control or a general idiom". Applicability claims stay Inferred; platform documentation is not evidence in the catalog, but step 5 already tells the agent to confirm against current platform documentation, and that applies here too.
- **D2 Evidence import. Resolved.** Import the 47-capture subset. Convert the 20 Android JPEGs to PNG for the runtime and retain the original JPEG bytes under `supporting/native-ui-patterns/research/notes/android/captures-2026-09-08/`. Keep the folder `assets/<platform>/settings/`: folders record the source application by existing convention, and the iOS folder already exists. Name files by state, not by screen title (`switch-dependent-rows.png`, `join-sheet-gated-commit.png`, `skeleton-rows.png`), so route tables read as pattern states. The 13 unselected iOS PNGs stay outside the repository; their SHA256 values go into the research note. The 4 unselected Android JPEGs are retained with the raw set.
- **D3 Word budgets. Resolved.** Keep the `SCENARIOS` limits as they are. They bound the tokens an agent spends per routed scenario. Fit new rows by these rules: one line per state; comparison pairs in one row; merge the existing low-value context rows (for example the three "entry or return context" rows in `references/ios/editing.md` become one row); no 13th route file. Raise a constant only if these rules cannot fit a batch, and record the old and new value in that batch.
- **D4 Validator constants and metadata. Resolved.** Apply in B0 as written: `EXPECTED_SCREENSHOTS`, the heading count, the README mapping table, the SKILL.md capture-metadata paragraph (two capture sets), and second environment sections in `research/limitations.md` and `research/coverage.md`.

- **D5 Personal data in the 2026-09-08 set. Resolved 2026-09-09 (raised at the start of B2).** Outcome: manual redaction by the owner plus scripted boxes on nearby network names; the owner keeps the residual items listed under "Implementation status". Original text of the decision follows. The repository is public. The set comes from a signed-in personal phone. Inventory in `pii/ios-inventory.tsv` and `pii/android-inventory.tsv`. iOS import subset (31): high S-I01, S-I03, S-I04, S-I05, S-I09, S-I12, S-I13, S-I24, S-I28, S-I44; medium S-I07, S-I08, S-I14, S-I15, S-I25, S-I26; low S-I40; none 14. Android raw set (20, all in the working tree since B0): high S-A12, S-A17; medium S-A14, S-A16; low S-A05, S-A18; none 14. B1 already placed S-I05 (3 emails, 2 phone numbers) in the working tree; nothing is committed. Proposed treatment: replace identifier text with placeholders drawn in the system font at the same size, color, and edge (`redact.py`, prototypes `tmp/redact/S-I12.png` and `tmp/redact/S-I01.png`); blur faces inside their circles; keep the redaction specs outside the repository; record each altered capture and its altered fields in `research/notes/captures-2026-09-08.md` with both SHA256 values; remove the raw Android JPEGs from the repository and keep them with the audit. No further import until this is decided.

## Proposed implementation batches

Each batch is independent after B0. Acceptance for every batch: `python3 supporting/native-ui-patterns/check_skill.py` exits 0 (after the `.DS_Store` is removed or ignored), `python3 supporting/native-ui-patterns/test_check_skill.py` exits 0, every new PNG is linked from a same-platform route table row, and every new catalog heading has a README mapping row.

### B0 Evidence import and contract update (prerequisite)

- Findings: none directly; enables all.
- Files: `screenshot-map.tsv` (47 new rows: original path, runtime path, sha256, width, height, bytes); `check_skill.py` (`EXPECTED_SCREENSHOTS`, heading count; `SCENARIOS` unchanged per D3); `test_check_skill.py` (one test for the JPEG-to-PNG conversion record, one for the two-set metadata sentence); `skills/native-ui-patterns/SKILL.md` (metadata paragraph; step 4 refinement per D1); `supporting/native-ui-patterns/docs/README.md` ("How to read the evidence": define the Applicability line and its three values); `research/limitations.md`, `research/coverage.md` (new environment and Settings state rows; generalization boundary updated for the Applicability line); new `research/notes/captures-2026-09-08.md` (ledger, SHA256 of originals, conversion note); `assets/android/.DS_Store` removal.
- File naming: `assets/<platform>/settings/<state>.png`, state named by pattern state, not screen title.
- Import set: iOS S-I01, S-I03, S-I04, S-I05, S-I07, S-I08, S-I09, S-I12, S-I13, S-I14, S-I15, S-I17, S-I19, S-I20, S-I21, S-I22, S-I24, S-I25, S-I26, S-I27, S-I28, S-I32, S-I33, S-I34, S-I35, S-I37, S-I39, S-I40, S-I42, S-I43, S-I44; Android S-A01, S-A02, S-A03, S-A04, S-A06, S-A07, S-A08, S-A11, S-A13, S-A14, S-A15, S-A16, S-A17, S-A18, S-A19, S-A20.
- Benefit: the validator accepts the new evidence and the runtime states its provenance truthfully.
- Acceptance: both commands exit 0; PNG count and byte total match the mapping; no PNG under `supporting/`.

### B1 iOS controls (highest value)

- Findings: F001, F002, F003, F004.
- Catalog: `docs/ios/forms-and-controls.md` (3 new headings; broaden Grouped form rows).
- Runtime: `references/ios/editing.md` (route rows for S-I26, S-I43, S-I35, S-I32/S-I37 pair, S-I05); `SKILL.md` route cell "Switches, filters, and value controls" for iOS changes from "Record a coverage gap" to `references/ios/editing.md`.
- Mapping: S-I26, S-I43, S-I35, S-I32, S-I37, S-I05.
- Benefit: removes the only explicit coverage gap in the routing table.
- Acceptance: `iOS edit form` budget holds or D3 is applied; the route cell no longer says gap.

### B2 iOS row anatomy

- Findings: F005, F006, F024, F025.
- Catalog: `docs/ios/lists-content-feedback.md` (2 new headings; amend Identity-led list row); `docs/ios/forms-and-controls.md` (trailing accessory field).
- Runtime: `references/ios/content-states.md` (S-I40, S-I12, S-I07); `references/ios/accessibility.md` (S-I16); `references/ios/navigation.md` (S-I44).
- Mapping: S-I40, S-I12, S-I07, S-I16, S-I44, S-I01.

### B3 iOS action rows

- Findings: F007, F008.
- Catalog: `docs/ios/forms-and-controls.md` (2 new headings).
- Runtime: `references/ios/editing.md` (S-I27, S-I22 pair; S-I24).
- Mapping: S-I27, S-I22, S-I24, S-I13, S-I28.
- Benefit: first destructive and command row guidance for iOS.

### B4 iOS in-screen cards

- Findings: F009, F010, F011.
- Catalog: `docs/ios/navigation-and-presentation.md` (Feature hero card; remove the aside); `docs/ios/lists-content-feedback.md` (2 new headings).
- Runtime: `references/ios/navigation.md` (S-I14); `references/ios/onboarding-permissions.md` (S-I25 as the persistent alternative); `references/ios/content-states.md` (S-I34, S-I08).
- Mapping: S-I14, S-I25, S-I34, S-I08.

### B5 iOS navigation and headers

- Findings: F012, F013, F014.
- Catalog: `docs/ios/navigation-and-presentation.md` (2 new headings; amend Large-title hierarchy).
- Runtime: `references/ios/navigation.md` (S-I03, S-I12; S-I32/S-I33 pair; S-I27, S-I39).
- Mapping: S-I03, S-I04, S-I09, S-I32, S-I33, S-I39.
- Acceptance: `cross-platform peer navigation` budget holds or D3 is applied.

### B6 iOS list utilities

- Findings: F015, F016, F026.
- Catalog: `docs/ios/lists-content-feedback.md` (2 new headings); `docs/ios/forms-and-controls.md` (search variation).
- Runtime: `references/ios/content-states.md` (S-I07, S-I21); `references/ios/search.md` (S-I21).
- Mapping: S-I21 (shared with B7).

### B7 iOS data summaries and loading states

- Findings: F017, F018, F019, F020.
- Catalog: `docs/ios/lists-content-feedback.md` (3 new headings; amend Centered empty state).
- Runtime: `references/ios/content-states.md` (S-I40, S-I20, S-I28, S-I25, S-I19).
- Mapping: S-I17, S-I20, S-I19, S-I28.
- Research: `coverage.md` "Loading and failures" row for iOS.

### B8 iOS sheets and editing

- Findings: F021, F022, F023.
- Catalog: `docs/ios/navigation-and-presentation.md` (Full-screen task surface variant; Authentication passcode sheet); `docs/ios/forms-and-controls.md` (Content-gated commit control third app); `docs/ios/interactions-and-accessibility.md` (Immediate keyboard focus caveat); `docs/ios/lists-content-feedback.md` (Reorderable list).
- Runtime: `references/ios/editing.md` (S-I14/S-I15 pair; S-I27); `references/ios/onboarding-permissions.md` (S-I42).
- Mapping: S-I15, S-I42.

### B9 Android controls

- Findings: F027, F028, F029, F030.
- Catalog: `docs/android/forms-and-controls.md` (3 new headings; amend Trailing switch).
- Runtime: `references/android/editing.md` (S-A11, S-A20, S-A01, S-A16/S-A14 pair).
- Mapping: S-A11, S-A20, S-A01, S-A06, S-A14, S-A16.

### B10 Android navigation

- Findings: F031, F032, F042.
- Catalog: `docs/android/navigation-and-presentation.md` (2 new headings; amend Search-led top surface); `docs/android/lists-content-feedback.md` (Grouped card list note).
- Runtime: `references/android/navigation.md` (S-A18/S-A07 pair; S-A17 versus existing root).
- Mapping: S-A18, S-A07, S-A17.
- Acceptance: `cross-platform peer navigation` budget.

### B11 Android list anatomy

- Findings: F033, F034, F035, F036.
- Catalog: `docs/android/lists-content-feedback.md` (amend Grouped card list; Recent-items heading; amend Floating primary action); `docs/android/forms-and-controls.md` (Inline pill button).
- Runtime: `references/android/content-states.md` (S-A18, S-A04, S-A15); `references/android/editing.md` (S-A02); `references/android/navigation.md` (S-A16, S-A07).
- Mapping: S-A04, S-A15, S-A02.

### B12 Android cards and framing

- Findings: F037, F038, F041.
- Catalog: `docs/android/lists-content-feedback.md` (2 new headings); `docs/android/navigation-and-presentation.md` (intro paragraph and footnote).
- Runtime: `references/android/content-states.md` (S-A03, S-A06); `references/android/accessibility.md` (S-A03); `references/android/onboarding-permissions.md` cross-reference.
- Mapping: S-A03, S-A13, S-A19.

### B13 Android data summaries

- Findings: F039, F040.
- Catalog: `docs/android/lists-content-feedback.md` (2 new headings, single-capture evidence).
- Runtime: `references/android/content-states.md` (S-A19, S-A08).
- Mapping: S-A08 (S-A19 shared with B12).

### B14 iOS routing corrections from the earlier audit run

- Source: an earlier audit run of the same day (a separate session; its report is archived in `research/audits/2026-09-08-existing-corpus/`) planned these corrections as its B1, applied them, then rolled them back together with its stopped privacy migration. Its corrected copies of the 3 files are not in the working tree; `research/audits/2026-09-08-existing-corpus/b14-routing-corrections.patch` holds exactly the 6 corrected rows and applies to the current tree. Its findings do not come from the 2026-09-08 capture set, so this batch sits outside B0 to B13.
- Claims from that run, Unconfirmed here until the 3 existing assets are reopened: the Settings `search-before-query.png` route is named "Focused search before a query" while the capture shows the bottom field over the root content with no keyboard; the Files "Closed versus open secondary menu" pair compares two different bases and a keyboard tutorial overlay occludes the open state; the "Temporal day content" route uses `day-location-permission.png` while `day-before-event.png` shows the unobscured grid.
- Runtime: `references/ios/search.md` (rename the resting route; add the sentence that the focused-empty state before a query is uncaptured), `references/ios/navigation.md` (Recents or On My iPhone location row; More menu as one obscured state, not a pair), `references/ios/content-states.md` (route `day-before-event.png`). Existing assets only; no import.
- Check: 12 routes, the one-state-or-explicit-pair policy, and the budgets stay unchanged. Text-only requests still skip screenshots.
- Order: after B4.

## Regression checks after any batch

```sh
python3 supporting/native-ui-patterns/check_skill.py
python3 supporting/native-ui-patterns/test_check_skill.py
```

Also confirm by hand: every new route row names one state or an explicit pair; text-only requests still skip screenshots; no runtime file links to `supporting/`.

## Quality gate

- Every file in the owner's screenshot folder has a final status in `screenshot-ledger.tsv` (64 reviewed, 1 skipped non-image).
- Every actionable finding lists at least one new screenshot in Source. Existing assets were opened only for comparison (general.png, root.png ×2, event-empty.png, event-form.png, wallet/location-permission.png, shortcuts/empty-library.png, display-and-touch.png, photos/sign-in-primer.png).
- iOS and Android findings are separate. No cross-platform equivalence is claimed.
- Behavior is marked Unconfirmed everywhere a still image is the only evidence.
- Ledger totals match this report: 31, 6, 5, 8, 9, 15.
- 14 workers covered all 64 images with no overlap.

## Implementation status (2026-09-09)

- B0 applied: `.DS_Store` removed from the runtime, 20 raw Android JPEGs retained under `supporting/native-ui-patterns/research/notes/android/captures-2026-09-08/`, capture note with SHA256 of all 64 originals, SKILL.md metadata paragraph and step 4 refinement, Applicability definition in `docs/README.md`, environment sections in `limitations.md` and `coverage.md`.
- B1 applied: 6 captures imported to `assets/ios/settings/` (switch-dependent-rows, stacked-switches-footers, brightness-slider, appearance-picker, notifications-display-picker, sign-in-security-captions); 3 catalog headings added and Grouped form rows broadened; 5 route rows in `references/ios/editing.md`; SKILL.md iOS value-control cell now routes to iOS editing; validator constants 99 PNGs and 43 headings; 2 regression tests added. Orchestrator removed one unsupported footer-link claim and made the retained-capture count explicit.
- Validation after B1: `check_skill.py` PASS (iOS edit form 1,217 of 1,400 words; cross-platform peer navigation 1,317 of 1,700); `test_check_skill.py` 16 tests OK. Nothing is committed.
- Remaining: B2 to B13 as specified above. B2 (iOS row anatomy) is next.
- B2 stopped before import (2026-09-09): personal data found in the B2 captures and in the already imported S-I05; see D5 and `batches/B2-notes.md`. B2 will use S-I14 in place of S-I16 (S-I16 is outside the D2 subset; S-I14 shows the same info button plus the leading check).
- D5 outcome (2026-09-09): the owner redacted 22 originals by hand in place (solid black boxes, one blur). Verification in `pii/verify-result.tsv`. B1.1 applied: S-I05 re-imported from the redacted file (445,709 bytes), `EXPECTED_SCREENSHOTS = (99, 36_160_063)`, 4 redacted Android JPEGs replaced in the repository, research note table refreshed with a "Manual redaction" section (kinds only), redaction-mark sentences in SKILL.md, `limitations.md`, and Grouped form rows. Validator PASS, 16 tests OK. Residual items left by the owner: third-party network names on S-I14, S-I15, S-A14, S-A16; a relay email on S-I28; a wallpaper sample thumbnail on S-A12; own device names on S-I24, S-I40; a cartoon avatar on S-I44; subscriptions on S-I07; a car name on S-I25; a city on S-I26. S-I14 stayed out of B2 pending the network-name question; its routes move to B4 (hero card) and B8 (join-sheet pair), where the audit already imports it. The Q2 answer on 2026-09-09 was "redact them": the orchestrator boxed the nearby network names on S-I14, S-I15, S-A14, and S-A16 with `redact.py` (backups of the owner's versions in `pii/backup-before-box/`); B1.2 recorded the 4 new hashes, 2 new redaction rows, and replaced the 2 Android copies. Q3 answer: the remaining items stay; the wallpaper thumbnail on S-A12 is a stock Android sample. The owner handles the local WIP commits that predate the redaction (Q1 answer).
- B2 applied (2026-09-09, without S-I14): 5 captures imported (`icon-rows-subtitles`, `label-value-rows`, `app-icon-rows-metadata`, `external-link-rows`, `root-signed-in`); 2 catalog headings added (Icon-led settings row, Label/value information rows), Identity-led list row amended, Trailing accessory field added to Grouped form rows; 4 route rows in `content-states.md`, 1 in `navigation.md`, 1 in `accessibility.md`; `EXPECTED_SCREENSHOTS = (104, 38_983_862)`, 45 headings. Validator PASS (cross-platform 1,376 of 1,700), 16 tests OK. Info-button and leading-check evidence (S-I14) moves to B4.
- B3 applied (2026-09-09): 5 captures imported (`add-row-in-group`, `offload-delete-command-cards`, `link-over-destructive-card`, `destructive-row-centered`, `sign-out-row-footer`); 2 catalog headings (Link-style action row, Destructive action row); D3 merge of the 3 context rows in `references/ios/editing.md` plus 4 new rows; `EXPECTED_SCREENSHOTS = (109, 41_759_068)`, 47 headings. Validator PASS (iOS edit form 1,362 of 1,400), 16 tests OK. B8 must fit its editing rows inside the remaining 38 words or shorten existing cells; raise the constant only as a last resort per D3.
- Archive move (2026-09-09): `audit.md` (this file, scrubbed), `findings-ledger.tsv`, `screenshot-ledger.tsv` (source paths shortened to `captures-2026-09-08/…`), `consolidation-notes.md`, and `redact.py` copied to `supporting/native-ui-patterns/research/audits/2026-09-08/`. The capture note's Provenance section and the archive README point at this directory. B14 added. Nothing is committed.
- S-I28 re-redaction (2026-09-09, by the owner, runtime copy only): a black box now covers the account identifier in the footer of `sign-out-row-footer.png`; the file in the owner's capture folder is unchanged. Recorded in `screenshot-map.tsv`, the capture note (table row, redaction row, totals), and the Destructive action row entry; `EXPECTED_SCREENSHOTS = (109, 41_819_305)` (was `41_759_068`). Three Finder `.DS_Store` files that reappeared under the runtime tree were removed from the working tree; they are tracked in the owner's WIP commit and need `git rm` there.
- Consolidation outside the repository (2026-09-09): the 15 pending iOS originals were copied, hash-verified, into `research/notes/ios/captures-2026-09-08/`; the validator now allows supporting PNGs only there and rejects a duplicate of a runtime PNG. The 16 imported iOS files matched the runtime copies (S-I28 differs only by the owner's later box) and the 20 Android files matched the retained JPEGs. The owner's capture folder (64 files), the private audit directory (worker reports, batch specs, personal-data inventory, scratch images), and the earlier run's directory (byte copies of runtime assets, harness, rollback state) were then deleted. The earlier run's report and the B14 patch were kept under `research/audits/2026-09-08-existing-corpus/`. Every batch from B4 on sources its iOS captures from the pending folder and moves them.
