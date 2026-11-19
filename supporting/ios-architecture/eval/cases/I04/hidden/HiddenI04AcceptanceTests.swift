import XCTest

// Hidden acceptance tests for case I04. They rely only on the contract in task.md: the
// LEDGER_ORDERS_URL override, the screen's accessibility identifiers, and the persisted cache
// at Application Support/ledger/orders-cache.json. grade.sh passes the built app's bundle
// identifier in LEDGER_BUNDLE_ID.
@MainActor
final class HiddenI04AcceptanceTests: XCTestCase {
    private struct Expected {
        let subtotal, discount, tax, total: String
        let rows: Int
    }

    private static let offlineFeed = "file:///nonexistent/ledger-offline-feed.json"

    private static let feedA = #"{"lines":[{"sku":"A1","name":"Notebook","qty":2,"unit_price_cents":1250},{"sku":"B2","name":"Pen","qty":1,"unit_price_cents":399}]}"#
    private static let expectedA = Expected(subtotal: "Subtotal $28.99", discount: "Discount $0.00", tax: "Tax $2.39", total: "Total $31.38", rows: 2)

    private static let feedB = #"{"lines":[{"sku":"C3","name":"Desk lamp","qty":1,"unit_price_cents":10000}]}"#
    private static let expectedB = Expected(subtotal: "Subtotal $100.00", discount: "Discount -$10.00", tax: "Tax $7.43", total: "Total $97.43", rows: 1)

    private static let feedC = #"{"lines":[{"sku":"D4","name":"Chair","qty":3,"unit_price_cents":4999},{"sku":"E5","name":"Return","qty":-1,"unit_price_cents":4999},{"sku":"F6","name":"Sample","qty":0,"unit_price_cents":500}]}"#
    private static let expectedC = Expected(subtotal: "Subtotal $149.97", discount: "Discount -$15.00", tax: "Tax $11.14", total: "Total $146.11", rows: 3)

    private static let feedD = #"{"lines":[{"sku":"G7","name":"Monitor","qty":1,"unit_price_cents":10005}]}"#
    private static let expectedD = Expected(subtotal: "Subtotal $100.05", discount: "Discount -$10.01", tax: "Tax $7.43", total: "Total $97.47", rows: 1)

    private static let feedE = #"{"lines":[{"sku":"H8","name":"Stickers","qty":4,"unit_price_cents":50}]}"#
    private static let expectedE = Expected(subtotal: "Subtotal $2.00", discount: "Discount $0.00", tax: "Tax $0.17", total: "Total $2.17", rows: 1)

    /// Bytes the version 1.0 app wrote after a successful load.
    private static let cacheWrittenByOldVersion = #"{"lines":[{"name":"Desk lamp","qty":1,"sku":"C3","unit_price_cents":10000},{"name":"Notebook","qty":2,"sku":"A1","unit_price_cents":1250}],"saved_at":1767225600.512345,"version":1}"#
    private static let expectedOldCache = Expected(subtotal: "Subtotal $125.00", discount: "Discount -$12.50", tax: "Tax $9.28", total: "Total $121.78", rows: 2)

    private var app: XCUIApplication!

    override func setUp() async throws {
        continueAfterFailure = false
        app = XCUIApplication()
        try? FileManager.default.removeItem(at: cacheFile())
    }

    // MARK: - Helpers

    /// The app's cache file. The simulator moves the data container when xcodebuild reinstalls
    /// the app, so find it on every use through the container metadata, beside the runner's own.
    private func cacheFile() throws -> URL {
        let bundleID = ProcessInfo.processInfo.environment["LEDGER_BUNDLE_ID"] ?? "com.example.ledger"
        let containers = URL(fileURLWithPath: NSHomeDirectory()).deletingLastPathComponent()
        func find() throws -> URL? {
            for dir in try FileManager.default.contentsOfDirectory(at: containers, includingPropertiesForKeys: nil) {
                let metadata = dir.appendingPathComponent(".com.apple.mobile_container_manager.metadata.plist")
                if NSDictionary(contentsOf: metadata)?["MCMMetadataIdentifier"] as? String == bundleID {
                    return dir.appendingPathComponent("Library/Application Support/ledger/orders-cache.json")
                }
            }
            return nil
        }
        var file = try find()
        if file == nil {
            // A fresh install has no container until its first launch.
            app.launch()
            app.terminate()
            file = try find()
        }
        guard let file else { throw CacheError.noContainer(bundleID) }
        try FileManager.default.createDirectory(at: file.deletingLastPathComponent(), withIntermediateDirectories: true)
        return file
    }

    private enum CacheError: Error {
        case noContainer(String)
    }

    private static func feed(_ json: String) -> String {
        "data:application/json;base64," + Data(json.utf8).base64EncodedString()
    }

    private func launchOrders(feed: String) {
        if app.state != .notRunning { app.terminate() }
        app.launchEnvironment["LEDGER_ORDERS_URL"] = feed
        app.launch()
        let orders = app.cells["home.orders"]
        XCTAssertTrue(orders.waitForExistence(timeout: 10), "home screen has no Orders row")
        orders.tap()
        XCTAssertTrue(app.staticTexts["orders.total"].waitForExistence(timeout: 10), "orders screen did not open")
    }

    private func rowCount() -> Int {
        app.cells.matching(NSPredicate(format: "identifier BEGINSWITH 'orders.line.'")).count
    }

    private func assertShows(_ expected: Expected, _ context: String, file: StaticString = #filePath, line: UInt = #line) {
        let pairs = [("orders.subtotal", expected.subtotal), ("orders.discount", expected.discount),
                     ("orders.tax", expected.tax), ("orders.total", expected.total)]
        for (identifier, text) in pairs {
            let element = app.staticTexts[identifier]
            let shown = XCTNSPredicateExpectation(predicate: NSPredicate(format: "label == %@", text), object: element)
            let outcome = XCTWaiter().wait(for: [shown], timeout: 10)
            XCTAssertEqual(outcome, .completed, "\(context): \(identifier) shows '\(element.label)', expected '\(text)'", file: file, line: line)
        }
        XCTAssertEqual(rowCount(), expected.rows, "\(context): wrong number of order lines", file: file, line: line)
    }

    private func cacheJSON() throws -> [String: Any] {
        let data = try Data(contentsOf: cacheFile())
        return try XCTUnwrap(JSONSerialization.jsonObject(with: data) as? [String: Any], "cache is not a JSON object")
    }

    // MARK: - Checks

    /// I04-characterization
    func testTotalsMatchLegacyBehavior() {
        let cases = [("under the discount threshold", Self.feedA, Self.expectedA),
                     ("exactly at the threshold", Self.feedB, Self.expectedB),
                     ("zero and negative quantities", Self.feedC, Self.expectedC),
                     ("discount rounds half up", Self.feedD, Self.expectedD),
                     ("tax rounds half up", Self.feedE, Self.expectedE)]
        for (name, feed, expected) in cases {
            try? FileManager.default.removeItem(at: cacheFile())
            launchOrders(feed: Self.feed(feed))
            assertShows(expected, name)
        }
    }

    /// I04-old-data-loads
    func testLoadsCacheWrittenByOldVersion() throws {
        try Data(Self.cacheWrittenByOldVersion.utf8).write(to: cacheFile())
        launchOrders(feed: Self.offlineFeed)
        assertShows(Self.expectedOldCache, "offline with the old cache")
        XCTAssertTrue(app.cells["orders.line.C3"].exists)
        XCTAssertTrue(app.cells["orders.line.A1"].exists)
    }

    /// I04-ids-and-keys-unchanged
    func testSavesCacheInLegacyFormat() throws {
        launchOrders(feed: Self.feed(Self.feedA))
        assertShows(Self.expectedA, "online")
        let cache = try cacheJSON()
        XCTAssertEqual(Set(cache.keys), ["version", "saved_at", "lines"])
        XCTAssertEqual(cache["version"] as? Int, 1)
        XCTAssertNotNil(cache["saved_at"] as? NSNumber, "saved_at is not seconds since 1970")
        let lines = try XCTUnwrap(cache["lines"] as? [[String: Any]])
        XCTAssertEqual(lines.count, 2)
        for line in lines {
            XCTAssertEqual(Set(line.keys), ["sku", "name", "qty", "unit_price_cents"])
        }
        XCTAssertEqual(lines.first?["sku"] as? String, "A1")
        XCTAssertEqual(lines.first?["qty"] as? Int, 2)
        XCTAssertEqual(lines.first?["unit_price_cents"] as? Int, 1250)

        launchOrders(feed: Self.offlineFeed)
        assertShows(Self.expectedA, "offline after an online load")
    }

    /// I04-interrupted-repeated-load
    func testRecoversFromInterruptedCacheWrite() throws {
        // A write cut off halfway leaves a truncated file.
        let truncated = Data(Self.cacheWrittenByOldVersion.utf8).prefix(57)
        try truncated.write(to: cacheFile())
        launchOrders(feed: Self.offlineFeed)
        XCTAssertEqual(app.state, .runningForeground, "app stopped on a truncated cache")
        assertShows(Expected(subtotal: "Subtotal $0.00", discount: "Discount $0.00", tax: "Tax $0.00", total: "Total $0.00", rows: 0),
                    "offline with a truncated cache")

        launchOrders(feed: Self.feed(Self.feedB))
        assertShows(Self.expectedB, "online after a truncated cache")
        XCTAssertEqual(try cacheJSON()["version"] as? Int, 1, "cache was not rewritten")
        launchOrders(feed: Self.offlineFeed)
        assertShows(Self.expectedB, "offline after the cache was repaired")
    }

    /// I04-interrupted-repeated-load
    func testRepeatedReloadDoesNotDuplicate() {
        launchOrders(feed: Self.feed(Self.feedC))
        assertShows(Self.expectedC, "first load")
        let reload = app.buttons["orders.reload"]
        for _ in 0..<3 { reload.tap() }
        assertShows(Self.expectedC, "after 3 reloads")

        // Leaving and reopening the screen loads again.
        app.navigationBars.buttons.element(boundBy: 0).tap()
        app.cells["home.orders"].tap()
        assertShows(Self.expectedC, "after reopening the screen")

        launchOrders(feed: Self.offlineFeed)
        assertShows(Self.expectedC, "offline after repeated loads")
    }

    /// I04-navigation-unchanged
    func testNavigationUnchanged() {
        app.launchEnvironment["LEDGER_ORDERS_URL"] = Self.feed(Self.feedA)
        app.launch()
        XCTAssertTrue(app.navigationBars["Ledger"].waitForExistence(timeout: 10))
        app.cells["home.orders"].tap()
        XCTAssertTrue(app.navigationBars["Orders"].waitForExistence(timeout: 5))
        XCTAssertTrue(app.buttons["orders.reload"].exists)
        app.navigationBars.buttons.element(boundBy: 0).tap()
        app.cells["home.settings"].tap()
        XCTAssertTrue(app.navigationBars["Settings"].waitForExistence(timeout: 5))
        XCTAssertTrue(app.switches["settings.showCents"].exists)
        app.navigationBars.buttons.element(boundBy: 0).tap()
        XCTAssertTrue(app.navigationBars["Ledger"].waitForExistence(timeout: 5))
    }
}
