import SwiftUI
struct SpendingChart: View {
    let values: [Double]
    var body: some View {
        Canvas { context, size in
            let width = size.width / CGFloat(values.count)
            for (index, value) in values.enumerated() {
                let rect = CGRect(x: CGFloat(index) * width, y: size.height * (1 - value), width: width - 4, height: size.height * value)
                context.fill(Path(rect), with: .color(.accentColor))
            }
        }
    }
}
