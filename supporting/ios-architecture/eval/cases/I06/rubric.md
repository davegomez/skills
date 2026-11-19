# I06 rubric (blind reviewer)

`grade.sh` already settles the build, the states, the retry matrix, cancellation, the Spanish strings, the automated accessibility audit (without contrast), and the token in captured logs and `UserDefaults`. Grade only these checks. Each result is `pass`, `fail`, `na`, or `unverified`, with file and line evidence.

| Check id | Priority | Severity | Pass condition |
| --- | --- | --- | --- |
| I06-R-token-storage | security | critical | The access token is read from `AuthService` and held only in memory or the Keychain. No code writes it to a file, a cache, a preference, or a URL. |
| I06-R-no-credential-logging | security | major | No log, print, or analytics call can receive the token, the `Authorization` header, the full header set, or the request or response body on any path, including paths the hidden runs do not reach. |
| I06-R-generic-errors | security | minor | User-facing text shows no status codes, URLs, server messages, or error descriptions. |
| I06-R-response-validation | reliability | major | The code checks the status code and the content type before it decodes, and a decode failure becomes the error state, not a crash. |
| I06-R-retry-scope | reliability | major | Only the idempotent `GET` is retried. The wait between attempts grows exponentially, has jitter, and is bounded, and the backoff wait stops when the load is cancelled. |
| I06-R-cache-protection | security | minor | Saved books are kept in memory only, or in a file with a Data Protection class. |
| I06-R-voiceover-states | accessibility | major | Each state has a VoiceOver-readable label. Each book row reads its title and author together. No state is shown by color alone. |
| I06-R-contrast | accessibility | minor | Text in each state meets a 4.5:1 contrast ratio in light and dark appearance, or uses a system semantic color. The automated audit skips contrast. |
| I06-R-catalog-comments | maintainability | minor | Each new String Catalog entry has a comment that gives context to translators. |
| I06-R-policy-tests | reliability | minor | The change adds automated tests for the failure classification or the retry, offline, and cancellation rules. Tests that only launch the app do not count. |
