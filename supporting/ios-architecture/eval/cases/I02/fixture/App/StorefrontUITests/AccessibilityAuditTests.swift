import XCTest

/// Runs the automated accessibility audit on each main screen. Add 1 test for each new main screen.
final class AccessibilityAuditTests: XCTestCase {
    @MainActor
    func testRootScreenPassesAccessibilityAudit() throws {
        let app = XCUIApplication()
        app.launch()
        try app.performAccessibilityAudit()
    }
}
