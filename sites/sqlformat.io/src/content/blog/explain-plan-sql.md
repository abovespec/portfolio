---
title: "SQL EXPLAIN and Execution Plans: A Complete Guide"
description: "Learn to read SQL execution plans using EXPLAIN and EXPLAIN ANALYZE in PostgreSQL and MySQL. Identify seq scans, index scans, hash joins, and cost estimates."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["sql", "explain", "execution plan", "postgresql", "performance"]
draft: false
---

The SQL execution plan shows exactly how the database will process your query — which indexes it uses, how it joins tables, and where the time goes. Reading execution plans is the most reliable way to diagnose slow queries.

## EXPLAIN vs EXPLAIN ANALYZE

`EXPLAIN` estimates the cost without running the query. `EXPLAIN ANALYZE` runs the query and shows actual timings:

For more on this topic, see [*SQL Query Optimization: Practical Techniques That Actually Work*](/blog/sql-query-optimization).

```sql
-- Estimate only (no actual execution)
EXPLAIN
SELECT u.email, COUNT(o.order_id)
FROM users AS u
JOIN orders AS o ON u.user_id = o.user_id
GROUP BY u.email;

-- Run query + show actual vs estimated
EXPLAIN ANALYZE
SELECT u.email, COUNT(o.order_id)
FROM users AS u
JOIN orders AS o ON u.user_id = o.user_id
GROUP BY u.email;
```

Use `EXPLAIN` when the query is destructive or too slow to run. Use `EXPLAIN ANALYZE` for real performance data.

## Reading the output

```
HashAggregate  (cost=18.50..20.50 rows=200 width=36) (actual time=0.412..0.445 rows=3 loops=1)
  Group Key: u.email
  ->  Hash Join  (cost=1.07..16.00 rows=500 width=28) (actual time=0.071..0.362 rows=4 loops=1)
        Hash Cond: (o.user_id = u.user_id)
        ->  Seq Scan on orders  (cost=0.00..14.00 rows=400 width=8) (actual time=0.018..0.234 rows=4 loops=1)
        ->  Hash  (cost=1.04..1.04 rows=3 width=24) (actual time=0.031..0.031 rows=3 loops=1)
              ->  Seq Scan on users  (cost=0.00..1.03 rows=3 width=24) (actual time=0.013..0.019 rows=3 loops=1)
Planning Time: 0.253 ms
Execution Time: 0.512 ms
```

Each node has:
- **Node type** — what operation is performed (`HashAggregate`, `Hash Join`, `Seq Scan`, etc.)
- **cost=start..total** — estimated cost units (arbitrary, but consistent within one query)
- **rows** — estimated row count
- **actual time=start..end** — milliseconds from query start to first/last row (ANALYZE only)
- **loops** — how many times this node executed

The tree is read bottom-up: leaf nodes execute first, feeding results to parent nodes.

## Key node types

### Seq Scan (Sequential Scan)

Reads every row in the table. This is expected for small tables or when a large fraction of rows match. It's a problem when:
- The table is large
- You expected an index to be used
- `rows` is much smaller than the table size

For more on this topic, see [*SQL Style Guide: Conventions Every Team Should Follow*](/blog/sql-style-guide).

```
Seq Scan on orders  (cost=0.00..14000.00 rows=4 width=8)
                     Filter: (user_id = 123)
                     Rows Removed by Filter: 999996
```

`Rows Removed by Filter: 999996` with a small result set means you need an index on `user_id`.

### Index Scan

Uses a B-tree index to find rows. The index is traversed to locate matching rows, then the table is accessed for column data not in the index.

```
Index Scan using idx_orders_user_id on orders
  (cost=0.42..8.45 rows=4 width=64)
  Index Cond: (user_id = 123)
```

### Index Only Scan

All needed data is in the index — the table isn't accessed at all. This is the fastest read operation.

```
Index Only Scan using idx_users_status_email on users
  (cost=0.29..2.30 rows=100 width=16)
  Index Cond: (status = 'active')
  Heap Fetches: 0  ← table not touched
```

### Bitmap Index Scan + Bitmap Heap Scan

For queries matching many rows, the planner fetches all matching index entries first (Bitmap Index Scan), then accesses the table in page order (Bitmap Heap Scan). More efficient than many individual Index Scans:

```
Bitmap Heap Scan on orders
  ->  Bitmap Index Scan on idx_orders_created_at
        Index Cond: (created_at >= '2026-01-01')
```

### Hash Join

Builds a hash table from the smaller relation, then probes it with rows from the larger. Fast for large tables with no useful index on the join column:

```
Hash Join  (cost=25.00..1500.00 rows=5000 width=32)
  Hash Cond: (o.user_id = u.user_id)
  ->  Seq Scan on orders
  ->  Hash
        ->  Seq Scan on users
```

### Nested Loop

For each row in the outer table, scans (or seeks via index) the inner table. Good when the outer relation is small and the inner has an index:

For more on this topic, see [*SQL Joins Explained: INNER, LEFT, RIGHT, FULL, and CROSS*](/blog/sql-joins-explained).

```
Nested Loop  (cost=0.42..50.00 rows=10 width=32)
  ->  Seq Scan on users (small table, 10 rows)
  ->  Index Scan on orders
        Index Cond: (user_id = u.user_id)
```

Nested Loop on two large tables without indexes can be catastrophically slow.

### Merge Join

Requires both sides to be sorted on the join key. Fast when both sides are already sorted (e.g., primary key joins) or when sorting is cheap:

```
Merge Join  (cost=200.00..400.00 rows=5000 width=32)
  ->  Sort on users (user_id)
  ->  Sort on orders (user_id)
```

## Diagnosing common problems

### Large row count mismatch

When `rows` (estimate) differs greatly from `actual rows`:

```
Seq Scan on orders (cost=... rows=100 ...) (actual ... rows=50000 ...)
```

The planner used wrong statistics. Run `ANALYZE orders;` to update them. For persistent problems, lower `default_statistics_target` for that column:

```sql
ALTER TABLE orders ALTER COLUMN status SET STATISTICS 500;
ANALYZE orders;
```

### Missing index

A Seq Scan with `Rows Removed by Filter` showing most rows filtered out:

```
Seq Scan on events  (actual rows=1 loops=1)
  Filter: ((user_id = 123) AND (created_at > '2026-04-01'))
  Rows Removed by Filter: 4999999
```

Add the index:

```sql
CREATE INDEX idx_events_user_created ON events(user_id, created_at);
```

### Sort without index

```
Sort  (cost=50000.00..51000.00 rows=400000 width=32)
  Sort Key: created_at DESC
  Sort Method: external merge  Disk: 24576kB
```

"external merge" means the sort spilled to disk. Either add an index on the sort column or increase `work_mem`:

```sql
SET work_mem = '256MB';  -- session-level

-- Or add index if this is a common sort
CREATE INDEX idx_events_created_desc ON events(created_at DESC);
```

### Incorrect join strategy

If you see a Nested Loop on two large tables:

```
Nested Loop  (actual time=0.001..45000.000 rows=500000 loops=50000)
```

The planner may have underestimated row counts. Update statistics, or hint the planner:

```sql
SET enable_nestloop = OFF;  -- session-level, forces Hash Join
```

## EXPLAIN options in PostgreSQL

```sql
-- Human-readable format (default)
EXPLAIN ANALYZE SELECT ...;

-- JSON format (machine-readable, for explain.depesz.com)
EXPLAIN (ANALYZE, FORMAT JSON) SELECT ...;

-- Show buffer usage (reads from shared/local cache vs. disk)
EXPLAIN (ANALYZE, BUFFERS) SELECT ...;

-- Full detail
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) SELECT ...;
```

The `BUFFERS` option shows cache hits vs. disk reads:

```
Seq Scan on orders  (actual time=0.023..42.000 rows=400000 loops=1)
  Buffers: shared hit=12 read=1988
```

`shared hit` = served from cache; `read` = required disk I/O.

## MySQL EXPLAIN

MySQL's `EXPLAIN` output uses columns instead of a tree:

```sql
EXPLAIN
SELECT u.email, COUNT(o.order_id)
FROM users AS u
JOIN orders AS o ON u.user_id = o.user_id
GROUP BY u.email;
```

```
+----+-------------+-------+--------+---------------+---------+------+-------+
| id | select_type | table | type   | key           | key_len | rows | Extra |
+----+-------------+-------+--------+---------------+---------+------+-------+
|  1 | SIMPLE      | u     | index  | PRIMARY       | 4       | 3    | NULL  |
|  1 | SIMPLE      | o     | ref    | idx_user_id   | 4       | 5    | NULL  |
+----+-------------+-------+--------+---------------+---------+------+-------+
```

Key columns:
- **type** — `ALL` (full scan) is bad; `ref`, `eq_ref`, `const` are good
- **key** — which index is used; `NULL` means no index
- **rows** — estimated rows examined
- **Extra** — look for `Using filesort` (sort without index) and `Using temporary` (temp table)

Use `EXPLAIN FORMAT=JSON` in MySQL for the tree view equivalent:

```sql
EXPLAIN FORMAT=JSON SELECT ...;
```

## Visualization tools

- **explain.depesz.com** — paste PostgreSQL JSON output for color-coded visualization
- **explain.dalibo.com** — similar, with visual node graph
- **pgAdmin** — built-in graphical explain plan
- **DataGrip / DBeaver** — inline EXPLAIN with graphical view

The visual tools make it easier to spot the most expensive nodes in complex multi-table queries.

Format your queries before analyzing plans at [sqlformat.io](/).
