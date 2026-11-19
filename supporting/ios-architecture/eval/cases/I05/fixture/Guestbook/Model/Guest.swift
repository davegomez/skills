import Foundation

nonisolated struct Guest: Codable, Identifiable, Hashable, Sendable {
    let id: UUID
    var name: String
    var email: String
    var tableNumber: Int
}

extension Guest {
    /// Synthetic guests shown on first launch.
    static let samples: [Guest] = [
        Guest(id: UUID(uuidString: "0B6D8E52-3C1A-4F7B-9A20-5E4D1C2B3A01")!, name: "Avery Lindqvist", email: "avery.lindqvist@example.com", tableNumber: 1),
        Guest(id: UUID(uuidString: "0B6D8E52-3C1A-4F7B-9A20-5E4D1C2B3A02")!, name: "Mateo Okonkwo", email: "mateo.okonkwo@example.com", tableNumber: 1),
        Guest(id: UUID(uuidString: "0B6D8E52-3C1A-4F7B-9A20-5E4D1C2B3A03")!, name: "Priya Castellanos", email: "priya.castellanos@example.com", tableNumber: 2),
        Guest(id: UUID(uuidString: "0B6D8E52-3C1A-4F7B-9A20-5E4D1C2B3A04")!, name: "Jonah Whitfield", email: "jonah.whitfield@example.com", tableNumber: 3),
    ]
}
