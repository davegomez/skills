# Audit: iOS and iPadOS 27 kit images (2026-10-28)

## Scope

The owner exported 378 PNG images from Apple's "iOS and iPadOS 27" Figma design kit. The audit decided, for each image, whether it belongs in the `native-ui-patterns` runtime, gives facts for the text guidance, or has no value. The kit shows anatomy and variants with placeholder content; it shows no behavior. The images are Apple Design Resources under Apple's licence, kept in this repository by the owner's decision of 2026-10-28.

## Method

1. [`inventory.tsv`](inventory.tsv) lists every image with its id (`K001`–`K378`), exported path, SHA256, dimensions, byte count, and, for byte-identical copies, `duplicate_of`.
2. 11 read-only workers (`W01`–`W11`) each received one slice of the inventory and the brief in [`prompt.md`](prompt.md). Each worker opened every image in its slice, compared it with the existing iOS runtime captures, and wrote one ledger row per image (`workers/Wnn.tsv`) plus a findings note (`workers/Wnn.md`).
3. The merged ledgers were checked against the inventory: every id has exactly 1 row and 1 disposition.
4. [`selection.tsv`](selection.tsv) records the 63 images chosen for the runtime and their runtime paths.

## Dispositions

| Disposition | Count |
| --- | ---: |
| import | 129 |
| update | 3 |
| reference | 136 |
| reject | 102 |
| duplicate | 8 |
| **Total** | **378** |

The 102 rejects include all 11 product bezels. `W11` wrote 12 bezels in its report text; the ledger is correct.

## No capture was superseded

Workers proposed 3 updates. Each kit image lacks context that the stock-app capture has, so every capture stays:

- `K081` (empty states) versus `assets/ios/files/recents-empty.png`: the kit shows placeholder copy without the surrounding app navigation, title, and search field that the Files capture shows. `K081` is imported beside the capture, not in its place.
- `K093` (sliders) versus `assets/ios/settings/brightness-slider.png`: the kit shows slider positions on placeholder rows; the capture shows a real Settings slider with its glyphs and the rows around it.
- `K097` (switches) versus `assets/ios/settings/switch-dependent-rows.png`: the kit shows an on and an off switch; the capture shows the dependent rows and footer a switch reveals.

## Ledger repair

`W02` wrote the `K062` row twice on one line (14 fields), so the merge saw 377 rows. The second copy was kept, as it is consistent, and the merge now gives 378 rows.

## Selection rule

The 129 imports and 3 updates answer more visual questions than the runtime needs. The selection keeps 63, by these rules:

- One image per visual question.
- A whole example screen beats a component fragment, because it shows placement and surrounding content.
- Files over 1 MB are avoided; no selected image exceeds 1 MB.

The 63 selected images were copied byte-identically to `skills/native-ui-patterns/assets/ios/kit/`. Of the other 315, the 8 duplicate copies are not stored; `inventory.tsv` records them with `duplicate_of`. The remaining 307 were copied byte-identically, with their exported folder structure and names, to [`research/notes/ios/kit-27/`](../../notes/ios/kit-27/). No inventory image is stored in both places; `check_skill.py` enforces this against the two ledgers.

## Known defects in the kit

- `K091` (`examples/iphone/Picker.png`): the left phone's weekday header reads SUN MON WED THU FRI SAT SUN.
- `K356`, `K363`, `K364` (Lock Screen widget exports): blank.
