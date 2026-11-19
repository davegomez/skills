# I04 preflight

Run by hand on 2026-11-18. Xcode 27.3 (27C5020n), simulator `eval-i04-dev` (iPhone 17 Pro, iOS 27.3), `EVAL_SIM=D42ED757-6984-4307-AD3C-5D758D1B7DAD`. A second simulator let I04 run beside I03; both were deleted afterward.

Each run:

```sh
w=$(mktemp -d); cp -R fixture/. "$w/"
(cd "$w" && git init -q && git add -A && git commit -qm fixture && git apply <patch>)   # no apply for the fixture run
EVAL_SIM=$EVAL_SIM hidden/grade.sh "$w" <label>.json
```

`grade.sh` printed nothing and exited 0 on every run. Output tails are the result lines of each JSON.

## 1. Fixture alone fails the case-critical checks: PASS

The fixture already has the legacy behavior, so the behavior checks pass. The extraction checks fail.

```
== fixture (grade.sh exit 0, 169s)
  pass I04-build | xcodebuild build-for-testing succeeded
  pass I04-characterization | XCUITest testTotalsMatchLegacyBehavior passed
  pass I04-old-data-loads | XCUITest testLoadsCacheWrittenByOldVersion passed
  pass I04-ids-and-keys-unchanged | XCUITest testSavesCacheInLegacyFormat passed; bundle identifier com.example.ledger
  pass I04-interrupted-repeated-load | XCUITest testRecoversFromInterruptedCacheWrite, testRepeatedReloadDoesNotDuplicate passed
  pass I04-navigation-unchanged | XCUITest testNavigationUnchanged passed
  fail I04-package-extracted | no Package.swift in the result
  fail I04-domain-no-ui-import | no package target holds the totals logic
  pass I04-legacy-unchanged | 4 unrelated legacy files unchanged
```

## 2. Fixture plus reference.patch passes every check: PASS

```
== reference-1 (grade.sh exit 0, 173s)
  pass I04-build | xcodebuild build-for-testing succeeded
  pass I04-characterization | XCUITest testTotalsMatchLegacyBehavior passed
  pass I04-old-data-loads | XCUITest testLoadsCacheWrittenByOldVersion passed
  pass I04-ids-and-keys-unchanged | XCUITest testSavesCacheInLegacyFormat passed; bundle identifier com.example.ledger
  pass I04-interrupted-repeated-load | XCUITest testRecoversFromInterruptedCacheWrite, testRepeatedReloadDoesNotDuplicate passed
  pass I04-navigation-unchanged | XCUITest testNavigationUnchanged passed
  pass I04-package-extracted | local package(s) LedgerOrders; app imports OrdersData, OrdersDomain
  pass I04-domain-no-ui-import | totals target(s) OrdersDomain import no UI framework
  pass I04-legacy-unchanged | 4 unrelated legacy files unchanged
```

## 3. Each negative patch fails the check it names: PASS

```
== negative-I04-characterization (grade.sh exit 0, 158s)
  fail I04-characterization | XCUITest testTotalsMatchLegacyBehavior failed: ... - exactly at the threshold: orders.tax shows 'Tax $7.42', expected 'Tax $7.43'
  fail I04-interrupted-repeated-load | XCUITest testRecoversFromInterruptedCacheWrite failed: ... - online after a truncated cache: orders.tax shows 'Tax $7.42', expected 'Tax $7.43'
  (other 7 checks pass)
== negative-I04-domain-no-ui-import (grade.sh exit 0, 172s)
  fail I04-domain-no-ui-import | domain target imports UI: OrdersDomain imports UIKit
  (other 8 checks pass)
== negative-I04-interrupted-repeated-load (grade.sh exit 0, 169s)
  fail I04-interrupted-repeated-load | XCUITest testRepeatedReloadDoesNotDuplicate failed: ... - after 3 reloads: orders.subtotal shows 'Subtotal $599.88', expected 'Subtotal $149.97'
  (other 8 checks pass)
== negative-I04-legacy-unchanged (grade.sh exit 0, 171s)
  fail I04-legacy-unchanged | changed or removed: Ledger/SettingsViewController.swift
  (other 8 checks pass)
== negative-I04-old-data-loads (grade.sh exit 0, 185s)
  fail I04-old-data-loads | XCUITest testLoadsCacheWrittenByOldVersion failed: ... - offline with the old cache: orders.subtotal shows 'Subtotal $0.00', expected 'Subtotal $125.0
  (other 8 checks pass)
```

## 4. Same result 2 times in a row on the reference: PASS

```
== reference-2 (grade.sh exit 0, 174s)
  (same 9 pass lines as reference-1)
$ cmp reference-1.json reference-2.json && echo identical
identical
```
