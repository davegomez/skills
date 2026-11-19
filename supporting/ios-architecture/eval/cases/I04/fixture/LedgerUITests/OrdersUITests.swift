import XCTest

@MainActor
final class OrdersUITests: XCTestCase {
    private var app: XCUIApplication!

    override func setUp() async throws {
        continueAfterFailure = false
        app = XCUIApplication()
    }

    /// Serves `json` as the orders feed through a data URL, so the test needs no network.
    private func launch(feed json: String) {
        app.launchEnvironment["LEDGER_ORDERS_URL"] = "data:application/json;base64," + Data(json.utf8).base64EncodedString()
        app.launch()
    }

    func testShowsTotalsForFeed() {
        launch(feed: #"{"lines":[{"sku":"A1","name":"Notebook","qty":2,"unit_price_cents":1250},{"sku":"B2","name":"Pen","qty":1,"unit_price_cents":399}]}"#)
        app.cells["home.orders"].tap()
        XCTAssertTrue(app.staticTexts["orders.total"].waitForExistence(timeout: 5))
        XCTAssertTrue(app.cells["orders.line.A1"].waitForExistence(timeout: 5))
        XCTAssertEqual(app.staticTexts["orders.subtotal"].label, "Subtotal $28.99")
        XCTAssertEqual(app.staticTexts["orders.discount"].label, "Discount $0.00")
        XCTAssertEqual(app.staticTexts["orders.tax"].label, "Tax $2.39")
        XCTAssertEqual(app.staticTexts["orders.total"].label, "Total $31.38")
    }

    func testNavigatesToSettings() {
        launch(feed: #"{"lines":[]}"#)
        app.cells["home.settings"].tap()
        XCTAssertTrue(app.switches["settings.showCents"].waitForExistence(timeout: 5))
    }
}
