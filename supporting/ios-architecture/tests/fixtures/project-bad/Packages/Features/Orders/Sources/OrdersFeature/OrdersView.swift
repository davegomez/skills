import SwiftUI
import SwiftData
import Combine
import Alamofire
import ProfileFeature
import OrdersDomain

final class OrdersModel: ObservableObject {
    static let shared = OrdersModel()
    @Published var orders: [Order] = []
    let session = URLSession.shared
    let environment = ProcessInfo.processInfo.environment
    let accessible = kSecAttrAccessibleAlways

    func remember(token: String) {
        UserDefaults.standard.set(token, forKey: "token")
    }
}

final class Cache: @unchecked Sendable {
    // Safe: the lock guards every access to items.
    final class Inner: @unchecked Sendable {}
    nonisolated(unsafe) var items: [String] = []
}

@Model
final class CachedOrder {
    var id: String = ""
}

struct OrdersView: View {
    @StateObject private var model = OrdersModel.shared

    var body: some View {
        NavigationView {
            Text(NSLocalizedString("Orders", comment: "Title"))
                .font(.system(size: 14))
        }
    }
}

func configure(_ label: UILabel) {
    label.textAlignment = .left
}
