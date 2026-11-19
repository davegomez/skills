import Foundation

// Kept for the old dashboard. Events go nowhere until the new vendor ships.
class LegacyAnalytics {
    static let shared = LegacyAnalytics()
    private var events: [String] = []

    func track(_ name: String) {
        events.append(name)
        #if DEBUG
        NSLog("[analytics] %@", name)
        #endif
    }
}
