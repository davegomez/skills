import CoreClients
import CoreTesting
import Foundation
import Testing
@testable import __FEATURE__Feature

@Test func addItemUsesTheInjectedID() {
    let model = __FEATURE__Model(uuid: .incrementing())
    #expect(model.addItem(title: " Milk "))
    #expect(model.state.items.map(\.id.uuidString) == ["00000000-0000-0000-0000-000000000000"])
    #expect(model.state.items.map(\.title) == ["Milk"])
    #expect(model.errorMessage == nil)
}

@Test func emptyTitleShowsAnErrorUntilTheNextValidAdd() {
    let model = __FEATURE__Model(uuid: .incrementing())
    #expect(!model.addItem(title: "  "))
    #expect(model.errorMessage != nil)
    #expect(model.state.items.isEmpty)
    #expect(model.addItem(title: "Eggs"))
    #expect(model.errorMessage == nil)
}

@Test func removeItemsAtOffsets() {
    let model = __FEATURE__Model(uuid: .incrementing())
    model.addItem(title: "A")
    model.addItem(title: "B")
    model.addItem(title: "C")
    model.removeItems(at: [0, 2])
    #expect(model.state.items.map(\.title) == ["B"])
}
