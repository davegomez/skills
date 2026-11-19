let slug = try! Regex("^[a-z0-9-]+$")
func cleanUp(_ tempURL: URL) {
    try? FileManager.default.removeItem(at: tempURL)
}
