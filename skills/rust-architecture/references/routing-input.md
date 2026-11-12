# Routing, navigation, and input

Treat every URL, header, argument, environment variable, and file as untrusted. Parse input into domain types at the edge, then route typed commands.

- **Server (axum):** Use `{param}` path syntax, for example `/orders/{id}`. Group routes per feature and merge them in the root. Extract typed values (`Path<OrderId>`, `Json<CreateOrder>`). Set body size limits on all routes.
- **CLI:** Use the `noun verb` form: `app orders list`. Add new flags, but never rename old flags. Read secrets from stdin or the keychain, never from a flag, because flags show up in process lists and shell history.
- **Desktop (GPUI):** Hold navigation state in 1 root view entity as an enum (`Screen::OrderList`, `Screen::OrderDetail(OrderId)`). Change screens through actions, so keyboard shortcuts and menus use the same path. Validate dropped and opened files like network input.
