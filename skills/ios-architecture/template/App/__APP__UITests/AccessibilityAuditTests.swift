import XCTest

/// Runs the automated accessibility audit on each main screen. Add 1 test for each new main screen.
final class AccessibilityAuditTests: XCTestCase {
    @MainActor
    func testRootScreenPassesAccessibilityAudit() throws {
        let app = XCUIApplication()
        app.launch()
        // Skip only .textClipped: its heuristic flags plain 1-line sidebar rows, and the result changes with the row count.
        try app.performAccessibilityAudit(for: XCUIAccessibilityAuditType.all.subtracting(.textClipped))
    }
}
