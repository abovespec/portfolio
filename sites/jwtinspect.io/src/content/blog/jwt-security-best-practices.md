---
title: "JWT Security Best Practices: What to Do (and What to Avoid)"
description: "The most common JWT security mistakes and how to avoid them: algorithm confusion, weak secrets, insecure storage, missing claim validation, and the none algorithm attack."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["jwt", "security", "best practices", "authentication", "api security"]
draft: false
---

JWT authentication is straightforward to get right — and surprisingly easy to get dangerously wrong. Most JWT security vulnerabilities fall into a small set of categories. Here's what to watch for and how to fix it.

## 1. Never accept `alg: none`

**The attack:** The JWT header specifies the signing algorithm. An attacker can modify a valid token, change `alg` to `"none"`, and strip the signature — leaving a token with no cryptographic protection. Early JWT libraries accepted this as "unsigned" and treated the token as valid.

For more on this topic, see [*What Is a JWT Token? JSON Web Tokens Explained*](/blog/what-is-a-jwt-token).

```json
// Attacker-modified header
{ "alg": "none", "typ": "JWT" }

// Result: no signature required
eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJzdWIiOiJhZG1pbiJ9.
```

**Fix:** Explicitly specify which algorithms are acceptable when verifying. Never allow `none`.

```python
# Wrong — library may accept alg: none
jwt.decode(token, key)

# Correct — whitelist algorithms explicitly
jwt.decode(token, key, algorithms=["HS256"])
```

```js
// Node.js
jwt.verify(token, secret, { algorithms: ['HS256'] });
```

Modern JWT libraries disable `none` by default. Ensure you're using a maintained library version and check your configuration.

For more on this topic, see [*JWT vs Session Authentication: Which Should You Use?*](/blog/jwt-vs-session).

## 2. Use strong, unique secrets for HS256

**The attack:** HS256 uses a shared secret for both signing and verification. If the secret is weak (short, guessable, or predictable), an attacker can brute-force it using tools like `hashcat`:

```bash
hashcat -a 0 -m 16500 token.txt wordlist.txt
```

A weak secret like `"secret"`, `"jwt_secret"`, or any short string can be cracked quickly.

**Fix:**
- Use a cryptographically random secret of at least 256 bits (32 bytes)
- Generate it properly:

```python
import secrets
secret = secrets.token_hex(32)  # 64 hex chars = 256 bits
```

```bash
openssl rand -hex 32
```

- Store the secret in environment variables, not code
- Rotate secrets periodically

## 3. Validate all relevant claims

**The attack:** Many developers verify the signature but forget to validate claims like `iss`, `aud`, and `exp`. A token signed by one service may be accepted by another if `iss`/`aud` aren't checked.

**Fix:** Always validate `exp`, `iss`, and `aud`:

```python
jwt.decode(
    token,
    key,
    algorithms=["HS256"],
    issuer="https://auth.example.com",   # validates iss
    audience="https://api.example.com",  # validates aud
    # exp and nbf validated automatically
)
```

```js
jwt.verify(token, secret, {
  algorithms: ['HS256'],
  issuer: 'https://auth.example.com',
  audience: 'https://api.example.com',
});
```

## 4. Use asymmetric algorithms (RS256/ES256) for distributed systems

**The problem:** HS256 requires every service that verifies tokens to know the shared secret. If any of those services is compromised, the secret is exposed and all tokens are at risk.

**Fix:** Use RS256 (RSA) or ES256 (ECDSA). The auth server signs with the private key; every other service verifies with the public key. Compromising a verification service doesn't expose the signing key.

```python
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

with open("private.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

# Sign
token = jwt.encode(payload, private_key, algorithm="RS256")

# Verify (with public key only)
with open("public.pem", "rb") as f:
    public_key = serialization.load_pem_public_key(f.read())

decoded = jwt.decode(token, public_key, algorithms=["RS256"])
```

## 5. Don't store access tokens in localStorage

**The attack:** `localStorage` is accessible to any JavaScript on the page. If your site has an XSS vulnerability (even through a third-party script), an attacker can steal the access token.

**Fix options:**
- Store access tokens in memory (a JS variable or React context/state) — cleared on page refresh
- Store refresh tokens in `HttpOnly; SameSite=Strict` cookies — inaccessible to JavaScript

The tradeoff: memory storage is safest but requires re-authentication on page reload (solved with a silent token refresh using a cookie-stored refresh token).

## 6. Use short access token lifetimes

**The attack:** Long-lived access tokens give attackers a large window if a token is stolen.

**Fix:** Access tokens should expire in 15 minutes to 1 hour. Use refresh tokens for longer sessions.

```python
payload = {
    "sub": user_id,
    "exp": datetime.now(timezone.utc) + timedelta(minutes=15),
    "iat": datetime.now(timezone.utc),
}
```

The shorter the access token, the smaller the attacker's window if it's intercepted.

## 7. Implement refresh token rotation

When issuing a new access token, invalidate the old refresh token and issue a new one:

```python
def refresh_access_token(refresh_token: str) -> tuple[str, str]:
    payload = verify_refresh_token(refresh_token)
    
    # Revoke old refresh token
    revoke_refresh_token(payload["jti"])
    
    # Issue new tokens
    new_access_token = create_access_token(payload["sub"])
    new_refresh_token = create_refresh_token(payload["sub"])
    
    return new_access_token, new_refresh_token
```

If a stolen refresh token is used, rotation means it's invalidated after the first use — and the next legitimate use will fail, alerting you to a potential compromise.

## 8. Use HTTPS everywhere

JWTs in transit are as safe as the transport layer. Always serve your API over HTTPS. A JWT transmitted over HTTP can be captured by any network observer.

## 9. Don't put sensitive data in the payload

The JWT payload is **encoded, not encrypted** — anyone with the token can decode it with a Base64URL decoder. Never put:
- Passwords or password hashes
- Full credit card numbers or PII beyond necessary identifiers
- Private keys or secrets

If you need to encrypt the payload, use JWE (JSON Web Encryption) — a separate specification.

## Summary checklist

- [ ] Whitelist allowed algorithms; reject `none`
- [ ] Secret ≥ 256 bits for HS256; use RS256/ES256 for distributed systems
- [ ] Validate `exp`, `iss`, `aud` on every verify call
- [ ] Access tokens expire in ≤ 1 hour
- [ ] Refresh tokens stored in HttpOnly cookies; access tokens in memory
- [ ] Refresh token rotation enabled
- [ ] All traffic over HTTPS
- [ ] No secrets or unnecessary PII in payload

For more on this topic, see [*JWT Token Expiration: Access Tokens, Refresh Tokens, and Rotation*](/blog/jwt-token-expiration).

## Debug your JWT

Inspect your token's header, payload, and expiration at [jwtinspect.io](/) — helpful for catching algorithm mismatches, missing claims, or expired tokens during development.
