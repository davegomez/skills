---
name: react-testing-library
description: Write and review React component tests with Testing Library (@testing-library/react, user-event, jest-dom). Use when writing, reviewing, or refactoring React component tests, or adding test coverage to React components.
---

# React Testing Library

> The more your tests resemble the way your software is used, the more confidence they can give you.

A test gains _confidence_ when it finds elements and interacts with them the way a user would: by role, label, and text, through user-event. It loses _confidence_ when it reaches into _implementation details_ the user never sees, such as class names, DOM structure, component state, and test IDs. Every rule lives in [references/rules.md](references/rules.md). Read that file before you write or review anything.

## 1. Read the project setup

Both branches start here. Read `package.json`, the test config (`jest.config.*`, `vitest.config.*`, or the `test` block in `vite.config.*`), and the setup file the config names. Record:

- The runner (Jest or Vitest). For Vitest, also record whether `globals: true` is set.
- The versions of `@testing-library/react`, `@testing-library/dom`, `@testing-library/user-event`, and `@testing-library/jest-dom`.
- Whether `eslint-plugin-testing-library` and `eslint-plugin-jest-dom` are configured, and which of `prefer-explicit-assert` / `prefer-implicit-assert` is on.
- The project's custom render (a test-utils module that wraps `render`), if there is one.
- The test command and the lint command from `scripts`.

This step is done when every item has a value. If the setup is missing or broken, fix it with rules S1 to S4 before going on. Ask the user before you install any package.

## 2a. Write tests

1. Read the component. List what a user can observe: what renders, what each interaction changes, and what loads asynchronously.
2. Write one test for each observable behaviour. Start from the Test template in rules.md, use the project's custom render if it has one, and follow each rule's correct example.
3. Run the project's test command on the file. If the plugins are configured, also run ESLint on it.

Done when all of these hold:

- The file runs with the project's test command and every test passes.
- ESLint passes on the file, if the plugins are configured.
- Every absence assertion has a matching presence check (E3).

## 2b. Review tests

1. Read the test file and the component it tests.
2. Go through rules.md one group at a time and check every rule's `Detect:` pattern against the file. Report E4 only when the file conflicts with the project's ESLint config.
3. Write each finding on one line in this form: `high · src/Login.test.tsx:42 · Q2 · replace container.querySelector('.submit') with screen.getByRole('button', { name: /sign in/i })`.

Done when every rule in rules.md has been checked against the file, and the findings are ordered high to low. Each finding gives the severity, `file:line`, the rule ID, and the fix.
