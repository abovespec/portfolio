---
title: "Regex Lookahead and Lookbehind: Zero-Width Assertions Explained"
description: "Learn regex lookahead and lookbehind assertions: positive/negative variants, how they match without consuming characters, and practical examples in Python and JavaScript."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["regex", "lookahead", "lookbehind", "assertions", "python", "javascript"]
draft: false
---

Lookaheads and lookbehinds are **zero-width assertions** — they check for a pattern but don't include the matched characters in the result. This lets you match text based on what comes before or after it, without capturing that context.

## The four assertion types

| Syntax | Name | Matches when |
|--------|------|-------------|
| `(?=X)` | Positive lookahead | X follows the current position |
| `(?!X)` | Negative lookahead | X does NOT follow |
| `(?<=X)` | Positive lookbehind | X precedes the current position |
| `(?<!X)` | Negative lookbehind | X does NOT precede |

For more on this topic, see [*Regex Cheatsheet: Quick Reference for Regular Expressions*](/blog/regex-cheatsheet).

## Positive lookahead `(?=...)`

Match text only if followed by a specific pattern:

```regex
\d+(?=\s*dollars?)
```

This matches the number before "dollar" or "dollars", but the word isn't included in the match:

For more on this topic, see [*Regex Groups and Capturing: How to Extract Data with Parentheses*](/blog/regex-groups-capturing).

```python
import re

text = "I have 100 dollars and 50 euros"
matches = re.findall(r'\d+(?=\s*dollars?)', text)
print(matches)  # ['100']   (not '50' — it's not followed by "dollar")
```

**Another example — match a word before a colon:**

```python
text = "name: Alice\nage: 30\ncity: London"
keys = re.findall(r'\w+(?=:)', text)
print(keys)  # ['name', 'age', 'city']
```

## Negative lookahead `(?!...)`

Match text only if NOT followed by a specific pattern:

```regex
\d+(?!\s*dollars?)
```

Matches numbers that are NOT followed by "dollar/dollars":

```python
text = "I have 100 dollars and 50 euros"
matches = re.findall(r'\d+(?!\s*dollars?)', text)
print(matches)  # ['50', '10', '5']  (note: also catches digits within 100)
```

**Exclude extension from filename:**

```python
# Match filenames that are NOT .log files
files = ["error.log", "output.txt", "debug.log", "results.csv"]
non_logs = [f for f in files if re.search(r'\.\w+$(?<!\.log)', f)]
# Better approach with negative lookahead at the dot:
non_logs = [f for f in files if not re.search(r'\.log$', f)]
```

**Password validation — must contain at least one digit:**

```regex
^(?=.*\d).{8,}$
```

```python
def has_digit(password):
    return bool(re.match(r'^(?=.*\d).{8,}$', password))

has_digit("password")   # False (no digit)
has_digit("passw0rd")   # True
```

## Positive lookbehind `(?<=...)`

Match text only if preceded by a specific pattern:

```regex
(?<=\$)\d+(?:\.\d{2})?
```

Matches the number after a dollar sign, without including the `$`:

```python
text = "Items cost $42.99 and $10.00 total"
prices = re.findall(r'(?<=\$)\d+(?:\.\d{2})?', text)
print(prices)  # ['42.99', '10.00']
```

**Extract values after a key:**

```python
text = "user=alice&role=admin&id=42"
role = re.search(r'(?<=role=)\w+', text)
print(role.group())  # 'admin'
```

## Negative lookbehind `(?<!...)`

Match text only if NOT preceded by a specific pattern:

```regex
(?<!\d)\d+
```

Match digits that don't have a digit immediately before them (i.e., the start of a number):

```python
text = "item123, code456, stand-alone 789"
# Without lookbehind — matches all digit sequences
re.findall(r'\d+', text)
# ['123', '456', '789']

# Same result here; use negative lookbehind for more specific cases
```

**More practical: match "log" not preceded by "blog":**

```python
text = "blog post about log files and catalog"
matches = re.findall(r'(?<!b)log\b', text)
print(matches)  # ['log']  (not 'blog' or 'catalog')
```

## Combining multiple lookaheads

Lookaheads can be chained at the same position. This is how complex password validation works:

```python
# Password must be:
# - 8+ characters
# - At least one lowercase letter
# - At least one uppercase letter
# - At least one digit
# - At least one symbol

pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*]).{8,}$'

def validate_password(pwd):
    return bool(re.match(pattern, pwd))

validate_password("Password1!")  # True
validate_password("password1!")  # False (no uppercase)
validate_password("PASSWORD1!")  # False (no lowercase)
```

## JavaScript lookbehind (ES2018+)

JavaScript added lookbehind support in ES2018:

```javascript
// Positive lookbehind — available in Chrome, Firefox, Edge (not IE11)
const prices = "Items: $42.99 and $10.00".match(/(?<=\$)\d+\.\d{2}/g);
console.log(prices);  // ['42.99', '10.00']

// Negative lookbehind
const text = "100 apples, 200 oranges, not 300 bananas";
const matches = text.match(/\b\d+\b(?! bananas)/g);
console.log(matches);  // ['100', '200']
```

## Lookbehind limitations

**Fixed-length lookbehinds:** Standard regex engines require lookbehinds to be fixed-width (known length at compile time). Python 3.6+ and PCRE support variable-length lookbehinds; older engines don't.

For more on this topic, see [*Regex Tutorial: Learn Regular Expressions from Scratch*](/blog/regex-tutorial).

```python
# Python 3.6+: variable-length lookbehind works
re.search(r'(?<=foo+)bar', 'foooobar')  # Works in Python 3.6+

# JavaScript ES2018+: also supports variable-length lookbehind
```

**Performance:** Lookaheads and lookbehinds can cause backtracking in complex patterns. Keep them simple and specific.

Test lookahead and lookbehind patterns at [regexbuilder.io](/).
