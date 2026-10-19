# Android search

## Guidance

**Observed:** Several apps used prominent top search; Messages transformed an icon into a focused field. Settings focus showed live categorized results, Back, and Clear. In the exercised focused-search sequence, system Back first dismissed keyboard UI; a subsequent Back exited search. Whether Back clears a query is **Unconfirmed**. Settings alone showed an unmatched query with “Try searching in Tips & Support”; this was a Settings-only suggestion, not a generic recommended help destination. Clearing restored Settings. Host input produced a compact Gboard toolbar. **Inferred adaptation:** keep search prominent, provide visible exit/reset, and distinguish zero matches from failure. Give the field, result items, Back, and Clear meaningful labels, and preserve focus when results change. Indexing/network failures and broad cross-app no-results behavior remain **Unconfirmed**.

## Visual references

Choose the exact visual question and open only its named state. A pair is required only when the question explicitly asks for a comparison.

| Visual question / state | Matching capture(s) | What to inspect |
| --- | --- | --- |
| Settings resting search | [root](../../assets/android/settings/root.png) | Field placement, surrounding categories and top actions |
| Settings focused before-query or populated-results state | [before query](../../assets/android/settings/search-before-query.png) or [results](../../assets/android/settings/search-results.png) | Open only the requested state; inspect field/Back/Clear alignment, keyboard spacing, and result grouping |
| Settings zero-results recovery | [no results](../../assets/android/settings/search-no-results.png) | Centered recovery, retained query/actions, and Settings-specific Tips & Support context |
| Settings restored after clear/exit | [after clear](../../assets/android/settings/search-after-clear.png) | Restored content and search placement; open only when return context matters |
| Messages list-to-focused-search comparison | [empty list](../../assets/android/messages/empty-list.png) and [focused search](../../assets/android/messages/search-focused.png) | Icon-to-field transformation, category cards, keyboard and exit placement |
| Search over spatial content | Maps [Explore](../../assets/android/maps/sheet-collapsed.png) | Search placement above categories, map, sheet, and surrounding controls |
| Search-led empty surface | Contacts [empty list](../../assets/android/contacts/empty-list.png), Files [empty Downloads](../../assets/android/files/downloads-empty.png), or Phone [empty Home](../../assets/android/phone/empty-home.png) | Open only the relevant application; inspect field/actions relative to empty content and filters |
| Browser search entry | Chrome [signed-out new tab](../../assets/android/chrome/new-tab-signed-out.png) | Search/AI controls, shortcuts, and surrounding card hierarchy |

## Review checks

Check applicable resting, focus, pre-query, results, zero-results, clear, Back, loading, and failure states. Preserve the bounded Back sequence above; do not infer query-clearing behavior. Treat the compact keyboard as capture context, not a target keyboard specification.
