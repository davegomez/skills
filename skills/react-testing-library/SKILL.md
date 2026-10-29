---
name: react-testing-library
description: Write and review React and React Native component tests with Testing Library (@testing-library/react, @testing-library/react-native, user-event, jest-dom). Use when writing, reviewing, or refactoring component tests, or adding test coverage to React or React Native components.
---

# React Testing Library

> The more your tests resemble the way your software is used, the more confidence they can give you.

A test gains _confidence_ when it finds elements and interacts with them the way a user would: by role, label, and text, through user-event. It loses _confidence_ when it reaches into _implementation details_ the user never sees, such as class names, element structure, props, component state, and test IDs. The shared rules live in [references/rules.md](references/rules.md), and each platform's parts in [references/web.md](references/web.md) or [references/native.md](references/native.md).

## 1. Read the project setup

Both branches start here.

1. Pick the platform. The test file's import decides it: `@testing-library/react` is web, `@testing-library/react-native` is native. For a new test file, read the `package.json` nearest to the file, because a monorepo can hold both platforms.
2. Read rules.md, then web.md for web or native.md for native. A task that touches both platforms reads both platform files.
3. Read the `package.json` nearest to the test file, the test config (`jest.config.*`, the `jest` key in `package.json`, `vitest.config.*`, or the `test` block in `vite.config.*`), and the setup file the config names. Record installed versions from the lockfile or `node_modules`, and the `package.json` range only when nothing is installed. In a workspace, also check the root lockfile and the root `node_modules`, because packages can be hoisted. Read the Node version from `engines`, `.nvmrc`, or `.node-version`. Record:
   - Web: the runner (Jest or Vitest), and for Vitest whether `globals: true` is set; the versions of `react`, `@testing-library/react`, `@testing-library/dom`, `@testing-library/user-event`, and `@testing-library/jest-dom`; the Node version.
   - Native: the versions of `@testing-library/react-native`, `test-renderer`, and `react`; the Node version; the Jest `preset`. With a Jest `projects` config, record the preset of the project that runs the test file.
   - The linter. With ESLint, record whether `eslint-plugin-testing-library` (and on the web `eslint-plugin-jest-dom`) is configured, and which of `prefer-explicit-assert` / `prefer-implicit-assert` is on. With another linter, such as Biome, record it; S1 and E4 then do not apply.
   - The project's custom render (a test-utils module that wraps `render`), if there is one.
   - The test command and the lint command from `scripts`.

This step is done when every item for the platform has a value; "does not apply" counts as a value. If the setup is missing or broken:

- Writing: fix it with the Setup rules in rules.md and the platform file before going on. Ask the user before you install any package.
- Reviewing: report each setup problem as a finding that cites the config file or `package.json`.

## 2a. Write tests

1. Read the component. List what a user can observe: what renders, what each interaction changes, and what loads asynchronously.
2. Write one test for each observable behaviour. Start from the Test template in the platform file, use the project's custom render if it has one, and follow each rule's correct example.
3. Run the project's test command on the new test file only, without coverage flags, because a coverage threshold fails a single-file run. If the project lints with ESLint, also run ESLint on it.

Done when all of these hold:

- The file passes the project's test command.
- ESLint passes on the file, if the project lints with ESLint.
- Each new test failed once when you broke the behaviour it covers, and the source is restored (E3).

## 2b. Review tests

1. Read the test file, the component, and the child components and test utilities you need to know what renders. On native, find which platform file the test project resolves (for example `.ios.tsx` against `.android.tsx` under a Jest `projects` config), so that a finding about an element that renders only on another platform is correct. Stop there.
2. Go through rules.md and the platform file one group at a time, and check every `Detect:` pattern against every file read in step 2b.1 and the setup files from step 1. A rule that sends its findings to another rule (on native, E1 to N5 and M1 to N4) counts as checked through that rule.
3. Write 1 finding for each rule-and-fix pair, stated plainly, on one line in this form: `high · src/Login.test.tsx:42 · Q2 · replace container.querySelector('.submit') with screen.getByRole('button', { name: /sign in/i }) · also at 57, 81`. When 1 fix satisfies 2 rules, cite the first rule and name the second in the fix text. Cite the file the fix goes in: the test file, a component (M1 and N4 fixes go there), a test double, a test utility, or a config file. Paths are relative to the nearest `package.json`.
4. End the report with 1 line that lists the rule IDs checked with no finding, including those that do not apply, such as `clean: S3 S4 Q4 Q5 W1–W5 A1 A2`. A rule that sends its findings to another rule does not go on this line.

Done when every rule in rules.md and the platform file appears in a finding, on the `clean:` line, or as sent to another rule, and the findings are ordered high to low, then by file (alphabetically) and line. Each finding gives the severity, `file:line`, the rule ID, and the fix.
