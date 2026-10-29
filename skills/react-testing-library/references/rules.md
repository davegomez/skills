# Rules

This file holds the rules both platforms share. Each rule has an ID, a severity, a `Source:` line, the practice, a `Detect:` line with the pattern to look for in review, and its ESLint rule if one exists. ESLint rule names are `testing-library/<name>` unless they start with `jest-dom/`. The IDs Q6 and I3 are retired and are not reused.

The platform files complete these rules. A heading with the same ID, such as `### E1 · web` in [web.md](web.md) or `### E1 · native` in [native.md](native.md), adds that platform's examples, Detect patterns, and matchers. Read the two together and cite the bare ID (`E1`). Rules for one platform only live in its file: S2 and W6 in web.md, N1 to N8 in native.md. Examples in this file run unchanged on both platforms.

What the severities mean, in Kent C. Dodds's words from "Common mistakes with React Testing Library":

- **high**: "definitely listen to this advice! You're likely missing confidence or will have problematic tests"
- **medium**: "you might experience bugs, lose confidence, or be doing work you don't need to"
- **low**: "this is mostly just my opinion, feel free to ignore and you'll probably be fine."

`Source:` lines use these short names:

- KCD-CM: that article, https://kentcdodds.com/blog/common-mistakes-with-react-testing-library. KCD "<title>": another post on https://kentcdodds.com/blog.
- TL: the Testing Library docs, https://testing-library.com/docs. RTL is `@testing-library/react`, DTL is `@testing-library/dom`.
- RNTL: the RNTL 14 docs, https://oss.callstack.com/react-native-testing-library. RNTL-CM: its guide "Common mistakes". RNTL `src/…`: a file in the RNTL source.
- ETL: `eslint-plugin-testing-library`. EJD: `eslint-plugin-jest-dom`.
- `Level: derived`: neither KCD-CM nor RNTL-CM rates the rule, so the level is this skill's own.

## Setup

### S1 · medium · Lint tests with the Testing Library ESLint plugins

Source: KCD-CM "Not using ESLint plugins"; ETL README configs; RNTL-CM "ESLint plugins"; ETL `no-await-sync-events`, `await-async-events`.

This rule applies only when the project lints with ESLint. The config is in the platform's S1 section.

### S3 · medium · Let Testing Library clean up automatically in Jest

Source: KCD-CM "Using cleanup"; TL RTL api `cleanup`.

In Jest, Testing Library cleans up after each test by itself. On the web, the Vitest setup file in S2 is the only place a test suite calls `cleanup`.

Detect: `afterEach(cleanup)` or `cleanup()` in a Jest test file. ESLint: `no-manual-cleanup`.

### S4 · medium · Render inside each test, through the project's custom render

Source: TL RTL setup "Custom Render"; ETL `no-render-in-lifecycle`; TL user-event intro. Level: derived.

If the project has a test-utils render, use it. If not, pass providers (router, query client, theme) with the `wrapper` option, as in the platform's S4 example.

Detect: provider JSX copied into each test even though test-utils exists; `render` inside `beforeEach`. ESLint: `no-render-in-lifecycle`.

### S5 · high · Restore every global change after each test

Source: TL "Using Fake Timers"; Jest `restoreAllMocks`, `clearMocks`; Vitest `restoreMocks`, `mockClear`, `stubGlobal`. Level: derived.

A test that patches a global, a prototype, or a document property and leaves it patched makes later tests depend on their order. TL says to "restore the timers after your test runs, just like regular mocks. This prevents fake timers leaking into other test cases".

- Patch with `vi.spyOn` / `jest.spyOn` and restore with `restoreAllMocks` or the `restoreMocks` config option. `clearAllMocks` and `mockClear` do not remove a mock implementation, so they do not restore a spy.
- For a getter, spy with `vi.spyOn(obj, 'prop', 'get')` / `jest.spyOn(obj, 'prop', 'get')`.
- `spyOn` throws when the property does not exist (for example `scrollIntoView` in jsdom). There, save the original and put it back.
- Stub with `vi.stubGlobal` and restore with `vi.unstubAllGlobals`.
- Otherwise save the original and put it back in `afterEach`:

```js
const originalFetch = globalThis.fetch
afterEach(() => {
  globalThis.fetch = originalFetch
})
```

Detect: `Object.defineProperty(document|window|navigator, …)`, or a direct assignment to `globalThis.x`, `window.x`, or `SomeClass.prototype.x`, with no matching restore; a spy restored only with `clearAllMocks` or `mockClear`; fake timers that are never switched back to real timers. `restoreAllMocks` does not undo a direct assignment of `vi.fn()` or `jest.fn()`.

## Queries

### Q1 · high · Query by role first

Source: KCD-CM "Using the wrong query"; TL queries priority; TL ByRole; W3C html-aria; RNTL queries ByRole.

Pick queries in the platform's priority order, which starts with `ByRole`, and pass the accessible name as `name`. `ByTestId` fits only an element that has no role, no label, and no stable text, such as a non-interactive container or content that changes on every render.

Detect: `ByText` or `ByPlaceholderText` used on an element that has a role and an accessible name. ESLint: `no-test-id-queries` (not part of the recommended config).

### Q2 · high · Find elements the way a user does, not by tree structure

Source: KCD-CM "Using container"; TL RTL api `container`; RNTL-CM "Using container"; ETL `no-node-access`.

Correct: `screen.getByRole('button', { name: /click me/i })`. The platform's Q2 section lists the structure access to flag.

### Q3 · high · Query by the text the user sees

Source: KCD-CM "Not querying by text"; TL RTL setup "Custom Render"; TL example-react-intl.

Use the actual rendered text. If the app is localized, load the real translation resources for the default locale in the test setup file and query that locale's strings. Correct: `screen.getByRole('button', { name: /sign in/i })`.

Detect: an i18n key used as query text (`getByText('auth.signIn')`); a mocked translation function, for which TL's react-intl example lists the disadvantage "Tests may assert about message IDs but not enough about content"; `getByTestId` on an element that has visible text.

### Q4 · medium · Query and debug through `screen`

Source: KCD-CM "Not using screen"; RNTL-CM "Not using screen".

Take only `rerender`, `unmount`, and the values the project's custom render adds (such as a `user` instance, S4) from the result of `render`, and query and debug through `screen`.

Detect: queries or `debug` destructured from the result of `render`, such as `const { getByRole, debug } = render(`. Report a `container` destructure under Q2 only. ESLint: `prefer-screen-queries`.

### Q5 · low · Destructure the render result or call it `view`

Source: KCD-CM "Using wrapper"; ETL `render-result-naming-convention`.

Correct: `const { rerender } = render(<Counter />)` or `const view = render(<Counter />)`. Native puts `await` before `render` (N1).

Detect: a render result named `wrapper`, such as `const wrapper = render(`. ESLint: `render-result-naming-convention`.

## Interaction

### I1 · medium · Interact through user-event

Source: KCD-CM "Not using user-event"; TL user-event intro; RNTL user-event.

user-event fires the whole event sequence a real user triggers. `fireEvent` dispatches a single event. The platform's I1 section lists the `fireEvent` calls to flag.

### I2 · medium · Set up user-event in each test and await every call

Source: TL user-event intro and api; RNTL user-event. Level: derived.

Every user-event method returns a promise. Call `userEvent.setup()` inside the test, or in a setup function the test calls, before `render`. Make the test `async` and `await` each call.

Detect: a `user.*` call with no `await`; a `userEvent.<method>(` call without `setup()`; `userEvent.setup()` inside `beforeEach`. ESLint: `await-async-events`.

## Async

### W1 · high · Await `find*` for elements that appear later

Source: KCD-CM "Using waitFor to wait for elements that can be queried with find*"; TL "Appearance and Disappearance".

Correct: `const button = await screen.findByRole('button', { name: /submit/i })`. Await every `find*` and every `waitFor`.

Detect: `await waitFor(() => screen.getBy...)`; a `find*` or `waitFor` call with no `await`. ESLint: `prefer-find-by`, `await-async-queries`, `await-async-utils`.

### W2 · high · Make each `waitFor` assert the condition being awaited

Source: KCD-CM "Passing an empty callback to waitFor", "Performing side-effects in waitFor"; ETL `no-wait-for-snapshot`.

```jsx
await waitFor(() => expect(fetch).toHaveBeenCalledWith('/api/user'))
expect(screen.getByRole('dialog')).toMatchSnapshot()
```

Detect: `await waitFor(() => {})`; `toMatchSnapshot` or `toMatchInlineSnapshot` inside `waitFor`, which generates one snapshot per loop. ESLint: `no-wait-for-snapshot`.

### W3 · high · Trigger side effects before `waitFor`, never inside it

Source: KCD-CM "Performing side-effects in waitFor"; TL api-async `waitFor`; RNTL `src/wait-for.ts`.

`waitFor` reruns its callback on an interval until it passes or times out, so a side effect inside it runs over and over.

```jsx
await user.type(screen.getByLabelText(/search/i), 'react')
await waitFor(() => expect(fetch).toHaveBeenCalledWith('/api/search?q=react'))
```

Detect: a `user.*`, `fireEvent.*`, `render`, or state change inside a `waitFor` callback. ESLint: `no-wait-for-side-effects`.

### W4 · low · Put one assertion in each `waitFor`

Source: KCD-CM "Having multiple assertions in a single waitFor callback".

When the first assertion fails, the error shows up quickly. Put the other assertions after the `waitFor`. Correct: `await waitFor(() => expect(fetch).toHaveBeenCalledWith('/api/user'))`, then `expect(fetch).toHaveBeenCalledTimes(1)`.

Detect: two or more `expect` calls in a single `waitFor` callback. ESLint: `no-wait-for-multiple-assertions`.

### W5 · medium · Wait for disappearance with `query*`

Source: TL "Appearance and Disappearance"; TL api-async `waitForElementToBeRemoved`. Level: derived.

```jsx
await waitForElementToBeRemoved(() => screen.queryByText(/loading/i))
```

`waitForElementToBeRemoved` throws if the element is already gone when it is called. Use the platform's `waitFor` form when the element may never have appeared.

Detect: `waitForElementToBeRemoved` or `waitFor` used with `getBy*` to wait for removal. ESLint: `prefer-query-by-disappearance`.

## Assertions

### E1 · high · Assert with the Testing Library matchers

Source: KCD-CM "Using the wrong assertion"; jest-dom README; EJD rules; RNTL jest-matchers.

Assert state with the platform's matchers instead of reading element properties. The platform's E1 section lists the matchers and the reads to flag.

### E2 · high · Use `get*` for presence and `query*` only for absence

Source: KCD-CM "Using query* variants for anything except checking for non-existence"; RNTL guides.

Detect: a `queryBy*` asserted present; a `getBy*` asserted absent.

### E3 · high · Make sure each test can fail

Source: KCD "Make Your Test Fail"; W3C html-aria; RNTL queries `includeHiddenElements`. Level: derived.

Kent C. Dodds: "it's very possible that you've written a test that cannot fail". After a test passes, break the behaviour it covers in the source, run the test and see it fail, then restore the source. The platform's E3 section names the cases where an absence assertion passes no matter what.

Detect: the patterns in the platform's E3 section.

### E4 · low · Follow the project's choice for bare `get*` assertions

Source: KCD-CM "Using get* variants as assertions"; ETL `prefer-explicit-assert`, `prefer-implicit-assert`.

This is a team choice. If the project enables `prefer-explicit-assert`, wrap the query in `expect` with the presence matcher from E2. If it enables `prefer-implicit-assert`, a bare `screen.getByRole('alert')` is the assertion. If neither is enabled, use the explicit form. In a review, report this rule only when the file conflicts with the project's ESLint config.

Detect: the form opposite to the configured rule. ESLint: `prefer-explicit-assert`, `prefer-implicit-assert`.

## act

### A1 · medium · Let Testing Library utilities handle act

Source: KCD-CM "Wrapping things in act unnecessarily"; RNTL-CM "act".

`render`, `rerender`, `fireEvent`, user-event, `waitFor`, and `find*` already run inside `act`, so they need no `act` around them.

Detect: `act(() => render(...))`; `act` wrapped around `rerender`, `fireEvent`, or `user.*`. ESLint: `no-unnecessary-act`.

### A2 · medium · Wrap state changes made outside Testing Library in act

Source: KCD "Fix the not wrapped in act(...) warning"; react.dev `act`; React 19 upgrade guide; RNTL `act`. Level: derived.

Use `act` when you advance fake timers, call a function on a `renderHook` result, or update an external store or emitter directly. An act warning means something updated that the test never waits for. Wait for the result with `find*` or `waitFor`, or wrap whatever triggered it.

Detect: an act warning in the test output; a timer advance, `result.current.*()` call, or store update outside `act`.

## Component markup

### M1 · high · Give each element its role and name in the component

Source: KCD-CM "Adding aria-, role, and other accessibility attributes incorrectly"; TL ByRole; WAI-ARIA APG.

When an element is hard to query, the fix goes in the component, not the test. The platform's M1 section says how its markup carries roles and names.

## Debugging

Source: ETL `no-debugging-utils`.

Reference only, no severity. The platform file lists the tools. Delete every debug call before you finish. ESLint: `no-debugging-utils`.
