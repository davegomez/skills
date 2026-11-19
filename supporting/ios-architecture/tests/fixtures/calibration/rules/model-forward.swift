import Observation
import CheckoutDomain
@Observable final class CartModel {
    private(set) var state = CartState()
    private let analytics: any AnalyticsClient
    init(analytics: any AnalyticsClient) { self.analytics = analytics }
    func add(_ item: LineItem) {
        state = reduce(state, .add(item))
        analytics.track(.itemAdded)
    }
}
