import Foundation
import Observation
import OSLog

@MainActor
@Observable
final class NoteStore {
    private(set) var notes: [Note] = []
    @ObservationIgnored private let fileURL: URL
    @ObservationIgnored private let logger = Logger(subsystem: "com.example.quicknotes", category: "store")

    init(fileURL: URL = URL.applicationSupportDirectory.appending(path: "notes.json")) {
        self.fileURL = fileURL
        load()
    }

    var activeNotes: [Note] { notes.filter { !$0.isArchived } }
    var archivedNotes: [Note] { notes.filter(\.isArchived) }

    func note(id: UUID) -> Note? {
        notes.first { $0.id == id }
    }

    func add(title: String, body: String) {
        notes.append(Note(id: UUID(), title: title, body: body, isArchived: false, createdAt: .now))
        save()
    }

    func toggleArchived(id: UUID) {
        guard let index = notes.firstIndex(where: { $0.id == id }) else { return }
        notes[index].isArchived.toggle()
        save()
    }

    func replaceAll(with notes: [Note]) {
        self.notes = notes
        save()
    }

    private func load() {
        guard FileManager.default.fileExists(atPath: fileURL.path) else { return }
        do {
            notes = try JSONDecoder().decode([Note].self, from: Data(contentsOf: fileURL))
        } catch {
            logger.error("Could not read notes: \(error.localizedDescription, privacy: .public)")
        }
    }

    private func save() {
        do {
            try FileManager.default.createDirectory(
                at: fileURL.deletingLastPathComponent(),
                withIntermediateDirectories: true
            )
            try JSONEncoder().encode(notes).write(to: fileURL, options: [.atomic, .completeFileProtection])
        } catch {
            logger.error("Could not save notes: \(error.localizedDescription, privacy: .public)")
        }
    }
}
