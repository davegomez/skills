# Accessibility

Make every surface usable without sight, without a mouse, and without color. For GPUI, assume nothing is accessible until you add IDs and roles and test with a screen reader.

| Need | GPUI behavior | Action |
| --- | --- | --- |
| Screen readers | AccessKit. Opt-in per element. | Add `id`, `role`, and a label to every element. Test with VoiceOver, NVDA, and Orca. |
| Keyboard navigation | Elements have `tab_index` and `tab_stop`. `Window` has `focus_next` and `focus_prev`. GPUI binds no Tab key by default. | Bind Tab and Shift+Tab to `focus_next` and `focus_prev`, as the `a11y.rs` example does. Test every flow without a mouse. |
| Focus | The element that the OS reports as focused can differ from the focused control. | Draw a visible focus ring. After each GPUI update, re-test with a screen reader which element is reported as focused. |
| Visibility | Elements clipped out of view can be reported as visible. | After each GPUI update, re-test with a screen reader that clipped elements are not reported as visible. |
| Contrast and high contrast | No automatic OS high-contrast theme. | Ship a high-contrast theme. Check 4.5:1 text contrast. |
| Reduced motion | `App` has a `reduce_motion` flag. The animation and image elements obey it. GPUI does not set it from the OS setting. | Read the OS setting. Call `cx.set_reduce_motion(true)` when it is set. |
| Text scaling | Not automatic. | Scale the theme's rem size from a user setting. |

**Warning:** Do not ship a GPUI app to screen-reader users without a manual test on every target OS.

- **CLI:** Never use color as the only signal. Respect `NO_COLOR`. Print progress as discrete lines when `TERM=dumb` or stdout is not a terminal. Give `--json` and `--quiet` on every command.
- **Server:** Return errors as RFC 9457 problem details (`application/problem+json`) with a clear `title` and `detail`. Publish API docs as accessible HTML.
