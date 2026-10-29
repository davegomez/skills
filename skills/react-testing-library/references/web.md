# Web

The web parts of the rules, for `@testing-library/react`, user-event, and jest-dom. Each `### <ID> · web` section completes the rule with the same ID in [rules.md](rules.md), which also defines the short names in `Source:` lines. S2 and W6 apply to the web only.

## Setup

### S1 · web

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

Source: RTL README; jest-dom README and v6.0.0/v7.0.0 releases; TL RTL setup "Auto Cleanup in Vitest"; Vitest config `globals`. Level: derived.

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

Detect: `@testing-library/dom` missing from `package.json`; `@testing-library/jest-dom/extend-expect`; jest-dom under an unknown key such as `setupFilesAfterEach`; a Vitest config with no `globals: true` and no setup file that calls `cleanup`.

### S4 · web

```jsx
const Providers = ({ children }) => (
  <ThemeProvider theme={theme}>
    <MemoryRouter>{children}</MemoryRouter>
  </ThemeProvider>
)
render(<Profile />, { wrapper: Providers })
```

## Queries

### Q1 · web

Pick queries in this order: `ByRole`, `ByLabelText`, `ByPlaceholderText`, `ByText`, `ByDisplayValue`, `ByAltText`, `ByTitle`, `ByTestId`. Pass the role as a string:

```jsx
screen.getByRole('button', { name: /submit/i })
screen.getByRole('textbox', { name: /email/i })
screen.getByRole('heading', { name: /welcome/i })
```

The markup decides the role. An `<input>` with no `type` is a `textbox`. `type="search"` gives `searchbox`, `type="number"` gives `spinbutton`, and `type="password"` gives no role at all, so query it with `getByLabelText`. `form` and `region` count as roles only when the element has an accessible name.

Detect: a regex as the role (`getByRole(/butt/)`).

### Q2 · web

Detect: `const { container } = render(`; `querySelector` or `querySelectorAll` on `container`, `document`, or any element; `.closest(`, `.parentElement`, `.children`, `.firstChild`. ESLint: `no-container`, `no-node-access`.

### Q4 · web

Correct: `render(<Login />)`, then `screen.getByRole(...)` and `screen.debug()`. The one exception to `screen` is a `render` call with the `container` or `baseElement` option, and you should avoid those options.

### `within`

Reference only, no severity. `within(element)` returns the queries scoped to that element.

```jsx
const row = screen.getByRole('row', { name: /alice/i })
await user.click(within(row).getByRole('button', { name: /delete/i }))
```

## Interaction

### I1 · web

On the web the sequence covers pointer, keyboard, focus, and input. Correct: `await user.type(input, 'hello')`, `await user.click(button)`.

Detect: `fireEvent.click`, `fireEvent.change`, or `fireEvent.keyDown` where user-event has an equivalent. ESLint: `prefer-user-event`.

### I2 · web

In user-event 14, `user.type` clicks the element before typing. For key presses on the focused element, use `user.keyboard`.

```jsx
test('submits on Enter', async () => {
  const user = userEvent.setup()
  render(<Search />)
  await user.type(screen.getByRole('searchbox'), 'react')
  await user.keyboard('{Enter}')
})
```

ESLint: `prefer-user-event-setup`.

## Async

### W5 · web

```jsx
await waitFor(() => expect(screen.queryByText(/loading/i)).not.toBeInTheDocument())
```

### W6 · high · Configure fake timers so tests advance instead of hanging

Source: TL user-event options `advanceTimers`; DTL `src/helpers.ts`; Vitest config fake timers. Level: derived.

- Give user-event the clock: `userEvent.setup({ advanceTimers: jest.advanceTimersByTime })` or `{ advanceTimers: vi.advanceTimersByTime }`.
- `waitFor` and `find*` advance fake timers automatically only when a global `jest` exists. Under Vitest fake timers they wait until the test times out. Either use `vi.useFakeTimers({ shouldAdvanceTime: true })`, or advance the clock yourself inside `act` and then assert synchronously:

```jsx
await act(async () => {
  vi.advanceTimersByTime(1000)
})
expect(screen.getByRole('status')).toHaveTextContent(/saved/i)
```

Detect: `useFakeTimers` together with a bare `userEvent.setup()`; `vi.useFakeTimers()` followed by `find*` or `waitFor` with no `shouldAdvanceTime`.

## Assertions

### E1 · web

```jsx
expect(button).toBeDisabled()
expect(element).toBeVisible()
expect(element).toHaveTextContent(/hello/i)
expect(input).toHaveValue('test')
expect(link).toHaveAttribute('href', '/home')
```

On jest-dom 6.9 and later, `expect(first).toAppearBefore(second)` and `toAppearAfter` check DOM order. They ignore CSS that reorders elements.

On jest-dom 7, `toContainOneBy*` and `toContainAnyBy*` check whether an element contains descendants, including when there are none: `expect(related).toContainOneByRole('heading', { name: /related/i })`, `expect(results).not.toContainAnyByRole('alert')`.

Detect: `expect(button.disabled).toBe(true)`, `expect(el.textContent).toBe(...)`, `expect(el.className)`, `expect(el).not.toBeNull()`; `el.getAttribute(...)` in an assertion; element order checked by mapping `textContent` into an array and comparing it, or with `compareDocumentPosition` (replaced by `toAppearBefore` / `toAppearAfter` on jest-dom 6.9 and later). ESLint: the `jest-dom/prefer-*` rules.

### E2 · web

Correct: `expect(screen.getByRole('alert')).toBeInTheDocument()` and `expect(screen.queryByRole('alert')).not.toBeInTheDocument()`. ESLint: `prefer-presence-queries`.

### E3 · web

`form` and `region` have their role only when the element has an accessible name (Q1). An absence assertion that queries either role on an element without a name matches nothing, so it passes no matter what.

Detect: `queryByRole('form')` or `queryByRole('region')` on an element without a name.

## act

### A1 · web

Correct: `render(<Example />)`, then `await user.click(button)`, with no `act` around either.

### A2 · web

Import `act` and `renderHook` from `@testing-library/react`.

```jsx
await act(async () => {
  result.current.increment()
})
expect(result.current.count).toBe(1)
```

Detect: `act` imported from `react-dom/test-utils` (deprecated in React 19); imports from `@testing-library/react-hooks` (replaced by `renderHook` in RTL 13.1).

## Component markup

### M1 · web

Use semantic elements, and add ARIA only where HTML has no equivalent. Correct: `<button onClick={save}>Save</button>`, `<nav aria-label="Main">`. Native elements come with their roles. For custom widgets such as an autocomplete, a tabs component, or a menu, use an existing accessible component library or follow the WAI-ARIA Authoring Practices pattern (https://www.w3.org/WAI/ARIA/apg/patterns/).

A `section` needs an accessible name to be a region (Q1). Naming it with its visible heading through `aria-labelledby` is a valid accessibility fix: the APG says that if an area begins with a heading, the heading "can be used as the label for the area using the aria-labelledby attribute".

```jsx
<section aria-labelledby="billing-heading">
  <h2 id="billing-heading">Billing</h2>
</section>
```

Detect: `<button role="button">` and other roles that repeat the native one; `<div onClick>` acting as a button; `role` or `aria-*` added just so a test can find the element.

## Debugging

Source: TL api-debugging; ETL `no-debugging-utils`.

- If `getByRole` fails, its error lists every role and accessible name in the DOM. Read that list before you change the query.
- `screen.debug()` prints the DOM, and `screen.debug(element)` prints one subtree. Output is cut off at 7000 characters. Set the `DEBUG_PRINT_LIMIT` environment variable to raise the limit.
- `logRoles(document.body)` prints every element grouped by role.
- `screen.logTestingPlaygroundURL()` prints a link that suggests a query for each element.

## What jsdom does not do

Reference only, no severity. Source: jsdom README; jsdom source; TL example-drag.

- jsdom does no layout: the README calls it "currently outside the scope of jsdom".
- `document.hidden` is `true` unless jsdom runs with `pretendToBeVisual`.
- jsdom does not implement `scrollIntoView` or `inert`.

A test that needs these runs in a real browser.

## Test template

```jsx
// When Vitest runs without `globals: true`, also import { test, expect } from 'vitest'.
// If the project has test-utils, import render from there.
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { SignupForm } from './SignupForm'

// E3: once this passes, break the signup in SignupForm, see the test fail, then restore it.
test('confirms the signup after the user submits an email', async () => {
  const user = userEvent.setup()
  render(<SignupForm />)

  await user.type(screen.getByRole('textbox', { name: /email/i }), 'ada@example.com')
  await user.click(screen.getByRole('button', { name: /sign up/i }))

  expect(await screen.findByRole('status')).toHaveTextContent(/check your inbox/i)
  expect(screen.queryByRole('button', { name: /sign up/i })).not.toBeInTheDocument()
})
```
