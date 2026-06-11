---
title: "Database Naming Conventions: Tables, Columns, Keys, and Constraints"
description: "Database naming conventions for PostgreSQL and MySQL: table names, column names, primary and foreign keys, index names, constraint patterns, and a full CREATE TABLE example."
publishDate: 2026-06-07
updatedDate: 2026-06-07
author: "Editorial Team"
tags: ["database", "naming conventions", "sql", "postgresql", "snake case"]
draft: false
heroImage: "/images/blog/database-naming-conventions-hero.png"
---

Inconsistent database naming is one of the most persistent sources of developer friction. A schema where some tables are `Users`, others are `user_accounts`, and one is `tbl_Order` makes every query a memory exercise. Consistent naming conventions make schemas self-documenting and ORM integration predictable.

This guide covers naming conventions for tables, columns, keys, indexes, and constraints in PostgreSQL and MySQL — the two most common open-source relational databases.

## Table names: the plural vs singular debate

The most contested question in database naming is whether table names should be plural or singular. Both camps have reasonable arguments:

**Plural (`users`, `orders`, `products`)**
- A table contains multiple rows, so a plural name describes the collection
- Reads naturally in queries: `SELECT * FROM users WHERE ...`
- Preferred by Rails (ActiveRecord) convention

**Singular (`user`, `order`, `product`)**
- A table name describes what a single row represents — a `user`, not a `users`
- Avoids irregular plurals (`person` → `people`, `sheep` → `sheep`)
- Preferred by the SQL standard (table = a set of entities of a type)

**The practical answer:** Pick one and apply it uniformly. Most teams using Rails or Django go plural. Most teams working without an opinionated ORM go singular. The important thing is consistency. Mixing `users` and `order` in the same schema is the worst outcome.

## Case: snake_case for column and table names

In PostgreSQL, all unquoted identifiers are folded to lowercase. `UserAccount`, `userAccount`, and `useraccount` all refer to the same table. For this reason, **snake_case is the universal convention** for PostgreSQL schemas:

```sql
-- Tables
users
user_accounts
order_line_items
product_categories

-- Columns
user_id
first_name
email_address
created_at
updated_at
is_active
```

MySQL is case-sensitive for table names on Linux (because tables map to filesystem files, and Linux filesystems are case-sensitive), but column names are case-insensitive. For portability across operating systems and for consistency with PostgreSQL, **use lowercase snake_case everywhere**.

For more on snake_case as a convention, see [*What Is snake_case? A Practical Guide for Developers*](/blog/what-is-snake-case).

## Primary keys: id vs table_name_id

Two conventions exist for primary key column names:

**Generic `id`**

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    ...
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    ...
);
```

**Table-prefixed `table_name_id`**

```sql
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    ...
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    ...
);
```

The `id` convention is simpler and is the default in Rails (ActiveRecord) and Django. Its disadvantage is that JOIN-heavy queries become ambiguous: which `id` is `o.id` — the order or something else?

The `table_name_id` convention is more explicit and avoids ambiguity in complex queries. It is common in data warehousing and BI contexts, and is preferred by many DBAs who write a lot of raw SQL.

**Foreign key naming** follows naturally from whichever primary key convention you choose: a foreign key referencing `users.id` is named `user_id`. A foreign key referencing `users.user_id` is also named `user_id`. Either way, foreign key columns are `{referenced_table_singular}_id`.

## Column naming best practices

**Use descriptive, self-documenting names:**

```sql
-- Clear
first_name
email_address
phone_number
date_of_birth
account_balance

-- Unclear
fname
em
phone
dob
bal
```

**Avoid SQL reserved words as column names.** These words are reserved or commonly used in SQL syntax and will require quoting if used as identifiers:

```sql
-- Problematic column names (reserved or commonly reserved words)
order
user
group
status      -- works in PostgreSQL but can confuse parsers
value
type
name        -- technically fine but very vague
```

If you need a column for "order" in context of sorting, use `sort_order` or `display_order`. For "type", use `account_type` or `product_type`. Prefixing with the entity name eliminates both the reserved-word problem and the ambiguity problem.

**Boolean columns should be prefixed with `is_`, `has_`, or `can_`:**

```sql
is_active       BOOLEAN DEFAULT TRUE,
is_verified     BOOLEAN DEFAULT FALSE,
has_newsletter  BOOLEAN DEFAULT FALSE,
can_login       BOOLEAN DEFAULT TRUE,
```

**Timestamp columns use consistent suffixes:**

```sql
created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
deleted_at      TIMESTAMPTZ,               -- NULL = not deleted (soft delete)
published_at    TIMESTAMPTZ,
expires_at      TIMESTAMPTZ,
```

The `_at` suffix signals a point in time (timestamp). The `_on` suffix is also used for date-only columns: `shipped_on DATE`, `due_on DATE`.

## Index naming: tablename_columnname_idx

Index names are not required to be unique within a database (only within a table in PostgreSQL, globally in MySQL), but following a consistent pattern prevents confusion:

```
Pattern: {table}_{columns}_idx
```

Examples:

```sql
-- Single-column index
CREATE INDEX users_email_address_idx ON users(email_address);
CREATE INDEX orders_user_id_idx ON orders(user_id);

-- Multi-column (composite) index
CREATE INDEX orders_user_id_created_at_idx ON orders(user_id, created_at);

-- Unique index (use _key suffix instead of _idx)
CREATE UNIQUE INDEX users_email_address_key ON users(email_address);

-- Partial index
CREATE INDEX orders_user_id_pending_idx ON orders(user_id)
    WHERE status = 'pending';
```

## Constraint naming: full pattern

Named constraints are easier to debug. PostgreSQL's error message `ERROR: duplicate key value violates unique constraint "users_pkey"` is more actionable than an unnamed constraint error.

Standard patterns:

```
Primary key:   {table}_pkey
Foreign key:   {table}_{column}_fkey
Unique:        {table}_{column(s)}_key
Check:         {table}_{column}_{check_name}_check
Not null:      (usually enforced inline, not as named constraint)
```

Examples:

```sql
ALTER TABLE users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id),
    ADD CONSTRAINT users_email_address_key UNIQUE (email_address),
    ADD CONSTRAINT users_account_balance_check CHECK (account_balance >= 0);

ALTER TABLE orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (order_id),
    ADD CONSTRAINT orders_user_id_fkey FOREIGN KEY (user_id)
        REFERENCES users(user_id) ON DELETE CASCADE,
    ADD CONSTRAINT orders_status_check CHECK (
        status IN ('pending', 'processing', 'shipped', 'delivered', 'cancelled')
    );
```

## PostgreSQL: quoted identifiers and mixed case

PostgreSQL folds unquoted identifiers to lowercase. If you create a table named `UserAccount` without quotes, PostgreSQL stores it as `useracccount`. To use mixed case, you must double-quote the identifier everywhere:

```sql
-- Creates table 'useraccount' (lowercase)
CREATE TABLE UserAccount (id SERIAL PRIMARY KEY);

-- Creates table 'UserAccount' (mixed case, requires quoting everywhere)
CREATE TABLE "UserAccount" (id SERIAL PRIMARY KEY);

-- Now you must always quote it
SELECT * FROM "UserAccount";   -- works
SELECT * FROM UserAccount;     -- queries 'useraccount' — different table!
```

This is why PostgreSQL users overwhelmingly prefer snake_case: it removes the quoting requirement entirely. **Avoid mixed-case table and column names in PostgreSQL**. If you're migrating from a camelCase schema, convert to snake_case to make your life easier.

## MySQL vs PostgreSQL conventions

| Convention | PostgreSQL | MySQL |
|-----------|-----------|-------|
| Default case folding | Lowercase (unquoted) | Table names: OS-dependent; columns: lowercase |
| Case-sensitive names | With double-quotes | Depends on `lower_case_table_names` setting |
| Preferred naming style | snake_case | snake_case |
| Auto-increment primary key | `SERIAL` or `GENERATED ALWAYS AS IDENTITY` | `AUTO_INCREMENT` |
| Timestamp default | `DEFAULT NOW()` or `DEFAULT CURRENT_TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` |
| Boolean type | `BOOLEAN` | `TINYINT(1)` or `BOOLEAN` (alias) |

Both databases work best with lowercase snake_case for all identifiers.

## Complete CREATE TABLE example with good naming

Here is a well-named schema for a simple e-commerce order system in PostgreSQL:

```sql
-- Users table
CREATE TABLE users (
    user_id         SERIAL PRIMARY KEY,
    email_address   TEXT NOT NULL,
    first_name      TEXT NOT NULL,
    last_name       TEXT NOT NULL,
    password_hash   TEXT NOT NULL,
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,
    is_verified     BOOLEAN NOT NULL DEFAULT FALSE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX users_email_address_key ON users(email_address);
CREATE INDEX users_is_active_idx ON users(is_active) WHERE is_active = TRUE;


-- Products table
CREATE TABLE products (
    product_id      SERIAL PRIMARY KEY,
    product_name    TEXT NOT NULL,
    product_slug    TEXT NOT NULL,
    unit_price      NUMERIC(10, 2) NOT NULL,
    stock_quantity  INTEGER NOT NULL DEFAULT 0,
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT products_unit_price_check CHECK (unit_price >= 0),
    CONSTRAINT products_stock_quantity_check CHECK (stock_quantity >= 0)
);

CREATE UNIQUE INDEX products_product_slug_key ON products(product_slug);


-- Orders table
CREATE TABLE orders (
    order_id        SERIAL PRIMARY KEY,
    user_id         INTEGER NOT NULL,
    order_status    TEXT NOT NULL DEFAULT 'pending',
    total_amount    NUMERIC(10, 2) NOT NULL,
    shipped_at      TIMESTAMPTZ,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT orders_user_id_fkey FOREIGN KEY (user_id)
        REFERENCES users(user_id) ON DELETE RESTRICT,
    CONSTRAINT orders_order_status_check CHECK (
        order_status IN ('pending', 'processing', 'shipped', 'delivered', 'cancelled')
    ),
    CONSTRAINT orders_total_amount_check CHECK (total_amount >= 0)
);

CREATE INDEX orders_user_id_idx ON orders(user_id);
CREATE INDEX orders_order_status_idx ON orders(order_status);


-- Order line items table (junction/fact table)
CREATE TABLE order_line_items (
    line_item_id    SERIAL PRIMARY KEY,
    order_id        INTEGER NOT NULL,
    product_id      INTEGER NOT NULL,
    quantity        INTEGER NOT NULL,
    unit_price      NUMERIC(10, 2) NOT NULL,

    CONSTRAINT order_line_items_order_id_fkey FOREIGN KEY (order_id)
        REFERENCES orders(order_id) ON DELETE CASCADE,
    CONSTRAINT order_line_items_product_id_fkey FOREIGN KEY (product_id)
        REFERENCES products(product_id) ON DELETE RESTRICT,
    CONSTRAINT order_line_items_quantity_check CHECK (quantity > 0),
    CONSTRAINT order_line_items_unit_price_check CHECK (unit_price >= 0)
);

CREATE INDEX order_line_items_order_id_idx ON order_line_items(order_id);
CREATE INDEX order_line_items_product_id_idx ON order_line_items(product_id);
```

This schema demonstrates: consistent snake_case throughout, descriptive column names with appropriate suffixes (`_at`, `_id`, `_hash`, `_status`, `_quantity`), named constraints following the `{table}_{column(s)}_{type}` pattern, and indexes named with the `{table}_{column(s)}_idx` pattern.

## Naming convention summary for databases

| Object | Convention | Example |
|--------|-----------|---------|
| Table name | snake_case plural or singular | `users` or `user` |
| Column name | snake_case | `first_name`, `created_at` |
| Primary key | `id` or `table_id` | `user_id` |
| Foreign key | `{ref_table_singular}_id` | `user_id`, `product_id` |
| Boolean column | `is_`, `has_`, `can_` prefix | `is_active`, `has_newsletter` |
| Timestamp column | `_at` suffix | `created_at`, `deleted_at` |
| Date column | `_on` suffix | `due_on`, `shipped_on` |
| Primary key constraint | `{table}_pkey` | `users_pkey` |
| Unique constraint | `{table}_{col}_key` | `users_email_address_key` |
| Foreign key constraint | `{table}_{col}_fkey` | `orders_user_id_fkey` |
| Check constraint | `{table}_{col}_{name}_check` | `orders_status_check` |
| Index | `{table}_{col}_idx` | `orders_user_id_idx` |

## Convert identifiers between naming styles

If you're generating column names from camelCase application models, or documenting a schema for a JavaScript client, you'll often need to convert between snake_case and camelCase. The [caseconvert.io](/) converter handles all major naming styles — paste a list of column names and get the converted output instantly.
