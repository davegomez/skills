# Direct-observation coverage

Coverage below is transcribed from the worker [iOS inspection log](notes/ios/direct-observation-log.md), [iOS error-feedback pass](notes/ios/error-feedback-pass.md), [iOS application inventory](notes/ios/application-inventory.md), [Android inspection log](notes/android/direct-observation-log.md), [Android error-feedback pass](notes/android/error-feedback-pass.md), and [Android application inventory](notes/android/application-inventory.md). It reports reached states rather than guessed feature coverage.

## Session totals

| Platform run | Requested applications | Directly launched | Unavailable as requested | Retained evidence | Boundary |
| --- | ---: | ---: | ---: | --- | --- |
| iOS 27.0 Simulator, iPhone 17 Pro | 23 | 12 | 11 | 36 PNG screenshots | Available apps were launched; only the listed states and safe error-feedback attempts were inspected. |
| Android 17 Emulator, AVD `pixel_a17` | 18 | 14 | 4 | 57 PNG screenshots and 57 matching UI Automator XML dumps | Four launched apps were account/setup-limited; other apps also had content or permission limits; five apps received safe error-feedback attempts. |
| 2026-09-08 set: physical iPhone 17 Pro and physical Pixel 10 | 2 | 2 | 0 | 44 iOS PNG originals and 20 Android JPEG originals | Settings detail screens only, both devices signed in; no interaction was exercised. See the [capture note](notes/captures-2026-09-08.md). |

“Directly launched” does not mean that an app's primary content or all catalog categories were inspected. See the per-application outcome and the [limitations](limitations.md).

## iOS applications

| Application | Inspection outcome | Directly observed states | Screenshot evidence |
| --- | --- | --- | --- |
| Settings | Inspected | [Observed] Root, General detail, grouped rows, resting and focused Search, query-specific no-results feedback, and return after clearing | [root](../../../skills/native-ui-patterns/assets/ios/settings/root.png), [General](../../../skills/native-ui-patterns/assets/ios/settings/general.png), [no results](../../../skills/native-ui-patterns/assets/ios/settings/search-no-results.png), [after clear](../../../skills/native-ui-patterns/assets/ios/settings/search-after-clear.png) |
| Messages | Inspected | [Observed] Conversation list, one sample conversation, and composer states with Send absent while empty and available after temporary text; text was cleared and nothing was sent | [list](../../../skills/native-ui-patterns/assets/ios/messages/conversation-list.png), [conversation](../../../skills/native-ui-patterns/assets/ios/messages/conversation-empty-composer.png), [empty composer](../../../skills/native-ui-patterns/assets/ios/messages/composer-empty.png), [populated composer](../../../skills/native-ui-patterns/assets/ios/messages/composer-text-entered.png), [after clear](../../../skills/native-ui-patterns/assets/ios/messages/composer-after-clear.png) |
| Calendar | Inspected | [Observed] Introduction, day view with location prompt, and event-form states with Done disabled while Title was empty and enabled after temporary text; the title was cleared and nothing was saved | [intro](../../../skills/native-ui-patterns/assets/ios/calendar/whats-new.png), [day](../../../skills/native-ui-patterns/assets/ios/calendar/day-location-permission.png), [empty/disabled](../../../skills/native-ui-patterns/assets/ios/calendar/event-empty.png), [populated/enabled](../../../skills/native-ui-patterns/assets/ios/calendar/event-title-entered.png), [after discard](../../../skills/native-ui-patterns/assets/ios/calendar/day-after-event-discard.png) |
| Contacts | Inspected | [Observed] Sample list, detail, edit form, and malformed temporary email retained without visible inline error; the edit was discarded and nothing was saved or deleted | [list](../../../skills/native-ui-patterns/assets/ios/contacts/contact-list.png), [detail](../../../skills/native-ui-patterns/assets/ios/contacts/contact-detail.png), [malformed email without inline error](../../../skills/native-ui-patterns/assets/ios/contacts/edit-invalid-email.png), [after discard](../../../skills/native-ui-patterns/assets/ios/contacts/detail-after-invalid-email-discard.png) |
| Photos | Inspected, prompt-limited | Introduction, six-sample-photo Library behind notification prompt; no media changed | [intro](../../../skills/native-ui-patterns/assets/ios/photos/whats-new.png), [Library/prompt](../../../skills/native-ui-patterns/assets/ios/photos/library-notification-permission.png) |
| Maps | Prompt-limited | First-run surface behind initial location permission prompt only | [location prompt](../../../skills/native-ui-patterns/assets/ios/maps/location-permission.png) |
| Reminders | Prompt-limited | Welcome screen and iCloud-sync prompt over root; nothing created | [intro](../../../skills/native-ui-patterns/assets/ios/reminders/welcome.png), [sync prompt](../../../skills/native-ui-patterns/assets/ios/reminders/icloud-sync-prompt.png) |
| Files | Inspected | Recents, Browse/On My iPhone, locations/tags, More menu; no file changed | [Recents](../../../skills/native-ui-patterns/assets/ios/files/recents-empty.png), [Browse](../../../skills/native-ui-patterns/assets/ios/files/browse.png), [More menu](../../../skills/native-ui-patterns/assets/ios/files/more-menu.png) |
| Safari | Inspected, bounded | Start Page and bottom browser controls; no URL opened; focused address state not captured | [Start Page](../../../skills/native-ui-patterns/assets/ios/safari/start-page.png) |
| Health | Onboarding-limited | First welcome screen only | [welcome](../../../skills/native-ui-patterns/assets/ios/health/welcome.png) |
| Wallet | Prompt-limited | Root behind location prompt; permission refused; no pass or payment flow opened | [location prompt](../../../skills/native-ui-patterns/assets/ios/wallet/location-permission.png) |
| Shortcuts | Inspected with empty data | Empty All Shortcuts root and empty selection mode; nothing created | [root](../../../skills/native-ui-patterns/assets/ios/shortcuts/empty-library.png), [selection](../../../skills/native-ui-patterns/assets/ios/shortcuts/empty-selection-mode.png) |
| App Store | Unavailable | Absent from inspected Simulator app inventory | No screenshot possible: requested app was unavailable. |
| Mail | Unavailable | Absent from inspected Simulator app inventory | No screenshot possible: requested app was unavailable. |
| Camera | Unavailable | Absent from inspected Simulator app inventory | No screenshot possible: requested app was unavailable. |
| Notes | Unavailable | Absent from inspected Simulator app inventory; third-party Note Taker was not substituted | No screenshot possible: requested app was unavailable. |
| Phone | Unavailable | Absent from inspected Simulator app inventory | No screenshot possible: requested app was unavailable. |
| FaceTime | Unavailable | Absent from inspected Simulator app inventory | No screenshot possible: requested app was unavailable. |
| Clock | Unavailable | Absent from inspected Simulator app inventory | No screenshot possible: requested app was unavailable. |
| Weather | Unavailable | Absent from inspected Simulator app inventory | No screenshot possible: requested app was unavailable. |
| Music | Unavailable | Absent from inspected Simulator app inventory | No screenshot possible: requested app was unavailable. |
| Podcasts | Unavailable | Absent from inspected Simulator app inventory | No screenshot possible: requested app was unavailable. |
| Find My | Unavailable | Absent from inspected Simulator app inventory | No screenshot possible: requested app was unavailable. |

## Android applications

| Application | Inspection outcome | Directly observed states | Screenshot evidence |
| --- | --- | --- | --- |
| Settings | Inspected | [Observed] Category landing, populated Search Settings state, query-specific no-results recovery, return after clearing, Display & touch detail, and unchecked Dark theme switch | [main](../../../skills/native-ui-patterns/assets/android/settings/root.png), [search](../../../skills/native-ui-patterns/assets/android/settings/search-results.png), [no results](../../../skills/native-ui-patterns/assets/android/settings/search-no-results.png), [after clear](../../../skills/native-ui-patterns/assets/android/settings/search-after-clear.png), [detail](../../../skills/native-ui-patterns/assets/android/settings/display-and-touch.png) |
| Google Play Store | Account-limited | Sign-in-required landing only; sign-in not selected | [landing](../../../skills/native-ui-patterns/assets/android/play-store/sign-in-required.png) |
| Messages | Inspected with empty data | [Observed] Empty list, search categories, account sheet, and new-chat recipient attempts: temporary nonmatching text and keyboard submission produced no application-authored error, while `123` produced a “Send to 123” candidate; the candidate was not selected and nothing was sent | [main](../../../skills/native-ui-patterns/assets/android/messages/empty-list.png), [recipient before](../../../skills/native-ui-patterns/assets/android/messages/recipient-empty.png), [no match](../../../skills/native-ui-patterns/assets/android/messages/recipient-no-match.png), [candidate](../../../skills/native-ui-patterns/assets/android/messages/recipient-short-number-candidate.png), [after cancel](../../../skills/native-ui-patterns/assets/android/messages/empty-list-after-recipient-cancel.png) |
| Gmail | Account-limited | Feature introduction and address setup; no inbox reached | [intro](../../../skills/native-ui-patterns/assets/android/gmail/whats-new.png), [address setup](../../../skills/native-ui-patterns/assets/android/gmail/email-address-setup.png) |
| Calendar | Account-limited | Startup checking state followed by Google account setup; no calendar grid reached | [checking](../../../skills/native-ui-patterns/assets/android/calendar/checking-account.png), [account setup](../../../skills/native-ui-patterns/assets/android/calendar/account-setup.png) |
| Contacts | Inspected with empty data | [Observed] Notification permission declined; empty list, create form, malformed temporary email without inline validation, separate unsaved-change confirmation, and return after Discard; nothing saved | [permission](../../../skills/native-ui-patterns/assets/android/contacts/notification-permission.png), [main](../../../skills/native-ui-patterns/assets/android/contacts/empty-list.png), [malformed email without inline error](../../../skills/native-ui-patterns/assets/android/contacts/invalid-email.png), [unsaved-change confirmation](../../../skills/native-ui-patterns/assets/android/contacts/invalid-email-discard-prompt.png), [after discard](../../../skills/native-ui-patterns/assets/android/contacts/empty-list-after-discard.png) |
| Photos | Account-limited | Photos/Search shell behind sign-in primer; library/detail behavior not reached | [primer](../../../skills/native-ui-patterns/assets/android/photos/sign-in-primer.png) |
| Maps | Inspected, signed out | Sign-in onboarding, audio primer, bottom destinations, Explore categories, lower and expanded content sheet, search focus; no route or contribution created | [onboarding](../../../skills/native-ui-patterns/assets/android/maps/sign-in-onboarding.png), [audio primer](../../../skills/native-ui-patterns/assets/android/maps/audio-primer.png), [signed-out You](../../../skills/native-ui-patterns/assets/android/maps/you-signed-out.png), [Explore](../../../skills/native-ui-patterns/assets/android/maps/sheet-collapsed.png), [expanded sheet](../../../skills/native-ui-patterns/assets/android/maps/sheet-expanded.png) |
| Files | Inspected with empty data | [Observed] Downloads, file-type controls, list-layout control, “No items,” navigation drawer, and a temporary `/` folder name retained without inline error before Cancel | [main](../../../skills/native-ui-patterns/assets/android/files/downloads-empty.png), [drawer](../../../skills/native-ui-patterns/assets/android/files/navigation-drawer.png), [new-folder attempt](../../../skills/native-ui-patterns/assets/android/files/new-folder-invalid-name.png), [after cancel](../../../skills/native-ui-patterns/assets/android/files/downloads-after-folder-cancel.png) |
| Chrome | Inspected, signed out | Onboarding choices, new tab page, overflow menu; no URL loaded | [onboarding](../../../skills/native-ui-patterns/assets/android/chrome/stay-signed-out-onboarding.png), [post-choice](../../../skills/native-ui-patterns/assets/android/chrome/notification-primer.png), [new tab](../../../skills/native-ui-patterns/assets/android/chrome/new-tab-signed-out.png), [menu](../../../skills/native-ui-patterns/assets/android/chrome/overflow-menu.png) |
| Phone | Inspected with empty data | Home filters, empty call history, bottom navigation, keypad; no digits entered or call placed | [home](../../../skills/native-ui-patterns/assets/android/phone/empty-home.png), [keypad](../../../skills/native-ui-patterns/assets/android/phone/keypad.png) |
| Clock | Inspected with pre-existing data | [Observed] Clock and Alarm destinations, two off/unchecked alarm cards, graphical and text-input time-picker states, and an out-of-range hour attempt that left the prior value unchanged without explanatory error text; picker canceled without saving | [clock](../../../skills/native-ui-patterns/assets/android/clock/clock-tab.png), [alarms](../../../skills/native-ui-patterns/assets/android/clock/alarm-list.png), [text-input mode](../../../skills/native-ui-patterns/assets/android/clock/time-input-text-mode.png), [unchanged hour](../../../skills/native-ui-patterns/assets/android/clock/time-input-invalid-hour.png), [after cancel](../../../skills/native-ui-patterns/assets/android/clock/alarm-list-after-cancel.png) |
| Drive | Account-limited | Google account setup only; no file list reached | [account setup](../../../skills/native-ui-patterns/assets/android/drive/account-setup.png) |
| YouTube Music | Permission-limited | Sign-in/device-files onboarding and media-access explanation; permission not granted | [onboarding](../../../skills/native-ui-patterns/assets/android/youtube-music/device-files-onboarding.png), [media-access state](../../../skills/native-ui-patterns/assets/android/youtube-music/media-access-primer.png) |
| Camera | Unavailable as requested | Google Camera package absent; AOSP Camera2 was not substituted | No screenshot possible: requested Google app was unavailable. See [unavailable-app note](notes/android/unavailable-apps.md#not-installed-as-the-requested-google-app). |
| Weather | Unavailable as requested | Standalone Google Weather package absent; Google Search was not substituted | No screenshot possible: requested Google app was unavailable. See [unavailable-app note](notes/android/unavailable-apps.md#not-installed-as-the-requested-google-app). |
| Wallet | Unavailable as requested | Requested Google Wallet package absent | No screenshot possible: requested Google app was unavailable. See [unavailable-app note](notes/android/unavailable-apps.md#not-installed-as-the-requested-google-app). |
| Keep | Unavailable as requested | Requested Google Keep package absent | No screenshot possible: requested Google app was unavailable. See [unavailable-app note](notes/android/unavailable-apps.md#not-installed-as-the-requested-google-app). |

## Settings detail screens (2026-09-08 set)

The second capture set reached the screens below. Each row is one settled screenshot. No
interaction was exercised, so no row here records a state transition. Screenshot identifiers match
the [capture note](notes/captures-2026-09-08.md).

### iOS Settings

| Screenshot | Screen |
| --- | --- |
| S-I01 | Settings root (account row, Family, connectivity group, bottom search) |
| S-I02 | Apple Account hub |
| S-I03 | Personal Information (top) |
| S-I04 | Personal Information (scrolled, collapsed avatar header) |
| S-I05 | Sign-In & Security |
| S-I06 | Payment & Shipping (Edit) |
| S-I07 | Subscriptions (Sort) |
| S-I08 | iCloud+ hub (storage bar, promo card, app tiles) |
| S-I09 | Family |
| S-I10 | Find My |
| S-I11 | Sign in with Apple (apps list) |
| S-I12 | Device Info |
| S-I13 | Family member detail (destructive remove row) |
| S-I14 | Wi-Fi (networks list, Edit) |
| S-I15 | Join Wi-Fi password sheet (close + disabled checkmark) |
| S-I16 | Bluetooth (My Devices, Not Connected) |
| S-I17 | Battery (chart, daily usage) |
| S-I18 | Personal Hotspot |
| S-I19 | Software Update (up to date) |
| S-I20 | iPhone Storage (top, segmented bar) |
| S-I21 | iPhone Storage (scrolled, Show All, floating search) |
| S-I22 | Music app storage detail (Offload/Delete) |
| S-I23 | AppleCare & Warranty |
| S-I24 | AirPods Pro coverage detail |
| S-I25 | CarPlay (hero illustration, My Cars, Other Cars spinner) |
| S-I26 | Date & Time |
| S-I27 | Language & Region (reorder handles, Edit) |
| S-I28 | TV Provider (skeleton placeholders, Sign Out) |
| S-I29 | Transfer or Reset iPhone |
| S-I30 | Legal & Regulatory |
| S-I31 | Accessibility hub |
| S-I32 | Appearance (Light/Dark picker, top) |
| S-I33 | Appearance (scrolled, header collapse) |
| S-I34 | Control Center |
| S-I35 | Display & Brightness (slider) |
| S-I36 | Wallpaper (carousel, page dots) |
| S-I37 | Notifications (Display As picker) |
| S-I38 | Sounds & Haptics (ringtone slider) |
| S-I39 | Focus (+ add) |
| S-I40 | Screen Time (top, usage chart) |
| S-I41 | Screen Time (scrolled, destructive turn-off row) |
| S-I42 | Enter your passcode sheet |
| S-I43 | Emergency SOS |
| S-I44 | Game Center (external-link arrows) |

### Android Settings

| Screenshot | Screen |
| --- | --- |
| S-A01 | Sound & vibration (sliders) |
| S-A02 | Modes |
| S-A03 | Security & privacy (status card, dismissible suggestion, alerts pill) |
| S-A04 | Apps (recently opened, See all) |
| S-A05 | Network & internet |
| S-A06 | Enhanced HDR brightness (comparison, toggle card, slider) |
| S-A07 | Safety & emergency (large title, pill action) |
| S-A08 | Storage (usage bar, category bars) |
| S-A09 | Display & touch (split rows with switch) |
| S-A10 | Wallpaper & style (top) |
| S-A11 | Location (master switch, recent access) |
| S-A12 | Wallpaper & style (scrolled) |
| S-A13 | Parental controls |
| S-A14 | Wi-Fi password dialog with keyboard |
| S-A15 | Connected devices |
| S-A16 | Internet (Wi-Fi networks list) |
| S-A17 | Settings root (search, account row, categories) |
| S-A18 | Network details (Forget/Disconnect/Share) |
| S-A19 | Digital Wellbeing (ring chart, dismissible tip) |
| S-A20 | Sound & vibration (scrolled, switch rows) |

## State coverage across the runs

| State or behavior | iOS evidence | Android evidence | Remaining boundary |
| --- | --- | --- | --- |
| Resting search | [Observed] Settings, Files, Messages, and Shortcuts | [Observed] Several landing surfaces | [Unconfirmed] Safari's focused address field remains unavailable. |
| Focused search/results | [Observed] Settings focused search and query-specific no-results state | [Observed] Settings no-results state and focused Settings/Messages search | [Unconfirmed] Search indexing, network-backed search failure, and broader cross-application behavior remain unavailable. |
| Empty collections | [Observed] Files and Shortcuts | [Observed] Messages, Contacts, and Files | [Unconfirmed] Populated counterparts were not available for most of these apps. |
| Structured forms | [Observed] Calendar content gating and Contacts malformed email without inline error before discard | [Observed] Contacts, Messages, Clock, and Files safe malformed/out-of-range attempts, with no explicit validation error reached | [Unconfirmed] Save-, confirmation-, candidate-selection-, and send-triggered validation remain unavailable. |
| Menus/overlays | Files anchored menu | Chrome overflow and Messages account sheet | Submenus and destructive menu actions were not exercised. |
| Selection | Empty Shortcuts selection mode | No safe populated list supported selection inspection | Selected-item actions were not exercised. |
| Application-level invalid-input feedback | [Observed] Calendar and Messages gated empty content; Contacts showed no inline error before commit | [Observed] Contacts, Messages, Clock, and Files showed no explicit application-authored error in the safe pre-commit states reached | [Unconfirmed] Commit-, save-, candidate-selection-, and delivery-time errors remain unavailable. |
| System permission prompts and primers | [Observed] System location/notification prompts; refusal recorded for Wallet | [Observed] Contacts system dialog and Maps/YouTube Music application primers; no access granted | [Unconfirmed] Post-grant behavior was not tested; permission UI is not application-level error feedback. |
| Cancellation/back | [Observed] Explicit close/clear controls and safe discard paths | [Observed] Back, Cancel, Clear text, and Discard restored non-committed states | [Unconfirmed] iOS gesture-back behavior remains unavailable. |
| Unsaved-change confirmation | [Unconfirmed] No unsaved-change confirmation was reached | [Observed] Contacts confirmation appeared after leaving a modified form | [Unconfirmed] This confirmation does not establish invalid-input feedback or persistent-item deletion protection. |
| Loading and failures | [Unconfirmed] No product loading or failure flow was verified | [Observed] Android Calendar account setup showed one “Checking info…” state; [Unconfirmed] no product failure flow was verified | [Unconfirmed] Network/account-backed loading and failure states remain unavailable. |
| Switches, sliders, and pickers | [Observed] Settings switches on and off, one brightness slider, two visual pickers (2026-09-08 set) | [Observed] existing unchecked switches; sliders and master switch cards captured in the 2026-09-08 set, not yet imported | [Unconfirmed] toggling, dragging, and selection changes were not exercised |
| Row anatomy | [Observed] icon-led rows, label/value rows, identity-led rows with app icons, external-link arrows (2026-09-08 set) | [Observed] grouped card rows captured in the 2026-09-08 set, not yet imported | [Unconfirmed] row taps and accessory targets were not exercised |
| Action rows | [Observed] blue text-only add and command rows; red destructive rows alone or grouped, with consequence footers (2026-09-08 set) | [Observed] pill buttons and inline creation rows captured in the 2026-09-08 set, not yet imported | [Unconfirmed] activation, confirmation dialogs, and undo were not exercised |
| Accessibility adaptation | Label-based XCTest activation only | Saved UI Automator labels/states only | Screen-reader traversal, announcements, scaling, contrast, and external keyboard were not tested. |
| Motion/rotation/layout adaptation | Settled screenshots only | Pre/post settled Maps sheet positions only | Timing, easing, rotation, split screen, landscape, and other form factors were not tested. |
