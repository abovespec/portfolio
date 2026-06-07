---
title: "Passkeys and Passwordless Authentication: How They Work"
description: "Learn how passkeys and passwordless authentication work, why they're more secure than passwords, and which sites support them today."
publishDate: 2026-06-07
updatedDate: 2026-06-07
author: "Editorial Team"
tags: ["passkeys", "passwordless", "fido2", "webauthn", "authentication"]
draft: false
---

Passwords have a fundamental problem: they're secrets that need to be transmitted to a server, stored in a database, and remembered by humans. Every step in that chain creates risk. Passkeys eliminate all of it.

## What Is Passwordless Authentication?

Passwordless authentication verifies your identity without requiring you to enter a password. Instead of something you know (a password), it relies on something you have (a device) or something you are (biometrics).

Common passwordless methods include:
- **Passkeys** (FIDO2/WebAuthn) — the most secure option
- **Magic links** — a one-time link emailed to you
- **Email OTP** — a code sent to your email
- **Authenticator app login** — approve a push notification

Passkeys are the gold standard because they're phishing-resistant and don't involve codes or links that can be intercepted.

## How Passkeys Work

Passkeys use **public-key cryptography** (specifically FIDO2/WebAuthn). Here's the mechanism:

### Registration

1. You choose to create a passkey for a website
2. Your device generates a **key pair**: a public key and a private key
3. The **public key is stored on the server** — even if the server is breached, this key can't log attackers in
4. The **private key stays on your device** — it never leaves and is never transmitted

### Authentication

1. You visit the site and choose to sign in with your passkey
2. The server sends a **challenge** (a random value)
3. Your device asks you to authenticate locally — fingerprint, face scan, or device PIN
4. If verified, your device **signs the challenge** with the private key
5. The server verifies the signature using the stored public key
6. You're in

The critical property: the private key is never sent to the server. There's nothing for a phishing site to capture. Even a perfect clone of the real website cannot authenticate you because the private key on your device will refuse to sign challenges from unrecognized origins.

## Device-Bound vs. Synced Passkeys

### Device-Bound Passkeys

Some passkeys are tied to a single hardware key or device (like a YubiKey). They cannot be exported or synced. Maximum security, but if you lose the device, you need backup recovery options.

### Synced Passkeys

Most consumer passkey implementations (Apple, Google, Microsoft) sync passkeys through their respective cloud accounts:
- **Apple**: iCloud Keychain syncs passkeys across iPhone, iPad, and Mac
- **Google**: Google Password Manager syncs across Android and Chrome
- **Microsoft**: Windows Hello / Microsoft Authenticator

Synced passkeys trade a small amount of security (your cloud account becomes a target) for a large gain in usability — you can use your passkey on any of your devices without re-registering.

## Passkeys vs. Passwords

| Feature | Passwords | Passkeys |
|---------|-----------|---------|
| Phishing resistance | None — any fake site can capture them | Complete — tied to specific origin |
| Breach exposure | Hashed passwords can be cracked | Public keys are useless to attackers |
| Reuse risk | High — people reuse passwords | None — each site has unique keys |
| Memory burden | High | None |
| Credential stuffing | Vulnerable | Impossible |
| Setup complexity | Minimal | Low (but unfamiliar) |

## Passkeys vs. TOTP (Authenticator Apps)

Passkeys are stronger than TOTP codes in one key way: **TOTP codes can be phished**. A real-time phishing attack can intercept the 6-digit code you enter and replay it immediately. Passkeys cannot be phished because the cryptographic signature is bound to the exact domain of the legitimate site.

## Which Sites Support Passkeys?

Passkey adoption is growing rapidly. As of 2026, major services include:

- **Apple ID** — fully supports passkeys
- **Google Account** — supports passkeys for Google accounts
- **Microsoft Account** — supports passkeys with Windows Hello
- **GitHub** — supports passkeys
- **PayPal** — supports passkeys
- **eBay** — supports passkeys
- **Best Buy** — supports passkeys
- **Best Buy** — supports passkeys
- **Shopify** — supports passkeys for merchants
- **Kayak** — supports passkeys
- **Amazon** — supports passkeys
- **Adobe** — supports passkeys
- **1Password, Dashlane, Bitwarden** — can store and fill passkeys as password managers

The FIDO Alliance's passkey website (passkeys.io) maintains a current directory of services.

## Setting Up Passkeys

The setup process varies by site, but generally:

1. Go to your account security settings
2. Look for "Passkeys," "Passwordless sign-in," or "Security keys"
3. Click "Add passkey" or similar
4. Your browser prompts you to authenticate with your device (Touch ID, Face ID, Windows Hello, or a hardware key)
5. The passkey is created and registered

On subsequent logins, you'll see a "Sign in with passkey" option instead of (or in addition to) the password field.

## Recovery and Backup

The most common concern about passkeys: what happens if you lose your device?

- **Synced passkeys**: If your passkeys sync via iCloud, Google, or Microsoft, they're accessible from any device signed into that account
- **Recovery codes**: Most sites that support passkeys still offer backup codes or an email recovery path
- **Multiple passkeys**: Register passkeys on multiple devices (phone + laptop + hardware key) where the service allows it

Account recovery is the legitimate weak point in passkey systems today — most recovery flows fall back to email or SMS, which have their own security limitations.

## The Future of Passwords

Passkeys won't replace passwords overnight. Billions of existing accounts use passwords, and not every website will add passkey support immediately. For accounts that don't support passkeys:

- Use a **password manager** to store unique, strong passwords
- Use a **password generator** (like [passwordgen.io](/)) to create high-entropy passwords
- Add **TOTP-based MFA** as a second factor

But for accounts that do support passkeys, enabling them is the single best security upgrade you can make. You gain phishing resistance, eliminate the risk of password reuse, and remove the server-side breach exposure of stored password hashes — all at once.

Passwordless authentication isn't just more convenient. It's genuinely, structurally more secure.
