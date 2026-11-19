# I01 preflight

Run by hand on 2026-11-18. Xcode 27.3 (27C5020n), iOS SDK 27.3, simulator "eval-i01i02" (iPhone 15 Pro, iOS 27.3), deleted afterwards.

## Commands

Each variant: copy `fixture/` to a fresh folder, `git init`, 1 commit, `git apply` the patch (none for the fixture), then grade.

```sh
mkwork() { rm -rf "$2"; mkdir -p "$2"; cp -R I01/fixture/. "$2/"; (cd "$2" && git init -q && git add -A && git commit -q --allow-empty -m fixture && { [ -z "${3:-}" ] || git apply "$3"; }); }
export EVAL_SIM=<udid>
mkwork I01/fixture w-fixture                              && I01/hidden/grade.sh w-fixture res-fixture.json
mkwork I01/fixture w-refA I01/reference.patch             && I01/hidden/grade.sh w-refA res-refA.json
mkwork I01/fixture w-refB I01/reference.patch             && I01/hidden/grade.sh w-refB res-refB.json
for p in I01/negative/*.patch; do mkwork I01/fixture w-$(basename $p .patch) $p && I01/hidden/grade.sh w-$(basename $p .patch) res-$(basename $p .patch).json; done
diff <(jq -c .checks res-refA.json) <(jq -c .checks res-refB.json) && echo identical
```

## Output (`id result evidence`, evidence cut at 140 characters)

```text
== fixture exit=0 seconds=0
  I01-builds fail  no Xcode workspace or project within 3 levels of the folder root
  I01-app-target-settings fail  no build: no Xcode workspace or project within 3 levels of the folder root
  I01-profile-facts fail  no build: no Xcode workspace or project within 3 levels of the folder root
  I01-privacy-manifest fail  no build: no Xcode workspace or project within 3 levels of the folder root
  I01-unit-tests-pass fail  no build: no Xcode workspace or project within 3 levels of the folder root
  I01-add-and-toggle fail  no build: no Xcode workspace or project within 3 levels of the folder root
  I01-state-survives-relaunch fail  no build: no Xcode workspace or project within 3 levels of the folder root
  I01-list-accessibility-audit fail  no build: no Xcode workspace or project within 3 levels of the folder root
== refA exit=0 seconds=78
  I01-builds pass  xcodebuild build -scheme PackingList succeeded; app PackingList.app
  I01-app-target-settings pass  SWIFT_VERSION=6.0 SWIFT_DEFAULT_ACTOR_ISOLATION=MainActor
  I01-profile-facts pass  IPHONEOS_DEPLOYMENT_TARGET=27.3 PRODUCT_BUNDLE_IDENTIFIER=com.example.eval.PackingList.debug
  I01-privacy-manifest pass  PackingList.app/PrivacyInfo.xcprivacy is a valid plist with NSPrivacyTracking
  I01-unit-tests-pass pass  14 unit tests outside the scaffold bundles ran; 0 unit tests failed
  I01-add-and-toggle pass  XCUITest testAddAndToggle() passed
  I01-state-survives-relaunch pass  XCUITest testStateSurvivesRelaunch() passed
  I01-list-accessibility-audit pass  XCUITest testListScreenAccessibilityAudit() passed
== refB exit=0 seconds=74
  I01-builds pass  xcodebuild build -scheme PackingList succeeded; app PackingList.app
  I01-app-target-settings pass  SWIFT_VERSION=6.0 SWIFT_DEFAULT_ACTOR_ISOLATION=MainActor
  I01-profile-facts pass  IPHONEOS_DEPLOYMENT_TARGET=27.3 PRODUCT_BUNDLE_IDENTIFIER=com.example.eval.PackingList.debug
  I01-privacy-manifest pass  PackingList.app/PrivacyInfo.xcprivacy is a valid plist with NSPrivacyTracking
  I01-unit-tests-pass pass  14 unit tests outside the scaffold bundles ran; 0 unit tests failed
  I01-add-and-toggle pass  XCUITest testAddAndToggle() passed
  I01-state-survives-relaunch pass  XCUITest testStateSurvivesRelaunch() passed
  I01-list-accessibility-audit pass  XCUITest testListScreenAccessibilityAudit() passed
== I01-add-and-toggle exit=0 seconds=92
  I01-builds pass  xcodebuild build -scheme PackingList succeeded; app PackingList.app
  I01-app-target-settings pass  SWIFT_VERSION=6.0 SWIFT_DEFAULT_ACTOR_ISOLATION=MainActor
  I01-profile-facts pass  IPHONEOS_DEPLOYMENT_TARGET=27.3 PRODUCT_BUNDLE_IDENTIFIER=com.example.eval.PackingList.debug
  I01-privacy-manifest pass  PackingList.app/PrivacyInfo.xcprivacy is a valid plist with NSPrivacyTracking
  I01-unit-tests-pass fail  0 unit tests outside the scaffold bundles ran; 0 unit tests failed; ** TEST SUCCEEDED ** 
  I01-add-and-toggle fail  XCUITest testAddAndToggle(): Failed. XCTAssertTrue failed - no text field labelled 'Item name' on the first screen
  I01-state-survives-relaunch fail  XCUITest testStateSurvivesRelaunch(): Failed. XCTAssertTrue failed - no text field labelled 'Item name' on the first screen
  I01-list-accessibility-audit fail  XCUITest testListScreenAccessibilityAudit(): Failed. XCTAssertTrue failed - no text field labelled 'Item name' on the first screen
== I01-app-target-settings exit=0 seconds=81
  I01-builds pass  xcodebuild build -scheme PackingList succeeded; app PackingList.app
  I01-app-target-settings fail  SWIFT_VERSION=5.0 SWIFT_DEFAULT_ACTOR_ISOLATION=MainActor
  I01-profile-facts pass  IPHONEOS_DEPLOYMENT_TARGET=27.3 PRODUCT_BUNDLE_IDENTIFIER=com.example.eval.PackingList.debug
  I01-privacy-manifest pass  PackingList.app/PrivacyInfo.xcprivacy is a valid plist with NSPrivacyTracking
  I01-unit-tests-pass pass  14 unit tests outside the scaffold bundles ran; 0 unit tests failed
  I01-add-and-toggle pass  XCUITest testAddAndToggle() passed
  I01-state-survives-relaunch pass  XCUITest testStateSurvivesRelaunch() passed
  I01-list-accessibility-audit pass  XCUITest testListScreenAccessibilityAudit() passed
== I01-list-accessibility-audit exit=0 seconds=86
  I01-builds pass  xcodebuild build -scheme PackingList succeeded; app PackingList.app
  I01-app-target-settings pass  SWIFT_VERSION=6.0 SWIFT_DEFAULT_ACTOR_ISOLATION=MainActor
  I01-profile-facts pass  IPHONEOS_DEPLOYMENT_TARGET=27.3 PRODUCT_BUNDLE_IDENTIFIER=com.example.eval.PackingList.debug
  I01-privacy-manifest pass  PackingList.app/PrivacyInfo.xcprivacy is a valid plist with NSPrivacyTracking
  I01-unit-tests-pass pass  14 unit tests outside the scaffold bundles ran; 0 unit tests failed
  I01-add-and-toggle pass  XCUITest testAddAndToggle() passed
  I01-state-survives-relaunch pass  XCUITest testStateSurvivesRelaunch() passed
  I01-list-accessibility-audit fail  XCUITest testListScreenAccessibilityAudit(): Failed. Contrast nearly passed
== I01-privacy-manifest exit=0 seconds=74
  I01-builds pass  xcodebuild build -scheme PackingList succeeded; app PackingList.app
  I01-app-target-settings pass  SWIFT_VERSION=6.0 SWIFT_DEFAULT_ACTOR_ISOLATION=MainActor
  I01-profile-facts pass  IPHONEOS_DEPLOYMENT_TARGET=27.3 PRODUCT_BUNDLE_IDENTIFIER=com.example.eval.PackingList.debug
  I01-privacy-manifest fail  no valid PrivacyInfo.xcprivacy with NSPrivacyTracking at the root of PackingList.app
  I01-unit-tests-pass pass  14 unit tests outside the scaffold bundles ran; 0 unit tests failed
  I01-add-and-toggle pass  XCUITest testAddAndToggle() passed
  I01-state-survives-relaunch pass  XCUITest testStateSurvivesRelaunch() passed
  I01-list-accessibility-audit pass  XCUITest testListScreenAccessibilityAudit() passed
== I01-state-survives-relaunch exit=0 seconds=86
  I01-builds pass  xcodebuild build -scheme PackingList succeeded; app PackingList.app
  I01-app-target-settings pass  SWIFT_VERSION=6.0 SWIFT_DEFAULT_ACTOR_ISOLATION=MainActor
  I01-profile-facts pass  IPHONEOS_DEPLOYMENT_TARGET=27.3 PRODUCT_BUNDLE_IDENTIFIER=com.example.eval.PackingList.debug
  I01-privacy-manifest pass  PackingList.app/PrivacyInfo.xcprivacy is a valid plist with NSPrivacyTracking
  I01-unit-tests-pass pass  14 unit tests outside the scaffold bundles ran; 0 unit tests failed
  I01-add-and-toggle pass  XCUITest testAddAndToggle() passed
  I01-state-survives-relaunch fail  XCUITest testStateSurvivesRelaunch(): Failed. XCTAssertTrue failed - Passport is missing after relaunch
  I01-list-accessibility-audit pass  XCUITest testListScreenAccessibilityAudit() passed
$ diff <(jq -c .checks res-refA.json) <(jq -c .checks res-refB.json) && echo identical
identical
```

## Results

1. Fixture alone fails the case-critical checks: yes, 8 of 8 fail (no project).
2. Fixture plus `reference.patch` passes every check: yes, 8 of 8, in both runs.
3. Each negative fails the check its name names: yes, all 5.
4. Two reference runs in a row give the same result: yes, byte-identical check arrays.

Extra: the list audit test alone on a fresh install (no earlier test state), 2 runs:

```text
$ xcodebuild test -project runner/EvalUITests.xcodeproj -scheme EvalUITests -only-testing:EvalUITests/PackingListUITests/testListScreenAccessibilityAudit ...
audit-only fresh install run1: Passed
audit-only fresh install run2: Passed
```
