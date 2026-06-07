---
title: "HTML Beautifier: Making Minified or Messy HTML Readable"
description: "How to beautify HTML — format minified output, fix broken indentation, and make auto-generated markup readable. Tools for browser, CLI, and programmatic use."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["html", "beautifier", "formatting", "minified html", "code tools"]
draft: false
---

HTML beautifiers take minified, generated, or poorly indented HTML and produce clean, readable output. They're the inverse of minifiers — add whitespace back in, not take it out.

## When you need a beautifier

- Debugging minified HTML from a production build
- Reading auto-generated HTML from a CMS or tool
- Reviewing HTML in an email template (usually written as one long line)
- Copy-pasted code without indentation
- Inspecting HTML from a web scraper or API response

For more on this topic, see [*HTML Indentation Best Practices*](/blog/html-indentation-best-practices).

## Online beautifier

The fastest way: paste into [htmlformat.io](/) and click Format. Configurable indentation (2 or 4 spaces, tabs), no installation needed.

## js-beautify (CLI and API)

[js-beautify](https://github.com/beautifier/js-beautifier) handles HTML, CSS, and JS from the same tool:

```bash
npm install --save-dev js-beautify

# Format a file
npx html-beautify -f input.html -o output.html

# Common options
npx html-beautify \
  --indent-size 2 \
  --indent-char " " \
  --max-preserve-newlines 2 \
  --preserve-newlines \
  --wrap-line-length 0 \
  -f input.html
```

Key options:
- `--indent-size` — number of spaces (default 4)
- `--wrap-line-length` — max line length before wrapping attributes (0 = no wrapping)
- `--preserve-newlines` — keep blank lines from source
- `--wrap-attributes` — `"auto"`, `"force"`, `"force-aligned"`, `"force-expand-multiline"`

**Programmatic API:**

```js
const beautify = require('js-beautify').html;

const ugly = '<html><head><title>Page</title></head><body><p>Hello!</p></body></html>';
const pretty = beautify(ugly, { indent_size: 2, wrap_line_length: 100 });
console.log(pretty);
```

Output:
```html
<html>

<head>
  <title>Page</title>
</head>

<body>
  <p>Hello!</p>
</body>

</html>
```

## Prettier

Prettier formats and beautifies in one pass:

```bash
npx prettier --write "src/**/*.html"
```

Prettier produces the most opinionated output — not configurable like js-beautify, but excellent for team consistency. See [Prettier HTML configuration](/blog/prettier-html-formatting/) for setup details.

## Python: BeautifulSoup

```python
from bs4 import BeautifulSoup

def beautify_html(raw: str, indent: int = 2) -> str:
    soup = BeautifulSoup(raw, 'html.parser')
    return soup.prettify(indent_width=indent)

minified = '<div class="card"><h2>Title</h2><p>Body text here.</p></div>'
print(beautify_html(minified, indent=2))
```

Output:
```html
<div class="card">
  <h2>
   Title
  </h2>
  <p>
   Body text here.
  </p>
</div>
```

Note: BeautifulSoup's `prettify()` places text content on separate lines from tags. For HTML output where text should stay on the same line as its tag, post-process the output or use `lxml`'s `tostring` with `pretty_print=True`.

**With lxml:**

```python
from lxml import etree, html as lxmlhtml

def beautify_with_lxml(raw: str) -> str:
    tree = lxmlhtml.fromstring(raw)
    return etree.tostring(tree, pretty_print=True, encoding='unicode')

print(beautify_with_lxml('<div><p>Hello</p></div>'))
# <div><p>Hello</p></div>  (lxml preserves inline structure)
```

## Node.js: parse5 + serialize

```bash
npm install parse5
```

```js
const parse5 = require('parse5');
const { serialize } = require('parse5');

// parse5 doesn't add indentation natively
// use with js-beautify for formatted output
const beautify = require('js-beautify').html;

const fragment = parse5.parseFragment('<div><p>Hello</p></div>');
const serialized = serialize(fragment);
const formatted = beautify(serialized, { indent_size: 2 });
```

## DevTools "Copy outerHTML" trick

When debugging a page:

1. Right-click any element → Inspect
2. Right-click the element node in the Elements panel → Copy → Copy outerHTML
3. Paste into [htmlformat.io](/) for formatted, readable markup

This is faster than trying to read the Elements panel directly for complex nested structures.

## Beautifying HTML email

HTML emails are typically written as one long line for maximum email client compatibility. To read and edit them:

1. Copy the HTML source
2. Paste into [htmlformat.io](/)
3. Format and edit
4. Re-minify before sending (some email clients behave better with compact HTML)

Email HTML uses deprecated layout tables and inline styles — a beautifier makes these manageable to read even if the structure isn't pretty.

## Format HTML online

[htmlformat.io](/) — paste, format, copy. Works for any HTML: web pages, emails, templates, API responses.


For more on this topic, see [*HTML Minification: How It Works and When It's Worth It*](/blog/html-minification).