---
title: "SHA-256 Hash Explained: How It Works and Where It's Used"
description: "SHA-256 is a cryptographic hash from the SHA-2 family producing a fixed 256-bit output. Learn how it works, why SHA-1 was deprecated, and how to use SHA-256 in Python, JS, and the CLI."
publishDate: 2026-06-07
updatedDate: 2026-06-07
author: "Editorial Team"
tags: ["sha256", "cryptography", "hash functions", "security", "python"]
draft: false
---

SHA-256 (Secure Hash Algorithm 256-bit) is the most widely deployed member of the SHA-2 family, standardized by NIST in 2001. It takes any input — a byte, a file, or a petabyte of data — and produces a deterministic, fixed-length 256-bit (32-byte) output, usually represented as 64 lowercase hexadecimal characters.

```
SHA-256("hello") = 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
SHA-256("Hello") = 185f8db32921bd46d35cc5200032bb989d71ab8125a5657ad17bec5e3bda2f2
```

Notice how changing a single character produces a completely different hash — this is the **avalanche effect**, one of SHA-256's most important properties.

## Core properties of SHA-256

**Deterministic.** The same input always produces the same output. This makes SHA-256 suitable for verification: if two parties hash the same file independently and get the same digest, the files are identical.

**Fixed output size.** Every input, no matter how long, produces exactly 256 bits (64 hex characters). There is no way to guess the original input length from the hash.

**Avalanche effect.** A single bit change in the input completely scrambles the output. There is no detectable correlation between similar inputs.

**One-way (pre-image resistant).** Given a SHA-256 hash, it is computationally infeasible to find any input that produces that hash. Reversing SHA-256 would require brute force over an astronomically large search space.

**Collision resistant.** Finding two different inputs that produce the same hash is computationally infeasible with today's hardware. No practical collision has ever been found for SHA-256.

**Second pre-image resistant.** Given an input and its hash, finding a different input with the same hash is infeasible.

## SHA-256 output format

The raw output is 32 bytes (256 bits). It is almost always encoded as a lowercase hexadecimal string:

```
Input:  "The quick brown fox jumps over the lazy dog"
Output: d7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592
         ↑ 64 hex characters = 256 bits
```

In some contexts (email headers, certificates) the raw bytes are Base64-encoded to produce a 44-character string:

```
2/0z+/5m9O3Nf+vMqUZE9Vxswa3xq95bbAf5K+lI3h4=
```

## Common use cases

### Password storage with salt

SHA-256 alone is not suitable for password hashing because it is too fast — an attacker can compute billions of SHA-256 hashes per second using a GPU. Dedicated password hashing algorithms (bcrypt, Argon2, scrypt) are designed to be slow. That said, understanding SHA-256 is prerequisite knowledge.

When SHA-256 is used in a password context, it must be combined with a random salt to prevent rainbow table attacks:

```python
import hashlib, os

def hash_password(password: str) -> tuple[bytes, bytes]:
    salt = os.urandom(32)           # 256-bit random salt
    dk = hashlib.pbkdf2_hmac(
        'sha256',                   # SHA-256 as the PRF
        password.encode('utf-8'),
        salt,
        iterations=600_000          # NIST 2023 recommendation
    )
    return salt, dk
```

PBKDF2-HMAC-SHA256 with 600,000 iterations is acceptable for password hashing where bcrypt/Argon2 is unavailable (e.g., FIPS environments).

### File integrity verification

SHA-256 is the standard checksum format for software downloads. When you download an ISO or a package tarball, the publisher provides its SHA-256 hash. After downloading, you compute the hash locally and compare:

```bash
sha256sum ubuntu-24.04-desktop-amd64.iso
# 8762f7e74e4d64d72fceb5f70682e6b069932deedb4949c6975d0f0fe0a91be3  ubuntu-24.04-desktop-amd64.iso
```

If the hash matches the publisher's value, the file is intact and unmodified. If it differs, the download was corrupted or tampered with.

### Digital signatures

A digital signature signs the *hash* of a document, not the document itself. SHA-256 is the standard hash algorithm in RSA-SHA256 and ECDSA-SHA256 signatures, used in:

- TLS/HTTPS certificates (X.509 signatures)
- Code signing (Windows Authenticode, macOS Gatekeeper)
- SSH public key authentication
- JWT (JSON Web Token) with `RS256` or `ES256` algorithm header

### Bitcoin proof of work

Bitcoin's mining algorithm performs a double SHA-256 over a block header:

```
SHA-256(SHA-256(block_header))
```

Miners must find a nonce value that makes the resulting hash fall below a target threshold (i.e., start with a certain number of zero bits). This computational puzzle is the heart of Bitcoin's proof-of-work consensus.

### HMAC-SHA256

HMAC (Hash-based Message Authentication Code) uses SHA-256 as its underlying hash to produce a message authentication code. Webhook providers (GitHub, Stripe, Twilio) sign payloads with HMAC-SHA256 so that receivers can verify the payload was not tampered with:

```python
import hmac, hashlib

secret = b"my_webhook_secret"
payload = b'{"event": "payment.completed", "amount": 9900}'

signature = hmac.new(secret, payload, hashlib.sha256).hexdigest()
# "3a7bd3e2..."
```

## SHA-256 vs SHA-1: why SHA-1 is deprecated

SHA-1 produces a 160-bit (40 hex char) output. In 2017, Google's CWI Amsterdam team published SHAttered — the first practical SHA-1 collision, producing two different PDF files with identical SHA-1 hashes. The attack cost roughly $110,000 in cloud compute at the time.

| Property | SHA-1 | SHA-256 |
|----------|-------|---------|
| Output size | 160 bits (40 hex) | 256 bits (64 hex) |
| Collision resistance | Broken (2017) | No known attack |
| NIST status | Deprecated (2011) | Current standard |
| TLS usage | Forbidden in TLS 1.3 | Required |
| Git (default) | Legacy (being migrated) | SHA-256 mode available |

All browsers, certificate authorities, and security standards now prohibit SHA-1 for new certificates and signatures. If you encounter SHA-1 in legacy code, migrate to SHA-256.

## Command-line usage

**Linux / macOS:**

```bash
# Hash a string
echo -n "hello" | sha256sum
# 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824  -

# Hash a file
sha256sum /path/to/file.tar.gz

# Using OpenSSL (available on macOS and Linux)
echo -n "hello" | openssl dgst -sha256
# SHA2-256(stdin)= 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
```

**Windows (PowerShell):**

```powershell
Get-FileHash file.tar.gz -Algorithm SHA256
# Algorithm  Hash                                              Path
# SHA256     3A7BD3E2360A3D29EEA436FCFB7E44C735D117C42D1C...  file.tar.gz

# Or inline:
(Get-FileHash -Algorithm SHA256 -InputStream ([IO.MemoryStream]::new([Text.Encoding]::UTF8.GetBytes("hello")))).Hash
```

## Python example

```python
import hashlib

# Hash a string
digest = hashlib.sha256(b"hello").hexdigest()
print(digest)
# 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824

# Hash a large file without loading it all into memory
def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

print(sha256_file("/etc/hosts"))
```

The `hashlib` module is part of Python's standard library — no external packages needed.

## JavaScript example (Web Crypto API)

The `crypto.subtle.digest` API is available in all modern browsers and in Node.js (v15+):

```js
async function sha256(message) {
  const encoder = new TextEncoder();
  const data = encoder.encode(message);
  const hashBuffer = await crypto.subtle.digest("SHA-256", data);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map(b => b.toString(16).padStart(2, "0")).join("");
}

sha256("hello").then(console.log);
// 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
```

Note that `crypto.subtle` is asynchronous and returns a Promise. In Node.js you can also use the synchronous `crypto.createHash`:

```js
const crypto = require("crypto");
const hash = crypto.createHash("sha256").update("hello").digest("hex");
console.log(hash);
// 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
```

## SHA-256 vs SHA-512

SHA-512 produces a 512-bit (128 hex char) output and uses 64-bit word arithmetic, making it faster than SHA-256 on 64-bit hardware for large inputs. For most applications SHA-256 is sufficient — the 256-bit security level exceeds any near-future attack capability.

SHA-384 is a truncated variant of SHA-512 (384 bits) used in TLS 1.3 cipher suites.

## Try SHA-256 online

You can generate SHA-256 hashes instantly in your browser at [encodeonline.io](/). Paste any text, upload a file, or type a value and the tool computes the digest in real time — no data leaves your browser.
