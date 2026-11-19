import SwiftUI

struct GuestListView: View {
    @Bindable var store: GuestStore

    var body: some View {
        NavigationStack {
            List {
                ForEach(store.guests) { guest in
                    GuestRow(guest: guest)
                        .swipeActions {
                            Button("Remove", role: .destructive) { store.remove(guest) }
                        }
                }
            }
            .navigationTitle("Guests")
            .alert("Something went wrong", isPresented: errorShown) {
                Button("OK", role: .cancel) {}
            } message: {
                Text("Your latest change may not be saved.")
            }
        }
    }

    private var errorShown: Binding<Bool> {
        Binding(
            get: { store.lastError != nil },
            set: { if !$0 { store.lastError = nil } }
        )
    }
}
