import SwiftUI

enum Route: Hashable {
    case note(UUID)
    case archived
}

struct NoteListView: View {
    @Environment(NoteStore.self) private var store
    @State private var path: [Route] = []
    @State private var isAddingNote = false

    var body: some View {
        NavigationStack(path: $path) {
            List(store.activeNotes) { note in
                NavigationLink(value: Route.note(note.id)) {
                    NoteRow(note: note)
                }
            }
            .overlay {
                if store.activeNotes.isEmpty {
                    ContentUnavailableView(
                        "No Notes",
                        systemImage: "note.text",
                        description: Text("Tap Add Note to write one.")
                    )
                }
            }
            .navigationTitle("Notes")
            .navigationDestination(for: Route.self) { route in
                switch route {
                case .note(let id):
                    NoteDetailView(noteID: id)
                case .archived:
                    ArchivedListView()
                }
            }
            .toolbar {
                ToolbarItem(placement: .topBarLeading) {
                    NavigationLink("Archived", value: Route.archived)
                }
                ToolbarItem(placement: .primaryAction) {
                    Button("Add Note", systemImage: "plus") {
                        isAddingNote = true
                    }
                }
            }
            .sheet(isPresented: $isAddingNote) {
                NewNoteView()
            }
        }
    }
}

struct NoteRow: View {
    let note: Note

    var body: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text(note.title)
                .font(.headline)
            Text(note.body)
                .font(.subheadline)
                .foregroundStyle(.secondary)
                .lineLimit(1)
        }
    }
}

struct ArchivedListView: View {
    @Environment(NoteStore.self) private var store

    var body: some View {
        List(store.archivedNotes) { note in
            NavigationLink(value: Route.note(note.id)) {
                NoteRow(note: note)
            }
        }
        .overlay {
            if store.archivedNotes.isEmpty {
                ContentUnavailableView("No Archived Notes", systemImage: "archivebox")
            }
        }
        .navigationTitle("Archived")
    }
}
