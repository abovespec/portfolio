---
title: "Base64 Encoding in Python: A Complete Guide with Examples"
description: "Learn how to encode and decode Base64 in Python using the base64 module. Covers standard, URL-safe, and file encoding with practical code examples."
publishDate: 2026-06-07
updatedDate: 2026-06-07
author: "Editorial Team"
tags: ["base64", "python", "encoding", "programming"]
draft: false
---

Python's standard library includes a full-featured `base64` module that handles encoding and decoding without any third-party dependencies. This guide covers every common use case with working code examples.

## The Basics: Encoding and Decoding

```python
import base64

# Encode bytes to Base64
data = b'Hello, World!'
encoded = base64.b64encode(data)
print(encoded)  # b'SGVsbG8sIFdvcmxkIQ=='

# Decode Base64 back to bytes
decoded = base64.b64decode(encoded)
print(decoded)  # b'Hello, World!'
```

**Important**: `b64encode()` takes `bytes` and returns `bytes`. Strings must be encoded to bytes first.

## Working with Strings

```python
import base64

# Encoding a string
text = "Hello, World!"
encoded = base64.b64encode(text.encode('utf-8'))
print(encoded)          # b'SGVsbG8sIFdvcmxkIQ=='
print(encoded.decode()) # 'SGVsbG8sIFdvcmxkIQ=='  (as a string)

# Decoding back to a string
decoded_bytes = base64.b64decode(encoded)
decoded_text = decoded_bytes.decode('utf-8')
print(decoded_text)     # 'Hello, World!'
```

A common pattern wrapping both operations:

```python
def b64_encode_str(text: str) -> str:
    return base64.b64encode(text.encode('utf-8')).decode('utf-8')

def b64_decode_str(encoded: str) -> str:
    return base64.b64decode(encoded.encode('utf-8')).decode('utf-8')

b64_encode_str("Hello")   # 'SGVsbG8='
b64_decode_str('SGVsbG8=')  # 'Hello'
```

## URL-Safe Base64

Standard Base64 uses `+` and `/` characters that are not safe in URLs and filenames. The `urlsafe_b64encode` variant uses `-` and `_` instead.

```python
# Standard Base64 — may contain + and /
standard = base64.b64encode(b'\xfb\xff\xfe')
print(standard)   # b'+//+'

# URL-safe Base64 — uses - and _ instead
url_safe = base64.urlsafe_b64encode(b'\xfb\xff\xfe')
print(url_safe)   # b'-__-'

# Decode URL-safe Base64
base64.urlsafe_b64decode(url_safe)  # b'\xfb\xff\xfe'
```

**When to use URL-safe Base64:**
- JWTs (JSON Web Tokens) use URL-safe Base64 in their header and payload
- Base64-encoded values in URL query parameters
- Filenames containing Base64 data
- Any context where `+` might be misinterpreted as a space

## Handling Padding

Base64 pads output to a multiple of 4 characters with `=`. When receiving Base64 from external sources, the padding is sometimes stripped. Python's `b64decode` requires correct padding.

```python
# Missing padding causes an error
base64.b64decode('SGVsbG8')  # raises binascii.Error: Incorrect padding

# Fix by adding padding
def safe_b64decode(s: str) -> bytes:
    # Add padding to make length a multiple of 4
    padding = 4 - len(s) % 4
    if padding != 4:
        s += '=' * padding
    return base64.b64decode(s)

safe_b64decode('SGVsbG8')  # b'Hello'
safe_b64decode('SGVsbG8=')  # b'Hello' (already padded)
```

Alternatively, use `validate=False` (the default) and Python will handle minor padding issues, or use the `urlsafe` variant which is more lenient:

```python
base64.b64decode('SGVsbG8=')  # works
base64.urlsafe_b64decode('SGVsbG8=')  # also works
```

## Encoding Files to Base64

A common use case: embedding file contents (images, PDFs) as Base64 strings.

```python
import base64

# Encode a file
with open('image.png', 'rb') as f:
    image_data = f.read()

encoded = base64.b64encode(image_data).decode('utf-8')
print(f"Base64 length: {len(encoded)} characters")

# Create a data URI for use in HTML/CSS
data_uri = f"data:image/png;base64,{encoded}"
```

```html
<!-- Use in HTML -->
<img src="data:image/png;base64,SGVsbG8...">
```

### Decoding a Base64 File

```python
import base64

# Decode Base64 back to a file
encoded_str = "SGVsbG8..."  # your Base64 string
file_data = base64.b64decode(encoded_str)

with open('output.png', 'wb') as f:
    f.write(file_data)
```

## Encoding for HTTP Basic Authentication

HTTP Basic Auth requires `username:password` encoded as Base64 in the `Authorization` header.

```python
import base64
import urllib.request

def make_basic_auth_header(username: str, password: str) -> str:
    credentials = f"{username}:{password}"
    encoded = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    return f"Basic {encoded}"

# Usage
auth_header = make_basic_auth_header("admin", "secret123")
# 'Basic YWRtaW46c2VjcmV0MTIz'

# With requests library
import requests
response = requests.get(
    'https://api.example.com/data',
    headers={'Authorization': auth_header}
)
# Or use requests' built-in auth parameter:
response = requests.get(
    'https://api.example.com/data',
    auth=('admin', 'secret123')  # requests handles the encoding
)
```

## Base64 in Emails (MIME)

When Python's `email` module attaches binary files, it uses Base64 encoding internally. You can work with this directly using `base64.encodebytes()`, which adds newlines every 76 characters per the MIME standard:

```python
# encodebytes adds \n every 76 chars (for MIME compliance)
mime_encoded = base64.encodebytes(b'Hello, World!')
print(mime_encoded)  # b'SGVsbG8sIFdvcmxkIQ==\n'

# b64encode does NOT add newlines
inline_encoded = base64.b64encode(b'Hello, World!')
print(inline_encoded)  # b'SGVsbG8sIFdvcmxkIQ=='
```

For most modern uses, `b64encode` (without line breaks) is preferred. Use `encodebytes` only when the receiving system requires MIME-compliant Base64.

## Performance Notes

Base64 encoding increases data size by approximately 33% (every 3 bytes become 4 Base64 characters). For large files:

```python
# For very large files, process in chunks
def encode_large_file(input_path: str, output_path: str):
    with open(input_path, 'rb') as infile, \
         open(output_path, 'w') as outfile:
        while True:
            chunk = infile.read(57)  # 57 bytes = 76 Base64 chars per line
            if not chunk:
                break
            outfile.write(base64.b64encode(chunk).decode('utf-8'))
            outfile.write('\n')
```

For quick online encoding/decoding without writing code, try [encodeonline.io](/) — it handles Base64 and many other encodings directly in the browser.
