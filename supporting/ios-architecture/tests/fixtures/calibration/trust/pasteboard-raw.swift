import UIKit
@Observable final class RedeemModel {
    let api: PromoClient
    init(api: PromoClient) { self.api = api }
    func pasteAndRedeem() async throws {
        let code = UIPasteboard.general.string ?? ""
        try await api.redeem(code: code)
    }
}
