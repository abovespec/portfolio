---
title: "UUID vs GUID: Are They the Same Thing?"
description: "Understand the difference between UUID and GUID: RFC 4122, Microsoft's GUID format, generation methods, case sensitivity, and when to use each term."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["uuid", "guid", "unique identifier", "microsoft", "rfc 4122"]
draft: false
---

UUID and GUID are both 128-bit unique identifiers with the same structure. The terms are often used interchangeably, but there are differences in origin, terminology, and some implementation details.

## The short answer

**UUID** (Universally Unique Identifier) is the standard term from RFC 4122 (IETF). **GUID** (Globally Unique Identifier) is Microsoft's term for the same concept. They're the same format — 128 bits, 32 hex digits, displayed in 8-4-4-4-12 format.

For more on this topic, see [*How to Generate a UUID: Online, CLI, Python, JavaScript, and SQL*](/blog/generate-uuid).

```
550e8400-e29b-41d4-a716-446655440000
```

When developers say "GUID," they're usually in a .NET/Windows context. "UUID" is the cross-platform standard term.

## Where GUID comes from

Microsoft adopted the UUID format from the Open Software Foundation (OSF) DCE standard in the early 1990s for COM (Component Object Model). They called it GUID. The same format was later standardized as UUID in RFC 4122 (2005).

For more on this topic, see [*What Is a UUID? Format, Versions, and How They Work*](/blog/what-is-a-uuid).

In .NET, you generate a GUID with:

```csharp
// C#
Guid guid = Guid.NewGuid();
Console.WriteLine(guid.ToString());
// "550e8400-e29b-41d4-a716-446655440000"

// Different formatting options
guid.ToString("D");  // 550e8400-e29b-41d4-a716-446655440000
guid.ToString("N");  // 550e8400e29b41d4a716446655440000
guid.ToString("B");  // {550e8400-e29b-41d4-a716-446655440000}
guid.ToString("P");  // (550e8400-e29b-41d4-a716-446655440000)
```

## Technical differences

**Generation:** Historically, Windows GUIDs were generated using a variant of UUID v1 with a different algorithm. Modern `Guid.NewGuid()` in .NET uses UUID v4 (random).

**Variant bits:** Standard RFC 4122 UUIDs have variant bits `10xx`, giving values 8, 9, a, or b for the first character of the 4th group. Old-style Microsoft GUIDs used variant bits `110x` (values c or d). You can see the difference in the 17th character:

For more on this topic, see [*How to Generate UUIDs in Python, JavaScript, Go, and SQL*](/blog/how-to-generate-uuid-code).

```
RFC 4122 UUID: 550e8400-e29b-41d4-a716-...  ← 'a' = variant 10xx
Old MS GUID:   550e8400-e29b-41d4-c716-...  ← 'c' = variant 110x
```

Modern .NET `Guid.NewGuid()` generates RFC 4122 variant UUIDs, so this distinction is largely historical.

**Case sensitivity:** RFC 4122 says UUIDs should be lowercase. GUIDs in Microsoft documentation are often shown uppercase:

```
UUID (standard): 550e8400-e29b-41d4-a716-446655440000
GUID (Microsoft): 550E8400-E29B-41D4-A716-446655440000
```

For comparison purposes, treat UUIDs as case-insensitive (both formats are equivalent). Store lowercase in databases.

## In code

**Python:**
```python
import uuid

# UUID v4 (random)
uid = uuid.uuid4()
print(str(uid))       # "550e8400-e29b-41d4-a716-446655440000"
print(uid.hex)        # "550e8400e29b41d4a716446655440000" (no hyphens)
print(int(uid))       # integer representation
```

**JavaScript:**
```javascript
// Node.js 19+ / Web Crypto API
const uid = crypto.randomUUID();
// "550e8400-e29b-41d4-a716-446655440000"

// Or use the uuid package (npm)
import { v4 as uuidv4 } from 'uuid';
const uid = uuidv4();
```

**C# (.NET):**
```csharp
Guid guid = Guid.NewGuid();         // Random v4
Guid parsed = Guid.Parse("550e8400-e29b-41d4-a716-446655440000");
bool isValid = Guid.TryParse(input, out Guid result);
```

**Go:**
```go
import "github.com/google/uuid"

id := uuid.New()       // v4
fmt.Println(id.String())
```

## Which term to use

Use **UUID** when:
- Writing cross-platform or language-agnostic documentation
- Working with databases, APIs, or open standards
- Using any non-Microsoft technology

Use **GUID** when:
- Working in a .NET or Windows environment
- Working with COM, DCOM, or ActiveX
- Following the conventions of an existing Microsoft-based codebase

In database columns and API responses, "uuid" is the standard type name:

```sql
-- PostgreSQL
user_id UUID DEFAULT gen_random_uuid()

-- MySQL 8.0+
user_id CHAR(36) DEFAULT (UUID())
```

## GUID braces format

Some Microsoft systems use curly braces:

```
{550E8400-E29B-41D4-A716-446655440000}
```

This is purely display convention — the braces are not part of the actual UUID value. Strip them when parsing or storing.

Generate UUIDs at [uuidgen.io](/).
