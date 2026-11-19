import FeatureKit

/// Every destination of the root navigation stack. `Codable`, so that navigation state can be restored.
nonisolated enum AppRoute: Hashable, Codable {
    case feature(FeatureID)
}
