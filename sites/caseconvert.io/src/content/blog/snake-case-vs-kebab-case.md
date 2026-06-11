---
title: "snake_case vs kebab-case: Key Differences and When to Use Each"
description: "snake_case vs kebab-case compared: the underscore vs hyphen difference, which contexts prefer each, why JavaScript can't use kebab-case, and how to choose."
publishDate: 2026-06-07
updatedDate: 2026-06-07
author: "Editorial Team"
tags: ["snake case", "kebab case", "naming conventions", "css", "python"]
draft: false
heroImage: "/images/blog/snake-case-vs-kebab-case-hero.png"
---

snake_case and kebab-case look nearly identical — both are lowercase, both separate words — but the single difference between them (underscore vs hyphen) determines where each one can appear.

```
snake_case:   user_account_id       get_user_by_id      max_retry_count
kebab-case:   user-account-id       get-user-by-id      max-retry-count
```

## The key difference: underscore vs hyphen

The functional difference between the two styles is not aesthetic — it's **syntactic**.

- **Underscore (`_`)** is a valid identifier character in virtually every programming language. `user_id` is a single token, a complete variable name.
- **Hyphen (`-`)** is the subtraction operator in most programming languages. `user-id` is three tokens: `user`, `-`, `id` — interpreted as subtraction.

This is why kebab-case cannot be used for variable names in JavaScript, Python, Ruby, Java, Go, Rust, or C. Hyphens are arithmetic operators.

```javascript
// JavaScript: hyphen is subtraction
const user-name = "Alice";    // SyntaxError
const user_name = "Alice";    // snake_case — valid
const userName = "Alice";     // camelCase — valid

// Python: same issue
user-name = "Alice"           # SyntaxError
user_name = "Alice"           # snake_case — valid
```

The languages where kebab-case IS valid for identifiers are Lisp-family languages (Common Lisp, Clojure, Scheme, Racket), which use prefix notation that avoids infix arithmetic operators.

## Where snake_case is the standard

**Python** — PEP 8 mandates snake_case for all function names, method names, and variable names:

```python
def get_user_by_id(user_id: int) -> dict:
    max_retries = 3
    is_found = False
    return {"user_id": user_id, "is_found": is_found}
```

For a complete PEP 8 naming guide, see [*Python Naming Conventions: The Complete PEP 8 Guide*](/blog/python-naming-conventions-pep8).

**Ruby and Rails** — Methods and variables are snake_case, and Rails generates snake_case database column names from PascalCase model names:

```ruby
def send_welcome_email(user_id)
  user = User.find(user_id)
  UserMailer.welcome_email(user).deliver_later
end

# Rails model attributes
user.first_name
user.created_at
user.account_balance
```

**Rust** — Rust enforces snake_case at the compiler level. Using camelCase for a variable name generates a compiler warning:

```rust
fn get_user_by_id(user_id: u64) -> Option<User> {
    let max_retry_count = 3;
    database::find_user(user_id, max_retry_count)
}
```

**SQL and database columns** — snake_case is the near-universal convention for column and table names in PostgreSQL, MySQL, and SQLite:

```sql
CREATE TABLE user_accounts (
    user_id       SERIAL PRIMARY KEY,
    first_name    TEXT NOT NULL,
    last_name     TEXT NOT NULL,
    created_at    TIMESTAMPTZ DEFAULT NOW(),
    is_active     BOOLEAN DEFAULT TRUE
);
```

**Filesystem and configuration** — Many systems use snake_case for file and directory names, particularly in Python projects and configuration files:

```
config/
  database_settings.yaml
  logging_config.yaml

src/
  user_service.py
  email_helpers.py
```

## Where kebab-case is the standard

**CSS class names and custom properties** — kebab-case is universal in CSS:

```css
/* Class names */
.user-profile { }
.nav-menu-item { }
.card-header { }

/* Custom properties */
:root {
  --color-primary: #3b82f6;
  --spacing-md: 1rem;
  --border-radius-base: 4px;
}
```

For more on kebab-case, see [*What Is kebab-case?*](/blog/what-is-kebab-case).

**HTML attributes** — HTML attributes conventionally use kebab-case for multi-word names:

```html
<div
  data-user-id="42"
  data-account-type="premium"
  aria-label="User profile"
  aria-expanded="false"
></div>
```

**URL slugs and REST API paths** — kebab-case is the dominant URL convention, preferred by most SEO guidance and REST API design guides:

```
/api/v1/user-accounts
/blog/snake-case-vs-kebab-case
/docs/getting-started
/products/noise-cancelling-headphones
```

Search engines treat hyphens as word separators for indexing. Underscores are not treated as word separators in URLs, giving kebab-case an SEO advantage for slug content.

**npm package names** — nearly all npm packages use kebab-case:

```bash
npm install react-router-dom
npm install date-fns
npm install @tanstack/react-query
```

**CLI flags** — command-line tools use kebab-case for multi-word flags:

```bash
git commit --allow-empty
docker build --no-cache --build-arg VERSION=1.0
prettier --trailing-comma=all
```

## JSON API conventions: both are used

JSON keys don't have a single universal convention. The choice typically follows the backend language:

**snake_case from Python/Ruby backends:**

```json
{
  "user_id": 42,
  "first_name": "Alice",
  "created_at": "2026-06-07T12:00:00Z",
  "is_active": true
}
```

**camelCase from JavaScript/Node.js backends:**

```json
{
  "userId": 42,
  "firstName": "Alice",
  "createdAt": "2026-06-07T12:00:00Z",
  "isActive": true
}
```

**kebab-case from JSON:API spec:**

```json
{
  "data": {
    "attributes": {
      "first-name": "Alice",
      "created-at": "2026-06-07T12:00:00Z"
    }
  }
}
```

In practice, snake_case and camelCase dominate the JSON API space. kebab-case JSON keys are relatively rare outside JSON:API-compliant services.

## Mixing contexts: Python backend + JavaScript frontend

One of the most common real-world scenarios involves a Python backend returning snake_case JSON and a JavaScript frontend that prefers camelCase. This creates a translation problem at the API boundary.

Several approaches handle it:

**Option 1: Convert in the Python serializer**

Django REST Framework, FastAPI with Pydantic, and similar tools can serialize snake_case Python fields to camelCase JSON automatically:

```python
# FastAPI with alias_generator
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

class UserResponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    user_id: int
    first_name: str
    is_active: bool

# Serializes to: {"userId": 42, "firstName": "Alice", "isActive": true}
```

**Option 2: Convert in the JavaScript client**

Libraries like `humps` (JS) convert object keys between cases:

```javascript
import { camelizeKeys, decamelizeKeys } from "humps";

// API response: { user_id: 42, first_name: "Alice" }
const data = await fetch("/api/users/42").then(r => r.json());
const camelized = camelizeKeys(data);
// camelized: { userId: 42, firstName: "Alice" }

// Request body: need to send snake_case
const body = decamelizeKeys({ userId: 42, firstName: "Alice" });
// body: { user_id: 42, first_name: "Alice" }
```

**Option 3: Accept snake_case in JavaScript**

Some teams accept snake_case everywhere, including the JavaScript frontend, to avoid the translation layer. This is simpler but feels unidiomatic in JS.

## Which to choose for new projects

| Decision | Recommendation |
|----------|---------------|
| Python backend identifiers | snake_case (PEP 8 mandate) |
| JavaScript/TypeScript identifiers | camelCase (community standard) |
| CSS class names | kebab-case (universal CSS convention) |
| URL slugs | kebab-case (SEO and readability) |
| REST API URL paths | kebab-case |
| JSON keys (JS/Node.js backend) | camelCase |
| JSON keys (Python/Ruby backend) | snake_case or camelCase (consistent) |
| Database column names | snake_case (SQL standard) |
| Environment variables | UPPER_SNAKE_CASE |
| npm package names | kebab-case |
| CLI flags | kebab-case |

The most important rule: **be consistent within a context**. A REST API that uses snake_case for some endpoints and camelCase for others is worse than either choice applied uniformly.

## Comparison at a glance

| Property | snake_case | kebab-case |
|----------|-----------|------------|
| Separator | Underscore `_` | Hyphen `-` |
| Valid JS identifier? | Yes | No (syntax error) |
| Valid Python identifier? | Yes | No (syntax error) |
| Valid CSS identifier? | Yes (but unconventional) | Yes (standard) |
| Valid in URLs? | Yes (but SEO-disadvantaged) | Yes (preferred) |
| Primary use | Python, Ruby, Rust, SQL, env vars | CSS, HTML, URLs, CLI, npm |

## Convert between styles

Need to convert between snake_case, kebab-case, camelCase, or PascalCase? The [caseconvert.io](/) converter handles all major naming styles — paste any identifier or a block of text and convert instantly.
