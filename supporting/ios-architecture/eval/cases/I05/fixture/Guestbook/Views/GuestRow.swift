import SwiftUI

struct GuestRow: View {
    let guest: Guest

    var body: some View {
        VStack(alignment: .leading) {
            Text(guest.name)
                .font(.headline)
            Text("Table \(guest.tableNumber)")
                .font(.subheadline)
                .foregroundStyle(.secondary)
        }
        .accessibilityElement(children: .combine)
    }
}
