QuickNotes, in this folder, is a SwiftUI app that saves notes on the device. Add a deep link that opens an archive preview for a saved note.

- Link format: `quicknotes://notes/<note-id>/archive`, where `<note-id>` is the note's UUID.
- The link opens a preview that shows the note's title and asks the user to confirm. Give the confirm button the accessibility identifier `archive-preview.confirm` and the cancel button `archive-preview.cancel`.
- Confirm archives the note and closes the preview. Cancel closes the preview and changes nothing.
- Do not show the preview for a malformed link, a note that does not exist, or a note that is already archived. An alert is fine.
- The link must work when the app is already running and when it is not.
- Keep the existing screens and navigation working. Keep the `-uitest-seed` launch argument and its sample notes as they are; the acceptance tests use them.

Build and test with:

```sh
xcodebuild test -project QuickNotes.xcodeproj -scheme QuickNotes \
  -destination 'platform=iOS Simulator,name=iPhone 17 Pro' CODE_SIGNING_ALLOWED=NO
```

Code from this project may be sent to external services.
