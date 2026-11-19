import os
let logger = Logger(subsystem: "com.example.app", category: "Auth")
func didSignIn(_ user: User, order: Order) {
    logger.info("Signed in \(user.email)")
    logger.info("Order \(order.id, privacy: .private(mask: .hash)) placed")
}
