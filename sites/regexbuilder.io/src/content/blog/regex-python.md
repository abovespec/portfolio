---
title: "Regex in Python: Complete Guide to the re Module"
description: "Master Python regex with the re module. Covers re.match, re.search, re.findall, re.sub, re.compile, flags, named groups, and practical examples."
publishDate: 2026-06-07
updatedDate: 2026-06-07
author: "Editorial Team"
tags: ["regex", "python", "re module", "python regex", "pattern matching"]
draft: false
---

Python's `re` module is the standard library's built-in engine for regular expressions. It follows the PCRE (Perl-Compatible Regular Expression) tradition closely, supports named groups, verbose mode, and all the standard flags. This guide covers everything you need to work with regex in Python effectively.

## Importing the re module

All regex functionality lives in the `re` module. No pip install required — it ships with every Python installation.

```python
import re
```

Always use **raw strings** (`r"..."`) for your patterns. Raw strings tell Python not to interpret backslashes as escape sequences, so `\d`, `\s`, and `\b` reach the regex engine unchanged.

```python
# Wrong — Python interprets \b as a backspace character
pattern = "\bword\b"

# Correct — the backslash is passed to the regex engine
pattern = r"\bword\b"
```

## Core functions

### re.match — match at the start of a string

`re.match` only checks at the **beginning** of the string. It returns a match object or `None`.

```python
import re

result = re.match(r'\d+', '42 apples')
print(result.group())  # '42'

result = re.match(r'\d+', 'apples 42')
print(result)          # None — no digits at the start
```

### re.search — find first match anywhere

`re.search` scans the entire string and returns the **first** match found anywhere in it.

```python
result = re.search(r'\d+', 'I have 42 apples and 7 oranges')
print(result.group())  # '42'
print(result.start())  # 7 (index position)
print(result.end())    # 9
```

### re.findall — return all matches as a list

`re.findall` returns a flat list of all non-overlapping matches. If the pattern has groups, it returns a list of group tuples.

```python
text = 'I have 42 apples and 7 oranges and 100 grapes'

# No groups — returns list of matched strings
numbers = re.findall(r'\d+', text)
print(numbers)  # ['42', '7', '100']

# With groups — returns list of tuples
matches = re.findall(r'(\d+)\s+(\w+)', text)
print(matches)  # [('42', 'apples'), ('7', 'oranges'), ('100', 'grapes')]
```

### re.finditer — iterate over match objects

`re.finditer` returns an iterator of match objects, giving you access to position data for each match.

```python
for m in re.finditer(r'\d+', 'ports: 80, 443, 8080'):
    print(f"Found {m.group()!r} at position {m.start()}-{m.end()}")

# Found '80' at position 7-9
# Found '443' at position 11-14
# Found '8080' at position 16-20
```

### re.sub — substitute matches

`re.sub(pattern, replacement, string)` replaces all matches with a replacement string or the return value of a callable.

```python
# Basic substitution
result = re.sub(r'\s+', ' ', 'too   many   spaces')
print(result)  # 'too many spaces'

# Using backreferences in replacement — \1 refers to group 1
text = '2026-06-07'
formatted = re.sub(r'(\d{4})-(\d{2})-(\d{2})', r'\3/\2/\1', text)
print(formatted)  # '07/06/2026'

# Callable replacement
def double_number(m):
    return str(int(m.group()) * 2)

result = re.sub(r'\d+', double_number, 'I have 3 cats and 5 dogs')
print(result)  # 'I have 6 cats and 10 dogs'
```

`re.sub` also accepts a `count` argument to limit the number of replacements:

```python
result = re.sub(r'a', 'X', 'banana', count=2)
print(result)  # 'bXnXna'
```

### re.split — split a string by a pattern

```python
# Split on one or more whitespace characters
parts = re.split(r'\s+', 'one  two   three')
print(parts)  # ['one', 'two', 'three']

# Split on commas and/or semicolons with optional spaces
parts = re.split(r'[,;]\s*', 'a, b; c,d; e')
print(parts)  # ['a', 'b', 'c', 'd', 'e']
```

## Compiling patterns with re.compile

If you use the same pattern many times, compile it once for better performance.

```python
# Without compiling — pattern is re-compiled each call
for line in lines:
    re.search(r'\d{4}-\d{2}-\d{2}', line)

# With compiling — compiled once, reused
date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
for line in lines:
    date_pattern.search(line)
```

The compiled object has all the same methods: `.match()`, `.search()`, `.findall()`, `.finditer()`, `.sub()`, `.split()`.

```python
ip_pattern = re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b')
log_line = 'Request from 192.168.1.42 at 2026-06-07T12:00:00Z'
match = ip_pattern.search(log_line)
print(match.group())  # '192.168.1.42'
```

## Flags

Pass flags as the last argument to any `re` function, or combine them with `|`.

| Flag | Short | Effect |
|------|-------|--------|
| `re.IGNORECASE` | `re.I` | Case-insensitive matching |
| `re.MULTILINE` | `re.M` | `^` and `$` match line starts/ends, not just string |
| `re.DOTALL` | `re.S` | `.` matches newlines as well |
| `re.VERBOSE` | `re.X` | Whitespace and comments allowed in pattern |
| `re.ASCII` | `re.A` | `\w`, `\d`, `\s` match ASCII only, not full Unicode |
| `re.UNICODE` | `re.U` | Default in Python 3; `\w` matches Unicode word chars |

### IGNORECASE

```python
re.findall(r'python', 'Python PYTHON python', re.I)
# ['Python', 'PYTHON', 'python']
```

### MULTILINE

Without `re.M`, `^` and `$` match only at the very start and end of the whole string.

```python
text = "first line\nsecond line\nthird line"

# Without MULTILINE — ^ only matches the start of the entire string
re.findall(r'^\w+', text)
# ['first']

# With MULTILINE — ^ matches at each line start
re.findall(r'^\w+', text, re.M)
# ['first', 'second', 'third']
```

### DOTALL

```python
html = "<div>\n  <p>Hello</p>\n</div>"

# Without DOTALL — . doesn't match newlines
re.search(r'<div>(.+)</div>', html)          # None

# With DOTALL — . matches everything including newlines
m = re.search(r'<div>(.+)</div>', html, re.S)
print(m.group(1))  # '\n  <p>Hello</p>\n'
```

### VERBOSE

Write readable, documented patterns with comments:

```python
date_pattern = re.compile(r"""
    (\d{4})   # year
    -         # separator
    (\d{2})   # month
    -         # separator
    (\d{2})   # day
""", re.VERBOSE)

m = date_pattern.match('2026-06-07')
print(m.groups())  # ('2026', '06', '07')
```

## Named groups

Named groups use the syntax `(?P<name>...)`. They make patterns more readable and let you access captures by name instead of index.

```python
log_pattern = re.compile(r"""
    (?P<ip>\d{1,3}(?:\.\d{1,3}){3})   # IP address
    \s+-\s+-\s+
    \[(?P<timestamp>[^\]]+)\]           # timestamp in brackets
    \s+
    "(?P<method>[A-Z]+)\s+             # HTTP method
    (?P<path>[^\s"]+)                   # request path
""", re.VERBOSE)

line = '192.168.1.1 - - [07/Jun/2026:12:00:00] "GET /index.html'
m = log_pattern.search(line)
if m:
    print(m.group('ip'))        # '192.168.1.1'
    print(m.group('method'))    # 'GET'
    print(m.group('path'))      # '/index.html'
    print(m.groupdict())        # dict of all named groups
```

Reference named groups in substitutions with `\g<name>`:

```python
# Reformat date from YYYY-MM-DD to DD/MM/YYYY
result = re.sub(
    r'(?P<y>\d{4})-(?P<m>\d{2})-(?P<d>\d{2})',
    r'\g<d>/\g<m>/\g<y>',
    '2026-06-07'
)
print(result)  # '07/06/2026'
```

## Practical examples

### Email extraction from text

```python
import re

text = """
Contact us at support@example.com or sales@company.io.
Press inquiries: press@corp.example.org
"""

email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
emails = email_pattern.findall(text)
print(emails)
# ['support@example.com', 'sales@company.io', 'press@corp.example.org']
```

### Log file parsing

```python
import re

log_pattern = re.compile(
    r'(?P<ip>\d{1,3}(?:\.\d{1,3}){3})\s+'
    r'- - \[(?P<date>[^\]]+)\]\s+'
    r'"(?P<method>GET|POST|PUT|DELETE|PATCH)\s+(?P<path>[^\s"]+)[^"]*"\s+'
    r'(?P<status>\d{3})\s+'
    r'(?P<bytes>\d+|-)'
)

sample_log = '10.0.0.5 - - [07/Jun/2026:14:32:01 +0000] "GET /api/users HTTP/1.1" 200 1842'

m = log_pattern.search(sample_log)
if m:
    print(f"IP: {m.group('ip')}, Status: {m.group('status')}, Path: {m.group('path')}")
    # IP: 10.0.0.5, Status: 200, Path: /api/users
```

### URL extraction

```python
import re

text = "Visit https://www.example.com or http://api.test.io/v1/users?limit=10 for more."

url_pattern = re.compile(
    r'https?://[a-zA-Z0-9.-]+(?:\.[a-zA-Z]{2,})'
    r'(?:/[a-zA-Z0-9._~:/?#\[\]@!$&\'()*+,;=%-]*)?'
)

urls = url_pattern.findall(text)
print(urls)
# ['https://www.example.com', 'http://api.test.io/v1/users?limit=10']
```

### Validating and extracting structured data

```python
import re
from dataclasses import dataclass

@dataclass
class ParsedPhone:
    country_code: str
    area_code: str
    number: str

phone_pattern = re.compile(
    r'(?P<cc>\+1)?\s*'
    r'[\(]?(?P<area>\d{3})[\)]?\s*'
    r'[-.]?(?P<prefix>\d{3})'
    r'[-.]?(?P<line>\d{4})'
)

def parse_phone(s: str):
    m = phone_pattern.search(s)
    if m:
        return m.groupdict()
    return None

print(parse_phone('+1 (555) 867-5309'))
# {'cc': '+1', 'area': '555', 'prefix': '867', 'line': '5309'}
```

## Working with match objects

Every successful match returns a **match object** with useful attributes:

```python
m = re.search(r'(\w+)\s+(\w+)', 'hello world')

m.group()    # 'hello world' — entire match
m.group(0)   # 'hello world' — same as group()
m.group(1)   # 'hello' — first capturing group
m.group(2)   # 'world' — second capturing group
m.groups()   # ('hello', 'world') — all groups as a tuple
m.start()    # 0 — start index of match
m.end()      # 11 — end index
m.span()     # (0, 11) — start and end as tuple
m.string     # 'hello world' — original input string
```

## Common mistakes

**Using `re.match` when you want `re.search`:** `re.match` only matches at the start of the string. If you want to find a pattern anywhere, use `re.search` or `re.findall`.

**Forgetting raw strings:** `re.search("\bword\b", text)` won't work because `\b` becomes a backspace character. Always use `r"\bword\b"`.

**Not escaping dots:** `.` in regex means "any character". To match a literal dot, write `\.`.

**Greedy vs. lazy quantifiers:** `.*` is greedy and matches as much as possible. Use `.*?` to match as little as possible, which matters when parsing HTML-like content.

Build and test your Python regex patterns at [regexbuilder.io](/) before putting them into production code.
