# Localization

Use String Catalogs in the app and in each package, and load package strings from the package bundle.

- Use `Localizable.xcstrings` for UI text and `InfoPlist.xcstrings` for permission purpose strings and the display name.
- Set `defaultLocalization` in each `Package.swift` that has resources.
- In a package, load strings with `#bundle` or `.module`. Do not use `.main`, because it points to the app bundle.
- Generated String Catalog symbols are `internal`. If another package needs a string, expose a `public` API that returns `LocalizedStringResource`.
- Use plural and device variations in the catalog. Do not build plural strings in code.
- Format dates, numbers, currency, and measurements with `FormatStyle`. Do not format them by hand.
- Use leading and trailing, not left and right. Test right-to-left layout with a pseudo-language.
- Test the longest supported language at the largest text size.
- Send the catalogs to translators with comments that give context for each string.
