# Android navigation

## Guidance

**Observed:** Clock, Phone, Maps, and Contacts kept labeled bottom destinations with selected indicators. Chrome used an anchored menu, Messages an account sheet, and Files a drawer. Maps layered a handled content sheet over the map and one swipe changed its settled position while bottom navigation remained. **Inferred adaptation:** separate peers, hierarchy, commands, and spatial content; preserve visual/semantic selection and non-committing dismissal. Intermediate sheet anchors, motion, thresholds, and predictive Back remain **Unconfirmed**.

## Visual references

Choose the exact navigation question. Open only one named state unless the question explicitly compares two states.

| Visual question / state | Matching capture(s) | What to inspect |
| --- | --- | --- |
| Collapsed versus expanded map sheet | Maps [collapsed](../../assets/android/maps/sheet-collapsed.png) and [expanded](../../assets/android/maps/sheet-expanded.png) | Compare search/categories, drag cue, sheet bounds, and persistent bottom destinations |
| Signed-out You destination | Maps [You](../../assets/android/maps/you-signed-out.png) | Selected destination, signed-out content, and surrounding navigation |
| Clock versus Alarm peers | Clock [Clock](../../assets/android/clock/clock-tab.png) and [Alarm](../../assets/android/clock/alarm-list.png) | Compare content-to-destination spacing, selected indicator, and Add placement |
| Home versus Keypad peers | Phone [Home](../../assets/android/phone/empty-home.png) and [Keypad](../../assets/android/phone/keypad.png) | Compare bottom selection, content hierarchy, and keypad/action positions |
| Contacts empty destination | Contacts [empty list](../../assets/android/contacts/empty-list.png) | Peer selection, empty state, floating Add and surrounding chrome |
| Peer shell behind a blocker | Photos [sign-in primer](../../assets/android/photos/sign-in-primer.png) | Visible Photos/Search destinations, dim layer and modal card relationship |
| Closed versus open command menu | Chrome [new tab](../../assets/android/chrome/new-tab-signed-out.png) and [overflow](../../assets/android/chrome/overflow-menu.png) | Compare invoker/menu alignment, command grouping, and retained page context |
| Closed versus open account sheet | Messages [empty list](../../assets/android/messages/empty-list.png) and [account sheet](../../assets/android/messages/account-sheet.png) | Compare sheet height, action alignment, scrim/base context, and dismissal affordance |
| Closed versus open storage drawer | Files [Downloads](../../assets/android/files/downloads-empty.png) and [drawer](../../assets/android/files/navigation-drawer.png) | Compare drawer edge/width, destination grouping, and retained surrounding surface |

## Review checks

Check applicable selected/unselected peers, overlay/drawer open and dismissed, sheet positions, and dirty-form Back. Keep destinations, selection, invokers, and dismissal meaningful; settled before/after images do not establish motion.
