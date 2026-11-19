# I03 preflight

Run by hand on 2026-11-18. Xcode 27.3 (27C5020n), simulator `eval-i03i04` (iPhone 17 Pro, iOS 27.3), `EVAL_SIM=B7CBA66D-C98B-4517-9C8D-384C384513EA`.

Each run:

```sh
w=$(mktemp -d); cp -R fixture/. "$w/"
(cd "$w" && git init -q && git add -A && git commit -qm fixture && git apply <patch>)   # no apply for the fixture run
EVAL_SIM=$EVAL_SIM hidden/grade.sh "$w" <label>.json
```

`grade.sh` printed nothing and exited 0 on every run. Output tails are the result lines of each JSON.

## 1. Fixture alone fails the case-critical checks: PASS

```
== fixture (grade.sh exit 0, 53s)
  pass I03-build | xcodebuild build-for-testing succeeded
  fail I03-valid-link-confirmation | XCUITest testValidLinkShowsConfirmation failed: Failed to open the default app for a URL: The operation couldn’t be completed. (LSApplicationWorkspaceErrorDomain error 115.)
  fail I03-malformed-link-rejected | XCUITest testMalformedAndUnknownLinksAreRejected failed: Failed to open the default app for a URL: ...
  fail I03-link-needs-confirmation | XCUITest testLinkAloneDoesNotChangeState failed: Failed to open the default app for a URL: ...
  fail I03-cancel-keeps-data | XCUITest testCancelKeepsData failed: Failed to open the default app for a URL: ...
  fail I03-confirm-archives-once | XCUITest testConfirmArchivesExactlyOnce failed: Failed to open the default app for a URL: ...
  fail I03-existing-navigation | XCUITest testExistingNavigationStillWorks failed: Failed to open the default app for a URL: ...
  fail I03-preview-accessibility-audit | XCUITest testPreviewPassesAccessibilityAudit failed: Failed to open the default app for a URL: ...
```

## 2. Fixture plus reference.patch passes every check: PASS

```
== reference-1 (grade.sh exit 0, 179s)
  pass I03-build | xcodebuild build-for-testing succeeded
  pass I03-valid-link-confirmation | XCUITest testValidLinkShowsConfirmation passed
  pass I03-malformed-link-rejected | XCUITest testMalformedAndUnknownLinksAreRejected passed
  pass I03-link-needs-confirmation | XCUITest testLinkAloneDoesNotChangeState passed
  pass I03-cancel-keeps-data | XCUITest testCancelKeepsData passed
  pass I03-confirm-archives-once | XCUITest testConfirmArchivesExactlyOnce passed
  pass I03-existing-navigation | XCUITest testExistingNavigationStillWorks passed
  pass I03-preview-accessibility-audit | XCUITest testPreviewPassesAccessibilityAudit passed
```

## 3. Each negative patch fails the check it names: PASS

```
== negative-I03-confirm-archives-once (grade.sh exit 0, 154s)
  fail I03-malformed-link-rejected | XCUITest testMalformedAndUnknownLinksAreRejected failed: XCTAssertFalse failed - preview appeared for quicknotes://notes/33333333-3333-3333-3333-333333333333/archive
  fail I03-confirm-archives-once | XCUITest testConfirmArchivesExactlyOnce failed: XCTAssertFalse failed - preview appeared for an archived note
  (other 6 checks pass)
== negative-I03-link-needs-confirmation (grade.sh exit 0, 185s)
  fail I03-link-needs-confirmation | XCUITest testLinkAloneDoesNotChangeState failed: XCTAssertTrue failed - the link changed data without a confirmation
  (other 7 checks pass)
== negative-I03-malformed-link-rejected (grade.sh exit 0, 123s)
  fail I03-malformed-link-rejected | XCUITest testMalformedAndUnknownLinksAreRejected failed: com.example.quicknotes crashed
  (other 7 checks pass)
```

## 4. Same result 2 times in a row on the reference: PASS

```
== reference-2 (grade.sh exit 0, 179s)
  (same 8 pass lines as reference-1)
$ cmp reference-1.json reference-2.json && echo identical
identical
```
