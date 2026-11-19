import SwiftUI

@main
struct QuickNotesApp: App {
    @State private var store: NoteStore

    init() {
        let store = NoteStore()
        // UI tests start from a known set of notes.
        if CommandLine.arguments.contains("-uitest-seed") {
            store.replaceAll(with: SampleNotes.all)
        }
        _store = State(initialValue: store)
    }

    var body: some Scene {
        WindowGroup {
            NoteListView()
                .environment(store)
        }
    }
}
