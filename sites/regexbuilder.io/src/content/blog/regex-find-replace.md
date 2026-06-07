---
title: "Regex Find and Replace: VS Code, sed, Python, and JavaScript"
description: "Master regex find and replace in VS Code, sed, grep, Perl, JavaScript, and Python. Learn capture group backreferences and callable replacements."
publishDate: 2026-06-07
updatedDate: 2026-06-07
author: "Editorial Team"
tags: ["regex", "find and replace", "sed", "python", "javascript", "VS Code"]
draft: false
---

Find and replace with regex is one of the most powerful text-processing techniques a developer can master. Once you learn how to use capture groups in replacement strings, you can reformat dates, restructure data, rename patterns, and transform entire files in seconds rather than hours.

## The concept: capture and reuse

The key to powerful regex substitution is the combination of **capture groups** and **backreferences**. You capture parts of the matched text in groups (parentheses), then refer to those groups in the replacement string.

```
Pattern:  (\d{4})-(\d{2})-(\d{2})
Input:    2026-06-07
Groups:   $1=2026  $2=06  $3=07
Replace:  $3/$2/$1  →  07/06/2026
```

Different tools use different backreference syntax, but the concept is identical across all of them.

## VS Code

VS Code's built-in search (`Ctrl+H` / `Cmd+H`) supports regex mode. Click the `.*` icon in the search bar to enable it.

### Using capture groups in VS Code

Replacement strings use `$1`, `$2`, `$3`, ... for capture groups.

**Example: swap first and last name**

```
Search:  (\w+)\s+(\w+)
Replace: $2, $1
```

`John Smith` becomes `Smith, John`.

**Example: reformat ISO dates to US format**

```
Search:  (\d{4})-(\d{2})-(\d{2})
Replace: $2/$3/$1
```

`2026-06-07` becomes `06/07/2026`.

**Example: add quotes around bare JSON values**

```
Search:  :\s*(\w+)$
Replace: : "$1"
```

`"key": value` becomes `"key": "value"`.

### VS Code regex tips

- Use `$0` to insert the entire match in the replacement string.
- Hold `Ctrl+Alt+Enter` (or `Cmd+Option+Enter`) to replace all occurrences.
- Use `(?i)` at the start of the search pattern (or toggle the case-sensitive button) for case-insensitive matching.
- Multiline mode is always on in VS Code's regex search — `^` and `$` match line boundaries.

## Command line: sed

`sed` is the standard Unix stream editor. Its substitution syntax is `s/pattern/replacement/flags`.

### Basic sed substitution

```bash
# Replace first occurrence on each line
echo "hello hello" | sed 's/hello/world/'
# world hello

# Replace all occurrences (g flag)
echo "hello hello" | sed 's/hello/world/g'
# world world

# Case-insensitive (I flag — GNU sed only)
echo "Hello HELLO hello" | sed 's/hello/world/gI'
# world world world
```

### Backreferences in sed

sed uses `\1`, `\2`, ... for backreferences. Capture groups are `\(...\)` in basic regex (BRE) or `(...)` with `-E` for extended regex (ERE).

```bash
# Reformat date YYYY-MM-DD to DD/MM/YYYY (ERE with -E)
echo "Date: 2026-06-07" | sed -E 's/([0-9]{4})-([0-9]{2})-([0-9]{2})/\3\/\2\/\1/'
# Date: 07/06/2026

# Swap first and last name in a CSV column
echo "John,Smith,42" | sed -E 's/^([^,]+),([^,]+)/\2,\1/'
# Smith,John,42

# Add http:// prefix to bare domains
echo "example.com" | sed -E 's/^([a-z0-9.-]+\.[a-z]{2,})$/http:\/\/\1/'
# http://example.com
```

### sed in-place file editing

```bash
# Edit file in place (creates backup .bak)
sed -i.bak -E 's/foo/bar/g' file.txt

# Edit in place without backup (GNU sed)
sed -i 's/foo/bar/g' file.txt

# Process multiple files
sed -i -E 's/localhost/production.example.com/g' config/*.yaml
```

### Multiline operations with sed

```bash
# Delete blank lines
sed '/^$/d' file.txt

# Remove trailing whitespace from every line
sed -E 's/[[:space:]]+$//' file.txt
```

## Command line: grep

`grep` is for finding, not replacing. But it's useful for previewing what your pattern will match before you commit to a substitution.

```bash
# Show lines matching a pattern
grep -E '\d{4}-\d{2}-\d{2}' logfile.txt

# Show only the matched text (not full lines)
grep -oE '\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b' access.log

# Count matches per file
grep -cE 'ERROR|CRITICAL' *.log
```

## Command line: Perl

`perl -pe` is the most powerful one-liner option, with full PCRE support including lookaheads, named groups, and complex replacement logic.

```bash
# Perl one-liner — same as sed but with PCRE
perl -pe 's/(\d{4})-(\d{2})-(\d{2})/$3\/$2\/$1/g' dates.txt

# Named groups in Perl
perl -pe 's/(?<y>\d{4})-(?<m>\d{2})-(?<d>\d{2})/$+{d}\/$+{m}\/$+{y}/g' dates.txt

# Complex replacement with code block
perl -pe 's/\d+/sprintf("%05d", $&)/ge' ids.txt
# Pads every number to 5 digits: 42 → 00042
```

## Python: re.sub

Python's `re.sub(pattern, replacement, string)` supports both string replacements (with `\1`, `\2` backreferences) and callable replacements.

### String replacement with backreferences

```python
import re

# Reformat date
result = re.sub(r'(\d{4})-(\d{2})-(\d{2})', r'\3/\2/\1', '2026-06-07')
print(result)  # '07/06/2026'

# Named groups with \g<name>
result = re.sub(
    r'(?P<last>\w+),\s*(?P<first>\w+)',
    r'\g<first> \g<last>',
    'Smith, John'
)
print(result)  # 'John Smith'

# Wrap all numbers in brackets
result = re.sub(r'(\d+)', r'[\1]', 'I have 42 cats and 7 dogs')
print(result)  # 'I have [42] cats and [7] dogs'
```

### Callable replacement — the most powerful option

Pass a function as the replacement argument. The function receives the match object and returns the replacement string.

```python
import re

# Double every number
def double(m):
    return str(int(m.group()) * 2)

result = re.sub(r'\d+', double, 'I have 3 cats and 5 dogs')
print(result)  # 'I have 6 cats and 10 dogs'

# Normalize inconsistent date formats to ISO 8601
def normalize_date(m):
    month_map = {
        'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04',
        'may': '05', 'jun': '06', 'jul': '07', 'aug': '08',
        'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'
    }
    day = m.group('day').zfill(2)
    month = month_map[m.group('month').lower()]
    year = m.group('year')
    return f'{year}-{month}-{day}'

date_pattern = re.compile(
    r'(?P<day>\d{1,2})\s+(?P<month>[A-Za-z]{3})\s+(?P<year>\d{4})',
    re.IGNORECASE
)

text = 'Events on 7 Jun 2026 and 15 Dec 2026'
print(date_pattern.sub(normalize_date, text))
# 'Events on 2026-06-07 and 2026-12-15'
```

### Processing files with re.sub

```python
import re

def process_file(path: str):
    with open(path, 'r') as f:
        content = f.read()

    # Replace all TODO comments with FIXME
    content = re.sub(r'#\s*TODO:', '# FIXME:', content)

    # Normalize multiple blank lines to one
    content = re.sub(r'\n{3,}', '\n\n', content)

    # Convert camelCase variable names to snake_case
    content = re.sub(r'([a-z])([A-Z])', lambda m: f'{m.group(1)}_{m.group(2).lower()}', content)

    with open(path, 'w') as f:
        f.write(content)
```

## JavaScript: String.replace with regex

### Backreferences in replacement strings

JavaScript uses `$1`, `$2`, ... and `$<name>` for named groups.

```javascript
// Reformat date
'2026-06-07'.replace(/(\d{4})-(\d{2})-(\d{2})/, '$3/$2/$1');
// '07/06/2026'

// Named groups
'Smith, John'.replace(/(?<last>\w+),\s*(?<first>\w+)/, '$<first> $<last>');
// 'John Smith'

// Global replace — insert the full match with $&
'42 and 100'.replace(/\d+/g, '[$&]');
// '[42] and [100]'
```

### Callable replacement in JavaScript

```javascript
// Double every number
'I have 3 cats and 5 dogs'.replace(/\d+/g, (match) => Number(match) * 2);
// 'I have 6 cats and 10 dogs'

// The replacement function signature: (match, p1, p2, ..., offset, string)
const result = 'first-second-third'.replace(
  /(\w+)-(\w+)/g,
  (match, p1, p2) => `${p2.toUpperCase()}_${p1.toUpperCase()}`
);
console.log(result);  // 'SECOND_FIRST-third'

// Capitalize first letter of each word
'hello world foo bar'.replace(/\b\w/g, (c) => c.toUpperCase());
// 'Hello World Foo Bar'
```

## Practical transformation examples

### Rename function parameters

```
Pattern:  function\s+(\w+)\s*\(\s*req\s*,\s*res\s*\)
Replace:  function $1(request, response)
```

### Convert hex colors to RGB

```python
import re

def hex_to_rgb(m):
    r = int(m.group(1), 16)
    g = int(m.group(2), 16)
    b = int(m.group(3), 16)
    return f'rgb({r}, {g}, {b})'

css = 'color: #ff5733; background: #1a2b3c;'
result = re.sub(r'#([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})', hex_to_rgb, css)
print(result)
# 'color: rgb(255, 87, 51); background: rgb(26, 43, 60);'
```

### Restructure CSV columns

```bash
# Move column 3 to column 1 in a CSV (columns: name,age,id)
# Input:  Alice,30,001
# Output: 001,Alice,30
sed -E 's/^([^,]+),([^,]+),([^,]+)$/\3,\1,\2/' data.csv
```

### Slugify URLs

```javascript
function slugify(title) {
  return title
    .toLowerCase()
    .replace(/[^\w\s-]/g, '')         // remove non-word chars
    .replace(/\s+/g, '-')             // spaces to hyphens
    .replace(/-{2,}/g, '-')           // collapse multiple hyphens
    .replace(/^-+|-+$/g, '');         // trim leading/trailing hyphens
}

slugify('Hello, World! This is a Test.');
// 'hello-world-this-is-a-test'
```

Build and verify your find-and-replace patterns interactively at [regexbuilder.io](/) before running them on production files.
