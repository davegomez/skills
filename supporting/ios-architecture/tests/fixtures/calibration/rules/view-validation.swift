import SwiftUI
struct SignUpView: View {
    @State private var email = ""
    @State private var password = ""
    var isValid: Bool {
        email.contains("@") && password.count >= 12 && password.rangeOfCharacter(from: .decimalDigits) != nil
    }
    var body: some View {
        Form {
            TextField("Email", text: $email)
            SecureField("Password", text: $password)
            Button("Create account") {}.disabled(!isValid)
        }
    }
}
