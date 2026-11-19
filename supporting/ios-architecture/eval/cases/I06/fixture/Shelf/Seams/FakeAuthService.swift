/// Fake sign-in. Always returns the same synthetic access token.
nonisolated struct FakeAuthService: AuthService {
    static let token = "shelf-fake-token-Qm7Zp2Lx9Rv4"

    func accessToken() async throws -> String {
        Self.token
    }
}
