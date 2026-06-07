---
title: "Prettier HTML Formatting: Configuration and Common Issues"
description: "Configure Prettier for HTML files: print width, attribute wrapping, whitespace sensitivity, and integration with VS Code, ESLint, and pre-commit hooks."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["prettier", "html", "formatting", "vscode", "code style"]
draft: false
---

Prettier formats HTML files consistently, but its HTML handling has some quirks — particularly around whitespace and attribute wrapping — that are worth understanding before you commit to it.

## Basic setup

```bash
npm install --save-dev prettier

# Format a file
npx prettier --write "src/**/*.html"

# Check without modifying (for CI)
npx prettier --check "src/**/*.html"
```

## Configuration options for HTML

Create `.prettierrc` in your project root:

```json
{
  "printWidth": 100,
  "tabWidth": 2,
  "useTabs": false,
  "htmlWhitespaceInsensitivity": "css",
  "bracketSameLine": false,
  "singleAttributePerLine": false,
  "endOfLine": "lf"
}
```

### `printWidth`

Lines longer than `printWidth` (default: 80) trigger attribute wrapping. For HTML with long attribute lists, 100–120 is often more practical:

For more on this topic, see [*HTML Beautifier: Making Minified or Messy HTML Readable*](/blog/html-beautifier-guide).

```html
<!-- printWidth: 80 — wraps attributes -->
<input
  class="form-control"
  type="email"
  name="email"
  placeholder="you@example.com"
>

<!-- printWidth: 200 — keeps on one line if it fits -->
<input class="form-control" type="email" name="email" placeholder="you@example.com">
```

### `htmlWhitespaceInsensitivity`

This setting controls how Prettier handles whitespace in HTML:

For more on this topic, see [*How to Validate HTML: W3C Validator, HTMLHint, and CI Integration*](/blog/validate-html).

- `"css"` (default): respects CSS display type. Block elements are whitespace-insensitive; inline elements are sensitive.
- `"strict"`: all whitespace is significant — Prettier won't remove any spaces.
- `"ignore"`: all whitespace is insignificant — Prettier may remove spaces between inline elements.

The `"css"` default is correct for most projects. Use `"strict"` if you have unusual whitespace requirements.

### `bracketSameLine`

Controls whether the `>` closing a tag's opening bracket stays on the last attribute line:

```html
<!-- bracketSameLine: false (default) -->
<input
  class="form-control"
  type="email"
>

<!-- bracketSameLine: true -->
<input
  class="form-control"
  type="email">
```

### `singleAttributePerLine`

Force each attribute onto its own line when wrapping (Prettier ≥ 2.6):

```json
{ "singleAttributePerLine": true }
```

```html
<!-- Without singleAttributePerLine -->
<input class="form-control" type="email"
  name="email" placeholder="you@example.com">

<!-- With singleAttributePerLine -->
<input
  class="form-control"
  type="email"
  name="email"
  placeholder="you@example.com"
>
```

## VS Code integration

1. Install the Prettier extension (id: `esbenp.prettier-vscode`)
2. Add to your `settings.json`:

```json
{
  "[html]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.formatOnSave": true
  }
}
```

If you have multiple formatters installed (e.g., the built-in VS Code HTML formatter), make Prettier explicit for HTML files to avoid conflicts.

For more on this topic, see [*How to Format HTML: Tools, Rules, and Editor Shortcuts*](/blog/how-to-format-html).

## Ignoring specific HTML blocks

To skip formatting for a section:

```html
<!-- prettier-ignore -->
<table class="complex-layout">
  <tr><td>This won't be reformatted</td></tr>
</table>
```

Or ignore entire files by listing them in `.prettierignore`:

```
# .prettierignore
dist/
*.min.html
vendor/
```

## Pre-commit hook

Run Prettier on staged HTML files before every commit:

```bash
npm install --save-dev husky lint-staged

# package.json
{
  "lint-staged": {
    "*.html": "prettier --write"
  }
}
```

```bash
npx husky init
echo "npx lint-staged" > .husky/pre-commit
```

## Common Prettier HTML issues

**Prettier reformats template syntax:** Prettier doesn't understand Jinja2, ERB, or Blade syntax by default. Install the appropriate plugin:

```bash
npm install --save-dev prettier-plugin-jinja-template
```

```json
{
  "plugins": ["prettier-plugin-jinja-template"],
  "overrides": [
    {
      "files": ["*.html"],
      "options": { "parser": "jinja-template" }
    }
  ]
}
```

**Attribute wrapping differs from team expectation:** Tune `printWidth` and `singleAttributePerLine` until the output matches your team's style. Once set, Prettier is consistent — the configuration is the contract.

**Inline elements get unexpected line breaks:** This is the whitespace sensitivity issue. If Prettier is adding or removing spaces between inline elements, try `"htmlWhitespaceInsensitivity": "strict"` to see if it resolves the specific case, then tune from there.

## Format HTML online

For one-off formatting without any setup, paste HTML into [htmlformat.io](/) — configurable indentation, instant output.
