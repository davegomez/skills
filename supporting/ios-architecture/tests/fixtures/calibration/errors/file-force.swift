func readNotes(at fileURL: URL) -> String {
    let text = try! String(contentsOf: fileURL, encoding: .utf8)
    return text
}
