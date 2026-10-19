# iOS navigation

## Guidance

**Observed:** Settings, Files, and Shortcuts used prominent current-level titles; pushed Settings content changed to “General” with a visible return control. Files and Photos placed persistent labeled peer destinations in a rounded translucent dock. Files alone showed an anchored More menu over retained Browse content. Safari’s bottom toolbar held commands, not peers. Settings marked rows that leave the stack with a diagonal arrow and kept the chevron on pushed rows. **Inferred adaptation:** distinguish hierarchy changes, peer switching, and transient commands; keep title, selection, return, and dismissal meaningful. Edge-swipe Back, submenu behavior, and transitions remain **Unconfirmed**.

## Visual references

Choose the exact visual question. Open only one named state unless the question explicitly compares two states.

| Visual question / state | Matching capture(s) | What to inspect |
| --- | --- | --- |
| Root versus pushed hierarchy | Settings [root](../../assets/ios/settings/root.png) and [General](../../assets/ios/settings/general.png) | Compare title and back-control alignment, grouped content start, surrounding rows |
| Recents or Browse peer destination | Files [Recents](../../assets/ios/files/recents-empty.png) or [Browse](../../assets/ios/files/browse.png) | Open the requested destination; inspect dock selection, title/search relationship, and content |
| Closed versus open secondary menu | Files [Browse](../../assets/ios/files/browse.png) and [More open](../../assets/ios/files/more-menu.png) | Compare invoker/menu alignment, overlay bounds, and retained surrounding content |
| Media peer navigation | Photos [Library](../../assets/ios/photos/library-notification-permission.png) | Split dock/trailing Search placement and content behind the prompt |
| Command toolbar rather than peers | Safari [Start Page](../../assets/ios/safari/start-page.png) | Bottom command positions, page chrome, surrounding shortcuts |
| Rows that leave the hierarchy: arrow versus chevron | Settings [Game Center](../../assets/ios/settings/external-link-rows.png) | Arrow versus chevron on sibling rows, count placement, link-row color |

## Review checks

Check relevant root, pushed, peer-selected, menu open/dismissed, and empty states. Preserve visible and semantic orientation. Treat each screenshot as application-specific settled evidence, not component geometry.
