---
title: "Unexpected Token in JSON: What It Means and How to Fix It"
description: "Decode the \"Unexpected token\" JSON parse error. Learn the 8 most common causes and exactly how to fix each one."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["json errors", "debugging", "unexpected token", "json parse", "json syntax"]
draft: false
---

You paste some JSON into your app, hit parse, and get back:

```
SyntaxError: Unexpected token < in JSON at position 0
```

or

```
JSON.parse: unexpected character at line 1 column 1 of the JSON data
```

These messages are frustrating because they tell you *where* the parser gave up, not *why* the JSON is invalid. This guide covers the eight most common root causes and how to fix each one.

## Why JSON parsing is strict

JSON is defined by [ECMA-404](https://www.ecma-international.org/publications-and-standards/standards/ecma-404/) and [RFC 8259](https://www.rfc-editor.org/rfc/rfc8259). The spec is intentionally minimal: no comments, no trailing commas, no single-quoted strings, no undefined values. Any character the parser doesn't expect at a given position throws an "unexpected token" error.

## 8 common causes — and their fixes

### 1. The response is HTML, not JSON

**Symptom:** `Unexpected token <` at position 0 — an `<` is the first character of an HTML tag.

**Cause:** Your server returned an HTML error page (404, 500, a login redirect) instead of JSON.

**Fix:** Check the response status and Content-Type header before parsing:

```js
const res = await fetch('/api/data');
if (!res.ok) {
  throw new Error(`HTTP ${res.status}: ${await res.text()}`);
}
const data = await res.json();
```

Always verify the actual server response in your browser's Network tab when debugging.

### 2. Trailing comma

**Symptom:** Parser error at the last element of an object or array.

**Cause:** JSON does not allow trailing commas. This is valid JavaScript but not valid JSON:

```json
{
  "name": "Alice",
  "age": 30,
}
```

**Fix:** Remove the comma after the last item:

```json
{
  "name": "Alice",
  "age": 30
}
```

If you're generating JSON programmatically, use your language's JSON serialiser (`json.dumps` in Python, `JSON.stringify` in JavaScript) instead of building strings manually.

### 3. Single-quoted strings

**Cause:** JSON requires double quotes. Single quotes are not valid.

```json
{ 'name': 'Alice' }
```

**Fix:**

```json
{ "name": "Alice" }
```

### 4. Unescaped special characters inside strings

**Cause:** Certain characters must be escaped inside JSON strings: `"`, `\`, and control characters (tabs, newlines).

```json
{ "path": "C:\Users\Alice\Documents" }
```

The `\U`, `\A`, `\D` sequences are not valid JSON escape sequences, so the parser chokes.

**Fix:** Escape every backslash:

```json
{ "path": "C:\\Users\\Alice\\Documents" }
```

Other escapes to know:

| Character | JSON escape |
|-----------|-------------|
| Double quote | `\"` |
| Backslash | `\\` |
| Newline | `\n` |
| Tab | `\t` |
| Carriage return | `\r` |
| Unicode | `\uXXXX` |

### 5. Comments in JSON

**Cause:** JSON has no comment syntax. Neither `//` nor `/* */` are allowed.

```json
{
  // user config
  "theme": "dark"
}
```

**Fix:** Remove the comment. If you need annotated config files, use [JSON5](https://json5.org/) or YAML instead, and convert to plain JSON before passing to APIs.

### 6. `undefined` values

**Cause:** `undefined` is not a JSON value type. JSON only supports `null`, booleans, numbers, strings, arrays, and objects.

```js
const data = { name: "Alice", age: undefined };
JSON.stringify(data); // {"name":"Alice"}  — age is silently dropped
```

If you receive a string `"undefined"` and try to parse it:

```js
JSON.parse("undefined"); // SyntaxError: Unexpected token u
```

**Fix:** Replace `undefined` with `null` before serialising, or filter the key out entirely.

### 7. Bare keys (no quotes around property names)

**Cause:** JavaScript object literal syntax allows unquoted keys; JSON does not.

```json
{ name: "Alice" }
```

**Fix:**

```json
{ "name": "Alice" }
```

### 8. BOM or invisible leading characters

**Cause:** Some editors prepend a UTF-8 Byte Order Mark (`﻿`) to files. The JSON parser sees an unexpected character before the `{` or `[`.

**Fix:** Strip the BOM when reading the file:

```python
with open('data.json', encoding='utf-8-sig') as f:
    data = json.load(f)
```

In Node.js:

```js
const raw = fs.readFileSync('data.json', 'utf8').replace(/^﻿/, '');
const data = JSON.parse(raw);
```

## Quick debugging workflow

1. **Copy the raw string** you're trying to parse and paste it into our [JSON formatter and validator](/) above.
2. Look at the error position — "position 0" almost always means HTML response or BOM; a mid-document position points to trailing commas or bad escapes.
3. Validate the Content-Type header. `application/json` means the server intended to send JSON; `text/html` means it didn't.
4. If the JSON was hand-written, run it through the validator to find the exact offending line.

## Useful references

- [ECMA-404 — The JSON Data Interchange Standard](https://www.ecma-international.org/publications-and-standards/standards/ecma-404/)
- [RFC 8259 — The JavaScript Object Notation (JSON) Data Interchange Format](https://www.rfc-editor.org/rfc/rfc8259)
- [MDN — JSON.parse](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON/parse)
- [json.org — JSON grammar](https://www.json.org/json-en.html)
