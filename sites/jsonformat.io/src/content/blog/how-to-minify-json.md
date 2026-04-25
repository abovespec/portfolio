---
title: "How to Minify JSON: Tools, Commands, and Code Examples"
description: "Minify JSON to reduce payload size using online tools, Python, JavaScript, jq, and command-line utilities. Includes benchmark data and when minification actually matters."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["json", "minify", "optimization", "performance", "json tools"]
draft: false
---

JSON minification removes all unnecessary whitespace — spaces, tabs, and newlines — without changing the data. The result is a smaller payload that parses faster and costs less to transfer. This guide covers every practical way to minify JSON and explains when it's worth the effort.

## What minification does

Before:

```json
{
  "user": {
    "id": 1,
    "name": "Alice",
    "email": "alice@example.com"
  }
}
```

After:

```json
{"user":{"id":1,"name":"Alice","email":"alice@example.com"}}
```

The content is identical. The minified version is 59 bytes; the pretty-printed version is 89 bytes — a 34% reduction for this trivial example. Real API responses with many nested objects typically compress 30–60%.

## Online minification

Paste your JSON into our [JSON formatter](/) above and click **Minify**. The result is a single-line JSON string ready to copy.

## Command line

### Python (no install required)

```bash
# Minify a file and print to stdout
python -m json.tool --compact input.json

# Minify and write to a new file
python -m json.tool --compact input.json > output.min.json

# Minify piped input
echo '{ "a": 1, "b": 2 }' | python -m json.tool --compact
```

### Node.js (no install required)

```bash
node -e "process.stdout.write(JSON.stringify(JSON.parse(require('fs').readFileSync('/dev/stdin','utf8'))))" < input.json
```

Or write it as a reusable script:

```js
// minify.js
const fs = require('fs');
const input = fs.readFileSync(process.argv[2], 'utf8');
process.stdout.write(JSON.stringify(JSON.parse(input)));
```

```bash
node minify.js input.json > output.min.json
```

### jq

```bash
# --compact-output / -c removes whitespace
jq -c . input.json > output.min.json

# Pipe from curl
curl -s https://api.example.com/data | jq -c .
```

### Bash one-liner (using Python)

```bash
python3 -c "import sys,json; print(json.dumps(json.load(sys.stdin),separators=(',',':')))" < input.json
```

## In code

### JavaScript

```js
// String input
const minified = JSON.stringify(JSON.parse(jsonString));

// Object input (already parsed)
const minified = JSON.stringify(obj);

// File in Node.js
const fs = require('fs');
const data = JSON.parse(fs.readFileSync('input.json', 'utf8'));
fs.writeFileSync('output.min.json', JSON.stringify(data));
```

The key insight: `JSON.stringify` without a `space` argument produces minified output by default.

### Python

```python
import json

# From a string
minified = json.dumps(json.loads(json_string), separators=(',', ':'))

# From a file
with open('input.json') as f:
    data = json.load(f)
with open('output.min.json', 'w') as f:
    json.dump(data, f, separators=(',', ':'))
```

`separators=(',', ':')` removes the space after `,` and `:` that Python adds by default.

### Go

```go
import (
    "bytes"
    "encoding/json"
)

func minifyJSON(pretty []byte) ([]byte, error) {
    var buf bytes.Buffer
    if err := json.Compact(&buf, pretty); err != nil {
        return nil, err
    }
    return buf.Bytes(), nil
}
```

### Ruby

```ruby
require 'json'
minified = JSON.generate(JSON.parse(json_string))
```

## Batch minification

```bash
# Minify all JSON files in a directory (Python)
for f in *.json; do
  python -m json.tool --compact "$f" > "${f%.json}.min.json"
done

# Using jq
find . -name '*.json' -exec sh -c 'jq -c . "$1" > "${1%.json}.min.json"' _ {} \;
```

## Does minification actually help?

### When it matters most

1. **High-throughput APIs** — Thousands of requests per second, each carrying a repeated structure. Smaller payloads reduce bandwidth costs and network latency.
2. **Mobile clients on constrained connections** — Even a 10 KB reduction per response compounds quickly.
3. **Static assets bundled in a build** — Translation files, config JSON shipped with a web app.

### When it doesn't matter

1. **Already compressed by the server** — HTTP responses are typically gzip or Brotli compressed. Compression works on repeated bytes, so pretty-printed JSON compresses almost as well as minified JSON. The difference after compression is often less than 5%.
2. **Internal service calls over a local network** — Latency is measured in microseconds; a few kilobytes of whitespace is irrelevant.
3. **Human-read configs** — Readability matters more than a few bytes.

### Numbers in context

A realistic medium-sized API response (10 KB pretty-printed):
- Raw: 10 KB pretty, 7 KB minified (30% reduction)
- gzip compressed: 1.8 KB pretty, 1.7 KB minified (~6% difference)

Conclusion: if your server gzips responses (it should), minification is a micro-optimisation. If it doesn't gzip, adding gzip is far more impactful than minifying.

## Minification in build pipelines

### Webpack / Vite (JSON assets)

Both bundlers minify JSON assets automatically in production builds when you import them as modules. No manual step needed.

### npm scripts

```json
{
  "scripts": {
    "minify-json": "node -e \"const fs=require('fs'); const f=process.argv[1]; fs.writeFileSync(f.replace('.json','.min.json'), JSON.stringify(JSON.parse(fs.readFileSync(f))))\" --"
  }
}
```

### Makefile

```makefile
%.min.json: %.json
	python -m json.tool --compact $< > $@
```

## Reversing minification (pretty-printing)

To go back to human-readable JSON from a minified file:

```bash
# Python
python -m json.tool input.min.json

# Node.js
node -e "console.log(JSON.stringify(JSON.parse(require('fs').readFileSync('input.min.json','utf8')), null, 2))"
```

Or paste into our [JSON formatter](/) and click **Format**.

## Quick reference

| Tool | Command |
|------|---------|
| Python CLI | `python -m json.tool --compact input.json` |
| Node.js inline | `node -e "process.stdout.write(JSON.stringify(JSON.parse(fs.readFileSync('in.json','utf8'))))"` |
| jq | `jq -c . input.json` |
| JavaScript | `JSON.stringify(JSON.parse(str))` |
| Python code | `json.dumps(json.loads(s), separators=(',',':'))` |
| Online | Paste above → Minify button |

## References

- [MDN — JSON.stringify](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON/stringify)
- [Python docs — json module](https://docs.python.org/3/library/json.html)
- [ECMA-404 — JSON Standard](https://www.ecma-international.org/publications-and-standards/standards/ecma-404/)
- [jq manual](https://stedolan.github.io/jq/manual/)
