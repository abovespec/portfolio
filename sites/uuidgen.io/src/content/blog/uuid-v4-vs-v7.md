---
title: "UUID v4 vs v7: Which Should You Use?"
description: "Compare UUID v4 (random) vs UUID v7 (time-ordered). Learn when each is appropriate, how v7 improves database index performance, and migration strategies."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["uuid", "uuid v4", "uuid v7", "database", "primary key"]
draft: false
---

UUID v4 has been the default choice for years. UUID v7, standardized in RFC 9562 (2024), is now the recommended choice for most new applications. Here's the difference and when to use each.

## UUID v4 (random)

UUID v4 is 122 bits of cryptographically random data. The remaining 6 bits are fixed version and variant bits.

For more on this topic, see [*What Is a UUID? Format, Versions, and How They Work*](/blog/what-is-a-uuid).

```
Structure:
xxxxxxxx-xxxx-4xxx-[89ab]xxx-xxxxxxxxxxxx

Example:
550e8400-e29b-41d4-a716-446655440000
                ↑ '4' = version 4
```

**Generation:**
```python
import uuid
uid = uuid.uuid4()  # fully random
```

For more on this topic, see [*UUID vs GUID: Are They the Same Thing?*](/blog/uuid-vs-guid).

**Properties:**
- Completely random — no pattern, no time information
- 122 bits of entropy (~5.3 × 10^36 possible values)
- Not sortable by creation time
- Widely supported in every database, ORM, and UUID library

## UUID v7 (time-ordered random)

UUID v7 uses a Unix millisecond timestamp prefix followed by random bits:

```
Structure:
tttttttt-tttt-7xxx-[89ab]xxx-xxxxxxxxxxxx
└────────────┘
Unix ms timestamp (48 bits)

Example:
017f22e2-79b0-7cc3-98c4-dc0c0c07398f
                ↑ '7' = version 7
```

**Generation:**
```python
# pip install uuid7
import uuid7
uid = uuid7.uuid7()
```

For more on this topic, see [*How to Generate a UUID: Online, CLI, Python, JavaScript, and SQL*](/blog/generate-uuid).

```javascript
import { v7 as uuidv7 } from 'uuid';
const uid = uuidv7();
```

**Properties:**
- Monotonically increasing (later UUIDs sort after earlier ones)
- First 48 bits = Unix timestamp in milliseconds
- ~74 bits of random data (enough for collision resistance)
- Sortable by creation time lexicographically

## The database performance problem with v4

In relational databases, tables are usually stored as B-trees sorted by the primary key. When you insert rows with sequential keys (like auto-increment integers), new rows go at the end of the tree — efficient.

With UUID v4, each new row has a random key that inserts at a random position in the B-tree. This causes:
- **Page fragmentation** — the B-tree splits pages frequently
- **Cache misses** — random inserts access different pages than recent inserts
- **Slower inserts** at scale — especially noticeable in PostgreSQL, MySQL, SQL Server

The effect is measurable at millions of rows. At billions of rows, it's severe.

**UUID v7 solves this:** Because v7 UUIDs are monotonically increasing, new rows consistently insert at the end of the B-tree — just like auto-increment integers.

## Benchmark comparison

High-volume insert benchmarks (approximate, varies by hardware):

| ID type | Inserts/second (10M rows) | Index fragmentation |
|---------|--------------------------|-------------------|
| Auto-increment INT | ~100K/s | Minimal |
| UUID v7 | ~90K/s | Low |
| UUID v4 | ~40K/s | High |

The performance difference only becomes significant at scale (millions+ of rows). For most small-to-medium applications, UUID v4 is perfectly adequate.

## When to use UUID v4

- Applications with moderate write volume (< millions of inserts/day)
- When you need maximum randomness (no time correlation)
- When you don't want to expose creation order via the UUID
- When you're using a database that already uses UUID v4 and migration isn't justified
- For non-PK uses (session tokens, file names, log IDs)

## When to use UUID v7

- New applications where you're choosing an ID strategy fresh
- High write-volume systems (millions of inserts/day)
- Systems that need to sort records by creation time using the ID
- When you want to avoid the B-tree fragmentation problem from the start
- Replacing auto-increment IDs in distributed systems where central coordination isn't feasible

## UUID v7 in PostgreSQL

PostgreSQL doesn't have native v7 support yet, but the `pg_uuidv7` extension adds it:

```sql
CREATE EXTENSION IF NOT EXISTS pg_uuidv7;

CREATE TABLE events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v7(),
    data JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

Alternatively, generate v7 in your application and pass it to PostgreSQL as a regular UUID:

```python
import uuid7
import psycopg2

conn = psycopg2.connect(...)
cur = conn.cursor()
cur.execute(
    "INSERT INTO events (id, data) VALUES (%s, %s)",
    (str(uuid7.uuid7()), '{"key": "value"}')
)
```

## Extracting the timestamp from UUID v7

```python
import uuid7

uid = uuid7.uuid7()
ts_ms = uuid7.uuid7_to_time(uid)  # milliseconds since Unix epoch
```

```javascript
import { v7 as uuidv7 } from 'uuid';
const uid = uuidv7();

// Extract timestamp from first 48 bits
const uuidBytes = Buffer.from(uid.replace(/-/g, ''), 'hex');
const timestampMs = Number(uuidBytes.readBigUInt64BE(0) >> 16n);
const date = new Date(timestampMs);
```

## Summary

| | UUID v4 | UUID v7 |
|-|---------|---------|
| Randomness | 122 bits | ~74 bits |
| Sortable | No | Yes |
| DB PK performance | Degrades at scale | Stays good |
| Time info exposed | No | Yes (ms timestamp) |
| Standard | RFC 4122 (2005) | RFC 9562 (2024) |
| Library support | Universal | Growing |

**Recommendation:** Use v7 for new database primary keys. Use v4 for everything else.

Generate UUID v4 and v7 at [uuidgen.io](/).
