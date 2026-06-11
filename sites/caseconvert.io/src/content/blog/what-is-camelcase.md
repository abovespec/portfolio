---
title: "What Is camelCase? Definition, Rules, and Usage Guide"
description: "camelCase explained: lower vs upper camelCase, which languages use it, common mistakes like getHTTPRequest, and how to convert to and from it."
publishDate: 2026-06-07
updatedDate: 2026-06-07
author: "Editorial Team"
tags: ["camelcase", "naming conventions", "javascript", "java", "programming style"]
draft: false
heroImage: "/images/blog/what-is-camelcase-hero.png"
---

camelCase is a naming style that writes multi-word identifiers without spaces, capitalizing the first letter of every word after the first:

```
firstName
getUserById
isActiveAccount
maxRetryCount
```

The name comes from the capital letters in the middle of words — they look like the humps of a camel.

## Lower camelCase vs upper camelCase (PascalCase)

There are two closely related variants, and the distinction matters:

**Lower camelCase** (usually just called "camelCase") starts with a lowercase letter:

```
firstName
getUserById
accountBalance
```

**Upper camelCase**, also called **PascalCase**, starts with an uppercase letter:

```
FirstName
GetUserById
AccountBalance
```

In everyday usage, "camelCase" almost always means lower camelCase. When someone says "use PascalCase for classes," they are referring to upper camelCase with a specific name. The term PascalCase was popularized by the Pascal programming language and its descendants, particularly the .NET/C# world.

For more on the relationship between these two styles, see [*camelCase vs snake_case: Which Should You Use?*](/blog/camelcase-vs-snake-case).

## Which languages use camelCase?

camelCase is the default for variables, functions, and methods in a wide range of languages:

**JavaScript and TypeScript**

The most common language where you encounter camelCase daily. Variables, function names, method names, and object properties all follow lower camelCase. Classes use PascalCase.

```javascript
// Variables
const firstName = "Alice";
let isLoggedIn = false;

// Functions
function getUserById(userId) { }
const formatCurrency = (amount) => { };

// Object properties
const user = {
  firstName: "Alice",
  lastLogin: new Date(),
};

// Classes use PascalCase
class UserAccount { }
```

**Java**

Java has followed camelCase conventions since its earliest days. Fields, local variables, and methods are lower camelCase; class names are PascalCase; constants use UPPER_SNAKE_CASE.

```java
public class UserAccount {
    private String firstName;
    private int maxRetryCount = 3;

    public String getFirstName() {
        return firstName;
    }

    public boolean isAccountActive() {
        return this.active;
    }
}
```

**C#**

C# uses camelCase for private fields and local variables, PascalCase for public properties and methods. This split is codified in Microsoft's official .NET naming guidelines.

```csharp
public class UserAccount
{
    private string firstName;           // camelCase private field
    public string FirstName { get; }    // PascalCase public property

    public bool IsActive()              // PascalCase public method
    {
        int retryCount = 0;             // camelCase local variable
        return retryCount == 0;
    }
}
```

**Swift**

Swift documentation and the Swift API Design Guidelines explicitly recommend lower camelCase for variables, constants, and functions, and upper camelCase (PascalCase) for types.

```swift
let firstName = "Alice"
var isLoggedIn = false

func getUserById(userId: Int) -> User { }

struct UserAccount { }  // PascalCase for types
```

**Kotlin**

Kotlin follows the same pattern as Java. Functions and properties use camelCase; classes and objects use PascalCase.

```kotlin
val firstName = "Alice"
var isActiveAccount = true

fun getUserById(userId: Int): User { }

class UserAccount(val firstName: String)
```

## Why camelCase exists

Programming identifiers cannot contain spaces. The early alternative was to run words together (`getfirstname`) or use underscores (`get_first_name`). camelCase emerged as a readable compromise that doesn't require a separator character — the capital letters act as visual word boundaries.

In languages like Java, where verbose, descriptive names are the norm (`convertUserInputToUpperCaseStringWithTrim`), camelCase remains the only practical way to write readable multi-word names without a visual delimiter.

## How to read camelCase aloud

When reading or discussing camelCase identifiers, you split on the capital letters:

- `getUserById` → "get user by id"
- `isActiveAccount` → "is active account"
- `maxRetryCount` → "max retry count"

Some teams say the full name as a phrase: "get user by ID." Some read the capital letter names explicitly: "camel capital G, capital U, capital B, capital I." In practice, experienced developers just say the full phrase naturally.

## Converting human language to camelCase

To convert a plain English phrase to camelCase:

1. Split the phrase into words
2. Lowercase all letters
3. Capitalize the first letter of every word except the first
4. Join with no separator

Example:
- "user account balance" → `userAccountBalance`
- "get active users" → `getActiveUsers`
- "maximum retry count" → `maxRetryCount`
- "is valid email address" → `isValidEmailAddress`

## Common mistake: consecutive capitals (getHTTPRequest vs getHttpRequest)

One of the most debated camelCase questions is how to handle acronyms and abbreviations. Consider the identifier that accesses an HTTP request. Two conventions exist:

**All-caps acronym style:**
```
getHTTPRequest
parseXMLDocument
loadHTMLContent
```

**camelCase-normalized acronym style:**
```
getHttpRequest
parseXmlDocument
loadHtmlContent
```

The second style (normalizing acronyms to title-case) is now widely preferred because consecutive all-caps letters make word boundaries ambiguous. `getHTTPSRedirectURL` is much harder to parse than `getHttpsRedirectUrl`.

Google's Java Style Guide and most modern JavaScript linters recommend treating acronyms as ordinary words:

```javascript
// Preferred
function getHttpRequest() { }
function parseXmlDocument() { }
const htmlContent = "";

// Avoid (harder to scan)
function getHTTPRequest() { }
function parseXMLDocument() { }
const HTMLContent = "";
```

The main exception is two-letter acronyms used at the start of an identifier, where many guides still allow all-caps: `ioStream`, `dbConnection`. But even these are increasingly written as `iostream`, `dbConnection`.

## camelCase rules at a glance

| Rule | Example |
|------|---------|
| First word is entirely lowercase | `firstName` not `FirstName` |
| Every subsequent word starts with a capital | `getUserById` not `getuserId` |
| No separators between words | `maxRetryCount` not `max_Retry_Count` |
| Acronyms treated as words | `getHttpRequest` not `getHTTPRequest` |
| Numbers allowed | `getUser2Factor` is valid |

## camelCase vs other naming styles

| Style | Example | Primary use |
|-------|---------|-------------|
| camelCase | `firstName` | JS/TS/Java variables and functions |
| PascalCase | `FirstName` | Classes and types in most languages |
| snake_case | `first_name` | Python, Ruby, Rust, SQL |
| UPPER_SNAKE | `FIRST_NAME` | Constants, environment variables |
| kebab-case | `first-name` | CSS, HTML, URLs |

## Converting between camelCase and other styles

If you're working across a JavaScript frontend and a Python backend, you'll regularly need to convert between camelCase and snake_case. The [caseconvert.io](/) converter handles all five major naming styles — paste a block of identifiers and get the converted output in one step.
