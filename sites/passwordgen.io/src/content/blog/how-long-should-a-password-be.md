---
title: "How Long Should a Password Be? NIST Guidance and Practical Recommendations"
description: "Find out how long a password should be. Covers NIST's current guidance, how length affects brute-force resistance, and recommendations by account type."
publishDate: 2026-06-07
updatedDate: 2026-06-07
author: "Editorial Team"
tags: ["password length", "password", "nist", "security", "brute force"]
draft: false
heroImage: "/images/blog/how-long-should-a-password-be-hero.png"
---

If you have ever wondered whether your 8-character password is good enough — it is not. The single most important thing you can do to make a password stronger is to make it longer. More characters mean exponentially more possible combinations, and that directly translates to how long it takes an attacker to guess your password.

This article covers what the research and standards bodies say, the math behind why length matters so much, and concrete recommendations by account type.

## What NIST says about password length

NIST SP 800-63B is the gold standard for password policy in the United States, and its length guidance has shifted dramatically from what most organizations used to require.

**Current NIST recommendations (SP 800-63B, as updated):**

- **Minimum length: 8 characters** — this is the absolute floor; NIST calls anything shorter unacceptable
- **Recommended minimum: 15 characters** — for general-purpose accounts
- **Maximum length: at least 64 characters** — systems must accept passwords up to 64 characters; NIST encourages accepting even longer passwords
- **No truncation** — if a user creates a 40-character password, the system must store all 40 characters, not silently truncate it

The reason NIST raised the maximum is that many sites used to cap passwords at 16 or 20 characters, which prevented users from using passphrases or very long machine-generated passwords. That cap is now considered a bad practice.

## How length affects brute-force difficulty

Every additional character multiplies — not adds — the number of possible passwords. The math uses the password's character pool size raised to the power of its length.

For a password drawn from printable ASCII (95 characters):

```
Length  |  Possible combinations     |  Entropy (bits)
--------|---------------------------|----------------
 8      |  6.6 × 10^15              |  52.6
10      |  5.99 × 10^19             |  65.7
12      |  5.4 × 10^23              |  78.9
15      |  4.6 × 10^29              |  98.6
16      |  4.4 × 10^31              |  105.2
20      |  3.6 × 10^39              |  131.5
24      |  2.9 × 10^47              |  157.9
```

Going from 8 to 16 characters does not double the difficulty — it multiplies it by about 6.6 billion. Going from 12 to 20 characters multiplies it by about 666 quadrillion.

### Cracking time estimates

Modern password crackers can test billions of guesses per second when attacking simple hash functions (MD5, SHA-1). Even with strong hashing algorithms like bcrypt or Argon2id, dedicated hardware can test thousands to millions of guesses per second.

At 10 billion guesses per second (a fast offline attack against a weak hash):

| Password length (ASCII) | Time to exhaust all possibilities |
|------------------------|----------------------------------|
| 8 characters | About 8 days |
| 10 characters | About 190 years |
| 12 characters | About 17 million years |
| 15 characters | About 1.5 trillion years |
| 20 characters | Far beyond the age of the universe |

For online attacks (where the server throttles guesses), even an 8-character password is hard to crack — but that protection disappears the moment a site suffers a data breach and an attacker has the hashed passwords to attack offline.

## Why longer beats more complex

A common misconception is that adding symbols or mixed case compensates for length. The math shows otherwise.

Compare:
- `P@ssw0rd!` — 9 characters, uses all four character types (uppercase, lowercase, digits, symbols)
- `correcthorse` — 12 characters, lowercase only

The 9-character "complex" password has about 55 bits of entropy based on character count. But `P@ssw0rd!` is also a known pattern — it appears in every serious cracking wordlist with rule variations. Effective entropy might be closer to 10–15 bits.

The 12-character lowercase password, if truly randomly generated, has 56.5 bits of theoretical entropy. Attackers cannot easily shortcut this unless they know it came from a small wordlist.

Now compare more fairly — same character set (full ASCII), different lengths:

- 8 characters: 52.6 bits
- 12 characters: 78.9 bits
- 16 characters: 105.2 bits

Each 4-character increase adds about 26 bits of entropy when using full ASCII. That is equivalent to multiplying the search space by about 67 billion. No symbol requirement achieves that kind of improvement.

NIST explicitly removed composition rules (must contain uppercase, number, symbol) from SP 800-63B specifically because the data showed they provide minimal security improvement while making passwords harder to remember and more likely to be reused.

## Recommendations by account type

Not all accounts carry the same risk. Here is a practical guide:

### Email accounts: 16 characters minimum

Your email is the master key to every other account — password resets, account recovery, two-factor backup codes. If an attacker gets your email, they can reset everything else. Treat it like a bank account.

**Recommended:** 20+ characters, randomly generated, stored in a password manager.

### Banking and financial accounts: 16–20 characters

Financial accounts are direct targets. Many banks still have frustratingly low length limits (12 or 16 characters) — use the maximum they allow.

**Recommended:** Whatever the site's maximum is, generated randomly.

### Work VPN and SSO: 20+ characters

Corporate credentials are prime targets because compromising one employee's VPN access can expose an entire network. Many organizations now use MFA alongside passwords, but the password itself should still be strong.

**Recommended:** 20+ characters. If your organization allows passphrases, a 6-word EFF passphrase (about 77 bits) is excellent.

### Social media: 16 characters minimum

Compromised social accounts are used for fraud, scamming contacts, and as stepping stones to more sensitive accounts. They deserve strong passwords even if you think they are low stakes.

### Gaming accounts: 16 characters minimum

Game accounts with stored payment methods, valuable in-game items, or linked email addresses are routinely targeted. A strong password costs nothing.

### Master password for a password manager: Memorized passphrase

This is the one password you actually need to remember. It should not be generated the same way as other passwords — you need to be able to type it.

**Recommended:** A 6–8 word passphrase drawn from the EFF wordlist. Six words gives about 77 bits of entropy, which is stronger than most randomly generated 12-character passwords. Seven or eight words gives 90–103 bits — excellent for a memorized password.

**Example structure (do not use this exact phrase):** `correct horse battery staple maple ridge` — six random words, spaces allowed, easy to type and remember.

### Wi-Fi passwords: 20+ characters

Your Wi-Fi password is often entered manually on devices that do not auto-fill, so there is a temptation to keep it short. But it is also stored permanently on every device you connect and is a relatively static credential. Use a long one, and change it only when you suspect compromise.

### API keys and machine credentials: 32+ characters (128+ bits)

Machine-to-machine credentials should use cryptographically random tokens of at least 32 bytes (256 bits). Use `secrets.token_hex(32)` in Python or `openssl rand -hex 32` in the shell. These are never typed by humans and are stored in secrets managers, so there is no reason to limit their length.

## Passphrase length equivalence

Passphrases use words rather than characters. Using the EFF long wordlist (7,776 words), each word contributes about 12.9 bits of entropy.

| Words | Bits of entropy | Roughly equivalent to |
|-------|----------------|----------------------|
| 4 words | 51.7 bits | 8-char ASCII password |
| 5 words | 64.6 bits | 10-char ASCII password |
| 6 words | 77.5 bits | 12-char ASCII password |
| 7 words | 90.4 bits | 14-char ASCII password |
| 8 words | 103.3 bits | 16-char ASCII password |

The key advantage of passphrases is memorability. A 6-word passphrase is about as strong as a 12-character random password but can be remembered reliably. For credentials you must type from memory — your password manager master password, your device login password — a passphrase is the better choice.

For everything else, use a password manager and let it generate 20-character random passwords. You do not need to remember them.

## The practical problem with short passwords

Many older systems were designed with 8-character minimum and 16-character maximum limits. These limits were based on storage constraints and UI assumptions from the 1990s, not security research.

If a site caps your password at 12 or 16 characters, that is a signal that their password handling may have other issues too. Use whatever maximum they allow, enable two-factor authentication if available, and monitor for breach notifications via services like Have I Been Pwned.

## Quick reference

| Account type | Minimum recommended length |
|-------------|---------------------------|
| Email | 20 characters |
| Banking | 20 characters (or site max) |
| Work VPN / SSO | 20 characters |
| Social media | 16 characters |
| Password manager master | 6-word passphrase (memorized) |
| Wi-Fi | 20 characters |
| API keys / tokens | 32 bytes (64 hex characters) |

## Start with the right tool

Generating a 20-character random password is trivial with the right tool. [passwordgen.io](/) lets you set exact length, choose your character set, and generate passwords using the browser's built-in CSPRNG — no data is sent to any server.

Set the length to at least 16 characters for normal accounts and 20 or more for anything you care about. The entropy displayed alongside the password shows exactly how strong it is. Then save it in a password manager and never think about it again.

Length is free. There is no reason to use a short password.
