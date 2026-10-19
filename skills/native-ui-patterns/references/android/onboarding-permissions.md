# Android onboarding and permissions

## Guidance

**Observed:** Photos used a sign-in card; Maps and Chrome offered deferral; Gmail introduced a setup step; Calendar, Play Store, and Drive were account-bound; YouTube Music separated device-files onboarding from media access explanation. Contacts showed a system notification dialog. These are distinct progression states. **Inferred adaptation:** name the boundary accurately, explain immediate value, preserve a limited path when possible, and separate application primer from system consent. Signed-in, post-grant, repeated request, and network-backed behavior remain **Unconfirmed**.

## Visual references

Choose the exact application/state question. Open one named state; open both only when comparing the progression.

| Visual question / state | Matching capture(s) | What to inspect |
| --- | --- | --- |
| System permission over app context | Contacts [notification permission](../../assets/android/contacts/notification-permission.png) | System dialog/actions, scrim, underlying app chrome and surrounding content |
| Sign-in onboarding versus optional primer | Maps [sign-in onboarding](../../assets/android/maps/sign-in-onboarding.png) and [audio primer](../../assets/android/maps/audio-primer.png) | Compare deferral/action placement, copy hierarchy, and surrounding context |
| Browser onboarding versus notification primer | Chrome [stay-signed-out](../../assets/android/chrome/stay-signed-out-onboarding.png) and [notification primer](../../assets/android/chrome/notification-primer.png) | Compare actions, illustration/copy alignment, and progression |
| Feature intro versus address setup | Gmail [What’s New](../../assets/android/gmail/whats-new.png) and [email setup](../../assets/android/gmail/email-address-setup.png) | Compare continuation hierarchy, account actions, and surrounding blank state |
| Account checking versus setup | Calendar [checking](../../assets/android/calendar/checking-account.png) and [account setup](../../assets/android/calendar/account-setup.png) | Compare progress placement and account hierarchy; no calendar content was reached |
| Account-required landing | Play Store [sign-in required](../../assets/android/play-store/sign-in-required.png), Drive [account setup](../../assets/android/drive/account-setup.png) | Branding, explanation/action placement and unavailable downstream context |
| Modal sign-in primer over shell | Photos [sign-in primer](../../assets/android/photos/sign-in-primer.png) | Card alignment, dimmed peer shell and blocked content |
| Device-files onboarding versus access explanation | YouTube Music [device-files onboarding](../../assets/android/youtube-music/device-files-onboarding.png) and [media-access primer](../../assets/android/youtube-music/media-access-primer.png) | Compare choice placement, explanation/action hierarchy, and underlying surface |

## Review checks

Check applicable first run, account requirement, primer, system request, allow, deny/defer, settings recovery, grant, and limited-function states. Verify current APIs separately; no screenshot establishes permission implementation.
