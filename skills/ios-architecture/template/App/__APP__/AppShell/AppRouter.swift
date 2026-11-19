import FeatureKit
import Observation

/// The navigation state of the shell: the selected feature and the stack of routes on top of it.
@Observable
final class AppRouter {
    var selection: FeatureID?
    var path: [AppRoute] = []

    func open(_ route: AppRoute) { path.append(route) }
    func popToRoot() { path.removeAll() }
}
