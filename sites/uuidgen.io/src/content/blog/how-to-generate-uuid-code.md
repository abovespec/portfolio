---
title: "How to Generate UUIDs in Python, JavaScript, Go, and SQL"
description: "Generate UUID v4 and v7 in Python (uuid module), JavaScript (crypto.randomUUID), Go (google/uuid), Java, C#, PHP, Rust, and SQL with working code examples."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["uuid", "generate uuid", "python", "javascript", "go", "programming"]
draft: false
---

Every major language has built-in or first-party UUID generation. Here's the canonical approach in each environment.

## Python

Python's standard library `uuid` module covers all UUID versions:

```python
import uuid

# UUID v4 (random) — most common
uid = uuid.uuid4()
print(uid)           # 550e8400-e29b-41d4-a716-446655440000
print(str(uid))      # same, as string
print(uid.hex)       # "550e8400e29b41d4a716446655440000" (no hyphens)
print(uid.bytes)     # b'\x55\x0e...' (16 bytes, raw)

# UUID v5 (name-based, deterministic)
namespace = uuid.NAMESPACE_URL
name = "https://example.com"
uid_v5 = uuid.uuid5(namespace, name)
# Always the same for the same inputs

# Parse a UUID string
uid = uuid.UUID("550e8400-e29b-41d4-a716-446655440000")
uid = uuid.UUID("550e8400e29b41d4a716446655440000")  # also works

# Validate
def is_valid_uuid(s: str) -> bool:
    try:
        uuid.UUID(s)
        return True
    except ValueError:
        return False

# UUID v7 (time-ordered) — external package
# pip install uuid7
import uuid7
uid_v7 = uuid7.uuid7()
print(uid_v7)  # 017f22e2-79b0-7cc3-98c4-dc0c0c07398f
```

## JavaScript / Node.js

```javascript
// Browser / Node.js 19+ / Deno — Web Crypto API
const uid = crypto.randomUUID();

// Node.js (all versions)
const { randomUUID } = require('crypto');
const uid = randomUUID();

// npm: uuid package — supports v1/v3/v4/v5/v7
// npm install uuid
import { v4 as uuidv4, v7 as uuidv7, validate, version } from 'uuid';

const uid_v4 = uuidv4();  // random
const uid_v7 = uuidv7();  // time-ordered (UUID v7)

// Validate
validate("550e8400-e29b-41d4-a716-446655440000");  // true
validate("not-a-uuid");                             // false
version("550e8400-e29b-41d4-a716-446655440000");   // 4
version(uuidv7());                                  // 7

// UUID v5 (deterministic)
import { v5 as uuidv5 } from 'uuid';
const MY_NAMESPACE = '550e8400-e29b-41d4-a716-446655440000';
const uid = uuidv5('https://example.com', MY_NAMESPACE);
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
    if err != nil {
        panic(err)
    }
    fmt.Println(id7.String())

    // Parse
    id, err = uuid.Parse("550e8400-e29b-41d4-a716-446655440000")
    if err != nil {
        // invalid UUID
    }

    // Validate
    _, err = uuid.Parse(s)
    isValid := err == nil

    // As bytes
    bytes := id[:]  // []byte, 16 bytes

    // UUID v5
    ns := uuid.NameSpaceURL
    id = uuid.NewSHA1(ns, []byte("https://example.com"))
}
```

## Java

```java
import java.util.UUID;

// UUID v4
UUID uid = UUID.randomUUID();
System.out.println(uid.toString());
// "550e8400-e29b-41d4-a716-446655440000"

// Parse
UUID parsed = UUID.fromString("550e8400-e29b-41d4-a716-446655440000");

// Get parts
long mostSig = uid.getMostSignificantBits();
long leastSig = uid.getLeastSignificantBits();
int version = uid.version();  // 4
int variant = uid.variant();  // 2

// UUID v7: no built-in — use java-uuid-generator library
// com.fasterxml.uuid:java-uuid-generator:4.x
import com.fasterxml.uuid.Generators;
UUID uid7 = Generators.timeBasedEpochGenerator().generate();
```

## C# (.NET)

```csharp
using System;

// UUID v4 (GUID)
Guid guid = Guid.NewGuid();
Console.WriteLine(guid.ToString());          // 550e8400-e29b-41d4-a716-446655440000
Console.WriteLine(guid.ToString("N"));       // without hyphens
Console.WriteLine(guid.ToString("B"));       // with braces
Console.WriteLine(guid.ToByteArray().Length); // 16

// Parse
Guid parsed = Guid.Parse("550e8400-e29b-41d4-a716-446655440000");

// Validate (TryParse)
if (Guid.TryParse(input, out Guid result)) {
    Console.WriteLine("Valid");
}

// .NET 9: UUID v7
// Guid guid7 = Guid.CreateVersion7();
```

## Rust

```rust
// Cargo.toml: uuid = { version = "1", features = ["v4", "v7"] }
use uuid::Uuid;

fn main() {
    // UUID v4
    let uid = Uuid::new_v4();
    println!("{}", uid);
    println!("{}", uid.as_hyphenated());    // with hyphens
    println!("{}", uid.as_simple());        // without hyphens
    println!("{:?}", uid.as_bytes());       // [u8; 16]

    // UUID v7
    let ts = uuid::Timestamp::now(uuid::NoContext);
    let uid7 = Uuid::new_v7(ts);

    // Parse
    let parsed = Uuid::parse_str("550e8400-e29b-41d4-a716-446655440000").unwrap();
}
```

## PHP

```php
// PHP 8.3+: built-in Uuid class (RFC 9562)
// Before 8.3: use ramsey/uuid package

// ramsey/uuid: composer require ramsey/uuid
use Ramsey\Uuid\Uuid;

$uid = Uuid::uuid4();
echo $uid->toString();  // "550e8400-e29b-41d4-a716-446655440000"

$uid7 = Uuid::uuid7();
echo $uid7->toString();  // time-ordered UUID v7

// Validate
$isValid = Uuid::isValid("550e8400-e29b-41d4-a716-446655440000");
```

## Ruby

```ruby
require 'securerandom'

# UUID v4
uid = SecureRandom.uuid
puts uid  # "550e8400-e29b-41d4-a716-446655440000"

# Without hyphens
uid_compact = SecureRandom.uuid.gsub('-', '')
```

Generate UUIDs at [uuidgen.io](/).
