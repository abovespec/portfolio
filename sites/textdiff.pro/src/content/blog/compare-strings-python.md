---
title: "How to Compare Strings in Python"
description: "Python string comparison: equality, ordering, case-insensitive matching, fuzzy similarity, and difflib for line-by-line diffs. With examples."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["python", "strings", "comparison", "difflib", "text processing"]
draft: false
---

Python provides several ways to compare strings, from simple equality checks to fuzzy matching and line-by-line diffs. Here's the full picture.

## Equality and inequality

The `==` operator checks if two strings have the same characters in the same order:

```python
a = "hello"
b = "hello"
c = "world"

a == b    # True
a == c    # False
a != c    # True
```

Python strings are immutable, so `==` always compares by value (not by identity). The `is` operator checks identity and should *not* be used for string comparison:

```python
# Don't use `is` for string comparison
a = "hello"
b = "hel" + "lo"
a == b    # True (correct)
a is b    # May be True or False depending on string interning — unreliable
```

## Lexicographic ordering

Python compares strings lexicographically (dictionary order) using Unicode code points:

```python
"apple" < "banana"   # True
"apple" < "Apple"    # False — lowercase 'a' (97) > uppercase 'A' (65)
"abc" < "abcd"       # True — shorter string comes first if prefix matches
"z" > "a"            # True
```

This matters for sorting:

```python
words = ["banana", "apple", "Cherry"]
sorted(words)
# ['Cherry', 'apple', 'banana']  ← uppercase before lowercase

sorted(words, key=str.lower)
# ['apple', 'banana', 'Cherry']  ← case-insensitive sort
```

## Case-insensitive comparison

Use `.lower()` or `.casefold()`:

```python
a = "Hello"
b = "hello"

a.lower() == b.lower()    # True
a.casefold() == b.casefold()  # True
```

`.casefold()` is the more aggressive normalization — it handles non-ASCII comparisons (like the German "ß" → "ss") correctly. Prefer `.casefold()` for internationalized text.

## Comparing substrings

```python
text = "The quick brown fox"

# Contains
"quick" in text       # True
"slow" in text        # False

# Starts/ends with
text.startswith("The")   # True
text.endswith("fox")     # True

# Find position
text.find("brown")    # 10 (index of first match, -1 if not found)
text.index("brown")   # 10 (raises ValueError if not found)
```

## Normalized comparison

Before comparing strings from different sources, normalize whitespace and encoding:

```python
def normalize(s: str) -> str:
    import unicodedata
    # Normalize Unicode forms (NFC combines characters, NFD decomposes)
    s = unicodedata.normalize("NFC", s)
    # Collapse whitespace
    return " ".join(s.split())

normalize("hello   world") == normalize("hello world")  # True
```

## Fuzzy / similarity comparison with `difflib`

Python's standard library includes `difflib`, which provides several similarity metrics:

```python
from difflib import SequenceMatcher

def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()

similarity("hello world", "hello earth")  # 0.727...
similarity("hello", "hello")              # 1.0
similarity("hello", "world")              # 0.2
```

The ratio ranges from 0.0 (no match) to 1.0 (identical). Under the hood, `SequenceMatcher` uses a variant of the Myers diff algorithm.

For more on this topic, see [*How Does diff Work? The Algorithm Behind File Comparison*](/blog/how-does-diff-work).

`get_close_matches` is useful for fuzzy search:

```python
from difflib import get_close_matches

words = ["color", "colour", "colors", "flavour", "flavor"]
get_close_matches("colour", words, n=3, cutoff=0.6)
# ['colour', 'color', 'colors']
```

## Line-by-line diff with `difflib`

To get a diff between two multiline strings, `difflib` provides several formatters:

```python
import difflib

text1 = """line one
line two
old line three
line four
""".splitlines(keepends=True)

For more on this topic, see [*How to Compare Two Text Files in Linux*](/blog/compare-two-text-files-linux).

text2 = """line one
line two
new line three
line five
""".splitlines(keepends=True)

# Unified diff
diff = difflib.unified_diff(text1, text2, fromfile="original", tofile="modified")
print("".join(diff))
```

Output:
```diff
--- original
+++ modified
@@ -1,4 +1,4 @@
 line one
 line two
-old line three
-line four
+new line three
+line five
```

For more on this topic, see [*Myers Diff Algorithm: How git diff Finds Changes*](/blog/myers-diff-algorithm).

For an HTML-formatted diff:

```python
html = difflib.HtmlDiff().make_file(text1, text2, "original", "modified")
with open("diff.html", "w") as f:
    f.write(html)
```

## Regular expressions for pattern matching

For pattern-based comparison, use `re`:

```python
import re

# Check if string matches a pattern
re.match(r"^\d{4}-\d{2}-\d{2}$", "2026-04-25")  # matches (ISO date)
re.match(r"^\d{4}-\d{2}-\d{2}$", "not-a-date")   # None

# Case-insensitive match
re.match(r"hello", "Hello World", re.IGNORECASE)  # matches

# Find all occurrences
re.findall(r"\bword\b", "word wordsmith sword word", re.IGNORECASE)
# ['word', 'word']
```

## Quick summary

| Goal | Approach |
|------|----------|
| Exact equality | `a == b` |
| Case-insensitive | `a.casefold() == b.casefold()` |
| Lexicographic order | `<`, `>`, `<=`, `>=` |
| Substring check | `"sub" in s` |
| Fuzzy similarity score | `SequenceMatcher(None, a, b).ratio()` |
| Close matches | `difflib.get_close_matches()` |
| Line-by-line diff | `difflib.unified_diff()` |
| Pattern match | `re.match()` / `re.fullmatch()` |

## Online text diff

For comparing longer texts — documents, config files, code blocks — paste them into [textdiff.pro](/) for a visual diff with added and removed lines highlighted.
