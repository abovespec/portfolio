---
title: "How to Generate a UUID: Online, CLI, Python, JavaScript, and SQL"
description: "Generate UUIDs online and in code. Covers Python uuid module, JavaScript crypto.randomUUID, Node.js uuid package, CLI uuidgen, SQL gen_random_uuid, and UUID v7."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["uuid", "generate uuid", "uuid v4", "python", "javascript"]
draft: false
---

Generating UUIDs is a one-liner in every major language and on the command line. This guide covers the canonical approach in each environment.

## Online

[uuidgen.io](/) generates UUIDs in your browser. Options include v4 (random), v7 (time-ordered), and batch generation.

## Command line

**Linux/macOS — built-in `uuidgen`:**
```bash
# UUID v4 (random)
uuidgen

For more on this topic, see [*UUID v4 vs v7: Which Should You Use?*](/blog/uuid-v4-vs-v7).

# Lowercase (macOS default is uppercase)
uuidgen | tr '[:upper:]' '[:lower:]'

# Generate 10 UUIDs
for i in {1..10}; do uuidgen; done
```

**Python one-liner:**
```bash
python3 -c "import uuid; print(uuid.uuid4())"

# Multiple UUIDs
python3 -c "import uuid; [print(uuid.uuid4()) for _ in range(10)]"
```

**Node.js one-liner:**
```bash
node -e "console.log(crypto.randomUUID())"
```

## Python

```python
import uuid

# UUID v4 (random) — most common
uid = uuid.uuid4()
print(uid)           # 550e8400-e29b-41d4-a716-446655440000
print(str(uid))      # same, as string
print(uid.hex)       # "550e8400e29b41d4a716446655440000" (no hyphens)
print(uid.int)       # 113059749145936325402354257176981405696 (integer)
print(uid.bytes)     # b'\x55\x0e...' (16 bytes, binary)

# UUID v1 (time-based, includes MAC address)
uid_v1 = uuid.uuid1()

# UUID v3 (name-based, MD5)
uid_v3 = uuid.uuid3(uuid.NAMESPACE_URL, "https://example.com")

# UUID v5 (name-based, SHA-1 — preferred over v3)
uid_v5 = uuid.uuid5(uuid.NAMESPACE_URL, "https://example.com")

# Parse a UUID string
parsed = uuid.UUID("550e8400-e29b-41d4-a716-446655440000")
# Also accepts without hyphens:
parsed2 = uuid.UUID("550e8400e29b41d4a716446655440000")

# Validate (catches invalid UUIDs)
def is_valid_uuid(s: str) -> bool:
    try:
        uuid.UUID(s)
        return True
    except ValueError:
        return False
```

## JavaScript / Node.js

```javascript
// Browser / Node.js 19+ / Deno — built-in Web Crypto API
const uid = crypto.randomUUID();
// "550e8400-e29b-41d4-a716-446655440000"

// Node.js all versions: crypto module
const { randomUUID } = require('crypto');
const uid = randomUUID();

// npm: uuid package (more control, UUID v1/v3/v4/v5/v7)
import { v4 as uuidv4, v7 as uuidv7 } from 'uuid';
const uid_v4 = uuidv4();
const uid_v7 = uuidv7();  // time-ordered

// Validate a UUID string
import { validate, version } from 'uuid';
validate("550e8400-e29b-41d4-a716-446655440000");  // true
version("550e8400-e29b-41d4-a716-446655440000");   // 4
```

## Go

```go
package main

import (
    "fmt"
    "github.com/google/uuid"
)

func main() {
    // UUID v4
    id := uuid.New()
    fmt.Println(id.String())

    // UUID v7 (time-ordered)
    id7, err := uuid.NewV7()
    if err != nil { panic(err) }
    fmt.Println(id7.String())

    // Parse
    parsed, err := uuid.Parse("550e8400-e29b-41d4-a716-446655440000")
    if err != nil { panic(err) }

    // Generate and get bytes
    id = uuid.New()
    bytes := id[:]  // [16]byte slice
}
```

## SQL — database-native UUID generation

**PostgreSQL:**
```sql
-- PostgreSQL 13+ (recommended)
SELECT gen_random_uuid();

-- pgcrypto extension (older PostgreSQL)
SELECT uuid_generate_v4();  -- requires: CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- UUID as default primary key
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT NOT NULL UNIQUE
);

-- UUID v7 (monotonic, good for PKs) — available via pg_uuidv7 extension
SELECT uuid_generate_v7();
```

**MySQL 8.0+:**
```sql
-- UUID v1
SELECT UUID();

-- UUID v4 equivalent (MySQL doesn't natively have v4, but UUID() is fine for most uses)
-- For truly random UUID, generate in application code

-- UUID as primary key
CREATE TABLE users (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    email VARCHAR(255) NOT NULL UNIQUE
);
```

**SQLite:**
```sql
-- SQLite doesn't have a built-in UUID function.
-- Generate in application code and insert as TEXT.

For more on this topic, see [*How to Generate UUIDs in Python, JavaScript, Go, and SQL*](/blog/how-to-generate-uuid-code).

CREATE TABLE users (
    id TEXT PRIMARY KEY NOT NULL,
    email TEXT NOT NULL UNIQUE
);
-- Insert: INSERT INTO users (id, email) VALUES (?, ?) with uuid in application
```

## UUID v7 (time-ordered) in code

UUID v7 is the recommended version for database primary keys — it sorts chronologically and avoids B-tree index fragmentation:

For more on this topic, see [*UUID in Databases: Primary Keys, Storage, and Performance*](/blog/uuid-in-database).

```python
# Python: using uuid7 package
# pip install uuid7
import uuid7
uid = uuid7.uuid7()
print(uid)  # 017f22e2-79b0-7cc3-98c4-dc0c0c07398f
```

```javascript
// npm: uuid package
import { v7 as uuidv7 } from 'uuid';
const uid = uuidv7();
```

```go
id, _ := uuid.NewV7()
```

The first 48 bits of UUID v7 are the Unix timestamp in milliseconds, so UUIDs generated later sort after UUIDs generated earlier.

Generate UUIDs at [uuidgen.io](/).
