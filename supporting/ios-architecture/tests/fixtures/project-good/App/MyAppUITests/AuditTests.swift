import XCTest

final class AuditTests: XCTestCase {
    @MainActor
    func testHomeScreenAudit() throws {
        let app = XCUIApplication()
        app.launch()
        try app.performAccessibilityAudit()
    }
}
