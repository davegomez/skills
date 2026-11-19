import Combine
import Foundation
final class LegacyCartViewModel: ObservableObject {
    @Published var items: [LineItem] = []
    private var cancellables = Set<AnyCancellable>()
    func load() {
        URLSession.shared.dataTaskPublisher(for: URL(string: "https://api.example.com/cart")!)
            .map(\.data)
            .decode(type: [LineItem].self, decoder: JSONDecoder())
            .replaceError(with: [])
            .receive(on: DispatchQueue.main)
            .assign(to: \.items, on: self)
            .store(in: &cancellables)
    }
}
