import SwiftUI
struct CartView: View {
    let items: [LineItem]
    var total: Decimal {
        let subtotal = items.reduce(0) { $0 + $1.price * Decimal($1.quantity) }
        let discounted = items.count > 3 ? subtotal * 0.9 : subtotal
        return discounted * 1.08
    }
    var body: some View {
        List(items) { item in Text(item.name) }
        Text(total, format: .currency(code: "USD"))
    }
}
