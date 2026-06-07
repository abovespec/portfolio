---
title: "UUID in Python: A Complete Guide to the uuid Module"
description: "Learn how to generate UUIDs in Python using the built-in uuid module. Covers uuid4, uuid1, uuid5, uuid3, and working with UUID objects in APIs and databases."
publishDate: 2026-06-07
updatedDate: 2026-06-07
author: "Editorial Team"
tags: ["uuid", "python", "uuid4", "programming", "backend"]
draft: false
---

Python's built-in `uuid` module provides everything you need to generate and work with UUIDs. No external dependencies required for the most common use cases.

## The uuid Module Basics

```python
import uuid
```

The module provides four main generation functions, each corresponding to a UUID version, plus classes and utilities for working with UUID objects.

## uuid.uuid4(): Random UUID (Most Common)

UUID version 4 is randomly generated — 122 bits of randomness with 6 bits used for version and variant markers.

```python
import uuid

# Generate a random UUID
new_uuid = uuid.uuid4()
print(new_uuid)           # e.g., 550e8400-e29b-41d4-a716-446655440000
print(type(new_uuid))     # <class 'uuid.UUID'>

# Get it as a string
uuid_str = str(new_uuid)  # '550e8400-e29b-41d4-a716-446655440000'

# Get it without hyphens
compact = new_uuid.hex    # '550e8400e29b41d4a716446655440000'

# Get as bytes (16 bytes)
uuid_bytes = new_uuid.bytes  # b'\x55\x0e\x84...'
```

UUID v4 is the right choice for most use cases: database primary keys, session IDs, API keys, and any context where you need globally unique identifiers without coordination.

**When NOT to use uuid4**: if your IDs need to be chronologically sortable (e.g., for database index performance), use uuid7 instead (see below).

## uuid.uuid1(): Time-Based UUID

UUID version 1 incorporates the current timestamp and the MAC address of the generating machine.

```python
time_uuid = uuid.uuid1()
print(time_uuid)  # e.g., 1a2b3c4d-0000-1000-8000-a1b2c3d4e5f6

# Access the timestamp (100-nanosecond intervals since Oct 15, 1582)
print(time_uuid.time)     # integer timestamp
print(time_uuid.node)     # MAC address integer
```

**Privacy warning**: Because uuid1 includes your machine's MAC address, it can expose the generating machine's identity. Use it only in controlled environments where this is acceptable. For most application development, uuid4 is preferable.

**Sortability**: uuid1 values are time-ordered, but not in a way that makes database indexing efficient — the timestamp is split across multiple fields in a non-sequential byte order.

## uuid.uuid5() and uuid.uuid3(): Deterministic UUIDs

These generate a UUID deterministically from a **namespace** and a **name**. The same input always produces the same UUID.

### uuid.uuid5() (SHA-1 based — preferred)

```python
# uuid5 takes a namespace UUID and a name string
user_id = uuid.uuid5(uuid.NAMESPACE_DNS, 'example.com')
print(user_id)  # always the same for this input

# Built-in namespaces
uuid.NAMESPACE_DNS   # for fully-qualified domain names
uuid.NAMESPACE_URL   # for URLs
uuid.NAMESPACE_OID   # for ISO OIDs
uuid.NAMESPACE_X500  # for X.500 distinguished names

# Custom namespace
my_namespace = uuid.UUID('12345678-1234-5678-1234-567812345678')
item_id = uuid.uuid5(my_namespace, 'product-12345')
```

### uuid.uuid3() (MD5 based — legacy)

Same API as uuid5, but uses MD5 internally. MD5 is deprecated for security purposes. Prefer uuid5 for new code.

```python
legacy_id = uuid.uuid3(uuid.NAMESPACE_DNS, 'example.com')
```

**Use cases for uuid5/uuid3:**
- Generating consistent IDs for the same logical entity across systems
- Content-addressable storage
- Deduplicating records by hashing a natural key
- Converting existing identifiers into UUID format

## The UUID Object

The `uuid.UUID` class has useful attributes:

```python
u = uuid.UUID('550e8400-e29b-41d4-a716-446655440000')

u.hex         # '550e8400e29b41d4a716446655440000'
u.int         # integer representation
u.bytes       # 16-byte bytes object
u.bytes_le    # bytes in little-endian format
u.fields      # tuple of UUID fields
u.version     # UUID version (4 for uuid4)
u.variant     # UUID variant (RFC_4122)
str(u)        # '550e8400-e29b-41d4-a716-446655440000'
```

### Parsing UUID Strings

```python
# Parse from string
u = uuid.UUID('550e8400-e29b-41d4-a716-446655440000')

# Parse from hex (no hyphens)
u = uuid.UUID('550e8400e29b41d4a716446655440000')

# Parse from bytes
u = uuid.UUID(bytes=b'\x55\x0e\x84\x00...')  # 16 bytes

# Parse from integer
u = uuid.UUID(int=113059749145936325402354257176981405696)
```

### Validating UUIDs

```python
def is_valid_uuid(value: str) -> bool:
    try:
        uuid.UUID(str(value))
        return True
    except ValueError:
        return False

is_valid_uuid('550e8400-e29b-41d4-a716-446655440000')  # True
is_valid_uuid('not-a-uuid')                             # False
is_valid_uuid('550e8400-e29b-41d4-a716-44665544000Z')  # False
```

## Storing UUIDs in Databases

### PostgreSQL

PostgreSQL has a native `UUID` data type that stores UUIDs efficiently as 16 bytes:

```python
# With psycopg2 — uuid objects work natively
import psycopg2
import uuid

conn = psycopg2.connect("...")
cur = conn.cursor()

user_id = uuid.uuid4()
cur.execute("INSERT INTO users (id, name) VALUES (%s, %s)", (user_id, "Alice"))
```

### SQLite

SQLite doesn't have a UUID type. Store as TEXT (36 chars) or BLOB (16 bytes):

```python
# Store as string
cursor.execute("INSERT INTO items (id) VALUES (?)", (str(uuid.uuid4()),))

# Store as bytes (more efficient)
cursor.execute("INSERT INTO items (id) VALUES (?)", (uuid.uuid4().bytes,))
```

### SQLAlchemy

```python
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.types import String
import uuid

# PostgreSQL — use native UUID type
class User(Base):
    __tablename__ = 'users'
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

# SQLite/other — store as string
class Item(Base):
    __tablename__ = 'items'
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
```

### Django

```python
from django.db import models
import uuid

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
```

Django's `UUIDField` handles serialization/deserialization automatically.

## UUID v7: Time-Ordered Random UUIDs

Python's built-in `uuid` module (as of Python 3.13) added uuid7 support. For earlier versions, use the `uuid6` third-party package:

```bash
pip install uuid6
```

```python
import uuid6

# UUID v7: time-ordered with random suffix
new_uuid = uuid6.uuid7()
print(new_uuid)  # e.g., 018e-5e9e-7d4c-8001-a123b456c789

# Compare: uuid7 values are sortable chronologically
id1 = uuid6.uuid7()
id2 = uuid6.uuid7()
assert id1 < id2  # True — later UUID is lexicographically greater
```

UUID v7 is the recommended choice for database primary keys because:
1. Chronological order means sequential inserts → no index fragmentation
2. Still random enough for security (74 bits of randomness)
3. Standard UUID format — 16 bytes, same as uuid4

Generate UUIDs online with [uuidgen.io](/) to quickly get v4, v7, or other versions without any code setup.
