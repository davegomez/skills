import XCTest
final class CartTotalsTests: XCTestCase {
    func testBulkDiscount() {
        let rules = PriceRules()
        XCTAssertEqual(rules.total(of: .sample(count: 4)), 36)
    }
}
