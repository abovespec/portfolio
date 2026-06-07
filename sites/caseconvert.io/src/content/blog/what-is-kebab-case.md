---
title: "What Is kebab-case? Where It's Used and Why It Matters"
description: "kebab-case defined: the name origin, where it's required (CSS, HTML, URLs, npm), and why JavaScript variables can't use it. Includes conversion examples."
publishDate: 2026-06-07
updatedDate: 2026-06-07
author: "Editorial Team"
tags: ["kebab case", "naming conventions", "css", "html", "urls"]
draft: false
---

kebab-case is a naming style that writes multi-word identifiers in all lowercase with hyphens between words:

```
first-name
user-account-id
background-color
max-retry-count
```

## Where the name comes from

The name is a visual joke. Imagine words as chunks of meat skewered on a hyphen — like a shish kebab. Each word is threaded onto the dash that connects them. It's a memorable way to distinguish hyphens from underscores when talking about naming styles.

Alternative names for the same convention include **hyphen-case**, **lisp-case** (because Lisp dialects used it for symbolic identifiers), and **spinal-case** (a less common term you'll see in some CSS tooling docs).

## Where kebab-case is the standard

### CSS class names and selectors

CSS is the most common place most developers encounter kebab-case. Class names, IDs, and custom property names all use it by convention:

```css
/* Class names */
.user-profile { }
.nav-link { }
.card-header { }

/* CSS custom properties (variables) */
:root {
  --color-primary: #3b82f6;
  --font-size-base: 1rem;
  --border-radius-sm: 4px;
  --spacing-lg: 2rem;
}

/* Using a custom property */
.button {
  background-color: var(--color-primary);
  border-radius: var(--border-radius-sm);
}
```

CSS parsers are case-insensitive for class names, and hyphens are valid in identifiers (but cannot be a variable or operator). Using kebab-case in CSS is idiomatic and universal.

### HTML attributes and custom element names

HTML attributes are case-insensitive, and kebab-case has long been the convention for multi-word attribute names. It is the required format for custom HTML element names (Web Components):

```html
<!-- Data attributes use kebab-case -->
<div
  data-user-id="42"
  data-account-type="premium"
  aria-label="User profile card"
></div>

<!-- Custom elements must use kebab-case (required by the spec) -->
<user-profile-card user-id="42"></user-profile-card>
<nav-menu is-open="true"></nav-menu>
```

The Web Components specification explicitly requires custom element names to contain a hyphen. This prevents naming collisions with existing and future standard HTML elements.

### URL slugs and route paths

kebab-case is the dominant convention for URL slugs and REST API paths:

```
/blog/what-is-kebab-case
/docs/getting-started
/api/v1/user-accounts
/products/noise-cancelling-headphones
```

Search engines (Google included) treat hyphens in URLs as word separators for indexing purposes. A slug like `what-is-kebab-case` is correctly parsed as four words: "what", "is", "kebab", "case". Underscores are not treated as word separators in URLs, which is one reason SEO guidance recommends kebab-case slugs over snake_case.

### npm package names

npm packages use kebab-case almost universally:

```bash
npm install react-router-dom
npm install date-fns
npm install lodash-es
npm install @tanstack/react-query
```

The npm registry is case-insensitive, and the community standard is lowercase kebab-case. Scoped packages (`@scope/package-name`) follow the same rule.

### CLI flags and options

Command-line tools commonly use kebab-case for multi-word flags:

```bash
git commit --allow-empty --no-verify
docker build --no-cache --build-arg NODE_VERSION=20
node --max-old-space-size=4096
prettier --trailing-comma=all --single-quote
```

### JSON keys in some API conventions

Some REST API conventions use kebab-case for JSON response keys, particularly the JSON:API specification:

```json
{
  "data": {
    "type": "articles",
    "attributes": {
      "article-title": "What Is kebab-case?",
      "created-at": "2026-06-07T00:00:00Z",
      "word-count": 1200
    }
  }
}
```

That said, camelCase is more common for JSON keys in general REST practice, especially from JavaScript or Node.js backends. snake_case is common from Python or Ruby backends. kebab-case in JSON bodies is a specific JSON:API-influenced choice, not a universal REST convention.

## Why JavaScript variables CANNOT use kebab-case

This is the most important limitation of kebab-case: **the hyphen is the subtraction operator in JavaScript** (and most other programming languages). A parser reading `user-name` interprets it as the variable `user` minus the variable `name`, not as an identifier.

```javascript
// This is NOT a variable named user-name
// It is: (user) - (name) — subtraction!
const user-name = "Alice";   // SyntaxError: Unexpected token '-'

// You must use camelCase or snake_case for variables
const userName = "Alice";    // camelCase — correct
const user_name = "Alice";   // snake_case — also valid
```

The same limitation applies in Python, Ruby, Go, Java, Rust, and virtually every language where `-` is an arithmetic operator. Lisp-family languages (Common Lisp, Clojure, Scheme) are notable exceptions — they allow hyphens in identifiers because they use a prefix syntax that doesn't have infix operators in the same way.

## Converting other cases to kebab-case

**From camelCase or PascalCase:**

Split on capital letters, lowercase everything, join with hyphens:
- `firstName` → `first-name`
- `getUserById` → `get-user-by-id`
- `UserAccount` → `user-account`
- `isActiveAccount` → `is-active-account`

**From snake_case:**

Replace underscores with hyphens:
- `first_name` → `first-name`
- `get_user_by_id` → `get-user-by-id`
- `max_retry_count` → `max-retry-count`

## kebab-case in JSX and React

In React's JSX syntax, HTML attributes follow the DOM property names (camelCase), but CSS class names still use kebab-case as strings:

```jsx
// className takes a string — kebab-case class names are fine
function UserCard({ isActive }) {
  return (
    <div
      className={`user-card ${isActive ? "user-card--active" : ""}`}
      data-user-type="premium"
      aria-label="User profile card"
    >
      <h2 className="user-card__name">Alice</h2>
    </div>
  );
}

// But JSX props (not HTML attrs) are camelCase
<input
  onChange={handleChange}    // camelCase JSX prop
  autoComplete="off"         // camelCase JSX prop
  className="text-input"     // but still kebab-case class string
/>
```

## Quick reference: where to use kebab-case

| Context | Use kebab-case? | Example |
|---------|-----------------|---------|
| CSS class names | Yes | `.nav-link` |
| CSS custom properties | Yes | `--color-primary` |
| HTML data attributes | Yes | `data-user-id` |
| URL slugs | Yes | `/blog/my-article` |
| npm package names | Yes | `react-query` |
| CLI flags | Yes | `--no-cache` |
| JavaScript variables | No (syntax error) | use `userName` |
| Python variables | No (syntax error) | use `user_name` |
| JSON keys (general REST) | Rarely | prefer `camelCase` or `snake_case` |

## Convert kebab-case instantly

Need to convert between kebab-case, camelCase, snake_case, or PascalCase? The [caseconvert.io](/) converter handles all major naming styles — paste any identifier or a block of text and get the converted output in one step.
