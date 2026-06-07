---
title: "How to Validate JSON: Common Errors and How to Fix Them"
description: "Validate JSON using online tools, command-line utilities, and code. Learn the 6 most common JSON validation errors and exactly how to resolve each one."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["json validation", "json errors", "json schema", "debugging", "json tools"]
draft: false
---

Valid JSON must satisfy two requirements: correct *syntax* (parseable by any compliant parser) and, for structured data, a matching *schema* (the right keys, types, and constraints). This guide covers both layers — how to check them, what errors look like, and how to fix them.

## Layer 1: Syntax validation

A JSON file is syntactically valid if it can be parsed without errors. The rules come from [ECMA-404](https://www.ecma-international.org/publications-and-standards/standards/ecma-404/) and [RFC 8259](https://www.rfc-editor.org/rfc/rfc8259).

### Online validation

Paste your JSON into our [JSON validator](/) above and click **Validate**. You'll see either a green "Valid JSON" confirmation or an error with the line and column number of the first problem.

### Command line

```bash
# Python (no install required)
python -m json.tool input.json

# Node.js (no install required)
node -e "JSON.parse(require('fs').readFileSync('input.json','utf8')); console.log('Valid')"

# jq (must be installed: brew install jq / apt install jq)
jq . input.json
```

All three tools print an error message pointing to the problem line if the JSON is invalid.

### In code

**JavaScript:**

```js
function validateJson(str) {
  try {
    JSON.parse(str);
    return { valid: true };
  } catch (e) {
    return { valid: false, error: e.message };
  }
}
```

**Python:**

```python
import json

def validate_json(s):
    try:
        json.loads(s)
        return True, None
    except json.JSONDecodeError as e:
        return False, str(e)
```

## 6 common syntax errors and how to fix them

### 1. Trailing comma

```json
{
  "name": "Alice",
  "age": 30,
}
```

Error: `Unexpected token }` (the parser expects another key-value pair after the comma).

For more on this topic, see [*Unexpected Token in JSON: What It Means and How to Fix It*](/blog/unexpected-token-json-error).

Fix: Remove the comma after the last key-value pair.

```json
{
  "name": "Alice",
  "age": 30
}
```

### 2. Single quotes instead of double quotes

```json
{ 'name': 'Alice' }
```

Fix: Replace all single quotes with double quotes.

```json
{ "name": "Alice" }
```

### 3. Unquoted keys

```json
{ name: "Alice" }
```

Fix: All keys must be quoted strings.

```json
{ "name": "Alice" }
```

### 4. Comments

```json
{
  // user config
  "theme": "dark"
}
```

Fix: Remove comments. JSON has no comment syntax. If you need comments, use YAML or JSON5 and convert to JSON programmatically.

### 5. Unescaped backslashes

```json
{ "path": "C:\Users\Alice" }
```

Error: The `\U` and `\A` sequences are not valid JSON escape sequences.

Fix: Escape each backslash:

```json
{ "path": "C:\\Users\\Alice" }
```

### 6. Wrong value types

```json
{ "active": True }
```

Error: `True` is a Python boolean literal. JSON booleans are lowercase.

Fix:

```json
{ "active": true }
```

JSON value types and their exact spellings:

| Type | Valid spellings |
|------|----------------|
| Boolean | `true`, `false` |
| Null | `null` |
| Number | `42`, `3.14`, `-1`, `1e10` |
| String | `"double-quoted"` |
| Array | `[1, 2, 3]` |
| Object | `{"key": "value"}` |

## Layer 2: Schema validation

Syntax validation tells you whether JSON can be parsed. Schema validation tells you whether the parsed data has the structure your application expects — required fields, correct types, value ranges, allowed patterns.

For more on this topic, see [*JSON Schema: Validate Your Data Structures*](/blog/json-schema-guide).

The standard for describing JSON structure is [JSON Schema](https://json-schema.org/).

### Example schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["id", "name", "email"],
  "properties": {
    "id": { "type": "integer", "minimum": 1 },
    "name": { "type": "string", "minLength": 1 },
    "email": { "type": "string", "format": "email" },
    "age": { "type": "integer", "minimum": 0, "maximum": 150 },
    "tags": {
      "type": "array",
      "items": { "type": "string" }
    }
  }
}
```

### Validate in Node.js with AJV

[AJV](https://ajv.js.org/) is the most popular JSON Schema validator for JavaScript:

For more on this topic, see [*Pretty-Printing JSON in JavaScript: JSON.stringify, DevTools, and Node.js*](/blog/pretty-print-json-javascript).

```bash
npm install ajv
```

```js
import Ajv from 'ajv';
import addFormats from 'ajv-formats';

const ajv = new Ajv();
addFormats(ajv);

const schema = { /* ... your schema ... */ };
const validate = ajv.compile(schema);

const data = { id: 1, name: "Alice", email: "alice@example.com" };
const valid = validate(data);

if (!valid) {
  console.error(validate.errors);
} else {
  console.log('Valid!');
}
```

### Validate in Python with jsonschema

```bash
pip install jsonschema
```

```python
import json
import jsonschema
from jsonschema import validate

schema = {
    "type": "object",
    "required": ["id", "name"],
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"}
    }
}

data = {"id": 1, "name": "Alice"}

try:
    validate(instance=data, schema=schema)
    print("Valid!")
except jsonschema.ValidationError as e:
    print(f"Invalid: {e.message}")
```

### Validate in VS Code

Add a `"$schema"` key to your JSON file and VS Code shows inline red squiggles for schema violations:

```json
{
  "$schema": "https://json.schemastore.org/package.json",
  "name": "my-app",
  "version": "1.0.0"
}
```

The [JSON Schema Store](https://www.schemastore.org/json/) hosts schemas for hundreds of popular config file formats.

## Batch validation

To validate multiple files at once:

```bash
# Python — validate all JSON files in a directory
for f in *.json; do
  python -m json.tool "$f" > /dev/null && echo "$f: valid" || echo "$f: INVALID"
done
```

```bash
# Node.js — using a script
find . -name '*.json' | while read f; do
  node -e "JSON.parse(require('fs').readFileSync('$f'))" && echo "$f OK" || echo "$f FAIL"
done
```

## Frequently asked questions

**Can JSON have comments?**
No. Comments are not part of the JSON specification. Use YAML, JSONC (JSON with Comments — supported in VS Code config files), or JSON5 if you need comments.

**What is the difference between `null` and an empty string `""`?**
`null` means the absence of a value. `""` is a value — an empty string. JSON Schema distinguishes them; your application logic should too.

**Are JSON keys case-sensitive?**
Yes. `"Name"` and `"name"` are different keys.

**Does JSON support integers and floats separately?**
The JSON spec has one `number` type. Your parser may represent integers and floats differently, but JSON itself doesn't distinguish.

## References

- [ECMA-404 — The JSON Standard](https://www.ecma-international.org/publications-and-standards/standards/ecma-404/)
- [RFC 8259 — JSON Data Interchange Format](https://www.rfc-editor.org/rfc/rfc8259)
- [json.org — JSON grammar](https://www.json.org/json-en.html)
- [JSON Schema — specification](https://json-schema.org/)
- [AJV — JSON Schema validator for JavaScript](https://ajv.js.org/)
- [jsonschema — Python library](https://python-jsonschema.readthedocs.io/)
