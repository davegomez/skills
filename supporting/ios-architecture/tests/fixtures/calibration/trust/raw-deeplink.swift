import SwiftUI
struct RootView: View {
    @State private var router = AppRouter()
    var body: some View {
        NavigationStack(path: $router.path) { HomeView() }
            .onOpenURL { url in
                router.path.append(.detail(id: url.lastPathComponent))
            }
    }
}
