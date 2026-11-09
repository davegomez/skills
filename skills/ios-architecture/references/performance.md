# Observability and performance

Measure before you optimize, and set performance budgets that CI checks.

- Add `OSSignposter` intervals around launch phases, network calls, and database work.
- Profile with Instruments: Time Profiler, SwiftUI, Hangs, Allocations, Network, and Swift Concurrency.
- Use the Swift Concurrency instrument to find actor contention and main-actor blocking.
- Collect field data with MetricKit and Xcode Organizer: launch time, hangs, scrolling, memory, and disk writes.
- Set budgets per reference device, for example time to first frame, memory peak, and app size.
- Test the budgets in CI with XCTest metrics. Fail the build when a budget is exceeded.
- Use lazy containers (`LazyVStack`, `List`) for long collections. Give each item a stable identity.
- Download and decode images off the main actor. Cache them with a size limit.
