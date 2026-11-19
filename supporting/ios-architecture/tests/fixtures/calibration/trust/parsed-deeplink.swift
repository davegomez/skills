import SwiftUI
extension AppRoute {
    init?(url: URL) {
        guard url.scheme == "https", url.host() == "example.com" else { return nil }
        let parts = url.pathComponents.dropFirst()
        guard parts.first == "orders", let raw = parts.dropFirst().first,
              let id = UUID(uuidString: raw) else { return nil }
        self = .detail(id: id)
    }
}
struct RootView: View {
    @State private var router = AppRouter()
    var body: some View {
        NavigationStack(path: $router.path) { HomeView() }
            .onOpenURL { url in
                guard let route = AppRoute(url: url) else { return }
                router.open(route)
            }
    }
}
