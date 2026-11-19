import os
let logger = Logger(subsystem: "com.example.app", category: "Catalog")
func didLoad(count: Int, duration: Double, requestID: String, status: Int) {
    logger.info("Loaded \(count, privacy: .public) items in \(duration, privacy: .public) ms")
    logger.error("Request \(requestID, privacy: .public) failed with status \(status, privacy: .public)")
}
