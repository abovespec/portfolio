---
title: "camelCase vs snake_case: Which Should You Use?"
description: "An honest comparison of camelCase and snake_case: how they work, which languages prefer which, and when to pick one over the other."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["naming conventions", "camelcase", "snake case", "programming style", "code style"]
draft: false
---

Naming conventions seem like a minor detail until you're in a code review arguing about `userId` vs `user_id`. The good news: this debate has mostly settled answers, and knowing them saves you the argument.

## What is camelCase?

camelCase writes multi-word identifiers by capitalizing the first letter of each word after the first, with no separators:

```
firstName
getUserById
isActiveAccount
maxRetryCount
```

The lowercase first variant (`firstName`) is called **lower camelCase** or just camelCase. The uppercase first variant (`FirstName`) is called **upper camelCase** or **PascalCase** — more on that distinction below.

The name comes from the humps formed by the capital letters in the middle of words.

## What is snake_case?

snake_case writes multi-word identifiers entirely in lowercase, separated by underscores:

For more on this topic, see [*What Is snake_case? A Practical Guide for Developers*](/blog/what-is-snake-case).

```
first_name
get_user_by_id
is_active_account
max_retry_count
```

The "snake" in the name refers to the low, flat profile of the text. A variant with all uppercase letters — `MAX_RETRY_COUNT` — is called **SCREAMING_SNAKE_CASE** or **UPPER_SNAKE_CASE**, and is standard for constants in many languages.

## Which languages use which?

Convention varies by language, and deviation from the norm reads as unidiomatic even if it's technically valid:

| Language | Variables/functions | Classes | Constants |
|----------|-------------------|---------|-----------|
| JavaScript / TypeScript | camelCase | PascalCase | UPPER_SNAKE |
| Python ([PEP 8](https://peps.python.org/pep-0008/)) | snake_case | PascalCase | UPPER_SNAKE |
| Ruby | snake_case | PascalCase | UPPER_SNAKE |
| Go | camelCase (unexported) / PascalCase (exported) | — | PascalCase |
| Java | camelCase | PascalCase | UPPER_SNAKE |
| C# | camelCase (private) / PascalCase (public) | PascalCase | PascalCase |
| Rust | snake_case | PascalCase | UPPER_SNAKE |
| PHP | camelCase or snake_case (mixed ecosystem) | PascalCase | UPPER_SNAKE |
| Swift | camelCase | PascalCase | camelCase |
| Kotlin | camelCase | PascalCase | UPPER_SNAKE |

For more on this topic, see [*camelCase to snake_case in JavaScript: Three Clean Solutions*](/blog/camelcase-to-snake-case-javascript).

**Rule of thumb:** Follow the convention of the language and its dominant frameworks. Consistency within a codebase matters more than cross-language uniformity.

## Where else do the conventions appear?

Beyond variable names, each style shows up in specific contexts:

**kebab-case** (hyphens instead of underscores) is the standard for:
- HTML attributes and custom element names
- CSS class names and custom properties (`--color-primary`)
- URL slugs and route paths (`/user-settings/security`)
- File names in web projects (`my-component.tsx`)

**snake_case** is standard for:
- Database column names (`created_at`, `user_id`)
- Python, Ruby, and Rust identifiers
- Environment variables (as UPPER_SNAKE: `DATABASE_URL`)
- JSON keys in some APIs (especially Python/Ruby backends)

**camelCase** is standard for:
- JavaScript and TypeScript identifiers
- Java and Swift identifiers
- JSON keys from JavaScript/Node.js backends
- GraphQL field names

## The readability argument

A common question: which is more readable?

Research on code readability is limited, but the most-cited study ([Bonita Sharif and Jonathan Maletic, 2010](https://www.cs.kent.edu/~jmaletic/papers/ICPC2010-camelstudy.pdf)) found that snake_case was faster to read when participants were unfamiliar with either style. However, the effect was small, and experienced programmers showed no meaningful difference.

In practice, readability comes from *consistency*, not the specific style. Code that mixes `getUserId`, `get_user_id`, and `GetUserId` in the same file is harder to scan than code that picks one and sticks with it.

## PascalCase — the third convention

Upper camelCase (PascalCase) is worth calling out separately because it's nearly universal for class names across languages:

```
class UserAccount {}        // Java, JS, TS, C#
class UserAccount:          # Python, Ruby
type UserAccount struct {}  // Go (exported)
struct UserAccount {}       // Rust
```

If your team debates `UserAccount` vs `user_account` for class names, the answer is almost always PascalCase regardless of language.

## When you have a choice

Some contexts — JSON API keys, configuration files, database schemas — don't have a hard language mandate. A few factors to weigh:

- **Who consumes the output?** If your API is consumed by JavaScript clients, camelCase keys save them a transformation step. If consumed by Python or Ruby, snake_case is more natural.
- **Are there existing conventions?** Extending an existing API or schema usually means matching it, even if you'd choose differently from scratch.
- **Tooling support?** ORM libraries, serializers, and linters often have default conventions. Going with the grain reduces configuration.

For more on this topic, see [*Naming Conventions in Programming: The Complete Guide*](/blog/naming-conventions-programming).

## Quick reference

| Style | Example | Common use |
|-------|---------|------------|
| camelCase | `firstName` | JS/TS/Java variables, JSON keys (JS) |
| PascalCase | `FirstName` | Classes everywhere, Go exported names |
| snake_case | `first_name` | Python/Ruby/Rust vars, DB columns |
| UPPER_SNAKE | `FIRST_NAME` | Constants, environment variables |
| kebab-case | `first-name` | URLs, CSS classes, HTML attributes |

## Convert between styles online

If you're migrating a codebase or working across language boundaries, the [caseconvert.io](/) converter handles all five styles and processes entire blocks of text at once.
