# Testing

Write domain tests first (test-driven development), then feature tests, then a small number of UI tests. Hold domain coverage at 90% or more.

| Layer | Tool | Target |
| --- | --- | --- |
| Domain | Swift Testing (`@Test`, `#expect`, `#require`) | 90% or more line coverage |
| Feature models | Swift Testing with fake clients | Main flows and every error state |
| Views | swift-snapshot-testing | Light, dark, largest Dynamic Type, right-to-left |
| Persistence | Swift Testing with fixtures | Every schema migration |
| UI flows and audits | XCTest (XCUITest) | Critical journeys and `performAccessibilityAudit()` |
| Performance | XCTest metrics and Instruments | Launch, scrolling, heavy operations |

**Techniques**

- Use parameterized tests (`@Test(arguments:)`) for tables of inputs.
- Use golden tests: store expected outputs for fixed seeds and inputs.
- Use property-based tests for invariants. Generate inputs with `SeededGenerator` in a loop, and record the seed in the failure message.
- Use replay tests: store a seed and a list of actions, then replay them through the reducer to any state.
- Test the live `Networking` client with a stub `URLProtocol`. Cover status codes, malformed bodies, timeouts, retries, and cancellation.
- Test the live persistence stores against a temporary on-disk database, not only the in-memory fake.
- Use fakes, not mocks with call counts, for services. Test results, not calls.

**XCTest and Swift Testing**

- Write all new unit tests in Swift Testing.
- Move existing XCTest unit tests to Swift Testing step by step. Both frameworks can run in the same test target.
- Keep UI tests in XCTest unless the pinned Xcode version supports UI tests in Swift Testing.

**CI**

- Run all tests on every pull request in Xcode Cloud or another CI service.
- Turn on code coverage in the test plan. Fail the build when domain coverage goes below 90%.
- Run tests on the oldest and newest supported iOS versions.
- Run UI tests with the largest text size and with a right-to-left language at least once per release.
