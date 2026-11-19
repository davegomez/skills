import CoreClients
import DesignSystem
import SwiftUI
import __FEATURE__Domain

struct __FEATURE__View: View {
    @State var model: __FEATURE__Model
    @State private var draft = ""
    @AccessibilityFocusState private var isErrorFocused: Bool

    var body: some View {
        List {
            Section {
                TextField(text: $draft) { Text("New item", bundle: .module) }
                    .onSubmit(add)
                Button(action: add) { Text("Add", bundle: .module) }
                if let message = model.errorMessage {
                    InlineErrorMessage(message)
                        .accessibilityFocused($isErrorFocused)
                }
            }
            Section {
                if model.state.items.isEmpty {
                    Text("No items yet.", bundle: .module)
                        .foregroundStyle(.secondary)
                }
                ForEach(model.state.items) { item in
                    Text(item.title)
                }
                .onDelete(perform: model.removeItems)
            }
        }
        .navigationTitle(Text("__FEATURE__", bundle: .module))
    }

    private func add() {
        if model.addItem(title: draft) {
            draft = ""
        } else {
            isErrorFocused = true
        }
    }
}

#Preview {
    NavigationStack {
        __FEATURE__View(model: __FEATURE__Model(uuid: .live))
    }
}
