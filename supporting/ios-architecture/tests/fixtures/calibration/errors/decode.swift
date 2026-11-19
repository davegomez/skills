func load(_ data: Data) -> User? {
    let user = try? JSONDecoder().decode(User.self, from: data)
    return user
}
