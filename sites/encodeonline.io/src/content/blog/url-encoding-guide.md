---
title: "URL Encoding (Percent-Encoding): The Complete Guide"
description: "URL encoding converts special characters to percent-encoded %XX sequences. Learn which chars need encoding, encodeURI vs encodeURIComponent, and how to encode URLs in any language."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["url encoding", "percent encoding", "javascript", "web development", "http"]
draft: false
---

URL encoding (formally called **percent-encoding**, defined in [RFC 3986](https://www.rfc-editor.org/rfc/rfc3986)) converts characters that aren't safe in a URL into a `%XX` form, where `XX` is the byte's hexadecimal value.

## Why URLs need encoding

URLs are ASCII text, but they can represent resources with names containing spaces, non-ASCII characters, or characters that have reserved meaning in URL syntax (like `?`, `#`, `&`).

```
# Invalid URL — space not allowed
https://example.com/search?q=hello world

# Valid, percent-encoded URL
https://example.com/search?q=hello%20world
```

Without encoding, a space in a query string would be ambiguous or invalid, and special characters like `#` would be interpreted as URL fragment separators.

## Unreserved characters (never encoded)

RFC 3986 defines characters that are "unreserved" — they can appear anywhere in a URL without needing encoding:

```
A–Z  a–z  0–9  -  .  _  ~
```

Everything else must be percent-encoded when it appears as data (not as part of URL structure).

## Reserved characters (context-dependent)

Reserved characters have structural meaning in URLs and should be encoded when used as data:

```
:  /  ?  #  [  ]  @  !  $  &  '  (  )  *  +  ,  ;  =
```

For example, `&` separates query parameters. If a parameter value contains `&`, it must be encoded as `%26`:

```
# Wrong — the & in the value breaks query parsing
?name=Alice&Bob&age=30

# Correct
?name=Alice%26Bob&age=30
```

## Percent-encoding format

Each byte is encoded as `%` followed by two uppercase hex digits:

```
space  →  %20
!      →  %21
"      →  %22
#      →  %23
$      →  %24
%      →  %25  (percent itself)
&      →  %26
'      →  %27
(      →  %28
+      →  %2B
/      →  %2F
=      →  %3D
?      →  %3F
@      →  %40
```

For non-ASCII characters, encode the UTF-8 byte sequence. The € sign (€) is `0xE2 0x82 0xAC` in UTF-8, so it encodes as `%E2%82%AC`.

## JavaScript: encodeURI vs encodeURIComponent

JavaScript has two built-in encoding functions with different scopes:

**`encodeURI()`** — encodes a complete URL. Leaves structural characters (`/ : ? # &`) unencoded because they're part of the URL structure:

```js
encodeURI("https://example.com/search?q=hello world&lang=en")
// "https://example.com/search?q=hello%20world&lang=en"
// Note: ? and & are NOT encoded — they're structural
```

**`encodeURIComponent()`** — encodes a URL component (a query value, a path segment). Encodes everything except unreserved characters:

```js
encodeURIComponent("hello world")   // "hello%20world"
encodeURIComponent("a=1&b=2")       // "a%3D1%26b%3D2"
encodeURIComponent("€100")          // "%E2%82%AC100"
```

**The rule:** Use `encodeURIComponent()` for values that go *inside* a URL (query string values, path segments). Use `encodeURI()` only when encoding a complete URL that you're not constructing — it's rare to need it directly.

```js
// Building a URL — use encodeURIComponent for each value
const name = "Alice & Bob";
const url = `https://example.com/search?q=${encodeURIComponent(name)}`;
// "https://example.com/search?q=Alice%20%26%20Bob"
```

**`decodeURIComponent()`** reverses the encoding:

```js
decodeURIComponent("hello%20world")  // "hello world"
decodeURIComponent("a%3D1%26b%3D2") // "a=1&b=2"
```

## Python: urllib.parse

```python
from urllib.parse import quote, unquote, urlencode

# Encode a URL component (like encodeURIComponent)
quote("hello world")      # "hello%20world"
quote("a=1&b=2")          # "a%3D1%26b%3D2"
quote("€100")             # "%E2%82%AC100"

# Decode
unquote("hello%20world")  # "hello world"

# Build a query string
params = {"q": "hello world", "lang": "en", "page": 1}
urlencode(params)
# "q=hello+world&lang=en&page=1"
# Note: urlencode uses + for spaces in query strings (form encoding)
```

**`quote` vs `urlencode` for spaces:**
- `quote()` encodes space as `%20`
- `urlencode()` encodes space as `+` (HTML form encoding, `application/x-www-form-urlencoded`)

Both are valid and interoperable; `+` for spaces is the form encoding convention; `%20` is the URI encoding convention.

## Other languages

**Go:**

```go
import "net/url"

encoded := url.QueryEscape("hello world & more")
// "hello+world+%26+more"

decoded, _ := url.QueryUnescape("hello+world+%26+more")
// "hello world & more"

// PathEscape uses %20 not + for spaces (correct for path segments)
url.PathEscape("my file name.txt")
// "my%20file%20name.txt"
```

**Ruby:**

```ruby
require 'uri'

URI.encode_www_form_component("hello world")  # "hello+world"
URI.encode_uri_component("hello world")       # "hello%20world" (Ruby 3.1+)
URI.decode_www_form_component("hello+world")  # "hello world"
```

**Bash:**

```bash
python3 -c "import urllib.parse; print(urllib.parse.quote('hello world'))"
# hello%20world
```

## Common mistakes

**Double-encoding:** Encoding an already-encoded string:
```js
encodeURIComponent("hello%20world")
// "hello%2520world" — the % itself got encoded to %25
```

Always decode before re-encoding, or check if the input is already encoded.

**Not encoding `+` in query values:** Some decoders interpret `+` as a space (form encoding). If a value might contain `+`, encode it as `%2B`.

**Encoding the whole URL with encodeURIComponent:** This breaks the structural characters (`/`, `:`, etc.) in the base URL.

## Online URL encoder

To encode or decode a URL or query string, use [encodeonline.io](/) — handles percent-encoding, decoding, and shows the decoded form side by side.
