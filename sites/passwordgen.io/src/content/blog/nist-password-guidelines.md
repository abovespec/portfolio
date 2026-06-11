---
title: "NIST Password Guidelines 2024: What SP 800-63B Actually Says"
description: "A plain-language summary of NIST SP 800-63B password guidelines: no complexity rules, no forced rotation, check against breached passwords, and more."
publishDate: 2026-06-07
updatedDate: 2026-06-07
author: "Editorial Team"
tags: ["nist", "password guidelines", "sp 800-63b", "security policy", "password"]
draft: false
heroImage: "/images/blog/nist-password-guidelines-hero.png"
---

For decades, organizations followed password rules that security researchers now know make things worse: mandatory capital letters, required symbols, 90-day rotation, security questions. Most of those rules came from a 2003 NIST document — one whose own author later said he got it wrong.

The current standard, **NIST Special Publication 800-63B** ("Digital Identity Guidelines: Authentication and Lifecycle Management"), was first published in 2017 and has been updated since. It represents a fundamental reversal of much of the old advice. If your organization still enforces complexity rules and regular rotation, it is following guidance that NIST itself has abandoned.

This article summarizes the key requirements in plain language and explains the reasoning behind each one.

## Where NIST 800-63B comes from

NIST (the National Institute of Standards and Technology) is a U.S. federal agency that publishes technical standards. SP 800-63B is part of the 800-63 suite covering digital identity. While formally aimed at federal agencies and their contractors, it has become the baseline reference for password policy across the private sector globally.

The document is freely available at [pages.nist.gov/800-63-3/sp800-63b.html](https://pages.nist.gov/800-63-3/sp800-63b.html). The NIST 800-63-4 revision (second public draft published in 2022–2023) further strengthens these recommendations.

## Key guideline 1: Do not mandate complexity rules

**Old advice:** Passwords must contain uppercase letters, lowercase letters, digits, and at least one special character.

**NIST 800-63B says:** Verifiers (systems that check passwords) should not impose composition rules.

### Why the old rule is counterproductive

Complexity requirements were intended to increase the search space for attackers. In practice, they train users to choose predictable patterns:

- Required capital? Put it at the start.
- Required number? Put `1` at the end.
- Required symbol? Add `!` at the end.

The result is passwords like `Password1!` — technically compliant, genuinely weak. Attackers know these patterns and target them first in their cracking rules.

True entropy comes from randomness, not from rule compliance. A randomly generated 16-character lowercase password has more entropy than a human-chosen 10-character password with all four character types.

NIST's position: complexity requirements "provide no real additional security benefit" and create friction that leads users toward reuse and predictable patterns.

## Key guideline 2: Enforce a minimum length of 8; recommend 15+

NIST sets the minimum at 8 characters — an absolute floor, not a target. For general-purpose passwords, NIST recommends a minimum of 15 characters.

Systems must also:
- Accept passwords up to at least 64 characters
- Not silently truncate passwords
- Allow all printable ASCII characters (Unicode support is also recommended)

The maximum-length requirement is important because it allows users to employ passphrases and password manager-generated credentials of any length. Systems that cap passwords at 16 or 20 characters are non-compliant with NIST and frustrate users who want to use stronger credentials.

## Key guideline 3: Check new passwords against breach lists

This is the most technically significant addition in 800-63B. When a user sets or changes a password, the system should check it against:

- Known breached password lists (e.g., the Have I Been Pwned corpus of over 800 million compromised passwords)
- Commonly used passwords (the top 10,000 most popular passwords)
- Dictionary words
- Repetitive or sequential characters (`aaaaaa`, `123456`)
- Context-specific terms (the service name, the user's username, obvious variations)

If the password appears in any of these lists, the system should reject it and prompt the user to choose a different one.

### Why this matters

Credential stuffing attacks work by taking passwords from one breach and testing them elsewhere. If an attacker knows that `hunter2` is in millions of breach databases, it is a useless password no matter how long ago it was set.

The NIST approach shifts the focus from password appearance (does it have a symbol?) to password exposure (has this password been seen before?). A genuinely random 12-character password that has never appeared in a breach is far safer than a "complex" password taken from a wordlist.

The [Have I Been Pwned API](https://haveibeenpwned.com/API/v3#PwnedPasswords) uses k-anonymity — only a hash prefix is sent — so checking a password against the breach corpus does not expose the password itself.

## Key guideline 4: Do not force periodic rotation

**Old advice:** Passwords expire every 90 days and must be changed.

**NIST 800-63B says:** Do not require passwords to expire on a schedule. Only require a change when there is evidence of compromise.

### Why forced rotation makes things worse

Regular expiration leads directly to predictable patterns:
- `Summer2025!` → `Fall2025!` → `Winter2026!`
- `Password1` → `Password2` → `Password3`

Users know they have to change passwords frequently, so they make the minimum possible change. Attackers know this and test predictable variations.

Forced rotation also increases support costs (password reset requests spike before and after reset windows) and trains users to distrust the password system.

NIST's position: "Verifiers should not require memorized secrets to be changed arbitrarily (e.g., periodically)." The only time to require a change is when there is a confirmed or suspected compromise.

## Key guideline 5: No hints, no security questions

**Old advice:** Provide a password hint. Set security questions like "What is your mother's maiden name?"

**NIST 800-63B says:** Do not allow password hints. Do not use knowledge-based authentication (KBA — security questions).

### Why security questions fail

Security questions have two fatal flaws:

1. **The answers are often guessable or public.** Mother's maiden name, high school mascot, childhood street — these are frequently discoverable through social media, public records, or social engineering.

2. **Users lie to make answers memorable, making them predictable.** If users always answer "Pizza" to any security question to make it easy to remember, that answer is easy to guess.

Security questions represent a secret that is significantly easier to guess than a good password, but they are sometimes used to bypass the password entirely. NIST eliminated them from compliant authentication systems entirely.

Password hints have the same problem — if your hint for `P@ssw0rd1` is "my usual," an attacker who sees that hint immediately has a good candidate.

## Key guideline 6: Allow all printable ASCII and spaces

NIST explicitly requires that systems accept all printable ASCII characters, including spaces. Spaces are specifically mentioned because they allow users to enter passphrases (sequences of words separated by spaces) as passwords.

Systems must:
- Not reject passwords based on character type (e.g., "symbols not allowed")
- Accept spaces within passwords (not just trim them)
- Ideally support Unicode characters (for international users)

Blocking certain characters — a common "security" measure — reduces the available character pool and actually decreases entropy while frustrating users with non-US keyboard layouts.

## Key guideline 7: Use proper password hashing

This guideline applies to the system storing passwords, not the user creating them, but it matters enormously:

- Passwords must be hashed with a one-way function before storage
- NIST recommends memory-hard functions: **Argon2** (recommended), **bcrypt**, **scrypt**, or **PBKDF2** with SHA-256 and at least 600,000 iterations
- Each password must be salted with at least 32 bits of random salt, unique per password
- Plain-text storage is never acceptable

The purpose of a memory-hard hash is to make offline cracking expensive. Even if an attacker steals a database of hashed passwords, cracking them should require significant time and compute resources. MD5 or SHA-1 (even salted) does not meet this standard — a modern GPU can test billions of MD5 hashes per second.

## Key guideline 8: Use rate limiting and lockout instead of complexity

Rather than burdening users with complexity requirements, NIST recommends protecting accounts through:

- **Rate limiting** on authentication attempts
- **Lockout** after a specified number of failures (NIST suggests 100 failed attempts is a reasonable maximum before requiring intervention, though tighter limits are appropriate for high-value accounts)
- **Multi-factor authentication** (which NIST strongly recommends adding wherever possible)

These controls protect accounts at the system level rather than relying on users to create unpredictable passwords — which, as the research consistently shows, they cannot reliably do.

## Contrast: Old advice vs. NIST 800-63B

| Old guidance | NIST 800-63B |
|-------------|-------------|
| Require uppercase + lowercase + digit + symbol | Do not impose composition rules |
| Minimum 8 characters | Minimum 8; recommend 15+ |
| Expire passwords every 90 days | Change only on evidence of compromise |
| Allow up to 16 characters | Allow at least 64 characters |
| Use security questions for recovery | Do not use knowledge-based authentication |
| Allow common passwords | Check against breach corpus and reject common passwords |
| Truncate long passwords | Never truncate; store full hash |
| Password hints allowed | Do not allow password hints |

## What this means for users

Even if your workplace has not caught up to NIST 800-63B, you can apply these principles yourself:

1. **Use a password manager** to generate and store long, random passwords — no need to remember them.
2. **Use 15+ characters** for important accounts; 20+ for high-value ones.
3. **Never reuse passwords.** Each account gets a unique credential.
4. **Check breaches.** [Have I Been Pwned](https://haveibeenpwned.com) shows whether your passwords have appeared in known breaches.
5. **Enable two-factor authentication** on every account that offers it.

For generating compliant passwords — long, random, drawn from a full character set — use [passwordgen.io](/). It generates passwords in your browser using a CSPRNG, displays entropy, and never transmits your passwords to any server.

## Summary

NIST SP 800-63B replaced decades of security theater with evidence-based guidance: longer is better, random beats complex, rotation is counterproductive, and breach-list checking matters more than symbol requirements. The standard is freely available, widely cited, and the right baseline for any organization or individual thinking seriously about password security.
