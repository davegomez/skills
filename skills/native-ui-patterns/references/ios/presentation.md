# iOS presentation

## Guidance

**Observed:** Files alone showed an anchored More menu over retained Browse content. **Kit:** sheets carry a grabber, a leading close button, a centered title, and a blue commit circle; iPhone sheets sit at the bottom over dimmed content, and iPad sheets float as centered cards. Alerts set 2 actions side by side and stack 3 or more, with the default action filled blue and the destructive action in red text. Action sheets are cards near the top trailing toolbar, destructive action first and no Cancel row. Context menus lead with a row of icon tiles, then normal, disabled, and red destructive rows, and mark submenus with a chevron. Popovers, with an arrow toward the anchor, are iPad only. **Inferred adaptation:** keep transient choices near their source, keep dismissal and commit distinct, and set destructive choices apart by color and position. Submenu behavior, dismissal gestures, and transitions remain **Unconfirmed**.

## Visual references

Choose the exact visual question and open only its named image. Open both only for an explicit comparison.

| Visual question / state | Matching capture(s) | What to inspect |
| --- | --- | --- |
| Closed versus open secondary menu | Files [Browse](../../assets/ios/files/browse.png) and [More open](../../assets/ios/files/more-menu.png) | Compare invoker/menu alignment, overlay bounds, and retained surrounding content |
| iPhone sheet: medium, large, stacked | Kit [iPhone sheets](../../assets/ios/kit/sheet-iphone.png) | Inset medium sheet with all corners rounded, large sheet near the top, previous sheet peeking behind |
| iPad: sheet as a centered card | Kit [iPad sheet](../../assets/ios/kit/sheet-ipad.png) | Four rounded corners, shadow, width short of the screen, close and commit placement |
| Alert with 2 versus 3 actions and a text field | Kit [alert](../../assets/ios/kit/alert.png) | Side-by-side Cancel and Default versus stacked Default, Destructive, Cancel; field group; left-aligned text |
| Action sheet, iPhone or iPad | Kit [iPhone](../../assets/ios/kit/action-sheet-iphone.png) or [iPad](../../assets/ios/kit/action-sheet-ipad.png) | Card position, red Destructive first, stacked pill actions; dimmed iPhone content versus no iPad scrim |
| Share sheet, iPhone versus iPad | Kit [share sheet](../../assets/ios/kit/share-sheet.png) | Bottom sheet versus arrowed card; Collaborate header; people, app, and action rows; Light versus Dark |
| Context menu anatomy and placement | Kit [iPhone](../../assets/ios/kit/context-menu-iphone.png) or [iPad horizontal](../../assets/ios/kit/context-menu-ipad-horizontal.png) | Icon-tile row, row states, divider, submenu chevron; menu below versus beside the content |
| Menus with sections, shortcuts, and an edit menu | Kit [menus](../../assets/ios/kit/menus.png) | Section titles, subtitle rows, trailing shortcuts, wrapped long titles, Cut, Copy, Paste capsule |
| Submenu row states | Kit [submenu states](../../assets/ios/kit/submenu-states.png) | Right chevron, highlighted row with down chevron, dimmed disabled row, Light versus Dark |
| iPad: popover arrow positions | Kit [popover arrows](../../assets/ios/kit/popover-arrows.png) | Arrow on each edge at leading, center, or trailing positions; shared card shape |

## Review checks

Check relevant closed, open, dismissed, detent, stacked, disabled-item, destructive, and expanded-submenu states. For iPad, check the anchor and arrow; for iPhone, check the sheet counterpart.
