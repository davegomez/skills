import Foundation

struct Note: Identifiable, Hashable, Codable, Sendable {
    let id: UUID
    var title: String
    var body: String
    var isArchived: Bool
    var createdAt: Date
}

enum SampleNotes {
    static let all: [Note] = [
        Note(
            id: UUID(uuidString: "11111111-1111-1111-1111-111111111111")!,
            title: "Groceries",
            body: "Milk, eggs, coffee beans",
            isArchived: false,
            createdAt: Date(timeIntervalSince1970: 1_767_225_600)
        ),
        Note(
            id: UUID(uuidString: "22222222-2222-2222-2222-222222222222")!,
            title: "Trip ideas",
            body: "Lisbon in spring, Kyoto in autumn",
            isArchived: false,
            createdAt: Date(timeIntervalSince1970: 1_767_312_000)
        ),
        Note(
            id: UUID(uuidString: "33333333-3333-3333-3333-333333333333")!,
            title: "Old receipts",
            body: "Scan and file the 2025 receipts",
            isArchived: true,
            createdAt: Date(timeIntervalSince1970: 1_735_689_600)
        ),
    ]
}
