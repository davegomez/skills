import SwiftUI

enum HomeRoute: Hashable {
    case readingList
}

struct HomeView: View {
    let dependencies: AppDependencies
    @State private var path: [HomeRoute] = AppDependencies.startsOnReadingList() ? [.readingList] : []

    var body: some View {
        NavigationStack(path: $path) {
            List {
                NavigationLink(value: HomeRoute.readingList) {
                    Label("Reading List", systemImage: "books.vertical")
                }
                .accessibilityIdentifier("home.readingList")
            }
            .navigationTitle("Shelf")
            .navigationDestination(for: HomeRoute.self) { route in
                switch route {
                case .readingList:
                    ReadingListView(dependencies: dependencies)
                }
            }
        }
    }
}
