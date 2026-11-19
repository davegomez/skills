/// Authentication seam. Returns the access token of the signed-in user.
nonisolated protocol AuthService: Sendable {
    func accessToken() async throws -> String
}
