import Foundation
struct Money: Equatable, Sendable {
    var amount: Decimal
    var currency: String
    func adding(_ other: Money) -> Money? {
        guard currency == other.currency else { return nil }
        return Money(amount: amount + other.amount, currency: currency)
    }
}
