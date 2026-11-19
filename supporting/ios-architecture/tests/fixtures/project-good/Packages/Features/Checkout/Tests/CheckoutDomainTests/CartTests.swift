import Testing
@testable import CheckoutDomain

@Test func addAppendsItem() {
    let item = LineItem(id: UUID(), price: 2)
    #expect(reduce(CartState(), .add(item)).items == [item])
}
