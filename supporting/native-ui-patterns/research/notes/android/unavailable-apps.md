# Unavailable or inspection-limited Android apps

## Not installed as the requested Google app

- **Camera:** [Observed] `adb shell pm path com.google.android.GoogleCamera` returned no package. [Observed] `com.android.camera2` was installed at `/product/app/Camera2/Camera2.apk`, but it was not used as a substitute because the requested Google Camera app was unavailable.
- **Weather:** [Observed] `adb shell pm path com.google.android.apps.weather` returned no package. [Observed] `com.google.android.googlequicksearchbox` was installed, but Google Search was not substituted for a standalone Weather app.
- **Wallet:** [Observed] `adb shell pm path com.google.android.apps.walletnfcrel` returned no package.
- **Keep:** [Observed] `adb shell pm path com.google.android.keep` returned no package.

## Installed but account- or permission-limited

- **Google Play Store:** [Observed] The only visible primary action was Sign in; catalog and detail surfaces were not inspected.
- **Gmail:** [Observed] After the “New in Gmail” acknowledgement, the app displayed address setup and “Add an email address”; no inbox was reached.
- **Calendar:** [Observed] The launch sequence showed “Checking info…” and then a Google Accounts “Sign in with ease” screen; no calendar view was reached.
- **Drive:** [Observed] Launching Drive showed the same Google Accounts setup surface; no file list was reached.
- **Photos:** [Observed] A “Keep your memories safe” sign-in primer covered the media surface; Photos and Search bottom destinations were visible behind it, but library/detail behavior was not inspected.
- **YouTube Music:** [Observed] “Device files only” led to an in-app explanation requiring media permission; the audit did not grant it, so device-file lists and player detail were not inspected.

## Explicit non-substitutions

- [Observed] No OEM or third-party app was opened to fill a missing requested app.
- [Observed] No web source, browser search, account login, pre-granted permission, purchase, message send, phone call, saved contact, saved alarm, or persistent-data deletion was used.
- [Inferred] The unavailable and limited statuses are properties of this inspected AVD state and may differ on another Android 17 image.
