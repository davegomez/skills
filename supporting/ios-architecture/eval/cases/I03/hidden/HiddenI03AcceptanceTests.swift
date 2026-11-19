import XCTest

// Hidden acceptance tests for case I03. They rely only on the contract in task.md:
// the link format, the 2 preview button identifiers, the `-uitest-seed` sample notes,
// and the fixture's visible screens.
@MainActor
final class HiddenI03AcceptanceTests: XCTestCase {
    private let groceriesID = "11111111-1111-1111-1111-111111111111"
    private let archivedID = "33333333-3333-3333-3333-333333333333"
    private var app: XCUIApplication!

    private var confirmButton: XCUIElement { app.buttons["archive-preview.confirm"] }
    private var cancelButton: XCUIElement { app.buttons["archive-preview.cancel"] }

    override func setUp() async throws {
        continueAfterFailure = false
        app = XCUIApplication()
        app.launchArguments = ["-uitest-seed"]
        app.launch()
        XCTAssertTrue(app.staticTexts["Groceries"].waitForExistence(timeout: 10), "seeded list did not load")
    }

    // MARK: - Helpers

    /// Opens the link through the system, as a tapped link would. `XCUIApplication.open`
    /// relaunches the app with its launch arguments, which would reset the seeded data.
    private func open(_ link: String) {
        XCUIDevice.shared.system.open(URL(string: link)!)
    }

    private func groceriesLink() -> String {
        "quicknotes://notes/\(groceriesID)/archive"
    }

    private func dismissAlertIfPresent() {
        let alert = app.alerts.firstMatch
        if alert.waitForExistence(timeout: 1) {
            alert.buttons.firstMatch.tap()
            XCTAssertTrue(alert.waitForNonExistence(timeout: 5))
        }
    }

    private func relaunchWithoutSeed() {
        app.terminate()
        app.launchArguments = []
        app.launch()
        XCTAssertTrue(app.staticTexts["Trip ideas"].waitForExistence(timeout: 10), "list did not load after relaunch")
    }

    private func count(_ title: String) -> Int {
        app.staticTexts.matching(NSPredicate(format: "label == %@", title)).count
    }

    /// Asserts that Groceries is active: shown in Notes, absent from Archived.
    private func assertGroceriesActive(_ message: String) {
        XCTAssertTrue(app.staticTexts["Groceries"].waitForExistence(timeout: 5), message)
        app.buttons["Archived"].tap()
        XCTAssertTrue(app.staticTexts["Old receipts"].waitForExistence(timeout: 5))
        XCTAssertEqual(count("Groceries"), 0, message)
        app.navigationBars.buttons.element(boundBy: 0).tap()
        XCTAssertTrue(app.staticTexts["Trip ideas"].waitForExistence(timeout: 5))
    }

    /// Asserts that Groceries is archived exactly once.
    private func assertGroceriesArchivedOnce(_ message: String) {
        XCTAssertTrue(app.staticTexts["Trip ideas"].waitForExistence(timeout: 5))
        XCTAssertEqual(count("Groceries"), 0, message)
        app.buttons["Archived"].tap()
        XCTAssertTrue(app.staticTexts["Old receipts"].waitForExistence(timeout: 5))
        XCTAssertEqual(count("Groceries"), 1, message)
        app.navigationBars.buttons.element(boundBy: 0).tap()
        XCTAssertTrue(app.staticTexts["Trip ideas"].waitForExistence(timeout: 5))
    }

    // MARK: - Checks

    /// I03-valid-link-confirmation
    func testValidLinkShowsConfirmation() {
        // Leave the Notes list so the title on screen can only come from the preview.
        app.buttons["Archived"].tap()
        XCTAssertTrue(app.staticTexts["Old receipts"].waitForExistence(timeout: 5))
        open(groceriesLink())
        XCTAssertTrue(confirmButton.waitForExistence(timeout: 10), "preview did not appear for a valid link")
        XCTAssertTrue(cancelButton.exists, "preview has no cancel button")
        XCTAssertTrue(app.staticTexts["Groceries"].exists, "preview does not show the note title")
        cancelButton.tap()
        XCTAssertTrue(confirmButton.waitForNonExistence(timeout: 5))

        // Cold start: the link launches the app and still reaches the preview.
        app.terminate()
        open(groceriesLink())
        XCTAssertTrue(confirmButton.waitForExistence(timeout: 15), "preview did not appear on a cold start")
    }

    /// I03-malformed-link-rejected
    func testMalformedAndUnknownLinksAreRejected() {
        let links = [
            "quicknotes://notes/not-a-uuid/archive",
            "quicknotes://notes/99999999-9999-9999-9999-999999999999/archive",
            "quicknotes://notes/\(groceriesID)/delete",
            "quicknotes://notes/\(groceriesID)/archive/extra",
            "quicknotes://notes/\(groceriesID)",
            "quicknotes://notes//archive",
            "quicknotes://settings/\(groceriesID)/archive",
            "quicknotes://notes/../notes/\(groceriesID)/archive",
            "quicknotes://notes/\(groceriesID)%00/archive",
            "quicknotes://notes/\(archivedID)/archive",
            "quicknotes://notes/\(String(repeating: "a", count: 4_000))/archive",
        ]
        for link in links {
            open(link)
            XCTAssertFalse(confirmButton.waitForExistence(timeout: 2), "preview appeared for \(link.prefix(80))")
            XCTAssertEqual(app.state, .runningForeground, "app is not running after \(link.prefix(80))")
            dismissAlertIfPresent()
        }
        relaunchWithoutSeed()
        assertGroceriesActive("rejected links changed data")
        app.buttons["Archived"].tap()
        XCTAssertTrue(app.staticTexts["Old receipts"].waitForExistence(timeout: 5), "archived note changed")
    }

    /// I03-link-needs-confirmation
    func testLinkAloneDoesNotChangeState() {
        open(groceriesLink())
        _ = confirmButton.waitForExistence(timeout: 10)
        relaunchWithoutSeed()
        assertGroceriesActive("the link changed data without a confirmation")
    }

    /// I03-cancel-keeps-data
    func testCancelKeepsData() {
        open(groceriesLink())
        XCTAssertTrue(confirmButton.waitForExistence(timeout: 10))
        cancelButton.tap()
        XCTAssertTrue(confirmButton.waitForNonExistence(timeout: 5), "preview stayed open after cancel")
        assertGroceriesActive("cancel changed data")
        relaunchWithoutSeed()
        assertGroceriesActive("cancel changed stored data")
    }

    /// I03-confirm-archives-once
    func testConfirmArchivesExactlyOnce() {
        open(groceriesLink())
        XCTAssertTrue(confirmButton.waitForExistence(timeout: 10))
        confirmButton.tap()
        XCTAssertTrue(confirmButton.waitForNonExistence(timeout: 5), "preview stayed open after confirm")
        assertGroceriesArchivedOnce("confirm did not archive the note once")

        // The same link again must not offer to archive, or undo, an archived note.
        open(groceriesLink())
        XCTAssertFalse(confirmButton.waitForExistence(timeout: 2), "preview appeared for an archived note")
        dismissAlertIfPresent()
        relaunchWithoutSeed()
        assertGroceriesArchivedOnce("stored state after confirm is wrong")
    }

    /// I03-existing-navigation
    func testExistingNavigationStillWorks() {
        open(groceriesLink())
        XCTAssertTrue(confirmButton.waitForExistence(timeout: 10))
        cancelButton.tap()
        XCTAssertTrue(confirmButton.waitForNonExistence(timeout: 5))

        app.staticTexts["Trip ideas"].tap()
        XCTAssertTrue(app.staticTexts["Lisbon in spring, Kyoto in autumn"].waitForExistence(timeout: 5))
        app.navigationBars.buttons.element(boundBy: 0).tap()

        app.buttons["Archived"].tap()
        XCTAssertTrue(app.staticTexts["Old receipts"].waitForExistence(timeout: 5))
        app.navigationBars.buttons.element(boundBy: 0).tap()

        app.buttons["Add Note"].tap()
        let title = app.textFields["new-note.title"]
        XCTAssertTrue(title.waitForExistence(timeout: 5))
        title.tap()
        title.typeText("Call the plumber")
        app.buttons["Save"].tap()
        XCTAssertTrue(app.staticTexts["Call the plumber"].waitForExistence(timeout: 5))

        // The existing archive button on the note screen still works.
        app.staticTexts["Trip ideas"].tap()
        app.buttons["note.toggleArchive"].tap()
        XCTAssertTrue(app.staticTexts["Groceries"].waitForExistence(timeout: 5))
        XCTAssertEqual(count("Trip ideas"), 0)
    }

    /// I03-preview-accessibility-audit
    func testPreviewPassesAccessibilityAudit() throws {
        open(groceriesLink())
        XCTAssertTrue(confirmButton.waitForExistence(timeout: 10))
        // Ignored: items inside navigation bars (the audit flags the standard toolbar buttons for
        // contrast and Dynamic Type) and "nearly passed" contrast warnings, which the system
        // secondary label colour triggers. Every other issue fails the check.
        let bars = app.navigationBars.allElementsBoundByIndex.map(\.frame)
        try app.performAccessibilityAudit { issue in
            if issue.compactDescription.localizedCaseInsensitiveContains("nearly passed") { return true }
            guard let frame = issue.element?.frame else { return false }
            return bars.contains { $0.contains(frame) }
        }
    }
}
