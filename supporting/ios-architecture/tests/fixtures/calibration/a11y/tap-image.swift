import SwiftUI
struct FavoriteBadge: View {
    @Binding var isFavorite: Bool
    var body: some View {
        Image(systemName: isFavorite ? "heart.fill" : "heart")
            .onTapGesture { isFavorite.toggle() }
    }
}
