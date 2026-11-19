import XCTest

final class ShelfLaunchTests: XCTestCase {
    @MainActor
    func testHomeShowsReadingListLink() {
        let app = XCUIApplication()
        app.launchEnvironment["EVAL_SCENARIO"] = "success"
        app.launch()
        let link = app.descendants(matching: .any).matching(identifier: "home.readingList").firstMatch
        XCTAssertTrue(link.waitForExistence(timeout: 10))
    }
}
