---
title: "What Is snake_case? A Practical Guide for Developers"
description: "snake_case explained: how it works, where it's used, and why Python, Ruby, and databases default to it. Includes comparison with camelCase and kebab-case."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["snake case", "naming conventions", "programming style", "python", "databases"]
draft: false
---

snake_case is a naming style that writes multi-word identifiers entirely in lowercase, with underscores between words:

```
user_id
first_name
get_user_by_id
max_retry_count
is_active
```

The name comes from the visual: the underscores make text look like it's slithering along the ground like a snake.

## What makes a valid snake_case identifier?

- All letters are lowercase
- Words are separated by single underscores
- No spaces, hyphens, or capital letters
- Numbers are allowed anywhere: `user_v2`, `http_200_response`
- Leading underscores are a convention for "private" in Python: `_internal_func`
- Double leading underscores invoke name mangling in Python classes: `__private`

These are not snake_case:
```
First_Name    ← capital letter
user-id       ← hyphen, not underscore (that's kebab-case)
userID        ← camelCase, no underscore
User_ID       ← mixed case
```

## Where snake_case is the standard

**Python** — [PEP 8](https://peps.python.org/pep-0008/), the official Python style guide, mandates snake_case for all function names, method names, and variables:

For more on this topic, see [*Naming Conventions in Programming: The Complete Guide*](/blog/naming-conventions-programming).

```python
def get_user_by_id(user_id: int) -> User:
    ...

max_connections = 10
is_authenticated = False
```

Classes use PascalCase; constants use UPPER_SNAKE_CASE.

**Ruby** — Ruby follows the same convention: methods and variables are snake_case, classes are PascalCase:

```ruby
def send_welcome_email(user_id)
  ...
end

active_users = User.where(active: true)
```

**Rust** — Rust enforces snake_case at the compiler level. A variable named `myVar` triggers a warning; `my_var` is correct:

```rust
fn get_user_by_id(user_id: u64) -> User {
    ...
}

let max_retry_count = 3;
```

**SQL and database columns** — snake_case is the dominant convention for column and table names across PostgreSQL, MySQL, and SQLite:

```sql
CREATE TABLE user_accounts (
    user_id       SERIAL PRIMARY KEY,
    first_name    TEXT NOT NULL,
    last_name     TEXT NOT NULL,
    created_at    TIMESTAMPTZ DEFAULT NOW()
);
```

Some ORMs (Django, ActiveRecord) generate snake_case column names automatically from PascalCase model names.

**Environment variables** — UPPER_SNAKE_CASE (a variant) is the standard for environment variable names:

```bash
DATABASE_URL=postgres://localhost/mydb
SECRET_KEY=abc123
MAX_CONNECTIONS=20
```

## Where snake_case is *not* the standard

- **JavaScript/TypeScript** — camelCase for variables, PascalCase for classes
- **Java** — camelCase for variables and methods, PascalCase for classes
- **Go** — camelCase for unexported names, PascalCase for exported
- **CSS** — kebab-case for class names and custom properties
- **URL paths** — kebab-case (`/user-settings`) is preferred over snake_case

For more on this topic, see [*camelCase vs snake_case: Which Should You Use?*](/blog/camelcase-vs-snake-case).

## snake_case vs camelCase vs kebab-case

| Style | Example | Standard use |
|-------|---------|--------------|
| snake_case | `user_id` | Python, Ruby, Rust, SQL |
| camelCase | `userId` | JavaScript, TypeScript, Java |
| PascalCase | `UserId` | Classes in most languages |
| UPPER_SNAKE | `USER_ID` | Constants, environment variables |
| kebab-case | `user-id` | CSS, HTML, URLs |

For more on this topic, see [*camelCase to snake_case in Python: Four Approaches*](/blog/camelcase-to-snake-case-python).

The distinction matters at API boundaries. A Python backend that exposes `user_id` and a JavaScript frontend that expects `userId` need explicit conversion — either in the serializer or the client. Libraries like `humps` (Python) or `change-case` (JavaScript) handle this.

## Why Python chose snake_case

Guido van Rossum's original rationale (captured in PEP 8 and various Python mailing list posts) was that snake_case reads more like natural English, particularly for longer identifiers. `get_user_by_id` parses as four distinct words; `getUserById` requires training your eye to find the word boundaries.

It's partly a historical accident: Python emerged in a Unix/C context where underscored identifiers were common. JavaScript emerged from a Java/ECMAScript context where camelCase was already the norm.

## UPPER_SNAKE_CASE for constants

When you want a constant in Python, Ruby, or Rust, the convention is snake_case with all letters uppercased:

```python
MAX_CONNECTIONS = 100
DEFAULT_TIMEOUT = 30
API_BASE_URL = "https://api.example.com"
```

In Python, UPPER_SNAKE doesn't technically prevent mutation (unlike `const` in JavaScript), but the convention signals intent to other developers.

## Convert between styles

Working across a Python backend and a JavaScript frontend? The [caseconvert.io](/) tool converts identifiers between snake_case, camelCase, PascalCase, and kebab-case — paste a block of identifiers and get the converted output instantly.
