---
title: "How JWT Authentication Works: The Complete Flow"
description: "A step-by-step guide to JWT authentication: login, token issuance, request verification, refresh tokens, and logout. With sequence diagrams and code examples."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["jwt", "authentication", "security", "api", "access tokens"]
draft: false
---

JWT authentication replaces server-side session storage with a self-contained token. The server signs a token, the client holds it, and the server verifies it on every request — no database lookup required.

## The complete authentication flow

```
1. Client → Auth Server:   POST /login  { username, password }
2. Auth Server → Client:   200 OK  { access_token: "eyJ...", refresh_token: "eyJ..." }
3. Client → API:           GET /api/users  Authorization: Bearer eyJ...
4. API verifies token, processes request
5. API → Client:           200 OK  { users: [...] }
```

### Step 1: Login

The client sends credentials to the authentication endpoint:

```http
POST /auth/login HTTP/1.1
Content-Type: application/json

{
  "username": "alice@example.com",
  "password": "correctpassword"
}
```

### Step 2: Token issuance

The auth server validates credentials and issues tokens:

```python
import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = "your-256-bit-secret"
ALGORITHM = "HS256"

def create_access_token(user_id: str, roles: list[str]) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": user_id,
        "roles": roles,
        "iat": now,
        "exp": now + timedelta(minutes=15),
        "iss": "auth.example.com",
        "aud": "api.example.com",
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
```

The server responds with both an access token and a refresh token:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VyXzEyMyIsImV4cCI6MTcxNDAwNzIwMH0.abc123",
  "token_type": "bearer",
  "expires_in": 900,
  "refresh_token": "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VyXzEyMyIsInR5cGUiOiJyZWZyZXNoIiwiZXhwIjoxNzE0NjA0ODAwfQ.xyz456"
}
```

Access tokens are **short-lived** (15 minutes to 1 hour). Refresh tokens are **longer-lived** (days to weeks) and are only used to get new access tokens.

### Step 3: Authenticated requests

The client attaches the access token to every request using the `Authorization` header:

```http
GET /api/users HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VyXzEyMyIsImV4cCI6MTcxNDAwNzIwMH0.abc123
```

### Step 4: Token verification

The API middleware verifies the token before processing any request:

```python
import jwt
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer

security = HTTPBearer()

def verify_token(credentials = Depends(security)):
    try:
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            audience="api.example.com",  # verify aud claim
            issuer="auth.example.com",   # verify iss claim
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

The verification checks:
1. **Signature** — the token was signed by the expected key
2. **Expiration (`exp`)** — the token hasn't expired
3. **Audience (`aud`)** — the token was meant for this service
4. **Issuer (`iss`)** — the token came from the expected auth server
5. **Not-before (`nbf`)** — the token is currently valid (not yet in the future)

### Step 5: Token refresh

When the access token expires, the client uses the refresh token to get a new one:

```http
POST /auth/refresh HTTP/1.1
Content-Type: application/json

{
  "refresh_token": "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VyXzEyMyIsInR5cGUiOiJyZWZyZXNoIn0.xyz456"
}
```

The auth server verifies the refresh token and issues a new access token. If using **refresh token rotation**, the old refresh token is also invalidated and a new one is issued.

### Logout

JWTs are stateless — there's no server-side session to destroy. Logout strategies:

- **Short expiration + client deletion:** Delete the tokens client-side. If the access token expires in 15 minutes, the attacker's window is small.
- **Refresh token revocation:** Keep a blocklist of revoked refresh token JTI values. Blacklist the refresh token on logout; access tokens continue to work until they expire.
- **Access token revocation:** Maintain a blocklist for access tokens (reintroduces database lookups — partially defeats the point of JWT).

For most applications, short access token lifetimes + refresh token revocation is the right balance.

## Token storage security

Where to store tokens in a browser:

| Storage | XSS risk | CSRF risk | Notes |
|---------|----------|-----------|-------|
| Memory (JS variable) | Low | Low | Lost on page refresh |
| HttpOnly Cookie | None | Medium (need CSRF protection) | Recommended for refresh tokens |
| localStorage | High | None | Accessible to any script on the page |
| sessionStorage | High | None | Cleared on tab close |

**Best practice:** Store the access token in memory (a JS variable or React context). Store the refresh token in an HttpOnly, SameSite=Strict cookie. This keeps the sensitive refresh token inaccessible to JavaScript.

## Node.js implementation

```js
const jwt = require('jsonwebtoken');

// Issue
const token = jwt.sign(
  { sub: 'user_123', roles: ['admin'] },
  process.env.JWT_SECRET,
  { expiresIn: '15m', issuer: 'auth.example.com', audience: 'api.example.com' }
);

// Verify
try {
  const payload = jwt.verify(token, process.env.JWT_SECRET, {
    issuer: 'auth.example.com',
    audience: 'api.example.com',
  });
  console.log(payload.sub); // 'user_123'
} catch (err) {
  // TokenExpiredError, JsonWebTokenError, NotBeforeError
  console.error(err.name, err.message);
}
```

## Debug JWT tokens

Paste any JWT into [jwtinspect.io](/) to see the decoded header and payload instantly — useful for checking claims, expiration times, and algorithm choices during development.
