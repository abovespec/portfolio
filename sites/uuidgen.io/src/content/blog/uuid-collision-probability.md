---
title: "UUID Collision Probability: How Likely Is a UUID v4 Collision?"
description: "Understand the actual math behind UUID v4 collision probability. Covers the birthday paradox, 122 random bits, practical thresholds, and when to worry about RNG quality."
publishDate: 2026-06-07
updatedDate: 2026-06-07
author: "Editorial Team"
tags: ["uuid", "uuid v4", "collision", "probability", "security"]
draft: false
---

"What are the chances two UUIDs are the same?" is one of the most common questions developers ask when first using UUIDs. The short answer is: the probability is so small that for any realistic application, you can treat it as zero. But understanding the actual math helps you make informed decisions — and explains when you should care.

## What makes UUID v4 random

UUID v4 is defined by RFC 4122 as a UUID where 122 of the 128 bits are filled with cryptographically random data. The remaining 6 bits are fixed:

- 4 bits encode the version (always `0100` for v4)
- 2 bits encode the variant (always `10` for RFC 4122)

```
xxxxxxxx-xxxx-4xxx-[89ab]xxx-xxxxxxxxxxxx
              ↑    ↑
          version  variant
```

This means the total number of distinct UUID v4 values is:

```
2^122 = 5,316,911,983,139,663,491,615,228,241,121,378,304
      ≈ 5.3 × 10^36
```

That's 5.3 undecillion possible values. To put it in perspective: if you stacked a sheet of paper for every possible UUID v4, the stack would extend beyond the observable universe — many times over.

## The birthday paradox applied to UUIDs

The naive approach to collision probability — "what's the chance the next UUID matches an existing one?" — dramatically underestimates the real risk. The correct framework is the birthday paradox.

The birthday paradox says: in a group of just 23 people, there's a greater than 50% chance two share a birthday. This seems counterintuitive until you realize you're comparing every possible pair, not just pairs involving one specific person.

For UUIDs, the birthday paradox formula gives us the approximate number of UUIDs `n` needed before the collision probability exceeds 50%:

```
n ≈ sqrt(2 × ln(2) × 2^122)
n ≈ sqrt(2 × 0.693 × 5.3 × 10^36)
n ≈ 2.71 × 10^18
```

That's **2.71 × 10^18** — approximately 2.7 billion billion UUIDs — before there's a 50% chance of any collision. This number is so large it has no practical meaning for any software system.

## Putting the numbers in context

To understand just how safe UUID v4 is, consider these scenarios:

**If every person on Earth generated UUIDs:**

With 8 billion people each generating 1 million UUIDs per day, you'd produce:

```
8 × 10^9 people × 10^6 UUIDs/day = 8 × 10^15 UUIDs/day
```

At this rate, to reach 2.7 × 10^18 total UUIDs, you'd need:

```
2.7 × 10^18 / 8 × 10^15 ≈ 337 days
```

Even if every person on Earth generated a million UUIDs every day for a year, the collision probability would still be well below 1%.

**If you generate 1 billion UUIDs per second for 100 years:**

```
10^9 UUIDs/s × 3.15 × 10^7 s/year × 100 years ≈ 3.15 × 10^18 UUIDs
```

At that generation rate sustained for a century, the probability of at least one collision is approximately:

```
P ≈ 1 - e^(-n²/(2 × 2^122))
P ≈ 1 - e^(-(3.15 × 10^18)²/(2 × 5.3 × 10^36))
P ≈ 1 - e^(-0.936)
P ≈ 0.61 (about 61%)
```

In other words, generating one billion UUIDs per second for a full century gets you into meaningful collision territory — but no realistic application comes anywhere close to this volume.

**Practical perspective for most applications:**

If your application generates 10,000 UUIDs per day, you'd need to run for over 74 billion years (roughly 5 times the age of the universe) before reaching even a 0.1% collision probability.

## The actual collision probability formula

For `n` generated UUIDs and a total UUID space of `N = 2^122`, the approximate probability of at least one collision is:

```
P(collision) ≈ 1 - e^(-n(n-1)/(2N))

For small n/N ratios (which is always the case in practice):
P(collision) ≈ n² / (2N)
```

Some concrete examples:

| UUIDs generated | Collision probability |
|----------------|----------------------|
| 1,000 | ~9.4 × 10^-29 (effectively zero) |
| 1,000,000 | ~9.4 × 10^-23 (effectively zero) |
| 1,000,000,000 | ~9.4 × 10^-17 (effectively zero) |
| 1,000,000,000,000 | ~9.4 × 10^-11 (still negligible) |
| 2.7 × 10^18 | ~50% |

## When RNG quality matters more than math

The theoretical collision probability assumes your random number generator produces truly uniform, cryptographically random bits. In practice, the greatest real-world UUID collision risk is not from probability — it's from poor random number generation.

**Problematic scenarios:**

- **Seeded PRNG with the same seed.** If multiple processes all start with the same seed (e.g., seed based on startup time with second precision), they can generate the same sequence of UUIDs.
- **Virtualization without entropy.** Newly spun-up VMs or containers sometimes have depleted entropy pools and fall back to weak randomness until the system accumulates entropy.
- **Non-cryptographic PRNG.** Libraries using `Math.random()` in older JavaScript environments or `rand()` in C generate predictable sequences unsuitable for UUID generation.
- **Forked processes sharing PRNG state.** If a process forks after seeding a PRNG, both the parent and child can produce the same sequence.

**How to ensure good randomness:**

```python
# Python's uuid module uses os.urandom() — cryptographically secure by default
import uuid
uid = uuid.uuid4()  # safe
```

```javascript
// The 'uuid' npm package uses crypto.randomUUID() or the Web Crypto API
import { v4 as uuidv4 } from 'uuid';
const uid = uuidv4();  // safe

// Also available natively in Node.js 14.17+ and modern browsers:
const uid = crypto.randomUUID();  // safe
```

```go
// github.com/google/uuid uses crypto/rand
import "github.com/google/uuid"
uid := uuid.New()  // safe
```

Always use a cryptographically secure random number generator (CSPRNG). Standard UUID libraries do this correctly — the risk arises when developers implement their own UUID generation or use non-cryptographic randomness.

## UUID v5 for deterministic IDs

If you need a UUID derived from known data (so that the same input always produces the same UUID), use UUID v5 rather than v4. UUID v5 hashes a namespace UUID and a name string using SHA-1:

```python
import uuid

# Always produces the same UUID for the same namespace + name
canonical_id = uuid.uuid5(uuid.NAMESPACE_URL, "https://example.com/users/alice")
# Output: da6f9e7b-7d98-5a78-9df0-a8a5a75cf66b (deterministic)
```

UUID v5 values have zero collision probability for distinct inputs (barring SHA-1 preimage collisions, which are not a practical concern). They're useful for:

- Converting external identifiers (URLs, email addresses, product SKUs) to UUIDs deterministically
- Content-addressable storage
- Idempotent record creation (insert with a known UUID derived from content)

For more on this topic, see [*How to Generate a UUID: Online, CLI, Python, JavaScript, and SQL*](/blog/generate-uuid).

## UUID v7 and collision probability

UUID v7 replaces the 48-bit timestamp prefix that UUID v1 used with a Unix millisecond timestamp, then fills the remaining ~74 bits with random data. With 74 random bits, the collision probability is:

```
2^74 ≈ 1.9 × 10^22 possible values per millisecond
```

Even in the astronomically unlikely case of a collision in the same millisecond, the timestamp component guarantees uniqueness across different milliseconds. In practice, UUID v7 is just as collision-safe as v4 for any real workload.

## Summary

UUID v4 collision probability is not a practical concern for any real software system:

- You'd need to generate **2.7 × 10^18** UUIDs before collision probability reaches 50%
- At **1 billion UUIDs per second** it would take **86 years** to even approach that threshold
- The real collision risk comes from **poor RNG quality**, not mathematical probability
- Use established UUID libraries that rely on CSPRNGs
- Use **UUID v5** when you need deterministic (non-random) UUIDs from known inputs

Generate cryptographically secure UUID v4 values instantly at [uuidgen.io](/).
