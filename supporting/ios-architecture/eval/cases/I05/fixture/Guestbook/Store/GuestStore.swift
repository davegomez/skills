import Foundation
import Observation

/// Guest list of one event, saved as JSON in the app's documents folder.
@Observable
final class GuestStore {
    enum StoreError: Error, Equatable {
        case loadFailed
        case saveFailed
    }

    private(set) var guests: [Guest] = []
    var lastError: StoreError?
    private let fileURL: URL

    init(directory: URL = .documentsDirectory) {
        fileURL = directory.appending(path: "guests.json")
    }

    func load() {
        do {
            guests = try JSONDecoder().decode([Guest].self, from: Data(contentsOf: fileURL))
        } catch CocoaError.fileReadNoSuchFile {
            guests = Guest.samples
        } catch {
            AppLog.store.error("Guest list unreadable: \(String(describing: type(of: error)), privacy: .public)")
            lastError = .loadFailed
        }
    }

    func remove(_ guest: Guest) {
        guests.removeAll { $0.id == guest.id }
        persist()
    }

    private func persist() {
        do {
            let data = try JSONEncoder().encode(guests)
            try data.write(to: fileURL, options: [.atomic, .completeFileProtection])
        } catch {
            AppLog.store.error("Guest list not saved: \(String(describing: type(of: error)), privacy: .public)")
            lastError = .saveFailed
        }
    }
}
