import UIKit

// TODO: move to the new settings screen once design is ready (LEDGER-212)
class SettingsViewController: UIViewController {
    let defaults = UserDefaults.standard
    var currencySwitch: UISwitch!
    var versionLabel: UILabel!

    override func viewDidLoad() {
        super.viewDidLoad()
        title = L10n.Settings.title
        view.backgroundColor = .systemBackground

        let label = UILabel()
        label.text = L10n.Settings.showCents
        label.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(label)

        currencySwitch = UISwitch()
        currencySwitch.isOn = defaults.bool(forKey: "showCents")
        currencySwitch.addTarget(self, action: #selector(toggled), for: .valueChanged)
        currencySwitch.accessibilityIdentifier = "settings.showCents"
        currencySwitch.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(currencySwitch)

        versionLabel = UILabel()
        let version = Bundle.main.infoDictionary!["CFBundleShortVersionString"] as! String
        versionLabel.text = L10n.Settings.version(version)
        versionLabel.textColor = .lightGray
        versionLabel.font = UIFont.systemFont(ofSize: 11)
        versionLabel.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(versionLabel)

        NSLayoutConstraint.activate([
            label.leadingAnchor.constraint(equalTo: view.layoutMarginsGuide.leadingAnchor),
            label.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor, constant: 24),
            currencySwitch.trailingAnchor.constraint(equalTo: view.layoutMarginsGuide.trailingAnchor),
            currencySwitch.centerYAnchor.constraint(equalTo: label.centerYAnchor),
            versionLabel.leadingAnchor.constraint(equalTo: label.leadingAnchor),
            versionLabel.topAnchor.constraint(equalTo: label.bottomAnchor, constant: 32),
        ])
    }

    @objc func toggled() {
        defaults.set(currencySwitch.isOn, forKey: "showCents")
        defaults.synchronize()
        LegacyAnalytics.shared.track("settings_show_cents_\(currencySwitch.isOn)")
    }
}
