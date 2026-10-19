# iOS 27 direct observation log

## Method

- [Observed] All product evidence came from the local iOS 27.0 Simulator; no web source was used.
- [Observed] Apple apps were launched by installed bundle identifier with `xcrun simctl launch`.
- [Observed] Screenshots were captured only with `xcrun simctl io <UDID> screenshot <path>` after the displayed state was observed.
- [Observed] Safe taps used an ephemeral local XCTest UI runner and visible accessibility labels; the runner itself was not treated as product evidence.
- [Observed] No message was sent, event/reminder/shortcut created, contact/file/photo changed, account entered, purchase initiated, call placed, or permission granted.

## Direct-inspection commands

```sh
xcrun simctl list devices available
xcrun simctl list runtimes
xcrun simctl boot C4E8218D-BF55-4FC3-B421-68FD02401D89
open -a Simulator
xcrun simctl bootstatus C4E8218D-BF55-4FC3-B421-68FD02401D89 -b
xcrun simctl listapps C4E8218D-BF55-4FC3-B421-68FD02401D89
xcrun simctl launch C4E8218D-BF55-4FC3-B421-68FD02401D89 <apple-bundle-id>
xcrun simctl terminate C4E8218D-BF55-4FC3-B421-68FD02401D89 <apple-bundle-id>
xcrun simctl io C4E8218D-BF55-4FC3-B421-68FD02401D89 screenshot <png-path>
xcodebuild test -project <ephemeral-inspector-project> -scheme Inspector \
  -destination 'platform=iOS Simulator,id=C4E8218D-BF55-4FC3-B421-68FD02401D89' \
  -only-testing:InspectorUITests/InspectorUITests/<safe-test>
xcrun simctl ui C4E8218D-BF55-4FC3-B421-68FD02401D89 content_size
xcrun simctl ui C4E8218D-BF55-4FC3-B421-68FD02401D89 appearance
```

## Observation sequence

1. [Observed] Booted the available iPhone 17 Pro on iOS 27.0 build 24A5423a and waited for boot completion.
2. [Observed] Enumerated installed apps and matched the 12 requested Apple bundle identifiers listed in [application-inventory.md](application-inventory.md).
3. [Observed] Launched each available app and captured its first reachable state.
4. [Observed] A Maps location prompt remained above subsequently launched apps until Maps was terminated; affected interim captures were overwritten after the prompt was cleared.
5. [Observed] Wallet then presented its own location prompt; XCTest tapped the visible “Don’t Allow” action, and the test passed.
6. [Observed] Label-based XCTest actions successfully opened Settings General, John Appleseed detail/edit, Files Browse/More, a sample Messages conversation, Shortcuts selection, Calendar’s primary/event surfaces, Photos Library, and Reminders’ post-introduction prompt.
7. [Observed] Each successful resulting state was captured afterward with `simctl io screenshot`.
8. [Observed] Safari’s Start Page was captured without navigation or network activity.

## Automation results

- [Observed] 12 bounded UI tests passed: Wallet permission refusal, Settings General, Contacts detail, Contacts edit, Files Browse, Files More, Messages detail, Shortcuts selection, Calendar Continue, Calendar Add, Photos Continue, and Reminders Continue.
- [Observed] A label-query test for Safari’s address field failed to find the attempted label.
- [Observed] A later coordinate-based Safari focus run exceeded four minutes; the enclosing command was stopped and any remaining `xcodebuild` process was terminated.
- [Observed] No screenshot was produced for the hung Safari focus attempt, so no keyboard/focus claim for Safari is included.
- [Observed] macOS System Events could read the Simulator window geometry but was denied Assistive Access for clicking (`-25211`); no security permission was changed to work around that denial.
- [Unconfirmed] Edge-swipe navigation, contact delete confirmation, and Dynamic Type capture were queued after the Safari test and therefore did not execute.

## Screenshot set

- [Observed] Settings: [root](../../../../../skills/native-ui-patterns/assets/ios/settings/root.png), [General](../../../../../skills/native-ui-patterns/assets/ios/settings/general.png).
- [Observed] Messages: [list](../../../../../skills/native-ui-patterns/assets/ios/messages/conversation-list.png), [conversation](../../../../../skills/native-ui-patterns/assets/ios/messages/conversation-empty-composer.png).
- [Observed] Calendar: [introduction](../../../../../skills/native-ui-patterns/assets/ios/calendar/whats-new.png), [day/location prompt](../../../../../skills/native-ui-patterns/assets/ios/calendar/day-location-permission.png), [event form](../../../../../skills/native-ui-patterns/assets/ios/calendar/event-form.png).
- [Observed] Contacts: [list](../../../../../skills/native-ui-patterns/assets/ios/contacts/contact-list.png), [detail](../../../../../skills/native-ui-patterns/assets/ios/contacts/contact-detail.png), [edit form](../../../../../skills/native-ui-patterns/assets/ios/contacts/edit-form.png).
- [Observed] Files: [Recents](../../../../../skills/native-ui-patterns/assets/ios/files/recents-empty.png), [Browse](../../../../../skills/native-ui-patterns/assets/ios/files/browse.png), [More menu](../../../../../skills/native-ui-patterns/assets/ios/files/more-menu.png).
- [Observed] Photos: [introduction](../../../../../skills/native-ui-patterns/assets/ios/photos/whats-new.png), [Library/notification prompt](../../../../../skills/native-ui-patterns/assets/ios/photos/library-notification-permission.png).
- [Observed] Reminders: [introduction](../../../../../skills/native-ui-patterns/assets/ios/reminders/welcome.png), [sync prompt](../../../../../skills/native-ui-patterns/assets/ios/reminders/icloud-sync-prompt.png).
- [Observed] Shortcuts: [root](../../../../../skills/native-ui-patterns/assets/ios/shortcuts/empty-library.png), [selection](../../../../../skills/native-ui-patterns/assets/ios/shortcuts/empty-selection-mode.png).
- [Observed] Safari: [Start Page](../../../../../skills/native-ui-patterns/assets/ios/safari/start-page.png).
- [Observed] Health: [welcome](../../../../../skills/native-ui-patterns/assets/ios/health/welcome.png).
- [Observed] Maps: [location prompt](../../../../../skills/native-ui-patterns/assets/ios/maps/location-permission.png).
- [Observed] Wallet: [location prompt](../../../../../skills/native-ui-patterns/assets/ios/wallet/location-permission.png).

## Gaps retained rather than inferred

- [Unconfirmed] App Store, Mail, Camera, Notes, Phone, FaceTime, Clock, Weather, Music, Podcasts, and Find My behavior because those apps were unavailable.
- [Unconfirmed] Deep links, search results, gestures/transitions, destructive confirmation, VoiceOver announcements, focus order, Dynamic Type adaptation, increased contrast, and landscape behavior.
- [Unconfirmed] Account-backed and network-backed empty/loading/error states.
