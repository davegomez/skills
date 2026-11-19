import WidgetKit
import SwiftUI
struct OrdersProvider: TimelineProvider {
    func placeholder(in context: Context) -> OrdersEntry { OrdersEntry(date: .now, count: 0) }
    func getSnapshot(in context: Context, completion: @escaping (OrdersEntry) -> Void) { completion(placeholder(in: context)) }
    func getTimeline(in context: Context, completion: @escaping (Timeline<OrdersEntry>) -> Void) {
        let count = SharedStore(appGroup: "group.com.example").openOrderCount()
        completion(Timeline(entries: [OrdersEntry(date: .now, count: count)], policy: .atEnd))
    }
}
