Ledger, in this folder, is a UIKit app. Its Orders screen (`Ledger/OrdersViewController.swift`) mixes the order totals logic with network and file calls in 1 view controller. Move the totals logic and the screen's data loading into a local Swift package, so that both can be tested without the UI.

- Keep the app's behavior. The Orders screen shows the same lines, totals, and status text as today, and the navigation stays as it is.
- Users already have saved orders on their devices. Those must still load after the update, and the app must keep saving to the same file in the same format.
- Keep the bundle identifier, the accessibility identifiers of the screens, and the `LEDGER_ORDERS_URL` launch environment override; the acceptance tests use them.
- Change only what this move needs.

Build and test with:

```sh
xcodebuild test -project Ledger.xcodeproj -scheme Ledger \
  -destination 'platform=iOS Simulator,name=iPhone 17 Pro' CODE_SIGNING_ALLOWED=NO
```
