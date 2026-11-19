import os
let logger = Logger(subsystem: "com.example.app", category: "Auth")
func didSignIn(_ user: User) {
    logger.info("Signed in \(user.email, privacy: .public)")
}
