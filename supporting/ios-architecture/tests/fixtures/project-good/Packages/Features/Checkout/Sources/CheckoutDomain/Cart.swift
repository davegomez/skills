import Foundation

public struct LineItem: Equatable, Sendable, Identifiable {
    public let id: UUID
    public var price: Decimal
}

public struct CartState: Equatable, Sendable {
    public var items: [LineItem] = []
    public init() {}
}

public enum CartAction: Sendable {
    case add(LineItem)
    case clear
}

public func reduce(_ state: CartState, _ action: CartAction) -> CartState {
    var next = state
    switch action {
    case .add(let item): next.items.append(item)
    case .clear: next.items = []
    }
    return next
}
