# Navigation and deep links

Use `NavigationStack` with a typed route enum, owned by a router in the shell. Treat every incoming URL as untrusted input.

- Use `NavigationSplitView` for iPad and wide layouts.
- Keep the navigation path in an `@Observable` router that the shell owns.
- Use a typed array when all routes share 1 type. Use `NavigationPath` when routes from unrelated types share 1 stack.
- Add a coordinator layer only when you have deep links, several entry points, or flows that cross features.

```swift
enum AppRoute: Hashable, Codable {
    case feature(FeatureID)
    case detail(id: String)
}

@Observable
final class AppRouter {
    var path: [AppRoute] = []
    func open(_ route: AppRoute) { path.append(route) }
    func popToRoot() { path.removeAll() }
}
```

**Deep links and universal links**

- Support universal links with an `apple-app-site-association` file and the Associated Domains entitlement.
- Handle links with `.onOpenURL` and `.onContinueUserActivity`.
- Parse every incoming URL into an `AppRoute`. Reject unknown or invalid input.
- Do not perform an action with side effects directly from a link. Show a confirmation screen first.
- Make `AppRoute` `Codable` so that you can restore navigation state after the system stops the app.
