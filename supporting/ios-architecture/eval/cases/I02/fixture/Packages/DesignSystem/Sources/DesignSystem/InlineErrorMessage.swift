import SwiftUI

/// An error message next to the control that caused it. An icon and the spoken "Error" prefix carry the
/// state, so color is not the only signal. The text uses a text style, so it scales with Dynamic Type.
public struct InlineErrorMessage: View {
    private let message: LocalizedStringResource

    public init(_ message: LocalizedStringResource) {
        self.message = message
    }

    public var body: some View {
        Label {
            Text(message)
        } icon: {
            Image(systemName: "exclamationmark.triangle.fill")
        }
        .font(.callout)
        .foregroundStyle(.red)
        .accessibilityElement(children: .ignore)
        .accessibilityLabel(Text("Error: \(Text(message))", bundle: .module, comment: "VoiceOver label of an inline error message"))
    }
}

#Preview("Largest text size") {
    InlineErrorMessage("Enter a title.")
        .padding()
        .environment(\.dynamicTypeSize, .accessibility5)
}
