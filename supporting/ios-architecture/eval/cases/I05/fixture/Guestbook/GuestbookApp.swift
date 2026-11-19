import SwiftUI

@main
struct GuestbookApp: App {
    @State private var store = GuestStore()

    var body: some Scene {
        WindowGroup {
            GuestListView(store: store)
                .task { store.load() }
        }
    }
}
