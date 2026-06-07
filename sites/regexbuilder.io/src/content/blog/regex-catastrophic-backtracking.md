---
title: "Catastrophic Backtracking in Regex: What It Is and How to Prevent It"
description: "Learn what catastrophic backtracking is, why nested quantifiers cause exponential time complexity, real ReDoS incidents, and how to write safe regex patterns."
publishDate: 2026-06-07
updatedDate: 2026-06-07
author: "Editorial Team"
tags: ["regex", "backtracking", "redos", "performance", "security"]
draft: false
---

A regular expression that takes milliseconds on short strings can hang indefinitely on slightly longer input. This isn't a bug in your code — it's a fundamental property of how most regex engines work, and it can be exploited to cause denial-of-service attacks. Understanding catastrophic backtracking is essential for anyone writing regex that processes untrusted input.

## How NFA Regex Engines Work

Most programming language regex engines (Python, JavaScript, Java, Ruby, PHP, Perl) use **Non-deterministic Finite Automaton (NFA)** engines, specifically the backtracking variant.

When an NFA engine tries to match a pattern, it:
1. Tries to match the first part of the pattern
2. If it gets stuck, **backtracks** to try alternative paths
3. Repeats until it finds a match or exhausts all possibilities

For most patterns, backtracking is fast because there are few alternatives to try. The problem arises when patterns allow an **exponential number of alternatives**.

## The Classic Example: Nested Quantifiers

Consider matching this pattern against the string "aaaaaaaab":

```
(a+)+
```

This pattern says: "one or more 'a' characters, grouped, one or more times."

For the string "aaaa" (4 a's), the engine can decompose the match in many ways:
- One group: ["aaaa"]
- Two groups: ["aaa", "a"], ["aa", "aa"], ["a", "aaa"]
- Three groups: ["aa", "a", "a"], ["a", "aa", "a"], ["a", "a", "aa"]
- Four groups: ["a", "a", "a", "a"]

That's already 8 ways. For n characters, there are 2^(n-1) ways to partition them.

Now add a `b` that can't be matched — `(a+)+b` against "aaaaaaaaaa" (10 a's with no b). The engine tries every possible grouping, finds none of them lead to a match, and must exhaust all 2^9 = 512 paths before giving up. With 20 a's: 2^19 = 524,288 paths. With 30 a's: 2^29 ≈ 537 million paths.

**That's catastrophic backtracking.** The time complexity is exponential in the length of the input.

## Real-World ReDoS Incidents

Regex Denial of Service (ReDoS) attacks exploit this vulnerability against systems that process untrusted input.

### The Cloudflare Outage (2019)

On July 2, 2019, a new WAF (Web Application Firewall) rule containing a backtracking-prone regex caused Cloudflare's firewall software to consume 100% CPU across their infrastructure worldwide. The regex that caused it:

```
(?:(?:\"|'|\]|\}|\\|\d|(?:nan|infinity|true|false|null|undefined|symbol|math)
|\`|\-|\+)+[)]*;?((?:\s|-|~|!|\{\}|\|\||\+)*.*(?:.*=.*)))
```

This pattern — intended to detect SQL injection — contained nested quantifiers that backtracked catastrophically on certain inputs. The fix took 27 minutes. Cloudflare's outage report was published and is still available.

### Stack Overflow (2016)

A user pasted a very long string into Stack Overflow's post editor, which processed it with a regex containing `^[^\n]*$` — initially safe — but elsewhere in their markdown processor, a pattern like `(.|\n)*` caused catastrophic backtracking. The site's servers became unresponsive.

### email-validator npm Package (2019)

A popular Node.js email validation package contained a vulnerable regex. An attacker could send a malicious email address to any application using this package and cause the validation to take seconds or minutes per request.

## Identifying Vulnerable Patterns

Catastrophic backtracking typically involves:

1. **Nested quantifiers**: `(a+)+`, `(a*)*`, `(a+)*`
2. **Alternation with overlap**: `(a|a)*`, `(ab|a)(b|ab)*`
3. **Overlapping character classes**: `([a-z]+[\d]+)+`

**Safe patterns:**
```
a+b         — no backtracking: either matches or doesn't
[a-z]+      — simple quantifier on atomic unit
```

**Dangerous patterns:**
```
(a+)+b      — nested quantifiers
(a|aa)+b    — overlapping alternation
(\w+\s+)+   — word + space repeated
```

A rough heuristic: if you can divide the matched portion of a string in multiple ways and still satisfy the pattern, backtracking grows non-linearly.

## Mitigation Strategies

### 1. Rewrite the Pattern

Often, dangerous patterns can be rewritten to eliminate ambiguity:

```
# Dangerous
(a+)+b

# Safe equivalent — use possessive or atomic group
(?>a+)+b    # atomic group (PCRE, Java)
a++b        # possessive quantifier (PCRE, Java)
```

In JavaScript (which lacks atomic groups and possessive quantifiers), you need to restructure the logic itself:

```javascript
// Dangerous pattern for "word word word..."
/(\w+\s+)+$/

// Safe alternative — avoid repetition of groups containing quantifiers
/^\w+(\s+\w+)*$/
```

### 2. Use Possessive Quantifiers (PCRE, Java)

Possessive quantifiers (`++`, `*+`, `?+`) never backtrack — once they consume characters, those characters are not available for the rest of the pattern to try.

```
a++         — possessive: grabs all a's, won't give any back
```

Available in: PCRE, Java, PHP. **Not available in**: JavaScript, Python standard `re`.

### 3. Use Atomic Groups (PCRE, Java)

Atomic groups `(?>...)` prevent backtracking into the group once it's matched.

```
(?>a+)      — matches one or more a's, atomically
(?>a+)+b    — safe version of (a+)+b
```

Available in: PCRE, Java, .NET. **Not available in**: JavaScript, Python `re` (available in Python `regex` third-party module).

### 4. Use Python's `regex` Module

The third-party `regex` module for Python supports possessive quantifiers and atomic groups, unlike the built-in `re`:

```python
import regex
pattern = regex.compile(r'(?>a+)+b')
```

### 5. Input Length Limits

Even without rewriting patterns, limiting input length limits exposure. If email addresses are capped at 254 characters (the RFC 5321 maximum), an email validation regex can only backtrack on 254 characters maximum — making exponential complexity more manageable.

### 6. Timeout Settings

Some platforms let you set a regex execution timeout:

```python
import signal

def timeout_handler(signum, frame):
    raise TimeoutError("Regex timed out")

signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(2)  # 2 second timeout
try:
    result = re.match(pattern, input_string)
finally:
    signal.alarm(0)
```

JavaScript doesn't have native timeout support, but you can run regex in a Worker thread with a timeout.

### 7. Use a ReDoS Linter

- **vuln-regex-detector**: scans patterns for ReDoS vulnerability
- **safe-regex** (npm): checks if a regex is safe
- **eslint-plugin-regexp**: includes ReDoS detection rules

## Testing Patterns for Safety

Before deploying any regex that processes user input:

1. Test it against long strings of almost-matching input (e.g., `"a".repeat(50) + "b"`)
2. Time the execution for different input lengths
3. If execution time grows super-linearly with input length, the pattern is vulnerable
4. Use [regexbuilder.io](/) to test patterns interactively against various inputs

The rule: any regex that operates on untrusted input should be audited for catastrophic backtracking. The attack vector is real, the incidents are documented, and the fix is usually straightforward once you know what to look for.
