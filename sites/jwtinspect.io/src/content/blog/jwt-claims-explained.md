---
title: "JWT Claims Explained: iss, sub, aud, exp, iat, nbf, and jti"
description: "A complete reference for JWT registered claims: what iss, sub, aud, exp, iat, nbf, and jti mean, how to set them, and how to validate each one correctly."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["jwt", "claims", "security", "authentication", "reference"]
draft: false
---

JWT claims are the key-value pairs in the token's payload. The JWT specification ([RFC 7519](https://www.rfc-editor.org/rfc/rfc7519)) defines a set of **registered claims** — standard names with agreed meanings. Libraries validate these claims automatically when you tell them to.

## The seven registered claims

### `iss` — Issuer

Who created and signed the token. Typically the URL of your authentication server.

```json
{ "iss": "https://auth.example.com" }
```

Validation: The verifying server should check that `iss` matches the expected issuer. This prevents tokens issued by one service from being accepted by another.

```python
jwt.decode(token, key, algorithms=["HS256"], issuer="https://auth.example.com")
```

### `sub` — Subject

The principal that is the subject of the JWT — usually the user identifier. Should be unique within the issuer's context.

```json
{ "sub": "user_abc123" }
```

The `sub` is the user ID your application uses to look up user data. It's typically a UUID, database ID, or opaque identifier. Avoid using email as `sub` if emails can change.

### `aud` — Audience

Who the token is intended for. A string or array of strings identifying the intended recipients.

```json
{ "aud": "https://api.example.com" }
{ "aud": ["https://api.example.com", "https://analytics.example.com"] }
```

Validation: The verifying server should reject tokens where its own identifier isn't in `aud`. This prevents tokens meant for one service from being used against another.

```js
// Node.js — reject if audience doesn't match
jwt.verify(token, secret, { audience: 'https://api.example.com' });
```

### `exp` — Expiration Time

Unix timestamp (seconds since epoch) after which the token must not be accepted.

```json
{ "exp": 1714007200 }
```

Best practices:
- Access tokens: 15 minutes to 1 hour
- Refresh tokens: 7 to 30 days
- One-time use tokens (email verification): minutes to hours

Every JWT library validates `exp` automatically when you verify a token. The error is typically `TokenExpiredError` or equivalent.

```python
from datetime import datetime, timedelta, timezone

exp = datetime.now(timezone.utc) + timedelta(minutes=15)
payload = {"sub": "user_123", "exp": exp}
```

### `iat` — Issued At

Unix timestamp when the token was created. Useful for:
- Audit logging (when did this session start?)
- Invalidating tokens issued before a password change
- Clock skew detection

```json
{ "iat": 1714000000 }
```

If a user changes their password, you can store the timestamp and reject tokens where `iat` is before the password change time.

### `nbf` — Not Before

Unix timestamp before which the token must not be accepted. Useful for issuing tokens that activate in the future (scheduled access, pre-authorized operations).

```json
{ "nbf": 1714003600 }
```

A token with `nbf` in the future will be rejected even if `exp` hasn't passed. Most libraries validate `nbf` automatically.

### `jti` — JWT ID

A unique identifier for the token. Used primarily for revocation — if you maintain a blocklist, store the `jti` values of invalidated tokens.

```json
{ "jti": "a1b2c3d4-e5f6-7890-abcd-ef1234567890" }
```

```python
import uuid
payload = {
    "sub": "user_123",
    "jti": str(uuid.uuid4()),
    "exp": ...
}
```

On logout, add the `jti` to a Redis blocklist with an expiry matching the token's `exp`. On each request, check if the token's `jti` is in the blocklist before processing.

## Custom claims

Beyond registered claims, you can add application-specific claims:

```json
{
  "sub": "user_123",
  "exp": 1714007200,
  "iat": 1714000000,
  "roles": ["admin", "user"],
  "plan": "pro",
  "org_id": "org_456",
  "permissions": ["read:users", "write:posts"]
}
```

**Collision avoidance:** The JWT spec recommends either using public (IANA-registered) claim names or URI-namespaced names to avoid collisions with other systems:

```json
{
  "https://myapp.example.com/roles": ["admin"]
}
```

In practice, short non-namespaced names (`roles`, `plan`, `org`) are common when you control both issuer and verifier.

## Claims validation checklist

When verifying a JWT, a correct implementation must:

- [x] Verify the signature using the correct algorithm and key
- [x] Reject tokens where the algorithm in the header doesn't match expectations (never accept `alg: none`)
- [x] Check `exp` — reject expired tokens
- [x] Check `nbf` if present — reject not-yet-valid tokens
- [x] Check `iss` — reject tokens from unexpected issuers
- [x] Check `aud` — reject tokens not intended for this service
- [ ] Check `jti` against a revocation list if you need immediate revocation
- [ ] Check `iat` against a user's "sessions invalidated at" timestamp if password change revocation is needed

Most JWT libraries handle `exp`, `nbf`, `iss`, and `aud` automatically when you pass them as options. Implement `jti` blocklisting and `iat` invalidation yourself if needed.

## Inspect claims in a token

Paste any JWT into [jwtinspect.io](/) to see every claim in the payload decoded — including expiration time in human-readable format.
