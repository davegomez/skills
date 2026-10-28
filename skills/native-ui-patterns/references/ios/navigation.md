# iOS navigation

## Guidance

**Observed:** Settings, Files, and Shortcuts used prominent current-level titles; pushed Settings content changed to “General” with a visible return control. Files and Photos placed persistent labeled peer destinations in a rounded translucent dock. Safari’s bottom toolbar held commands, not peers. Settings marked rows that leave the stack with a diagonal arrow and kept the chevron on pushed rows. **Kit:** the tab bar floats as a capsule whose selected tab sits on a gray pill in blue; Search or a prominent tab detaches as a trailing round button. On iPad the tab bar sits at the top, with a sidebar toggle and search glyph, beside a sidebar of rows with a gray selected capsule. Bottom toolbars may also hold search or page dots, still not peers. **Inferred adaptation:** distinguish hierarchy changes, peer switching, and transient commands; keep title, selection, return, and dismissal meaningful. Edge-swipe Back and transitions remain **Unconfirmed**.

## Visual references

Choose the exact visual question. Open only one named state unless the question explicitly compares two states.

| Visual question / state | Matching capture(s) | What to inspect |
| --- | --- | --- |
| Root versus pushed hierarchy | Settings [root](../../assets/ios/settings/root.png) and [General](../../assets/ios/settings/general.png) | Compare title and back-control alignment, grouped content start, surrounding rows |
| Recents or Browse peer destination | Files [Recents](../../assets/ios/files/recents-empty.png) or [Browse](../../assets/ios/files/browse.png) | Open the requested destination; inspect dock selection, title/search relationship, and content |
| Media peer navigation | Photos [Library](../../assets/ios/photos/library-notification-permission.png) | Split dock/trailing Search placement and content behind the prompt |
| Command toolbar rather than peers | Safari [Start Page](../../assets/ios/safari/start-page.png) or Kit [bottom toolbars](../../assets/ios/kit/toolbar-bottom-iphone.png) | Bottom command positions and page chrome; kit button pairs, search, and page dots |
| Floating tab bar with a detached button | Kit [tab bar](../../assets/ios/kit/tab-bar-iphone.png) or [minimized](../../assets/ios/kit/tab-bar-minimized.png) | Selected pill and tint, glyph over label, trailing round button; minimized single tab |
| Top toolbar title and action layouts | Kit [iPhone](../../assets/ios/kit/toolbar-top-iphone.png) or [iPad](../../assets/ios/kit/toolbar-top-ipad.png) | Centered, leading, and large titles; blue prominent circle; grouped capsule; iPad tabs and search |
| iPad: top tab bar | Kit [iPad tab bar](../../assets/ios/kit/tab-bar-ipad.png) | Centered text tabs between sidebar toggle and search glyph, trailing buttons |
| iPad: sidebar beside content | Kit [sidebar](../../assets/ios/kit/sidebar-ipad.png) or [window](../../assets/ios/kit/window-with-sidebar.png) | Sidebar width and tint, Edit and Search on top, selected capsule, collapsible headings, resize corner |
| iPad: sidebar row levels and states | Kit [sidebar rows](../../assets/ios/kit/sidebar-row-states.png) | Indent per level, selected capsule, expand chevron, dimmed disabled row |
| Rows that leave the hierarchy: arrow versus chevron | Settings [Game Center](../../assets/ios/settings/external-link-rows.png) | Arrow versus chevron on sibling rows, count placement, link-row color |

## Review checks

Check relevant root, pushed, peer-selected, minimized, sidebar-selected, and empty states. Preserve visible and semantic orientation. Treat each screenshot as application-specific settled evidence, not component geometry.
