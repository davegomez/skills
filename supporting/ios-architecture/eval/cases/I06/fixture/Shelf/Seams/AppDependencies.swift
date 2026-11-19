import Foundation

/// Services built once at launch and passed to every screen.
nonisolated struct AppDependencies: Sendable {
    let http: any HTTPClient
    let auth: any AuthService

    /// `EVAL_SCENARIO` selects the fake transport; without it the app uses the live client.
    /// Sign-in is always the fake service.
    static func fromLaunchEnvironment(
        _ environment: [String: String] = ProcessInfo.processInfo.environment
    ) -> AppDependencies {
        let http: any HTTPClient
        if let name = environment["EVAL_SCENARIO"] {
            guard let scenario = Scenario(rawValue: name) else {
                fatalError("Unknown EVAL_SCENARIO")
            }
            http = FakeHTTPClient(scenario: scenario)
        } else {
            http = URLSessionHTTPClient()
        }
        return AppDependencies(http: http, auth: FakeAuthService())
    }

    /// `EVAL_START=list` opens the reading list at launch.
    static func startsOnReadingList(
        _ environment: [String: String] = ProcessInfo.processInfo.environment
    ) -> Bool {
        environment["EVAL_START"] == "list"
    }
}
