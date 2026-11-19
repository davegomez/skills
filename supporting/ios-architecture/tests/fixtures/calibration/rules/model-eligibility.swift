import Observation
@Observable final class CheckoutModel {
    var user: User
    var canBuyAlcohol = false
    init(user: User) { self.user = user }
    func refresh() {
        canBuyAlcohol = user.age >= 21 && user.country == "US" && !user.isSuspended
    }
}
