---
title: "UUID vs Auto-Increment: Which Primary Key Strategy Is Right for You?"
description: "Compare UUID primary keys vs auto-incrementing integer IDs. Covers storage, index performance, distributed systems, security, and when to use each."
publishDate: 2026-06-07
updatedDate: 2026-06-07
author: "Editorial Team"
tags: ["uuid", "database", "primary key", "auto-increment", "distributed systems"]
draft: false
---

Choosing a primary key strategy is one of the first decisions you make when designing a database schema, and it's hard to change later. The two dominant options are auto-incrementing integers (INT or BIGINT with `AUTO_INCREMENT` / `SERIAL`) and UUIDs. Each has real tradeoffs. Here's how to think through the choice.

## Auto-incrementing integers: the simple default

Auto-increment IDs assign each new row the next available integer: 1, 2, 3, and so on. The database manages this counter internally.

```sql
-- PostgreSQL
CREATE TABLE orders (
    id    BIGSERIAL PRIMARY KEY,
    total NUMERIC(10, 2) NOT NULL
);

-- MySQL
CREATE TABLE orders (
    id    BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    total DECIMAL(10, 2) NOT NULL
);
```

**Storage:** An INT is 4 bytes; BIGINT is 8 bytes. This is 2–4x smaller than a UUID (16 bytes).

**Index performance:** Because rows are inserted in ascending order, the B-tree index grows at the right edge. New inserts never split existing pages — a pattern databases optimize well. Read and write performance on the primary key index remains predictable regardless of table size.

**Human-readable:** An ID of `42` is easy to remember, type into a support ticket, or include in a log message. IDs like `550e8400-e29b-41d4-a716-446655440000` are harder to communicate verbally.

**Joins and foreign keys:** Integer foreign keys occupy less space on disk and in memory. In a table with billions of foreign key references, the difference in total storage can be significant.

### The problems with auto-increment

Despite the performance and simplicity benefits, auto-increment IDs have real weaknesses.

**Sequential enumeration attack.** If `/api/orders/42` works, an attacker can try `/api/orders/41`, `/api/orders/43`, and so on to enumerate all records. Even with authorization checks, leaking the existence of records is an information disclosure. UUIDs eliminate this entirely — you can't guess `550e8400-e29b-41d4-a716-446655440000`.

**No distributed generation.** Auto-increment requires a central authority — the database — to assign the next ID. In distributed systems with multiple write nodes, sharded databases, or offline-first apps that sync later, you can't generate a guaranteed-unique integer without coordination. Coordination means latency, and latency means bottlenecks.

**Merging is hard.** If you run two databases and need to merge their data — during an acquisition, a multi-region deployment, or a database migration — integer primary keys conflict. Record ID 42 exists in both databases, referring to different rows. UUID merges are trivially safe.

**Exposes business metrics.** A sequential order ID reveals how many orders you've processed. Competitors who make a purchase on day one and day thirty can compute your order volume from the ID delta.

## UUIDs as primary keys

A UUID (Universally Unique Identifier) is a 128-bit value, typically represented as a 36-character hexadecimal string:

```
550e8400-e29b-41d4-a716-446655440000
```

Because they are generated without central coordination, UUIDs can be created in application code before the row is even written to the database.

```python
import uuid
record_id = uuid.uuid4()  # generated in the application layer
```

**Globally unique without coordination.** UUIDs can be generated on any machine, in any process, at any time, and you can be statistically certain they will never collide. This is the fundamental property that makes them safe in distributed systems.

**Safe to expose.** A UUID in a URL path (`/orders/550e8400-e29b-41d4-a716-446655440000`) reveals nothing about the total number of orders, creation time, or the IDs of adjacent records.

**Client-side generation.** In offline-first mobile apps, event-sourcing systems, and distributed writes, you can assign an ID before the database is involved. This simplifies logic, eliminates roundtrips, and enables optimistic UI updates.

**Safe merges.** You can combine data from multiple databases, import records from external systems, or replicate across regions without ID conflicts.

### The problems with UUID v4

**Storage size.** At 16 bytes, a UUID primary key is 2–4x larger than a BIGINT. On a table with 500 million rows and multiple foreign key columns, this difference in storage adds up to gigabytes. Index sizes grow proportionally.

**Index fragmentation.** UUID v4 is entirely random. When a new row is inserted, its UUID falls at a random position in the B-tree primary key index. The database must split existing index pages to accommodate the new key. Over millions of inserts, this causes:

- Increased write amplification
- Higher cache miss rates (recently used pages are rarely the ones being written)
- Growing index bloat requiring more frequent maintenance (VACUUM, ANALYZE)

This fragmentation is measurable at millions of rows and severe at billions. It's the primary reason DBAs historically resisted UUID primary keys.

**Less readable.** Debugging with UUIDs in log files, support tickets, and shell queries is more cumbersome. Tools like `psql` display UUIDs as full 36-character strings, which reduces readability of query output.

## UUID v7: the middle ground

UUID v7, standardized in RFC 9562 (2024), addresses the fragmentation problem while keeping all the UUID advantages. It uses a 48-bit Unix millisecond timestamp prefix followed by random bits:

```
017f22e2-79b0-7cc3-98c4-dc0c0c07398f
├──────────────┤
Unix timestamp ms    └─ random bits
```

Because the timestamp prefix is monotonically increasing, UUID v7 values generated at different times sort in chronological order. New inserts consistently append to the right edge of the B-tree — the same efficient pattern as auto-increment integers.

```python
# pip install uuid7
import uuid7
pk = uuid7.uuid7()
```

```javascript
import { v7 as uuidv7 } from 'uuid';
const pk = uuidv7();
```

UUID v7 gives you:
- Globally unique IDs without central coordination
- Lexicographic sort = chronological sort
- Near-sequential B-tree inserts (low fragmentation)
- ~74 bits of random data (still collision-resistant)

The only UUID advantage it sacrifices is complete unpredictability — the millisecond timestamp is embedded in the ID, so you can determine roughly when a record was created from the UUID alone.

For more on this topic, see [*UUID v4 vs v7: Which Should You Use?*](/blog/uuid-v4-vs-v7).

## Side-by-side comparison

| Property | Auto-increment INT/BIGINT | UUID v4 | UUID v7 |
|---------|--------------------------|---------|---------|
| Storage | 4–8 bytes | 16 bytes | 16 bytes |
| Index performance | Excellent | Degrades at scale | Good |
| Globally unique | No | Yes | Yes |
| No central authority | No | Yes | Yes |
| Sortable by creation | Yes | No | Yes |
| Safe to expose in URLs | No (enumerable) | Yes | Yes |
| Human-readable | Yes | No | No |
| Distributed generation | No | Yes | Yes |
| Merge-safe | No | Yes | Yes |
| Standard support | Universal | Universal | Growing |

## When to use auto-increment integers

- **Simple, single-database applications** where enumeration isn't a concern and you control access at the application layer.
- **High-volume OLAP / analytics** where storage efficiency and join performance are critical and IDs are never exposed externally.
- **Internal-only tables** where records are never exposed via API and no distributed generation is needed.
- **Existing schemas** where migrating to UUIDs would require significant effort with marginal benefit.

## When to use UUIDs

- **Public-facing APIs** where resource IDs appear in URLs and you want to prevent enumeration.
- **Distributed systems** with multiple write nodes, event-sourced architectures, or microservices that each generate their own IDs.
- **Multi-region or multi-database deployments** where records may be merged.
- **Offline-first or mobile applications** that generate records locally before syncing to a server.
- **Any new application** starting fresh — the operational benefits of UUIDs compound over time.

When using UUIDs as primary keys in a new application, prefer **UUID v7** over v4 to avoid index fragmentation.

## Practical migration path

If you're migrating an existing auto-increment schema to UUIDs, a common pattern is to keep the integer as an internal surrogate key and add a UUID column for external exposure:

```sql
ALTER TABLE orders ADD COLUMN public_id UUID NOT NULL DEFAULT gen_random_uuid();
CREATE UNIQUE INDEX idx_orders_public_id ON orders(public_id);
```

Your API exposes `public_id`, while internal joins continue to use the efficient integer `id`. This approach gets you the security benefit of UUIDs without the index fragmentation cost on your largest tables.

## Summary

Auto-increment integers win on raw performance and simplicity. UUIDs win on security, portability, and distributed systems. UUID v7 closes most of the performance gap while keeping the UUID benefits. For any new application with public-facing resource IDs or distributed writes, UUIDs — especially v7 — are the right default choice.

Generate UUIDs for your next project at [uuidgen.io](/).
