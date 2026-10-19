# iOS 27 safe error-feedback pass

## Scope and method

- [Observed] This pass used only the local iPhone 17 Pro iOS 27.0 Simulator with device identifier `C4E8218D-BF55-4FC3-B421-68FD02401D89`; no web source was used.
- [Observed] Apple apps were launched and inspected with a temporary local XCTest UI runner, and every retained PNG was captured afterward with `xcrun simctl io`.
- [Observed] Temporary text was cleared or discarded without activating any action that could save, send, call, purchase, grant permission, or delete persistent data.
- [Observed] The pass reviewed the existing iOS catalog before inspection, added a cross-app content-gating pattern, and recorded Settings no-results feedback as a variation of the existing centered empty-state pattern rather than duplicating it.

## Calendar — new event title gating

- [Observed] Attempted path: Calendar day view → Add → empty New Event form → enter `Temporary` in Title → clear Title → Cancel.
- [Observed] Before: the day view was captured before opening the form: [calendar-event-before.png](../../../../../skills/native-ui-patterns/assets/ios/calendar/day-before-event.png).
- [Observed] During empty state: Calendar displayed the New Event form with Title focused and Done visibly muted; XCTest exposed Done as disabled: [calendar-event-empty-disabled.png](../../../../../skills/native-ui-patterns/assets/ios/calendar/event-empty.png).
- [Observed] During populated state: entering `Temporary` changed Done to an enabled tinted control: [calendar-event-title-enables-done.png](../../../../../skills/native-ui-patterns/assets/ios/calendar/event-title-entered.png).
- [Observed] After: Title was cleared, Done returned to disabled, Cancel was activated, and the day view returned without an event being saved: [calendar-event-after-discard.png](../../../../../skills/native-ui-patterns/assets/ios/calendar/day-after-event-discard.png).
- [Observed] Side-effect boundary: Done was never activated because it could create a persistent event.
- [Unconfirmed] Any validation or error feedback that occurs only after activating Done is inaccessible under this pass’s safety boundary.

## Contacts — invalid email entry

- [Observed] Attempted path: Contacts list → John Appleseed → Edit → add email → enter `not-an-email` → close → Discard Changes.
- [Observed] Before: the unmodified edit form was captured before adding the temporary email: [contacts-invalid-email-before.png](../../../../../skills/native-ui-patterns/assets/ios/contacts/edit-before-invalid-email.png).
- [Observed] During: Contacts accepted `not-an-email` in a newly added email row, displayed no visible inline text containing “invalid,” “error,” or “valid email,” and exposed Done as enabled: [contacts-invalid-email-no-inline-error.png](../../../../../skills/native-ui-patterns/assets/ios/contacts/edit-invalid-email.png).
- [Observed] After: close opened the discard path; activating Discard Changes returned to John Appleseed detail and removed the temporary row without modifying the contact: [contacts-invalid-email-after-discard.png](../../../../../skills/native-ui-patterns/assets/ios/contacts/detail-after-invalid-email-discard.png).
- [Observed] Side-effect boundary: Done was never activated because it could persist contact changes; Discard Changes was used only to abandon the temporary edit.
- [Unconfirmed] Format validation or error feedback that occurs only after Done is activated is inaccessible under this pass’s safety boundary.
- [Observed] Catalog result: no canonical invalid-email pattern was added because no error presentation was observed.

## Messages — composer content gating

- [Observed] Attempted path: Messages list → first Simulator-provided conversation → empty composer → enter `Temporary` → clear the composer.
- [Observed] Before: the empty composer showed its `iMessage` placeholder and no Send control in the accessibility hierarchy: [messages-composer-empty-before.png](../../../../../skills/native-ui-patterns/assets/ios/messages/composer-empty.png).
- [Observed] During: entering `Temporary` displayed an enabled blue Send control: [messages-composer-text-enables-send.png](../../../../../skills/native-ui-patterns/assets/ios/messages/composer-text-entered.png).
- [Observed] After: clearing the temporary text restored the `iMessage` placeholder and removed the Send control: [messages-composer-after-clear.png](../../../../../skills/native-ui-patterns/assets/ios/messages/composer-after-clear.png).
- [Observed] Side-effect boundary: Send was never activated, and no message was sent.
- [Unconfirmed] Delivery failure, recipient validation, and post-send error states remain inaccessible because reaching them would require sending or attempting to send.

## Settings — unmatched search query

- [Observed] Attempted path: Settings root → Search → enter `zzzz-no-match` → clear Search.
- [Observed] Before: the Settings root and idle Search field were captured: [settings-search-before.png](../../../../../skills/native-ui-patterns/assets/ios/settings/search-before-query.png).
- [Observed] During: the unmatched query replaced the list with a centered magnifying-glass symbol, `No Results for “zzzz-no-match”`, and `Check the spelling or try a new search`: [settings-search-no-results.png](../../../../../skills/native-ui-patterns/assets/ios/settings/search-no-results.png).
- [Observed] After: clearing the query removed the no-results state and restored the Settings list: [settings-search-after-clear.png](../../../../../skills/native-ui-patterns/assets/ios/settings/search-after-clear.png).
- [Observed] Side-effect boundary: only local search text was entered and cleared; no setting was changed.
- [Unconfirmed] Search indexing failure and any network-backed search error were not reachable from this safe local path.

## Retained gaps

- [Unconfirmed] Calendar and Contacts submit-time validation remain unavailable because Done could save persistent data.
- [Unconfirmed] Messages delivery and recipient errors remain unavailable because Send was outside the safety boundary.
- [Unconfirmed] Settings account, network, and permission-dependent errors were not attempted because they would require accounts, external services, or permission changes.
- [Observed] No generic validation claim was added for Contacts, and no cross-application generalization was made from the Settings-only no-results state.
