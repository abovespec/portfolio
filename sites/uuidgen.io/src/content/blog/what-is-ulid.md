---
title: "What Is a ULID? Universally Unique Lexicographically Sortable Identifiers Explained"
description: "Learn what ULIDs are, how their 48-bit timestamp + 80-bit random structure works, how they compare to UUID v7, and when to use them in JS, Python, and Go."
publishDate: 2026-06-07
updatedDate: 2026-06-07
author: "Editorial Team"
tags: ["ulid", "uuid", "unique identifier", "database", "distributed systems"]
draft: false
---

UUIDs have a well-known weakness as database primary keys: UUID v4 is entirely random, which means each new insert lands at a random position in the B-tree index. At millions of rows this causes significant fragmentation and write slowdowns. ULID was designed to solve this problem while keeping the distributed-generation and collision-resistance properties that make UUIDs attractive.

## The problem ULID solves

When you use a UUID v4 as a primary key, every insert is essentially random from the B-tree's perspective. The database must split index pages to fit new entries, creating fragmentation over time. On large tables, this translates to:

- Slower writes as the index tree becomes deeper and less cache-friendly
- Larger index sizes from fragmentation overhead
- More frequent maintenance (VACUUM, index rebuilds)

You also lose the ability to sort records by creation time using the primary key — you have to store a separate `created_at` column and index it independently.

ULID (Universally Unique Lexicographically Sortable Identifier) addresses both problems in a single identifier.

## ULID structure

A ULID is a 128-bit identifier, the same as a UUID. It consists of two components:

```
01ARZ3NDEKTSV4RRFFQ69G5FAV

├────────────┤├────────────────┤
  Timestamp       Randomness
  48 bits          80 bits
  10 chars         16 chars
```

**Timestamp component (48 bits / 10 chars):** The number of milliseconds since the Unix epoch (January 1, 1970). A 48-bit millisecond counter won't overflow until the year 10889 — well beyond any practical concern.

**Randomness component (80 bits / 16 chars):** Cryptographically random bits, providing collision resistance. With 80 random bits per millisecond, the probability of a collision within the same millisecond is approximately 1 in 10^24.

**Encoding:** ULID uses Crockford Base32, an encoding that:
- Avoids visually ambiguous characters (I, L, O, U)
- Is case-insensitive
- Sorts correctly as a plain string (lexicographic sort = chronological sort)
- Produces 26 characters, compared to UUID's 36

A ULID looks like this:

```
01ARZ3NDEKTSV4RRFFQ69G5FAV
```

Compare to a UUID:

```
550e8400-e29b-41d4-a716-446655440000
```

ULID is shorter (26 vs 36 characters), has no hyphens, and sorts in creation order.

## Lexicographic sorting

The key property of ULIDs is that alphabetical (lexicographic) sort order equals chronological order. This is because the timestamp component comes first and is encoded in a way that preserves sort order:

```javascript
const ids = [
  '01ARZ3NDEKTSV4RRFFQ69G5FAV',  // created first
  '01ARZ3NDEKTSV4RRFFQ69G5FAW',  // created ~same ms
  '01BXYZ0000000000000000000A',  // created much later
];

ids.sort();  // already in chronological order
```

This means you can sort a table by primary key and get records in creation order — no separate `created_at` index needed. This is the same property that makes UUID v7 attractive for databases.

## Monotonic ULIDs (same-millisecond ordering)

A basic ULID implementation generates a new random 80-bit component for every ULID, even within the same millisecond. This is fine for most use cases but means two ULIDs generated in the same millisecond are not guaranteed to sort in generation order.

**Monotonic ULID** mode solves this: if two ULIDs are generated within the same millisecond, the second one increments the randomness component of the first by 1 rather than generating fresh random bits:

```
01ARZ3NDEKTSV4RRFFQ69G5FAV  ← first in this ms
01ARZ3NDEKTSV4RRFFQ69G5FAW  ← second in this ms (incremented by 1)
01ARZ3NDEKTSV4RRFFQ69G5FAX  ← third in this ms (incremented by 1)
```

This guarantees strict monotonic ordering within a single process, even at microsecond-level generation rates. Most ULID libraries implement a monotonic factory option.

## ULID vs UUID v7

Both ULID and UUID v7 (standardized in RFC 9562, 2024) solve the same underlying problem: time-ordered, collision-resistant identifiers suitable for database primary keys. The differences are practical rather than fundamental.

| Property | ULID | UUID v7 |
|---------|------|---------|
| Length | 26 characters | 36 characters |
| Encoding | Crockford Base32 | Hexadecimal |
| Format | No hyphens | 8-4-4-4-12 with hyphens |
| Timestamp precision | Millisecond (48 bits) | Millisecond (48 bits) |
| Random bits | 80 bits | ~74 bits |
| Standardized | Informal spec | RFC 9562 (IETF) |
| Database native type | None (TEXT/VARCHAR) | UUID type in PostgreSQL, etc. |
| Library support | Good (most languages) | Growing rapidly |
| Case-sensitive | No (Base32 is case-insensitive) | Convention: lowercase |

**UUID v7 has a key advantage:** PostgreSQL, MySQL, and SQL Server have native UUID data types that store 16 bytes internally. A ULID stored as TEXT uses 26 bytes. For high-volume tables with many rows and foreign key references, this storage difference is significant.

**ULID has a key advantage:** The 26-character Base32 format is shorter and has no hyphens, which can be more ergonomic in URLs, log files, and user-facing contexts.

For a new application choosing between the two, UUID v7 is generally recommended because of its IETF standardization and native database type support. ULID is an excellent choice if you prefer its format or are working in an ecosystem with strong ULID library support.

For more on this topic, see [*UUID v4 vs v7: Which Should You Use?*](/blog/uuid-v4-vs-v7).

## Generating ULIDs in JavaScript

```javascript
// npm install ulid
import { ulid, monotonicFactory } from 'ulid';

// Basic ULID
const id = ulid();
// "01ARZ3NDEKTSV4RRFFQ69G5FAV"

// ULID with a specific timestamp
const withTime = ulid(Date.now());
// Uses current time as timestamp component

// Monotonic ULIDs (guaranteed ordering within a millisecond)
const monotonicUlid = monotonicFactory();
const id1 = monotonicUlid();
const id2 = monotonicUlid();  // always > id1, even in same ms

// Extract timestamp from a ULID
import { decodeTime } from 'ulid';
const timestamp = decodeTime(id);  // Unix ms timestamp
const date = new Date(timestamp);
```

## Generating ULIDs in Python

```python
# pip install python-ulid
from ulid import ULID

# Generate a new ULID
uid = ULID()
print(str(uid))          # "01ARZ3NDEKTSV4RRFFQ69G5FAV"
print(uid.timestamp())   # Unix timestamp in seconds (float)
print(uid.datetime)      # datetime object

# Parse an existing ULID string
parsed = ULID.from_str("01ARZ3NDEKTSV4RRFFQ69G5FAV")

# Convert to UUID format for database compatibility
print(uid.to_uuid())     # UUID object (same 128 bits, different representation)

# Storing in a database (as string or bytes)
ulid_str = str(uid)        # 26-char string
ulid_bytes = bytes(uid)    # 16 bytes (same as UUID binary storage)
```

## Generating ULIDs in Go

```go
// go get github.com/oklog/ulid/v2
package main

import (
    "fmt"
    "math/rand"
    "time"

    "github.com/oklog/ulid/v2"
)

func main() {
    // Generate a ULID with cryptographic entropy
    entropy := ulid.Monotonic(rand.New(rand.NewSource(time.Now().UnixNano())), 0)
    id := ulid.MustNew(ulid.Timestamp(time.Now()), entropy)

    fmt.Println(id.String())           // "01ARZ3NDEKTSV4RRFFQ69G5FAV"
    fmt.Println(id.Time())             // time.Time value

    // Parse
    parsed, err := ulid.Parse("01ARZ3NDEKTSV4RRFFQ69G5FAV")
    if err != nil {
        panic(err)
    }
    fmt.Println(parsed.Time())
}
```

## Storing ULIDs in databases

Since ULID is not a standardized type, storage options depend on the database:

**PostgreSQL:**
```sql
-- Option 1: Store as TEXT (26 bytes, sorts correctly as string)
CREATE TABLE events (
    id TEXT PRIMARY KEY NOT NULL,
    data JSONB
);

-- Option 2: Store as UUID (16 bytes — same bits, UUID representation)
-- Convert ULID to UUID in application layer
CREATE TABLE events (
    id UUID PRIMARY KEY NOT NULL,
    data JSONB
);
-- In Python: uid.to_uuid() converts ULID to equivalent UUID object
```

**MySQL:**
```sql
-- Option 1: CHAR(26) — fixed width, sorts correctly
CREATE TABLE events (
    id CHAR(26) PRIMARY KEY NOT NULL,
    data JSON
);

-- Option 2: BINARY(16) — 16 bytes, efficient storage
CREATE TABLE events (
    id BINARY(16) PRIMARY KEY NOT NULL,
    data JSON
);
```

For the best combination of storage efficiency and sort performance, convert ULIDs to their 16-byte binary representation and store in a UUID/BINARY(16) column. Most ULID libraries provide this conversion.

## Use cases

ULID is a strong choice for:

- **Event stores and audit logs** where chronological ordering is important and you want to query by ID range to get recent events
- **Message queues and stream processing** where ordered IDs help with partitioning and replay
- **API resources** where you want a shorter, cleaner identifier than UUID in URLs
- **Distributed systems** where records are generated on multiple nodes and merged into a central store

## Summary

ULID gives you the best of multiple worlds: the distributed, collision-resistant generation of UUID, the chronological sortability of auto-increment integers, and a compact 26-character URL-safe format. Its main trade-off versus UUID v7 is the lack of native database type support, which means slightly higher storage costs when persisted as TEXT.

For new projects deciding between ULID and UUID v7, prefer UUID v7 if native database type support is important, or ULID if you prefer the compact format and your ORM handles the string/binary conversion cleanly.

Explore UUID v4 and v7 generation at [uuidgen.io](/).
