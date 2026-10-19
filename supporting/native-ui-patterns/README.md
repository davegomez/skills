# Native UI patterns development archive

This directory preserves the pre-conversion catalog, research, and development checks. The runtime now holds 109 PNG files: the 93 original PNG byte streams plus 16 imported from the 2026-09-08 set. The 93 original PNG byte streams were relocated exactly once to `skills/native-ui-patterns/assets/<platform>/<application>/<state>.png`; catalog and research links now point there. [`screenshot-map.tsv`](screenshot-map.tsv) is the development-only old-path → runtime-path, SHA256, PNG-dimension, and byte-count record. All 57 Android UI Automator XML dumps and archive `.DS_Store` files remain here; the three pre-expansion runtime `.DS_Store` files moved to `preserved-runtime-metadata/` so runtime contains no metadata caches. Supporting documentation may depend on runtime evidence; the runtime never depends on supporting material.

A second capture set, taken on 2026-09-08, covers Settings on one signed-in physical iPhone 17 Pro and one signed-in physical Pixel 10. Its 20 original Android JPEG byte streams are retained unchanged in [`research/notes/android/captures-2026-09-08/`](research/notes/android/captures-2026-09-08/), and the [capture note](research/notes/captures-2026-09-08.md) records the SHA256, dimensions, and byte count of all 64 originals. Later batches import the selected captures into `skills/native-ui-patterns/assets/<platform>/settings/` under state-named file names, decoding each Android JPEG losslessly to PNG; until a batch imports a capture, the runtime does not contain it. The iOS captures that wait for their batch are kept in [`research/notes/ios/captures-2026-09-08/`](research/notes/ios/captures-2026-09-08/); a batch moves its file from there into the runtime, so no capture exists twice. The audit that selected the captures, its findings and screenshot ledgers, its batch plan, and the redaction tool are archived in [`research/audits/2026-09-08/`](research/audits/2026-09-08/audit.md).

## Validate

From the repository root:

```sh
python3 supporting/native-ui-patterns/check_skill.py
```

Run the checker’s focused regressions:

```sh
python3 supporting/native-ui-patterns/test_check_skill.py
```

To prove mapped screenshots and raw non-image evidence are preserved against a pre-migration supporting snapshot (or the older original corpus):

```sh
python3 supporting/native-ui-patterns/check_skill.py \
  --baseline /path/to/pre-migration/supporting/native-ui-patterns \
  --runtime-baseline /path/to/pre-expansion/runtime/native-ui-patterns
```

The stdlib-only check enforces the exact runtime file set, approved frontmatter and 12 direct routes, local link/anchor closure, allowed dependency direction, and representative text-read budgets. It verifies exactly 109 byte-unique PNGs against the mapping’s hashes, headers, dimensions, and byte counts; platform-correct conditional visual routes for every capture; no supporting PNG outside the pending iOS originals folder, and no pending original that duplicates a runtime PNG; all 47 pattern mappings; 57 XML dumps; and optional baseline preservation. Regression tests exercise duplicate, missing, changed, malformed, unreachable, wrong-platform, and broken/external-link failures plus the visual-versus-text loading instructions. These string checks validate the package contract, not agent behavior.

## Provenance and maintenance

The original searchable catalog starts at [docs/README.md](docs/README.md). Evidence scope and curator boundaries live in [research/limitations.md](research/limitations.md), with coverage, uncertain findings, observation logs, inventories, and dumps beside them. Historical observation claims remain scoped to their original runs; only storage links and maintenance notes changed for relocation.

When evidence changes, retain raw capture/log bytes, update the catalog and affected operation reference, then update the single screenshot mapping and run both validations. Keep runtime references operation-specific and task-conditional so a visual task opens one matched overview plus relevant state variants, not a global gallery. Store each capture once by platform/application/state; multiple operation references may link the same file.

## Original pattern mapping

Every original catalog section maps to at least one runtime operation file. A source pattern can contribute a bounded variation to another operation (for example, centered empty state to Search), but this table names its primary home.

| Original pattern | Runtime operation |
| --- | --- |
| `Large-title hierarchy` | iOS navigation |
| `Floating bottom navigation dock` | iOS navigation |
| `Full-screen task surface` | iOS editing |
| `Grouped form rows` | iOS editing |
| `Search field with dictation affordance` | iOS search |
| `System permission alert` | iOS onboarding and permissions |
| `Add and remove rows (application-specific)` | iOS editing |
| `Content-gated commit control` | iOS editing |
| `Switch row` | iOS editing |
| `Inline slider row` | iOS editing |
| `Visual option picker` | iOS editing |
| `Link-style action row` | iOS editing |
| `Destructive action row` | iOS editing |
| `Identity-led list row` | iOS content states |
| `Icon-led settings row` | iOS content states |
| `Label/value information rows` | iOS content states |
| `Centered empty state` | iOS content states; zero-results variation in iOS search |
| `Feature-introduction surface` | iOS onboarding and permissions |
| `Photo thumbnail grid (application-specific)` | iOS content states |
| `Time-grid day view (application-specific)` | iOS content states |
| `Explicit selection mode (application-specific)` | iOS content states |
| `Anchored overflow menu (application-specific)` | iOS navigation |
| `Immediate keyboard focus` | iOS editing |
| `Accessibility-labeled visible controls` | iOS accessibility |
| `Bottom navigation with selected destination` | Android navigation |
| `Search-led top surface` | Android search |
| `Contextual overlay menu` | Android navigation |
| `Navigation drawer` | Android navigation |
| `Draggable map content sheet` | Android navigation |
| `Trailing switch in a settings or list row` | Android editing and controls |
| `Labeled chip or compact filter control` | Android editing and controls |
| `Structured create-contact form` | Android editing and controls |
| `Recipient-first composition form` | Android editing and controls |
| `Modal time picker` | Android editing and controls |
| `Unsaved-change confirmation` | Android editing and controls |
| `Search focus mode with explicit exit` | Android search |
| `Semantic labels for icon-only actions` | Android accessibility |
| `Semantic selected and checked state` | Android accessibility |
| `System Back as non-committing exit` | Android navigation |
| `Drag gesture changes sheet position` | Android navigation |
| `Permission prompt boundary` | Android onboarding and permissions |
| `Grouped card list` | Android content states |
| `Illustrated empty state` | Android content states |
| `Query-specific no-results recovery` | Android search |
| `Floating primary action` | Android content states |
| `Sign-in or permission primer` | Android onboarding and permissions |
| `Visible selected and unchecked states` | Android content states |
