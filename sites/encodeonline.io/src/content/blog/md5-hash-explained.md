---
title: "MD5 Hash: What It Is, How It Works, and When Not to Use It"
description: "MD5 produces a 128-bit hash of any input. Learn how MD5 works, why it's cryptographically broken, what it's still useful for, and which alternatives to use for security."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["md5", "hashing", "cryptography", "security", "checksums"]
draft: false
---

MD5 (Message Digest 5) is a hash function that takes any input and produces a 128-bit (32 hex character) digest. It was published in 1991 by Ronald Rivest and was widely used for file integrity checks and password hashing — until its cryptographic weaknesses became practically exploitable.

## What MD5 looks like

```
Input:  "Hello, World!"
MD5:    65a8e27d8879283831b664bd8b7f0ad4

Input:  "Hello, World." (period instead of exclamation)
MD5:    d9e7d8bdb98a89a15fac6e6de5e58a10
```

For more on this topic, see [*URL Encoding (Percent-Encoding): The Complete Guide*](/blog/url-encoding-guide).

A single character change produces a completely different hash (the **avalanche effect**). The output is always exactly 32 hex characters (128 bits), regardless of input length.

For more on this topic, see [*HTML Entities: The Complete Reference for Special Characters*](/blog/html-entities-guide).

## How MD5 works (overview)

MD5 processes input in **512-bit (64-byte) blocks**:

1. **Padding:** The input is padded so its length is congruent to 448 mod 512. A `1` bit is appended, then `0` bits, then the original length as a 64-bit integer.
2. **Initialization:** Four 32-bit state variables (A, B, C, D) are initialized with fixed constants.
3. **Processing:** Each 512-bit block goes through four rounds of 16 operations each, using bitwise operations (AND, OR, XOR, NOT), modular addition, and left rotations.
4. **Final output:** After processing all blocks, the four 32-bit state variables are concatenated to form the 128-bit digest.

The full specification is in [RFC 1321](https://www.rfc-editor.org/rfc/rfc1321).

## Computing MD5 in common languages

**Command line:**

```bash
# Linux
echo -n "Hello, World!" | md5sum
# 65a8e27d8879283831b664bd8b7f0ad4  -

# macOS
echo -n "Hello, World!" | md5
# 65a8e27d8879283831b664bd8b7f0ad4

# File checksum
md5sum file.iso
```

**Python:**

```python
import hashlib

hashlib.md5(b"Hello, World!").hexdigest()
# '65a8e27d8879283831b664bd8b7f0ad4'

# File hash
def md5_file(path: str) -> str:
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()
```

**JavaScript (Node.js):**

```js
const crypto = require('crypto');

crypto.createHash('md5').update('Hello, World!').digest('hex');
// '65a8e27d8879283831b664bd8b7f0ad4'
```

**Go:**

```go
import (
    "crypto/md5"
    "fmt"
)

fmt.Sprintf("%x", md5.Sum([]byte("Hello, World!")))
// "65a8e27d8879283831b664bd8b7f0ad4"
```

## Why MD5 is cryptographically broken

MD5 has two serious cryptographic weaknesses:

**1. Collision attacks:** Two different inputs can produce the same MD5 hash. Collisions were first demonstrated theoretically in 1996 and practically in 2004 by Xiaoyun Wang et al. Today, MD5 collisions can be computed in seconds on consumer hardware.

**Practical consequence:** An attacker can craft a malicious file that has the same MD5 hash as a legitimate file. MD5 cannot reliably verify that a file hasn't been tampered with when the attacker controls the file content.

**2. Preimage resistance is weakened:** Finding a message that hashes to a given MD5 value is harder than a collision, but MD5's margin has eroded significantly compared to modern hash functions.

For more on this topic, see [*Hash Functions Explained: MD5, SHA-1, SHA-256, and Beyond*](/blog/hash-functions-explained).

**Rainbow table attacks on passwords:** MD5 without salting is trivially reversed for common passwords. Tools like hashcat can crack unsalted MD5 passwords in milliseconds using precomputed rainbow tables.

## What MD5 is still useful for

MD5's weaknesses are specifically cryptographic. It remains valid for **non-security uses**:

- **Non-cryptographic checksums** for accidental data corruption (not malicious tampering) — if you're checking whether a file transferred correctly over a reliable channel, MD5 is fine.
- **Cache keys and ETags** — identifying content for caching purposes where collision attacks aren't a threat.
- **Content-based deduplication** in non-adversarial systems.
- **Hash maps and bloom filters** as a fast hash function.
- **Checksums in legacy systems** where changing the hash function would require widespread migration.

## MD5 vs SHA-256 for security use cases

| Property | MD5 | SHA-256 |
|----------|-----|---------|
| Output size | 128 bits | 256 bits |
| Collision resistance | Broken (collisions computable in seconds) | No known practical attacks |
| Preimage resistance | Weakened | No known practical attacks |
| Speed | Very fast | Fast |
| Password hashing | Never use | Don't use directly — use bcrypt/argon2 |
| File integrity | Only for accidental errors | Use for security-sensitive verification |
| Digital signatures | Never use | Acceptable (SHA-384/512 preferred) |

For file integrity in security contexts (software distribution, code signing), use SHA-256 or SHA-512. For password hashing, use bcrypt, Argon2, or scrypt — dedicated password hashing functions that incorporate salting and work factor tuning.

## Password hashing: never use raw MD5 or SHA

MD5(password) and even SHA256(password) are dangerously fast. GPU clusters can try billions of MD5 hashes per second. Use a slow, purposefully expensive function:

```python
import bcrypt

# Hash a password
hashed = bcrypt.hashpw(b"mysecretpassword", bcrypt.gensalt())

# Verify
bcrypt.checkpw(b"mysecretpassword", hashed)  # True
```

Or with Argon2 (the current recommended standard, winner of [Password Hashing Competition](https://www.password-hashing.net/)):

```python
from argon2 import PasswordHasher

ph = PasswordHasher()
hash = ph.hash("mysecretpassword")
ph.verify(hash, "mysecretpassword")  # True
```

## Compute MD5 online

For generating an MD5 checksum of text or a file without installing tools, use [encodeonline.io](/) — paste your text and get the hash instantly.
