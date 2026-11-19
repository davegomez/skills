import XCTest

/// Black-box tests of the I02 contract in task.md. They drive the installed app by bundle ID and find
/// elements by the labels and identifiers that task.md names, so a different internal design still passes.
final class OrderSummaryUITests: XCTestCase {
    private let entryLabel = "Order summary"

    override func setUp() {
        continueAfterFailure = false
    }

    @MainActor
    func testEntryReachableExactlyOnce() throws {
        let app = try launchedApp(scenario: nil)
        let entries = rootEntries(in: app)
        XCTAssertEqual(entries.count, 1, "want exactly 1 '\(entryLabel)' entry on the first screen, found \(entries.count)")
        entries[0].tap()
        XCTAssertTrue(element("order.total", in: app).waitForExistence(timeout: 10),
                      "the entry did not open a screen with the order total (no scenario set: sample order)")
    }

    @MainActor
    func testSampleOrderTotals() throws {
        let app = try openSummary(scenario: "sample")
        let total = element("order.total", in: app)
        XCTAssertTrue(total.waitForExistence(timeout: 10), "no element with identifier order.total")
        for (name, lineTotal) in [("Notebook", "$14.97"), ("Pen set", "$12.49"), ("Desk lamp", "$14.54")] {
            XCTAssertTrue(text(containing: name, in: app).exists, "line '\(name)' is missing")
            XCTAssertTrue(text(containing: lineTotal, in: app).exists, "line total \(lineTotal) of '\(name)' is missing")
        }
        assertAmount("order.subtotal", "$42.00", in: app)
        assertAmount("order.tax", "$3.47", in: app)
        assertAmount("order.total", "$45.47", in: app)
    }

    @MainActor
    func testEmptyState() throws {
        let app = try openSummary(scenario: "empty")
        XCTAssertTrue(text(containing: "Your order is empty", in: app).waitForExistence(timeout: 10),
                      "no 'Your order is empty.' message")
        XCTAssertFalse(element("order.total", in: app).exists, "an empty order still shows a total")
    }

    @MainActor
    func testErrorState() throws {
        let app = try openSummary(scenario: "error")
        let message = text(containing: "load your order", in: app)
        XCTAssertTrue(message.waitForExistence(timeout: 10), "no 'We couldn't load your order.' message")
        XCTAssertFalse(element("order.total", in: app).exists, "a failed load still shows a total")
        let retry = app.buttons.matching(NSPredicate(format: "label ==[c] %@", "Try again")).firstMatch
        XCTAssertTrue(retry.exists, "no 'Try again' button")
        retry.tap()
        // The fake always fails in this scenario, so the error stays.
        XCTAssertTrue(message.waitForExistence(timeout: 10), "the error message went away after 'Try again'")
    }

    // MARK: Contract helpers

    @MainActor
    private func launchedApp(scenario: String?) throws -> XCUIApplication {
        let bundleID = try XCTUnwrap(ProcessInfo.processInfo.environment["EVAL_APP_BUNDLE_ID"], "EVAL_APP_BUNDLE_ID not set")
        let app = XCUIApplication(bundleIdentifier: bundleID)
        app.launchArguments += ["-AppleLanguages", "(en)", "-AppleLocale", "en_US"]
        if let scenario { app.launchEnvironment["ORDER_SCENARIO"] = scenario }
        app.launch()
        return app
    }

    @MainActor
    private func openSummary(scenario: String) throws -> XCUIApplication {
        let app = try launchedApp(scenario: scenario)
        let entries = rootEntries(in: app)
        let entry = try XCTUnwrap(entries.first, "no '\(entryLabel)' entry on the first screen")
        entry.tap()
        return app
    }

    /// Hittable elements labelled "Order summary"; nested matches (a text inside its row) count once.
    @MainActor
    private func rootEntries(in app: XCUIApplication) -> [XCUIElement] {
        let query = app.descendants(matching: .any).matching(NSPredicate(format: "label ==[c] %@", entryLabel))
        _ = query.firstMatch.waitForExistence(timeout: 15)
        let kinds: Set<XCUIElement.ElementType> = [.button, .cell, .link, .staticText, .other]
        let candidates = query.allElementsBoundByIndex
            .filter { kinds.contains($0.elementType) && $0.isHittable }
            .sorted { $0.frame.width * $0.frame.height > $1.frame.width * $1.frame.height }
        var kept: [XCUIElement] = []
        for candidate in candidates {
            let frame = candidate.frame
            let nested = kept.contains { $0.frame.insetBy(dx: -2, dy: -2).contains(frame) || frame.insetBy(dx: -2, dy: -2).contains($0.frame) }
            if !nested { kept.append(candidate) }
        }
        return kept
    }

    @MainActor
    private func element(_ identifier: String, in app: XCUIApplication) -> XCUIElement {
        app.descendants(matching: .any).matching(identifier: identifier).firstMatch
    }

    @MainActor
    private func text(containing text: String, in app: XCUIApplication) -> XCUIElement {
        app.descendants(matching: .any).matching(
            NSPredicate(format: "label CONTAINS[c] %@ OR value CONTAINS[c] %@", text, text)
        ).firstMatch
    }

    /// The amount must be in the label or value of the identified element, or of a text inside it.
    @MainActor
    private func assertAmount(_ identifier: String, _ amount: String, in app: XCUIApplication) {
        let target = element(identifier, in: app)
        XCTAssertTrue(target.exists, "no element with identifier \(identifier)")
        let own = target.label + " " + ((target.value as? String) ?? "")
        let inner = target.descendants(matching: .any).matching(NSPredicate(format: "label CONTAINS %@", amount)).firstMatch
        XCTAssertTrue(own.contains(amount) || inner.exists, "\(identifier) shows '\(own)', want \(amount)")
    }
}
