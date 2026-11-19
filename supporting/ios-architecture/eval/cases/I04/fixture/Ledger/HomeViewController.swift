import UIKit

class HomeViewController: UITableViewController {
    private enum Row: Int, CaseIterable {
        case orders
        case settings
    }

    override func viewDidLoad() {
        super.viewDidLoad()
        title = L10n.Home.title
        tableView.register(UITableViewCell.self, forCellReuseIdentifier: "HomeCell")
    }

    override func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        Row.allCases.count
    }

    override func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "HomeCell", for: indexPath)
        var content = cell.defaultContentConfiguration()
        switch Row(rawValue: indexPath.row)! {
        case .orders:
            content.text = L10n.Home.orders
            cell.accessibilityIdentifier = "home.orders"
        case .settings:
            content.text = L10n.Home.settings
            cell.accessibilityIdentifier = "home.settings"
        }
        cell.contentConfiguration = content
        cell.accessoryType = .disclosureIndicator
        return cell
    }

    override func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        tableView.deselectRow(at: indexPath, animated: true)
        switch Row(rawValue: indexPath.row)! {
        case .orders:
            navigationController?.pushViewController(OrdersViewController(), animated: true)
        case .settings:
            navigationController?.pushViewController(SettingsViewController(), animated: true)
        }
    }
}
