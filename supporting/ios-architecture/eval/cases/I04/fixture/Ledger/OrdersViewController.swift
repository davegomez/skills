import UIKit

struct OrderLine: Codable {
    var sku: String
    var name: String
    var quantity: Int
    var unitPriceCents: Int

    enum CodingKeys: String, CodingKey {
        case sku
        case name
        case quantity = "qty"
        case unitPriceCents = "unit_price_cents"
    }
}

/// The file the screen saves after each successful load. Users of every version have one.
struct OrdersCacheFile: Codable {
    var version: Int
    var savedAt: Date
    var lines: [OrderLine]

    enum CodingKeys: String, CodingKey {
        case version
        case savedAt = "saved_at"
        case lines
    }
}

private struct OrdersResponse: Decodable {
    var lines: [OrderLine]
}

class OrdersViewController: UIViewController, UITableViewDataSource {
    private var lines: [OrderLine] = []

    private let tableView = UITableView(frame: .zero, style: .insetGrouped)
    private let statusLabel = UILabel()
    private let subtotalLabel = UILabel()
    private let discountLabel = UILabel()
    private let taxLabel = UILabel()
    private let totalLabel = UILabel()

    private var cacheURL: URL {
        let support = FileManager.default.urls(for: .applicationSupportDirectory, in: .userDomainMask)[0]
        return support.appendingPathComponent("ledger", isDirectory: true).appendingPathComponent("orders-cache.json")
    }

    private var endpoint: URL {
        // QA builds point the screen at a staging or canned feed.
        if let override = ProcessInfo.processInfo.environment["LEDGER_ORDERS_URL"], let url = URL(string: override) {
            return url
        }
        return URL(string: "https://api.ledger.example/v1/orders")!
    }

    override func viewDidLoad() {
        super.viewDidLoad()
        title = L10n.Orders.title
        view.backgroundColor = .systemGroupedBackground
        navigationItem.rightBarButtonItem = UIBarButtonItem(
            title: L10n.Orders.reload, style: .plain, target: self, action: #selector(reloadTapped)
        )
        navigationItem.rightBarButtonItem?.accessibilityIdentifier = "orders.reload"
        layoutViews()
        loadCachedOrders()
        fetchOrders()
    }

    @objc private func reloadTapped() {
        fetchOrders()
    }

    // MARK: - Loading

    private func loadCachedOrders() {
        guard let data = try? Data(contentsOf: cacheURL) else {
            statusLabel.text = L10n.Orders.Status.empty
            updateTotals()
            return
        }
        let decoder = JSONDecoder()
        decoder.dateDecodingStrategy = .secondsSince1970
        if let cache = try? decoder.decode(OrdersCacheFile.self, from: data), cache.version == 1 {
            lines = cache.lines
            statusLabel.text = L10n.Orders.Status.offline
        } else {
            statusLabel.text = L10n.Orders.Status.empty
        }
        tableView.reloadData()
        updateTotals()
    }

    private func fetchOrders() {
        statusLabel.text = L10n.Orders.Status.loading
        URLSession.shared.dataTask(with: endpoint) { [weak self] data, response, error in
            DispatchQueue.main.async {
                guard let self = self else { return }
                if let http = response as? HTTPURLResponse, !(200..<300).contains(http.statusCode) {
                    self.showLoadFailure()
                    return
                }
                guard error == nil, let data = data,
                      let decoded = try? JSONDecoder().decode(OrdersResponse.self, from: data) else {
                    self.showLoadFailure()
                    return
                }
                self.lines = decoded.lines
                self.saveCache()
                self.statusLabel.text = L10n.Orders.Status.updated
                self.tableView.reloadData()
                self.updateTotals()
            }
        }.resume()
    }

    private func showLoadFailure() {
        statusLabel.text = lines.isEmpty ? L10n.Orders.Status.empty : L10n.Orders.Status.offline
    }

    private func saveCache() {
        let encoder = JSONEncoder()
        encoder.dateEncodingStrategy = .secondsSince1970
        encoder.outputFormatting = [.sortedKeys]
        let cache = OrdersCacheFile(version: 1, savedAt: Date(), lines: lines)
        do {
            try FileManager.default.createDirectory(
                at: cacheURL.deletingLastPathComponent(), withIntermediateDirectories: true
            )
            try encoder.encode(cache).write(to: cacheURL, options: .atomic)
        } catch {
            print("Ledger: could not save the orders cache: \(error)")
        }
    }

    // MARK: - Totals

    private func updateTotals() {
        var subtotal = 0
        for line in lines where line.quantity > 0 {
            subtotal += line.quantity * line.unitPriceCents
        }
        // 10% off orders of $100.00 or more, rounded half up.
        var discount = 0
        if subtotal >= 10_000 {
            discount = (subtotal + 5) / 10
        }
        // 8.25% sales tax on the discounted amount, rounded half up.
        let taxable = subtotal - discount
        let tax = (taxable * 825 + 5_000) / 10_000
        let total = taxable + tax

        subtotalLabel.text = L10n.Orders.subtotal(formatCents(subtotal))
        discountLabel.text = L10n.Orders.discount(formatCents(-discount))
        taxLabel.text = L10n.Orders.tax(formatCents(tax))
        totalLabel.text = L10n.Orders.total(formatCents(total))
    }

    private func formatCents(_ cents: Int) -> String {
        let formatter = NumberFormatter()
        formatter.numberStyle = .currency
        formatter.locale = Locale(identifier: "en_US")
        return formatter.string(from: NSNumber(value: Double(cents) / 100)) ?? ""
    }

    // MARK: - Table

    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        lines.count
    }

    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "LineCell")
            ?? UITableViewCell(style: .subtitle, reuseIdentifier: "LineCell")
        let line = lines[indexPath.row]
        var content = UIListContentConfiguration.subtitleCell()
        content.text = line.name
        content.secondaryText = L10n.Orders.Line.detail(line.quantity, formatCents(line.unitPriceCents))
        cell.contentConfiguration = content
        cell.accessibilityIdentifier = "orders.line.\(line.sku)"
        return cell
    }

    // MARK: - Layout

    private func layoutViews() {
        tableView.dataSource = self
        tableView.accessibilityIdentifier = "orders.table"

        let labels = [statusLabel, subtotalLabel, discountLabel, taxLabel, totalLabel]
        let identifiers = ["orders.status", "orders.subtotal", "orders.discount", "orders.tax", "orders.total"]
        for (label, identifier) in zip(labels, identifiers) {
            label.accessibilityIdentifier = identifier
            label.font = .preferredFont(forTextStyle: .body)
            label.adjustsFontForContentSizeCategory = true
            label.numberOfLines = 0
        }
        statusLabel.font = .preferredFont(forTextStyle: .footnote)
        statusLabel.textColor = .secondaryLabel
        totalLabel.font = .preferredFont(forTextStyle: .headline)

        let footer = UIStackView(arrangedSubviews: labels)
        footer.axis = .vertical
        footer.spacing = 4
        footer.isLayoutMarginsRelativeArrangement = true
        footer.directionalLayoutMargins = NSDirectionalEdgeInsets(top: 12, leading: 20, bottom: 12, trailing: 20)
        footer.backgroundColor = .secondarySystemGroupedBackground

        let stack = UIStackView(arrangedSubviews: [tableView, footer])
        stack.axis = .vertical
        stack.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(stack)
        NSLayoutConstraint.activate([
            stack.leadingAnchor.constraint(equalTo: view.leadingAnchor),
            stack.trailingAnchor.constraint(equalTo: view.trailingAnchor),
            stack.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor),
            stack.bottomAnchor.constraint(equalTo: view.safeAreaLayoutGuide.bottomAnchor),
        ])
    }
}
