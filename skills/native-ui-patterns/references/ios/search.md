# iOS search

## Guidance

**Observed:** Settings, Files, Messages, and Shortcuts used rounded Search fields with leading magnifiers and trailing microphones, but placement varied. Focused Settings search retained exit/clear behavior; a temporary unmatched query produced centered feedback and clearing restored content. **Kit:** the field keeps its magnifier and microphone in placeholder, typing, and entered states, on an opaque or clear glass capsule; a two-segment scope control can sit beside it. On iPad, search sits at the top: a trailing toolbar field or a field directly below the tab bar. **Inferred adaptation:** keep placement stable within one screen, distinguish zero matches from failure, echo a query when useful, and retain reset/exit. Dictation, Safari focus, loading, and network/indexing failures remain **Unconfirmed**.

## Visual references

Choose the exact visual question and open only its named state. Open both captures only for an explicit comparison.

| Visual question / state | Matching capture(s) | What to inspect |
| --- | --- | --- |
| Bottom-anchored resting search | Settings [root](../../assets/ios/settings/root.png) | Field placement over content, icon/text alignment, surrounding rows |
| Focused search before a query | Settings [before query](../../assets/ios/settings/search-before-query.png) | Field/keyboard spacing plus exit and clear placement |
| Query-specific zero results | Settings [no results](../../assets/ios/settings/search-no-results.png) | Centered feedback, retained query, and surrounding search controls |
| Field placeholder, typing, and entered | Kit [field states](../../assets/ios/kit/search-field-states.png) | Opaque versus clear glass capsule, blue caret, term weight, dimmed microphone on glass |
| Search beside a scope control | Kit [scope control](../../assets/ios/kit/search-scope-control.png) | Centered narrow field versus wide field with a two-segment control |
| iPad: search placement | Kit [below the tab bar](../../assets/ios/kit/tab-bar-ipad.png) or [in the toolbar](../../assets/ios/kit/toolbar-top-ipad.png) | Field width under the tab capsule, or trailing field with microphone beside buttons |
| Search restored after clear | Settings [after clear](../../assets/ios/settings/search-after-clear.png) | Restored context; open only when reset outcome matters |
| Search below a large title | Files [Recents](../../assets/ios/files/recents-empty.png) or Shortcuts [empty library](../../assets/ios/shortcuts/empty-library.png) | Open the relevant app; inspect title-to-field spacing, microphone position, and content start |
| Search within a list surface | Messages [conversation list](../../assets/ios/messages/conversation-list.png) | Field/list alignment and surrounding navigation/actions |

## Review checks

Check only supported resting, focused, results, zero-results, clear, and exit states. Add loading/failure states only from target-product evidence. Keep the field visible around the keyboard and label clear, dictation, and exit actions.
