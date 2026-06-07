---
title: "Two-Factor Authentication (2FA): How It Works and How to Set It Up"
description: "Learn what two-factor authentication is, the types of 2FA available, why SMS is weak, and how to set up TOTP authenticator apps for your accounts."
publishDate: 2026-06-07
updatedDate: 2026-06-07
author: "Editorial Team"
tags: ["two factor authentication", "2fa", "totp", "security", "authentication"]
draft: false
---

A strong password is necessary but not sufficient. Credential breaches, phishing attacks, and password reuse mean that passwords alone can be compromised without any mistake on your part — your credentials may be in a breach database you have never heard of. Two-factor authentication (2FA) adds a second layer that remains effective even when your password is known.

This article explains how 2FA works, the different types available, their strengths and weaknesses, and how to set up the most common forms.

## What is two-factor authentication?

Two-factor authentication requires two separate pieces of evidence — called factors — to verify your identity. Factors fall into three categories:

1. **Something you know** — a password, PIN, or passphrase
2. **Something you have** — a phone, hardware security key, or smart card
3. **Something you are** — a fingerprint, face scan, or other biometric

A single-factor system asks for one of these. Two-factor authentication combines two from different categories. The key word is *different categories* — requiring both a password and a PIN is not 2FA because both are "something you know."

The most common combination is:
- First factor: password (something you know)
- Second factor: a code from your phone or a hardware key (something you have)

### Why two factors?

Each factor has different attack surfaces. A password can be:
- Stolen from a database breach
- Phished in a fake login page
- Guessed if weak
- Leaked by a keylogger

A hardware token or authenticator app code is:
- Not stored on a server that can be breached
- Only accessible to someone who physically has your device
- Time-limited (TOTP codes expire every 30 seconds)

An attacker would need to compromise both the server (to get your password) and your physical device simultaneously. That combination of attacks is rare and difficult to execute at scale.

## Types of 2FA

### SMS-based 2FA

The most widely deployed form of 2FA sends a one-time code to your phone via text message. To log in, you enter your password and then the code you received.

**How it works:** After successful password entry, the service generates a random 6–8 digit code, stores it temporarily, and sends it via the carrier's SMS network to your registered number. You type the code into the login form.

**Weaknesses:**

SMS 2FA has serious vulnerabilities that are well-documented in the security community:

- **SIM swapping:** An attacker calls your carrier, impersonates you, and convinces customer support to transfer your number to a SIM card they control. All your SMS codes then go to them. This attack has been used to drain cryptocurrency accounts, break into email accounts, and compromise high-profile targets. It requires social engineering, not technical skill.

- **SS7 protocol vulnerabilities:** The Signaling System 7 protocol that underlies the global telephone network has known security weaknesses that allow attackers (typically nation-state actors or organized crime with access to carrier-level equipment) to intercept SMS messages in transit.

- **Malware:** Android malware can silently read incoming SMS messages and forward them to attackers.

- **SIM cloning:** In some regions, corrupt carrier employees have been involved in illegitimately duplicating SIM cards.

NIST SP 800-63B classifies SMS-based authentication as "restricted" — permissible but with risk acknowledgment required. For most consumers, SMS 2FA is still far better than no 2FA. For high-value accounts, it should be replaced with a stronger method.

### TOTP authenticator apps

Time-based One-Time Passwords (TOTP), defined in RFC 6238, generate 6-digit codes directly on your device without any network communication at the moment of use.

**How it works:**
1. When you enable TOTP, the service generates a secret key (typically 160–320 bits, encoded in a QR code or as a Base32 string).
2. You scan the QR code with an authenticator app, which stores the secret.
3. At login, your app computes `HMAC-SHA1(secret, floor(unix_time / 30))` and displays the result as a 6-digit code.
4. The server computes the same value independently.
5. Codes change every 30 seconds; servers typically accept one window on either side to account for clock drift.

Because the code is computed locally on your device using a shared secret and the current time, the server never sends anything over the network during login — there is nothing to intercept.

**Popular TOTP apps:**

- **Authy** — Supports encrypted cloud backup of secrets, multi-device sync. The backup means your TOTP codes survive a lost phone. Backup is encrypted with a separate password.
- **Google Authenticator** — Simple, widely supported. Originally no backup; Google added optional cloud backup. Easy to use.
- **Microsoft Authenticator** — Supports TOTP for non-Microsoft services alongside Microsoft-specific push notifications.
- **1Password / Bitwarden** — Password managers that also store TOTP secrets alongside passwords. Convenient but concentrates your "something you know" and "something you have" factors, somewhat undermining the principle.
- **Aegis** (Android, open source) — Strong choice for security-conscious users; supports encrypted local backups.
- **Raivo OTP** (iOS, open source) — Popular iOS alternative.

**Weaknesses of TOTP:**
- Phishing can still work in real time — a fake login page can ask for your current TOTP code and immediately replay it to the real site before it expires.
- If your device is compromised (malware, someone physically accessing your phone), the secret can be extracted.
- If you do not back up your TOTP secrets, losing your phone means losing access to every account.

### Hardware security keys (FIDO U2F / FIDO2)

Hardware keys — the most common being YubiKey from Yubico, but also Google Titan Key, Solo, and others — implement the FIDO2 and WebAuthn standards (also known as CTAP, Client to Authenticator Protocol).

**How it works:** The key contains a secure element (a tamper-resistant chip) that generates a unique public/private key pair for each site you register with. At login, the server sends a challenge, the key signs it with the private key, and the server verifies the signature with the stored public key. Crucially, the private key never leaves the hardware device.

**Advantages:**
- **Phishing-resistant by design.** The key is bound to the specific domain (e.g., `accounts.google.com`). If a phishing site uses `accounts-google.com`, the key will not authenticate — the domain does not match the registered origin.
- **Nothing to intercept over the network.**
- **Physical presence required** — the attacker must have your key in hand.

**Weaknesses:**
- If you lose the key and have no backup, you may be locked out.
- Requires a USB-A, USB-C, or NFC interface; not universally supported by all services.
- More expensive than an app (YubiKey 5 series runs approximately $50–$70 USD).

For the highest security accounts — Google, GitHub, financial accounts — hardware keys are the gold standard. NIST classifies FIDO2 hardware authenticators at Authenticator Assurance Level 3 (AAL3), the highest level.

### Push notification 2FA

Services like Duo Security, Microsoft Authenticator, and Okta Verify can send a push notification to your phone asking you to approve or deny a login attempt. Tap "Approve" and you are in.

**Weaknesses:** "Push fatigue" attacks — also called MFA bombing — send repeated push requests hoping the user will tap "Approve" out of frustration or habit. This attack successfully compromised several high-profile companies in recent years. Mitigations include requiring the user to enter a displayed number in the app (number matching), but not all implementations use this.

### Email-based one-time codes

Some services send a code to your email address rather than SMS. This provides 2FA protection only if your email account itself is well-secured — it is effectively only as strong as your email account's own 2FA.

## How to set up TOTP 2FA step by step

1. **Install an authenticator app** — Authy or Google Authenticator for most users; Aegis if you are on Android and want open-source software.

2. **Go to security settings** on the account you want to protect. Look for "Two-factor authentication," "Two-step verification," or "Login verification."

3. **Select authenticator app** as your 2FA method (not SMS, if you have the choice).

4. **Scan the QR code** with your authenticator app, or manually enter the secret key it displays.

5. **Confirm setup** by entering the 6-digit code currently shown in your app.

6. **Save your recovery codes.** Every service that offers TOTP will give you one-time backup codes (typically 8–16 codes, each usable once). **Print or save these now.** If you lose your phone, these codes let you regain access. Store them somewhere safe: a printed copy in a secure location, or your password manager.

7. **Test it.** Log out and log back in to confirm 2FA is working before you close that browser window.

## Recovery codes and backup planning

Recovery codes are single-use emergency access codes provided when you set up 2FA. They exist to let you regain access if you lose your authentication device.

Best practices:
- **Save them immediately** — most services show them only once
- **Store in multiple places:** your password manager and a printed copy stored physically
- **Do not store them only on the device you use for 2FA** — if that device is lost, you need access to the codes from somewhere else
- **Do not share them** — anyone with a recovery code can bypass your 2FA

If you use Authy, its encrypted cloud backup protects your TOTP secrets across devices, which reduces (but does not eliminate) the need for recovery codes.

## 2FA and passwords together

Two-factor authentication does not replace a strong password — it layers on top of it. Start with a strong, unique password for every account, then add 2FA for the accounts that matter most: email, banking, work systems, social media, password manager.

Generate strong, unique passwords at [passwordgen.io](/) and enable 2FA on every account that supports it. The combination makes credential-based attacks impractical for the vast majority of attackers.

## Which 2FA method should you use?

From strongest to weakest:

1. **FIDO2 hardware key** — phishing-resistant, strongest available
2. **TOTP authenticator app** — strong, free, widely supported
3. **Push notification 2FA** — convenient, watch for push fatigue attacks
4. **SMS** — better than nothing, but has known weaknesses
5. **No 2FA** — avoid for any account you care about

Even SMS 2FA reduces account compromise risk dramatically. If a service only offers SMS, enable it. If it offers TOTP, use that instead. If it offers FIDO2, use that.

The most important step is simply enabling 2FA at all. Most account takeovers target users with no second factor at all.
