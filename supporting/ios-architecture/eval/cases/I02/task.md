This folder holds Storefront, an iOS app. Add an order summary feature to it.

What the feature does:
- The first screen of the app gets exactly 1 entry labelled "Order summary". Tapping it opens the order summary screen.
- The screen shows the current order: for each line, the item name, the quantity, the unit price, and the line total. Below the lines it shows the subtotal, the tax, and the total.
- There is no order backend yet. Add a fake order service and inject it into the feature. The app picks the fake's behavior from the launch environment variable `ORDER_SCENARIO`:
  - `sample`, and also when the variable is missing or has another value: the sample order below.
  - `empty`: an order with no lines.
  - `error`: loading the order fails.
- The sample order:

  | Item | Quantity | Unit price |
  | --- | --- | --- |
  | Notebook | 3 | $4.99 |
  | Pen set | 1 | $12.49 |
  | Desk lamp | 1 | $14.54 |

Rules for the amounts:
- Line total = quantity × unit price.
- Subtotal = the sum of the line totals.
- Tax = 8.25% of the subtotal, rounded to the nearest cent. Half a cent rounds up.
- Total = subtotal + tax.
- Show every amount in US dollars with 2 decimals, for example $4.99.

States:
- Empty order: show the message "Your order is empty." and no subtotal, tax, or total.
- Load failure: show the message "We couldn't load your order." and a "Try again" button that loads the order again. Show no subtotal, tax, or total.

Tests and scope:
- Add automated tests for the amount rules and the empty and error states. They must run and pass in the Storefront scheme's test action.
- Leave the existing packages `Packages/Core`, `Packages/DesignSystem`, `Packages/Networking`, and `Packages/Persistence` unchanged.
- It must build and run on the iOS Simulator without code signing.

Our acceptance tests read the amounts through these accessibility identifiers, so keep them exactly:
- `order.subtotal`, `order.tax`, and `order.total`: 1 element each, whose accessibility label or value contains the formatted amount, for example "$4.99".
