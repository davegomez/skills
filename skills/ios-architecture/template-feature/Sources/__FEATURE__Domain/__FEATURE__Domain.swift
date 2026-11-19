import Foundation

public struct __FEATURE__Item: Identifiable, Equatable, Sendable {
    public let id: UUID
    public let title: String

    /// Trims the title, and rejects a title with no characters left.
    public static func make(id: UUID, title: String) throws(__FEATURE__Error) -> __FEATURE__Item {
        let trimmed = title.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !trimmed.isEmpty else { throw .emptyTitle }
        return __FEATURE__Item(id: id, title: trimmed)
    }
}

/// Expected failures. The feature layer maps each case to a user-facing message.
public enum __FEATURE__Error: Error, Equatable, Sendable {
    case emptyTitle
}

public struct __FEATURE__State: Equatable, Sendable {
    public var items: [__FEATURE__Item]
    public init(items: [__FEATURE__Item] = []) { self.items = items }
}

public enum __FEATURE__Action: Equatable, Sendable {
    case add(__FEATURE__Item)
    case remove(id: UUID)
    case clear
}

/// The pure reducer. Invariant: each item ID appears at most once.
public func reduce(_ state: __FEATURE__State, _ action: __FEATURE__Action) -> __FEATURE__State {
    var next = state
    switch action {
    case .add(let item):
        if !next.items.contains(where: { $0.id == item.id }) { next.items.append(item) }
    case .remove(let id):
        next.items.removeAll { $0.id == id }
    case .clear:
        next.items = []
    }
    return next
}
