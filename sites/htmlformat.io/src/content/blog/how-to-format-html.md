---
title: "How to Format HTML: Tools, Rules, and Editor Shortcuts"
description: "Format messy HTML with online tools, Prettier, VS Code, or CLI utilities. Covers indentation rules, attribute ordering, and formatting HTML templates."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["html", "formatting", "prettier", "vscode", "code style"]
draft: false
---

Formatted HTML is easier to read, review, and debug. Unformatted HTML — especially generated or minified — is nearly impossible to edit by hand. Here's how to format HTML in every common workflow.

## Online formatter

Paste minified or unindented HTML into [htmlformat.io](/) and click Format — no install needed.

## VS Code

VS Code includes an HTML formatter out of the box. Three ways to trigger it:

**Format document:** `Shift+Alt+F` (Windows/Linux) or `Shift+Option+F` (Mac)

**Format on save:** Add to `settings.json`:

```json
{
  "editor.formatOnSave": true,
  "[html]": {
    "editor.defaultFormatter": "vscode.html-language-features"
  }
}
```

**Command palette:** `Ctrl+Shift+P` → "Format Document"

### VS Code HTML formatting options

In `settings.json`:

```json
{
  "html.format.indentInnerHtml": true,
  "html.format.wrapLineLength": 120,
  "html.format.wrapAttributes": "auto",
  "html.format.endWithNewline": true,
  "html.format.preserveNewLines": true,
  "html.format.maxPreserveNewLines": 2
}
```

The built-in formatter handles basic cases well. For more control over attribute wrapping and template syntax, switch to Prettier.

## Prettier

[Prettier](https://prettier.io/) is the de-facto standard formatter for web projects. It formats HTML consistently with zero configuration:

```bash
npm install --save-dev prettier

# Format a file in place
npx prettier --write "src/**/*.html"

# Check formatting (for CI)
npx prettier --check "src/**/*.html"
```

### Prettier HTML configuration

Create `.prettierrc`:

```json
{
  "printWidth": 100,
  "tabWidth": 2,
  "useTabs": false,
  "htmlWhitespaceInsensitivity": "css",
  "bracketSameLine": false,
  "singleAttributePerLine": false
}
```

Key HTML-specific options:

- `printWidth` — maximum line length before wrapping attributes (default 80)
- `htmlWhitespaceInsensitivity` — `"css"` (default): respects CSS display context. `"strict"`: treats all whitespace as significant. `"ignore"`: treats all whitespace as insignificant.
- `singleAttributePerLine` — force each attribute onto its own line when wrapping (Prettier ≥ 2.6)

### Prettier VS Code integration

```bash
npm install --save-dev prettier
```

Install the Prettier VS Code extension, then set it as the default formatter:

```json
{
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.formatOnSave": true
}
```

## HTML Tidy

HTML Tidy is a command-line tool that formats and repairs HTML (closes unclosed tags, fixes nesting errors):

```bash
# Install
sudo apt install tidy           # Debian/Ubuntu
brew install tidy-html5          # macOS

# Format in place
tidy -i -m file.html

# Format with options
tidy --indent yes --wrap 120 --indent-spaces 2 -o output.html input.html
```

HTML Tidy also reports accessibility and standards issues, making it useful as a light linter as well as a formatter.

## Formatting rules to know

**Self-closing void elements:** In HTML5, void elements (`<br>`, `<img>`, `<input>`, `<hr>`, `<meta>`, `<link>`) don't have closing tags. Don't write `<br />` in HTML — that's XML/XHTML syntax.

```html
<!-- HTML5: correct -->
<img src="photo.jpg" alt="Mountain view">
<br>
<input type="text">

<!-- XHTML (not needed in HTML5) -->
<img src="photo.jpg" alt="Mountain view" />
```

**Boolean attributes:** Attributes like `disabled`, `required`, `checked`, `readonly` are boolean — their presence is what matters, not their value. Both are valid:

```html
<input required>
<input required="required">  <!-- also valid -->
<input required="">          <!-- also valid -->
```

Prettier normalizes these to the bare attribute form.

**Attribute order:** No enforced spec, but conventional order improves readability:

```html
<input
  class="form-input"
  id="email"
  type="email"
  name="email"
  placeholder="you@example.com"
  required
  aria-label="Email address"
>
```

Class and ID first, type and name second, content attributes, then states (required, disabled), then ARIA.

**Indentation depth:** Standard is 2 spaces. Deeply nested HTML becomes hard to read; if you're at 5+ levels of indentation, consider component extraction.

## Formatting HTML templates

Prettier supports major template formats with plugins:

```bash
# Jinja2 / Twig / Nunjucks
npm install --save-dev prettier-plugin-jinja-template

# Svelte
npm install --save-dev prettier-plugin-svelte

# Blade (Laravel)
npm install --save-dev prettier-plugin-blade

# Astro
npm install --save-dev prettier-plugin-astro
```

## Python: format HTML programmatically

```python
from bs4 import BeautifulSoup

def format_html(raw_html: str) -> str:
    soup = BeautifulSoup(raw_html, 'html.parser')
    return soup.prettify()

raw = '<div><p>Hello <strong>world</strong></p></div>'
print(format_html(raw))
```

Output:
```html
<div>
 <p>
  Hello
  <strong>
   world
  </strong>
 </p>
</div>
```

BeautifulSoup's `prettify()` uses 1-space indentation by default. For custom indentation:

```python
import re
formatted = soup.prettify()
# Replace 1-space indent with 2-space
formatted = re.sub(r'^(\s+)', lambda m: m.group(1).replace(' ', '  '), formatted, flags=re.MULTILINE)
```

## Quick format

Paste any HTML into [htmlformat.io](/) for instant formatting with configurable indentation.
