```text
In README.md replace the single exact string "npm instal" with "npm install". Change no other byte. Verify that the diff contains exactly that one replacement. Do not add a test file, run an install, or reformat the document.
```

Unchanged: the task fixes the method, scope, and judge. Its diff check already catches the main way this edit can go wrong. Because "npm instal" is a prefix of "npm install", a careless replace could produce "npm installl" or touch a second occurrence. Any extra rung, method, or field would either break "change no other byte" or repeat that check.
