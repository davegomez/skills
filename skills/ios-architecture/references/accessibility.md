# Accessibility

Make every common task possible with each assistive technology, and publish Accessibility Nutrition Labels for every app and every update. Both are release requirements.

**Controls**

- **VoiceOver:** Give every control a label, a value, and traits. Add a hint only when the result of an action is not clear from the label. Group related elements with `.accessibilityElement(children: .combine)`. Add `.accessibilityAction` for every custom gesture.
- **Voice Control:** Make visible labels match accessibility labels. Add `.accessibilityInputLabels` for controls with long or ambiguous names.
- **Dynamic Type:** Use text styles, not fixed font sizes. Test at the largest accessibility sizes. Change the layout (for example, from `HStack` to `VStack`) when text does not fit.
- **Motion:** Read `accessibilityReduceMotion`. Replace large movement with fades.
- **Contrast and color:** Meet contrast targets in light and dark appearance. Do not use color alone to show state.
- **Media:** Provide captions for video and audio descriptions where the content needs them.
- **Focus:** Move VoiceOver focus to new content after navigation and to the first error after a failed submit.

**Accessibility Nutrition Labels (required)**

Accessibility Nutrition Labels show on the App Store product page which accessibility features the app supports. Apple makes the labels voluntary for now and plans to require them. This architecture requires them now.

1. Before the first release, test every common task with each feature: VoiceOver, Voice Control, Larger Text, Dark Interface, Differentiate Without Color Alone, Sufficient Contrast, Reduced Motion, Captions, and Audio Descriptions.
2. Record the result for each feature and each supported device type.
3. Declare in App Store Connect only the features that pass for all common tasks.
4. Repeat the test for every release. Update the labels before you submit.
5. Add a backlog item for each feature that does not pass.

**Warning:** Do not declare a feature that you did not test. App Review can ask you to correct misleading labels.

**Automated audits**

- Call `XCUIApplication().performAccessibilityAudit()` in UI tests on every main screen.
- Run the audits in CI. Fail the build on a new issue.

**Manual audits**

- Test each release with VoiceOver, Voice Control, and the largest text size.
- Use Accessibility Inspector for each new screen.
