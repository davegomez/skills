import SwiftUI
struct RootView: View {
    let account: AccountService
    var body: some View {
        HomeView()
            .onOpenURL { url in
                guard let route = AppRoute(url: url) else { return }
                if case .deleteAccount = route {
                    Task { try await account.deleteAccount() }
                }
            }
    }
}
