# Android 17 direct observation log

## Session boundary

- [Observed] Direct inspection ran on 2026-09-06 using the local Android Emulator and ADB only.
- [Observed] AVD `pixel_a17` booted as `emulator-5554` with Android release 17/API 37.
- [Observed] Screenshots were captured with `adb exec-out screencap -p`; corresponding UI hierarchies were captured with `adb shell uiautomator dump` and are stored in [`ui-dumps/`](ui-dumps/).
- [Observed] Thirty-seven PNG captures and thirty-seven matching XML dumps remain after removal of duplicate or misleading captures.
- [Observed] The emulator had no signed-in Google account during inspection.

## Direct-inspection command set

[Observed] The audit used the following command forms; package and output names varied by app.

```sh
emulator @pixel_a17 -no-snapshot-save -no-audio
adb devices -l
adb shell getprop ro.build.version.release
adb shell getprop ro.build.version.sdk
adb shell getprop ro.build.fingerprint
adb shell wm size
adb shell wm density
adb shell pm list packages
adb shell pm path <package>
adb shell cmd package resolve-activity --brief <package>
adb shell dumpsys package <package>
adb shell am force-stop <package>
adb shell am start -a android.intent.action.MAIN -c android.intent.category.LAUNCHER -p <package>
adb shell am start -a android.settings.SETTINGS
adb shell input tap <x> <y>
adb shell input text <text>
adb shell input keyevent 3
adb shell input keyevent 4
adb shell input keyevent 66
adb shell input swipe 640 2150 640 650 600
adb exec-out screencap -p > <evidence-name>.png
adb shell uiautomator dump /sdcard/window.xml
adb pull /sdcard/window.xml <evidence-name>.xml
```

## Observations by app

### Settings

- [Observed] Launched with `android.settings.SETTINGS`.
- [Observed] Captured the category landing surface, entered `display` in Search Settings, and opened Display & touch.
- [Observed] Search exposed a leading back arrow, trailing clear action, categorized results, and a compact floating Gboard toolbar.
- [Observed] Display & touch exposed grouped rows and a Dark theme switch reported as `checkable="true"`, `checked="false"`, and `content-desc="Dark theme"`.

### Google Play Store

- [Observed] Launch resolved to `com.android.vending/.AssetBrowserActivity`.
- [Observed] The surface required Sign in to proceed to store content.
- [Observed] Sign in was not selected.

### Messages

- [Observed] Captured the empty conversation list, search categories, account sheet, and New chat recipient form.
- [Observed] Search categories included Unread, Known, Unknown, Starred, Images, Videos, Places, and Links.
- [Observed] The account sheet included Archived, Trash, Spam & blocked, Mark all as read, Device pairing, Messages settings, and Help & feedback.
- [Observed] Start chat opened a focused “To:” field; no recipient or message was entered.

### Gmail

- [Observed] Acknowledged the “New in Gmail” feature screen with GOT IT.
- [Observed] The following screen offered Add an email address and TAKE ME TO GMAIL, but no inbox became available without an address.
- [Observed] No account flow was started.

### Calendar

- [Observed] Launch first showed “Checking info…” and then the Google Accounts “Sign in with ease” screen.
- [Observed] No calendar grid or event form became reachable in the no-account state.

### Contacts

- [Observed] The Android notification permission dialog was shown; Don’t allow was selected.
- [Observed] The app then exposed Contacts and Organize bottom destinations and a “No contacts yet” empty state.
- [Observed] The add action opened Create contact. A temporary `Audit` first-name value was entered to inspect focus and unsaved-change behavior.
- [Observed] Back produced “Your changes have not been saved” with Discard and Save. Home was used to leave without selecting either action; no contact was saved.

### Photos

- [Observed] The Photos/Search shell was visible behind a dim layer.
- [Observed] A centered “Keep your memories safe” card required Sign in to proceed to the media library.
- [Observed] Sign in was not selected.

### Maps

- [Observed] Skip was selected on the sign-in onboarding screen.
- [Observed] The subsequent audio primer offered Continue and Not now; Not now was selected, and no audio permission dialog was invoked.
- [Observed] Explore, You, and Contribute bottom destinations were visible. Explore showed category controls including Restaurants, Hotels, Coffee, and Shopping.
- [Observed] An upward ADB swipe moved the Explore content sheet to an expanded position while preserving bottom navigation.
- [Observed] Search focus was entered, but no route, reservation, review, or contribution was created.

### Files

- [Observed] Launch resolved to `com.google.android.documentsui/com.android.documentsui.LauncherActivity`.
- [Observed] Downloads showed file-type controls, a list-layout control, and a “No items” empty state.
- [Observed] The top-left menu opened a drawer with Recent, Images, Videos, Audio, and Documents destinations.

### Chrome

- [Observed] Stay signed out was selected on Chrome onboarding.
- [Observed] No thanks was selected on the notification primer.
- [Observed] The new tab page exposed search, AI Mode, Incognito, shortcuts, and a Chrome tips card.
- [Observed] The overflow menu exposed New tab, New Incognito tab, Add tab to new group, History, Delete browsing data, Downloads, Bookmarks, Recent tabs, Settings, Customize new tab page, and Help & feedback.
- [Observed] Delete browsing data was not selected, and no URL was loaded.

### Phone

- [Observed] Captured Home with All/Missed/Contacts/Non-spam filters, empty call history, and Home/Keypad/Voicemail bottom navigation.
- [Observed] Captured the keypad with digits, star, hash, delete, and Call controls.
- [Observed] No digit was entered and no call was placed.

### Clock

- [Observed] Captured Clock and Alarm destinations.
- [Observed] Alarm contained two pre-existing disabled alarm cards at 8:30 AM and 9:00 AM; their UI nodes reported `checked="false"`.
- [Observed] Tapping add opened a time picker with graphical clock, AM/PM, keyboard mode, Cancel, and OK.
- [Observed] Back dismissed the picker; no alarm was created, edited, deleted, or toggled.

### Drive

- [Observed] Launch resolved to `com.google.android.apps.docs/.app.NewMainProxyActivity` and displayed Google Accounts setup.
- [Observed] No sign-in step was started, so file and detail surfaces were not reached.

### YouTube Music

- [Observed] Onboarding offered Sign in and Device files only.
- [Observed] Device files only opened an in-app explanation that media-file permission was required and exposed Allow.
- [Observed] Allow was not selected; media and player detail were not reached.

## Safety and evidence controls

- [Observed] No message, email, call, form, contact, alarm, route, review, contribution, purchase, download, upload, or sign-in was completed.
- [Observed] No app data was cleared and no persistent user data was deleted.
- [Observed] No permission was bypassed or pre-granted; Contacts notification access was declined, Maps audio access was deferred, and YouTube Music media access was left ungranted.
- [Observed] The Contacts unsaved-change dialog was inspected without choosing Save or Discard.
- [Observed] The Clock time picker was dismissed with Back without choosing OK.

## Gaps

- [Observed] Representative populated detail screens were unavailable in Messages, Contacts, Files, Gmail, Calendar, Drive, Photos, Play Store, and YouTube Music because the AVD had no content/account or the app required sign-in/permission.
- [Observed] No safe populated list supported meaningful multi-select inspection; selection mode is therefore unconfirmed.
- [Observed] No persistent-item deletion confirmation was exercised; only the safe unsaved Contacts form confirmation was inspected.
- [Observed] TalkBack traversal, spoken announcements, font scaling, contrast instrumentation, rotation, split screen, and external keyboard traversal were not tested.
- [Observed] Transition timing and easing were not measured; only pre/post settled states were captured.
- [Unconfirmed] Behavior on physical Android 17 devices, other form factors, signed-in accounts, populated datasets, and other app versions remains unconfirmed.
