---
title: "What Is a JWT Token? JSON Web Tokens Explained"
description: "JWT (JSON Web Token) is a compact, self-contained way to securely transmit claims between parties. Learn the structure, how signing works, and when to use it."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["jwt", "authentication", "security", "api", "json web tokens"]
draft: false
---

A **JWT (JSON Web Token)** is a compact, URL-safe token format for transmitting claims — statements about a user or entity — between two parties. JWTs are digitally signed, which means the receiver can verify that the content hasn't been tampered with.

The JWT specification is defined in [RFC 7519](https://www.rfc-editor.org/rfc/rfc7519).

## What a JWT looks like

A JWT is three Base64URL-encoded strings joined by dots:

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyXzEyMyIsIm5hbWUiOiJBbGljZSIsImlhdCI6MTcxNDAwMDAwMCwiZXhwIjoxNzE0MDA3MjAwfQ.X2YHjhYy8cPP1SHRxCbQ8q0c7wBx5nzL4DqPp4GMvck
```

Each part decodes to JSON:

**Header:**
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

**Payload:**
```json
{
  "sub": "user_123",
  "name": "Alice",
  "iat": 1714000000,
  "exp": 1714007200
}
```

**Signature:** The result of signing `base64url(header) + "." + base64url(payload)` with a secret key using the algorithm specified in the header.

## The three parts

### 1. Header

The header declares the token type and signing algorithm:

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

Common algorithms:
- `HS256` — HMAC with SHA-256 (symmetric: same key signs and verifies)
- `RS256` — RSA with SHA-256 (asymmetric: private key signs, public key verifies)
- `ES256` — ECDSA with SHA-256 (asymmetric: smaller signatures than RS256)

### 2. Payload

The payload contains **claims** — key-value pairs about the subject. Standard claims ([RFC 7519 §4.1](https://www.rfc-editor.org/rfc/rfc7519#section-4.1)):

| Claim | Meaning |
|-------|---------|
| `sub` | Subject — identifies the user (`user_123`, UUID, email) |
| `iss` | Issuer — who created the token (`auth.example.com`) |
| `aud` | Audience — intended recipient (`api.example.com`) |
| `exp` | Expiration time — Unix timestamp after which the token is invalid |
| `iat` | Issued at — Unix timestamp when the token was created |
| `nbf` | Not before — Unix timestamp before which the token is invalid |
| `jti` | JWT ID — unique identifier, used for revocation |

Custom claims can be added for application-specific data:

```json
{
  "sub": "user_123",
  "exp": 1714007200,
  "iat": 1714000000,
  "roles": ["admin", "user"],
  "plan": "pro"
}
```

**Important:** The payload is Base64URL-encoded, not encrypted. Anyone with the token can decode and read the payload — only the signature prevents tampering. Never put secrets or sensitive data in a JWT payload unless you also encrypt the token (JWE).

### 3. Signature

The signature verifies that the token hasn't been modified:

```
HMACSHA256(
  base64url(header) + "." + base64url(payload),
  secret_key
)
```

For HS256, the same secret key both signs (server) and verifies (server). For RS256, the private key signs and the public key verifies — allowing third parties to verify tokens without knowing the signing key.

## Why JWTs are useful

**Self-contained:** The token carries its own claims. The API server can verify the token and read the user's ID and roles without querying a database on every request.

**Stateless:** No session storage is needed on the server. Any server with the verification key can validate any token. This scales naturally in distributed systems.

**Cross-service:** With asymmetric signing (RS256/ES256), multiple services can verify tokens signed by a central auth server using only the public key.

## How a JWT-based login flow works

1. **User logs in** — client sends credentials to the auth server
2. **Auth server creates a JWT** — signs it with a private/secret key and returns it to the client
3. **Client stores the JWT** — typically in memory, an HttpOnly cookie, or (less securely) localStorage
4. **Client sends the JWT with each request** — in the `Authorization: Bearer <token>` header
5. **API server verifies the JWT** — checks the signature, validates claims (`exp`, `iss`, `aud`)
6. **API processes the request** — if valid, extracts the user ID and claims from the payload

## Decoding a JWT

Decoding (reading the payload) requires no secret — you just Base64URL-decode each part:

```python
import base64, json

def decode_jwt_payload(token: str) -> dict:
    payload_b64 = token.split(".")[1]
    # Pad to a multiple of 4
    padding = 4 - len(payload_b64) % 4
    payload_b64 += "=" * (padding % 4)
    return json.loads(base64.urlsafe_b64decode(payload_b64))

decode_jwt_payload("eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VyXzEyMyJ9.abc")
# {'sub': 'user_123'}
```

**Verification** (confirming the signature is valid) requires the secret or public key.

## Inspect JWTs online

Paste any JWT into [jwtinspect.io](/) to decode the header and payload and verify the structure — useful for debugging authentication issues without setting up local tooling.
