---
title: "Encoding vs Encryption vs Hashing: What's the Difference?"
description: "Encoding, encryption, and hashing are three distinct operations often confused with each other. Learn what each does, when to use it, and why Base64 is not encryption."
publishDate: 2026-06-07
updatedDate: 2026-06-07
author: "Editorial Team"
tags: ["encoding", "encryption", "hashing", "security", "cryptography"]
draft: false
heroImage: "/images/blog/encoding-vs-encryption-hero.png"
---

"I'm encoding the password in Base64 to keep it secure." This sentence appears in real codebases and real pull requests — and it is dangerously wrong. Encoding, encryption, and hashing are three entirely different operations. Conflating them is one of the most common security mistakes developers make.

This article gives you a precise mental model for each concept.

## The three operations at a glance

| Property | Encoding | Encryption | Hashing |
|----------|----------|------------|---------|
| Reversible? | Yes (no key needed) | Yes (requires the key) | No |
| Requires a secret? | No | Yes | No |
| Purpose | Format transformation | Confidentiality | Integrity / fingerprinting |
| Examples | Base64, URL encoding, HTML entities | AES, RSA, ChaCha20 | SHA-256, MD5, bcrypt |

---

## Encoding

Encoding converts data from one representation to another using a publicly known, reversible scheme. There is no key, no secret, and no security guarantee. Anyone who knows the encoding scheme can decode the data immediately.

### Base64

Base64 represents arbitrary binary data using 64 printable ASCII characters (A–Z, a–z, 0–9, +, /). It was invented to safely transmit binary data through text-only channels like email.

```python
import base64

encoded = base64.b64encode(b"hello world")
# b'aGVsbG8gd29ybGQ='

decoded = base64.b64decode(b"aGVsbG8gd29ybGQ=")
# b'hello world'
```

The encoded value `aGVsbG8gd29ybGQ=` reveals **nothing** about security — it is trivially reversible by any person or program. Storing a password as Base64 provides zero protection.

### URL encoding (percent-encoding)

URL encoding converts characters that are not safe in a URL context into a `%XX` hexadecimal escape:

```
hello world  →  hello%20world
email@host   →  email%40host
```

The encoding is defined in RFC 3986 and is fully reversible. Every browser, HTTP library, and command-line tool can decode it.

### HTML entity encoding

HTML entity encoding replaces characters that have special meaning in HTML markup:

```
<script>  →  &lt;script&gt;
"hello"   →  &quot;hello&quot;
```

HTML encoding is a critical security control for XSS prevention — but it is still just encoding, not encryption. It protects against *injection*, not confidentiality. The character `<` encoded as `&lt;` is universally decodable.

### When to use encoding

- Transmitting binary data over a text channel (Base64 in email attachments, data URIs)
- Making data safe for use in a specific context (URL encoding query strings, HTML encoding output)
- Wire formats that require specific character sets (JSON, XML, HTTP headers)

Encoding is never a substitute for encryption or hashing.

---

## Encryption

Encryption transforms plaintext into ciphertext using a cryptographic algorithm and a **key**. The ciphertext is meaningless without the key. The process is reversible — decryption with the correct key restores the original plaintext.

### Symmetric encryption (AES)

Symmetric encryption uses the same key for encryption and decryption. AES (Advanced Encryption Standard) is the dominant symmetric cipher:

```python
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

key = os.urandom(32)      # 256-bit AES key, keep secret
nonce = os.urandom(12)    # 96-bit nonce, unique per message

aead = AESGCM(key)
ciphertext = aead.encrypt(nonce, b"secret message", None)
# ciphertext is opaque bytes — meaningless without key + nonce

plaintext = aead.decrypt(nonce, ciphertext, None)
# b"secret message"
```

AES-GCM also provides authentication — it detects if the ciphertext was tampered with. This is the recommended mode for modern symmetric encryption.

### Asymmetric encryption (RSA)

Asymmetric encryption uses a key pair: a public key for encryption, a private key for decryption. RSA is the most common asymmetric algorithm:

```python
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

ciphertext = public_key.encrypt(
    b"secret message",
    padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
)

plaintext = private_key.decrypt(
    ciphertext,
    padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
)
# b"secret message"
```

The public key can be distributed freely. Only the holder of the private key can decrypt.

### When to use encryption

- Storing sensitive data that must be retrieved later (database field encryption)
- Transmitting private data over an untrusted network (TLS/HTTPS)
- Encrypting files or backups at rest
- End-to-end messaging (Signal Protocol, PGP)

The key question for encryption: **does the application need to retrieve the original value?** If yes, use encryption. If no (e.g., passwords), use hashing.

---

## Hashing

A cryptographic hash function maps an input of any size to a fixed-size output (the "digest" or "hash"). Hashing is **one-way**: given a hash, it is computationally infeasible to recover the original input. There is no key.

### SHA-256

```python
import hashlib

digest = hashlib.sha256(b"hello").hexdigest()
# "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"

# Same input always → same output
# Different input → completely different output (avalanche effect)
hashlib.sha256(b"Hello").hexdigest()
# "185f8db32921bd46d35cc5200032bb989d71ab8125a5657ad17bec5e3bda2f2"
```

### bcrypt for passwords

For password storage, use a dedicated password hashing function that is deliberately slow:

```python
import bcrypt

# Hash a password (bcrypt automatically generates and stores the salt)
hashed = bcrypt.hashpw(b"user_password", bcrypt.gensalt())
# b'$2b$12$eImiTXuWVxfM37uY4JANjQ...'

# Verify (never compare hashes directly — use constant-time comparison)
valid = bcrypt.checkpw(b"user_password", hashed)  # True
```

bcrypt's work factor can be increased over time to keep pace with faster hardware.

### When to use hashing

- **Passwords:** Store the hash, never the plaintext. Verify by hashing the input and comparing.
- **File integrity:** Hash a file to detect corruption or tampering.
- **Data deduplication:** Hash content to detect duplicates without comparing byte-by-byte.
- **Digital signatures:** Sign the hash of a document (not the document itself).
- **Caching:** Use a hash as a cache key for the content.

The key question for hashing: **does the application ever need the original value?** If no, hash it.

---

## The "Base64 is encryption" misconception

This mistake surfaces in several forms:

- "We Base64-encode passwords before storing them"
- "The API key is safe because it's Base64-encoded in the header"
- "We obfuscate the config file by Base64-encoding it"

Base64 adds **zero security**. It takes about three seconds to decode:

```bash
echo "aGVsbG8gd29ybGQ=" | base64 -d
# hello world
```

Any attacker who gains access to a Base64-encoded password or API key has immediate access to the plaintext. Base64 is a **format transformation**, not a security measure.

**The correct approaches:**

| Goal | Wrong approach | Correct approach |
|------|---------------|-----------------|
| Store passwords | Base64 or MD5 | bcrypt / Argon2 |
| Protect API keys at rest | Base64 | AES-256 encryption |
| Verify file integrity | CRC32 | SHA-256 |
| Transmit binary over email | No encoding | Base64 (this is what it's for) |

---

## Security implications

Using encoding where encryption is needed is a security vulnerability. Examples of real-world mistakes:

**HTTP Basic Authentication** sends credentials as `Base64(username:password)` in the `Authorization` header. This is specified in RFC 7617 — but it is **not** secure on its own. Basic Auth must be used over HTTPS (TLS encryption) to protect the credential. Without TLS, the Base64 is trivially decoded by anyone who intercepts the network traffic.

**"Security through obscurity"** is the mistaken belief that encoding or obfuscation provides meaningful protection. Attackers routinely recognize and decode Base64, ROT13, hex encoding, and similar transformations in seconds. Rely on proven cryptographic algorithms, not encoding tricks.

---

## Decision guide

```
Do you need to reconstruct the original value?
├── YES → Is the data confidential?
│         ├── YES → Encrypt it (AES for symmetric, RSA/ECDH for asymmetric)
│         └── NO  → Encode it (Base64, URL encoding, etc.)
└── NO  → Hash it
          ├── Is it a password? → bcrypt / Argon2 / scrypt
          └── Is it data? → SHA-256 / SHA-3
```

---

## Try encoding tools online

[encodeonline.io](/) lets you experiment with Base64 encoding and decoding, URL encoding, HTML entities, and hash generation (MD5, SHA-256) directly in your browser. Understanding the output of each operation side by side helps build the intuition to choose the right tool for each security context.
