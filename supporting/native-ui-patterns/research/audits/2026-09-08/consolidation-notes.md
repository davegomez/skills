# Consolidation notes

## Baseline (recorded before analysis, 2026-09-08)

Run from the repository root:

```
python3 supporting/native-ui-patterns/check_skill.py
native-ui-patterns check: FAIL
- unexpected runtime path: assets/android/.DS_Store
exit 1

python3 supporting/native-ui-patterns/test_check_skill.py
Ran 14 tests in 1.022s
OK
exit 0
```

The checker failure is a Finder metadata file inside the runtime asset tree, not a content regression. It was not fixed during this audit. Running the tests created `supporting/native-ui-patterns/__pycache__/` (untracked); it was left in place. `git status` was otherwise clean at start.

## Validator contract that any implementation batch must respect

- `EXPECTED_SCREENSHOTS = (93, 33_473_851)`: exact PNG count and byte total in the runtime asset tree. Any new capture changes both constants and needs a new row in `screenshot-map.tsv` (original_path, runtime_path, sha256, width, height, bytes).
- Runtime PNGs must be byte-unique, PNG format (JPEG is rejected by header check), and linked from at least one table row (`| ... |`) in a same-platform reference under `references/<platform>/`.
- `archived_patterns()` must find exactly 40 `## ` headings across `docs/<platform>/*.md`, and `README.md`'s original pattern mapping table must list exactly those headings. Any new catalog section changes the 40 and needs a mapping row.
- Word budgets: iOS edit form (SKILL + ios/editing) 1,400; Android no-results (SKILL + android/search) 1,300; cross-platform peer navigation (SKILL + both navigation files) 1,700.
- SKILL.md frontmatter description and several guard phrases are pinned by string checks.
- The routing table must contain exactly the 12 existing references; a new operation row must reuse an existing file or the constant `EXPECTED_ROUTES` must change.

## Corpus environment (from the screenshots themselves)

- iOS: 44 PNG, 1206x2622. Status bar shows cellular, Wi-Fi, battery 90. Light appearance. Signed-in Apple Account with populated Family, subscriptions, devices. S-I12 (Device Info) shows "iPhone 17 Pro", "iOS 27.0". Capture times 16:58 to 17:06 in sequential IMG_4293..IMG_4336 order.
- Android: 20 JPEG, 1000x2244. Dark theme. Signed-in Google account (avatar row on root). S-A15 says the device is visible as "Pixel 10". OS version is not visible; unknown. File mtimes are identical, so capture order is unknown; UUID filenames carry no order.
- Both sets are the platform Settings application only. No other application appears.

## Worker plan

14 workers, model sonnet, general-purpose subagent, read-only. Groups keep sequences together (root -> account -> personal info; storage list -> scrolled -> app detail; Wi-Fi list -> join sheet; Display & touch -> HDR detail; Internet -> network details / join). See `screenshot-ledger.tsv` for the assignment of every file.

## Merge map (worker finding -> consolidated finding)

W01: F01->F025, F02->F025, F03->F014+F012, F04->F024, F05->F004, F06->F013, F07->F007, F08->F004
W02: F01->F004, F02->F007+F025, F03->F014, F04->F015, F05->F025, F06->F025, F07->F018, F08->F011, F09->A01 (F012 note), F10->F015, F11->A02
W03: F01->F012, F02->F005, F03->F001, F04->F006, F05->F012, F06->F008, F07->F009, F08->F025, F09->F004
W04: F01->F009, F02->F001, F03->F021, F04->F024; app-specific spinner->F019
W05: F01->F017, F02->F017, F03->F016, F04->F020, F05->F018, F06->F011, F07->F012, F08->F015, F09->F026, F10->F004+F025, F11->F008; artist rows->A06; Size sort->F015/U04
W06: F01->F009, F02->A04, F03->F011, F04->F007+F008, F05->F019, F06->F005 (chevron-only row noted under F004)
W07: F01->F001, F02->F023 (+F014 Edit), F03->F007, F04->F025, F05->F019, F06->F008, F07->F009, F08->F007, F09->F006 (+A05)
W08: F01->F003, F02->F002, F03->F014, F04->F010, F05->F007, F06->A03, F07->F013
W09: F01->F003, F02->F001, F03->F002, F04->F025, F05->F004, F06->F005, F07->F014
W10: F01->F017, F02->F007, F03->F008, F04->F001, F05->F005, F06->F022, F07->F009, F08->F024
W11: F01->F042, F03->F033, F04->F027, F05->F033, F06->F033, F07->F032, F08->F033, F09->F028, F10->F030, F11->F030, F12->F030, F13->F041, F14->F036
W12: F01->F029, F02->F039, F03->F039, F04->F038, F05->F035, F06->F027+F028, F08->F041; Modes rows uncertain->F033
W13: F01->A07, F02->A07 (+F033 trailing-control note), F03->F035, F04->F037, F05->F038, F06->F037, F07->F027, F08->F034
W14: F01->F031, F02->F035, F03->F038, F04->F033, F05->F034, F06->F034, F07->F040, F08->F040, F09->F041

## Corrections applied

- W01 "stale Wallet back label" on S-I01: not present (orchestrator crop). Dropped.
- W03 "centered title duplicates General": wrong. general.png has no bar title (W01, W08, orchestrator crop). Reclassified as F014.
- W11 cited paths for S-A05/S-A14/S-A15 were swapped. Ledger paths are authoritative.
- W04 "Other Networks" spinner app-specific: merged with CarPlay spinner into F019.
- W11 "back arrow + title" duplicate of Semantic labels: that entry documents content-desc only. Reclassified into F031.
- W13 mislabeled S-A11 "See all" leading icon as overflow-style; the crop reads as a vertical three-dot glyph. Kept as described; the icon identity does not change the finding.

## Orchestrator verification opens

- assets/ios/settings/general.png (top crop): back circle, no bar title, hero card "General".
- S-I01 top crop: no app back label.
- S-I15 top and bottom crops: card sheet with rounded top and bottom corners over a dimmed strip; X leading; dimmed checkmark trailing.
- S-I42 top crop: same sheet framing; X only.
