# Native UI patterns audit

## Recommendation

Correct existing evidence claims and exact-state routing before expanding the catalog. The strongest immediate changes are F1, F2, F4 and F5: distinguish resting from focused Settings search, stop treating different Files locations as a controlled menu comparison, acknowledge the logged Contacts discard path without inventing its prompt appearance, and use the already-retained unobscured Calendar day.

All 157 screenshots were visually inspected. The package is not publication-ready: 21 existing assets require sanitisation under this audit, and the baseline checker fails on an unexpected Finder metadata file. Neither issue was repaired. No repository file, source image, XML dump, mapping, validator or test was changed, and no sanitised derivative was created.

New control coverage is potentially useful, particularly the bounded slider/switch and preview-selection candidates F10–F12. Importing the entire additional collection is not justified. Most additional images repeat Settings containers, and sensitive dashboards or incomplete states should remain deferred.

## Scope and evidence rules

[Observed] This audit covers the runtime skill, all twelve operation references, all eight supporting catalogs and their forty canonical sections, supporting index/comparison/coverage/limitations/uncertain findings, original-pattern and screenshot mappings, validator/tests, both application inventories and observation/error-feedback logs, Android unavailable-app notes and all 57 matching Android XML dumps. The additional screenshot directory was inventoried recursively, including non-image metadata files.

[Observed] Processing was explicitly authorised for this Pi session and OpenAI Codex-backed native subagents. Two disjoint native workers reviewed iOS and Android, with no child fan-out. Their receipts and successful image-tool results corroborate 80 and 77 visual inspections respectively, with no failed or blocked screenshot opens. The primary reopened representative and disputed images, checked exact catalog sections and local logs, and reconciled the worker proposals. Filenames, metadata and XML corroborated observations, never substituted for opening an image.

[Observed] Runtime sources retain their mapped simulator/emulator provenance: iOS 27.0 build 24A5423a on the recorded iPhone 17 Pro simulator, and Android 17/API 37 on the recorded signed-out emulator. Additional images are visually identifiable as Settings interfaces. Their folder names did not supply version evidence. Only E032 and E039 visibly state iOS 27.0. The other 62 additional images have unknown OS versions. No adjacent screenshot inherits the device, build or application version from those two images.

[Observed] means directly visible pixels or a specifically cited local action/semantic record. [Inferred] means a proposed design adaptation or reuse judgment. [Unconfirmed] means the evidence does not establish the claim. Stills cannot establish gestures, transitions, dismissal outcomes, persistence, hidden states, accessibility focus or speech, platform APIs, or effective touch targets. Exact Android XML can establish particular exposed node properties, not complete accessibility. Local iOS automation logs establish only the labels, states and actions they actually record.

[Inferred] All additional recurrence is within Settings unless explicitly stated otherwise. A useful application-specific example can be admitted with that limit. One app, familiar appearance or a filename does not establish a platform-wide convention. Raster dimensions describe the files, not points, dp or proven physical target sizes.

## Baseline and preserved contract

| Check | Observed baseline |
| --- | --- |
| Runtime organisation | Six operations per platform, twelve references, one entry point |
| Supporting canonical sections | 40 total: 17 iOS, 23 Android |
| Mapped original PNGs | 93 total: 36 iOS, 57 Android |
| Original PNG bytes | 33,473,851 |
| Android XML dumps | 57, all matched through historical mapping |
| XML bytes | 1,134,708 |
| Additional screenshots | 64: 44 iOS PNGs, 20 Android JPEGs |
| Total images / distinct hashes | 157 / 157 |
| Supporting PNG copies | 0 |
| Mapping mismatches | 0 across paths, hashes, dimensions and bytes |
| Image dimensions | Existing iOS 1206×2622, Android 1280×2856. Additional iOS 1206×2622, Android 1000×2244 |
| Baseline git state | Tracked/untracked status clean, diff empty. Ignored metadata files still exist |

The exact pre-audit commands ran from the repository root with `PYTHONDONTWRITEBYTECODE=1`:

```text
python3 supporting/native-ui-patterns/check_skill.py
exit 1: unexpected runtime path: assets/android/.DS_Store

python3 supporting/native-ui-patterns/test_check_skill.py
exit 0: 14 tests passed
```

[Observed] The first command stops at the unexpected runtime path. It is not a clean package-validation pass, and the later checks were not proved by that command. Separate inventory and link/contract inspection supplies the bounded structural evidence in this report. The ignored file was preserved rather than silently removed. Baseline stdout/stderr and git receipts are under `baseline/`.

| Representative read | Current words | Existing limit |
| --- | ---: | ---: |
| iOS editing: entry point plus operation | 991 | 1,400 |
| Android no-results search: entry point plus operation | 1,026 | 1,300 |
| Cross-platform peer navigation: entry point plus two operations | 1,260 | 1,700 |

[Inferred] No budget increase is justified. Put detailed anatomy in supporting catalogs. Runtime guidance should retain short decision cues and exact visual routes. Text-only behavioural requests must skip images. Visual requests must open one named state or an explicit comparison pair, not automatically load entry, interaction and reset sequences.

[Observed] The validator fixes runtime file membership/frontmatter/routes, original image counts/bytes/hashes/dimensions, the forty canonical headings and their mapping, XML counts/bytes, local link/anchor closure, platform-correct reachability, dependency direction and representative read budgets. Supporting may depend on runtime. Runtime must not depend on supporting research or this private audit.

[Inferred] Text corrections can leave these structural contracts intact. New canonical headings or imported/redacted assets require deliberate inventory and validator/test migration. Do not rename a historical heading or change an image hash merely to make a check pass. Preserve the immutable original inventory separately from the approved current distributable inventory. No preservation, routing, link, platform or read-budget safeguard should be disabled.


### Audit tooling limits

Both native workers completed their assigned image reviews. A supplemental steering attempt was not delivered: `Workflow 22554952-25b1-4963-b301-5bbf199f89f6 has no live foreground child.` The primary therefore reconciled those supplemental observations directly in this report rather than treating them as worker-reviewed. A non-image read initially targeted a nonexistent root docs/README path, and a later compressed-read call refused a private Desktop path outside its project root. The actual supporting document and private artifact were read through the authorised local read tool. No screenshot inspection was failed or blocked, and no provider, external CLI fallback or publication channel was substituted.

## Ledger and review accounting

`evidence-ledger.json` is the authoritative private image ledger. Each screenshot has a stable ID, current source path, original mapped path when available, SHA-256, byte count, format, raster dimensions, platform/app/version basis, provenance, owner, visual-inspection note/status, sensitive-region categories, metadata review, privacy disposition and final finding links. Exact additional source paths remain in that private ledger. The report uses screenshot IDs instead of personal values or identifying source names.

`findings.json` contains the structured consolidated findings rendered below. `visual-tool-verification.json` records the worker image-tool coverage. `metadata-audit.json`, `nonimage-metadata-ledger.json`, `structural-audit.json` and `inventory-checks.json` preserve supporting checks. Worker source findings, notes and receipts remain under `workers/`. Consolidated findings supersede worker drafts where they disagree.

| Corpus | Visually reviewed | Failed | Blocked | Safe for reuse | Requires sanitisation | Excluded | Unresolved |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Existing iOS | 36 | 0 | 0 | 24 | 12 | 0 | 0 |
| Existing Android | 57 | 0 | 0 | 48 | 9 | 0 | 0 |
| Additional iOS | 44 | 0 | 0 | 0 | 44 | 0 | 0 |
| Additional Android | 20 | 0 | 0 | 7 | 8 | 5 | 0 |
| Total | 157 | 0 | 0 | 79 | 73 | 5 | 0 |

Sanitised derivatives: 0. Safe-for-reuse is a technical pixel/metadata privacy judgment, not publication-rights clearance or permission to import an asset. Unknown rights/provenance remain separate admission questions. Excluded images were inspected and remain untouched at their source paths, not deleted. The 14 inventoried Finder metadata files are separate non-image records with unresolved privacy disposition, not additional screenshots.

[Observed] The primary corrected two worker-level issues: the iOS worker left additional `platform` fields unknown despite explicitly recording a visually confirmed iPhone interface, and E008 storage telemetry was too permissively marked safe. The final ledger uses visually supported platform labels, keeps OS-version limits, and marks E008 requires-sanitization. The primary also corrected the resting-search description, counted six visible audio sliders in E001 rather than the worker draft's four, and rejected any keypad/slot inference from E062's blank entry region.

## Taxonomy and integration decisions

1. D1. Preserve the operation-first runtime. Neither Settings breadth nor control additions warrant a seventh operation, per-app runtime files or an expanded entry point.
2. D2. Keep purpose and component anatomy distinct. Task presentation and grouped inputs, map sheet bounds and the exercised drag, visual checked styling and XML state remain separate evidence layers. F6 and F7 retain existing umbrella headings but name non-equivalent presentations beneath them.
3. D3. New mechanisms require a real gap. Continuous adjustment and preview-led choice qualify as bounded candidates. Repeated grouped cards and alternate switch glyphs belong to existing patterns. F9 is a missing detailed catalog counterpart to an already-routed state, not a new runtime feature.
4. D4. Preserve state distinctions without multiplying canonicals. Empty versus unmatched-query causes, original versus later discard attempts and lower versus expanded map positions remain explicit. No byte-identical duplicates exist, but visual overlap is not a reason to delete historical sequence evidence.
5. D5. Defer uncertain or privacy-destroyed evidence. Placeholder rows do not establish a loading lifecycle, a blank credential task does not establish a keypad, and four unrelated sensitive dashboards do not become one pattern by sharing a page shape.

## Privacy and publication blockers

1. R1. Existing package blockers: R014, R019, R020, R022, R034, R042, R043, R044, R056, R063, R065–R070 and R076–R080. Their categories include contact/form inputs, recipient identifiers, message/calendar content, and faces in editorial/promotional imagery. Some local logs identify deliberately temporary test tokens. Their conservative redaction disposition is not a claim that those tokens are real identities. Sample-looking content alone was not accepted as clearance.
2. R2. Additional material includes account/profile identities, family/child information, addresses and payment/subscription context, network identifiers and an exposed network credential, device/serial/agreement identifiers, paired vehicles/accessories, and activity/location/health/security information. E038's credential must never enter a public example. E003, E007, E011 and E019 are excluded because their sensitive domain content is central to the evidence. E012 is excluded for its personal preview/child-face content. Values are intentionally absent from this narrative.
3. R3. All 44 additional iOS PNGs retain capture-time/UserComment/XMP-related metadata categories requiring sanitisation. Original PNG metadata appears limited to colour/dimension-related fields in the bounded inspection. One additional Android JPEG has auxiliary HDR/multipicture data. That is not itself proof of personal metadata, but public exports should not retain unreviewed auxiliary payloads or hidden thumbnails. No GPS field detected is not equivalent to privacy clearance.
4. R4. Related text can reproduce what pixel redaction removes. Preserve original XML, logs and raw inventory privately, and review text nodes, attributes, paths, device identifiers and diagnostic metadata before distribution. Public summaries should cite safe source IDs and non-sensitive semantic facts. Do not rewrite historical observation logs in place or publish the private audit/harness, which contains original evidence and sensitive paths.
5. R5. The 14 Finder cache files require a deliberate packaging disposition. The currently reported cache causes validation failure. The broader inventory includes caches outside the runtime too, but none was removed. A future approved cleanup should preserve private evidence where needed and exclude unexpected artifacts from the distribution, not weaken the runtime allowlist.

### Proposed sanitisation procedure, not executed

1. A1. Preserve byte-identical originals privately with restricted access, hashes and provenance. Resolve reuse rights and name the exact approved source IDs before any derivative work. Preserve historical mapping independently of distributable asset membership.
2. A2. Create a separate derivative only for a demonstrated catalog need. Use opaque neutral masks over identities, faces, addresses, identifiers, credentials, private content and sensitive quantitative context. Do not use blur, pixelation, translucent overlays, editable layers or invented replacement values. If masks destroy the relevant anatomy, exclude the image and request a controlled safe recapture.
3. A3. Flatten to a fresh raster, strip EXIF/XMP/text comments, timestamps, thumbnails and unnecessary auxiliary payloads, and use a neutral filename. Keep only necessary colour-management information after inspection. Reopen the exported bytes and verify masks, edges, readability, metadata and lack of recoverable original layers or previews.
4. A4. Record source ID/hash, derivative ID/path/hash, dimensions, byte count, exact redacted categories/regions, metadata disposition, tool/process, reviewer and approval date in a separate provenance manifest. Do not overwrite the source hash with the derivative hash or silently redirect an original mapping row.
5. A5. Admit only verified derivatives through an exact distributable manifest. Keep private-original preservation evidence separate from portable validation of public assets. Check mapping/link closure, platform routing, required pattern coverage and conditional image loading. Removing an image from the current package does not remove prior git history. Assess historical exposure separately if the package has already been distributed, with no history rewriting authorised by this audit.

## Prioritised findings

The index below is followed by complete records. Each record identifies current coverage, concrete catalog-field wording, exact screenshot IDs/regions, the separate nonvisual evidence when available, integration, confidence and privacy/priority. Screenshot paths resolve through `evidence-ledger.json` by ID. Proposed wording is not installed documentation.
Consolidated candidates: 10 existing-pattern-improvement, 3 new-pattern, 4 uncertain, 3 existing-pattern-variation, 2 application-specific, 1 duplicate. Counts refer to findings, not independent platform observations.

| ID | Finding | Classification | Priority / disposition |
| --- | --- | --- | --- |
| F1 | Correct the Settings pre-query visual route | existing-pattern-improvement | high / proposed |
| F2 | Separate Files location context from the open Browse menu | existing-pattern-improvement | high / proposed |
| F3 | Describe task bounds and grouped form anatomy precisely | existing-pattern-improvement | high / proposed |
| F4 | Bound the recorded iOS dirty-dismiss path correctly | existing-pattern-improvement | high / proposed |
| F5 | Use the unobscured Calendar day as the temporal canonical | existing-pattern-improvement | high / proposed |
| F6 | Give command panels and account sheets separate anatomy | existing-pattern-improvement | high / proposed |
| F7 | Separate modal sign-in, permission primer sheet and account wall | existing-pattern-improvement | high / proposed |
| F8 | Update the Android discard-confirmation evidence to both passes | existing-pattern-improvement | high / proposed |
| F9 | Document the already-routed single-field folder dialog | existing-pattern-improvement | medium / proposed |
| F10 | Labeled continuous-value cards in Pixel Settings | new-pattern | medium / proposed |
| F11 | Slider and switch mechanisms in iOS Settings | new-pattern | medium / proposed |
| F12 | Preview-led appearance choice | new-pattern | medium / proposed |
| F13 | Credential-task appearance without visible input mechanism | uncertain | defer / defer |
| F14 | Clarify trailing-switch glyph and split-row variation | existing-pattern-variation | medium / proposed |
| F15 | Dark-theme grouped Settings cards across detail pages | existing-pattern-variation | low / proposed |
| F16 | Deepen shared iOS grouped row grammar | existing-pattern-variation | medium / proposed |
| F17 | Consequence-labeled offload versus deletion actions | application-specific | low / optional |
| F18 | Storage capacity breakdown dashboard | application-specific | defer / defer |
| F19 | Placeholder rows are not a proven loading lifecycle | uncertain | defer / defer |
| F20 | Privacy-limited dashboard candidates remain separate | uncertain | defer / defer |
| F21 | Positive validation, gesture and accessibility gaps remain gaps | uncertain | defer / defer |
| F22 | Do not multiply iOS empty/search-empty canonicals | duplicate | low / no-addition |
| F23 | Do not promise search remains visible in the expanded map sheet | existing-pattern-improvement | medium / proposed |

<a id="f1"></a>

### F1. Correct the Settings pre-query visual route

Identity: ios · existing-pattern-improvement · Input control / Search. Proposed operation: search.

Scope and purpose: [Observed] Existing Settings resting, queried and cleared captures. [Inferred] An exact-state route prevents a designer from copying resting geometry for focused input.

Current coverage:
- Catalog: `supporting/native-ui-patterns/docs/ios/forms-and-controls.md#search-field-with-dictation-affordance`, `supporting/native-ui-patterns/docs/ios/lists-content-feedback.md#centered-empty-state`.
- Runtime: `skills/native-ui-patterns/references/ios/search.md`.
- Gap: The row Focused search before a query points to R089, which shows the resting root, bottom field and no keyboard. The log explicitly calls this idle. This is a routing error, not a missing search pattern.

Proposed catalog-field wording:
- Description: [Observed] Settings resting search is a bottom rounded field over the category list. The retained focused queried state moves the field above the keyboard, with a separate circular exit control to its right.
- Visual structure: [Observed] R089 has a large left-aligned title and inset white row groups above the bottom magnifier/placeholder/microphone field. R090 replaces the list with a centred symbol/title/helper cluster and retains the query and clear control above the keyboard.
- Interaction: [Observed] The error-feedback pass entered an unmatched query and cleared it back to the list. [Unconfirmed] A focused-empty-before-query screenshot was not retained.
- States: [Observed] Resting before query, focused zero results, restored after clear. Do not relabel resting as focused.
- Variations: [Observed] Keep zero results under Centered empty state, not a new error pattern.
- Design guidance: [Inferred] Select the exact captured state. Do not invent a focused-empty visual specification from the idle image.

Visual evidence, with paths in the private ledger:
- R089: Full screen: resting bottom field, no caret/keyboard.
- R090: Lower field/keyboard and central no-results content establish focused queried anatomy.
- R088: Restored root state after clearing, not a focused-empty substitute.

Behavioural or semantic evidence:
- `supporting/native-ui-patterns/research/notes/ios/error-feedback-pass.md`, Settings — unmatched search query: The Before item says root and idle Search. During and After record query entry and clearing.

Integration:
- Catalog: Clarify resting versus focused evidence in the existing search entry.
- Runtime: Rename the R089 row to Resting Settings before query entry. Route focused queried/no-results questions to R090. Explicitly record focused-empty as uncaptured.
- Index mapping: No heading, index, mapping, image or route-count change.

Confidence: high. Primary reopened all three relevant states and checked the explicit log description.

Privacy: Cited captures currently safe-for-reuse under this audit.

Priority: high. Improves existing evidence accuracy or explanatory depth. Inspected sample only. 3 cited images, not independent observations or platform prevalence.

<a id="f2"></a>

### F2. Separate Files location context from the open Browse menu

Identity: ios · existing-pattern-improvement · Navigation / anchored menu. Proposed operation: navigation.

Scope and purpose: [Observed] Files On My iPhone and Browse-root menu captures. [Inferred] State identity and occlusion must be accurate before using a visual comparison.

Current coverage:
- Catalog: `supporting/native-ui-patterns/docs/ios/navigation-and-presentation.md#large-title-hierarchy`, `supporting/native-ui-patterns/docs/ios/interactions-and-accessibility.md#anchored-overflow-menu-application-specific`.
- Runtime: `skills/native-ui-patterns/references/ios/navigation.md`, `skills/native-ui-patterns/references/ios/search.md`.
- Gap: R071 is the On My iPhone location. R072 is the Browse root with a menu and a separate keyboard tutorial sheet. The current closed-versus-open pair is not a same-base controlled comparison, and the large-title entry cites R071 for a Browse-root title it does not show.

Proposed catalog-field wording:
- Description: [Observed] Files shows a compact centred On My iPhone title in the empty location. The separate Browse-root capture shows a large left-aligned title and an upper-trailing rounded command panel.
- Visual structure: [Observed] R071 has paired back/forward controls, centred location title, a search row, centred empty symbol/title, and a detached peer dock. R072 has a two-row panel over the top-trailing Browse area, Locations/Tags groups below, and an unrelated tutorial sheet covering the lower screen. The invoker is obscured by the open panel.
- Interaction: [Observed] The original log records label-based Browse/More activation. [Unconfirmed] The two retained images do not establish an unchanged base screen across that activation.
- States: [Observed] Empty location and open Browse-root menu are separate captured contexts.
- Variations: [Observed] Large root title versus compact location title is a hierarchy variation, not evidence of a new peer component.
- Design guidance: [Inferred] Use R072 alone for open-menu anatomy and R071 for location anatomy. Request a clean Browse-root before/open pair if invoker alignment or transition continuity matters.

Visual evidence, with paths in the private ledger:
- R071: Compact location title, empty state and selected Browse dock.
- R072: Open panel and Browse root, with invoker/lower UI obscured by overlays.

Behavioural or semantic evidence:
- `supporting/native-ui-patterns/research/notes/ios/direct-observation-log.md`, Automation results: Successful label-based Files Browse and More actions are recorded, without a clean same-root before/open pair.

Integration:
- Catalog: Correct evidence labels and attach the Browse-root description to R072 with its occlusion caveat. Retain historical filenames.
- Runtime: Replace Closed versus open secondary menu with Open Browse-root menu → R072. Label R071 On My iPhone location. Keep a same-root comparison as a capture gap.
- Index mapping: No heading or mapping change. Do not rename an original merely to improve its label.

Confidence: high. Primary visually compared both images and the existing claims.

Privacy: Both captures safe-for-reuse, but R072 is visually occluded, not clean canonical transition evidence.

Priority: high. Improves existing evidence accuracy or explanatory depth. Inspected sample only. 2 cited images, not independent observations or platform prevalence.

<a id="f3"></a>

### F3. Describe task bounds and grouped form anatomy precisely

Identity: ios · existing-pattern-improvement · Presentation / grouped forms. Proposed operation: editing.

Scope and purpose: [Observed] Calendar creation and Contacts editing in the mapped simulator. [Inferred] Preserve the focused-task pattern without implying both surfaces have identical geometry.

Current coverage:
- Catalog: `supporting/native-ui-patterns/docs/ios/navigation-and-presentation.md#full-screen-task-surface`, `supporting/native-ui-patterns/docs/ios/forms-and-controls.md#grouped-form-rows`.
- Runtime: `skills/native-ui-patterns/references/ios/editing.md`.
- Gap: Full-screen is too geometrically absolute for Calendar, whose rounded task surface begins below a dimmed status strip. Current grouped-row anatomy omits the Calendar accent, distinct field groups and major contrast with the Contacts profile/form structure.

Proposed catalog-field wording:
- Description: [Observed] Calendar and Contacts isolate editing in dedicated task surfaces with leading dismissal and trailing checkmark controls. Calendar has a rounded top boundary below dimmed background. Contacts presents profile identity above a longer grouped form.
- Visual structure: [Observed] Calendar centres an Event/Reminder selector between circular top actions. A blue vertical accent spans the leading side of the separate title and date/time cards. Section labels introduce Location and Options, with icons and trailing values inside white rounded groups. The keyboard obscures lower options. Contacts instead places a large centred identity badge and photo action above name, phone and email groups, with inset dividers and aligned add/remove affordances.
- Interaction: [Observed] Original XCTest actions opened the two tasks. The later error pass entered and discarded temporary text. [Unconfirmed] Save outcomes and sheet-drag dismissal were not tested.
- States: [Observed] Empty focused Calendar, populated Calendar and existing-value Contacts. Visible control muting alone is not a semantic disabled claim.
- Variations: [Observed] Keep task presentation and grouped input anatomy as different evidence layers. Do not merge their canonical sections.
- Design guidance: [Inferred] Keep dismissal and commit separated, align input groups, and validate keyboard occlusion in the target viewport. Do not infer full-screen APIs from these pixels.

Visual evidence, with paths in the private ledger:
- R062: Calendar task top bounds, selector, accent, groups and keyboard.
- R069: Contacts top actions, identity header and repeatable grouped fields.

Behavioural or semantic evidence:
- `supporting/native-ui-patterns/research/notes/ios/direct-observation-log.md`, Automation results: Calendar Add and Contacts Edit activations succeeded.
- `supporting/native-ui-patterns/research/notes/ios/error-feedback-pass.md`, Calendar — new event title gating; Contacts — invalid email entry: Later temporary input and discard occurred. Qualify original-pass-only Notes instead of claiming no text was ever entered.

Integration:
- Catalog: Keep the historical Full-screen task surface heading for this small batch, but make Description explicitly a dedicated task with application-specific bounds. Add the detailed anatomy to existing Visual structure fields.
- Runtime: Add only a brief rounded-task versus profile-form distinction if useful. Existing image routes remain.
- Index mapping: No heading rename/count or image changes. A later rename would require deliberate original-mapping/anchor migration.

Confidence: high. Primary reopened Calendar and Contacts originals and checked both observation passes.

Privacy: R069 contains contact identities and values. Publication blocked until approved sanitisation/recapture. Text-only correction can proceed without publishing new evidence.

Priority: high. Improves existing evidence accuracy or explanatory depth. Inspected sample only. 2 cited images, not independent observations or platform prevalence.

<a id="f4"></a>

### F4. Bound the recorded iOS dirty-dismiss path correctly

Identity: ios · existing-pattern-improvement · Editing cancellation. Proposed operation: editing.

Scope and purpose: [Observed] Contacts temporary-email edit/discard path. [Inferred] Separate known cancellation behaviour from the uncaptured appearance of its prompt.

Current coverage:
- Catalog: `supporting/native-ui-patterns/docs/ios/forms-and-controls.md#add-and-remove-rows-application-specific`, `supporting/native-ui-patterns/docs/ios/navigation-and-presentation.md#full-screen-task-surface`.
- Runtime: `skills/native-ui-patterns/references/ios/editing.md`.
- Research: `supporting/native-ui-patterns/research/coverage.md#state-coverage-across-the-runs`, `supporting/native-ui-patterns/research/limitations.md#missing-interaction-and-content-states`.
- Gap: Runtime calls iOS dirty-dismiss confirmation Unconfirmed and coverage says no confirmation was reached. The error-feedback log explicitly records close → Discard Changes → restored detail. Appearance is uncaptured, not the entire discard path.

Proposed catalog-field wording:
- Description: [Observed] The Contacts error-feedback pass abandoned temporary edits through close and Discard Changes, returning to the prior detail.
- Visual structure: [Unconfirmed] No retained screenshot shows the intervening discard prompt, its bounds or its actions. The form and returned detail do not substitute for that image.
- Interaction: [Observed] The log records Discard Changes activation and removal of the temporary row without persisting the edit.
- States: [Observed] Modified form and restored detail retained. [Unconfirmed] Prompt appearance, alternate actions and gesture dismissal.
- Variations: [Unconfirmed] No broader iOS dirty-dismiss convention established.
- Design guidance: [Inferred] Preserve a non-committing exit. Use target-product testing or a new safe capture when the confirmation UI itself is needed.

Visual evidence, with paths in the private ledger:
- R070: Modified Contacts form, not the discard prompt.
- R067: Returned detail corroborates the logged exit outcome, not the intermediate dialog anatomy.

Behavioural or semantic evidence:
- `supporting/native-ui-patterns/research/notes/ios/error-feedback-pass.md`, Contacts — invalid email entry: Attempted path and After explicitly record close → Discard Changes → restored detail.

Integration:
- Catalog: Qualify original-pass Notes and current research summaries. Preserve raw logs unchanged.
- Runtime: Replace blanket dirty-dismiss Unconfirmed with recorded Contacts discard path and uncaptured prompt appearance. Do not add a visual route to a nonexistent prompt.
- Index mapping: No canonical heading, index, mapping or asset changes.

Confidence: high. The raw local log is explicit. The stronger visual-dialog claim remains Unconfirmed.

Privacy: Contact form/detail assets require sanitisation before reuse. No raw personal values belong in replacement wording.

Priority: high. Improves existing evidence accuracy or explanatory depth. Inspected sample only. 2 cited images, not independent observations or platform prevalence.

<a id="f5"></a>

### F5. Use the unobscured Calendar day as the temporal canonical

Identity: ios · existing-pattern-improvement · Temporal content. Proposed operation: content-states.

Scope and purpose: [Observed] Calendar has unobscured day captures in the error pass as well as a permission-covered day. [Inferred] A clean canonical better guides temporal layout without loading extra context.

Current coverage:
- Catalog: `supporting/native-ui-patterns/docs/ios/lists-content-feedback.md#time-grid-day-view-application-specific`.
- Runtime: `skills/native-ui-patterns/references/ios/content-states.md`.
- Gap: The temporal route currently chooses R060 with a central permission alert even though R059 already shows the full grid. This is evidence selection, not a new calendar pattern.

Proposed catalog-field wording:
- Description: [Observed] The day view places navigation controls above a weekday/date strip, a centred day heading, and an hourly content grid.
- Visual structure: [Observed] A leading month/back capsule faces a trailing command capsule. The selected day uses a red filled circle. Hour labels align along the leading edge of horizontal rules. A red current-time line carries a small filled time label. Bottom Today and view/inbox controls float in separate groups.
- Interaction: [Observed] Add opened the event task and discard returned to the day in the error pass.
- States: [Observed] Unobscured empty day and permission-covered day. [Unconfirmed] Populated events, multi-day/month variants and drag editing.
- Variations: [Observed] Keep the permission-covered frame for consent-context questions, not as the default temporal overview.
- Design guidance: [Inferred] Open R059 alone for day-grid anatomy. Extra entry/return frames are only for an explicit context comparison.

Visual evidence, with paths in the private ledger:
- R059: Unobscured date strip, grid, time rule and bottom commands.
- R060: Permission overlay demonstrates consent context and its occlusion, not the clean grid.

Behavioural or semantic evidence:
- `supporting/native-ui-patterns/research/notes/ios/error-feedback-pass.md`, Calendar — new event title gating: Before and After day views surround the non-committing form path.

Integration:
- Catalog: Add R059 as the primary day-view evidence link without duplicating the stored image.
- Runtime: Route Temporal day content to R059. Keep R060 reachable through onboarding/permissions.
- Index mapping: No files, images, original mapping or heading changes.

Confidence: high. Both variants exist and the primary reopened the unobscured original.

Privacy: No sensitive calendar event content is visible in R059.

Priority: high. Improves existing evidence accuracy or explanatory depth. Inspected sample only. 2 cited images, not independent observations or platform prevalence.

<a id="f6"></a>

### F6. Give command panels and account sheets separate anatomy

Identity: android · existing-pattern-improvement · Secondary navigation / overlays. Proposed operation: navigation.

Scope and purpose: [Observed] Chrome overflow and Messages account surface. [Inferred] Shared secondary-action purpose is insufficient design guidance when coverage and containers differ.

Current coverage:
- Catalog: `supporting/native-ui-patterns/docs/android/navigation-and-presentation.md#contextual-overlay-menu`.
- Runtime: `skills/native-ui-patterns/references/android/navigation.md`.
- Gap: The current umbrella is valid as a purpose grouping but its compact description flattens an anchored partial-width command panel and a near-full-height account surface. Runtime already separates the two visual routes.

Proposed catalog-field wording:
- Description: [Observed] The sample contains two distinct secondary-action presentations: an upper-trailing Chrome command panel and a near-full-height Messages account/utility surface.
- Visual structure: [Observed] Chrome leaves a substantial leading strip of the page exposed. Its rounded shadowed panel begins with circular quick actions, then a visually emphasised update row and icon/label commands separated into groups. Messages covers almost all application content, placing centred account branding and Sign in above a divider, an upper-trailing close icon, and inset rounded groups of utility rows with a quiet footer. The underlying list is not visibly retained within the sheet frame.
- Interaction: [Observed] Local records support opening the account/overflow surfaces and non-committing Back dismissal. [Unconfirmed] Item outcomes, sheet drag and animation.
- States: [Observed] Closed/open states exist. Inspect one exact state unless the request compares them.
- Variations: [Observed] Name these Anchored command panel and Account utility sheet. They are not equivalent components and should not be merged with the map-content sheet.
- Design guidance: [Inferred] Choose partial-context command access versus a larger account utility surface according to the task. Shared secondary purpose does not prescribe common geometry.

Visual evidence, with paths in the private ledger:
- R005: Chrome partial-width panel, quick-action row, dividers and exposed page context.
- R037: Messages account header, close action, grouped utility rows, almost complete base coverage.

Behavioural or semantic evidence:
- `supporting/native-ui-patterns/research/notes/android/direct-observation-log.md`, Observations by app > Chrome; Messages: Records opened overlay contents.
- `supporting/native-ui-patterns/docs/android/interactions-and-accessibility.md`, System Back as non-committing exit: Curated evidence records Messages account-sheet dismissal with Back.

Integration:
- Catalog: Keep Contextual overlay menu as the original canonical heading, but add named Variations or ### subheads with separate anatomy. Do not add two competing top-level patterns in this batch.
- Runtime: No new route needed. Existing Chrome and Messages rows already preserve the distinction.
- Index mapping: No mapping/count changes. Comparison may link the same umbrella while naming the two presentations.

Confidence: high. Primary reopened the exact captures. The visual distinction is direct.

Privacy: Both currently safe-for-reuse. Visible editorial page content in Chrome is not evidence of personal browsing history.

Priority: high. Improves existing evidence accuracy or explanatory depth. Inspected sample only. 2 cited images, not independent observations or platform prevalence.

<a id="f7"></a>

### F7. Separate modal sign-in, permission primer sheet and account wall

Identity: android · existing-pattern-improvement · Onboarding and blocked-state feedback. Proposed operation: onboarding-permissions.

Scope and purpose: [Observed] Photos sign-in card, Maps audio primer and Play Store account-required landing. [Inferred] Designers need the actual blocking relationship and action hierarchy, not an interchangeable primer label.

Current coverage:
- Catalog: `supporting/native-ui-patterns/docs/android/lists-content-feedback.md#sign-in-or-permission-primer`, `supporting/native-ui-patterns/docs/android/interactions-and-accessibility.md#permission-prompt-boundary`.
- Runtime: `skills/native-ui-patterns/references/android/onboarding-permissions.md`.
- Gap: The umbrella conflates presentation and progression boundaries. In particular, the Maps audio primer is a tall bottom sheet over a dimmed map, not simply another full-page sign-in screen.

Proposed catalog-field wording:
- Description: [Observed] Keep account requirement, optional capability explanation, and system permission decision distinct. The inspected account and primer surfaces use different bounds and actions.
- Visual structure: [Observed] Photos centres a broad rounded white card within a uniform scrim over the peer shell. Heading, illustration, explanatory copy and compact Sign in button form a centred stack. Maps places a full-width, rounded-top sheet below visible dimmed map/search context, with left-aligned heading/copy, centred illustration, a wide filled Continue action and quieter Not now beneath it. Play Store uses an undimmed full-page logo/name/copy stack and one visible Sign in progression action.
- Interaction: [Observed] Maps Not now deferred the request. Play Store and Photos sign-in were not selected. [Unconfirmed] Post-grant/signed-in outcomes and platform APIs.
- States: [Observed] Primer/required-account appearances only. Contacts system permission dialog remains a different evidence layer.
- Variations: [Observed] Name modal account primer, contextual capability-primer sheet and account-required landing. Keep them under the current umbrella with independent descriptions.
- Design guidance: [Inferred] Show whether context remains available and whether deferral is offered. Do not describe a system-consent dialog as the same UI as an app primer.

Visual evidence, with paths in the private ledger:
- R048: Centred account card over dimmed Photos shell.
- R032: Tall bottom primer sheet, dimmed map context and asymmetric continuation/deferral emphasis.
- R049: Undimmed account-required landing and single visible progression action.

Behavioural or semantic evidence:
- `supporting/native-ui-patterns/research/notes/android/direct-observation-log.md`, Observations by app > Photos; Maps; Google Play Store: Records the bounded sign-in/deferral choices and absent downstream inspection.

Integration:
- Catalog: Deepen named variants under the existing umbrella. Preserve Permission prompt boundary as behavioural/consent coverage, not a duplicate visual entry.
- Runtime: Clarify Maps audio row as a contextual primer sheet. Keep the exact state/comparison routing.
- Index mapping: No heading, asset or mapping changes. Do not add a generic loading pattern for the Calendar setup state.

Confidence: high. Exact original images and app logs were read.

Privacy: Cited states safe-for-reuse under this audit. Generic map geography is not an observed personal location.

Priority: high. Improves existing evidence accuracy or explanatory depth. Inspected sample only. 3 cited images, not independent observations or platform prevalence.

<a id="f8"></a>

### F8. Update the Android discard-confirmation evidence to both passes

Identity: android · existing-pattern-improvement · Safe abandonment confirmation. Proposed operation: editing.

Scope and purpose: [Observed] Contacts initial first-name modification and later temporary email modification. [Inferred] The catalog should not imply cancellation was never exercised when the later log records it.

Current coverage:
- Catalog: `supporting/native-ui-patterns/docs/android/forms-and-controls.md#unsaved-change-confirmation`, `supporting/native-ui-patterns/docs/android/forms-and-controls.md#structured-create-contact-form`.
- Runtime: `skills/native-ui-patterns/references/android/editing.md`.
- Gap: The standalone confirmation entry still says the audit left via Home without choosing either action and cites only R022. The later pass exercised Discard from R019 and returned to the list. This is a state/evidence improvement, not a new confirmation pattern.

Proposed catalog-field wording:
- Description: [Observed] Leaving an unsaved modified Contacts form displayed a compact centred warning with Discard and Save actions.
- Visual structure: [Observed] A pale rounded dialog dims the form, places consequence copy above two horizontally separated text actions towards the trailing side, and exposes the surrounding form only as subdued context. The first-name and email cases place the same dialog over different scrolled form regions.
- Interaction: [Observed] The first pass left via Home. The later error pass used Back then Discard, returning to the empty list. [Unconfirmed] Save outcome and persistent-item deletion.
- States: [Observed] Modified form, warning visible and discarded return. Keep the two edit contexts as lifecycle evidence, not separate patterns.
- Variations: [Observed] First-name and email temporary-edit contexts only, both Contacts.
- Design guidance: [Inferred] State the consequence and separate abandoning work from preserving it. Do not label unsaved text abandonment a persistent deletion confirmation.

Visual evidence, with paths in the private ledger:
- R022: Original warning over first-name edit.
- R019: Warning over email edit in later pass.
- R016: Empty-list return associated with the logged Discard action.

Behavioural or semantic evidence:
- `supporting/native-ui-patterns/research/notes/android/direct-observation-log.md`, Observations by app > Contacts: Original Home exit without Discard/Save.
- `supporting/native-ui-patterns/research/notes/android/error-feedback-pass.md`, Attempt log and evidence mapping, Contacts row: Later Back → warning → Discard → empty list.

Integration:
- Catalog: Update Interaction/States/evidence links in Unsaved-change confirmation and reconcile its older-pass Notes.
- Runtime: Existing dirty-dismiss and return routes suffice. Do not auto-load both warnings.
- Index mapping: No heading/count/mapping changes. One canonical warning per accepted edit context, no copied assets.

Confidence: high. Both warning captures and the explicit later log were checked.

Privacy: R019/R022 conservatively require sanitisation of form-entered text before reuse. This does not assert the logged test tokens are real identities.

Priority: high. Improves existing evidence accuracy or explanatory depth. Inspected sample only. 3 cited images, not independent observations or platform prevalence.

<a id="f9"></a>

### F9. Document the already-routed single-field folder dialog

Identity: android · existing-pattern-improvement · Forms and editing / bounded input dialog. Proposed operation: editing.

Scope and purpose: [Observed] Files New folder pre-commit states already routed at runtime. [Inferred] A small value-entry task needs different anatomy from a full Contacts form or time picker.

Current coverage:
- Catalog: `supporting/native-ui-patterns/docs/android/forms-and-controls.md#structured-create-contact-form`, `supporting/native-ui-patterns/docs/android/forms-and-controls.md#modal-time-picker`.
- Runtime: `skills/native-ui-patterns/references/android/editing.md`.
- Gap: No supporting section describes the Files dialog despite a runtime row and retained log/dumps. It is not a new runtime capability. The absent detailed catalog counterpart is a documentation gap.

Proposed catalog-field wording:
- Description: [Observed] Files places one Name input and Cancel/OK actions inside a centred dialog above dimmed Downloads content.
- Visual structure: [Observed] The broad pale rectangular dialog has modest corner rounding, a centred title, an outlined full-width input with its label interrupting the top border, and two trailing text actions along the bottom. R029 is the cleaner dialog state but a floating input toolbar covers its leading edge. R028 also retains an open menu/underlying visual bleed and is not a clean settled anatomy reference.
- Interaction: [Observed] The safe attempt opened New folder, entered temporary text and cancelled. Matching dumps report OK enabled before and after entry. [Unconfirmed] Creation and validation on OK.
- States: [Observed] Empty and populated pre-commit images, plus a returned Downloads frame. Neither no visible error nor enabled OK proves a valid filename.
- Variations: [Unconfirmed] Error, successful creation, software-keyboard and clean unoccluded variants.
- Design guidance: [Inferred] Keep one-field input and its consequence local. Do not model the floating input toolbar or the empty-frame bleed as intentional application anatomy.

Visual evidence, with paths in the private ledger:
- R028: Empty input plus capture occlusion/bleed and still-open menu.
- R029: Populated outlined input, Cancel/OK and leading input-toolbar occlusion.

Behavioural or semantic evidence:
- `supporting/native-ui-patterns/research/notes/android/error-feedback-pass.md`, Attempt log and evidence mapping, Files row: Temporary pre-commit text was retained without inline error and Cancel returned to Downloads.
- `supporting/native-ui-patterns/research/notes/android/ui-dumps/files-new-folder-empty.xml`, OK button node: enabled=true in empty state.
- `supporting/native-ui-patterns/research/notes/android/ui-dumps/files-new-folder-invalid-name.xml`, OK button node: enabled=true after temporary entry.

Integration:
- Catalog: Propose a new supporting canonical heading Single-field creation dialog (application-specific), because hiding it under Contacts/time picker would erase a useful design distinction.
- Runtime: Keep existing folder row and add its occlusion caveat. No new operation file.
- Index mapping: Add heading/index/original-mapping extension deliberately. Checker heading contract becomes 41 if this batch is applied alone. No new PNGs required. Preserve the original 40-section historical mapping separately from expanded catalog membership.

Confidence: high. The runtime coverage and two original appearances are direct, but clean unoccluded appearance is unavailable.

Privacy: No personal value identified in these Files captures. Visual quality, not privacy, limits their canonical use.

Priority: medium. Improves existing evidence accuracy or explanatory depth. Inspected sample only. 2 cited images, not independent observations or platform prevalence.

<a id="f10"></a>

### F10. Labeled continuous-value cards in Pixel Settings

Identity: android · new-pattern · Forms and controls. Proposed operation: editing.

Scope and purpose: [Observed] Settings on one unidentified-version device, with several audio/brightness uses. [Inferred] Continuous adjustment is distinct from selection dialogs and binary switches. Recurrence is within this app, not proof of an Android-wide convention.

Current coverage:
- Catalog: `supporting/native-ui-patterns/docs/android/forms-and-controls.md#trailing-switch-in-a-settings-or-list-row`, `supporting/native-ui-patterns/docs/android/forms-and-controls.md#labeled-chip-or-compact-filter-control`, `supporting/native-ui-patterns/docs/android/forms-and-controls.md#modal-time-picker`.
- Runtime: `skills/native-ui-patterns/references/android/editing.md`.
- Gap: Current Android forms have summaries, switches and discrete selectors, but no visible continuous-value control. A changed colour alone would be a variation. A track/thumb/value mechanism is a distinct control.

Proposed catalog-field wording:
- Description: [Observed] Pixel Settings places horizontal track/fill/thumb controls below labels in joined dark rounded cards.
- Visual structure: [Observed] E001 contains six stacked labelled sliders, each with a filled segment, darker remainder, narrow vertical thumb and trailing purpose icon. No numeric percentage is visible. E006 places one Intensity track inside a separate lower card, with Dimmer/Brighter endpoint text beneath it, below a stock-image comparison and a separate availability switch.
- Interaction: [Unconfirmed] No drag, tap, increment, accessibility adjustment, range, step size or persistence was tested.
- States: [Observed] One displayed position per control. Static evidence is not a before/after pair.
- Variations: [Observed] Six audio-level rows versus a single HDR intensity card. The latter uses endpoint text rather than the audio purpose icons. Do not infer numeric ranges or a brightness-level percentage.
- Design guidance: [Inferred] Keep label, value and endpoints legible without relying on fill alone. Confirm control semantics and adjustment behaviour in implementation.

Visual evidence, with paths in the private ledger:
- E001: Six stacked audio sliders with labels, purpose icons and distinct relative positions.
- E006: HDR intensity track in the lower card, separate from the feature switch and stock-image comparison.

Behavioural or semantic evidence:
No separate behavioural or semantic record is relied on for this finding. Appearance alone does not establish an interaction or semantic claim.

Integration:
- Catalog: Propose Labeled continuous-value control (Settings, application-specific) in Android forms. Link both examples, nominate only one canonical for a matching task.
- Runtime: Add a brief editing cue and one exact visual route after a verified derivative is admitted. No new operation file.
- Index mapping: New supporting heading and index entry. Add a provenance extension for new derivatives without rewriting original 93 mappings. Checker/tests require an explicit asset and catalog-contract migration.

Confidence: high for appearance, unconfirmed for behaviour. Two directly inspected examples show the mechanism in one app.

Privacy: E001 and E006 are technically safe-for-reuse under this audit. E006 retains auxiliary HDR container metadata, not confirmed personal metadata. Publication rights/source provenance are still unconfirmed.

Priority: medium. Distinct mechanism absent from the current catalog. Inspected sample only. 2 cited images, not independent observations or platform prevalence.

<a id="f11"></a>

### F11. Slider and switch mechanisms in iOS Settings

Identity: ios · new-pattern · Forms and controls. Proposed operation: editing.

Scope and purpose: [Observed] Additional iPhone Settings captures, exact versions unknown for these files. [Inferred] New control mechanisms should not be buried inside a generic grouped-row description.

Current coverage:
- Catalog: `supporting/native-ui-patterns/docs/ios/forms-and-controls.md#grouped-form-rows`, `supporting/native-ui-patterns/docs/ios/navigation-and-presentation.md#large-title-hierarchy`.
- Runtime: `skills/native-ui-patterns/references/ios/editing.md`.
- Gap: The existing grouped-form entry describes alignment and grouping, but does not document slider tracks/thumbs or the binary-switch mechanism. IOS-1 correctly found missing anatomy but combined distinct controls under one improvement.

Proposed catalog-field wording:
- Description: [Observed] Settings presents continuous-looking sliders and binary-looking switches inside inset light cards. Describe these as separate controls sharing a grouped container.
- Visual structure: [Observed] Brightness uses a long horizontal track, an oval/rounded thumb and small endpoint symbols. Related cards put a leading text label opposite a trailing pill switch with a white thumb. Selected-looking switches use coloured tracks, while other states use muted neutral tracks. Do not turn this visual appearance into a claim of checked semantics.
- Interaction: [Unconfirmed] Adjustment, switching, delayed application, persistence, range and accessibility APIs were not exercised.
- States: [Observed] Static displayed positions and on/off-looking appearances only.
- Variations: [Observed] Continuous adjustment and binary selection remain separate named subentries, not a merged generic setting. F16 owns the shared row/container grammar.
- Design guidance: [Inferred] Keep value adjustment, binary selection and drill-down affordances visually distinct. Validate semantics and hit areas separately.

Visual evidence, with paths in the private ledger:
- E055: Brightness track/rounded thumb and switches beneath it.
- E058: Ringtone slider and binary-looking settings in Sounds & Haptics.
- E053: Scrolled Appearance rows with switches and trailing values.

Behavioural or semantic evidence:
No separate behavioural or semantic record is relied on for this finding. Appearance alone does not establish an interaction or semantic claim.

Integration:
- Catalog: Propose two named canonical entries or a controls section with separate slider/switch subsections. Approve exact heading membership before updating the checker. Do not hide both in generic Grouped form rows.
- Runtime: One concise control-family cue with separate exact-state routes only if each is needed. Stay in editing.md.
- Index mapping: Requires approved new-asset provenance and catalog/index additions. No automatic import of all examples.

Confidence: high for appearance, unconfirmed for behaviour. Primary reconciled the worker grouping against directly inspected control images.

Privacy: All cited additional iOS files require metadata sanitisation. Some reveal personal configuration and need pixel review before derivative approval.

Priority: medium. Distinct mechanism absent from the current catalog. Inspected sample only. 3 cited images, not independent observations or platform prevalence.

<a id="f12"></a>

### F12. Preview-led appearance choice

Identity: ios · new-pattern · Forms and controls / visual selection. Proposed operation: editing.

Scope and purpose: [Observed] One additional Settings appearance screen. [Inferred] Choosing among visual outcomes through preview cards is a different mechanism from selecting a text row.

Current coverage:
- Catalog: `supporting/native-ui-patterns/docs/ios/forms-and-controls.md#grouped-form-rows`, `supporting/native-ui-patterns/docs/ios/navigation-and-presentation.md#large-title-hierarchy`.
- Runtime: `skills/native-ui-patterns/references/ios/editing.md`.
- Gap: Neither a preview choice nor its selected marker is described in the existing iOS catalog. This is not simply another grouped row or colour-theme variation.

Proposed catalog-field wording:
- Description: [Observed] Settings presents side-by-side appearance previews with labels and a selected circular marker beneath one option.
- Visual structure: [Observed] Two compact device-like previews share a rounded group. Their content previews show contrasting light/dark outcomes. Each has a centred text label and an aligned circular selection marker beneath it. A separate Automatic switch row follows, with another disclosure/value row below.
- Interaction: [Unconfirmed] Selecting a preview, automatic scheduling and theme persistence were not exercised.
- States: [Observed] One option is visibly selected-looking. Alternative selected state and transition are not retained.
- Variations: [Unconfirmed] No other app or platform recurrence established.
- Design guidance: [Inferred] Pair previews with explicit labels and a non-colour selection marker. Do not claim the preview exactly predicts every system surface.

Visual evidence, with paths in the private ledger:
- E052: Upper preview pair, labels, selection marker, automatic row and schedule/value context.

Behavioural or semantic evidence:
No separate behavioural or semantic record is relied on for this finding. Appearance alone does not establish an interaction or semantic claim.

Integration:
- Catalog: Propose Preview-based single choice (Settings, application-specific).
- Runtime: Add one editing route only after approved sanitised evidence exists. It is not a reason for a new appearance operation.
- Index mapping: One new supporting heading/index entry plus derivative provenance and checker-contract update.

Confidence: high for visible selection, unconfirmed for interaction. The selection mechanism is directly visible in one application.

Privacy: Metadata stripping and personal-settings review required. Do not inherit device/OS identity from adjacent files.

Priority: medium. Distinct mechanism absent from the current catalog. Inspected sample only. 1 cited images, not independent observations or platform prevalence.

<a id="f13"></a>

### F13. Credential-task appearance without visible input mechanism

Identity: ios · uncertain · Dedicated task surface. Proposed operation: none until a complete safe state is captured.

Scope and purpose: [Observed] One Settings passcode-request sheet, with the entry area blank. [Unconfirmed] The image cannot support a keypad or masked-slot pattern.

Current coverage:
- Catalog: `supporting/native-ui-patterns/docs/ios/navigation-and-presentation.md#full-screen-task-surface`.
- Runtime: `skills/native-ui-patterns/references/ios/editing.md`.
- Gap: The top task boundary is a covered presentation variation. The blank lower area does not establish a new credential-input mechanism.

Proposed catalog-field wording:
- Description: [Observed] A white rounded task sheet appears over dimmed context, with a leading circular close control, centred blue lock icon, bold passcode-request title and muted explanatory copy.
- Visual structure: [Observed] The lower sheet is blank. No keyboard, keypad, input slots, entered code or error is visible.
- Interaction: [Unconfirmed] No credential entry, authentication, retry, lockout or cancellation outcome was tested.
- States: [Observed] Request copy and blank entry region only. [Unconfirmed] Whether the omitted controls are transient, protected from capture or otherwise absent.
- Variations: [Observed] Sheet geometry is a variation of an already-covered task presentation, not evidence for a distinct fixed-length code entry.
- Design guidance: [Inferred] Do not fabricate the missing mechanism or copy a security workflow from an incomplete still.

Visual evidence, with paths in the private ledger:
- E062: Top lock/title/helper and close control. The rest of the rounded sheet is blank.

Behavioural or semantic evidence:
No separate behavioural or semantic record is relied on for this finding. Appearance alone does not establish an interaction or semantic claim.

Integration:
- Catalog: No new canonical pattern. Record a narrowly scoped incomplete-evidence note only.
- Runtime: No new image route.
- Index mapping: No changes. A safe recapture would require explicit approval and must never expose a credential.

Confidence: high for visible top anatomy, low for any input pattern. Primary reopened the original and confirmed the absence of keypad or slots.

Privacy: Metadata sanitisation required. No visible credential value in this frame. E038 contains an exposed network credential and is not a substitute.

Priority: defer. Reusable pattern or missing state not established. Inspected sample only. 1 cited images, not independent observations or platform prevalence.

<a id="f14"></a>

### F14. Clarify trailing-switch glyph and split-row variation

Identity: android · existing-pattern-variation · Settings rows / binary control. Proposed operation: editing.

Scope and purpose: [Observed] Pixel Settings row with label/summary, chevron, divider and trailing switch. [Inferred] This is a useful variation within existing row/control coverage, not a new top-level pattern.

Current coverage:
- Catalog: `supporting/native-ui-patterns/docs/android/forms-and-controls.md#trailing-switch-in-a-settings-or-list-row`, `supporting/native-ui-patterns/docs/android/interactions-and-accessibility.md#semantic-selected-and-checked-state`.
- Runtime: `skills/native-ui-patterns/references/android/editing.md`, `skills/native-ui-patterns/references/android/content-states.md`.
- Gap: The canonical switch entry already covers the chevron/divider and Clock variation. The real increment is explicit check/X styling in additional Settings stills, and separating this visual cue from XML-confirmed state.

Proposed catalog-field wording:
- Description: [Observed] Some Settings rows put a title/summary and a chevron beside a vertical divider and a trailing pill switch.
- Visual structure: [Observed] The leading text region occupies most of the rounded row. A chevron sits before the divider, and the switch is visually separated on the trailing side. R050 shows a muted track and cross-mark thumb. E009 shows coloured on-looking controls in several dark rows.
- Interaction: [Unconfirmed] Independent row versus switch hit targets, tap outcomes and accessibility grouping. The divider suggests separation but cannot prove it.
- States: [Observed] R008/R050 matching dumps expose checked=false. E009/E020 show check/X glyph treatments, but additional-image semantic state is Unconfirmed.
- Variations: [Observed] R008 Clock switches lack the same divider/disclosure composition. Keep that difference explicit.
- Design guidance: [Inferred] Preserve the visible division when a row offers both detail navigation and a binary setting, but verify the intended actions and accessible names independently.

Visual evidence, with paths in the private ledger:
- R050: Existing split-looking Settings row establishes current overlap.
- E009: Multiple dark Settings rows with chevrons, dividers and on-looking switches.
- R008: Clock supplies already-covered switch anatomy without the split row.
- E020: Adjacent apparent on/check and off/X switches in the lower System sounds group.

Behavioural or semantic evidence:
- `supporting/native-ui-patterns/research/notes/android/ui-dumps/settings-display-detail.xml`, Dark theme row and switch nodes: Use the exact dump only for exposed node properties. It does not establish independent effective touch targets.
- `supporting/native-ui-patterns/research/notes/android/ui-dumps/clock-alarm-list.xml`, Switch nodes: Existing Clock semantic switches corroborate current binary-control coverage.

Integration:
- Catalog: Refine Trailing switch in a settings or list row. Its split-row variation already exists, so do not add another canonical entry.
- Runtime: Only a concise variation note if needed. One exact image route, not an automatic two-image load.
- Index mapping: No new canonical heading. Additional evidence still requires approved provenance/asset-count migration.

Confidence: high for geometry, unconfirmed for target behaviour. Primary compared original Settings/Clock and additional E009.

Privacy: Cited originals and E009 currently safe-for-reuse technically. Publication-rights clearance remains separate.

Priority: medium. Bounded variation within existing anatomy. Inspected sample only. 4 cited images, not independent observations or platform prevalence.

<a id="f15"></a>

### F15. Dark-theme grouped Settings cards across detail pages

Identity: android · existing-pattern-variation · Grouped card list. Proposed operation: content-states.

Scope and purpose: [Observed] Five additional dark Pixel Settings detail pages. [Inferred] Only a bounded colour/grouping variation of existing multirow containers.

Current coverage:
- Catalog: `supporting/native-ui-patterns/docs/android/lists-content-feedback.md#grouped-card-list`.
- Runtime: `skills/native-ui-patterns/references/android/content-states.md`.
- Gap: The canonical anatomy and detail-page route already exist. The additional evidence only extends the visible variation to dark multirow detail pages with prominent section spacing.

Proposed catalog-field wording:
- Description: Keep the existing grouped-card description; optionally note a dark Settings detail-page variation.
- Visual structure: [Observed] Muted section labels precede rounded dark-gray containers on a near-black background; spacing between sections exceeds spacing between joined rows inside one container.
- Interaction: [Unconfirmed] Additional stills do not establish grouping semantics or target behavior.
- States: [Observed] Rows show title/summary hierarchy with optional leading icons and optional trailing chevrons or switches.
- Variations: [Observed] Containers may hold one action, multiple joined rows, or rows with embedded binary/detail controls.
- Design guidance: [Inferred] Group by task, keep row titles/states legible, preserve stronger inter-section spacing, and label nested controls semantically.
- Notes: Single-application, OS-version-unknown variation; not a platform-wide dark-theme prescription.

Visual evidence, with paths in the private ledger:
- E002: Do Not Disturb/Bedtime/Driving group and lower create-mode card. Dark grouped rows plus a separate single-action container.
- E009: Adaptive display and Lock screen section groups. Dark multirow containers with summaries, dividers, chevrons, and switches.
- E013: parental limit/filter groups and PIN card. Repeated section-label and grouped-container hierarchy.
- E015: Other devices and Saved devices sections. Single and grouped dark cards separated by section spacing.
- E020: System sounds & vibrations section. Long joined-row group with consistent trailing controls.

Behavioural or semantic evidence:
No separate behavioural or semantic record is relied on for this finding. Appearance alone does not establish an interaction or semantic claim.

Integration:
- Catalog: At most one bounded variation sentence under Grouped card list.
- Runtime: No new route. Existing grouped Settings root/detail route is sufficient.
- Index mapping: No changes unless one source is formally admitted with derivative provenance.

Confidence: medium. The visual variation recurs across five pages, but all are one app, version is unknown, and no semantic hierarchy is available.

Privacy: Selected E002/E009/E013/E015/E020 are technically safe-for-reuse. Rights and exact OS version remain unknown.

Priority: low. Bounded variation within existing anatomy. Inspected sample only. 5 cited images, not independent observations or platform prevalence.

<a id="f16"></a>

### F16. Deepen shared iOS grouped row grammar

Identity: ios · existing-pattern-variation · Inset grouped drill-down and read-only rows. Proposed operation: navigation.

Scope and purpose: [Observed] Repeated additional Settings pages. [Inferred] Useful row variants belong beneath existing hierarchy/grouping patterns, while F11–F13 retain distinct control mechanisms.

Current coverage:
- Catalog: `supporting/native-ui-patterns/docs/ios/navigation-and-presentation.md#large-title-hierarchy`, `supporting/native-ui-patterns/docs/ios/forms-and-controls.md#grouped-form-rows`.
- Runtime: `skills/native-ui-patterns/references/ios/navigation.md`, `skills/native-ui-patterns/references/ios/editing.md`.
- Gap: Existing descriptions under-specify terminal alignment and explanatory copy. The additional corpus does not justify a new Settings-list pattern or many per-page headings.

Proposed catalog-field wording:
- Description: [Observed] Settings reuses inset rounded groups with leading labels and differentiated trailing values, disclosures or no action marker.
- Visual structure: [Observed] Cards sit on a pale page with vertically separated section groups. Labels align consistently at the leading edge. Muted current values align towards the trailing edge before chevrons, while read-only metadata rows may omit chevrons. Thin inset separators and quieter multi-line explanatory copy below groups structure the page.
- Interaction: [Unconfirmed] A visible chevron suggests drill-down, but additional images have no action logs. Do not state all rows are tappable or share hit areas.
- States: [Observed] Static root/detail/settings-list appearances only.
- Variations: [Observed] Trailing value plus disclosure, disclosure without value, read-only value, explanatory footer, and control-bearing row. Refer to F11 for control mechanics rather than collapsing them into container anatomy.
- Design guidance: [Inferred] Choose the terminal affordance according to row purpose. Avoid adding a chevron to static information or presenting a disclosure as a switch.

Visual evidence, with paths in the private ledger:
- R086: Existing Settings General groups establish current grouped navigation coverage.
- E039: Update summary and values/disclosures provide an additional bounded example.
- E054: Detail setting rows and explanatory copy deepen the existing grammar.
- E032: Device Info rows contrast read-only trailing values with navigable service rows. Sensitive values are not reproduced.

Behavioural or semantic evidence:
No separate behavioural or semantic record is relied on for this finding. Appearance alone does not establish an interaction or semantic claim.

Integration:
- Catalog: Add concise named variations and anatomy to existing grouping entries. Keep navigation and input responsibilities separate.
- Runtime: One sentence at most, no wholesale extra screenshot list. Generic navigation can retain R086.
- Index mapping: No new canonical heading. Additional images are optional corroboration, not required imports.

Confidence: high for visual recurrence within Settings. The worker inspected all additional iOS images and the primary separated container variation from control mechanisms.

Privacy: Additional images require metadata sanitisation. Prefer existing safe R086 where its anatomy suffices.

Priority: medium. Bounded variation within existing anatomy. Inspected sample only. 3 cited images, not independent observations or platform prevalence.

<a id="f17"></a>

### F17. Consequence-labeled offload versus deletion actions

Identity: ios · application-specific · Editing / consequential actions. Proposed operation: editing.

Scope and purpose: [Observed] A Settings per-app storage detail. [Inferred] Distinguishing two storage-recovery consequences is useful, but it is not an observed deletion-confirmation flow.

Current coverage:
- Catalog: `supporting/native-ui-patterns/docs/ios/forms-and-controls.md#add-and-remove-rows-application-specific`.
- Runtime: `skills/native-ui-patterns/references/ios/editing.md`.
- Gap: Existing coverage concerns repeatable form rows. This page instead contrasts two large consequential actions with explanation. No confirmation or executed outcome is captured.

Proposed catalog-field wording:
- Description: [Observed] Separate Offload App and Delete App actions appear below app/storage facts, each followed by consequence copy.
- Visual structure: [Observed] Blue versus red centred action text sits in separate full-width rounded white rows. Muted explanatory paragraphs immediately follow each action. The app identity and size summary form a different card above.
- Interaction: [Unconfirmed] Neither action was exercised. The copy describes retaining versus removing data, but actual retention/deletion was not verified.
- States: [Observed] Pre-action detail only.
- Variations: [Unconfirmed] Other apps and confirmation steps.
- Design guidance: [Inferred] Explain the consequence beside each action rather than relying on red alone.

Visual evidence, with paths in the private ledger:
- E042: Middle action rows and adjacent consequence text, excluding personal media/usage details.

Behavioural or semantic evidence:
No separate behavioural or semantic record is relied on for this finding. Appearance alone does not establish an interaction or semantic claim.

Integration:
- Catalog: Optional application-specific supporting example after safe derivative approval. Do not call it a persistent-deletion confirmation pattern.
- Runtime: No route needed in the first batches.
- Index mapping: A future independent canonical entry requires an explicit heading/index/asset migration.

Confidence: high for appearance only. 

Privacy: Personal storage measurements/media library and metadata require sanitisation. Preserve only action anatomy if the evidence remains useful.

Priority: low. Useful only within the stated product/context until further evidence. Inspected sample only. 1 cited images, not independent observations or platform prevalence.

<a id="f18"></a>

### F18. Storage capacity breakdown dashboard

Identity: android · application-specific · Quantitative content. Proposed operation: content-states.

Scope and purpose: [Observed] A Settings storage page. [Inferred] Capacity summary and per-category breakdown can be useful, but the numerical/ratio data is personal telemetry and one app does not establish a platform convention.

Current coverage:
- Catalog: `supporting/native-ui-patterns/docs/android/lists-content-feedback.md#grouped-card-list`.
- Runtime: `skills/native-ui-patterns/references/android/content-states.md`.
- Gap: Existing cards describe grouping, not quantitative capacity encoding. Defer import rather than promote every dashboard to a pattern.

Proposed catalog-field wording:
- Description: [Observed] A top capacity summary/bar precedes a cleanup action and category rows with usage measurements.
- Visual structure: [Observed] The page separates aggregate capacity from lower category rows, aligns measurements at the trailing side and uses a horizontal fill cue above.
- Interaction: [Unconfirmed] Cleanup, drill-down, refresh and calculation behaviour.
- States: [Observed] One static personal usage distribution.
- Variations: [Unconfirmed] Empty/full thresholds, alerts and accessible chart alternatives.
- Design guidance: [Inferred] Pair visual proportion with readable quantities. Use controlled safe data before publishing a canonical example.

Visual evidence, with paths in the private ledger:
- E008: Top usage/bar and per-category quantities, without reproducing their values.

Behavioural or semantic evidence:
No separate behavioural or semantic record is relied on for this finding. Appearance alone does not establish an interaction or semantic claim.

Integration:
- Catalog: No immediate addition. Safe recapture could justify a separate application-specific quantitative entry.
- Runtime: No new route now.
- Index mapping: No changes until safe source and value are demonstrated.

Confidence: high for appearance, limited reuse. 

Privacy: Primary changed worker safe-for-reuse to requires-sanitization. Redaction of quantities and proportions may remove the evidence, so prefer controlled recapture.

Priority: defer. Useful only within the stated product/context until further evidence. Inspected sample only. 1 cited images, not independent observations or platform prevalence.

<a id="f19"></a>

### F19. Placeholder rows are not a proven loading lifecycle

Identity: ios · uncertain · Content state. Proposed operation: none.

Scope and purpose: [Observed] One TV Provider settings still contains placeholder-shaped rows. [Unconfirmed] Their trigger, animation, duration and eventual result.

Current coverage:
- Catalog: `supporting/native-ui-patterns/docs/ios/lists-content-feedback.md#centered-empty-state`.
- Runtime: `skills/native-ui-patterns/references/ios/content-states.md`.
- Gap: There is no verified loading lifecycle in current coverage. This still offers skeleton-like anatomy, not sufficient evidence to fill that gap as observed loading behaviour.

Proposed catalog-field wording:
- Description: [Observed] The available-apps group contains four repeated placeholder-looking rows.
- Visual structure: [Observed] Each row has a rounded-square leading block, two neutral horizontal bars and a trailing pill, separated by thin lines inside a rounded white group.
- Interaction: [Unconfirmed] No wait, fetch, refresh or transition was observed.
- States: [Observed] Placeholder appearance only. [Unconfirmed] Loaded, failed, animated or persistent-redaction interpretation.
- Variations: [Unconfirmed] Recurrence outside this single page.
- Design guidance: [Inferred] Keep this as an uncertain candidate. Capture the initiating action and settled outcome before naming a loading pattern.

Visual evidence, with paths in the private ledger:
- E048: Available-apps placeholder group, not the signed-in account/footer.

Behavioural or semantic evidence:
No separate behavioural or semantic record is relied on for this finding. Appearance alone does not establish an interaction or semantic claim.

Integration:
- Catalog: Uncertain-findings note only if later approved. Do not add a confirmed loading heading.
- Runtime: No new route.
- Index mapping: No import or count change.

Confidence: high for shapes, low for lifecycle. 

Privacy: Account identity/subscription context and metadata require sanitisation. This is not an anonymous demonstration screenshot.

Priority: defer. Reusable pattern or missing state not established. Inspected sample only. 1 cited images, not independent observations or platform prevalence.

<a id="f20"></a>

### F20. Privacy-limited dashboard candidates remain separate

Identity: android · uncertain · Status, recommendations and activity. Proposed operation: none.

Scope and purpose: [Observed] Four non-equivalent Settings pages use security, emergency, location-access and digital-activity content. [Inferred] These are separate candidate compositions, not one reusable dashboard pattern.

Current coverage:
- Catalog: `supporting/native-ui-patterns/docs/android/lists-content-feedback.md#grouped-card-list`.
- Runtime: `skills/native-ui-patterns/references/android/content-states.md`, `skills/native-ui-patterns/references/android/onboarding-permissions.md`.
- Gap: Grouping is already covered. Domain-specific summary mechanisms and behaviours have not been safely established as reusable patterns.

Proposed catalog-field wording:
- Description: [Observed] Security combines status/recommendation, emergency exposes safety settings, location shows recent access, and digital wellbeing uses activity metrics.
- Visual structure: [Observed] Summary devices differ. Preserve four separate source records rather than merging their anatomy.
- Interaction: [Unconfirmed] No actions, refreshes, recovery paths or semantic readings.
- States: [Observed] One personal configuration/activity state per page.
- Variations: [Unconfirmed] These are not confirmed variations of one pattern.
- Design guidance: [Inferred] Do not publish identifying or sensitive domain content merely to claim broader coverage. A controlled safe recapture should answer a specific design question.

Visual evidence, with paths in the private ledger:
- E003: Security status/recommendation, excluded.
- E007: Health/safety configuration, excluded.
- E011: Location-access context, excluded.
- E019: Personal digital-activity metrics, excluded.

Behavioural or semantic evidence:
No separate behavioural or semantic record is relied on for this finding. Appearance alone does not establish an interaction or semantic claim.

Integration:
- Catalog: Retain as separate uncertain candidates in the private ledger. No umbrella canonical entry.
- Runtime: No route.
- Index mapping: No import. Existing privacy-excluded source classification remains.

Confidence: low for reusable pattern. 

Privacy: All four excluded because the sensitive content is central to the claimed evidence.

Priority: defer. Reusable pattern or missing state not established. Inspected sample only. 4 cited images, not independent observations or platform prevalence.

<a id="f21"></a>

### F21. Positive validation, gesture and accessibility gaps remain gaps

Identity: both · uncertain · Cross-operation state coverage. Proposed operation: none.

Scope and purpose: [Observed] Existing bounded tests avoided persistent save/send/grant outcomes. [Inferred] The next capture should resolve a specific implementation question, not satisfy a category quota.

Current coverage:
- Catalog: `supporting/native-ui-patterns/docs/ios/forms-and-controls.md#content-gated-commit-control`, `supporting/native-ui-patterns/docs/android/interactions-and-accessibility.md#semantic-selected-and-checked-state`.
- Runtime: `skills/native-ui-patterns/references/ios/editing.md`, `skills/native-ui-patterns/references/android/editing.md`, `skills/native-ui-patterns/references/ios/accessibility.md`, `skills/native-ui-patterns/references/android/accessibility.md`.
- Gap: Pre-commit input retained without visible error is not accepted data. Muted pixels are not semantic disabled state. Still bounds cannot prove hit targets, focus order, spoken labels or gesture response.

Proposed catalog-field wording:
- Description: [Observed] Existing field-gating, pre-commit no-error and cancellation evidence is bounded.
- Visual structure: [Observed] Current images show input, control appearance and surrounding layout only.
- Interaction: [Unconfirmed] Successful save/send, submit-time validation, non-destructive retry/error recovery, assistive-technology interaction and most gesture outcomes.
- States: [Unconfirmed] No new screenshots close these gaps merely by resembling familiar platform UI.
- Variations: [Observed] Android original XML supports specific node properties. iOS local automation logs support specific exercised labels and gating. Neither proves complete accessibility.
- Design guidance: [Inferred] Use a sandbox with authorised synthetic data, paired action/result captures and exact semantic records when the missing state affects a decision.

Visual evidence, with paths in the private ledger:
- R070: iOS temporary email: no visible inline feedback before logged discard.
- R020: Android temporary email: pre-save appearance, not acceptance proof.

Behavioural or semantic evidence:
- `supporting/native-ui-patterns/research/notes/ios/error-feedback-pass.md`, Contacts — invalid email entry: No submit-time validation tested.
- `supporting/native-ui-patterns/research/notes/android/error-feedback-pass.md`, Attempt log and evidence mapping: Safe pre-commit attempts and cancel/discard only.

Integration:
- Catalog: Keep explicit unconfirmed states, correcting only the known Contacts discard path in F4.
- Runtime: Retain review-check prompts, no guessed visual routes.
- Index mapping: Future captures need scoped authorisation and provenance. No current changes.

Confidence: high for limits. 

Privacy: Prefer safe synthetic-data captures. Do not exercise real communication, payments, permission grants or destructive actions without explicit separate approval.

Priority: defer. Reusable pattern or missing state not established. Inspected sample only. 2 cited images, not independent observations or platform prevalence.

<a id="f22"></a>

### F22. Do not multiply iOS empty/search-empty canonicals

Identity: ios · duplicate · Centered empty state. Proposed operation: content-states / search.

Scope and purpose: [Observed] Empty Files/Shortcuts and unmatched Settings search share an existing centred symbol/title/helper composition. [Inferred] Different causes are important state labels, not automatic new pattern headings.

Current coverage:
- Catalog: `supporting/native-ui-patterns/docs/ios/lists-content-feedback.md#centered-empty-state`.
- Runtime: `skills/native-ui-patterns/references/ios/content-states.md`, `skills/native-ui-patterns/references/ios/search.md`.
- Gap: The existing entry already includes query-empty and content-empty evidence. F1 corrects state routing, not the taxonomy.

Proposed catalog-field wording:
- Description: Retain the existing canonical and cause-specific state labels.
- Visual structure: [Observed] Central symbol/title/helper clusters have different surrounding navigation and keyboard contexts.
- Interaction: [Observed] Only the recorded Settings query/clear path supports recovery. Do not transfer that behaviour to empty Files or Shortcuts.
- States: [Observed] No content versus no matching query.
- Variations: [Observed] Keep keyboard/search context distinct from a content-empty destination.
- Design guidance: [Inferred] Reuse the canonical structure and select the exact cause/state, rather than importing another nearly identical image.

Visual evidence, with paths in the private ledger:
- R071: Empty Files location.
- R090: Unmatched Settings query with keyboard.
- R091: Empty Shortcuts library.

Behavioural or semantic evidence:
No separate behavioural or semantic record is relied on for this finding. Appearance alone does not establish an interaction or semantic claim.

Integration:
- Catalog: No new heading.
- Runtime: Keep existing exact-state routes, with F1 correction.
- Index mapping: No import, merge deletion or original mapping changes.

Confidence: high. 

Privacy: Cited originals safe-for-reuse technically.

Priority: low. Already covered, no new canonical proposed. Inspected sample only. 3 cited images, not independent observations or platform prevalence.

<a id="f23"></a>

### F23. Do not promise search remains visible in the expanded map sheet

Identity: android · existing-pattern-improvement · Layered map content presentation. Proposed operation: navigation.

Scope and purpose: [Observed] Mapped Maps low/expanded sheet states. [Inferred] Different sheet heights change which map/search controls remain visible.

Current coverage:
- Catalog: `supporting/native-ui-patterns/docs/android/navigation-and-presentation.md#draggable-map-content-sheet`, `supporting/native-ui-patterns/docs/android/interactions-and-accessibility.md#drag-gesture-changes-sheet-position`.
- Runtime: `skills/native-ui-patterns/references/android/navigation.md`.
- Gap: The description should distinguish retained map context from retained search controls. Search/categories visible above the low sheet are covered in the expanded frame.

Proposed catalog-field wording:
- Description: [Observed] A rounded map-content sheet rises from the bottom while retaining a narrow map strip in its expanded state.
- Visual structure: [Observed] Both frames show a centred drag handle and inset content headings/cards. The lower sheet leaves the top search capsule and categories exposed. The expanded sheet covers those controls and most map content, while the bottom peer navigation remains visible. Different visible card positions do not establish synchronised scroll continuity.
- Interaction: [Observed] The local action log records one upward swipe that expanded the sheet. [Unconfirmed] Exact detents, snapping, reverse drag, dismissal and APIs.
- States: [Observed] Lower and expanded retained positions.
- Variations: [Observed] This is map content, not the account/utility sheet in F6.
- Design guidance: [Inferred] Evaluate how increased content exposure occludes map commands. Load the pair only for an explicit position comparison.

Visual evidence, with paths in the private ledger:
- R033: Lower sheet with search/category controls above it.
- R034: Expanded sheet covers search, leaves map strip and bottom peer bar.

Behavioural or semantic evidence:
- `supporting/native-ui-patterns/research/notes/android/direct-observation-log.md`, Observations by app > Maps: One safe upward swipe expanded the sheet.

Integration:
- Catalog: Clarify visible-context changes in Draggable map content sheet and cross-check its gesture entry. Do not merge the two evidence layers.
- Runtime: Existing runtime wording already says bottom navigation remained and explicitly compares search/categories. Preserve it. The false retained-search claim is in the catalog Description.
- Index mapping: No heading, mapping or image changes.

Confidence: high for image states and logged single gesture. 

Privacy: R033 is technically safe-for-reuse. R034 requires sanitisation of people/faces in editorial imagery. No personal current-location marker is established. Text-only correction does not authorise redistributing the raw expanded image.

Priority: medium. Improves existing evidence accuracy or explanatory depth. Inspected sample only. 2 cited images, not independent observations or platform prevalence.

## Approval-gated implementation batches

These are proposals, not authorised work. Each batch needs an explicit selected scope. Publication remains blocked until all distributable privacy blockers are resolved, even if text corrections pass validation.

### B0. Restore a truthful baseline packaging check

Scope: only the unexpected runtime Finder cache files enumerated in `nonimage-metadata-ledger.json`. Preserve any required private copy, then remove them from the distributable runtime only after approval. Do not remove screenshots, rewrite mappings or broadly clean ignored content. Do not relax the runtime path allowlist.

Acceptance: record exact before/after file paths and hashes privately, rerun both existing Python commands, and retain any newly exposed failure as a blocker instead of fixing it opportunistically. No source image/hash changes. This batch is separate because the current checker stops at the first cache and cannot certify the remaining package.

### B1. Correct iOS visual routing using current assets

Findings: F1, F2 and F5.

Targets: `skills/native-ui-patterns/references/ios/search.md`, `navigation.md` and `content-states.md` only. Rename the resting-search route, remove the false same-base Files menu comparison, and choose the unobscured Calendar day for temporal anatomy. Preserve old images, all twelve operations and exact-state conditional loading. Do not add screenshots or enlarge the entry point.

Acceptance: both existing commands after B0, focused route assertions for the chosen image identities and preserved one-state/pair policy, and manual reopening of R089/R090, R071/R072 and R059/R060. Confirm that behavioural text-only requests still skip images. This is the highest-value first content batch.

### B2. Reconcile iOS catalog and discard claims

Findings: F1–F5, with the existing-asset portion of F16 only if explicitly selected.

Targets: the existing iOS `forms-and-controls.md`, `navigation-and-presentation.md` and `lists-content-feedback.md` catalog sections named in the findings, plus `references/ios/editing.md` and the specific coverage/limitations/uncertain statements that contradict the logged Contacts discard path. Split presentation/search anatomy and discard-history reconciliation into separate commits if useful, but keep each claim consistent across its affected summaries. Raw logs remain unchanged.

Acceptance: both commands, unchanged forty-heading/original-mapping contract, exact local-log citations, and manual verification that a logged discard action is not presented as a captured dialog appearance. Qualify original-pass Notes rather than deleting historical evidence. No new assets, route files or broad copy edits.

### B3. Deepen existing Android presentation and cancellation descriptions

Findings: F6, F7, F8 and F23. The existing-asset semantics portion of F14 may be included only if selected.

Targets: existing sections in Android `navigation-and-presentation.md`, `lists-content-feedback.md` and `forms-and-controls.md`. Use named variations for command panels, account sheets and primers. Correct expanded-map visibility and the later exercised Discard path. Current runtime routing mostly already expresses these distinctions and needs no automatic image expansion.

Acceptance: both commands, preserved canonical headings/anchors, exact dump/log provenance where used, and manual comparisons of the named states. Assert that map search is not claimed visible in the expanded frame and that unexercised actions remain Unconfirmed. No new images.

### B4. Establish and apply an approved privacy migration

Scope requires separate approval: private original preservation, the source-to-derivative manifest design, precise initial source IDs, permitted redactions, public-original disposition and reviewer. Start with one coherent family, such as the six existing Contacts images R065–R070, rather than all 73 sanitisation candidates. This is not approval to sanitise now.

Targets after approval: private preservation storage and provenance records, selected public derivative assets, their affected links, the relevant screenshot inventory/mapping extension, and `check_skill.py` / `test_check_skill.py`. Preserve the historical 93-original inventory and its hashes. Define exact current distributable membership separately so a sanitised export cannot masquerade as the original. Portable public validation must not require access to private originals.

Acceptance: tests first for the changed manifest contract. Require original/derivative distinction, exact hashes/dimensions/bytes, missing/unknown/unreviewed derivative rejection, no accidental private-path or source-image inclusion, complete public link/platform reachability and unchanged operation/budget safeguards. Require flattened-output metadata inspection and independent visual privacy review. Both existing commands must pass under the deliberately migrated contract. Remaining package blockers remain explicitly blocked.

### B5. Fill the already-routed Files dialog catalog gap

Finding: F9.

Targets: Android forms catalog, supporting index and the additive canonical-membership/original-mapping documentation, checker and tests. Keep the existing runtime row and two stored captures. A new supporting heading is justified by the distinct single-field dialog, but the current images' input-toolbar/capture occlusion must be stated.

Acceptance: if applied alone, catalog membership increases from forty to forty-one deliberately, while all original forty remain traceable. Tests must fail for missing original headings, missing new membership, broken links and platform misrouting. Both commands and manual occlusion review are required. Do not claim a clean settled screenshot or validation outcome that was not captured. Defer this batch if the owner requires clean canonical imagery first.

### B6. Admit the smallest useful additional control set

Findings: prioritise F10, then F11 and F12. F14–F16 are optional bounded variations, not reasons to import every Settings page.

Choose exact source IDs and settle rights/provenance first. Potential representatives are E006 for Android continuous intensity and E055 for iOS slider/switch anatomy. E052 is a separate preview-choice mechanism. Do not import E001 and E006 together by default, or infer a comparison pair from unrelated stills. All required privacy work depends on B4. Unknown versions remain explicit.

Targets after approval: selected derivative assets/manifests, detailed supporting control entries and index, concise existing editing references, checker/tests for the exact new membership. The owner must choose the heading plan for iOS slider and switch mechanisms before the forty-heading contract is changed. Do not use a generic grouping heading merely to evade the contract change.

Acceptance: focused tests for additive headings and exact asset counts/hashes/bytes/dimensions, complete legacy preservation, local link closure and platform-correct reachability. Manual appearance review, no claimed interaction/semantics without evidence, and verified conditional loading. Recheck the three representative read budgets without raising them. Both existing commands must pass.

## Capture backlog, only when a design question warrants it

1. C1. Obtain a clean Files Browse-root closed/open-menu pair if invoker alignment or transition continuity matters. Existing R071/R072 cannot answer that specific comparison. Preserve the current historical pair rather than replacing its identity.
2. C2. Capture the iOS Contacts discard prompt itself with authorised synthetic data if its anatomy is required. The recorded action path is already established. A new still is needed only for the missing appearance and alternate-action context.
3. C3. Capture Settings focused-empty search if that precise state is required. Existing resting, queried and cleared states are not substitutes.
4. C4. Capture an unoccluded Files single-field dialog if it will become a canonical visual example. Retain action/log context and avoid committing a persistent folder solely to prove layout.
5. C5. Resolve loading or incomplete credential candidates with a bounded action/wait/result record only if needed. E048 and E062 do not establish a loading lifecycle or input mechanism. Never enter or expose a real credential for screenshot evidence.
6. C6. Use a controlled safe environment for required validation, error-recovery, save/send or permission-result questions, with explicit side-effect approval. Pair action/result captures with exact semantic evidence where relevant. Accessibility testing needs focus order, spoken output and target interaction, not more stills alone.
7. C7. Recapture quantitative dashboards with approved non-personal data only if the capacity/activity summary solves a concrete design gap. Do not mask the evidence away and then claim the remaining geometry proves the original information design.

## Final handoff and approval boundary

`final-verification.json` records source-preservation checks, final git state and repeated validation results. `citation-checks.json` records repository path/anchor checks and ledger ID closure. The private folder and its artifacts must not be committed, uploaded or bundled into the skill.

No implementation, sanitisation, cache cleanup, source relocation, package publication or git-history operation is authorised by this audit. Recommended next approval: B0 for the narrowly enumerated runtime cache disposition, then B1 for the three-file routing correction. Approve B4 separately before any source-to-derivative work.

### Final verification result

[Observed] All 268 inventoried source files retain their baseline hashes. All 157 image hashes are unchanged. Git status, HEAD, branch, worktree and diff match the baseline. The repeated checker still exits 1 on the same unexpected runtime cache. The repeated regression command exits 0 with 14 tests passed. All 90 cited repository paths/anchors exist, and finding-to-image ledger references close. No completion claim is made for package validation or publication readiness.
