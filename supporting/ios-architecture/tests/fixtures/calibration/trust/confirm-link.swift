import SwiftUI
struct RootView: View {
    @State private var pendingProduct: ProductID?
    var body: some View {
        HomeView()
            .onOpenURL { url in
                guard case .buy(let product)? = AppRoute(url: url) else { return }
                pendingProduct = product
            }
            .sheet(item: $pendingProduct) { product in
                ConfirmPurchaseView(product: product)
            }
    }
}
