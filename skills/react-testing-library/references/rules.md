# Rules

This file holds every rule for writing and for reviewing. Each rule has an ID, a severity, the practice, a correct example, a `Detect:` line with the pattern to look for in review, and its ESLint rule if one exists. ESLint rule names are `testing-library/<name>` unless they start with `jest-dom/`.

What the severities mean:

- **high**: the test can pass while the feature is broken, or it fails or hangs for reasons that have nothing to do with the feature.
- **medium**: the test gives less _confidence_ or costs more upkeep.
- **low**: style only.

## Setup

### S1 · medium · Lint tests with both Testing Library plugins

```js
// eslint.config.js
import testingLibrary from 'eslint-plugin-testing-library'
import jestDom from 'eslint-plugin-jest-dom'

const files = ['**/*.test.{js,jsx,ts,tsx}']
export default [
  { files, ...testingLibrary.configs['flat/react'] },
  { files, ...jestDom.configs['flat/recommended'] },
]
```

Detect: neither plugin appears in the ESLint config.

### S2 · high · Finish the runner setup

- RTL 16 and later lists `@testing-library/dom` as a peer dependency, so install it next to `@testing-library/react`. RTL 16.3 supports React 18 and 19 only.
- jest-dom 6 and later: in the setup file, import the entry for your runner. `extend-expect` no longer exists.

  | Runner | Config key | Import |
  |---|---|---|
  | Jest | `setupFilesAfterEnv` | `@testing-library/jest-dom` |
  | Jest with `@jest/globals` | `setupFilesAfterEnv` | `@testing-library/jest-dom/jest-globals` |
  | Vitest | `setupFiles` | `@testing-library/jest-dom/vitest` |

- jest-dom 7 also needs `@testing-library/dom` as a peer and Node 22.
- Cleanup: RTL unmounts after each test only if a global `afterEach` exists. Jest always provides one. Vitest provides one only with `globals: true`. Without that, register cleanup in the setup file:

```ts
// vitest.setup.ts
import { afterEach } from 'vitest'
import { cleanup } from '@testing-library/react'
import '@testing-library/jest-dom/vitest'

afterEach(() => {
  cleanup()
})
```

Detect: `@testing-library/dom` missing from `package.json`; `@testing-library/jest-dom/extend-expect`; jest-dom under an unknown key such as `setupFilesAfterEach`; a Vitest config with no `globals: true` and no setup file that calls `cleanup`. The usual symptom is "Found multiple elements" errors caused by DOM left over from earlier tests.

### S3 · medium · Let RTL clean up automatically in Jest

In Jest, RTL cleans up after each test by itself. The Vitest setup file in S2 is the only place a test suite calls `cleanup`.

Detect: `afterEach(cleanup)` or `cleanup()` in a Jest test file. ESLint: `no-manual-cleanup`.

### S4 · medium · Render inside each test, through the project's custom render

If the project has a test-utils render, use it. If not, pass providers (router, query client, theme) with the `wrapper` option:

```jsx
const Providers = ({ children }) => (
  <ThemeProvider theme={theme}>
    <MemoryRouter>{children}</MemoryRouter>
  </ThemeProvider>
)
render(<Profile />, { wrapper: Providers })
```

Detect: provider JSX copied into each test even though test-utils exists; `render` inside `beforeEach`. ESLint: `no-render-in-lifecycle`.

## Queries

### Q1 · high · Query by role first

Pick queries in this order: `ByRole`, `ByLabelText`, `ByPlaceholderText`, `ByText`, `ByDisplayValue`, `ByAltText`, `ByTitle`, `ByTestId`. Pass the role as a string and the accessible name as `name`:

```jsx
screen.getByRole('button', { name: /submit/i })
screen.getByRole('textbox', { name: /email/i })
screen.getByRole('heading', { name: /welcome/i })
```

The markup decides the role. An `<input>` with no `type` is a `textbox`. `type="search"` gives `searchbox`, `type="number"` gives `spinbutton`, and `type="password"` gives no role at all, so query it with `getByLabelText`. `form` and `region` count as roles only when the element has an accessible name. `ByTestId` fits only an element that has no role, no label, and no stable text, such as a non-interactive container or content that changes on every render.

Detect: `ByText`, `ByLabelText`, or `ByPlaceholderText` used on a button, link, input, or heading that has a role and a name; a regex as the role (`getByRole(/butt/)`). ESLint: `no-test-id-queries` (not part of the recommended config).

### Q2 · high · Find elements the way a user does, not by DOM structure

Correct: `screen.getByRole('button', { name: /click me/i })`.

Detect: `container.querySelector`, `.closest(`, `.parentElement`, `.children`, `.firstChild`. ESLint: `no-container`, `no-node-access`.

### Q3 · high · Query by the text the user sees

Use the actual rendered text. If the app is localized, render it in the default locale and query that locale's strings. Correct: `screen.getByRole('button', { name: /sign in/i })`.

Detect: an i18n key used as query text (`getByText('auth.signIn')`); a mocked `t` that returns keys; `getByTestId` on an element that has visible text.

### Q4 · medium · Query and debug through `screen`

Correct: `render(<Login />)`, then `screen.getByRole(...)` and `screen.debug()`. Take only `rerender` or `unmount` from the result of `render`. The one exception to `screen` is a `render` call with the `container` or `baseElement` option, and you should avoid those options.

Detect: `const { getByRole, debug } = render(`. ESLint: `prefer-screen-queries`.

### Q5 · low · Destructure the render result or call it `view`

Correct: `const { rerender } = render(<Counter />)` or `const view = render(<Counter />)`.

Detect: `const wrapper = render(`. ESLint: `render-result-naming-convention`.

### Q6 · medium · Scope repeated elements with `within`

```jsx
const row = screen.getByRole('row', { name: /alice/i })
await user.click(within(row).getByRole('button', { name: /delete/i }))
```

Detect: `getAllByRole(...)[n]` used to pick one item out of a list, table, or dialog.

## Interaction

### I1 · medium · Interact through user-event

user-event fires the whole event sequence a real user triggers (pointer, keyboard, focus, input). `fireEvent` dispatches a single event. Correct: `await user.type(input, 'hello')`, `await user.click(button)`.

Detect: `fireEvent.click`, `fireEvent.change`, or `fireEvent.keyDown` where user-event has an equivalent. ESLint: `prefer-user-event`.

### I2 · medium · Set up user-event in each test and await every call

In user-event 14, every method returns a promise. Call `userEvent.setup()` inside the test, or in a setup function the test calls, before `render`. Make the test `async` and `await` each call. `user.type` clicks the element before typing. For key presses on the focused element, use `user.keyboard`.

```jsx
test('submits on Enter', async () => {
  const user = userEvent.setup()
  render(<Search />)
  await user.type(screen.getByRole('searchbox'), 'react')
  await user.keyboard('{Enter}')
})
```

Detect: a `user.*` call with no `await`; `userEvent.click(` called without `setup()`; `userEvent.setup()` inside `beforeEach`. ESLint: `await-async-events`, `prefer-user-event-setup`.

## Async

### W1 · high · Await `find*` for elements that appear later

Correct: `const button = await screen.findByRole('button', { name: /submit/i })`. Await every `find*` and every `waitFor`. If you don't, the assertion keeps running after the test has already passed.

Detect: `await waitFor(() => screen.getBy...)`; a `find*` or `waitFor` call with no `await`. ESLint: `prefer-find-by`, `await-async-queries`, `await-async-utils`.

### W2 · high · Make each `waitFor` assert the condition being awaited

```jsx
await waitFor(() => expect(fetch).toHaveBeenCalledWith('/api/user'))
expect(screen.getByRole('dialog')).toMatchSnapshot()
```

Detect: `await waitFor(() => {})`; `toMatchSnapshot` or `toMatchInlineSnapshot` inside `waitFor`. Both resolve right away and assert nothing about the async work. ESLint: `no-wait-for-snapshot`.

### W3 · high · Trigger side effects before `waitFor`, never inside it

`waitFor` reruns its callback on an interval and on every DOM mutation, so a side effect inside it runs over and over.

```jsx
await user.keyboard('{ArrowDown}')
await waitFor(() => expect(screen.getAllByRole('option')).toHaveLength(3))
```

Detect: a `user.*`, `fireEvent.*`, `render`, or state change inside a `waitFor` callback. ESLint: `no-wait-for-side-effects`.

### W4 · low · Put one assertion in each `waitFor`

When the first assertion fails, the error shows up quickly. Put the other assertions after the `waitFor`. Correct: `await waitFor(() => expect(fetch).toHaveBeenCalledWith('/api/user'))`, then `expect(fetch).toHaveBeenCalledTimes(1)`.

Detect: two or more `expect` calls in a single `waitFor` callback. ESLint: `no-wait-for-multiple-assertions`.

### W5 · medium · Wait for disappearance with `query*`

```jsx
await waitForElementToBeRemoved(() => screen.queryByText(/loading/i))
await waitFor(() => expect(screen.queryByText(/loading/i)).not.toBeInTheDocument())
```

`waitForElementToBeRemoved` throws if the element is already gone when it is called. Use the `waitFor` form when the element may never have appeared.

Detect: `waitForElementToBeRemoved` or `waitFor` used with `getBy*` to wait for removal. ESLint: `prefer-query-by-disappearance`.

### W6 · high · Configure fake timers so tests advance instead of hanging

- Give user-event the clock: `userEvent.setup({ advanceTimers: jest.advanceTimersByTime })` or `{ advanceTimers: vi.advanceTimersByTime }`.
- `waitFor` and `find*` advance fake timers automatically only when a global `jest` exists. Under Vitest fake timers they wait until the test times out. Either use `vi.useFakeTimers({ shouldAdvanceTime: true })`, or advance the clock yourself inside `act` and then assert synchronously:

```jsx
act(() => {
  vi.advanceTimersByTime(1000)
})
expect(screen.getByRole('status')).toHaveTextContent(/saved/i)
```

Detect: `useFakeTimers` together with a bare `userEvent.setup()`; `vi.useFakeTimers()` followed by `find*` or `waitFor` with no `shouldAdvanceTime`.

## Assertions

### E1 · high · Assert with jest-dom matchers

```jsx
expect(button).toBeDisabled()
expect(element).toBeVisible()
expect(element).toHaveTextContent(/hello/i)
expect(input).toHaveValue('test')
```

On jest-dom 7, `toContainOneBy*` and `toContainAnyBy*` check whether an element contains descendants, including when there are none: `expect(related).toContainOneByRole('heading', { name: /related/i })`, `expect(results).not.toContainAnyByRole('alert')`.

Detect: `expect(button.disabled).toBe(true)`, `expect(el.textContent).toBe(...)`, `expect(el.className)`, `expect(el).not.toBeNull()`. ESLint: the `jest-dom/prefer-*` rules.

### E2 · high · Use `get*` for presence and `query*` only for absence

Correct: `expect(screen.getByRole('alert')).toBeInTheDocument()` and `expect(screen.queryByRole('alert')).not.toBeInTheDocument()`.

Detect: `expect(screen.queryBy...).toBeInTheDocument()`; `expect(screen.getBy...).not.toBeInTheDocument()`. ESLint: `prefer-presence-queries`.

### E3 · high · Pair every absence assertion with a presence check

A wrong role, a missing accessible name, or a typo makes an absence assertion pass no matter what. Before the action that removes the element, check that it is present with the same exact role and name. The roles that need a name are listed in Q1.

```jsx
const dialog = screen.getByRole('dialog', { name: /confirm/i })
await user.click(within(dialog).getByRole('button', { name: /cancel/i }))
expect(screen.queryByRole('dialog', { name: /confirm/i })).not.toBeInTheDocument()
```

Detect: a `query*` + `.not.toBeInTheDocument()` with no earlier `get*`/`find*` of the same query; `queryByRole('form')` or `queryByRole('region')` on an element without a name.

### E4 · low · Follow the project's choice for bare `get*` assertions

This is a team choice. If the project enables `prefer-explicit-assert`, wrap the query: `expect(screen.getByRole('alert')).toBeInTheDocument()`. If it enables `prefer-implicit-assert`, a bare `screen.getByRole('alert')` is the assertion. If neither is enabled, use the explicit form. In a review, report this rule only when the file conflicts with the project's ESLint config.

Detect: the form opposite to the configured rule. ESLint: `prefer-explicit-assert`, `prefer-implicit-assert`.

## act

### A1 · medium · Let RTL utilities handle act

`render`, `fireEvent`, user-event (through RTL), `waitFor`, and `find*` already run inside `act`. Correct: `render(<Example />)`, then `await user.click(button)`, with no `act` around either.

Detect: `act(() => render(...))`; `act` wrapped around `fireEvent` or `user.*`. ESLint: `no-unnecessary-act`.

### A2 · medium · Wrap state changes made outside RTL in act

Use `act` when you advance fake timers, call a function on a `renderHook` result, or update an external store or emitter directly. An act warning means something updated that the test never waits for. Wait for the result with `find*` or `waitFor`, or wrap whatever triggered it. Import `act` and `renderHook` from `@testing-library/react`.

```jsx
act(() => {
  result.current.increment()
})
expect(result.current.count).toBe(1)
```

Detect: an act warning in the test output; a timer advance, `result.current.*()` call, or store update outside `act`; `act` imported from `react-dom/test-utils` (deprecated in React 19); imports from `@testing-library/react-hooks` (replaced by `renderHook` in RTL 13.1).

## Component markup

### M1 · high · Use semantic elements, and add ARIA only where HTML has no equivalent

Correct: `<button onClick={save}>Save</button>`, `<nav aria-label="Main">`. Native elements come with their roles. For custom widgets such as an autocomplete, a tabs component, or a menu, use an existing accessible component library or follow the WAI-ARIA Authoring Practices pattern (https://www.w3.org/WAI/ARIA/apg/patterns/).

Detect: `<button role="button">` and other roles that repeat the native one; `<div onClick>` acting as a button; `role` or `aria-*` added just so a test can find the element. The fix goes in the component, not the test.

## Debugging

Reference only, no severity.

- If `getByRole` fails, its error lists every role and accessible name in the DOM. Read that list before you change the query.
- `screen.debug()` prints the DOM, and `screen.debug(element)` prints one subtree. Output is cut off at 7000 characters. Set the `DEBUG_PRINT_LIMIT` environment variable to raise the limit.
- `logRoles(document.body)` prints every element grouped by role.
- `screen.logTestingPlaygroundURL()` prints a link that suggests a query for each element.
- Delete every debug call before you finish. ESLint: `no-debugging-utils`.

## Test template

```jsx
// When Vitest runs without `globals: true`, also import { test, expect } from 'vitest'.
// If the project has test-utils, import render from there.
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { SignupForm } from './SignupForm'

test('confirms the signup after the user submits an email', async () => {
  const user = userEvent.setup()
  render(<SignupForm />)

  await user.type(screen.getByRole('textbox', { name: /email/i }), 'ada@example.com')
  await user.click(screen.getByRole('button', { name: /sign up/i }))

  expect(await screen.findByRole('status')).toHaveTextContent(/check your inbox/i)
  // The click above already proved the button was present (E3).
  expect(screen.queryByRole('button', { name: /sign up/i })).not.toBeInTheDocument()
})
```
