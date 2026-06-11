---
title: "JavaScript Naming Conventions: The Complete Style Guide"
description: "JavaScript naming conventions for variables, classes, constants, booleans, private members, files, and CSS classes in JSX. Covers Airbnb, Google, and StandardJS guides."
publishDate: 2026-06-07
updatedDate: 2026-06-07
author: "Editorial Team"
tags: ["javascript", "naming conventions", "camelcase", "programming style", "code style"]
draft: false
heroImage: "/images/blog/javascript-naming-conventions-hero.png"
---

JavaScript's naming conventions are enforced by community style guides rather than the language spec. The interpreter accepts almost any identifier, so the rules are social contracts — and violating them is jarring to other developers who read your code.

This guide covers the community-standard conventions for every identifier type in JavaScript and TypeScript, plus notes on where the major style guides agree or differ.

For related naming convention guides, see [*Naming Conventions in Programming: The Complete Guide*](/blog/naming-conventions-programming).

## Variables and functions: camelCase

Variables, function names, and function parameters all use **lower camelCase**:

```javascript
// Variables
const firstName = "Alice";
let isLoggedIn = false;
var accountBalance = 1500;

// Function declarations
function getUserById(userId) {
  return users.find(u => u.id === userId);
}

// Arrow functions
const formatCurrency = (amount, currency = "USD") => {
  return new Intl.NumberFormat("en-US", { style: "currency", currency }).format(amount);
};

// Function parameters
function createUser(firstName, lastName, emailAddress) {
  return { firstName, lastName, emailAddress };
}
```

For more on camelCase itself, see [*What Is camelCase?*](/blog/what-is-camelcase).

## Classes and constructors: PascalCase

Classes and constructor functions use **PascalCase** (upper camelCase). This convention is a signal that the function is intended to be called with `new`:

```javascript
// ES6 classes
class UserAccount {
  constructor(firstName, lastName) {
    this.firstName = firstName;
    this.lastName = lastName;
  }

  getFullName() {
    return `${this.firstName} ${this.lastName}`;
  }
}

// Constructor functions (pre-ES6 pattern)
function HttpClient(baseUrl) {
  this.baseUrl = baseUrl;
}

// Instantiation
const user = new UserAccount("Alice", "Smith");
const client = new HttpClient("https://api.example.com");
```

React components are a practical application of this rule: component names must start with a capital letter so React knows to treat them as components rather than HTML tags.

```jsx
// PascalCase — React treats this as a component
function UserProfileCard({ user }) {
  return <div className="user-profile-card">{user.name}</div>;
}

// Lowercase — React treats this as a native HTML element
// <userprofilecard /> → no such HTML element, renders nothing useful
```

## Constants: UPPER_SNAKE_CASE for module-level values

Module-level values that are truly constant — never reassigned during program execution — use **UPPER_SNAKE_CASE**:

```javascript
// Module-level constants
const MAX_RETRY_COUNT = 3;
const DEFAULT_TIMEOUT_MS = 5000;
const API_BASE_URL = "https://api.example.com/v1";
const SUPPORTED_CURRENCIES = ["USD", "EUR", "GBP"];

// Configuration objects
const DB_CONFIG = {
  host: "localhost",
  port: 5432,
  database: "myapp",
};
```

The convention applies to `const` declarations that are semantically constants — not just any `const`. A `const` that holds a mutable object (like an array or object literal) is technically not immutable, but the UPPER_SNAKE name signals that the reference itself won't be reassigned.

Local variables inside functions use camelCase even when declared `const`, because they aren't module-level constants:

```javascript
function calculateTax(price, taxRate) {
  const taxAmount = price * taxRate;   // camelCase, not TAX_AMOUNT
  const totalPrice = price + taxAmount;
  return totalPrice;
}
```

## Private class members

JavaScript now has native private class fields using the `#` prefix:

```javascript
class BankAccount {
  #balance;           // truly private — inaccessible outside class
  #accountNumber;

  constructor(initialBalance) {
    this.#balance = initialBalance;
    this.#accountNumber = Math.random().toString(36).slice(2);
  }

  deposit(amount) {
    if (amount <= 0) throw new Error("Amount must be positive");
    this.#balance += amount;
  }

  get balance() {
    return this.#balance;
  }
}

const account = new BankAccount(1000);
account.#balance;  // SyntaxError: Private field '#balance' must be declared in an enclosing class
```

Before native private fields, the conventional signal for "this is private" was a leading underscore:

```javascript
class LegacyService {
  constructor() {
    this._cache = new Map();   // conventional private — technically accessible
    this._baseUrl = "https://api.example.com";
  }

  _fetchFromCache(key) {
    return this._cache.get(key);
  }
}
```

The `_underscore` convention is still common in older codebases and transpiled TypeScript. For new code, prefer `#privateFields` when your target environment supports them (all modern browsers and Node.js 12+).

## Boolean naming: is, has, can, should

Boolean variables and functions that return booleans benefit from a verb prefix that makes `if` statements read like natural language:

```javascript
// "is" prefix — state or condition
const isActive = true;
const isLoggedIn = false;
const isEmpty = list.length === 0;

function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// "has" prefix — possession or membership
const hasPermission = user.roles.includes("admin");
const hasErrors = errors.length > 0;

function hasActiveSubscription(userId) {
  return subscriptions.some(s => s.userId === userId && s.active);
}

// "can" prefix — capability or permission
const canEdit = user.role === "editor" || user.role === "admin";
const canSubmit = isFormValid && !isSubmitting;

// "should" prefix — suggestion or conditional behavior
const shouldRefetch = staleDuration > MAX_STALE_MS;
const shouldRedirect = !isAuthenticated && isProtectedRoute;
```

Reading a well-named boolean in an `if` statement should feel like reading English:

```javascript
if (isLoggedIn && hasPermission && canEdit) {
  showEditButton();
}

if (isEmpty) {
  renderEmptyState();
}
```

## CSS class names in JSX: kebab-case strings

This is a common source of confusion. JSX *props* use camelCase (`className`, `onClick`, `htmlFor`), but the CSS class name *values* inside those props are still kebab-case strings, because they map to CSS rules:

```jsx
// JSX props are camelCase
<div
  className="user-profile-card"
  onClick={handleClick}
  htmlFor="email-input"
>

// Dynamic class names — the class strings are still kebab-case
function Button({ variant = "primary", isDisabled = false }) {
  return (
    <button
      className={[
        "btn",
        `btn--${variant}`,
        isDisabled ? "btn--disabled" : "",
      ].join(" ")}
      disabled={isDisabled}
    >
      Click me
    </button>
  );
}
```

Libraries like `clsx` and `classnames` make this more ergonomic, but the underlying CSS class names remain kebab-case.

For more on kebab-case, see [*What Is kebab-case?*](/blog/what-is-kebab-case).

## File naming conventions

There is no single universal standard for JavaScript file names, but two patterns dominate:

**kebab-case files** — common for utilities, modules, and configuration:

```
user-service.js
format-currency.js
api-client.js
date-utils.js
webpack.config.js
```

**PascalCase files** — common for React components, Vue single-file components, and class-based modules:

```
UserProfileCard.jsx
NavigationMenu.tsx
ShoppingCart.vue
HttpClient.js
```

Many projects use both: PascalCase for component files and kebab-case for everything else. The key is to be consistent within the project. Most linters and build tools can enforce either convention.

## TypeScript-specific conventions

TypeScript adds interfaces and type aliases. Common conventions:

```typescript
// Interfaces: PascalCase, no "I" prefix (modern convention)
interface UserAccount {
  id: number;
  firstName: string;
  email: string;
}

// Some older codebases use "I" prefix (Microsoft/C# influence)
interface IUserAccount { }   // less common in modern TS

// Type aliases: PascalCase
type UserId = string;
type ApiResponse<T> = {
  data: T;
  error: string | null;
};

// Enums: PascalCase enum name, PascalCase or UPPER_SNAKE members
enum UserRole {
  Admin = "ADMIN",
  Editor = "EDITOR",
  Viewer = "VIEWER",
}
```

## Major style guides compared

Three style guides dominate JavaScript naming conversations:

**Airbnb JavaScript Style Guide**
- Variables and functions: camelCase
- Classes: PascalCase
- Constants: UPPER_SNAKE for true module-level constants
- Requires `const` by default, `let` for reassignment, no `var`
- Filename: PascalCase for React components, camelCase otherwise

**Google JavaScript Style Guide**
- Variables and functions: camelCase
- Classes: PascalCase
- Constants: UPPER_SNAKE
- Also covers TypeScript conventions explicitly
- Requires descriptive names; abbreviations generally discouraged

**StandardJS**
- Variables and functions: camelCase
- Classes: PascalCase
- No semicolons (this is a formatting rule, but part of the "standard")
- Less prescriptive about constants — camelCase `const` is fine

The three guides agree on the core conventions: camelCase variables, PascalCase classes. The differences are in edge cases, formatting preferences, and `const` usage.

## Quick reference

| Identifier type | Convention | Example |
|----------------|------------|---------|
| Variable | camelCase | `firstName`, `isActive` |
| Function | camelCase | `getUserById()` |
| Parameter | camelCase | `function f(userId)` |
| Class | PascalCase | `UserAccount` |
| Constructor function | PascalCase | `function HttpClient()` |
| Module-level constant | UPPER_SNAKE | `MAX_RETRY_COUNT` |
| Private field (native) | `#camelCase` | `#balance` |
| Private field (convention) | `_camelCase` | `_cache` |
| Boolean variable | `is/has/can + camelCase` | `isActive`, `hasErrors` |
| CSS class (string) | kebab-case | `"user-profile-card"` |
| React component file | PascalCase | `UserCard.jsx` |
| Utility/module file | kebab-case | `format-date.js` |
| Interface (TypeScript) | PascalCase | `UserAccount` |
| Type alias (TypeScript) | PascalCase | `UserId` |
| Enum (TypeScript) | PascalCase | `UserRole` |

## Convert between JavaScript naming styles

Working across a JavaScript frontend and a Python backend means translating between camelCase (JavaScript) and snake_case (Python) constantly. The [caseconvert.io](/) converter handles all five major naming styles — paste a block of identifiers and get the converted output in one click.
