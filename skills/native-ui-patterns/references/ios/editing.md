# iOS editing

## Guidance

**Observed:** Calendar and Contacts used dedicated task surfaces with separated dismissal/commit controls and grouped fields. Calendar focused Title and gated Done; Messages omitted Send while empty and exposed it after text. Contacts used adjacent add/remove rows and retained malformed temporary email without visible inline error before discard. Settings used trailing switches in on and off states with gray footer captions, an inline slider with bounding glyphs, and preview-tile pickers with a check or capsule selection cue. Settings used blue text-only rows for add actions and commands, and red text-only rows, alone or last in a card, with a footer that states the consequence. **Inferred adaptation:** group by meaning, keep dismissal and commit distinct, focus only a clearly primary input, and make content gating legible. Save/send, submit-time validation, persistent deletion, and iOS dirty-dismiss confirmation remain **Unconfirmed**.

## Visual references

Choose the exact visual question and open only the named state or explicit comparison pair. Entry, exit, and reset context are separate questions.

| Visual question / state | Matching capture(s) | What to inspect |
| --- | --- | --- |
| Calendar form hierarchy and keyboard | [event form](../../assets/ios/calendar/event-form.png) | Task-surface bounds, close/commit alignment, grouped rows, keyboard occlusion |
| Empty versus populated Done state | [empty form](../../assets/ios/calendar/event-empty.png) and [title entered](../../assets/ios/calendar/event-title-entered.png) | Title focus plus disabled/enabled Done treatment and placement |
| Contact form and repeatable rows | [edit form](../../assets/ios/contacts/edit-form.png) | Field grouping, add/remove controls, top actions, and surrounding form |
| Contact invalid-email comparison | [before invalid email](../../assets/ios/contacts/edit-before-invalid-email.png) and [invalid email](../../assets/ios/contacts/edit-invalid-email.png) | Added row, keyboard spacing, and absent visible inline feedback |
| Empty versus available message commit | [empty composer](../../assets/ios/messages/composer-empty.png) and [text entered](../../assets/ios/messages/composer-text-entered.png) | Composer/keyboard alignment and Send appearance/placement |
| Entry, return, or reset context | Calendar [before entry](../../assets/ios/calendar/day-before-event.png) or [after discard](../../assets/ios/calendar/day-after-event-discard.png); Contacts [detail after discard](../../assets/ios/contacts/detail-after-invalid-email-discard.png); Messages [conversation](../../assets/ios/messages/conversation-empty-composer.png) or [after clear](../../assets/ios/messages/composer-after-clear.png) | Open only the requested side; inspect surrounding context and restored controls |
| Switch on versus off with dependent rows and footer | [dependent rows](../../assets/ios/settings/switch-dependent-rows.png) | Track and knob ends, divider to the dependent rows, footer placement outside the card |
| Stacked switches under one section header | [stacked switches](../../assets/ios/settings/stacked-switches-footers.png) | Card, footer, and header caption spacing between peer switch units |
| Inline slider with bounding glyphs | [brightness slider](../../assets/ios/settings/brightness-slider.png) | Track fill, thumb, leading and trailing glyph sizes, divider to the row below |
| Visual picker: radio versus capsule selection | [radio selection](../../assets/ios/settings/appearance-picker.png) and [capsule selection](../../assets/ios/settings/notifications-display-picker.png) | Tile spacing, caption cue, and what follows the card |
| Section header and footer captions | [Sign-In and Security captions](../../assets/ios/settings/sign-in-security-captions.png) | Caption alignment outside the card and mixed trailing controls inside it |
| Add row inside a group versus standalone command card | [add row in a group](../../assets/ios/settings/add-row-in-group.png) and [command cards](../../assets/ios/settings/offload-delete-command-cards.png) | Row position in the card, alignment, ellipsis, and footer placement outside the card |
| Reversible versus irreversible command cards | [command cards](../../assets/ios/settings/offload-delete-command-cards.png) | Blue card above red card, one footer per card, color as the only other difference |
| Link row above destructive row in one card | [link over destructive](../../assets/ios/settings/link-over-destructive-card.png) | Divider between the two rows, left alignment, and absent footer |
| Standalone destructive row, centered, with or without footer | [centered, no footer](../../assets/ios/settings/destructive-row-centered.png) and [centered with footer](../../assets/ios/settings/sign-out-row-footer.png) | Card isolation, whitespace above, centered text, and footer paragraphs below |

## Review checks

Check applicable empty, focused, populated, disabled/enabled commit, cancel, dirty-dismiss, saved, validation, error, switch on/off, slider position, picker selection, and destructive isolation and consequence footer states. A missing visible error in these pre-commit captures is a gap, not proof of validity.
