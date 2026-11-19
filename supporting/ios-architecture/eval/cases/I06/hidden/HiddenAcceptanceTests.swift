import XCTest

// Hidden acceptance tests for I06. They use only the public contract in task.md:
// EVAL_SCENARIO, the accessibility identifiers, and the pinned English and Spanish strings.
// Each test method maps to 1 check id in grade.sh.
final class HiddenAcceptanceTests: XCTestCase {
    private let timeout: TimeInterval = 15

    override func setUp() {
        continueAfterFailure = false
    }

    // MARK: States

    @MainActor
    func testStateLoading() {
        let app = launch("cancel")
        openList(app)
        XCTAssertTrue(element(app, "reading.loading").waitForExistence(timeout: timeout), "no loading state")
        XCTAssertTrue(label(app, "Loading books").exists, "loading text missing")
    }

    @MainActor
    func testStateList() {
        let app = launch("success")
        openList(app)
        XCTAssertTrue(element(app, "reading.list").waitForExistence(timeout: timeout), "no list")
        for title in ["Middlemarch", "The Age of Innocence", "Kindred"] {
            XCTAssertTrue(label(app, title).waitForExistence(timeout: timeout), "missing \(title)")
        }
        XCTAssertTrue(label(app, "Reading List").exists, "title missing")
        XCTAssertFalse(element(app, "reading.error").exists, "error shown on success")
    }

    @MainActor
    func testStateEmpty() {
        let app = launch("empty")
        openList(app)
        XCTAssertTrue(element(app, "reading.empty").waitForExistence(timeout: timeout), "no empty state")
        XCTAssertTrue(label(app, "No books yet").exists, "empty text missing")
        XCTAssertFalse(element(app, "reading.error").exists, "error shown on empty")
    }

    @MainActor
    func testStateError() {
        let app = launch("permanent")
        openList(app)
        XCTAssertTrue(element(app, "reading.error").waitForExistence(timeout: timeout), "no error state")
        XCTAssertTrue(label(app, "Could not load your reading list.").exists, "error text missing")
        let retry = element(app, "reading.retry")
        XCTAssertTrue(retry.exists, "no retry control")
        XCTAssertTrue(label(app, "Try Again").exists, "retry text missing")
    }

    @MainActor
    func testOfflineShowsCache() {
        let app = launch("offline")
        openList(app)
        XCTAssertTrue(label(app, "Persuasion").waitForExistence(timeout: timeout), "first load missing")
        goBack(app)
        openList(app)
        XCTAssertTrue(element(app, "reading.offline").waitForExistence(timeout: timeout), "no offline state")
        XCTAssertTrue(label(app, "You are offline. Showing saved books.").exists, "offline text missing")
        XCTAssertTrue(label(app, "Persuasion").exists, "cached books not shown")
        hold(3)
        XCTAssertFalse(label(app, "Beloved").exists, "offline load was retried automatically")
        XCTAssertTrue(element(app, "reading.offline").exists, "offline state replaced")
    }

    // MARK: Retry matrix

    @MainActor
    func testRetryTransientRecovers() {
        let app = launch("transient")
        openList(app)
        XCTAssertTrue(label(app, "Frankenstein").waitForExistence(timeout: timeout), "transient failure not retried to success")
        XCTAssertFalse(element(app, "reading.error").exists, "error shown after recovery")
    }

    @MainActor
    func testRetryTransientLimit() {
        let app = launch("transient-exhausted")
        openList(app)
        XCTAssertTrue(element(app, "reading.error").waitForExistence(timeout: timeout), "no error after 3 failed attempts")
        XCTAssertFalse(label(app, "Moby-Dick").exists, "more than 3 attempts")
        hold(3)
        XCTAssertFalse(label(app, "Moby-Dick").exists, "retried after the error state")
        element(app, "reading.retry").tap()
        XCTAssertTrue(label(app, "Moby-Dick").waitForExistence(timeout: timeout), "Try Again did not load")
    }

    @MainActor
    func testRetryPermanentNoRetry() {
        let app = launch("permanent")
        openList(app)
        XCTAssertTrue(element(app, "reading.error").waitForExistence(timeout: timeout), "no error state")
        hold(3)
        XCTAssertFalse(label(app, "Dubliners").exists, "permanent failure was retried")
        element(app, "reading.retry").tap()
        XCTAssertTrue(label(app, "Dubliners").waitForExistence(timeout: timeout), "Try Again did not load")
    }

    @MainActor
    func testRetryCancel() {
        let app = launch("cancel")
        openList(app)
        XCTAssertTrue(element(app, "reading.loading").waitForExistence(timeout: timeout), "no loading state")
        goBack(app)
        hold(2)
        XCTAssertFalse(element(app, "reading.error").exists, "cancellation shown as an error")
        XCTAssertEqual(app.alerts.count, 0, "cancellation raised an alert")
        openList(app)
        XCTAssertTrue(label(app, "Walden").waitForExistence(timeout: timeout), "cancelled load was retried or reopen failed")
        XCTAssertFalse(element(app, "reading.error").exists, "error after reopen")
    }

    // MARK: Second locale

    @MainActor
    func testSecondLocale() {
        var app = launch("success", spanish: true)
        openList(app)
        XCTAssertTrue(label(app, "Kindred").waitForExistence(timeout: timeout), "list missing")
        XCTAssertTrue(label(app, "Lista de lectura").exists, "title not in Spanish")

        app = launch("empty", spanish: true)
        openList(app)
        XCTAssertTrue(label(app, "Todavía no hay libros").waitForExistence(timeout: timeout), "empty text not in Spanish")

        app = launch("permanent", spanish: true)
        openList(app)
        XCTAssertTrue(label(app, "No se pudo cargar tu lista de lectura.").waitForExistence(timeout: timeout), "error text not in Spanish")
        XCTAssertTrue(label(app, "Reintentar").exists, "retry text not in Spanish")

        app = launch("cancel", spanish: true)
        openList(app)
        XCTAssertTrue(label(app, "Cargando libros").waitForExistence(timeout: timeout), "loading text not in Spanish")

        app = launch("offline", spanish: true)
        openList(app)
        XCTAssertTrue(label(app, "Persuasion").waitForExistence(timeout: timeout), "first load missing")
        goBack(app)
        openList(app)
        XCTAssertTrue(label(app, "Sin conexión. Se muestran los libros guardados.").waitForExistence(timeout: timeout), "offline text not in Spanish")
    }

    // MARK: Accessibility

    @MainActor
    func testAccessibilityAudit() throws {
        for (scenario, id) in [("success", "reading.list"), ("empty", "reading.empty"), ("permanent", "reading.error")] {
            let app = launch(scenario)
            openList(app)
            XCTAssertTrue(element(app, id).waitForExistence(timeout: timeout), "\(scenario): state missing")
            // Contrast is left to the rubric: the audit flags system secondary colors as "nearly passed".
            try app.performAccessibilityAudit(for: XCUIAccessibilityAuditType.all.subtracting(.contrast))
        }
    }

    // MARK: Helpers

    @MainActor
    private func launch(_ scenario: String, spanish: Bool = false) -> XCUIApplication {
        let app = XCUIApplication()
        app.launchEnvironment["EVAL_SCENARIO"] = scenario
        let language = spanish ? ["-AppleLanguages", "(es)", "-AppleLocale", "es_ES"] : ["-AppleLanguages", "(en)", "-AppleLocale", "en_US"]
        app.launchArguments += language
        app.launch()
        return app
    }

    @MainActor
    private func openList(_ app: XCUIApplication) {
        let link = element(app, "home.readingList")
        XCTAssertTrue(link.waitForExistence(timeout: timeout), "home link missing")
        link.tap()
    }

    @MainActor
    private func goBack(_ app: XCUIApplication) {
        let back = app.navigationBars.buttons.element(boundBy: 0)
        XCTAssertTrue(back.waitForExistence(timeout: timeout), "no back button")
        back.tap()
        XCTAssertTrue(element(app, "home.readingList").waitForExistence(timeout: timeout), "did not return home")
    }

    @MainActor
    private func element(_ app: XCUIApplication, _ identifier: String) -> XCUIElement {
        app.descendants(matching: .any).matching(identifier: identifier).firstMatch
    }

    @MainActor
    private func label(_ app: XCUIApplication, _ text: String) -> XCUIElement {
        app.descendants(matching: .any).matching(NSPredicate(format: "label CONTAINS %@", text)).firstMatch
    }

    private func hold(_ seconds: TimeInterval) {
        _ = XCTWaiter.wait(for: [XCTestExpectation(description: "hold")], timeout: seconds)
    }
}
