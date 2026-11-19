import CoreClients
import Foundation
import Observation
import __FEATURE__Domain

@Observable
final class __FEATURE__Model {
    private(set) var state = __FEATURE__State()
    private(set) var errorMessage: LocalizedStringResource?
    private let uuid: UUIDGenerator

    init(uuid: UUIDGenerator) {
        self.uuid = uuid
    }

    /// Returns `true` when the item was added. On failure, `errorMessage` says how to recover.
    @discardableResult
    func addItem(title: String) -> Bool {
        do {
            let item = try __FEATURE__Item.make(id: uuid(), title: title)
            state = __FEATURE__Domain.reduce(state, .add(item))
            errorMessage = nil
            return true
        } catch {
            errorMessage = Self.message(for: error)
            return false
        }
    }

    func removeItems(at offsets: IndexSet) {
        for id in offsets.map({ state.items[$0].id }) {
            state = __FEATURE__Domain.reduce(state, .remove(id: id))
        }
    }

    static func message(for error: __FEATURE__Error) -> LocalizedStringResource {
        switch error {
        case .emptyTitle:
            LocalizedStringResource("Enter a title.", bundle: .atURL(Bundle.module.bundleURL))
        }
    }
}
