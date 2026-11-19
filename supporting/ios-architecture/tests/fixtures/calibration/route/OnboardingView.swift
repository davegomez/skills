import SwiftUI
struct OnboardingView: View {
    let onFinish: () -> Void
    var body: some View {
        VStack(spacing: 24) {
            Image(systemName: "sparkles").font(.largeTitle)
            Text("Welcome to Orders")
                .font(.title)
            Text("Track every order in 1 place.")
            Button("Get started", action: onFinish)
                .buttonStyle(.borderedProminent)
        }
        .padding()
    }
}
