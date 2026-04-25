---
title: "Pretty-Printing JSON in JavaScript: JSON.stringify, DevTools, and Node.js"
description: "Learn to pretty-print JSON in JavaScript using JSON.stringify's indent parameter, browser DevTools, Node.js, and the command line. Includes real code examples."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["javascript", "json", "json.stringify", "pretty print", "node.js"]
draft: false
---

Pretty-printing JSON in JavaScript takes one function call. But there are a handful of tricks that make the output cleaner, more portable, or easier to produce from different environments. This guide covers them all.

## `JSON.stringify` — the core API

`JSON.stringify(value, replacer, space)` has three parameters. Most developers only use the first one. The third — `space` — controls indentation.

```js
const data = { name: "Alice", age: 30, skills: ["JS", "Python"] };

// Compact (default)
JSON.stringify(data);
// '{"name":"Alice","age":30,"skills":["JS","Python"]}'

// Pretty-printed with 2-space indent
JSON.stringify(data, null, 2);
```

Output:

```json
{
  "name": "Alice",
  "age": 30,
  "skills": [
    "JS",
    "Python"
  ]
}
```

### Indent with tabs instead of spaces

```js
JSON.stringify(data, null, '\t');
```

### The `replacer` parameter

The second parameter is often set to `null`, but it's useful when you want to control which keys appear in the output:

```js
// Array form: only include listed keys
JSON.stringify(data, ['name', 'age'], 2);

// Function form: filter or transform values
JSON.stringify(data, (key, value) => {
  if (key === 'age') return undefined; // omit key
  return value;
}, 2);
```

### Serialising circular structures

`JSON.stringify` throws a `TypeError` on circular references. A simple workaround:

```js
function safeStringify(obj, indent = 2) {
  const seen = new WeakSet();
  return JSON.stringify(obj, (key, value) => {
    if (typeof value === 'object' && value !== null) {
      if (seen.has(value)) return '[Circular]';
      seen.add(value);
    }
    return value;
  }, indent);
}
```

### Custom `toJSON` methods

Any object with a `toJSON` method will use that method's return value during serialisation:

```js
class Product {
  constructor(name, price, internalCode) {
    this.name = name;
    this.price = price;
    this.internalCode = internalCode;
  }
  toJSON() {
    // Strip internalCode from API responses
    return { name: this.name, price: this.price };
  }
}

const p = new Product('Widget', 9.99, 'INTERNAL-123');
JSON.stringify(p, null, 2);
// { "name": "Widget", "price": 9.99 }
```

## Pretty-printing in the browser console

You don't need `JSON.stringify` to inspect objects in DevTools — the browser does it for you. But if you have a raw JSON string:

```js
// In the browser console
console.log(JSON.parse(rawJsonString));
// The browser renders the parsed object as an expandable tree
```

To copy formatted JSON to the clipboard from the console:

```js
copy(JSON.stringify(data, null, 2));
```

## Pretty-printing in Node.js

### From a script

```js
const fs = require('fs');

const raw = fs.readFileSync('input.json', 'utf8');
const data = JSON.parse(raw);
const pretty = JSON.stringify(data, null, 2);

fs.writeFileSync('output.json', pretty);
```

### From the command line with Node

```bash
node -e "const d = require('./input.json'); process.stdout.write(JSON.stringify(d, null, 2))"
```

### Using `--experimental-json-modules` (ESM)

```js
import data from './input.json' assert { type: 'json' };
console.log(JSON.stringify(data, null, 2));
```

## Pretty-printing a fetch response

A common pattern: fetch JSON from an API and log it cleanly:

```js
const res = await fetch('https://api.example.com/users/1');
const data = await res.json();
console.log(JSON.stringify(data, null, 2));
```

Or write the response to a file in Node.js:

```js
import { writeFileSync } from 'fs';

const res = await fetch('https://api.example.com/users/1');
const data = await res.json();
writeFileSync('user.json', JSON.stringify(data, null, 2));
```

## VS Code — format JSON in the editor

If you're editing a `.json` file, VS Code has built-in formatting via Prettier or its own JSON formatter:

- **Format document:** `Shift+Alt+F` (Windows/Linux) or `Shift+Option+F` (Mac)
- **Format on save:** Add to `settings.json`:

```json
{
  "[json]": {
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  }
}
```

## What `JSON.stringify` cannot handle

| Value | Behaviour |
|-------|-----------|
| `undefined` | Key silently omitted |
| `Function` | Key silently omitted |
| `Symbol` | Key silently omitted |
| `NaN` | Serialised as `null` |
| `Infinity` | Serialised as `null` |
| `Date` | Serialised as ISO 8601 string via `toJSON` |
| `BigInt` | `TypeError` — wrap in a replacer or use `.toString()` |

For `BigInt`:

```js
JSON.stringify({ n: 9007199254740993n }, (key, value) =>
  typeof value === 'bigint' ? value.toString() : value
, 2);
```

## Quick reference

```js
// Compact
JSON.stringify(obj)

// 2-space indent
JSON.stringify(obj, null, 2)

// 4-space indent
JSON.stringify(obj, null, 4)

// Tabs
JSON.stringify(obj, null, '\t')

// Pick specific keys
JSON.stringify(obj, ['id', 'name'], 2)

// Parse then pretty-print a string
JSON.stringify(JSON.parse(rawString), null, 2)
```

## References

- [MDN — JSON.stringify](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON/stringify)
- [MDN — JSON.parse](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON/parse)
- [ECMA-404 — The JSON Standard](https://www.ecma-international.org/publications-and-standards/standards/ecma-404/)
- [json.org](https://www.json.org/json-en.html)
