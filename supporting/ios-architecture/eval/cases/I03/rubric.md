# I03 rubric

Checks for the blind reviewer. The hidden tests already settle link acceptance and rejection, the confirmation step, cancel, archiving once after a repeated link, existing navigation, and an accessibility audit of the preview. Grade each check `pass`, `fail`, `na`, or `unverified`, with file and line evidence.

| Check | Priority | Severity | Pass condition |
| --- | --- | --- | --- |
| I03-R1-validate-before-use | security | critical | The handler turns the URL into a typed value through 1 validating step that checks the scheme, host, path shape, and ID before any lookup or state change. Nothing force-unwraps or indexes link parts without a bounds check. |
| I03-R2-no-sensitive-logs | security | major | No new log, print, or analytics call records a note's title or body, or the raw link, with public privacy. |
| I03-R3-confirm-is-idempotent | reliability | major | Confirming cannot archive twice or undo an archive: the store operation sets the archived state rather than toggling it, or the confirm action cannot run twice. |
| I03-R4-preview-accessible | accessibility | major | The preview names the note and the action in text that VoiceOver reads. The confirm button states the action ("Archive"), not only "OK" or "Yes". Builder-chosen text colors meet contrast (the audit ignores system bar items and near-miss contrast). |
| I03-R5-tests-cover-link | reliability | minor | The change adds tests that cover a valid link and at least 1 malformed link and 1 unknown note ID. |
| I03-R6-scope | maintainability | minor | The change is limited to link registration, parsing, the preview, and the archive operation. It adds no dependency and does not restructure unrelated screens. |
