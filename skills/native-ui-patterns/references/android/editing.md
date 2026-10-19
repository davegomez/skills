# Android editing and controls

## Guidance

**Observed:** Contacts used a full-page create form; Messages focused recipient choice before composition; Clock offered graphical/text time entry; Files used a folder dialog. Settings/Clock exposed trailing unchecked switches, and Phone/Maps/Files used labeled compact controls. Safe temporary inputs often produced no visible authored error. Modified Contacts showed a discard/save dialog. **Inferred adaptation:** keep save/exit stable, label fields independently, distinguish control state visually/semantically, pair commit/cancel, and explain rejected input. Save/send/OK validation and created outcomes remain **Unconfirmed**.

## Visual references

Choose the exact visual question and open only its named state or explicit comparison pair. Initial and return context are separate questions.

| Visual question / state | Matching capture(s) | What to inspect |
| --- | --- | --- |
| Contact form resting or focused | [create form](../../assets/android/contacts/create-form.png) or [focused form](../../assets/android/contacts/create-form-focused.png) | Open only the requested state; inspect top actions, fields/repeatable rows, keyboard, and surrounding form |
| Contact invalid email | [invalid email](../../assets/android/contacts/invalid-email.png) | Input placement and absent visible inline feedback |
| Contact dirty-dismiss prompt | [invalid-email discard prompt](../../assets/android/contacts/invalid-email-discard-prompt.png) or alternate [unsaved-changes dialog](../../assets/android/contacts/unsaved-changes-dialog.png) | Choose the relevant edit path; inspect dialog/action placement and destructive/preserving separation |
| Contact entry or discarded return context | [list before validation](../../assets/android/contacts/empty-list-before-validation.png) or [list after discard](../../assets/android/contacts/empty-list-after-discard.png) | Open only when entry/return context matters; inspect restored list and surrounding controls |
| Recipient form resting state | [recipient form](../../assets/android/messages/recipient-form.png) or [empty field](../../assets/android/messages/recipient-empty.png) | Choose the relevant resting capture; inspect recipient field, keyboard, Back, and surrounding suggestions |
| Recipient failed attempt | [invalid submit](../../assets/android/messages/recipient-invalid-submit.png) or [no match](../../assets/android/messages/recipient-no-match.png) | Open only the attempted state under review; inspect candidate area and absent authored feedback |
| Recipient short-number candidate | [short-number candidate](../../assets/android/messages/recipient-short-number-candidate.png) | Candidate placement and relationship to the focused field |
| Recipient cancellation result | [empty list after cancel](../../assets/android/messages/empty-list-after-recipient-cancel.png) | Restored list; open only when cancel outcome matters |
| Graphical versus text time entry | [graphical picker](../../assets/android/clock/time-picker.png) and [text-input mode](../../assets/android/clock/time-input-text-mode.png) | Dialog bounds, mode control, input alignment, and Cancel/OK placement |
| Alternate selected-time context before text mode | [picker before text mode](../../assets/android/clock/time-picker-before-text-mode.png) | Initial selected time and surrounding picker; open only when that context matters |
| Invalid-hour attempt | [invalid hour](../../assets/android/clock/time-input-invalid-hour.png) | Unchanged value and absent explanatory feedback; open only for invalid-input review |
| Time-picker cancellation result | [alarm list after cancel](../../assets/android/clock/alarm-list-after-cancel.png) | Restored alarm content; open only when cancellation outcome matters |
| New-folder empty versus invalid input | [empty dialog](../../assets/android/files/new-folder-empty.png) and [invalid name](../../assets/android/files/new-folder-invalid-name.png) | Dialog/field/actions, keyboard spacing, and absent feedback |
| Folder entry or cancellation context | [Downloads before](../../assets/android/files/downloads-before-folder.png) or [Downloads after cancel](../../assets/android/files/downloads-after-folder-cancel.png) | Open only when entry/return context matters; inspect surrounding Downloads state |
| Trailing switch and row hierarchy | Settings [Display & touch](../../assets/android/settings/display-and-touch.png) or Clock [Alarm list](../../assets/android/clock/alarm-list.png) | Open the relevant app; inspect label/state adjacency, nested target placement, and grouping |
| Compact filters/categories | Phone [Home](../../assets/android/phone/empty-home.png), Maps [Explore](../../assets/android/maps/sheet-collapsed.png), or Files [Downloads](../../assets/android/files/downloads-empty.png) | Open only the relevant app; inspect filled selection, label/icon spacing, and surrounding content |

## Review checks

Check applicable empty/focused/populated, selected/unchecked, invalid, confirm/cancel, dirty dismissal, saved, and error states. Silent retention/rejection in a pre-commit capture is an evidence gap, not valid-input guidance.
