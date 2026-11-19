import SwiftUI
import os
import CheckoutDomain

private let logger = Logger(subsystem: "com.example.myapp", category: "Checkout")

@Observable
final class CheckoutModel {
    private(set) var state = CartState()

    func add(_ item: LineItem) {
        state = reduce(state, .add(item))
        logger.info("Added item \(item.id, privacy: .private(mask: .hash))")
    }
}

struct CheckoutView: View {
    @State private var model = CheckoutModel()

    var body: some View {
        NavigationStack {
            List(model.state.items) { item in
                Text(item.price, format: .currency(code: "USD"))
                    .font(.body)
            }
            .navigationTitle(Text("Checkout", bundle: .module))
        }
    }
}
