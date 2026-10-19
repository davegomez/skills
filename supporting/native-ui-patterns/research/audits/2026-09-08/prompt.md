# Audit new screenshots for additions to native-ui-patterns

## Objective and authority

Audit the screenshots under:

the owner's capture folder (outside the repository at the time)

Use these screenshots to find UI and UX patterns that should be added to, expanded within, or better represented by the existing `native-ui-patterns` skill.

**The new screenshot directory is the discovery corpus for this audit.**

Do not search the repository's existing screenshot corpus for additional missing patterns.

Use existing repository screenshots and documentation only when needed to:

- Understand current coverage.
- Find the closest existing pattern.
- Detect duplicates.
- Compare an existing documented variation.
- Decide how a candidate should integrate with the skill.
- Confirm that a proposed addition is genuinely new or meaningfully different.

Do not generate findings merely by reviewing existing screenshots.

Every proposed `new-pattern`, `existing-pattern-variation`, or `existing-pattern-improvement` must originate from evidence found in the owner's capture folder (outside the repository at the time).

Treat missing coverage as a hypothesis to investigate, not a quota to fill.

This run produces an audit and proposed changes only.

Stop for my approval before changing the skill, catalog, source evidence, mapping, validator, or tests.

Propose small implementation batches for a later run.

---

## Inputs and output

Repository:

the repository root

Primary screenshot corpus:

the owner's capture folder (outside the repository at the time)

Review the screenshot directory recursively.

Every supported finding must trace back to at least one screenshot from this directory.

Write the audit and worker artifacts to a new directory under the system Desktop folder.

Use:

`native-ui-patterns-audit-<timestamp>`

Include:

- `audit.md`
- A machine-readable screenshot ledger.
- A machine-readable findings ledger.
- Individual worker reports.
- Consolidation notes when useful.

Do not modify repository files during this audit.

---

# 1. Establish the existing skill contract

Before analyzing the new screenshots, understand enough of the existing skill to classify new evidence correctly.

Read the repository's `AGENTS.md` and applicable pointers.

Inspect:

- `skills/native-ui-patterns/SKILL.md`
- All platform operation references used by that skill.
- `supporting/native-ui-patterns/README.md`
- `supporting/native-ui-patterns/docs/README.md`
- The platform catalog files it indexes.
- `supporting/native-ui-patterns/research/limitations.md`
- `supporting/native-ui-patterns/research/coverage.md`
- `supporting/native-ui-patterns/research/uncertain-findings.md`
- `supporting/native-ui-patterns/screenshot-map.tsv`
- `supporting/native-ui-patterns/check_skill.py`
- `supporting/native-ui-patterns/test_check_skill.py`

Consult existing observation logs, application inventories, Android hierarchy dumps, comparison documents, or original screenshots only when a candidate finding requires them.

Do not systematically re-review the existing screenshot corpus.

The existing corpus is reference material, not an audit target.

Preserve these architectural distinctions:

- The runtime is a compact, operation-routed skill.
- The supporting catalog contains detailed visual documentation and provenance.
- Runtime files must remain self-contained.
- Visual routes should select useful evidence instead of becoming a general screenshot gallery.
- Text-only requests should continue to avoid loading screenshots unnecessarily.

Run from the repository root:

```sh
python3 supporting/native-ui-patterns/check_skill.py
python3 supporting/native-ui-patterns/test_check_skill.py
```

Record both exit codes before analysis.

Preserve unrelated working-tree changes.

Report baseline failures without fixing them.

### Completion condition

Before screenshot analysis starts, the orchestrator must understand:

- The current taxonomy.
- Existing runtime operations.
- Existing catalog coverage.
- Integration boundaries.
- Baseline validation status.

Do not spend this phase searching for new patterns.

---

# 2. Inventory only the new screenshot corpus

Recursively inventory:

the owner's capture folder (outside the repository at the time)

Assign one stable screenshot ID to every file.

Record at least:

- Screenshot ID.
- Source path.
- Platform when identifiable.
- Application when identifiable.
- Dimensions.
- Capture sequence or related-screen group when identifiable.
- Assigned worker.
- Review status.

Unknown values must remain unknown.

Do not infer device or OS metadata from the existing repository corpus.

Group screenshots that clearly represent the same interaction sequence.

Examples include:

- Before and after opening a control.
- Collapsed and expanded states.
- List and detail screens from the same workflow.
- Default and selected states.
- Sequential steps of the same form.
- Related modal presentation states.

Keep these sequences together when delegating work.

### Completion condition

Every screenshot under the owner's capture folder (outside the repository at the time) must have:

- A stable ID.
- An assignment group.
- A worker owner.

Do this before the full visual review begins.

---

# 3. Fan out screenshot analysis aggressively

Use multiple read-only visual subagents.

Do not limit delegation to one iOS worker and one Android worker.

Do not create only two broad platform assignments unless the entire new corpus contains too few screenshots to justify more workers.

Prefer many bounded screenshot assignments that can run independently.

## Assignment strategy

Partition the new screenshots using this priority:

1. Keep interaction sequences together.
2. Group screenshots from the same application and nearby workflow when practical.
3. Divide large application groups into separate capture sequences.
4. Balance the number and complexity of screenshots across workers.
5. Avoid overlapping screenshot ownership.

A worker should normally inspect a small, focused batch rather than an entire platform.

For a substantial screenshot corpus, target approximately:

- 2–5 screenshots per worker for visually dense or unrelated captures.
- 7–10 screenshots per worker for simple related sequences.

These are guidelines, not strict limits.

Use enough parallel workers to cover independent groups efficiently.

If the environment supports substantial concurrency and the corpus justifies it, prefer several workers running concurrently rather than 2 large workers.

## Minimum delegation expectation

If there are enough independent screenshot groups, use at least 4 workers.

For a large corpus, use more.

Do not artificially cap delegation at 4.

The orchestrator should primarily coordinate, review, deduplicate, and integrate findings rather than perform most first-pass screenshot inspection itself.

## Model choice

Use a faster available model for first-pass screenshot analysis when it:

- Supports visual inspection.
- Can follow the required finding schema.
- Is appropriate for the task.

Reserve stronger or slower reasoning for:

- Ambiguous classifications.
- Conflicting worker findings.
- Deduplication.
- Taxonomy decisions.
- Integration planning.

## Worker context

Each worker receives:

- Its exact screenshot IDs.
- Their source paths.
- Relevant existing catalog sections when already known.
- The classification rules below.
- The visual-analysis requirements below.

Do not ask workers to audit unrelated existing screenshots.

A worker may inspect existing documentation or a specific existing screenshot only to answer:

> Is the pattern in my assigned new screenshot already covered?

Workers must return their findings in separate artifacts.

### Completion condition

Every new screenshot must receive a visual inspection result.

Count separately:

- Reviewed.
- Unsupported format.
- Failed to open.
- Otherwise blocked.

---

# 4. Inspect the new screenshots visually

Open every assigned screenshot.

Do not classify a screenshot from:

- Its filename alone.
- OCR alone.
- Folder names alone.
- Existing documentation alone.
- Hierarchy data alone.

Use the full-resolution image when a reduced preview hides relevant details.

A screenshot can support several UI patterns.

Several screenshots can support one pattern.

Do not force one finding per screenshot.

For each screenshot, identify useful visible structures such as:

- Navigation.
- Toolbars.
- Forms.
- Input controls.
- Selection controls.
- Lists.
- Rows.
- Cards.
- Menus.
- Contextual actions.
- Sheets.
- Dialogs.
- Overlays.
- Search interfaces.
- Filters.
- Empty states.
- Loading states.
- Error states.
- Status presentation.
- Inline actions.
- Buttons.
- Floating actions.
- Icon usage.
- Content hierarchy.
- Editing states.
- Account interfaces.
- Settings patterns.
- Media presentation.
- Confirmation interfaces.
- Keyboard-related layout.
- Other reusable platform-native patterns.

Do not restrict analysis to this list.

Look for patterns that another agent would need to understand when designing a native-feeling interface.

---

# 5. Compare every candidate against existing coverage

After a worker identifies a candidate in a new screenshot, inspect the existing skill and supporting catalog for the closest coverage.

Classify each candidate as:

- `new-pattern`
- `existing-pattern-variation`
- `existing-pattern-improvement`
- `duplicate`
- `application-specific`
- `uncertain`

## new-pattern

Use when the new screenshot contains a distinct and useful reusable pattern that the skill does not currently document.

## existing-pattern-variation

Use when the general pattern exists, but the new screenshot demonstrates a design-relevant variation that the current documentation does not represent adequately.

Examples include:

- Compact versus expanded presentation.
- Anchored versus full-width presentation.
- Inline versus modal selection.
- Leading versus trailing controls.
- Single-line versus multi-line structures.
- Different hierarchy for destructive actions.
- Different presentation for editing mode.

## existing-pattern-improvement

Use when the new screenshot exposes a weakness in an existing entry.

Examples include:

- The description is visually incomplete.
- Important anatomy is missing.
- Existing wording is too broad.
- Existing wording is too narrow.
- A useful state is absent.
- Runtime routing could select a better visual example.

## duplicate

Use when the existing documentation already explains the visual and UX concept adequately.

Cite the exact existing entry.

Do not propose a change only because the new screenshot is another example.

## application-specific

Use when the evidence is useful but does not support a reusable platform pattern.

Do not generalize branded or highly specialized application presentation.

## uncertain

Use when the screenshot does not provide enough evidence for a confident classification.

Record what is missing.

---

# 6. Keep discovery anchored to the new screenshots

This is a critical audit rule.

Existing screenshots may confirm, contradict, or contextualize a candidate.

They must not independently create candidates.

A finding is in scope only when at least one screenshot from:

the owner's capture folder (outside the repository at the time)

led to that finding.

Do not:

- Browse the existing 93-image corpus looking for undocumented patterns.
- Create improvements based only on existing screenshots.
- Turn the audit into another exhaustive review of the original research.
- Assign workers to inspect old screenshots without a specific new-screenshot candidate to compare.
- Count old screenshots as part of the review completion target.

When an existing screenshot reveals something interesting while checking a candidate, do not expand the scope.

Record it separately as an optional future audit note if necessary.

The current task remains focused on the supplied new screenshots.

---

# 7. Use evidence-bounded claims

Use the project's claim labels:

- **Observed**
- **Inferred**
- **Unconfirmed**

## Observed

Use for appearance directly visible in an inspected screenshot.

Also use for behavior directly exercised and recorded in an existing local observation log.

## Inferred

Use for bounded interpretation or design guidance derived from the evidence.

## Unconfirmed

Use for behavior or details not established by available evidence.

A still screenshot can establish visual appearance.

A still screenshot does not establish:

- Activation behavior.
- Dismissal behavior.
- Gestures.
- Animation.
- Focus order.
- Screen-reader output.
- Hit targets.
- Implementation APIs.
- Transition timing.

Do not turn plausible behavior into an observed claim.

If behavioral evidence exists in an existing observation log, cite it separately.

---

# 8. Produce visually precise descriptions

The main value of this audit is not only naming patterns.

Descriptions must allow another agent to understand the visual idea without seeing the source application.

Avoid descriptions such as:

- "Standard settings row."
- "Typical native sheet."
- "Normal form field."
- "iOS-style menu."
- "Android-style card."

Describe the actual anatomy.

When relevant, include:

- Position within the screen.
- Relationship to navigation.
- Width relative to the container.
- Horizontal and vertical alignment.
- Grouping.
- Containers.
- Background treatment.
- Section boundaries.
- Typography hierarchy.
- Primary and secondary text placement.
- Leading icons.
- Trailing icons.
- Control placement.
- Dividers.
- Corner treatment.
- Scrims.
- Selection indicators.
- Action hierarchy.
- State indicators.
- Relationship to nearby content.
- Relationship to the keyboard.
- Visible scrolling context.
- Overlay position.
- Dismissal affordances visible in the screenshot.

Prefer relative relationships.

Do not invent exact platform measurements.

If measurements are useful, measure the original raster and label the values as image pixels.

Do not convert raster pixels into:

- iOS points.
- Android dp.
- Font metrics.
- Safe-area values.
- Device-independent geometry.

unless those values have independent evidence.

---

# 9. Worker finding format

Give every candidate a stable finding ID.

Examples:

`F001`

`F002`

`F003`

For every actionable finding, record:

| Field                     | Required content                                                                                              |
| ------------------------- | ------------------------------------------------------------------------------------------------------------- |
| Identity                  | Pattern name, platform, classification, existing category, and proposed runtime operation.                    |
| Source                    | New screenshot IDs from the owner's capture folder (outside the repository at the time) that caused the finding.                          |
| Scope                     | Application and visible screen context when identifiable.                                                     |
| UX problem                | The reusable user or design problem the pattern addresses. Label design interpretation as Inferred.           |
| Current coverage          | Exact existing catalog/runtime entry or explicit absence.                                                     |
| Gap                       | Explain what the new screenshot adds and why the existing coverage is insufficient.                           |
| Visual structure          | Precise description of layout, hierarchy, controls, icons, containers, spacing relationships, and state cues. |
| Interaction               | Only behavior established by evidence. Mark unsupported behavior Unconfirmed.                                 |
| States                    | Visible states and any relevant existing documented states.                                                   |
| Variations                | Meaningful design variations represented by the new evidence.                                                 |
| Evidence                  | Screenshot IDs, source paths, relevant regions, and the specific observation each image supports.             |
| Existing evidence checked | Existing entries or screenshots inspected solely for comparison or deduplication.                             |
| Integration               | Proposed catalog change and concise runtime guidance when useful.                                             |
| Confidence                | `high`, `medium`, or `low`, with the reason.                                                                  |
| Priority                  | Why this addition or improvement is useful to an agent using the skill.                                       |

The `Source` field must contain at least one screenshot from the new screenshot directory for every actionable finding.

---

# 10. Consolidate worker results

The primary orchestrator owns final classification.

Do not concatenate worker reports and treat that as the final audit.

After workers finish:

1. Collect all candidate findings.
2. Group candidates describing the same underlying pattern.
3. Search the existing skill for the closest current coverage.
4. Resolve duplicates.
5. Resolve conflicting classifications.
6. Reopen new screenshots when visual evidence is ambiguous.
7. Inspect existing evidence only where comparison requires it.
8. Normalize terminology.
9. Check platform scope.
10. Check application scope.
11. Check claim labels.
12. Check that every actionable finding originates from the new screenshot directory.
13. Rank the surviving findings by usefulness.

When 2 workers identify the same pattern from different screenshots, consolidate the evidence into one finding.

Do not create separate entries merely because:

- Different applications use the pattern.
- Several screenshots show different content.
- Multiple workers discovered it independently.

Preserve separate variations when they affect a real design decision.

---

# 11. Audit output

Produce:

`audit.md`

and machine-readable ledgers for screenshots and findings.

The report must contain the following sections.

## Scope and baseline

Include:

- Repository reviewed.
- New screenshot directory reviewed.
- Baseline validation results.
- Number of new screenshots discovered.
- Number successfully inspected.
- Number blocked or failed.

Do not include existing repository screenshots in the inspected screenshot total.

## Delegation summary

Include:

- Number of workers used.
- Screenshot groups assigned to each worker.
- Number of screenshots assigned to each.
- Failed or incomplete assignments.
- Reassignments when applicable.

This section should make under-delegation visible.

## Candidate totals

After consolidation, report counts for:

- `new-pattern`
- `existing-pattern-variation`
- `existing-pattern-improvement`
- `duplicate`
- `application-specific`
- `uncertain`

## Proposed new patterns

Include all accepted `new-pattern` findings.

## Proposed variations

Include all accepted `existing-pattern-variation` findings.

## Existing pattern improvements

Include all accepted `existing-pattern-improvement` findings.

## Duplicates

List rejected candidates and their matching existing entries.

## Application-specific findings

Record useful evidence that should not become general platform guidance.

## Uncertain findings

Record unsupported or ambiguous candidates and the evidence needed to resolve them.

## Future capture backlog

Record useful gaps exposed by the new screenshots that cannot be documented with current evidence.

For each backlog item, identify:

- Platform.
- Application or workflow when known.
- Required state.
- Claim the additional capture or interaction would establish.

Do not use the backlog as permission to audit old screenshots for unrelated missing coverage.

---

# 12. Propose implementation batches

Group accepted findings into small implementation batches.

Each batch should identify:

- Finding IDs.
- Catalog files affected.
- Runtime references affected.
- Screenshot mapping changes.
- Validator changes if necessary.
- Test changes if necessary.
- Expected benefit.
- Acceptance checks.

Prefer coherent batches instead of one large change.

For example:

- A batch for 3 related iOS presentation patterns.
- A batch for Android list/action variations.
- A batch for runtime routing improvements.
- A batch for new visual evidence and mapping changes.

Do not implement these batches during this run.

---

# 13. Preserve existing architecture

Do not use this audit as a reason to redesign the skill.

Retain the existing model:

- Compact skill entry point.
- Operation-routed runtime references.
- Detailed supporting catalog.
- Conditional visual loading.
- Explicit mapping between documentation and evidence.
- Validation of the package contract.

New screenshots should improve the existing architecture rather than bypass it.

Prefer one strong representative visual for a documented state when several screenshots communicate the same idea.

A screenshot may support multiple operations or catalog entries when appropriate.

Do not duplicate an image solely because several patterns refer to it.

---

# 14. Final quality gate

Before handing back the audit, confirm:

- Every screenshot in the owner's capture folder (outside the repository at the time) has a final review status.
- Every actionable finding originates from at least one new screenshot.
- Existing screenshots did not independently generate findings.
- Every candidate has been checked against existing coverage.
- Duplicate findings have been consolidated.
- iOS and Android remain independently scoped.
- Application-specific observations are labeled correctly.
- Visual descriptions explain the actual anatomy.
- Static screenshots are not used to invent behavior.
- Finding IDs and screenshot IDs resolve correctly.
- Ledger totals match the report totals.
- Worker assignments cover the complete new screenshot corpus.
- Independent screenshot groups were delegated across several workers when the corpus size allowed it.
- Existing validation commands and any later required regression checks are identified.

End with:

1. The report path.
2. The screenshot ledger path.
3. The findings ledger path.
4. The number of screenshots reviewed.
5. The number of workers used.
6. The highest-value proposed implementation batch.
7. Any blockers.
8. The approval required to proceed.

Make no skill, catalog, screenshot mapping, validator, test, or evidence changes during this run.
