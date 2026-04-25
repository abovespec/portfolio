---
title: "camelCase to snake_case in JavaScript: Three Clean Solutions"
description: "Convert camelCase identifiers to snake_case in JavaScript using regex, reduce, or a utility library. Includes edge-case handling for abbreviations."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["javascript", "snake case", "camelcase", "string manipulation", "naming conventions"]
draft: false
---

JavaScript uses camelCase by convention, but working with Python backends, PostgreSQL databases, or legacy APIs often requires converting to snake_case. Here are three approaches that handle abbreviations correctly.

## The regex approach (recommended)

A single-pass regex inserts underscores before uppercase letters. The tricky part is handling consecutive capitals like `HTTP` or `JSON`:

```js
function camelToSnake(str) {
  return str
    // Insert _ between a lowercase/digit and an uppercase: "aB" → "a_B"
    .replace(/([a-z0-9])([A-Z])/g, '$1_$2')
    // Insert _ between a run of uppercase and a new capitalized word: "ABCDef" → "ABC_Def"
    .replace(/([A-Z]+)([A-Z][a-z])/g, '$1_$2')
    .toLowerCase();
}

camelToSnake('firstName');          // "first_name"
camelToSnake('getUserById');        // "get_user_by_id"
camelToSnake('parseHTTPResponse');  // "parse_http_response"
camelToSnake('myJSONKey');          // "my_json_key"
camelToSnake('HTMLParser');         // "html_parser"
```

The two-replace pattern handles both standard camelCase and acronym runs. A single replace handles simple cases but produces `"parse_h_t_t_p_response"` for abbreviations.

## Converting object keys

When working with API responses, you often need to convert all keys in a nested object:

```js
function camelToSnake(str) {
  return str
    .replace(/([a-z0-9])([A-Z])/g, '$1_$2')
    .replace(/([A-Z]+)([A-Z][a-z])/g, '$1_$2')
    .toLowerCase();
}

function deepCamelKeysToSnake(obj) {
  if (Array.isArray(obj)) {
    return obj.map(deepCamelKeysToSnake);
  }
  if (obj !== null && typeof obj === 'object') {
    return Object.fromEntries(
      Object.entries(obj).map(([key, value]) => [
        camelToSnake(key),
        deepCamelKeysToSnake(value),
      ])
    );
  }
  return obj;
}
```

Usage:

```js
const apiResponse = {
  userId: 42,
  firstName: 'Alice',
  address: {
    streetName: 'Main St',
    zipCode: '12345',
  },
  recentOrders: [
    { orderId: 1, totalAmount: 99.99 },
  ],
};

deepCamelKeysToSnake(apiResponse);
// {
//   user_id: 42,
//   first_name: 'Alice',
//   address: { street_name: 'Main St', zip_code: '12345' },
//   recent_orders: [{ order_id: 1, total_amount: 99.99 }]
// }
```

## Using a library: `change-case`

The [`change-case`](https://github.com/blakeembrey/change-case) package is well-maintained and handles a wide range of edge cases:

```bash
npm install change-case
```

```js
import { snakeCase } from 'change-case';

snakeCase('firstName');          // "first_name"
snakeCase('getUserById');        // "get_user_by_id"
snakeCase('parseHTTPResponse');  // "parse_http_response"
snakeCase('myJSONKey');          // "my_json_key"
```

`change-case` also exports `camelCase`, `pascalCase`, `kebabCase`, and others, so it's useful when you need bidirectional conversion in the same project.

For projects that want zero dependencies and handle only the common case, the regex function above is the right call. For projects already using a utility library (lodash, for example), check for a built-in before adding `change-case`.

**Lodash's `_.snakeCase`:**

```js
import _ from 'lodash';

_.snakeCase('firstName');    // "first_name"
_.snakeCase('parseHTTP');    // "parse_http"
```

Lodash's implementation splits on word boundaries using a Unicode-aware regex and handles most real-world inputs correctly.

## TypeScript: typed utility

For TypeScript projects, you can type-check simple conversions at compile time using template literal types:

```ts
type CamelToSnake<T extends string> =
  T extends `${infer Head}${infer Tail}`
    ? Head extends Uppercase<Head>
      ? `_${Lowercase<Head>}${CamelToSnake<Tail>}`
      : `${Head}${CamelToSnake<Tail>}`
    : T;

type Result = CamelToSnake<'firstName'>;  // "first_name" — inferred at compile time
```

This works for simple identifiers but gets expensive for the compiler on very long strings or complex abbreviation patterns. For runtime conversion, use the regex approach with a type assertion.

## Edge cases

```js
camelToSnake('');              // ""        — empty string safe
camelToSnake('alreadysnake'); // "alreadysnake" — no change
camelToSnake('ID');            // "id"       — all-caps treated as one word
camelToSnake('userID');        // "user_id"  — correct with two-pass regex
camelToSnake('getHTTPS');      // "get_https"
```

Test your implementation against identifiers from your actual data source before shipping.

## Online converter

For one-off conversions — renaming a batch of variables, converting an API schema — paste your identifiers into [caseconvert.io](/) and get the output in any case style without writing any code.
