---
title: "Password Entropy Explained: How to Measure Password Strength in Bits"
description: "Learn what password entropy means, how to calculate it in bits, and why it's the most accurate measure of password strength."
publishDate: 2026-06-07
updatedDate: 2026-06-07
author: "Editorial Team"
tags: ["password entropy", "password strength", "security", "bits", "randomness"]
draft: false
heroImage: "/images/blog/password-entropy-hero.png"
---

Password strength meters on most websites are largely theater. They check whether you included a capital letter or a symbol, but those rules tell you almost nothing about how hard a password actually is to crack. The real measure is **entropy** — a number expressed in bits that captures how unpredictable a password is, regardless of how it looks.

## What is password entropy?

Entropy is borrowed from information theory. In the context of passwords, entropy measures the number of possible values an attacker must search through before finding the correct password by brute force. The higher the entropy, the harder the search.

Entropy is expressed in **bits**. One bit of entropy means two possibilities. Two bits means four. Thirty bits means about one billion. Each additional bit doubles the search space.

```
Entropy (bits) → Possible values
10 bits        → 1,024
20 bits        → 1,048,576 (≈ 1 million)
30 bits        → 1,073,741,824 (≈ 1 billion)
40 bits        → 1,099,511,627,776 (≈ 1 trillion)
60 bits        → ≈ 1.15 × 10^18
80 bits        → ≈ 1.21 × 10^24
128 bits       → ≈ 3.4 × 10^38
```

The jump from 60 to 80 bits is not 20 more possible passwords — it is one million times more.

## The entropy formula

For a password chosen uniformly at random from a pool of characters:

```
Entropy (bits) = log2(pool_size ^ length)
               = length × log2(pool_size)
```

Where:
- `pool_size` is the number of distinct characters the generator draws from
- `length` is the number of characters in the password

### Pool sizes for common character sets

| Character set | Pool size |
|--------------|-----------|
| Digits only (0–9) | 10 |
| Lowercase letters (a–z) | 26 |
| Lowercase + digits | 36 |
| Mixed case letters | 52 |
| Mixed case + digits | 62 |
| Printable ASCII (no space) | 94 |
| Full printable ASCII (with space) | 95 |

### Worked examples

```python
import math

def entropy(pool_size, length):
    return length * math.log2(pool_size)

# 8-char lowercase-only password
print(f"{entropy(26, 8):.1f} bits")   # 37.6 bits — very weak

# 8-char with full printable ASCII
print(f"{entropy(95, 8):.1f} bits")   # 52.6 bits — marginal

# 12-char with full printable ASCII
print(f"{entropy(95, 12):.1f} bits")  # 78.9 bits — adequate for most uses

# 16-char with mixed case + digits
print(f"{entropy(62, 16):.1f} bits")  # 95.3 bits — strong

# 20-char with full printable ASCII
print(f"{entropy(95, 20):.1f} bits")  # 131.5 bits — excellent

# 4-word passphrase from a 7,776-word list (EFF wordlist)
print(f"{entropy(7776, 4):.1f} bits") # 51.7 bits — roughly 8-char ASCII

# 6-word passphrase from a 7,776-word list
print(f"{entropy(7776, 6):.1f} bits") # 77.5 bits — comparable to 12-char ASCII
```

## What different entropy levels mean in practice

### Under 40 bits — Weak

Passwords in this range are crackable in seconds to hours on a single modern GPU. This includes any 6-character password and most 8-character passwords that use only lowercase letters. Even online services with no rate limiting are at risk.

**Example:** An 8-character lowercase-only password has 37.6 bits. A cracking rig doing 10 billion guesses per second exhausts the entire space in under a millisecond.

### 40–60 bits — Marginal

Acceptable only for low-stakes accounts with strict rate limiting (e.g., a wifi password where the attacker would need physical proximity and the service locks out after a few attempts). Not suitable for any account that stores sensitive data.

### 60–80 bits — Adequate for online accounts

At 80 bits, an attacker doing 10 billion guesses per second would need over 37 million years to exhaust the search space by brute force. Online accounts with even basic rate limiting are effectively protected. This range is appropriate for most consumer accounts.

### 80–128 bits — Strong

This range is appropriate for high-value accounts (banking, email, work systems), encryption keys used for files, and any scenario where an attacker might have the password hash and can attack offline. Offline cracking with a botnet of thousands of GPUs is still impractical against 80-bit passwords.

### 128+ bits — Recommended for machine secrets

API keys, HMAC secrets, session tokens, and database credentials should live in this range. Many modern standards (NIST SP 800-132, for example) recommend 112 bits as a floor for derived keys, with 128+ preferred. A 20-character random ASCII password or a 32-byte random token both exceed 128 bits.

## Why length matters more than complexity

This is the core insight that entropy reveals. Consider two passwords:

- `P@ssw0rd!` — 9 characters, uses uppercase, lowercase, digits, symbols
- `xvnmqrbdkplw` — 12 characters, lowercase only

The "complex" password has entropy of about 55 bits. The lowercase-only password has entropy of about 56.5 bits — roughly the same, despite looking "simpler." But here is the critical difference: `P@ssw0rd!` is a predictable human pattern and would be tried in the first few thousand guesses by any serious attacker. The random lowercase string has the full 56.5 bits of entropy only if it was truly randomly generated.

A genuinely random 12-character lowercase password beats a human-chosen "complex" password nearly every time.

Going from 12 to 20 characters — without adding any special characters — increases entropy from 63.1 bits to 105.2 bits (using lowercase + digits). That is a 2^42 increase in search space, or over four trillion times harder.

## Entropy and passphrases

Passphrases draw from a wordlist rather than a character pool. The EFF long wordlist contains 7,776 words. Each word adds log2(7,776) ≈ 12.9 bits of entropy.

| Passphrase length | Entropy |
|-------------------|---------|
| 3 words | 38.8 bits |
| 4 words | 51.7 bits |
| 5 words | 64.6 bits |
| 6 words | 77.5 bits |
| 7 words | 90.4 bits |
| 8 words | 103.3 bits |

A 6-word EFF passphrase (77.5 bits) is roughly as strong as a 12-character random ASCII password (78.9 bits) and significantly easier to memorize. For master passwords — the one password you must remember — a 6–8 word passphrase is an excellent choice.

## The difference between theoretical and effective entropy

The formula above assumes the password was generated by a truly random process. Human-chosen passwords have much lower effective entropy because humans follow predictable patterns:

- Starting with a capital letter
- Ending with a digit or `!`
- Substituting `@` for `a`, `3` for `e`, `0` for `o`
- Using dictionary words as a base

Cracking tools exploit this. A "complex" human-chosen password that theoretically has 50 bits of entropy might have effective entropy of 20 bits or less once an attacker applies wordlist rules.

**True entropy requires machine-generated randomness.** Tools like [passwordgen.io](/) use the Web Crypto API (`crypto.getRandomValues()`), which is a cryptographically secure random number generator (CSPRNG). Every password generated there has entropy equal to the theoretical maximum — length × log2(pool_size).

## Calculating entropy for specific password types

### Random character password (20 chars, full ASCII)

```
pool_size = 95 (all printable ASCII)
length    = 20
entropy   = 20 × log2(95)
          = 20 × 6.57
          = 131.5 bits
```

### 4-digit PIN

```
pool_size = 10
length    = 4
entropy   = 4 × log2(10)
          = 4 × 3.32
          = 13.3 bits
```

This is why PINs rely entirely on rate limiting and lockout — their entropy is too low to survive any offline attack.

### 128-bit hex token (like `secrets.token_hex(16)`)

```
pool_size = 16 (hex digits: 0–9, a–f)
length    = 32
entropy   = 32 × log2(16)
          = 32 × 4
          = 128 bits
```

### UUID v4

UUIDs contain 122 bits of random data. This puts them solidly above 128 bits of entropy and makes them suitable for session tokens — though they are long at 36 characters.

## How entropy relates to cracking time

Here is a rough guide based on an offline attack with a modern GPU (roughly 10 billion MD5 hashes per second — bcrypt and Argon2 are far slower):

| Entropy | Search space | Time at 10B/s |
|---------|-------------|---------------|
| 40 bits | 1.1 trillion | ~110 seconds |
| 60 bits | 1.15 × 10^18 | ~3,650 years |
| 80 bits | 1.21 × 10^24 | ~3.8 billion years |
| 128 bits | 3.4 × 10^38 | effectively forever |

Against modern password hashing algorithms like Argon2id (which might allow only 1,000 guesses per second on dedicated hardware), 60 bits is already astronomically hard to crack offline. The entropy requirements in the table above are conservative and assume a weak hashing function like MD5 or SHA-1 — which is why using proper password hashing matters too.

## Summary

Password entropy is the only rigorous measure of password strength. The formula is simple: `length × log2(pool_size)`. For most user accounts, aim for 80+ bits; for high-value accounts and secrets, aim for 128+ bits.

The fastest path to high entropy is longer passwords generated by a CSPRNG. Use [passwordgen.io](/) to generate passwords at any desired length with any character set, and the entropy calculation is shown directly so you can see exactly how strong each password is.
