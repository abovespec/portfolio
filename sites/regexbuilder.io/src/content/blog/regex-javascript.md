---
title: "Regex in JavaScript: Complete Guide with Practical Examples"
description: "Learn JavaScript regex from literals to ES2018+ named groups, lookbehind, and unicode. Covers String and RegExp methods with working code examples."
publishDate: 2026-06-07
updatedDate: 2026-06-07
author: "Editorial Team"
tags: ["regex", "javascript", "javascript regex", "RegExp", "ES2018"]
draft: false
heroImage: "/images/blog/regex-javascript-hero.png"
---

JavaScript has native regular expression support built into the language. Regex literals, the `RegExp` constructor, and methods on `String` and `RegExp` objects give you a complete toolkit for matching, extracting, validating, and transforming text.

## Two ways to create a regex

### Regex literals

The most common form. The pattern sits between forward slashes and flags follow the closing slash.

```javascript
const pattern = /hello/gi;
```

Regex literals are compiled at parse time — they're fast and the preferred choice when the pattern is known at write time.

### The RegExp constructor

Use `RegExp` when you need to build patterns dynamically from variables.

```javascript
const keyword = 'hello';
const pattern = new RegExp(keyword, 'gi');

// Building a pattern from user input — always escape it first
function escapeRegex(str) {
  return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}
const safePattern = new RegExp(escapeRegex(userInput), 'i');
```

## RegExp methods

### test — check for a match

`test` returns `true` or `false`. It's the fastest way to check if a pattern exists in a string.

```javascript
const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

emailPattern.test('user@example.com');   // true
emailPattern.test('not-an-email');       // false
```

### exec — detailed single match

`exec` returns a match array with index and input properties, or `null`. With the `g` flag, it advances an internal pointer on each call, letting you iterate through all matches.

```javascript
const pattern = /(\d+)/g;
const str = 'ports: 80, 443, 8080';
let match;

while ((match = pattern.exec(str)) !== null) {
  console.log(`Found ${match[1]} at index ${match.index}`);
}
// Found 80 at index 7
// Found 443 at index 11
// Found 8080 at index 16
```

Note: `exec` with the `g` flag mutates the regex object's `lastIndex`. Use a `while` loop as shown above, or use `matchAll` instead.

## String methods that accept regex

### match — find matches

Without the `g` flag, `match` returns the first match with capturing groups (like `exec`). With `g`, it returns an array of all matched strings (no group detail).

```javascript
const str = 'Color: #ff5733 and #1a2b3c';

// Without g — first match with groups
str.match(/#([0-9a-f]{6})/i);
// ['#ff5733', 'ff5733', index: 7, ...]

// With g — all matches as strings
str.match(/#[0-9a-f]{6}/gi);
// ['#ff5733', '#1a2b3c']
```

### matchAll — iterate all matches with groups

`matchAll` requires the `g` flag and returns an iterator of match objects, each including full capturing group detail.

```javascript
const str = 'key1=value1&key2=value2&key3=value3';
const pattern = /(\w+)=(\w+)/g;

for (const match of str.matchAll(pattern)) {
  console.log(`${match[1]} = ${match[2]}`);
}
// key1 = value1
// key2 = value2
// key3 = value3
```

### replace and replaceAll

`replace` substitutes the first match by default. With the `g` flag (or using `replaceAll`), it substitutes all matches.

**Backreferences in replacement strings:** `$1`, `$2`, ... refer to capturing groups.

```javascript
// Reformat date from YYYY-MM-DD to DD/MM/YYYY
'2026-06-07'.replace(/(\d{4})-(\d{2})-(\d{2})/, '$3/$2/$1');
// '07/06/2026'

// Replace all whitespace runs with a single space
'too   many   spaces'.replace(/\s+/g, ' ');
// 'too many spaces'

// Callable replacement — receives the match object
const result = '42 and 7'.replace(/\d+/g, (match) => Number(match) * 2);
console.log(result);  // '84 and 14'
```

**Special replacement patterns:**

| Pattern | Replacement inserts |
|---------|---------------------|
| `$$` | Literal `$` |
| `$&` | Entire matched substring |
| `` $` `` | String before the match |
| `$'` | String after the match |
| `$n` | nth capturing group |
| `$<name>` | Named capturing group |

```javascript
// Wrap every number in <strong> tags
'I have 42 cats'.replace(/\d+/g, '<strong>$&</strong>');
// 'I have <strong>42</strong> cats'
```

### search — find match index

`search` returns the index of the first match, or `-1` if not found. Unlike `indexOf`, it accepts a regex.

```javascript
'hello world 123'.search(/\d+/);   // 12
'hello world'.search(/\d+/);       // -1
```

### split — split on a pattern

```javascript
'one,  two;  three | four'.split(/[,;|]\s*/);
// ['one', ' two', ' three ', 'four']

// Split on separator but keep the delimiter via capturing group
'2026-06-07'.split(/(-)/);
// ['2026', '-', '06', '-', '07']
```

## Flags

| Flag | Meaning |
|------|---------|
| `g` | Global — find all matches, not just the first |
| `i` | Case-insensitive |
| `m` | Multiline — `^` and `$` match line starts/ends |
| `s` | Dotall — `.` matches newlines (ES2018+) |
| `u` | Unicode — enables full Unicode matching and `\u{HHHH}` escapes |
| `d` | Indices — match objects include `.indices` with start/end pairs (ES2022+) |
| `v` | Unicode sets mode — extended Unicode class expressions (ES2024+) |

```javascript
// g + i — find all words case-insensitively
'Cat cat CAT'.match(/cat/gi);   // ['Cat', 'cat', 'CAT']

// m — ^ matches start of each line
const text = 'first\nsecond\nthird';
text.match(/^\w+/gm);           // ['first', 'second', 'third']

// s — dot matches newlines
/<div>(.*?)<\/div>/s.exec('<div>\nhello\n</div>')[1];
// '\nhello\n'
```

## Named capture groups (ES2018+)

Named groups use `(?<name>...)` syntax and are accessible via `match.groups`.

```javascript
const datePattern = /(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2})/;
const match = '2026-06-07'.match(datePattern);

console.log(match.groups.year);   // '2026'
console.log(match.groups.month);  // '06'
console.log(match.groups.day);    // '07'

// Named backreference in replacement with $<name>
'2026-06-07'.replace(datePattern, '$<day>/$<month>/$<year>');
// '07/06/2026'
```

```javascript
// Parsing a log entry
const logPattern = /(?<ip>\d{1,3}(?:\.\d{1,3}){3})\s+- -\s+\[(?<date>[^\]]+)\]\s+"(?<method>\w+)\s+(?<path>\S+)/;

const log = '10.0.0.1 - - [07/Jun/2026:12:00:00] "GET /api/data HTTP/1.1"';
const { groups } = log.match(logPattern);

console.log(groups.ip);     // '10.0.0.1'
console.log(groups.method); // 'GET'
console.log(groups.path);   // '/api/data'
```

## Lookbehind assertions (ES2018+)

JavaScript gained lookbehind support in ES2018. Positive `(?<=...)` and negative `(?<!...)` assertions are now available in all modern browsers.

```javascript
// Positive lookbehind — match number after $
'Price: $42.99'.match(/(?<=\$)\d+\.\d{2}/);  // ['42.99']

// Negative lookbehind — match digits NOT after a letter
'code42 and 7 items'.match(/(?<![a-z])\d+/gi);  // ['7']

// Extract query parameter values
'?id=42&page=3'.match(/(?<=id=)\d+/);  // ['42']
```

## Unicode support with the u flag

The `u` flag enables full Unicode awareness and unlocks `\u{HHHH}` code point escapes.

```javascript
// Without u — '.' doesn't match astral plane characters
/^.$/.test('😀');    // false (surrogate pair issue)

// With u — '.' matches any Unicode code point
/^.$/u.test('😀');   // true

// Unicode property escapes (requires u flag)
/\p{Script=Greek}/u.test('α');     // true
/\p{Emoji}/u.test('😀');           // true
/\p{Lu}/u.test('A');               // true (uppercase letter)

// Match any letter from any language
'Héllo wörld'.match(/\p{L}+/gu);   // ['Héllo', 'wörld']
```

## Practical examples

### URL parser

```javascript
const urlPattern = /(?<protocol>https?):\/\/(?<host>[^\/\s]+)(?<path>\/[^\s?#]*)?(?:\?(?<query>[^\s#]*))?(?:#(?<hash>\S*))?/u;

const url = 'https://api.example.com/v1/users?limit=10&page=2#results';
const { groups } = url.match(urlPattern);

console.log(groups.protocol);  // 'https'
console.log(groups.host);      // 'api.example.com'
console.log(groups.path);      // '/v1/users'
console.log(groups.query);     // 'limit=10&page=2'
console.log(groups.hash);      // 'results'
```

### Form input validation

```javascript
const validators = {
  email: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/,
  username: /^[a-zA-Z0-9_]{3,20}$/,
  zipCode: /^\d{5}(-\d{4})?$/,
  hexColor: /^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$/,
};

function validate(field, value) {
  return validators[field]?.test(value) ?? false;
}

console.log(validate('email', 'user@example.com'));    // true
console.log(validate('username', 'alice_42'));         // true
console.log(validate('hexColor', '#ff5733'));          // true
console.log(validate('zipCode', '90210-1234'));        // true
```

### Highlight search terms in HTML

```javascript
function highlightTerms(text, terms) {
  const escaped = terms.map(t => t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'));
  const pattern = new RegExp(`(${escaped.join('|')})`, 'gi');
  return text.replace(pattern, '<mark>$1</mark>');
}

highlightTerms('The quick brown fox', ['quick', 'fox']);
// 'The <mark>quick</mark> brown <mark>fox</mark>'
```

### Tokenizing a simple expression

```javascript
const tokenPattern = /(?<number>\d+(?:\.\d+)?)|(?<op>[+\-*/])|(?<space>\s+)/g;
const expr = '3.14 + 2 * 10';

for (const { groups } of expr.matchAll(tokenPattern)) {
  if (groups.number) console.log('NUM:', groups.number);
  else if (groups.op) console.log('OP:', groups.op);
}
// NUM: 3.14
// OP: +
// NUM: 2
// OP: *
// NUM: 10
```

## Common pitfalls

**The sticky `lastIndex` bug:** When you reuse a regex with the `g` flag, `lastIndex` persists between calls. Either reset `pattern.lastIndex = 0` before each new search, or create a new regex each time. This is why `matchAll` is generally safer than `exec` in a loop.

**String `match` with `g` drops group detail:** If you need both all matches and their capturing groups, use `matchAll` instead of `match(/pattern/g)`.

**`u` flag breaks invalid patterns:** Adding `u` enables stricter parsing — patterns that silently worked before may throw a `SyntaxError`. Fix escaping issues revealed by the flag.

Test your JavaScript regex patterns interactively at [regexbuilder.io](/).
