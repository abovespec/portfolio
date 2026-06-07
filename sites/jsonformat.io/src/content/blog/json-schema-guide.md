---
title: "JSON Schema: Validate Your Data Structures"
description: "JSON Schema lets you define the shape of your JSON data and validate it automatically. This guide covers the essential keywords with practical examples."
publishDate: 2026-04-22
author: "Editorial Team"
tags: ["json", "json-schema", "validation", "api-design"]
---

JSON Schema is a vocabulary for describing the structure of JSON documents. You write a schema (which is itself a JSON document), and a validator checks whether your data conforms to it. This is useful for API request/response validation, configuration file checking, automated testing, and documentation.

The current stable specification is **Draft 2020-12**, though Draft 7 is still widely used in tooling.

## A minimal schema

Every JSON Schema document is a JSON object. The simplest valid schema accepts any value:

For more on this topic, see [*Unexpected Token in JSON: What It Means and How to Fix It*](/blog/unexpected-token-json-error).

```json
{}
```

A schema that rejects everything:

```json
{ "not": {} }
```

In practice, you constrain data with keywords. Here is a schema for a user object:

```json
{
  "type": "object",
  "required": ["id", "email"],
  "properties": {
    "id": { "type": "integer", "minimum": 1 },
    "email": { "type": "string", "format": "email" },
    "name": { "type": "string", "maxLength": 100 },
    "active": { "type": "boolean" }
  },
  "additionalProperties": false
}
```

This schema says:
- The root value must be an object
- `id` and `email` are required; `name` and `active` are optional
- `id` must be an integer ≥ 1
- `email` must be a string in email format
- No extra properties are allowed

## Core type keywords

`type` accepts a string or an array of strings:

```json
{ "type": "string" }
{ "type": ["string", "null"] }
```

Valid types: `string`, `number`, `integer`, `boolean`, `array`, `object`, `null`.

## String constraints

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 255,
  "pattern": "^[a-zA-Z0-9_-]+$",
  "format": "email"
}
```

Common `format` values: `email`, `uri`, `date` (`YYYY-MM-DD`), `date-time` (ISO 8601), `uuid`.

Note: `format` validation is optional in many validators — check your tooling.

## Number constraints

```json
{
  "type": "number",
  "minimum": 0,
  "maximum": 100,
  "exclusiveMinimum": 0,
  "multipleOf": 0.5
}
```

Use `integer` instead of `number` when you want to exclude decimal values.

## Array constraints

```json
{
  "type": "array",
  "items": { "type": "string" },
  "minItems": 1,
  "maxItems": 10,
  "uniqueItems": true
}
```

`items` applies the same schema to every element. For a tuple (positional items with different types), use `prefixItems` in Draft 2020-12:

```json
{
  "type": "array",
  "prefixItems": [
    { "type": "string" },
    { "type": "integer" },
    { "type": "boolean" }
  ],
  "items": false
}
```

## Combining schemas

`anyOf`, `oneOf`, and `allOf` let you compose schemas:

```json
{
  "anyOf": [
    { "type": "string" },
    { "type": "integer" }
  ]
}
```

`anyOf` — valid if the data matches at least one sub-schema.  
`oneOf` — valid if the data matches exactly one sub-schema.  
`allOf` — valid if the data matches all sub-schemas (useful for extending a base schema).

## Enumerations

```json
{ "enum": ["red", "green", "blue"] }
{ "const": "active" }
```

`enum` accepts any list of values. `const` is shorthand for a single-value enum.

## $defs and $ref

Use `$defs` to define reusable sub-schemas, and `$ref` to reference them:

```json
{
  "$defs": {
    "address": {
      "type": "object",
      "required": ["street", "city"],
      "properties": {
        "street": { "type": "string" },
        "city": { "type": "string" }
      }
    }
  },
  "type": "object",
  "properties": {
    "billing": { "$ref": "#/$defs/address" },
    "shipping": { "$ref": "#/$defs/address" }
  }
}
```

## Tooling

- **JavaScript** — `ajv` is the most popular validator; `zod` and `yup` generate schemas programmatically
- **Python** — `jsonschema` library
- **Go** — `gojsonschema`
- **Java** — `everit-org/json-schema`
- **VS Code** — built-in JSON schema support for `settings.json`, `tsconfig.json`, and any file you associate via `json.schemas`
- **Postman / Insomnia** — can validate API responses against a JSON Schema

For more on this topic, see [*How to Format JSON in VS Code: Shortcuts, Settings, and Extensions*](/blog/format-json-vscode).

For more on this topic, see [*What Is JSON? A Plain-English Introduction*](/blog/what-is-json).

## Generating schemas from data

If you have example data and need a starting schema, paste the JSON into the [formatter](/), then use a tool like [quicktype](https://quicktype.io) to generate a schema (or TypeScript types) from the example. Always review generated schemas — they reflect the shape of your examples, not necessarily all valid inputs.
