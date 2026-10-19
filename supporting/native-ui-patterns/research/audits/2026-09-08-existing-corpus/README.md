# Earlier audit run of the existing corpus (2026-09-08)

A separate session audited the 93 original captures and the runtime routing on 2026-09-08, before the audit of the new Settings captures in [`../2026-09-08/`](../2026-09-08/audit.md). This folder keeps that run's report and one patch. Its other artifacts (evidence ledger, findings JSON, worker outputs, harness, byte copies of runtime assets, and the rollback state) were deleted on 2026-09-09; they held no information that the report and the repository do not.

## What was verified afterwards

- The run flagged 21 existing captures as "requires sanitisation". Two of them were reopened on 2026-09-09: the flagged content is Apple's fictional sample contacts and a test recipient in the Emulator. The 21 flags are false positives. No existing asset was changed for privacy reasons.
- The run applied its B1 routing corrections to 3 iOS reference files and then rolled them back together with its stopped B4 privacy migration. The corrected rows are not in the tree. [`b14-routing-corrections.patch`](b14-routing-corrections.patch) holds only those rows over the current files; `git apply --check` passes. The main audit schedules it as B14, after B4, with the claims marked Unconfirmed until the 3 existing assets are reopened.
- Its B0 (runtime Finder cache files) is covered by the main audit's B0.
- Its B2, B3, B5, and B6 were not evaluated. They stay as candidates in the report.

## Files

- [`audit.md`](audit.md): the run's complete report: scope, baseline, ledger accounting, privacy claims (see above), findings F1 to F23, proposed batches B0 to B6, and the capture backlog. The index links inside it were turned into plain text so that the archive link check passes.
- [`b14-routing-corrections.patch`](b14-routing-corrections.patch): 6 changed lines across `references/ios/{search,navigation,content-states}.md`.
