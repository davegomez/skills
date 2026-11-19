Build a new iOS app in this folder: a small offline packing list.

What the app does:
- The first screen after launch is the packing list.
- I type an item name and add it to the list.
- I tap an item to mark it packed, and tap it again to mark it not packed.
- The list and each item's packed state are saved on the device. After I quit and relaunch the app, I see the same list with the same packed states.
- It works fully offline. There is no account and no server.
- Everyone must be able to use it, including with VoiceOver and large text sizes.

Project facts:
- App name: PackingList. The shared Xcode scheme named PackingList builds the app and runs its tests.
- Bundle identifier prefix: com.example.eval
- Minimum iOS version: 27.3
- Team: 1 developer.
- Regulated data: none. The app stores no health, financial, or other regulated personal data.
- Sync across devices: no. Accounts shared with other platforms: no.
- Storage: files on the device.
- You may send this project's code to outside services while you work.

Put the Xcode workspace or project in this folder, or in 1 subfolder of it. I have no signing team yet, so it must build and run on the iOS Simulator without code signing.

Include automated tests for the packing-list logic. They must run and pass in the PackingList scheme's test action.

Our acceptance tests drive the app through these accessibility elements, so keep them exactly:
- The text field for a new item has the accessibility label "Item name".
- The button that adds the item has the accessibility label "Add item".
- Each item in the list is 1 accessibility element. Its label is the item name, and its value is "Packed" or "Not packed". Tapping it toggles the packed state.
