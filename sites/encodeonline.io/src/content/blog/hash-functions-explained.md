---
title: "Hash Functions Explained: MD5, SHA-1, SHA-256, and Beyond"
description: "What hash functions are, how they work, and which to use. Covers MD5, SHA-1, SHA-256, SHA-512, bcrypt, and Argon2 with code examples."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["hashing", "sha256", "md5", "cryptography", "security"]
draft: false
---

A hash function takes any input — a file, a password, a message — and produces a fixed-length output called a **digest** or **hash**. The same input always produces the same hash; different inputs produce different hashes (with extraordinarily rare exceptions called collisions).

## Properties of a cryptographic hash function

A cryptographic hash function must have four properties:

1. **Deterministic** — the same input always gives the same output
2. **Fast to compute** — computing the hash should be quick
3. **Avalanche effect** — a single bit change in input should change roughly half the output bits
4. **One-way (preimage resistance)** — given a hash, it should be computationally infeasible to find the original input
5. **Collision resistance** — finding two different inputs that produce the same hash should be computationally infeasible

Hash functions used in security (digital signatures, TLS, file integrity) must be **cryptographically secure**. Functions that fail these properties are broken for security use, even if they remain useful for non-security tasks.

## Common hash algorithms

### MD5

- **Output:** 128 bits (32 hex chars)
- **Status:** Cryptographically broken — collisions computable in seconds
- **Use today:** Non-cryptographic checksums, cache keys, deduplication

```bash
echo -n "hello" | md5sum
# 5d41402abc4b2a76b9719d911017c592
```

### SHA-1

- **Output:** 160 bits (40 hex chars)
- **Status:** Cryptographically broken for collision resistance since 2017 ([SHAttered attack](https://shattered.io/))
- **Use today:** Legacy systems only; not acceptable for new deployments
- **Migration path:** Replace with SHA-256 or SHA-3

```bash
echo -n "hello" | sha1sum
# aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d
```

### SHA-256 (SHA-2 family)

- **Output:** 256 bits (64 hex chars)
- **Status:** No known practical attacks; current standard
- **Use today:** File integrity, digital signatures, TLS certificates, Bitcoin

```bash
echo -n "hello" | sha256sum
# 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
```

### SHA-512 (SHA-2 family)

- **Output:** 512 bits (128 hex chars)
- **Status:** No known practical attacks; stronger than SHA-256
- **Use today:** High-security contexts; SHA-512/256 (truncated) is a good SHA-256 replacement on 64-bit systems

```bash
echo -n "hello" | sha512sum
# 9b71d224bd62f3785d96d46ad3ea3d73319bfbc2890caadae2dff72519673ca72323c3d99ba5c11d7c7acc6e14b8c5da0c4663475c2e5c3adef46f73bcdec043
```

### SHA-3 (Keccak)

- **Output:** Variable (SHA3-256, SHA3-512, etc.)
- **Status:** NIST standard; different construction than SHA-2 (sponge function); no known attacks
- **Use today:** Alternative to SHA-2, particularly where SHA-2 implementation weaknesses are a concern

```python
import hashlib
hashlib.sha3_256(b"hello").hexdigest()
```

### BLAKE2

- **Output:** Variable (BLAKE2b up to 512 bits, BLAKE2s up to 256 bits)
- **Status:** No known attacks; faster than SHA-256 in software
- **Use today:** File hashing, checksums where performance matters (used in Git, WireGuard, libsodium)

```python
import hashlib
hashlib.blake2b(b"hello").hexdigest()
```

## Password hashing: a special case

Password hashing is different from data hashing. Regular hash functions (SHA-256, SHA-512) are designed to be fast, which is exactly wrong for passwords — faster hashing means an attacker can try billions of guesses per second.

Password hashing functions are deliberately slow and include salting:

### bcrypt

- Tunable work factor (cost parameter)
- Built-in salt generation
- Widely supported, time-tested since 1999

```python
import bcrypt

hashed = bcrypt.hashpw(b"mysecretpassword", bcrypt.gensalt(rounds=12))
bcrypt.checkpw(b"mysecretpassword", hashed)  # True
```

### Argon2

- Winner of the [Password Hashing Competition (2015)](https://www.password-hashing.net/)
- Tunable memory, parallelism, and time cost
- Current best practice for new systems

```python
from argon2 import PasswordHasher

ph = PasswordHasher(time_cost=3, memory_cost=65536, parallelism=4)
hash = ph.hash("mysecretpassword")
ph.verify(hash, "mysecretpassword")  # True
```

### scrypt

- Memory-hard; resistant to GPU/ASIC attacks
- Used by Litecoin, older Let's Encrypt implementations

```python
import hashlib
dk = hashlib.scrypt(b"password", salt=b"salt", n=2**14, r=8, p=1)
```

## Computing hashes in common languages

**Python (hashlib):**

```python
import hashlib

# SHA-256
hashlib.sha256(b"data").hexdigest()

# SHA-512
hashlib.sha512(b"data").hexdigest()

# File hash
def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()
```

**Node.js:**

```js
const crypto = require('crypto');

crypto.createHash('sha256').update('data').digest('hex');
crypto.createHash('sha512').update('data').digest('hex');
```

**Go:**

```go
import (
    "crypto/sha256"
    "fmt"
)

h := sha256.Sum256([]byte("data"))
fmt.Sprintf("%x", h)
```

**Bash:**

```bash
echo -n "data" | sha256sum | cut -d' ' -f1
echo -n "data" | sha512sum | cut -d' ' -f1

# File
sha256sum myfile.iso
```

## Choosing the right hash function

| Purpose | Recommended |
|---------|-------------|
| File integrity (new system) | SHA-256 or BLAKE2b |
| Digital signatures | SHA-256 or SHA-384 |
| TLS certificates | SHA-256 |
| Password hashing | Argon2id or bcrypt |
| Non-security checksum | MD5 or SHA-1 (fast, widely available) |
| High-performance hashing | BLAKE2b or BLAKE3 |
| Legacy interop | Match the existing system |

## Compute a hash online

To generate an MD5, SHA-256, or SHA-512 hash of a text string without installing tools, use [encodeonline.io](/).
