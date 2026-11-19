import XCTest

/// Black-box tests of the I01 contract in task.md. They drive the installed app by bundle ID, so they do
/// not depend on the app's project layout or type names. grade.sh passes the bundle ID and installs a
/// fresh copy of the app before the run.
final class PackingListUITests: XCTestCase {
    override func setUp() {
        continueAfterFailure = false
    }

    @MainActor
    func testAddAndToggle() throws {
        let app = try launchedApp()
        add("Toothbrush", in: app)
        let row = row("Toothbrush", in: app)
        XCTAssertTrue(row.waitForExistence(timeout: 5), "no row for the new item")
        XCTAssertEqual(row.value as? String, "Not packed")
        activate(row)
        XCTAssertTrue(waitForValue("Packed", of: row), "the item did not become packed")
        activate(row)
        XCTAssertTrue(waitForValue("Not packed", of: row), "the item did not become not packed again")
    }

    @MainActor
    func testStateSurvivesRelaunch() throws {
        var app = try launchedApp()
        add("Passport", in: app)
        add("Charger", in: app)
        let passport = row("Passport", in: app)
        XCTAssertTrue(passport.waitForExistence(timeout: 5), "no row for the new item")
        activate(passport)
        XCTAssertTrue(waitForValue("Packed", of: passport), "the item did not become packed")
        // A user does not quit within milliseconds of a tap; give an asynchronous save time to finish.
        sleep(1)
        app.terminate()

        app = try launchedApp()
        let passportAgain = row("Passport", in: app)
        let chargerAgain = row("Charger", in: app)
        XCTAssertTrue(passportAgain.waitForExistence(timeout: 10), "Passport is missing after relaunch")
        XCTAssertTrue(chargerAgain.waitForExistence(timeout: 5), "Charger is missing after relaunch")
        XCTAssertEqual(passportAgain.value as? String, "Packed")
        XCTAssertEqual(chargerAgain.value as? String, "Not packed")
    }

    @MainActor
    func testListScreenAccessibilityAudit() throws {
        let app = try launchedApp()
        add("Sunscreen", in: app)
        XCTAssertTrue(row("Sunscreen", in: app).waitForExistence(timeout: 5), "no row for the new item")
        // The text-clipping heuristic flags plain one-line List rows and depends on list content, so it is
        // not a stable gate; rubric.md I01-R-dynamic-type covers large text instead.
        try app.performAccessibilityAudit(for: XCUIAccessibilityAuditType.all.subtracting(.textClipped))
    }

    // MARK: Contract helpers

    @MainActor
    private func launchedApp() throws -> XCUIApplication {
        let bundleID = try XCTUnwrap(ProcessInfo.processInfo.environment["EVAL_APP_BUNDLE_ID"], "EVAL_APP_BUNDLE_ID not set")
        let app = XCUIApplication(bundleIdentifier: bundleID)
        app.launchArguments += ["-AppleLanguages", "(en)", "-AppleLocale", "en_US"]
        app.launch()
        XCTAssertTrue(field(in: app).waitForExistence(timeout: 15), "no text field labelled 'Item name' on the first screen")
        return app
    }

    /// The task names the field by its accessibility label; a placeholder or identifier of the same text also counts.
    @MainActor
    private func field(in app: XCUIApplication) -> XCUIElement {
        app.textFields.matching(
            NSPredicate(format: "label == %@ OR placeholderValue == %@ OR identifier == %@", "Item name", "Item name", "Item name")
        ).firstMatch
    }

    @MainActor
    private func add(_ name: String, in app: XCUIApplication) {
        let field = field(in: app)
        field.tap()
        field.typeText(name)
        let button = app.buttons.matching(NSPredicate(format: "label == %@", "Add item")).firstMatch
        XCTAssertTrue(button.waitForExistence(timeout: 5), "no button labelled 'Add item'")
        button.tap()
    }

    /// The row of an item: 1 element whose label is the name and whose value is "Packed" or "Not packed".
    @MainActor
    private func row(_ name: String, in app: XCUIApplication) -> XCUIElement {
        app.descendants(matching: .any).matching(
            NSPredicate(format: "label == %@ AND (value == 'Packed' OR value == 'Not packed')", name)
        ).firstMatch
    }

    /// A tap on a row-wide switch hits its middle, so tap the inner switch when the row is a toggle.
    @MainActor
    private func activate(_ row: XCUIElement) {
        let inner = row.switches.firstMatch
        if row.elementType == .switch, inner.exists { inner.tap() } else { row.tap() }
    }

    private func waitForValue(_ value: String, of element: XCUIElement) -> Bool {
        let expectation = XCTNSPredicateExpectation(predicate: NSPredicate(format: "value == %@", value), object: element)
        return XCTWaiter().wait(for: [expectation], timeout: 5) == .completed
    }
}
