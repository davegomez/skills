# React Native

The native parts of the rules, for `@testing-library/react-native` 14 (RNTL). Each `### <ID> · native` section completes the rule with the same ID in [rules.md](rules.md), which also defines the short names in `Source:` lines. N1 to N8 apply to native only. A React 18 project stays on RNTL 13, which N1 and N2 do not describe; tell the user, and check those two rules against the installed version.

## Setup

### S1 · native

eslint-plugin-testing-library has no React Native config. Use `flat/react` and override two rules: `flat/react` flags every correct v14 `await fireEvent`, and it checks the `await` on `userEvent` only. Leave `eslint-plugin-jest-dom` out.

```js
// eslint.config.js
import testingLibrary from 'eslint-plugin-testing-library'

const files = ['**/*.test.{js,jsx,ts,tsx}']
export default [
  { files, ...testingLibrary.configs['flat/react'] },
  {
    files,
    rules: {
      'testing-library/no-await-sync-events': 'off',
      'testing-library/await-async-events': ['error', { eventModule: ['fireEvent', 'userEvent'] }],
    },
  },
]
```

Detect: no `eslint-plugin-testing-library` config for native tests; `flat/react` without the two overrides; `eslint-plugin-jest-dom` in a native config.

### N2 · high · Set up RNTL 14 with its peers and Jest

Source: RNTL migration-v14; RNTL intro; Jest "Testing React Native Apps". Level: derived.

- RNTL 14 needs React 19+, React Native 0.78+, and Node `^22.13 || >=24`.
- Install the `test-renderer` peer with the minor version that matches React's minor: React 19.3 needs `test-renderer` 1.3. Remove `react-test-renderer` and `@types/react-test-renderer`.
- The matchers load from any RNTL import, so remove `@testing-library/jest-native` and its setup import.
- The documented setup runs native tests on Jest with a React Native preset. RNTL "is tested to work with Jest, but it should work with other test runners as well."
- The codemods `rntl-v14-update-deps` and `rntl-v14-async-functions` do most of a v13 upgrade.
- v14 throws when a component renders a string outside `<Text>`. Fix the component.

Detect: `react-test-renderer` or `@testing-library/jest-native` in `package.json`; a `test-renderer` minor that differs from the React minor; a Jest config with no `preset`, or with a `projects` config, a project with no `preset`.

### S4 · native

```jsx
const Providers = ({ children }) => (
  <GestureHandlerRootView>
    <ThemeProvider theme={theme}>{children}</ThemeProvider>
  </GestureHandlerRootView>
)
await render(<Profile />, { wrapper: Providers })
```

## Queries

### Q1 · native

Pick queries in this order: `ByRole`, `ByLabelText`, `ByPlaceholderText`, `ByText`, `ByDisplayValue`, `ByTestId`. `ByLabelText` matches `aria-label`, `aria-labelledby`, `accessibilityLabel`, and an Image's `alt`. `ByHintText` matches `accessibilityHint`. Test IDs mainly serve E2E tools.

`ByRole` matches the `role` or `accessibilityRole` prop (prefer `role`) on accessibility elements only:

- `Text`, `TextInput`, and `Switch` are accessibility elements by default. `Pressable` and `Touchable*` set it, and a `View` needs `accessible`.
- Only `Text` gets an implicit role (`text`). A `TextInput` matches `ByRole` only when it sets `role`, such as `role="textbox"`; otherwise query it with `ByLabelText`, `ByPlaceholderText`, or `ByDisplayValue`.
- Role strings match literally, apart from the `image`/`img` alias, so `'header'` does not find `role="heading"`. A regex role is allowed.
- Options: `name`, `disabled`, `selected`, `checked` (`true`, `false`, or `'mixed'`), `busy`, `expanded`, `value`, and `includeHiddenElements` (N8).

```jsx
screen.getByRole('button', { name: /submit/i })
screen.getByRole('switch', { name: /notifications/i, checked: true })
screen.getByLabelText(/email/i) // a TextInput
```

Detect: `getByRole('textbox')` for a TextInput that sets no `role`; a role string the component does not set, such as `'header'` for `role="heading"`; `ByTestId` on an element with a role, a label, or text.

### Q2 · native

Detect: `.parent`, `.children`, or `container.queryAll` used to find an element. `no-node-access` misses `.parent` and `.props`, so check for them by hand.

### Q4 · native

Correct: `await render(<Login />)`, then `screen.getByRole(...)` and `screen.debug()`. `screen.debug` takes options, not an element (see Debugging).

### `within`

Reference only, no severity. `within(element)` returns the queries scoped to that element.

```jsx
// renderItem gives each row aria-label={item.name}
const row = screen.getByLabelText('Alice')
await user.press(within(row).getByRole('button', { name: /delete/i }))
```

### N8 · medium · Keep hidden elements out of queries

Source: RNTL queries `#includeHiddenElements`. Level: derived.

Queries skip hidden elements by default (`includeHiddenElements: false`). Hidden means `display: none`, `aria-hidden`, `accessibilityElementsHidden`, `importantForAccessibility="no-hide-descendants"`, or a sibling of an `aria-modal` element. When a query misses an element because it is hidden, the user cannot reach it either: fix the component, or assert that it is hidden.

Detect: `includeHiddenElements: true` added to make a query find an element the user should reach.

## Interaction

### I1 · native

userEvent's `press` fires pressIn, press, and pressOut over at least 130 ms. `fireEvent.press` calls the nearest `onPress` handler and nothing else. Correct: `await user.press(button)`, `await user.type(input, 'hello')`.

Detect: `fireEvent.press`, `fireEvent.changeText`, or `fireEvent.scroll` where userEvent has `press`, `type`, or `scrollTo`. `prefer-user-event` has no mapping for `press`, so find these by hand.

### I2 · native

Import `userEvent` as a named export: `import { render, screen, userEvent } from '@testing-library/react-native'`. The default setup handles real timers and Jest fake timers. Pass `userEvent.setup({ advanceTimers })` only with other fake timers.

- `press(el)` and `longPress(el, { duration })`.
- `type(el, text, { skipPress, skipBlur, submitEditing })` works on a `TextInput` only. It sends a `keyPress` for each character and appends to the current value, so call `clear` first to replace a value. It fires nothing when `editable={false}`. Submit with `submitEditing: true`, because userEvent has no `keyboard` method.
- `paste` selects all, replaces the value, and sends no `keyPress`.
- `scrollTo(el, { y, contentSize, layoutMeasurement })`: pass `contentSize` and `layoutMeasurement` so a FlatList updates.
- `clear`, `pullToRefresh`, and `accessibilityAction`.

```jsx
const input = screen.getByLabelText(/name/i)
await user.clear(input)
await user.type(input, 'Ada', { submitEditing: true })
```

### N3 · high · Trigger handlers through userEvent or fireEvent

Source: RNTL fire-event; RNTL config `eventDiagnostics`; KCD "Testing Implementation Details". Level: derived.

Calling `.props.onPress()` or any `.props.onX()` directly skips the disabled, `pointerEvents`, and `editable` checks, so the test passes while the feature is broken. Correct: `await user.press(screen.getByRole('button', { name: /save/i }))`.

Detect: a `.props.on<Event>(` call in a test, such as `button.props.onPress()`.

### N7 · medium · Use fireEvent only where userEvent cannot reach

Source: RNTL fire-event, including `#layout`; RNTL migration-v14. Level: derived.

fireEvent walks up to the nearest enabled `onX` handler and passes no event data unless you give it. Use it for `fireEvent.layout` (RNTL 14.1), events a native module emits, and handlers on composite components that userEvent does not reach. Fire a direct (non-bubbling) event, such as `layout`, on the element that owns the handler.

```jsx
await fireEvent.layout(screen.getByLabelText(/chart/i), { width: 320, height: 200 })
```

`fireEvent.press` and `fireEvent.scroll` merge your event into a default event, so check handler arguments with `expect.objectContaining`.

Detect: a direct event fired on a child of the element with the handler; an exact event object in `toHaveBeenCalledWith` after `fireEvent.press` or `fireEvent.scroll`.

## Async

### N1 · high · Await every RNTL 14 async API

Source: RNTL migration-v14 "Async APIs", "Removed APIs"; RNTL `src/events/fire-event.ts`. Level: derived.

In v14 each of these returns a promise and needs `await`: `render`, `rerender`, `unmount`, `renderHook` (and its `rerender` and `unmount`), every `fireEvent` call, `act` (even with a sync callback), `cleanup`, every `userEvent` method, `findBy*`, and `waitFor`.

`await fireEvent(...)` also waits for the promise the handler returns, and so do `fireEvent.press`, `.changeText`, `.scroll`, and `.layout`.

v14 removed these APIs:

| Removed | Use |
|---|---|
| `renderAsync`, `renderHookAsync`, `fireEventAsync` | `render`, `renderHook`, `fireEvent` |
| `update` | `rerender` |
| `getQueriesForElement` | `within` |
| `UNSAFE_root` | `container` or `root` |
| `UNSAFE_*ByType`, `UNSAFE_*ByProps` | a query from Q1 |
| the `concurrentRoot` and `createNodeMock` options | nothing |

Detect: an un-awaited `render`, `rerender`, `unmount`, `fireEvent`, `act`, `renderHook`, or `user.*`; any removed API. No Testing Library ESLint rule catches a missing `await` on `render` or `act`.

### W5 · native

```jsx
await waitFor(() => expect(screen.queryByText(/loading/i)).not.toBeOnTheScreen())
```

### N6 · medium · Advance Jest fake timers inside `await act(...)`

Source: RNTL "Understanding act"; RNTL async utilities; RNTL user-event `#setup`. Level: derived.

```jsx
await act(() => jest.advanceTimersByTime(1000))
expect(screen.getByRole('alert')).toHaveTextContent(/saved/i)
```

`waitFor` and `findBy*` advance Jest fake timers automatically, and userEvent's default setup handles them (I2).

Detect: `jest.advanceTimersByTime` or `jest.runAllTimers` outside `await act(...)`.

## Assertions

### E1 · native

The matchers load from any RNTL import, with no setup and no jest-dom:

- Presence and content: `toBeOnTheScreen`, `toHaveTextContent`, `toContainElement`, `toBeEmptyElement`, `toHaveAccessibleName`.
- Values: `toHaveDisplayValue` checks a TextInput's value; `toHaveAccessibilityValue`.
- State: `toBeEnabled`, `toBeDisabled`, `toBeSelected`, `toBeChecked`, `toBePartiallyChecked`, `toBeExpanded`, `toBeCollapsed`, `toBeBusy`, `toBeVisible`.
- Style and props: `toHaveStyle` flattens the style and checks only the keys you list. `toHaveProp` is the last resort.

Disabled state is not inherited, so assert `toBeDisabled` on the pressable element, not on its text. Report E1 findings under N5.

### N5 · high · Assert with RNTL matchers instead of reading `.props`

Source: RNTL-CM "Using the wrong assertion"; RNTL jest-matchers.

| Instead of | Use |
|---|---|
| `.props.accessibilityState.selected` | `toBeSelected()` |
| comparing `.props.style` | `toHaveStyle({ ... })` |
| `.props.value` | `toHaveDisplayValue(...)` |
| `.props.accessibilityLabel` | `toHaveAccessibleName(...)` |
| `toBeTruthy()` or `not.toBeNull()` on a query result | `toBeOnTheScreen()` |

Detect: a `.props.` read inside `expect`; a helper that reads `.props` and whose result the test asserts on, such as `expect(isDisabled(button)).toBe(true)`; `toBeTruthy()` or `toBeNull()` on a query result; `toHaveValue(`, which RNTL names `toHaveDisplayValue`.

### E2 · native

Correct: `expect(screen.getByRole('alert')).toBeOnTheScreen()` and `expect(screen.queryByRole('alert')).not.toBeOnTheScreen()`.

### E3 · native

Queries skip hidden elements by default (N8), so an absence assertion also passes while the element is still rendered but hidden.

Detect: a `query*` absence assertion on an element the component hides (N8) instead of removing it.

## act

### A1 · native

`renderHook` also runs inside `act`. Correct: `await render(<Example />)`, then `await user.press(button)`, with no `act` around either.

### A2 · native

Import `act` and `renderHook` from `@testing-library/react-native`, and await `act` even with a sync callback (N1).

```jsx
const { result } = await renderHook(() => useCounter())
await act(() => {
  result.current.increment()
})
expect(result.current.count).toBe(1)
```

Detect: `act` imported from `react` or `react-test-renderer`.

## Component markup

### M1 · native

Native components have no semantic elements, so roles and names come from props, as N4 describes. Report M1 findings under N4.

### N4 · medium · Give each interactive component a role and an accessible name

Source: RNTL-CM summary; RNTL queries ByRole; RNTL accessibility. Level: derived.

Set `role` and an accessible name (`aria-label` or text content) on each interactive component, and set `accessible` on a pressable `View`.

```jsx
<Pressable role="button" aria-label="Delete Alice" onPress={onDelete}>
  <TrashIcon />
</Pressable>
```

Detect: a `Pressable` or `Touchable*` with no `role`; an icon-only control with no `aria-label`; a test that falls back to `ByTestId` because the component has no role or name.

## Debugging

Source: RNTL screen, async, config; ETL `no-debugging-utils`.

- `screen.debug({ message, mapProps })` prints the whole tree. `screen.toJSON()` returns it.
- `waitFor(..., { onTimeout: (error) => { screen.debug(); return error } })` prints the tree when a wait times out. The return value is optional at runtime, but the TypeScript type is `(error: Error) => Error`, so in TypeScript return the error.
- `configure({ eventDiagnostics: true })` (RNTL 14.1) warns when an event reaches no handler because the element is disabled, not editable, blocked by `pointerEvents`, or has no handler.

## What RNTL tests do not run

Reference only, no severity. Source: RNTL advanced testing-env; RNTL faq; RNTL queries `ByTestId`.

RNTL "Tests don't execute native code". Test native features with E2E tests on a device, for example with Detox. `fireEvent` reaches handlers that userEvent does not (N7).

## Test template

```jsx
// If the project has test-utils, import render from there.
import { render, screen, userEvent } from '@testing-library/react-native'
import { SignupForm } from './SignupForm'

// E3: once this passes, break the signup in SignupForm, see the test fail, then restore it.
test('confirms the signup after the user submits an email', async () => {
  const user = userEvent.setup()
  await render(<SignupForm />)

  await user.type(screen.getByLabelText(/email/i), 'ada@example.com')
  await user.press(screen.getByRole('button', { name: /sign up/i }))

  expect(await screen.findByText(/check your inbox/i)).toBeOnTheScreen()
  expect(screen.queryByRole('button', { name: /sign up/i })).not.toBeOnTheScreen()
})
```
