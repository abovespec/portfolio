---
title: "UUID Database Performance: UUID v4 vs UUID v7 vs Auto-Increment"
description: "Understand UUID performance tradeoffs in databases. Learn why random UUIDs hurt PostgreSQL indexes, how UUID v7 solves it, and when to use each ID type."
publishDate: 2026-06-07
updatedDate: 2026-06-07
author: "Editorial Team"
tags: ["uuid", "database", "postgresql", "performance", "primary key"]
draft: false
heroImage: "/images/blog/uuid-database-performance-hero.png"
---

UUIDs are globally unique and don't require a central counter, but they come with a database performance cost that surprises many developers. Understanding *why* the cost exists — and how to mitigate it — is essential for making good ID strategy decisions.

## The Root Cause: B-Tree Index Fragmentation

Most relational database primary key indexes use a **B-tree** data structure. B-trees maintain sorted order, which makes range scans and exact lookups fast. The problem with UUID v4 is that it's random: each new UUID is inserted at a random position in the sorted tree.

**With sequential IDs (auto-increment):**
- New values are always the largest value
- They always insert at the right edge of the B-tree
- Pages fill sequentially, then new pages are allocated
- The index is compact and dense

**With random UUIDs (v4):**
- New values land at random positions in the middle of existing pages
- Pages fill unevenly; many pages are partially empty
- The database must frequently split and rebalance pages
- The index becomes fragmented with many partially-used pages

The practical consequences:
- **Higher disk usage**: fragmented indexes consume more space
- **Slower inserts**: page splits are expensive I/O operations
- **Lower cache efficiency**: with sequential IDs, hot recent data stays in buffer cache; with random IDs, inserts scatter across the entire index

## Benchmark Numbers

Benchmarks vary widely based on hardware, database version, workload, and configuration, but a common finding for high-insert workloads:

- **UUID v4** can be 5–10x slower than auto-increment for sequential insert benchmarks
- **UUID v7** performs comparably to auto-increment for inserts
- The difference is most pronounced on large tables (tens of millions of rows) with limited buffer pool relative to index size

## UUID v4: When the Cost Is Acceptable

For many applications, UUID v4 performance is perfectly acceptable:

- **Small tables** (< a few million rows): the index fits in memory, fragmentation is irrelevant
- **Read-heavy workloads**: the insert cost matters less if you're not inserting at high rates
- **Already using UUIDs**: migrating isn't always worth the disruption
- **Distributed systems**: the coordination-free property of UUIDs is architecturally valuable

Don't over-optimize. Benchmark your actual workload before concluding you have a UUID performance problem.

## UUID v7: The Best of Both Worlds

UUID version 7 is time-ordered with a random suffix. The first 48 bits are a Unix millisecond timestamp, making UUID v7 values monotonically increasing (within the same millisecond, the random suffix provides ordering).

```
018e5e9e-7d4c-7001-a123-b456c7890def
^^^^^^^^                              — 48-bit ms timestamp
                   ^^^^               — 12-bit random + version bit
                         ^^^^^^^^^^^ — 62-bit random + variant bits
```

**Why this helps performance:**
- Inserts always land near the right edge of the B-tree
- Pages fill sequentially like auto-increment
- No fragmentation from random inserts

**UUID v7 in PostgreSQL:**

PostgreSQL 17+ includes `gen_random_uuid()` as a built-in function. For UUID v7, use the `pg_uuidv7` extension:

```sql
-- Install the extension
CREATE EXTENSION IF NOT EXISTS pg_uuidv7;

-- Use in a table
CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v7(),
    created_at TIMESTAMPTZ DEFAULT now(),
    amount NUMERIC
);
```

**UUID v7 in application code:**

```python
# Python: uuid6 package
pip install uuid6
import uuid6
new_id = uuid6.uuid7()

# JavaScript: uuidv7 package
npm install uuidv7
import { uuidv7 } from 'uuidv7';
const id = uuidv7();
```

## Storing UUIDs Efficiently

### Use the Native UUID Type (PostgreSQL)

PostgreSQL has a native `UUID` type that stores UUIDs as 16 bytes:

```sql
-- Good: native UUID type, 16 bytes
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid()
);

-- Worse: stored as text, 36+ bytes
CREATE TABLE users_bad (
    id VARCHAR(36) PRIMARY KEY
);
```

The 36-character text representation uses more than twice the storage of the 16-byte binary representation. At scale, this matters for both storage and index size (which affects buffer pool efficiency).

### MySQL: BINARY(16) vs CHAR(36)

MySQL doesn't have a native UUID type. Use `BINARY(16)` with conversion functions:

```sql
CREATE TABLE users (
    id BINARY(16) PRIMARY KEY DEFAULT (UUID_TO_BIN(UUID(), 1))
);

-- The second argument to UUID_TO_BIN reorders bytes for better performance
-- UUID_TO_BIN(uuid, 1) rearranges the time_hi and time_low fields
-- for more sequential inserts with UUID v1

-- Query by UUID
SELECT * FROM users WHERE id = UUID_TO_BIN('550e8400-e29b-41d4-a716-446655440000');

-- Convert back to string
SELECT BIN_TO_UUID(id) FROM users;
```

## Index Configuration

### PostgreSQL Fill Factor

When you know you'll insert UUIDs randomly (v4), you can set a lower fill factor to reduce page splits:

```sql
CREATE INDEX ON orders(id) WITH (fillfactor = 70);
```

This leaves 30% of each index page empty, reducing splits when random values insert in the middle. The tradeoff: larger index size.

### Partial Indexes

If you frequently query by UUID for recent records only, a partial index can help:

```sql
-- Index only recent orders
CREATE INDEX idx_recent_orders ON orders(id)
WHERE created_at > NOW() - INTERVAL '30 days';
```

## When to Use Each ID Type

| Use Case | Recommended |
|----------|-------------|
| Simple apps, small tables | Auto-increment integer |
| Distributed systems | UUID v7 |
| High-volume insert performance | UUID v7 or auto-increment |
| Existing UUID v4 system | Keep UUID v4 unless you have measured performance issues |
| Public-facing IDs (avoid enumeration) | UUID v4 or v7 |
| Deterministic/content-addressed | UUID v5 |
| Legacy GUID compatibility (.NET) | GUID = UUID (same standard) |

## The Summary

UUID v4 causes B-tree index fragmentation because random values insert at random positions. This increases insert time and disk usage at scale. UUID v7 solves this by combining a timestamp prefix with random bits, giving you sequential inserts while maintaining global uniqueness. For new systems, UUID v7 is the recommended choice for primary keys.

Generate UUIDs for testing at [uuidgen.io](/) — supports v4, v7, v1, and other versions.
