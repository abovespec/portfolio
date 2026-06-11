---
title: "MD5 vs SHA-256: Which Hash Algorithm Should You Use?"
description: "MD5 produces a 128-bit digest and has known collision vulnerabilities. SHA-256 produces 256 bits with no known practical attacks. Learn when to use each and how to migrate."
publishDate: 2026-06-07
updatedDate: 2026-06-07
author: "Editorial Team"
tags: ["md5", "sha256", "hash functions", "cryptography", "security"]
draft: false
heroImage: "/images/blog/md5-vs-sha256-hero.png"
---

MD5 and SHA-256 are both cryptographic hash functions, but they occupy very different places in the security landscape. MD5, designed by Ronald Rivest in 1991, is fast, compact, and broken. SHA-256, part of NIST's SHA-2 family published in 2001, is the current standard for security-critical applications. Understanding the difference tells you when each is appropriate and when switching is mandatory.

## Output size and format

**MD5** produces a 128-bit digest, represented as 32 lowercase hexadecimal characters:

```
MD5("hello") = 5d41402abc4b2a76b9719d911017c592
               ←————— 32 hex chars = 128 bits —————→
```

**SHA-256** produces a 256-bit digest, represented as 64 lowercase hexadecimal characters:

```
SHA-256("hello") = 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
                   ←——————————————— 64 hex chars = 256 bits ————————————————→
```

The longer output of SHA-256 means a vastly larger search space for any attacker trying to find collisions or invert the hash.

## Speed comparison

MD5 is faster than SHA-256:

| Algorithm | Throughput (typical CPU, single core) |
|-----------|--------------------------------------|
| MD5 | ~500 MB/s |
| SHA-256 | ~250 MB/s |
| SHA-256 (hardware AES-NI / SHA-NI) | ~3,000 MB/s+ |

Speed is a double-edged sword. For checksumming large files where security is not a concern, MD5's speed is an advantage. For password hashing and security contexts, MD5's speed is a liability — attackers can compute billions of MD5 hashes per second using a GPU.

## MD5 vulnerabilities

### Collision attacks

A collision is when two different inputs produce the same hash output. Collisions are catastrophic for security applications: an attacker who can craft a malicious file with the same MD5 hash as a legitimate file can impersonate it.

MD5 collision attacks were first demonstrated theoretically in 1996, and practical attack tools became available in the early 2000s. The most significant demonstrations:

- **2004 (Wang et al.):** Practical MD5 collision algorithm published. Collisions could be found in hours on a single PC.
- **2008 (Sotirov et al.):** Researchers used MD5 collisions to forge a rogue Certificate Authority certificate, enabling them to impersonate any HTTPS website. This directly led browser vendors to remove MD5 from certificate trust.
- **2012 (Flame malware):** The Flame cyberespionage malware used a chosen-prefix MD5 collision to forge a Windows Update certificate, allowing it to spread via Microsoft's infrastructure.

### GPU brute force

Even without collision attacks, MD5's speed makes it unsuitable for password storage. An RTX 4090 GPU can compute approximately 164 billion MD5 hashes per second. A leaked MD5-hashed password database is recoverable for common passwords in seconds using dictionary and rule-based attacks.

```bash
# Demonstrating MD5 speed with hashcat (educational context only)
# hashcat -m 0 hashes.txt wordlist.txt
# MD5 rate: ~164 GH/s on RTX 4090
```

### What MD5 is NOT vulnerable to

MD5 does not have known **pre-image attacks** at a practical scale. Given only an MD5 hash, brute-forcing the exact original input is still computationally expensive for long, random inputs. The attacks are primarily collision-based.

## SHA-256 current status

As of 2026, SHA-256 has no known practical attacks:

- No collisions found
- No pre-image attacks
- No length-extension attacks (unlike MD5 and SHA-1, SHA-256 is vulnerable to length extension attacks in certain API misuse patterns — use HMAC-SHA256 to avoid this)
- NIST approved, no deprecation in sight

The theoretical birthday-attack collision resistance of SHA-256 is 2^128 operations — far beyond the capability of any foreseeable hardware.

## Side-by-side comparison

| Property | MD5 | SHA-256 |
|----------|-----|---------|
| Output size | 128 bits (32 hex) | 256 bits (64 hex) |
| Speed (software) | ~500 MB/s | ~250 MB/s |
| Collision resistance | Broken (practical attacks) | No known attack |
| Pre-image resistance | No known practical attack | No known attack |
| NIST status | Not recommended for security | Current standard |
| TLS support | Removed | Required |
| Suitable for passwords | No | No (use bcrypt/Argon2) |
| Suitable for checksums | Acceptable (non-adversarial) | Preferred |
| Suitable for digital signatures | No | Yes |

## When MD5 is still acceptable

MD5 remains usable in **non-adversarial, non-security contexts**:

**Non-adversarial deduplication.** If you want to detect duplicate files in your own file system (where no attacker is crafting collisions), MD5 checksums work fine. Git originally used SHA-1 for similar reasons and is only now migrating to SHA-256.

**Checksums for accidental corruption.** Detecting random bit-flips in a downloaded file (corruption, not tampering) does not require collision resistance. MD5 is sufficient. However, SHA-256 is now the industry default for download checksums even in this context, because the cost is negligible.

**Hash table / cache keys.** Using MD5 as a hash key in a cache where collisions would only cause cache misses (not security issues) is acceptable.

**Legacy system compatibility.** If you interface with a legacy API or database that already uses MD5 and you have no control over it, you may not be able to change it immediately. Document the limitation and prioritize migration.

## When SHA-256 is required

Use SHA-256 (or stronger) wherever security matters:

**Digital signatures.** All modern PKI uses SHA-256 or SHA-384. SHA-1 signatures are rejected by browsers and operating systems.

**TLS certificates.** Certificate fingerprints and signatures use SHA-256. MD5 certificates have been rejected since 2008.

**File integrity for security-sensitive software.** Package managers (apt, brew, npm) all use SHA-256 for package integrity.

**HMAC for authentication.** HMAC-SHA256 is the standard for signing API requests, webhook payloads, and session tokens.

**Blockchain and distributed systems.** Bitcoin, Ethereum, and most blockchain systems use SHA-256 or Keccak-256.

## Password hashing: neither MD5 nor SHA-256

A critical point: for **password storage**, neither MD5 nor SHA-256 alone is appropriate. Both are general-purpose hash functions designed to be fast. Password hashing requires deliberately slow algorithms:

| Algorithm | Why it's suitable for passwords |
|-----------|--------------------------------|
| bcrypt | Configurable work factor, built-in salting |
| Argon2id | Memory-hard, GPU-resistant, 2015 PHC winner |
| scrypt | Memory-hard, configurable time and memory |
| PBKDF2-HMAC-SHA256 | NIST/FIPS approved, NIST recommends 600,000+ iterations |

```python
import bcrypt

# CORRECT: bcrypt for password storage
password = b"user_password"
hashed = bcrypt.hashpw(password, bcrypt.gensalt(rounds=12))

# WRONG: MD5 for password storage
import hashlib
bad_hash = hashlib.md5(b"user_password").hexdigest()  # Never do this
```

## Code examples

### Python

```python
import hashlib

text = "The quick brown fox jumps over the lazy dog"
data = text.encode("utf-8")

md5_hash = hashlib.md5(data).hexdigest()
sha256_hash = hashlib.sha256(data).hexdigest()

print(f"MD5    ({len(md5_hash)} chars): {md5_hash}")
print(f"SHA256 ({len(sha256_hash)} chars): {sha256_hash}")

# MD5    (32 chars): 9e107d9d372bb6826bd81d3542a419d6
# SHA256 (64 chars): d7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592
```

### Command line

```bash
# MD5
echo -n "hello" | md5sum
# 5d41402abc4b2a76b9719d911017c592  -

# SHA-256
echo -n "hello" | sha256sum
# 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824  -

# File hash
md5sum file.tar.gz
sha256sum file.tar.gz
```

### JavaScript

```js
async function compareHashes(text) {
  const data = new TextEncoder().encode(text);

  // SHA-256 via Web Crypto API
  const sha256Buffer = await crypto.subtle.digest("SHA-256", data);
  const sha256Hex = Array.from(new Uint8Array(sha256Buffer))
    .map(b => b.toString(16).padStart(2, "0"))
    .join("");

  console.log("SHA-256:", sha256Hex);
  // Note: Web Crypto API does not support MD5 — it's excluded intentionally
}

compareHashes("hello");
```

The Web Crypto API deliberately excludes MD5 and SHA-1, signaling that these algorithms should not be used in new security code.

## Migrating from MD5 to SHA-256

If you have an existing system using MD5 for checksums or identifiers:

1. **Add a SHA-256 column** to your database alongside the existing MD5 column.
2. **Backfill:** compute SHA-256 for all existing records (the original data must still be available).
3. **Dual-write:** for new records, write both MD5 and SHA-256.
4. **Switch reads:** update all queries and validation logic to use SHA-256.
5. **Drop MD5:** once all records have SHA-256 and no code reads MD5, remove the column.

For password databases where you only stored MD5 hashes (and thus cannot recover the plaintext), the migration strategy is:

1. On next login, verify with MD5 (legacy).
2. Immediately re-hash the plaintext login credential with bcrypt/Argon2.
3. Mark the account as migrated.
4. Force a password reset for accounts that never log in after a cutoff date.

## Try it online

Generate MD5 and SHA-256 hashes side by side at [encodeonline.io](/). Paste any text or upload a file to see both digests instantly — useful for understanding the output size difference and verifying your own implementations.
