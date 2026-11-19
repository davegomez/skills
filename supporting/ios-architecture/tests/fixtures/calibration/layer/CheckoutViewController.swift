import UIKit
final class CheckoutViewController: UIViewController {
    var items: [LineItem] = []
    @IBOutlet private var totalLabel: UILabel!
    override func viewDidLoad() {
        super.viewDidLoad()
        let total = items.reduce(0) { $0 + $1.price } * (items.count > 3 ? 0.9 : 1)
        totalLabel.text = "\(total)"
        URLSession.shared.dataTask(with: URL(string: "https://api.example.com/cart")!) { data, _, _ in
            _ = data
        }.resume()
    }
}
