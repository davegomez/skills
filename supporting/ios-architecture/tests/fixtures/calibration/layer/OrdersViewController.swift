import UIKit
final class OrdersViewController: UITableViewController {
    var orders: [Order] = []
    override func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int { orders.count }
    override func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "Order", for: indexPath)
        cell.textLabel?.text = orders[indexPath.row].title
        return cell
    }
}
