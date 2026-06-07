---
title: "How to Format JSON in Python: json.dumps, json.tool, and More"
description: "Pretty-print JSON in Python using json.dumps, the json.tool CLI module, and third-party tools. Includes real code examples and common pitfalls."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["python", "json", "formatting", "json.dumps", "pretty print"]
draft: false
---

Python ships with a full-featured JSON module in its standard library. You rarely need a third-party package to format, pretty-print, sort, or minify JSON. This guide covers every built-in path — from a one-liner in the terminal to production-ready options in application code.

## The standard library: `json`

Python's `json` module ([docs](https://docs.python.org/3/library/json.html)) handles both serialisation (`dumps` / `dump`) and deserialisation (`loads` / `load`).

For more on this topic, see [*How to Minify JSON: Tools, Commands, and Code Examples*](/blog/how-to-minify-json).

## Pretty-printing a Python dict

```python
import json

data = {"name": "Alice", "age": 30, "skills": ["Python", "SQL"]}

pretty = json.dumps(data, indent=2)
print(pretty)
```

For more on this topic, see [*Pretty-Printing JSON in JavaScript: JSON.stringify, DevTools, and Node.js*](/blog/pretty-print-json-javascript).

Output:

```json
{
  "name": "Alice",
  "age": 30,
  "skills": [
    "Python",
    "SQL"
  ]
}
```

**Key parameters:**

| Parameter | Purpose | Example |
|-----------|---------|---------|
| `indent` | Number of spaces (or a string) per level | `indent=2`, `indent=4`, `indent="\t"` |
| `sort_keys` | Sort object keys alphabetically | `sort_keys=True` |
| `ensure_ascii` | Set to `False` to allow non-ASCII characters | `ensure_ascii=False` |
| `separators` | Control the `,` and `:` separators for minification | `separators=(',', ':')` |

### Sorting keys

```python
json.dumps(data, indent=2, sort_keys=True)
```

Sorted output is useful for diffing JSON files or producing canonical representations.

For more on this topic, see [*How to Validate JSON: Common Errors and How to Fix Them*](/blog/how-to-validate-json).

### Non-ASCII characters

By default, `json.dumps` escapes every non-ASCII character as a `\uXXXX` sequence. For human-readable output in other languages, disable that:

```python
data = {"city": "Zürich", "greeting": "こんにちは"}
print(json.dumps(data, ensure_ascii=False, indent=2))
```

## Pretty-printing a JSON file

```python
import json

with open('input.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('output.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
```

## Formatting from the command line: `json.tool`

Python includes `json.tool` as a runnable module — no external installs needed.

```bash
# Pretty-print a file
python -m json.tool input.json

# Pretty-print piped input
echo '{"a":1,"b":2}' | python -m json.tool

# Write formatted output to a new file
python -m json.tool input.json output.json

# Sort keys
python -m json.tool --sort-keys input.json

# Use 4-space indent (Python 3.9+)
python -m json.tool --indent 4 input.json

# Compact / minified output
python -m json.tool --compact input.json
```

This is the fastest way to format JSON from a terminal without installing anything. It's also commonly used with `curl`:

```bash
curl -s https://api.example.com/endpoint | python -m json.tool
```

## Minifying JSON

To produce compact JSON with no whitespace:

```python
compact = json.dumps(data, separators=(',', ':'))
```

From the CLI:

```bash
python -m json.tool --compact input.json
```

## Formatting JSON strings (not dicts)

If you already have a JSON string and just want to reformat it:

```python
import json

raw = '{"name":"Alice","age":30}'
pretty = json.dumps(json.loads(raw), indent=2)
print(pretty)
```

This is a two-step process: parse the string into a Python object, then serialise it back with formatting options.

## Common pitfalls

### `TypeError: Object of type X is not JSON serializable`

Python's `json.dumps` only handles built-in types: `dict`, `list`, `str`, `int`, `float`, `bool`, and `None`. For custom types like `datetime`, `Decimal`, or dataclasses, you need a custom encoder:

```python
from datetime import datetime
import json

class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

data = {"created": datetime.now()}
print(json.dumps(data, cls=DatetimeEncoder, indent=2))
```

Or use `default` parameter for simpler cases:

```python
json.dumps(data, default=str, indent=2)
```

### Unicode in Python 2 vs Python 3

In Python 3, all strings are Unicode by default — `ensure_ascii=False` just controls whether the output bytes are escaped. Always specify `encoding='utf-8'` when opening files to avoid platform-dependent defaults.

### Circular references

`json.dumps` raises `ValueError: Circular reference detected` if your object graph contains cycles. Break the cycle before serialising or use a specialised library.

## Third-party options

For most formatting tasks the standard library is sufficient. If you need more features:

- **`rich`** — Beautiful terminal output with syntax highlighting: `from rich import print_json; print_json(raw_string)`
- **`orjson`** — Significantly faster serialisation; handles `datetime`, `UUID`, numpy arrays natively
- **`pydantic`** — Model-based JSON with automatic validation

## Quick reference

```python
import json

# Parse
obj = json.loads(json_string)          # string → dict
obj = json.load(open('file.json'))     # file → dict

# Serialise
s = json.dumps(obj)                    # dict → compact string
s = json.dumps(obj, indent=2)          # dict → pretty string
s = json.dumps(obj, separators=(',',':'))  # dict → minified string

json.dump(obj, open('out.json','w'))   # dict → file (compact)
json.dump(obj, open('out.json','w'), indent=2)  # dict → file (pretty)
```

## References

- [Python docs — json module](https://docs.python.org/3/library/json.html)
- [Python docs — json.tool CLI](https://docs.python.org/3/library/json.html#module-json.tool)
- [ECMA-404 — JSON Standard](https://www.ecma-international.org/publications-and-standards/standards/ecma-404/)
- [RFC 8259 — JSON Data Interchange Format](https://www.rfc-editor.org/rfc/rfc8259)
