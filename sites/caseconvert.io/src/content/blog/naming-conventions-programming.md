---
title: "Naming Conventions in Programming: The Complete Guide"
description: "camelCase, snake_case, PascalCase, kebab-case — which applies where, and why it matters. Covers all major languages and contexts."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["naming conventions", "programming style", "code quality", "camelcase", "snake case"]
draft: false
---

Naming conventions are the unwritten rules that determine whether your code looks like it belongs in a codebase or was imported from a different language. Getting them right is part of professional software development — not pedantry.

This guide covers the five main styles, where each is standard, and the edge cases worth knowing.

## The five styles at a glance

| Style | Example | Pattern |
|-------|---------|---------|
| camelCase | `firstName` | Lower first word, capitalize subsequent words |
| PascalCase | `FirstName` | Capitalize every word, no separator |
| snake_case | `first_name` | All lowercase, underscore separator |
| UPPER_SNAKE | `FIRST_NAME` | All uppercase, underscore separator |
| kebab-case | `first-name` | All lowercase, hyphen separator |

## camelCase

camelCase is the dominant style in JavaScript, TypeScript, Java, Swift, and Kotlin for variable and function names.

```js
// JavaScript
const firstName = 'Alice';
function getUserById(userId) { ... }
const isActiveAccount = true;
```

```java
// Java
String firstName = "Alice";
public User getUserById(int userId) { ... }
boolean isActiveAccount = true;
```

When to use it:
- Variables and function/method names in JS, TS, Java, Swift, Kotlin
- JSON keys from JavaScript backends
- GraphQL field names
- Object properties in JS/TS

## PascalCase (Upper CamelCase)

PascalCase differs from camelCase only in that the first word is also capitalized. It's nearly universal for class and type names:

```python
class UserAccount:          # Python
    ...

class UserAccount { }       // Java, C#, JS/TS

type UserAccount struct { } // Go (also for exported functions)

struct UserAccount { }      // Rust
```

When to use it:
- Class names in every mainstream language
- TypeScript interfaces and type aliases
- React components (`<UserCard />`)
- Go exported functions and variables (`GetUser` vs `getUser`)
- C# public members

## snake_case

snake_case is the standard in Python, Ruby, Rust, and for database column names.

```python
# Python (PEP 8 mandated)
def get_user_by_id(user_id: int) -> User:
    max_retry_count = 3
    is_authenticated = False
```

```sql
-- SQL (conventional)
SELECT user_id, first_name, created_at
FROM user_accounts
WHERE is_active = TRUE;
```

When to use it:
- All identifiers in Python and Ruby
- Variables and functions in Rust
- Database table and column names
- API keys from Python/Ruby backends
- File names in Python projects (`my_module.py`)

## UPPER_SNAKE_CASE

UPPER_SNAKE is snake_case with all letters capitalized. It universally signals "constant" — something that should not be mutated:

```python
# Python
MAX_CONNECTIONS = 100
DATABASE_URL = "postgres://localhost/mydb"
SECRET_KEY = "abc123"
```

```bash
# Shell / environment variables
export DATABASE_URL="postgres://localhost/mydb"
export SECRET_KEY="abc123"
```

```js
// JavaScript (const + uppercase signals semantic constant)
const MAX_RETRY_COUNT = 3;
const API_BASE_URL = 'https://api.example.com';
```

When to use it:
- Named constants in Python, Ruby, Rust, C, C++
- Environment variable names (always)
- Enum values in some languages (Java, C# use PascalCase instead)

## kebab-case

kebab-case uses hyphens instead of underscores. It's the style for web-facing contexts where underscores have different semantics or lower readability:

```css
/* CSS */
.user-card { }
.is-active { }
--color-primary: #0070f3;
```

```html
<!-- HTML custom elements and attributes -->
<my-component data-user-id="42"></my-component>
```

```
/user-settings/security
/blog/how-to-format-json
```

When to use it:
- CSS class names and custom properties
- HTML attribute names (data-*, aria-*)
- URL slugs and route paths
- File names for web projects (`user-card.tsx`, `get-started.md`)
- npm package names (`lodash`, `change-case`, `react-dom`)
- CLI flags (`--dry-run`, `--output-file`)

kebab-case cannot be used as an identifier in most programming languages (the hyphen is a subtraction operator), so it's limited to contexts where identifiers are strings or paths.

## Language cheat sheet

| Language | Variables/Functions | Classes | Constants | Files |
|----------|-------------------|---------|-----------|-------|
| JavaScript | camelCase | PascalCase | UPPER_SNAKE | kebab-case |
| TypeScript | camelCase | PascalCase | UPPER_SNAKE | kebab-case |
| Python | snake_case | PascalCase | UPPER_SNAKE | snake_case |
| Ruby | snake_case | PascalCase | UPPER_SNAKE | snake_case |
| Java | camelCase | PascalCase | UPPER_SNAKE | PascalCase |
| C# | camelCase (private) | PascalCase | PascalCase | PascalCase |
| Go | camelCase / PascalCase | — | PascalCase | snake_case |
| Rust | snake_case | PascalCase | UPPER_SNAKE | snake_case |
| Swift | camelCase | PascalCase | camelCase | PascalCase |
| PHP | camelCase or snake_case | PascalCase | UPPER_SNAKE | PascalCase |
| CSS | kebab-case | — | — | kebab-case |
| SQL | snake_case | — | — | snake_case |

## Cross-boundary conversions

The most common source of bugs from naming conventions is at **serialization boundaries** — where your backend language meets your frontend, or where your app meets a database.

**Python backend + JavaScript frontend:**
- Python produces `user_id`, `first_name` (snake_case)
- JavaScript expects `userId`, `firstName` (camelCase)
- Solution: use a serializer alias (Pydantic's `alias_generator`, Django REST Framework's `CamelCaseJSONParser`) or transform in the client

**JavaScript API + PostgreSQL:**
- Postgres uses snake_case columns (`user_id`)
- JavaScript uses camelCase (`userId`)
- Solution: configure your ORM (Knex `camelizeKeys`, Prisma default camelCase mapping) to handle conversion automatically

**Go exported names + JSON:**
- Go exports `UserID` (PascalCase)
- JSON convention for JavaScript clients is `userId` (camelCase)
- Solution: `json:"userId"` struct tags

## Consistency over correctness

Within a codebase, consistency matters more than following conventions exactly. A Python project that's been using camelCase for five years should not switch halfway through. A new project should follow the language convention from day one.

Linters enforce this:
- ESLint `camelcase` rule for JavaScript
- `pylint` / `pycodestyle` for Python (enforces PEP 8)
- `golint` / `staticcheck` for Go
- `rustfmt` for Rust (formats but also catches naming warnings)
- `rubocop` for Ruby

## Convert between styles

Need to rename a block of identifiers from one style to another? The [caseconvert.io](/) converter handles camelCase, PascalCase, snake_case, UPPER_SNAKE, and kebab-case — paste your identifiers and get the output instantly.
