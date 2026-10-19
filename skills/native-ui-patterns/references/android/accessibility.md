# Android focused accessibility review

## Guidance

**Observed:** UI Automator dumps exposed names for icon-only actions and selected/checked state for sampled destinations and switches. This supports limited hierarchy semantics only. **Inferred adaptation:** use task-specific names, include item identity for repeated controls, synchronize visible and programmatic state, and preserve focus meaningfully as search, overlays, and forms change.

## Visual references

For a visual accessibility question, choose only the matching row. For nonvisual assistive behavior, use target-product testing rather than loading captures.

| Visual question / state | Matching capture(s) | What to inspect |
| --- | --- | --- |
| Icon-only search actions | Messages [focused search](../../assets/android/messages/search-focused.png) | Back/field/action placement, visible labels, category grouping and keyboard context |
| Selected destination | Maps [Explore](../../assets/android/maps/sheet-collapsed.png) | Selected cues beyond color, label/icon alignment and surrounding navigation |
| Repeated unchecked controls | Clock [Alarm list](../../assets/android/clock/alarm-list.png) | Item-specific switch placement, card labels, state cues and target separation |
| Nested row switch | Settings [Display & touch](../../assets/android/settings/display-and-touch.png) | Row versus switch target, label/state adjacency and contrast cues |
| Permission choices | Contacts [notification permission](../../assets/android/contacts/notification-permission.png) | Choice order/labels, dialog contrast and obscured surrounding content |
| Keypad actions | Phone [keypad](../../assets/android/phone/keypad.png) | Digit/action arrangement, labels, delete/call prominence and bottom navigation |

## Review boundary

Review target names, roles, values/states, focusability, target distinction, reading/focus order, and transitions. TalkBack output/traversal, font scaling, contrast modes, rotation, split screen, keyboard, motion settings, and target sizes remain **Unconfirmed**; dumps and screenshots cannot establish them.
