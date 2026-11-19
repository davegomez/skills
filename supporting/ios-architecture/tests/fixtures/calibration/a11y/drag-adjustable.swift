import SwiftUI
struct VolumeKnob: View {
    @Binding var level: Int
    var body: some View {
        Circle()
            .gesture(DragGesture().onChanged { level = max(0, min(10, level + Int($0.translation.height / -20))) })
            .accessibilityElement()
            .accessibilityLabel("Volume")
            .accessibilityValue("\(level)")
            .accessibilityAdjustableAction { direction in
                switch direction {
                case .increment: level = min(10, level + 1)
                case .decrement: level = max(0, level - 1)
                @unknown default: break
                }
            }
    }
}
