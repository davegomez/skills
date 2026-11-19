import SwiftUI
struct OrdersView: View {
    @State var model: OrdersModel
    var body: some View {
        List(model.orders) { order in
            HStack {
                Text(order.title)
                Spacer()
                Text(order.placedAt, format: .dateTime.day().month())
            }
        }
        .toolbar { Button("Refresh") { Task { await model.reload() } } }
    }
}
