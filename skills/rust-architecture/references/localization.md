# Localization

Use Fluent (`fluent-bundle`) for user-facing messages in desktop apps and CLIs, and ICU4X (`icu`) for numbers, dates, and plural rules.

- **Desktop and CLI:** Load Fluent `.ftl` files per locale. Keep `--json` output locale-neutral (ISO 8601, `.` decimal).
- **Server:** Return error codes plus English text. Let clients localize.
- Keep message IDs stable. Never build sentences by joining fragments.
