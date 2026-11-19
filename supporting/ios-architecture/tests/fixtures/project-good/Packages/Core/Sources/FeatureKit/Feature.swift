import SwiftUI

public protocol Feature: Sendable {
    @MainActor func makeRootView() -> AnyView
}
