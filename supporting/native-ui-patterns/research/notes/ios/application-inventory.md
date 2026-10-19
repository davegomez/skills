# iOS 27 application inventory

## Inspection environment

- [Observed] Device: iPhone 17 Pro, UDID `C4E8218D-BF55-4FC3-B421-68FD02401D89`.
- [Observed] Runtime: iOS 27.0, build `24A5423a`, runtime identifier `com.apple.CoreSimulator.SimRuntime.iOS-27-0`.
- [Observed] Appearance and content size at the end of inspection: Light and Large.
- [Observed] Installed-app inventory came from `xcrun simctl listapps` on the booted device.

## Available and directly inspected

| Requested app | Bundle identifier | Accessible surface observed | Evidence |
|---|---|---|---|
| Settings | `com.apple.Preferences` | [Observed] Root, General detail, grouped rows, Search. | [root](../../../../../skills/native-ui-patterns/assets/ios/settings/root.png), [General](../../../../../skills/native-ui-patterns/assets/ios/settings/general.png) |
| Messages | `com.apple.MobileSMS` | [Observed] Conversation list and one sample conversation/composer; nothing sent. | [list](../../../../../skills/native-ui-patterns/assets/ios/messages/conversation-list.png), [conversation](../../../../../skills/native-ui-patterns/assets/ios/messages/conversation-empty-composer.png) |
| Calendar | `com.apple.mobilecal` | [Observed] What’s New, day view, location prompt, empty event form; nothing saved. | [intro](../../../../../skills/native-ui-patterns/assets/ios/calendar/whats-new.png), [day](../../../../../skills/native-ui-patterns/assets/ios/calendar/day-location-permission.png), [form](../../../../../skills/native-ui-patterns/assets/ios/calendar/event-form.png) |
| Contacts | `com.apple.MobileAddressBook` | [Observed] Sample list, John Appleseed detail, edit form; nothing saved or deleted. | [list](../../../../../skills/native-ui-patterns/assets/ios/contacts/contact-list.png), [detail](../../../../../skills/native-ui-patterns/assets/ios/contacts/contact-detail.png), [edit](../../../../../skills/native-ui-patterns/assets/ios/contacts/edit-form.png) |
| Photos | `com.apple.mobileslideshow` | [Observed] What’s New, six-sample-photo Library, notification prompt; no media changed. | [intro](../../../../../skills/native-ui-patterns/assets/ios/photos/whats-new.png), [library](../../../../../skills/native-ui-patterns/assets/ios/photos/library-notification-permission.png) |
| Maps | `com.apple.Maps` | [Observed] Initial location permission prompt over the first-run surface only. | [permission](../../../../../skills/native-ui-patterns/assets/ios/maps/location-permission.png) |
| Reminders | `com.apple.reminders` | [Observed] Welcome screen and iCloud-sync prompt over the root; no reminder created. | [intro](../../../../../skills/native-ui-patterns/assets/ios/reminders/welcome.png), [prompt](../../../../../skills/native-ui-patterns/assets/ios/reminders/icloud-sync-prompt.png) |
| Files | `com.apple.DocumentsApp` | [Observed] Recents, Browse/On My iPhone, locations/tags, More menu; no file changed. | [Recents](../../../../../skills/native-ui-patterns/assets/ios/files/recents-empty.png), [Browse](../../../../../skills/native-ui-patterns/assets/ios/files/browse.png), [menu](../../../../../skills/native-ui-patterns/assets/ios/files/more-menu.png) |
| Safari | `com.apple.mobilesafari` | [Observed] Start Page and bottom browser controls only; no URL opened. | [Start Page](../../../../../skills/native-ui-patterns/assets/ios/safari/start-page.png) |
| Health | `com.apple.Health` | [Observed] First welcome screen only. | [welcome](../../../../../skills/native-ui-patterns/assets/ios/health/welcome.png) |
| Wallet | `com.apple.Passbook` | [Observed] Root surface behind its location prompt; permission was refused and no pass/payment flow opened. | [permission](../../../../../skills/native-ui-patterns/assets/ios/wallet/location-permission.png) |
| Shortcuts | `com.apple.shortcuts` | [Observed] Empty All Shortcuts root and empty selection mode; nothing created. | [root](../../../../../skills/native-ui-patterns/assets/ios/shortcuts/empty-library.png), [selection](../../../../../skills/native-ui-patterns/assets/ios/shortcuts/empty-selection-mode.png) |

## Requested apps unavailable in this Simulator

- [Observed] App Store, Mail, Camera, Notes, Phone, FaceTime, Clock, Weather, Music, Podcasts, and Find My were absent from this device’s `simctl listapps` output.
- [Observed] No launch or UI claim was made for those eleven apps.
- [Observed] A third-party `dev.davidgomez.notetaker` app named Note Taker was present but was not treated as Apple Notes and was not launched.

## Coverage boundary

- [Observed] 12 of 23 requested Apple apps were available and launched.
- [Observed] 23 PNG screenshots were captured with `simctl io ... screenshot` after observed states.
- [Unconfirmed] Gestures, animated transitions, destructive confirmations, VoiceOver, Dynamic Type variants, and many deeper app flows were not completed within the bounded run.
- [Unconfirmed] Account-dependent, network-dependent, purchase, sending, calling, and device-hardware surfaces were not exercised.
