# iOS onboarding and permissions

## Guidance

**Observed:** Calendar, Photos, and Reminders used feature-introduction surfaces with clear continuation; Health showed a centered welcome. Later system or sync prompts remained separate. Maps, Wallet, Calendar, and Photos displayed system permission alerts over application context. **Inferred adaptation:** introduce immediate value concisely, separate explanation/setup from system consent, and preserve refusal. Post-grant, repeated denial, and permission API/SDK behavior remain **Unconfirmed**.

## Visual references

Choose the exact app/state question. Open one named state; open both only when comparing the progression.

| Visual question / state | Matching capture(s) | What to inspect |
| --- | --- | --- |
| Feature intro versus location decision | Calendar [What’s New](../../assets/ios/calendar/whats-new.png) and [day/location prompt](../../assets/ios/calendar/day-location-permission.png) | Compare heading/copy/action alignment, transition context, and alert placement |
| Feature intro versus notification decision | Photos [What’s New](../../assets/ios/photos/whats-new.png) and [Library/notification prompt](../../assets/ios/photos/library-notification-permission.png) | Compare continuation hierarchy, dimmed content, prompt controls, and library |
| Welcome versus sync boundary | Reminders [welcome](../../assets/ios/reminders/welcome.png) and [iCloud sync prompt](../../assets/ios/reminders/icloud-sync-prompt.png) | Compare welcome composition, follow-up prompt, and obscured root content |
| Centered welcome only | Health [welcome](../../assets/ios/health/welcome.png) | Illustration/copy/action vertical arrangement and surrounding whitespace |
| Location alert over first-run surface | Maps [location permission](../../assets/ios/maps/location-permission.png) | Alert/action alignment, dimmed application context, visible surrounding controls |
| Location alert and refusal path | Wallet [location permission](../../assets/ios/wallet/location-permission.png) | System choice placement and underlying wallet surface; post-refusal is not captured |

## Review checks

Check applicable intro, primer, system decision, deny/defer, repeated request, settings recovery, grant, and limited-function states. Treat alert pixels as capture evidence, not API choice or platform dimensions.
