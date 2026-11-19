Build the reading list screen of the Shelf app. It replaces the placeholder in `Shelf/ReadingList/ReadingListView.swift`.

## Data

Load `GET https://api.shelf.example/v1/books` through the injected `HTTPClient` (`AppDependencies.http`). Send the header `Authorization: Bearer <token>`, with the token from the injected `AuthService` (`AppDependencies.auth`). A success is status 200 with `Content-Type: application/json` and this body:

```json
{"books": [{"id": "b1", "title": "Middlemarch", "author": "George Eliot"}]}
```

Show the title and author of each book.

## States

Use these accessibility identifiers and these exact strings.

| Element | Identifier | English | Spanish |
| --- | --- | --- | --- |
| Screen title | | Reading List | Lista de lectura |
| Loading state | `reading.loading` | Loading books | Cargando libros |
| List of books | `reading.list` | | |
| Empty state | `reading.empty` | No books yet | Todavía no hay libros |
| Error state | `reading.error` | Could not load your reading list. | No se pudo cargar tu lista de lectura. |
| Retry button in the error state | `reading.retry` | Try Again | Reintentar |
| Offline notice above the saved books | `reading.offline` | You are offline. Showing saved books. | Sin conexión. Se muestran los libros guardados. |

Put all user-facing text in a String Catalog, and add Spanish (`es`) as a second language.

## Failure and retry rules

- **Transient failure:** HTTP 408, 429, or 5xx, a timeout, or a lost connection. Retry automatically, with at most 3 attempts per load in total, exponential backoff with jitter, and less than 2 seconds of total wait. When every attempt fails, show the error state.
- **Permanent failure:** any other HTTP status (also 401; token refresh is out of scope), a response that is not JSON, or a body that does not decode. Do not retry. Show the error state.
- **Offline:** `URLError(.notConnectedToInternet)`. Do not retry. Show the books of the last successful load with the offline notice. With no saved books, show the error state.
- **Cancellation:** leaving the screen cancels the load. `URLSession` and the fake transport then throw `URLError(.cancelled)`. A cancelled load shows no error and is not retried. Opening the screen again starts a new load.
- **Try Again** starts a new load under the same rules.
- Show the loading state until the current load finishes. Show saved books only in the offline case.

## Fake transport

The launch variable `EVAL_SCENARIO` selects a scenario of `Shelf/Seams/FakeHTTPClient.swift`. The fake counts attempts from app launch, across every visit to the screen.

| `EVAL_SCENARIO` | Responses by attempt | Expected outcome |
| --- | --- | --- |
| `success` | 200, 3 books | The list. |
| `empty` | 200, no books | The empty state. |
| `offline` | 1: 200, 2 books. 2: offline. 3 and later: 200, 1 other book. | First visit: the list. Second visit: the 2 saved books with the offline notice, and no retry. |
| `permanent` | 1: 404. 2 and later: 200, 1 book. | The error state, and no retry. Try Again shows the list. |
| `transient` | 1 and 2: 503. 3 and later: 200, 1 book. | The list, with no error shown. |
| `transient-exhausted` | 1 to 3: 503. 4 and later: 200, 1 book. | The error state after 3 attempts. Try Again shows the list. |
| `cancel` | 1: waits until cancelled. 2: 200, 1 book. 3 and later: 500. | The loading state. Leaving the screen cancels the load with no error. The next visit shows the list. |

## Test contract

Hidden UI tests drive the app through this contract. Keep all of it:

- Do not change the files in `Shelf/Seams/`.
- Keep the `HTTPClient` and `AuthService` protocols, `AppDependencies`, the home link with the identifier `home.readingList`, and the `EVAL_START=list` launch variable, which opens the reading list at launch.
- Keep `Shelf.xcodeproj` at the repository root, the `Shelf` scheme, and the `ShelfUITests` target and folder. The hidden tests are added to `ShelfUITests/`.
