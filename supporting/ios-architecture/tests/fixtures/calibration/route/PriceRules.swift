public struct PriceRules: Sendable, Equatable {
    public var bulkThreshold = 3
    public func total(of items: [LineItem]) -> Decimal {
        let subtotal = items.reduce(0) { $0 + $1.price * Decimal($1.quantity) }
        return items.count > bulkThreshold ? subtotal * 0.9 : subtotal
    }
}
