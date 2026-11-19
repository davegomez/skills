import XCTest

@MainActor
final class NavigationUITests: XCTestCase {
    private var app: XCUIApplication!

    override func setUp() async throws {
        continueAfterFailure = false
        app = XCUIApplication()
        app.launchArguments = ["-uitest-seed"]
        app.launch()
    }

    func testOpensNoteDetail() {
        app.staticTexts["Groceries"].tap()
        XCTAssertTrue(app.staticTexts["Milk, eggs, coffee beans"].waitForExistence(timeout: 5))
        XCTAssertTrue(app.buttons["note.toggleArchive"].exists)
    }

    func testShowsArchivedNotes() {
        app.buttons["Archived"].tap()
        XCTAssertTrue(app.staticTexts["Old receipts"].waitForExistence(timeout: 5))
        XCTAssertFalse(app.staticTexts["Groceries"].exists)
    }

    func testAddsNote() {
        app.buttons["Add Note"].tap()
        let title = app.textFields["new-note.title"]
        XCTAssertTrue(title.waitForExistence(timeout: 5))
        title.tap()
        title.typeText("Call the plumber")
        app.buttons["Save"].tap()
        XCTAssertTrue(app.staticTexts["Call the plumber"].waitForExistence(timeout: 5))
    }
}
