# Audit brief: iOS and iPadOS 27 kit images (2026-10-28)

You are one read-only audit worker. Your worker ID (`Wnn`) is in your spawn prompt.

## Context

The `native-ui-patterns` skill (`skills/native-ui-patterns/`) guides agents that design or review iOS and Android screens. It routes by operation to short reference files, and each file links settled-state screenshots of stock apps. The owner exported 378 PNG images from Apple's "iOS and iPadOS 27" Figma design kit to `/Users/dave/ui-patterns/ios-ipados/`. The kit shows canonical components and example screens with placeholder content ("Title", "Detail", "Tab 1"). It shows anatomy, variants, and device differences. It does not show behavior, real content, motion, or error flows.

The skill will gain a fourth evidence class, **Kit**: anatomy and variants shown in Apple's design kit. It will also gain these iOS reference files: `ios/controls.md` (controls move out of `ios/editing.md`), `ios/system-surfaces.md` (widgets, Lock Screen, notifications, Control Center controls, Home Screen quick actions, app icons), and `ios/foundations.md` (materials, Liquid Glass, color, text styles, Dynamic Type). iPad guidance goes into rows of the existing iOS files.

## Read first

1. `skills/native-ui-patterns/SKILL.md`
2. Every file in `skills/native-ui-patterns/references/ios/` (about 150 lines in total)
3. `supporting/native-ui-patterns/research/audits/2026-10-28/inventory.tsv`: your rows are the rows whose `worker` column is your ID. Paths are relative to `/Users/dave/ui-patterns/ios-ipados/`.

## Work

Open every one of your images with the Read tool, at its absolute path. A row with a `duplicate_of` value is byte-identical to that row: record `duplicate` and skip a second look. To judge supersession, you may open existing iOS runtime captures under `skills/native-ui-patterns/assets/ios/`. Open no other kit images.

Write exactly 2 files and change nothing else:

### `workers/Wnn.tsv`

Header and 1 row per inventory row of yours, tab-separated, no tabs or newlines inside a field:

`id	path	shows	disposition	target	supersedes	visual_question	facts	reason`

- `shows`: 1 sentence on what is visible.
- `disposition`, one of:
  - `import`: the image answers a visual question the skill lacks and belongs in the runtime.
  - `update`: the image answers the same visual question as an existing runtime capture with the same or better information; name that capture in `supersedes`.
  - `reference`: the image gives facts for the text guidance, but another image of the same pattern is the better runtime asset.
  - `reject`: no value for the skill (a fragment, background, swatch, bezel, or near-duplicate); give the reason.
  - `duplicate`: byte-identical to `duplicate_of`.
- `target`: the reference file the image or its facts belong to (`ios/navigation.md`, `ios/search.md`, `ios/editing.md`, `ios/controls.md`, `ios/content-states.md`, `ios/onboarding-permissions.md`, `ios/accessibility.md`, `ios/system-surfaces.md`, `ios/foundations.md`), or `none`.
- `supersedes`: a runtime path such as `assets/ios/settings/brightness-slider.png`, or empty. Supersede a stock-app capture only when the kit image answers the same question at least as well. A real capture of a state the kit lacks (errors, permission prompts, no results, discard, real content) is never superseded.
- `visual_question`: for `import` and `update`, the one question a designer opens this image to answer.
- `facts`: compact kit facts a designer needs: anatomy, variants, states, placement, grouping, iPhone versus iPad difference, Light versus Dark difference. Image pixels only; never claim points or dp.
- `reason`: required for `reference` and `reject`.

### `workers/Wnn.md`

At most 60 lines, with these sections:

1. New patterns: each pattern the skill lacks, with the IDs that show it and its target file.
2. Corrections: each existing sentence in a reference file that your images contradict or sharpen. Quote the sentence and cite the IDs.
3. iPad differences.
4. Conflicts with existing captures: where a runtime capture and the kit differ, say which one looks newer and why.
5. Best runtime set: the smallest set of your IDs that answers every visual question your group raises.

## Done

You are done when `workers/Wnn.tsv` has exactly 1 row for each of your inventory rows, and every row has a disposition. Prove it with a command that compares the 2 ID sets, and quote its output. Keep the 2 files as your only writes.

Report in at most 150 words: the count per disposition, your 5 most important findings, and the proof output. End with `needs: none` or `needs: <role>, because <criterion>`.
