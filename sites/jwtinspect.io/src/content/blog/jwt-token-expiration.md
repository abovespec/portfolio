---
title: "JWT Token Expiration: Access Tokens, Refresh Tokens, and Rotation"
description: "How to set JWT expiration times, handle token refresh, implement refresh token rotation, and choose the right access token lifetime for your use case."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["jwt", "token expiration", "refresh tokens", "security", "authentication"]
draft: false
---

JWT expiration is one of the most important — and most misunderstood — parts of JWT-based authentication. The right expiration strategy balances security (short tokens minimize damage from theft) and user experience (long tokens avoid frequent re-authentication).

## How expiration works

The `exp` claim is a Unix timestamp (seconds since the epoch). Any JWT library that verifies a token will reject it if the current time is past `exp`.

For more on this topic, see [*JWT vs Session Authentication: Which Should You Use?*](/blog/jwt-vs-session).

```json
{
  "sub": "user_123",
  "iat": 1714000000,
  "exp": 1714003600
}
```

Here, `iat` (issued at) is `1714000000` and `exp` is `1714003600` — a difference of 3600 seconds (1 hour).

Setting expiration in code:

```python
from datetime import datetime, timedelta, timezone

now = datetime.now(timezone.utc)
payload = {
    "sub": user_id,
    "iat": now,
    "exp": now + timedelta(minutes=15),
}
```

For more on this topic, see [*JWT Claims Explained: iss, sub, aud, exp, iat, nbf, and jti*](/blog/jwt-claims-explained).

```js
const token = jwt.sign(
  { sub: userId },
  SECRET,
  { expiresIn: '15m' }  // or '1h', '7d', 1800 (seconds)
);
```

## Access token lifetimes

Access tokens are the short-lived tokens sent with every API request. The shorter the lifetime, the smaller the window if a token is stolen.

| Lifetime | Tradeoff |
|----------|---------|
| < 5 minutes | Very secure; high refresh frequency; may cause UX friction |
| 15 minutes | Good balance; standard recommendation |
| 1 hour | Acceptable; longer exposure window |
| 24+ hours | High risk; token theft has a large window |

**Recommendation:** 15 minutes for most web applications. If you have a low-traffic API or want simplicity, 1 hour is acceptable. Never use multi-day access tokens.

## Refresh token lifetimes

Refresh tokens are used only to get new access tokens. They're longer-lived and should be stored securely (HttpOnly cookie, not localStorage).

| Use case | Refresh token lifetime |
|----------|----------------------|
| High-security app (banking, medical) | 1 day or session only |
| Standard web app | 7–30 days |
| Mobile app | 60–90 days |
| "Remember me" | Up to 1 year (with rotation) |

## The token refresh flow

When an access token expires, the client uses the refresh token to get a new one without requiring the user to log in again:

```
1. Client sends expired access token to protected endpoint
2. Server returns 401 Unauthorized
3. Client intercepts 401 and sends refresh token to /auth/refresh
4. Auth server validates refresh token, issues new access token
5. Client retries original request with new access token
```

**Client-side implementation (JavaScript):**

```js
async function fetchWithRefresh(url, options = {}) {
  let response = await fetch(url, {
    ...options,
    headers: {
      ...options.headers,
      Authorization: `Bearer ${getAccessToken()}`,
    },
  });

  if (response.status === 401) {
    const refreshed = await refreshAccessToken();
    if (!refreshed) {
      // Refresh failed — redirect to login
      window.location.href = '/login';
      return;
    }
    response = await fetch(url, {
      ...options,
      headers: {
        ...options.headers,
        Authorization: `Bearer ${getAccessToken()}`,
      },
    });
  }

  return response;
}

async function refreshAccessToken() {
  const response = await fetch('/auth/refresh', { method: 'POST', credentials: 'include' });
  if (!response.ok) return false;
  const { access_token } = await response.json();
  setAccessToken(access_token);
  return true;
}
```

The `credentials: 'include'` sends the HttpOnly refresh token cookie automatically.

## Refresh token rotation

**Without rotation:** A stolen refresh token can be used indefinitely (until it expires).

**With rotation:** Each time you use a refresh token to get a new access token, the old refresh token is invalidated and a new one is issued.

```python
def refresh_tokens(old_refresh_token: str) -> dict:
    # Verify the old refresh token
    payload = verify_refresh_token(old_refresh_token)
    
    # Check if it's been revoked
    if is_token_revoked(payload["jti"]):
        raise InvalidTokenError("Refresh token already used")
    
    # Revoke the old refresh token
    revoke_token(payload["jti"])
    
    # Issue new tokens
    return {
        "access_token": create_access_token(payload["sub"]),
        "refresh_token": create_refresh_token(payload["sub"]),
    }
```

**Benefit of rotation:** If a refresh token is stolen and used, the original legitimate user's next refresh attempt fails — alerting both the system and potentially the user to the compromise.

## Absolute expiration vs. idle expiration

**Absolute expiration:** Token expires N minutes after it was issued, regardless of activity.

**Sliding expiration (idle timeout):** Token expiration is pushed forward with each use. If the user is active, their session extends; if they're inactive, they're logged out.

JWT doesn't natively support sliding expiration, but you can approximate it:
- Issue a new access token with a fresh `exp` whenever the user makes a request (or at the refresh point)
- Use a server-side record to track last activity and expire refresh tokens after a period of inactivity

For more on this topic, see [*What Is a JWT Token? JSON Web Tokens Explained*](/blog/what-is-a-jwt-token).

## Clock skew handling

If the server issuing the token and the server verifying it have slightly different clocks, a token may appear to have expired a few seconds earlier or later than intended.

Libraries have a "leeway" option for this:

```python
jwt.decode(token, key, algorithms=["HS256"], leeway=10)  # 10-second tolerance
```

```js
jwt.verify(token, secret, { clockTolerance: 10 });  // seconds
```

A 10-30 second leeway is typically sufficient. Don't use large leeway values — they defeat the purpose of short-lived tokens.

## Check token expiration

Paste any JWT into [jwtinspect.io](/) to see the `exp` claim decoded to a human-readable date and time, alongside all other claims — helpful for quickly checking if a token is expired or when it will expire.
