import SwiftUI

struct NoteDetailView: View {
    let noteID: UUID
    @Environment(NoteStore.self) private var store
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        if let note = store.note(id: noteID) {
            ScrollView {
                Text(note.body)
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .padding()
            }
            .navigationTitle(note.title)
            .toolbar {
                ToolbarItem(placement: .bottomBar) {
                    Button(note.isArchived ? "Unarchive" : "Archive") {
                        store.toggleArchived(id: noteID)
                        dismiss()
                    }
                    .accessibilityIdentifier("note.toggleArchive")
                }
            }
        } else {
            ContentUnavailableView("Note Not Found", systemImage: "questionmark.folder")
        }
    }
}

struct NewNoteView: View {
    @Environment(NoteStore.self) private var store
    @Environment(\.dismiss) private var dismiss
    @State private var title = ""
    @State private var noteBody = ""

    var body: some View {
        NavigationStack {
            Form {
                TextField("Title", text: $title)
                    .accessibilityIdentifier("new-note.title")
                TextField("Body", text: $noteBody, axis: .vertical)
                    .lineLimit(3...8)
                    .accessibilityIdentifier("new-note.body")
            }
            .navigationTitle("New Note")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Cancel") { dismiss() }
                }
                ToolbarItem(placement: .confirmationAction) {
                    Button("Save") {
                        store.add(title: title.trimmingCharacters(in: .whitespacesAndNewlines), body: noteBody)
                        dismiss()
                    }
                    .disabled(title.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty)
                }
            }
        }
    }
}
