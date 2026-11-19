import os

/// One subsystem for the app, one category per area.
nonisolated enum AppLog {
    static let store = Logger(subsystem: "eval.i05.Guestbook", category: "GuestStore")
}
