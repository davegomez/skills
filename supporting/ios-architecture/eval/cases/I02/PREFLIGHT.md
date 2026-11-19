# I02 preflight

Run by hand on 2026-11-18. Xcode 27.3 (27C5020n), iOS SDK 27.3, simulator "eval-i01i02" (iPhone 15 Pro, iOS 27.3), deleted afterwards.

## Commands

Each variant: copy `fixture/` to a fresh folder, `git init`, 1 commit, `git apply` the patch (none for the fixture), then grade.

```sh
mkwork() { rm -rf "$2"; mkdir -p "$2"; cp -R I02/fixture/. "$2/"; (cd "$2" && git init -q && git add -A && git commit -q --allow-empty -m fixture && { [ -z "${3:-}" ] || git apply "$3"; }); }
export EVAL_SIM=<udid>
mkwork I02/fixture w-fixture                              && I02/hidden/grade.sh w-fixture res-fixture.json
mkwork I02/fixture w-refA I02/reference.patch             && I02/hidden/grade.sh w-refA res-refA.json
mkwork I02/fixture w-refB I02/reference.patch             && I02/hidden/grade.sh w-refB res-refB.json
for p in I02/negative/*.patch; do mkwork I02/fixture w-$(basename $p .patch) $p && I02/hidden/grade.sh w-$(basename $p .patch) res-$(basename $p .patch).json; done
diff <(jq -c .checks res-refA.json) <(jq -c .checks res-refB.json) && echo identical
```

## Output (`id result evidence`, evidence cut at 140 characters)

```text
== fixture exit=0 seconds=108
  I02-builds pass  xcodebuild build -scheme Storefront succeeded; app Storefront.app
  I02-adjacent-code-unchanged pass  Packages/Core Packages/DesignSystem Packages/Networking Packages/Persistence are identical to the fixture
  I02-test-plan-runs-new-tests fail  0 tests not in the fixture ran in the Storefront test action; 0 of them failed
  I02-reachable-exactly-once fail  XCUITest testEntryReachableExactlyOnce(): Failed. XCTAssertEqual failed: ("0") is not equal to ("1") - want exactly 1 'Order summary' entry 
  I02-totals-match-spec fail  XCUITest testSampleOrderTotals(): Failed. XCTUnwrap failed: expected non-nil value of type "XCUIElement" - no 'Order summary' entry on the f
  I02-empty-state fail  XCUITest testEmptyState(): Failed. XCTUnwrap failed: expected non-nil value of type "XCUIElement" - no 'Order summary' entry on the first sc
  I02-error-state fail  XCUITest testErrorState(): Failed. XCTUnwrap failed: expected non-nil value of type "XCUIElement" - no 'Order summary' entry on the first sc
== refA exit=0 seconds=64
  I02-builds pass  xcodebuild build -scheme Storefront succeeded; app Storefront.app
  I02-adjacent-code-unchanged pass  Packages/Core Packages/DesignSystem Packages/Networking Packages/Persistence are identical to the fixture
  I02-test-plan-runs-new-tests pass  12 tests not in the fixture ran in the Storefront test action; 0 of them failed; failed fixture tests (not graded): AccessibilityAuditTests/
  I02-reachable-exactly-once pass  XCUITest testEntryReachableExactlyOnce() passed
  I02-totals-match-spec pass  XCUITest testSampleOrderTotals() passed
  I02-empty-state pass  XCUITest testEmptyState() passed
  I02-error-state pass  XCUITest testErrorState() passed
== refB exit=0 seconds=63
  I02-builds pass  xcodebuild build -scheme Storefront succeeded; app Storefront.app
  I02-adjacent-code-unchanged pass  Packages/Core Packages/DesignSystem Packages/Networking Packages/Persistence are identical to the fixture
  I02-test-plan-runs-new-tests pass  12 tests not in the fixture ran in the Storefront test action; 0 of them failed; failed fixture tests (not graded): AccessibilityAuditTests/
  I02-reachable-exactly-once pass  XCUITest testEntryReachableExactlyOnce() passed
  I02-totals-match-spec pass  XCUITest testSampleOrderTotals() passed
  I02-empty-state pass  XCUITest testEmptyState() passed
  I02-error-state pass  XCUITest testErrorState() passed
== I02-adjacent-code-unchanged exit=0 seconds=62
  I02-builds pass  xcodebuild build -scheme Storefront succeeded; app Storefront.app
  I02-adjacent-code-unchanged fail  changed: Packages/Core; Only in Packages/Core/Sources/CoreClients: OrderClient.swift 
  I02-test-plan-runs-new-tests pass  12 tests not in the fixture ran in the Storefront test action; 0 of them failed; failed fixture tests (not graded): AccessibilityAuditTests/
  I02-reachable-exactly-once pass  XCUITest testEntryReachableExactlyOnce() passed
  I02-totals-match-spec pass  XCUITest testSampleOrderTotals() passed
  I02-empty-state pass  XCUITest testEmptyState() passed
  I02-error-state pass  XCUITest testErrorState() passed
== I02-error-state exit=0 seconds=77
  I02-builds pass  xcodebuild build -scheme Storefront succeeded; app Storefront.app
  I02-adjacent-code-unchanged pass  Packages/Core Packages/DesignSystem Packages/Networking Packages/Persistence are identical to the fixture
  I02-test-plan-runs-new-tests fail  12 tests not in the fixture ran in the Storefront test action; 1 of them failed: failureShowsTheErrorStateAndRetryLoadsAgain(); failed fixtu
  I02-reachable-exactly-once pass  XCUITest testEntryReachableExactlyOnce() passed
  I02-totals-match-spec pass  XCUITest testSampleOrderTotals() passed
  I02-empty-state pass  XCUITest testEmptyState() passed
  I02-error-state fail  XCUITest testErrorState(): Failed. XCTAssertTrue failed - no 'We couldn't load your order.' message
== I02-reachable-exactly-once exit=0 seconds=109
  I02-builds pass  xcodebuild build -scheme Storefront succeeded; app Storefront.app
  I02-adjacent-code-unchanged pass  Packages/Core Packages/DesignSystem Packages/Networking Packages/Persistence are identical to the fixture
  I02-test-plan-runs-new-tests pass  12 tests not in the fixture ran in the Storefront test action; 0 of them failed
  I02-reachable-exactly-once fail  XCUITest testEntryReachableExactlyOnce(): Failed. XCTAssertEqual failed: ("0") is not equal to ("1") - want exactly 1 'Order summary' entry 
  I02-totals-match-spec fail  XCUITest testSampleOrderTotals(): Failed. XCTUnwrap failed: expected non-nil value of type "XCUIElement" - no 'Order summary' entry on the f
  I02-empty-state fail  XCUITest testEmptyState(): Failed. XCTUnwrap failed: expected non-nil value of type "XCUIElement" - no 'Order summary' entry on the first sc
  I02-error-state fail  XCUITest testErrorState(): Failed. XCTUnwrap failed: expected non-nil value of type "XCUIElement" - no 'Order summary' entry on the first sc
== I02-test-plan-runs-new-tests exit=0 seconds=61
  I02-builds pass  xcodebuild build -scheme Storefront succeeded; app Storefront.app
  I02-adjacent-code-unchanged pass  Packages/Core Packages/DesignSystem Packages/Networking Packages/Persistence are identical to the fixture
  I02-test-plan-runs-new-tests fail  0 tests not in the fixture ran in the Storefront test action; 0 of them failed; failed fixture tests (not graded): AccessibilityAuditTests/t
  I02-reachable-exactly-once pass  XCUITest testEntryReachableExactlyOnce() passed
  I02-totals-match-spec pass  XCUITest testSampleOrderTotals() passed
  I02-empty-state pass  XCUITest testEmptyState() passed
  I02-error-state pass  XCUITest testErrorState() passed
== I02-totals-match-spec exit=0 seconds=69
  I02-builds pass  xcodebuild build -scheme Storefront succeeded; app Storefront.app
  I02-adjacent-code-unchanged pass  Packages/Core Packages/DesignSystem Packages/Networking Packages/Persistence are identical to the fixture
  I02-test-plan-runs-new-tests fail  12 tests not in the fixture ran in the Storefront test action; 3 of them failed: sampleOrderTotals(), taxRoundsHalfUp(subtotal:tax:), sample
  I02-reachable-exactly-once pass  XCUITest testEntryReachableExactlyOnce() passed
  I02-totals-match-spec fail  XCUITest testSampleOrderTotals(): Failed. XCTAssertTrue failed - order.tax shows 'Tax (8.25%), $3.46 ', want $3.47
  I02-empty-state pass  XCUITest testEmptyState() passed
  I02-error-state pass  XCUITest testErrorState() passed
$ diff <(jq -c .checks res-refA.json) <(jq -c .checks res-refB.json) && echo identical
identical
```

## Results

1. Fixture alone fails the case-critical checks: yes, the 5 behavior checks fail; I02-builds and I02-adjacent-code-unchanged pass, as they must for an untouched fixture.
2. Fixture plus `reference.patch` passes every check: yes, 7 of 7, in both runs.
3. Each negative fails the check its name names: yes, all 5.
4. Two reference runs in a row give the same result: yes, byte-identical check arrays.
