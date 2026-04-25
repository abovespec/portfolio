---
title: "Base64 Encoding Explained: How It Works and When to Use It"
description: "How Base64 encoding works: the alphabet, the 3-byte-to-4-character conversion, padding, and the URL-safe variant. With examples in Python, JavaScript, and Bash."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["base64", "encoding", "binary", "web development", "data"]
draft: false
---

Base64 encoding converts arbitrary binary data into a string of printable ASCII characters. It's used everywhere binary data needs to travel through text-based systems: email attachments, data URIs, HTTP Basic Auth headers, and JSON payloads carrying binary content.

## The problem Base64 solves

Many protocols were designed for text. Email (SMTP), HTTP headers, and JSON don't safely carry raw binary bytes — some byte values have special meaning (null terminators, line breaks, control characters) or aren't printable at all.

Base64 solves this by representing every possible byte value using only 64 safe characters: uppercase A–Z, lowercase a–z, digits 0–9, `+`, and `/` (plus `=` for padding). These 64 characters have consistent, well-defined representations across every text encoding.

## The 64-character alphabet

The Base64 alphabet maps 6-bit values (0–63) to characters:

```
0–25  →  A–Z
26–51 →  a–z
52–61 →  0–9
62    →  +
63    →  /
(pad) →  =
```

## How encoding works

Base64 processes input in **3-byte groups** and converts each group to **4 output characters**.

**Step 1:** Take 3 bytes (24 bits total).

```
Input bytes: 0x4D 0x61 0x6E
Binary:      01001101 01100001 01101110
```

**Step 2:** Split the 24 bits into four 6-bit groups.

```
011001  010110  000101  101110
```

**Step 3:** Map each 6-bit value to its Base64 character using the alphabet.

```
011001 = 25 → Z
010110 = 22 → W
000101 =  5 → F
101110 = 46 → u
```

So `"Man"` (bytes 0x4D 0x61 0x6E) encodes to `"TWFu"`.

You can verify:

```python
import base64
base64.b64encode(b"Man")  # b'TWFu'
```

## Padding

When the input length isn't a multiple of 3, Base64 pads the output with `=` characters.

- **1 leftover byte** → encode as 2 characters + `==`
- **2 leftover bytes** → encode as 3 characters + `=`

```python
base64.b64encode(b"M")     # b'TQ=='  (1 byte → 2 chars + 2 padding)
base64.b64encode(b"Ma")    # b'TWE='  (2 bytes → 3 chars + 1 padding)
base64.b64encode(b"Man")   # b'TWFu'  (3 bytes → 4 chars, no padding)
```

The `=` padding makes the output length always a multiple of 4.

## Size overhead

Base64 encoding increases size by approximately **33%**. Three input bytes become four output characters. A 3 MB image becomes a 4 MB Base64 string.

```
Output size = ⌈input_bytes / 3⌉ × 4
```

## URL-safe Base64

Standard Base64 uses `+` and `/`, which have special meaning in URLs. The URL-safe variant (Base64URL, defined in [RFC 4648 §5](https://www.rfc-editor.org/rfc/rfc4648#section-5)) replaces them:

- `+` → `-`
- `/` → `_`
- Padding (`=`) is often omitted

```python
import base64

data = b"\xfb\xff\xfe"
standard = base64.b64encode(data)     # b'+//+'
url_safe  = base64.urlsafe_b64encode(data)  # b'-__+'
```

JWT tokens use URL-safe Base64 without padding.

## Encoding in common languages

**Python:**

```python
import base64

encoded = base64.b64encode(b"Hello, World!")
# b'SGVsbG8sIFdvcmxkIQ=='

decoded = base64.b64decode(b"SGVsbG8sIFdvcmxkIQ==")
# b'Hello, World!'

# URL-safe
base64.urlsafe_b64encode(b"\xfb\xff\xfe")
base64.urlsafe_b64decode(b"-__+")
```

**JavaScript (browser):**

```js
// Encode (btoa works on binary strings, not raw bytes)
btoa("Hello, World!")          // "SGVsbG8sIFdvcmxkIQ=="

// Decode
atob("SGVsbG8sIFdvcmxkIQ==")  // "Hello, World!"

// For arbitrary binary data (Uint8Array):
const bytes = new Uint8Array([72, 101, 108, 108, 111]);
const b64 = btoa(String.fromCharCode(...bytes));
```

For modern Node.js:

```js
Buffer.from("Hello, World!").toString("base64")
// "SGVsbG8sIFdvcmxkIQ=="

Buffer.from("SGVsbG8sIFdvcmxkIQ==", "base64").toString("utf8")
// "Hello, World!"
```

**Bash:**

```bash
echo -n "Hello, World!" | base64
# SGVsbG8sIFdvcmxkIQ==

echo "SGVsbG8sIFdvcmxkIQ==" | base64 -d
# Hello, World!
```

## Common use cases

**HTTP Basic Auth:**

```
Authorization: Basic <base64(username:password)>
```

Never use Basic Auth over unencrypted HTTP — the encoding is trivially reversible.

**Data URIs (inline images in HTML/CSS):**

```html
<img src="data:image/png;base64,iVBORw0KGgo..." />
```

```css
background-image: url("data:image/svg+xml;base64,...");
```

**Email attachments (MIME):**

Email protocols carry attachments as Base64-encoded blocks in `Content-Transfer-Encoding: base64` sections.

**API payloads:**

JSON doesn't have a binary type. Sending binary data (keys, certificates, files) in a JSON API typically uses Base64.

## When NOT to use Base64

- **Storage:** Don't store binary data as Base64 in a database when you can store it as BYTEA or BLOB — you're adding 33% overhead and encoding/decoding cost.
- **Passwords:** Base64 is not encryption or hashing. A Base64-encoded password provides no security — decode it in one function call.
- **Large transfers:** The 33% size overhead matters for large files. Binary HTTP transfers are more efficient.

## Quick online encoder

For a fast encode/decode without writing code, use [encodeonline.io](/) — paste text or upload a file and get the Base64 output instantly.
