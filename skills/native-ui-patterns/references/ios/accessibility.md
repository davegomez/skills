# iOS focused accessibility review

## Guidance

**Observed:** XCTest located visible controls by labels across Settings, Contacts, Files, Shortcuts, Calendar, Photos, Reminders, and Wallet; Safari’s attempted address query failed. This supports limited programmatic naming only. **Inferred adaptation:** align visible and programmatic names, label icon-only/repeated actions specifically, expose state beyond color/opacity, and preserve meaningful focus across task changes.

## Visual references

For a visual accessibility review, choose only the matching control/state row. For nonvisual assistive behavior, use target-product testing rather than loading captures.

| Visual question / state | Matching capture(s) | What to inspect |
| --- | --- | --- |
| Labeled hierarchy controls | Settings [General](../../assets/ios/settings/general.png) | Visible labels, back/title alignment, row grouping and contrast cues |
| Icon-plus-text and menu actions | Files [More menu](../../assets/ios/files/more-menu.png) | Invoker/action labels, visual grouping, overlay/background distinction |
| Disabled selection actions | Shortcuts [empty selection](../../assets/ios/shortcuts/empty-selection-mode.png) | Enabled/disabled cues beyond position, action grouping, empty context |
| Disabled commit | Calendar [empty event](../../assets/ios/calendar/event-empty.png) | Done state cues, field focus, control placement around keyboard |
| Permission choices | Wallet [location permission](../../assets/ios/wallet/location-permission.png) | Choice labels, order, contrast, and surrounding dimmed content |
| Distinguishable row accessories | Settings [Game Center](../../assets/ios/settings/external-link-rows.png) | Arrow versus chevron, switch, and link-row color as non-color cues |

## Review boundary

Review name, role, value/state, distinguishability, reading/focus order, and transitions in the target. VoiceOver output/traversal, Switch Control, Dynamic Type adaptation, contrast modes, keyboard, Reduce Motion, orientation, and target sizes remain **Unconfirmed**; screenshots and XCTest labels cannot establish them.
