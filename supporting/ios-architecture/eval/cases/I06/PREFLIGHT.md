# I06 preflight

Run by hand on 2026-11-18 with Xcode 27.3 (27C5020n), on a dedicated iPhone 17 Pro simulator running iOS 27.3 (created with `xcrun simctl create`, deleted afterwards). Each run takes about 3 minutes.

## Commands

```sh
cp -R fixture W && cd W && git init -q && git add -A && git commit -qm fixture
git apply <patch under test>              # reference.patch, a negative, or nothing
EVAL_SIM=<udid> hidden/grade.sh W out.json
```

## Results

| Step | Patch | Expected | Result |
| --- | --- | --- | --- |
| 1 | none | fails the case-critical checks | pass: 13 checks fail; `test-seam-intact`, `build`, and `token-not-in-preferences` pass |
| 2 | `reference.patch` | passes every check | pass: 16 of 16 |
| 3 | `negative/I06-offline-shows-cache.patch` | fails `I06-offline-shows-cache` | pass; `I06-second-locale` also fails (no Spanish offline notice) |
| 3 | `negative/I06-retry-cancel.patch` | fails `I06-retry-cancel` | pass: only that check fails |
| 3 | `negative/I06-retry-permanent-no-retry.patch` | fails `I06-retry-permanent-no-retry` | pass; `state-error`, `second-locale`, and `accessibility-audit` also fail |
| 3 | `negative/I06-second-locale.patch` | fails `I06-second-locale` | pass; `I06-strings-in-catalog` also fails |
| 3 | `negative/I06-token-not-in-logs.patch` | fails `I06-token-not-in-logs` | pass: only that check fails |
| 3 | `negative/I06-token-not-in-preferences.patch` | fails `I06-token-not-in-preferences` | pass; `I06-token-not-in-logs` also fails (1 line: the system logs the preference write inside the app process) |
| 4 | `reference.patch`, 2 runs in a row | identical results | pass: same results and same evidence text |

The first run of the permanent-retry negative ended with exit 143 because an outside process sent SIGTERM to `xcodebuild` while another agent's build ran on the same machine. The re-run is the one recorded here.

## Output tail

```
fixture exit=0
  I06-test-seam-intact=pass I06-build=pass I06-state-loading=fail I06-state-list=fail I06-state-empty=fail I06-state-error=fail I06-offline-shows-cache=fail I06-retry-transient-recovers=fail I06-retry-transient-limit=fail I06-retry-permanent-no-retry=fail I06-retry-cancel=fail I06-second-locale=fail I06-accessibility-audit=fail I06-token-not-in-logs=fail I06-token-not-in-preferences=pass I06-strings-in-catalog=fail
  fail I06-token-not-in-logs  no request observed (os_log requests: 0, console launches with a request: 0 of 3)
reference-1 exit=0
  all 16 checks pass; I06-token-not-in-logs: 0 token lines in os_log (32 requests) and 3 console captures
reference-2 exit=0
  identical to reference-1 (ids, results, evidence)
neg-I06-offline-shows-cache exit=0
  fail I06-offline-shows-cache  XCUITest testOfflineShowsCache: XCTAssertTrue failed - no offline state
  fail I06-second-locale        XCUITest testSecondLocale: XCTAssertTrue failed - offline text not in Spanish
neg-I06-retry-cancel exit=0
  fail I06-retry-cancel  XCUITest testRetryCancel passed, but the transport never saw the request cancelled
neg-I06-retry-permanent-no-retry (re-run) exit=0
  fail I06-state-error               XCUITest testStateError: XCTAssertTrue failed - no error state
  fail I06-retry-permanent-no-retry  XCUITest testRetryPermanentNoRetry: XCTAssertTrue failed - no error state
  fail I06-second-locale             XCUITest testSecondLocale: XCTAssertTrue failed - error text not in Spanish
  fail I06-accessibility-audit       XCUITest testAccessibilityAudit: XCTAssertTrue failed - permanent: state missing
neg-I06-second-locale exit=0
  fail I06-second-locale       XCUITest testSecondLocale: XCTAssertTrue failed - title not in Spanish
  fail I06-strings-in-catalog  no .xcstrings file has the Spanish title
neg-I06-token-not-in-logs exit=0
  fail I06-token-not-in-logs  token found in 5 captured log lines
neg-I06-token-not-in-preferences exit=0
  fail I06-token-not-in-logs         token found in 1 captured log lines
  fail I06-token-not-in-preferences  token found in 1 preferences file(s)
```
