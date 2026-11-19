import os
let logger = Logger(subsystem: "com.example.app", category: "Networking")
func log(response data: Data, for request: URLRequest) {
    logger.debug("Response body \(String(decoding: data, as: UTF8.self), privacy: .public)")
}
