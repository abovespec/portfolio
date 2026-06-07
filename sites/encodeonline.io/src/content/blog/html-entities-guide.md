---
title: "HTML Entities: The Complete Reference for Special Characters"
description: "HTML entities convert special characters like <, >, &, and © to safe HTML representations. Includes the most common named entities, numeric references, and when to use them."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["html", "html entities", "web development", "encoding", "xss prevention"]
draft: false
---

HTML entities are special text sequences that represent characters with special meaning in HTML, or characters that can't be typed directly. They're essential for correctly rendering content and preventing cross-site scripting (XSS) vulnerabilities.

## Why HTML entities exist

HTML uses `<`, `>`, and `&` as part of its syntax. If you write literal `<b>` in text content, the browser parses it as an HTML tag. HTML entities let you include these characters as display text:

For more on this topic, see [*Base64 vs Hex Encoding: Which Should You Use?*](/blog/base64-vs-hex).

```html
<!-- This renders as a tag, not text: -->
<b>bold</b>

<!-- This renders as: <b>bold</b> -->
&lt;b&gt;bold&lt;/b&gt;
```

## The essential five

| Character | Entity | Numeric | Use |
|-----------|--------|---------|-----|
| `<` | `&lt;` | `&#60;` | Less-than / opening tag |
| `>` | `&gt;` | `&#62;` | Greater-than / closing tag |
| `&` | `&amp;` | `&#38;` | Ampersand (always escape in HTML) |
| `"` | `&quot;` | `&#34;` | Double quote in attributes |
| `'` | `&apos;` | `&#39;` | Single quote (HTML5; use `&#39;` for wider compat) |

The `&` character must be encoded whenever it appears in HTML content or attributes — even in harmless contexts like `&lang=en`. Use `&amp;lang=en`.

## Named entities reference

**Typography and punctuation:**

| Character | Entity | Decimal | Description |
|-----------|--------|---------|-------------|
| (non-breaking space) | `&nbsp;` | `&#160;` | Non-breaking space |
| — | `&mdash;` | `&#8212;` | Em dash |
| – | `&ndash;` | `&#8211;` | En dash |
| … | `&hellip;` | `&#8230;` | Horizontal ellipsis |
| " | `&ldquo;` | `&#8220;` | Left double quotation mark |
| " | `&rdquo;` | `&#8221;` | Right double quotation mark |
| ' | `&lsquo;` | `&#8216;` | Left single quotation mark |
| ' | `&rsquo;` | `&#8217;` | Right single quotation mark |
| ‒ | `&ndash;` | `&#8211;` | En dash |
| × | `&times;` | `&#215;` | Multiplication sign |
| ÷ | `&divide;` | `&#247;` | Division sign |
| ° | `&deg;` | `&#176;` | Degree sign |

**Symbols:**

| Character | Entity | Decimal | Description |
|-----------|--------|---------|-------------|
| © | `&copy;` | `&#169;` | Copyright |
| ® | `&reg;` | `&#174;` | Registered trademark |
| ™ | `&trade;` | `&#8482;` | Trademark |
| € | `&euro;` | `&#8364;` | Euro sign |
| £ | `&pound;` | `&#163;` | Pound sterling |
| ¥ | `&yen;` | `&#165;` | Yen sign |
| ¢ | `&cent;` | `&#162;` | Cent sign |
| § | `&sect;` | `&#167;` | Section sign |
| ¶ | `&para;` | `&#182;` | Paragraph sign |
| † | `&dagger;` | `&#8224;` | Dagger |
| ‡ | `&Dagger;` | `&#8225;` | Double dagger |
| ♠ | `&spades;` | `&#9824;` | Spade suit |
| ♣ | `&clubs;` | `&#9827;` | Club suit |
| ♥ | `&hearts;` | `&#9829;` | Heart suit |
| ♦ | `&diams;` | `&#9830;` | Diamond suit |

**Mathematical:**

| Character | Entity | Decimal | Description |
|-----------|--------|---------|-------------|
| ≠ | `&ne;` | `&#8800;` | Not equal to |
| ≤ | `&le;` | `&#8804;` | Less than or equal |
| ≥ | `&ge;` | `&#8805;` | Greater than or equal |
| ± | `&plusmn;` | `&#177;` | Plus-minus |
| ∞ | `&infin;` | `&#8734;` | Infinity |
| √ | `&radic;` | `&#8730;` | Square root |
| ∑ | `&sum;` | `&#8721;` | Summation |
| ∫ | `&int;` | `&#8747;` | Integral |
| π | `&pi;` | `&#960;` | Pi |
| α | `&alpha;` | `&#945;` | Alpha |
| β | `&beta;` | `&#946;` | Beta |

## Named vs numeric entities

Both forms are equivalent and browser support is identical for common characters:

```html
&lt;     ← named entity (easier to read)
&#60;    ← decimal numeric reference
&#x3C;   ← hexadecimal numeric reference
```

Named entities work only when the HTML document has a character set that defines them. Numeric entities always work. For the basic five (`&lt;`, `&gt;`, `&amp;`, `&quot;`, `&apos;`), always use the named form for readability.

For characters outside ASCII, you don't *need* entities if your HTML file is UTF-8 encoded and declares `<meta charset="UTF-8">`. Writing `© 2026` directly is equivalent to `&copy; 2026`. Use entities for characters that are hard to type or copy-paste.

## XSS prevention: always escape user input

HTML entity encoding is a primary defense against **reflected XSS** attacks. If you render user input in HTML without escaping it, an attacker can inject script tags:

For more on this topic, see [*Base64 Encoding Explained: How It Works and When to Use It*](/blog/base64-encoding-explained).

```html
<!-- User input: <script>alert(1)</script> -->

<!-- Dangerous — renders the script: -->
<p>Hello, <script>alert(1)</script></p>

<!-- Safe — renders as text: -->
<p>Hello, &lt;script&gt;alert(1)&lt;/script&gt;</p>
```

**Context matters:**
- In HTML content: escape `<`, `>`, `&`
- In HTML attributes: additionally escape `"` (or `'` for single-quoted attributes)
- In JavaScript: use JSON encoding or template systems, not HTML entity encoding
- In URLs: use percent-encoding, not HTML entities

For more on this topic, see [*URL Encoding (Percent-Encoding): The Complete Guide*](/blog/url-encoding-guide).

Modern frameworks (React, Vue, Angular) escape HTML by default when rendering variables. Don't use raw HTML injection (e.g., `innerHTML`, `dangerouslySetInnerHTML`) unless you've explicitly sanitized the content.

## Encoding HTML entities in code

**JavaScript:**

```js
function escapeHtml(text) {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

escapeHtml('<script>alert("xss")</script>');
// "&lt;script&gt;alert(&quot;xss&quot;)&lt;/script&gt;"
```

Or use a library like [`he`](https://github.com/mathiasbynens/he):

```js
import he from 'he';
he.encode('<div class="greeting">Hello</div>');
// "&lt;div class=&quot;greeting&quot;&gt;Hello&lt;/div&gt;"
```

**Python:**

```python
import html

html.escape('<script>alert("xss")</script>')
# '&lt;script&gt;alert(&quot;xss&quot;)&lt;/script&gt;'

html.unescape('&lt;b&gt;bold&lt;/b&gt;')
# '<b>bold</b>'
```

**Go:**

```go
import "html"

html.EscapeString(`<script>alert("xss")</script>`)
// "&lt;script&gt;alert(&#34;xss&#34;)&lt;/script&gt;"

html.UnescapeString("&lt;b&gt;bold&lt;/b&gt;")
// "<b>bold</b>"
```

## Online HTML entity tool

For converting text to HTML entities or decoding entity-encoded strings, use [encodeonline.io](/) — handles named entities, numeric references, and decode-to-text in one step.
