---
title: "Regex Flags and Modifiers: A Complete Reference Guide"
description: "Master regex flags including case-insensitive (i), global (g), multiline (m), and dotall (s). Covers Python, JavaScript, and PCRE with examples."
publishDate: 2026-06-07
updatedDate: 2026-06-07
author: "Editorial Team"
tags: ["regex", "flags", "modifiers", "regular expressions", "programming"]
draft: false
heroImage: "/images/blog/regex-flags-hero.png"
---

Regex flags (also called modifiers) change how a pattern is interpreted and applied. Without flags, a regex pattern is case-sensitive, matches only the first occurrence, and treats `.` as "any character except newline." Flags override these defaults.

## Common Flags Across Languages

Most regex engines share a core set of flags, though syntax varies:

| Flag | Meaning | Python | JavaScript | PCRE |
|------|---------|--------|-----------|------|
| Case-insensitive | `i` | `re.IGNORECASE` or `re.I` | `i` | `(?i)` or `/i` |
| Global (all matches) | `g` | N/A (use `findall`) | `g` | N/A (use `find_all`) |
| Multiline | `m` | `re.MULTILINE` or `re.M` | `m` | `(?m)` or `/m` |
| Dotall | `s` | `re.DOTALL` or `re.S` | `s` | `(?s)` or `/s` |
| Verbose | `x` | `re.VERBOSE` or `re.X` | N/A | `(?x)` or `/x` |
| Unicode | `u` | Default in Python 3 | `u` | Enabled by default |

## The `i` Flag: Case-Insensitive Matching

With `i`, uppercase and lowercase letters are treated as equivalent.

**Without `i`:** `/hello/` matches "hello" but not "Hello" or "HELLO"

**With `i`:** `/hello/i` matches "hello", "Hello", "HELLO", "HeLLo"

**Python:**
```python
import re
re.search(r'hello', 'Hello World', re.IGNORECASE)  # matches
re.findall(r'python', text, re.I)  # case-insensitive findall
```

**JavaScript:**
```javascript
/python/i.test('Python is great')  // true
'Hello World'.match(/hello/i)      // ['Hello']
```

**Inline flag (works in most engines):** `(?i)hello` — applies case-insensitive matching from that point in the pattern.

### Unicode Case Folding

With `i` and `u` flags together, matching extends to Unicode case equivalents. For example, the German `ß` (sharp s) is case-equivalent to `SS` in some contexts.

## The `g` Flag: Global Matching (JavaScript)

In JavaScript, patterns without `g` match only the first occurrence. With `g`, they match all occurrences.

```javascript
'aabbcc'.match(/[a-z]/);   // ['a'] — only first match
'aabbcc'.match(/[a-z]/g);  // ['a', 'a', 'b', 'b', 'c', 'c'] — all matches

// replace: without g, only first match is replaced
'hello world'.replace(/o/, 'O');   // 'hellO world'
'hello world'.replace(/o/g, 'O'); // 'hellO wOrld'
```

In Python, there's no `g` flag — `re.findall()` always returns all matches, and `re.search()` always returns only the first.

## The `m` Flag: Multiline Mode

Without `m`, `^` matches the start of the **string** and `$` matches the end of the **string**.

With `m`, `^` matches the start of each **line** and `$` matches the end of each **line**.

```python
text = "first line\nsecond line\nthird line"

# Without m: only matches at start of string
re.findall(r'^\w+', text)              # ['first']

# With m: matches at start of each line
re.findall(r'^\w+', text, re.M)       # ['first', 'second', 'third']
```

```javascript
const text = "first line\nsecond line\nthird line";

text.match(/^\w+/g)   // ['first'] — only start of string
text.match(/^\w+/gm)  // ['first', 'second', 'third'] — start of each line
```

**Common use case**: validating or extracting from multi-line text where each line follows a pattern.

```python
# Extract all lines that start with a bullet point
bullets = re.findall(r'^[-*]\s+(.+)', text, re.M)
```

## The `s` Flag: Dotall Mode (Single-Line Mode)

Without `s`, the dot `.` matches any character **except newline** (`\n`).

With `s`, `.` matches **any character including newline**.

```python
text = "start\nmiddle\nend"

re.search(r'start.+end', text)          # None — . doesn't match \n
re.search(r'start.+end', text, re.S)   # matches 'start\nmiddle\nend'
```

```javascript
const html = '<div>\n  <p>content</p>\n</div>';

/<div>.+<\/div>/.test(html)    // false — . doesn't cross newlines
/<div>.+<\/div>/s.test(html)   // true — . matches newlines too
```

**Note:** The `s` flag was added to JavaScript in ES2018. Older code uses `[\s\S]` as a workaround for "any character including newline."

## The `x` Flag: Verbose Mode (Free-Spacing)

With `x` (Python's `re.VERBOSE`), whitespace in the pattern is ignored (except inside character classes or when escaped), and `#` starts a comment to end of line. This makes complex patterns readable.

```python
# Without verbose: hard to read
phone_pattern = r'\+?1?[-.\s]?\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})'

# With verbose: documented and readable
phone_pattern = re.compile(r'''
    \+?1?           # optional country code
    [-.\s]?         # optional separator
    \(?             # optional opening paren
    (\d{3})         # area code
    \)?             # optional closing paren
    [-.\s]?         # optional separator
    (\d{3})         # exchange
    [-.\s]?         # optional separator
    (\d{4})         # number
''', re.VERBOSE)
```

JavaScript does not have a verbose mode. PCRE supports it with `/x` or `(?x)`.

## The `u` Flag: Unicode Mode (JavaScript)

JavaScript's `u` flag enables full Unicode support:
- Allows Unicode escapes: `\u{1F600}` for emoji
- Makes `.`, `^`, `$`, character classes handle Unicode code points (not UTF-16 code units)
- Enables `\p{Script=Latin}` Unicode property escapes (with `u` flag)

```javascript
/\u{1F600}/u.test('😀')  // true
/\p{Emoji}/u.test('😀')  // true — requires u flag
```

In Python 3, Unicode support is enabled by default. In Python 2, use `re.UNICODE`.

## Combining Multiple Flags

### JavaScript: chain flags in the literal
```javascript
/pattern/gim  // global + case-insensitive + multiline
/pattern/gims // global + case-insensitive + multiline + dotall (ES2018)
```

### Python: combine with bitwise OR
```python
re.findall(r'pattern', text, re.I | re.M)
re.compile(r'pattern', re.IGNORECASE | re.MULTILINE | re.DOTALL)
```

### Inline flags (work inside the pattern itself)
```
(?i)pattern       — case-insensitive from here
(?im)pattern      — case-insensitive + multiline
(?i:pattern)      — apply flag only to this group
```

Inline flags are useful when you need flag behavior in part of a pattern or when passing a pattern string to a function that doesn't accept a flags argument.

## Lesser-Known Flags

### `d` Flag (JavaScript ES2022): Indices
Returns start and end indices for each match and capture group.

```javascript
const match = 'hello world'.match(/(\w+)/d);
console.log(match.indices[0]); // [0, 5] — position of full match
console.log(match.indices[1]); // [0, 5] — position of group 1
```

### `re.ASCII` (Python): Limit to ASCII
Forces `\w`, `\d`, `\s` etc. to match only ASCII characters instead of full Unicode.

```python
re.findall(r'\w+', 'café', re.ASCII)  # ['caf'] — é excluded
re.findall(r'\w+', 'café')            # ['café'] — é included
```

## Testing Flags in regexbuilder.io

[regexbuilder.io](/) lets you toggle flags interactively and see how they affect match results in real time. You can test patterns against multi-line input with the `m` flag, or switch `s` on and off to see how dotall changes `.` behavior — without writing any code.
