import SwiftUI

struct ReadingListView: View {
    let dependencies: AppDependencies

    var body: some View {
        ContentUnavailableView("Coming Soon", systemImage: "books.vertical")
            .navigationTitle("Reading List")
    }
}
