// swiftlint:disable all
// Generated using SwiftGen — https://github.com/SwiftGen/SwiftGen
// DO NOT EDIT. Run `swiftgen` after changing Localizable.strings.

import Foundation

// swiftlint:disable superfluous_disable_command file_length implicit_return prefer_self_in_static_references

// MARK: - Strings

// swiftlint:disable explicit_type_interface function_parameter_count identifier_name line_length
// swiftlint:disable nesting type_body_length type_name vertical_whitespace_opening_braces
internal enum L10n {
  internal enum Home {
    /// Orders
    internal static let orders = L10n.tr("Localizable", "home.orders", fallback: "Orders")
    /// Settings
    internal static let settings = L10n.tr("Localizable", "home.settings", fallback: "Settings")
    /// Ledger
    internal static let title = L10n.tr("Localizable", "home.title", fallback: "Ledger")
  }
  internal enum Orders {
    /// Discount %@
    internal static func discount(_ p1: Any) -> String {
      return L10n.tr("Localizable", "orders.discount", String(describing: p1), fallback: "Discount %@")
    }
    /// Reload
    internal static let reload = L10n.tr("Localizable", "orders.reload", fallback: "Reload")
    /// Subtotal %@
    internal static func subtotal(_ p1: Any) -> String {
      return L10n.tr("Localizable", "orders.subtotal", String(describing: p1), fallback: "Subtotal %@")
    }
    /// Tax %@
    internal static func tax(_ p1: Any) -> String {
      return L10n.tr("Localizable", "orders.tax", String(describing: p1), fallback: "Tax %@")
    }
    /// Orders
    internal static let title = L10n.tr("Localizable", "orders.title", fallback: "Orders")
    /// Total %@
    internal static func total(_ p1: Any) -> String {
      return L10n.tr("Localizable", "orders.total", String(describing: p1), fallback: "Total %@")
    }
    internal enum Line {
      /// %d × %@
      internal static func detail(_ p1: Int, _ p2: Any) -> String {
        return L10n.tr("Localizable", "orders.line.detail", p1, String(describing: p2), fallback: "%d × %@")
      }
    }
    internal enum Status {
      /// No saved orders
      internal static let empty = L10n.tr("Localizable", "orders.status.empty", fallback: "No saved orders")
      /// Loading…
      internal static let loading = L10n.tr("Localizable", "orders.status.loading", fallback: "Loading…")
      /// Offline. Showing saved orders.
      internal static let offline = L10n.tr("Localizable", "orders.status.offline", fallback: "Offline. Showing saved orders.")
      /// Up to date
      internal static let updated = L10n.tr("Localizable", "orders.status.updated", fallback: "Up to date")
    }
  }
  internal enum Settings {
    /// Show cents
    internal static let showCents = L10n.tr("Localizable", "settings.showCents", fallback: "Show cents")
    /// Settings
    internal static let title = L10n.tr("Localizable", "settings.title", fallback: "Settings")
    /// Version %@
    internal static func version(_ p1: Any) -> String {
      return L10n.tr("Localizable", "settings.version", String(describing: p1), fallback: "Version %@")
    }
  }
}
// swiftlint:enable explicit_type_interface function_parameter_count identifier_name line_length
// swiftlint:enable nesting type_body_length type_name vertical_whitespace_opening_braces

// MARK: - Implementation Details

extension L10n {
  private static func tr(_ table: String, _ key: String, _ args: CVarArg..., fallback value: String) -> String {
    let format = BundleToken.bundle.localizedString(forKey: key, value: value, table: table)
    return String(format: format, locale: Locale.current, arguments: args)
  }
}

// swiftlint:disable convenience_type
private final class BundleToken {
  static let bundle: Bundle = {
    #if SWIFT_PACKAGE
    return Bundle.module
    #else
    return Bundle(for: BundleToken.self)
    #endif
  }()
}
// swiftlint:enable convenience_type
