import CoreClients
import Foundation
import Testing
import __FEATURE__Domain

// MARK: Unit tests

@Test func makeTrimsTheTitle() throws {
    #expect(try __FEATURE__Item.make(id: uuid(1), title: "  Milk \n").title == "Milk")
}

@Test(arguments: ["", "   ", "\n\t"])
func makeRejectsEmptyTitle(_ title: String) {
    #expect(throws: __FEATURE__Error.emptyTitle) { try __FEATURE__Item.make(id: uuid(1), title: title) }
}

@Test func addRemoveAndClear() throws {
    let milk = try __FEATURE__Item.make(id: uuid(1), title: "Milk")
    let eggs = try __FEATURE__Item.make(id: uuid(2), title: "Eggs")
    var state = reduce(reduce(__FEATURE__State(), .add(milk)), .add(eggs))
    #expect(state.items == [milk, eggs])
    state = reduce(state, .remove(id: milk.id))
    #expect(state.items == [eggs])
    #expect(reduce(state, .clear).items.isEmpty)
}

@Test func addingAKnownIDChangesNothing() throws {
    let milk = try __FEATURE__Item.make(id: uuid(1), title: "Milk")
    let other = try __FEATURE__Item.make(id: uuid(1), title: "Other")
    let state = reduce(__FEATURE__State(), .add(milk))
    #expect(reduce(state, .add(other)) == state)
}

// MARK: Property-based test

@Test func itemIDsStayUniqueForAnyActionSequence() throws {
    for seed in UInt64(0)..<200 {
        var generator = SeededGenerator(seed: seed)
        var state = __FEATURE__State()
        for _ in 0..<50 {
            state = reduce(state, try randomAction(using: &generator))
            #expect(Set(state.items.map(\.id)).count == state.items.count, "seed \(seed)")
        }
    }
}

// MARK: Golden test

/// The expected output for a fixed seed. When a change to `reduce` is intended, update the stored value.
@Test func replayMatchesGolden() throws {
    var generator = SeededGenerator(seed: 3)
    var state = __FEATURE__State()
    for _ in 0..<20 {
        state = reduce(state, try randomAction(using: &generator))
    }
    #expect(state.items.map(\.title) == ["item 5", "item 3", "item 2", "item 4"])
}

// MARK: Helpers

private func uuid(_ value: UInt8) -> UUID {
    UUID(uuid: (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, value))
}

/// A random action over a small pool of IDs, so that sequences add and remove the same items.
private func randomAction(using generator: inout SeededGenerator) throws -> __FEATURE__Action {
    let id = UInt8.random(in: 0..<8, using: &generator)
    switch Int.random(in: 0..<10, using: &generator) {
    case 0: return .clear
    case 1...4: return .remove(id: uuid(id))
    default: return .add(try __FEATURE__Item.make(id: uuid(id), title: "item \(id)"))
    }
}
