import SwiftUI
import StoreKit

@Observable
final class OrderStore {
    var orders: [Order] = []
}

public struct Order: Sendable {
    public var id: String
}

func isPremium() async -> Bool {
    for await _ in Transaction.currentEntitlements { return true }
    return false
}
