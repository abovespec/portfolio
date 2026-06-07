---
title: "8 Common JSON Errors and How to Fix Them"
description: "Trailing commas, single quotes, unquoted keys — here are the JSON mistakes developers make most often and exactly how to correct them."
publishDate: 2026-04-08
author: "Editorial Team"
tags: ["json", "debugging", "syntax"]
---

JSON parsing is unforgiving. One character out of place causes the entire document to be rejected with a cryptic error message. Here are the eight mistakes that cause the most frustration, along with clear examples of the broken syntax and the fix.

## 1. Trailing comma

The JSON spec does not allow a comma after the last element of an object or array.

For more on this topic, see [*How to Validate JSON: Common Errors and How to Fix Them*](/blog/how-to-validate-json).

```json
// ❌ Invalid
{
  "a": 1,
  "b": 2,
}

// ✅ Valid
{
  "a": 1,
  "b": 2
}
```

Trailing commas are legal in modern JavaScript object literals, which is why this trips up developers who are used to copying JS config snippets directly.

## 2. Single-quoted strings

JSON strings must use double quotes. Single quotes are not valid.

For more on this topic, see [*What Is JSON? A Plain-English Introduction*](/blog/what-is-json).

```json
// ❌ Invalid
{ 'name': 'Alice' }

// ✅ Valid
{ "name": "Alice" }
```

## 3. Unquoted keys

Every key in a JSON object must be a quoted string.

```json
// ❌ Invalid
{ name: "Alice" }

// ✅ Valid
{ "name": "Alice" }
```

This is another place where JavaScript habits cause trouble. In a JS object literal, keys do not need quotes (unless they contain special characters). In JSON, they always do.

## 4. Comments

Standard JSON has no comment syntax. Neither `//` nor `/* */` are valid.

```json
// ❌ Invalid
{
  // user identifier
  "id": 42
}
```

If you need comments in a configuration file, use JSONC (JSON with Comments, supported by VS Code and TypeScript's `tsconfig.json`) or JSON5, which also allows trailing commas and single-quoted strings.

## 5. `undefined`, `NaN`, and `Infinity`

JSON only has `null`. JavaScript's `undefined`, `NaN`, and `Infinity` are not valid JSON values.

```json
// ❌ Invalid
{ "value": undefined }
{ "ratio": NaN }
{ "limit": Infinity }

// ✅ Valid alternatives
{ "value": null }
{ "ratio": null }
{ "limit": null }
```

When serializing with `JSON.stringify()` in JavaScript, `undefined` values are silently dropped from objects and converted to `null` in arrays — which can produce surprising output.

## 6. Unescaped special characters in strings

Inside a JSON string, certain characters must be escaped with a backslash:

| Character | Escaped form |
|---|---|
| `"` | `\"` |
| `\` | `\\` |
| Newline | `\n` |
| Tab | `\t` |
| Carriage return | `\r` |
| Non-ASCII control characters | `\uXXXX` |

A literal unescaped newline inside a string is invalid JSON.

```json
// ❌ Invalid
{ "message": "line one
line two" }

// ✅ Valid
{ "message": "line one\nline two" }
```

## 7. Wrong number format

JSON numbers cannot have a leading plus sign, and they cannot be written in hexadecimal or octal notation. Very large or very small numbers must use standard decimal notation or scientific notation (`1e10`).

```json
// ❌ Invalid
{ "count": +5 }
{ "hex": 0xFF }

// ✅ Valid
{ "count": 5 }
{ "hex": 255 }
```

## 8. Bare values at the top level (sometimes)

A valid JSON document can be a bare value — a string, number, boolean, or null — not just an object or array. However, some parsers and APIs expect only objects or arrays at the top level. If you paste a bare string (`"hello"`) into a strict parser, you may see it rejected even though RFC 8259 allows it.

---

## Fixing errors quickly

The fastest way to identify and fix JSON errors is to paste your text into the [JSON Formatter & Validator](/) on this site. It highlights the exact position of the first error so you can fix it rather than hunting through the raw text.


For more on this topic, see [*Unexpected Token in JSON: What It Means and How to Fix It*](/blog/unexpected-token-json-error).