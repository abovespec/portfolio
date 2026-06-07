---
title: "Passphrase vs Password: Which Is More Secure?"
description: "Compare passphrases and passwords by entropy, memorability, and attack resistance. Learn when to use a passphrase, how Diceware works, and NIST recommendations."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["password", "passphrase", "security", "diceware", "entropy"]
draft: false
---

A **password** is typically a string of mixed characters. A **passphrase** is multiple words strung together. Both can be equally secure — but passphrases have advantages for cases where you need to memorize the secret.

## What is a passphrase?

A passphrase is two or more random words:

```
correct horse battery staple
marble engine sunset radio
purple volcano coffee lamp
```

The key word is *random*. Phrases that come from your head — "ilovemy dog" or "letmein2026" — aren't secure. Random word passphrases selected from a large wordlist are.

## Entropy comparison

Security is measured in bits of entropy — how many guesses an attacker needs to brute-force the password.

For more on this topic, see [*What Makes a Good Password? Length, Entropy, and Randomness*](/blog/what-makes-a-good-password).

**Random character password (full ASCII charset, 95 options per character):**
- 12 characters: ~79 bits
- 16 characters: ~105 bits
- 20 characters: ~131 bits

**Random passphrase (Diceware, 7,776 words per roll):**
- 4 words: ~51 bits
- 5 words: ~64 bits
- 6 words: ~77 bits
- 7 words: ~90 bits
- 8 words: ~103 bits

A 6-word Diceware passphrase (~77 bits) is roughly equivalent to a 12-character random character password in entropy. A 7-word passphrase (~90 bits) is very strong for most purposes.

## When to use a passphrase

**Use a passphrase when you need to memorize the secret:**
- Password manager master password
- Full-disk encryption password (VeraCrypt, LUKS)
- PGP key passphrase
- SSH key passphrase
- Shared team secrets passed verbally

**Use a random character password (via password manager) for everything else:**
- Online account logins
- API keys
- Database passwords

For more on this topic, see [*Password Generator: How to Generate Strong Passwords Online and in Code*](/blog/password-generator-guide).

The advantage of passphrases is memorability — four random words are much easier to remember than `Xk9#mQ2!pLr7vN`. The advantage of random character passwords is compactness — they pack more entropy per character.

## How Diceware works

Diceware uses physical dice to ensure randomness:

1. Roll 5 dice and record the numbers (e.g., 3-4-2-1-6)
2. Look up the number in the Diceware wordlist (34216 = "mouse")
3. Repeat for each word

```
34216 = mouse
16326 = candy
52421 = pine
21341 = dry
46643 = rock
55624 = smart
```

Result: **mouse candy pine dry rock smart**

You can also use an offline Diceware tool or a password manager's passphrase generator. The key is that the words are selected randomly, not by you.

For more on this topic, see [*Password Manager Comparison: Bitwarden, 1Password, Dashlane, KeePass*](/blog/password-manager-comparison).

## Diceware wordlist size

The standard Diceware list has 7,776 words (6^5, since each word is chosen with 5 dice rolls). Each word contributes `log₂(7776) ≈ 12.9 bits` of entropy.

Some generators use larger word lists (EFF word lists have 7,776 words carefully chosen to be unambiguous when spoken). The entropy per word varies with list size.

## The human-phrase trap

The biggest mistake is using a memorable sentence or phrase that comes from your head:

```
# These look like passphrases but are weak:
ilovemydog
correcthorsebatterystaple  ← famous xkcd example; now in attack wordlists
letmein1234
myfavoritecolor
```

Phrases from culture, movies, books, or your personal life are in attack wordlists. Only random selection from a large wordlist provides the security that passphrases promise.

## NIST stance on passphrases

NIST SP 800-63B recommends allowing long passwords (passphrases) and not penalizing length. Verifiers should:
- Accept up to 64+ characters (enabling passphrases)
- Not restrict special characters or spaces
- Not force arbitrary complexity rules that make passphrases harder

## Practical recommendation

| Use case | Recommendation |
|---------|---------------|
| Password manager master password | 6-word Diceware passphrase |
| Full-disk encryption | 6-7 word Diceware passphrase |
| PGP/SSH key | 6-word Diceware passphrase |
| Website accounts | 20-char random password (via manager) |
| API keys | 32+ char random string (base62 or hex) |
| Shared team credentials | Password manager's sharing feature |

For accounts where you have a password manager, use the longest random password the site allows. For secrets you must memorize, use a random passphrase.

Generate strong passwords and passphrases at [passwordgen.io](/).
