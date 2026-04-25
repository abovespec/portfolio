---
title: "What Is JSON? A Plain-English Introduction"
description: "JSON is the universal language of web APIs. Learn what it is, how it works, and why every developer needs to understand it."
publishDate: 2026-04-01
author: "Editorial Team"
tags: ["json", "beginner", "web-development"]
---

JSON (JavaScript Object Notation) is a lightweight text format for storing and exchanging structured data. Despite the "JavaScript" in its name, JSON is completely language-independent — you will find it in Python, Go, Rust, Java, Ruby, and virtually every other language ecosystem.

## The basic structure

A JSON document is built from two structures:

- **Objects** — unordered collections of key/value pairs, surrounded by curly braces `{}`
- **Arrays** — ordered lists of values, surrounded by square brackets `[]`

Values can be strings (in double quotes), numbers, booleans (`true`/`false`), `null`, another object, or another array. That's the entire type system.

```json
{
  "name": "Alice",
  "age": 30,
  "active": true,
  "scores": [95, 87, 92],
  "address": {
    "city": "Portland",
    "country": "US"
  }
}
```

## Why JSON won

Before JSON, XML was the dominant data exchange format. XML is verbose: every value needs an opening tag and a closing tag, attributes complicate nesting, and parsers are heavy. JSON carries the same information in roughly half the bytes and maps directly to the data structures (objects and arrays) that every programming language already has.

Douglas Crockford popularized JSON in the early 2000s. By 2010 it had become the default format for web APIs, and by 2015 it had largely replaced XML outside of enterprise and document-centric contexts.

## JSON vs JavaScript objects

JSON looks like a JavaScript object literal, but there are important differences:

| Feature | JSON | JS Object Literal |
|---|---|---|
| Keys must be quoted | Yes (double quotes only) | No |
| Trailing commas | Forbidden | Allowed |
| Comments | Forbidden | Allowed |
| `undefined` values | Forbidden | Allowed |
| `NaN` / `Infinity` | Forbidden | Allowed |
| Functions as values | Forbidden | Allowed |

When working with JSON in JavaScript, use `JSON.parse()` to convert a JSON string to a JS object, and `JSON.stringify()` to convert an object back to a JSON string.

## Common use cases

- **REST APIs** — nearly every web API sends and receives JSON payloads
- **Configuration files** — `package.json`, `tsconfig.json`, `composer.json`
- **Log aggregation** — structured logs are frequently stored as one JSON object per line (NDJSON)
- **Database documents** — MongoDB, CouchDB, and PostgreSQL's `jsonb` column type all store documents as JSON
- **Inter-process communication** — microservices, message queues, and WebSocket messages all commonly use JSON

## Validating JSON

One pitfall is that JSON has zero tolerance for syntax errors. A single missing comma, an extra trailing comma, or an unescaped special character will cause a parser to reject the entire document.

Use the [JSON Formatter & Validator](/) on this site to quickly check whether your JSON is valid and to see exactly where a problem is if it isn't.
