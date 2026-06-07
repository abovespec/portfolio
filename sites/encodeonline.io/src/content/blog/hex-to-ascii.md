---
title: "Hex to ASCII Conversion: A Complete Guide with Examples"
description: "Learn how hex encoding works, how ASCII maps to hex values, and how to convert hex strings to readable text using Python, JavaScript, and command-line tools."
publishDate: 2026-06-07
updatedDate: 2026-06-07
author: "Editorial Team"
tags: ["hex", "ascii", "encoding", "conversion", "python"]
draft: false
---

Hexadecimal (hex) encoding is ubiquitous in computing: memory addresses, color codes, cryptographic digests, network packet dumps, and binary file inspection all use it. Being able to read hex and convert it to ASCII text is a practical skill for anyone working with low-level data, network protocols, or binary formats.

## What is hexadecimal encoding?

Hexadecimal is base-16 — it uses sixteen symbols to represent values: the digits 0–9 and the letters A–F (or a–f). Each hex digit represents exactly 4 bits. Two hex digits represent one byte (8 bits).

```
Binary:  1010 1111
Hex:     A    F
Decimal: 175
```

Because one byte maps cleanly to exactly two hex digits, hexadecimal is the most natural format for representing raw binary data in a human-readable way.

## What is ASCII?

ASCII (American Standard Code for Information Interchange) is a character encoding standard that maps 128 characters to integer values 0–127. It covers:

- Control characters (0–31): non-printable characters like newline (10), tab (9), null (0)
- Printable characters (32–126): space, punctuation, digits 0–9, uppercase A–Z, lowercase a–z
- Delete (127): DEL control character

Each ASCII character has a decimal value, a hexadecimal value, and a binary representation. These are all the same byte — just different ways of writing it.

## ASCII to hex mapping: the key characters

Here are the most commonly encountered ASCII characters and their hex equivalents:

| Character | Decimal | Hex | Notes |
|-----------|---------|-----|-------|
| (space) | 32 | 20 | Word separator |
| ! | 33 | 21 | Exclamation mark |
| " | 34 | 22 | Double quote |
| # | 35 | 23 | Hash / number sign |
| 0 | 48 | 30 | Digit zero |
| 1 | 49 | 31 | Digit one |
| 9 | 57 | 39 | Digit nine |
| A | 65 | 41 | Uppercase A |
| B | 66 | 42 | Uppercase B |
| Z | 90 | 5A | Uppercase Z |
| a | 97 | 61 | Lowercase a |
| b | 98 | 62 | Lowercase b |
| z | 122 | 7A | Lowercase z |
| ~ | 126 | 7E | Tilde (last printable) |

The pattern is memorable: uppercase letters start at hex `41`, lowercase letters start at hex `61` (32 decimal higher, because the space character separates the two ranges), and digits start at hex `30`.

## The conversion process

Converting a hex string to ASCII requires three steps per character:

1. Take a pair of hex digits
2. Convert the pair to its decimal value
3. Map the decimal value to the corresponding ASCII character

### Example: converting "48 65 6C 6C 6F"

```
48  →  decimal 72  →  ASCII 'H'
65  →  decimal 101 →  ASCII 'e'
6C  →  decimal 108 →  ASCII 'l'
6C  →  decimal 108 →  ASCII 'l'
6F  →  decimal 111 →  ASCII 'o'
```

Result: **"Hello"**

### Example: decoding a hex dump

Here is a raw hex dump from a network packet:

```
47 45 54 20 2F 20 48 54 54 50 2F 31 2E 31 0D 0A
```

Decoding each pair:

```
47 → G    45 → E    54 → T    20 → (space)
2F → /    20 → (space)
48 → H    54 → T    54 → T    50 → P
2F → /    31 → 1    2E → .    31 → 1
0D → (carriage return)    0A → (newline)
```

Result: `GET / HTTP/1.1\r\n` — the first line of an HTTP/1.1 request.

## How hex encoding is used in practice

### Hex dumps for binary file inspection

When you need to examine the raw bytes of a binary file, hex editors and the `xxd` command produce hex dumps:

```bash
xxd /usr/bin/python3 | head -4
# 00000000: 7f45 4c46 0201 0100 0000 0000 0000 0000  .ELF............
# 00000010: 0300 3e00 0100 0000 7055 0000 0000 0000  ..>.....pU......
```

The left column is the file offset (also in hex), the middle is raw bytes in hex, and the right is the ASCII representation of those bytes (with `.` for non-printable bytes).

The first four bytes `7f 45 4c 46` decode to `\x7f ELF` — the ELF magic number that identifies Linux executables.

### Network protocol debugging

When debugging TCP streams, TLS handshakes, or custom binary protocols, tools like Wireshark display captured packets in hex. Being able to read hex and identify protocol fields is fundamental to network analysis.

### Cryptographic output

MD5 and SHA-256 hashes are displayed as hex strings:

```
SHA-256("hello") = 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
```

Each pair of characters represents one byte of the 32-byte (256-bit) output.

### Colors in CSS and HTML

CSS hex colors use the same base-16 format:

```css
color: #FF5733;
/*     RR GG BB
       FF = 255 (max red)
       57 = 87  (medium green)
       33 = 51  (low blue)
*/
```

### URL percent-encoding

URL percent-encoding represents each byte as `%XX` where XX is the hex value:

```
space  →  %20   (hex 20 = decimal 32 = ASCII space)
<      →  %3C   (hex 3C = decimal 60 = ASCII '<')
"      →  %22   (hex 22 = decimal 34 = ASCII '"')
```

## Command-line conversion

### xxd (Linux / macOS)

```bash
# Text to hex
echo -n "Hello" | xxd -p
# 48656c6c6f

# Hex to text
echo "48656c6c6f" | xxd -r -p
# Hello

# Formatted hex dump with ASCII sidebar
echo -n "Hello World!" | xxd
# 00000000: 4865 6c6c 6f20 576f 726c 6421           Hello World!
```

### echo with escape sequences

Bash and most shells support `\xHH` hex escape sequences:

```bash
echo -e '\x48\x65\x6c\x6c\x6f'
# Hello

printf '\x48\x65\x6c\x6c\x6f\n'
# Hello
```

### Python one-liner

```bash
python3 -c "print(bytes.fromhex('48656c6c6f').decode('ascii'))"
# Hello

python3 -c "print('Hello'.encode('ascii').hex())"
# 48656c6c6f
```

## Python examples

```python
# Hex string to ASCII text
hex_string = "48 65 6C 6C 6F 20 57 6F 72 6C 64"
hex_clean = hex_string.replace(" ", "")
text = bytes.fromhex(hex_clean).decode("ascii")
print(text)  # Hello World

# ASCII text to hex string
text = "Hello World"
hex_output = text.encode("ascii").hex()
print(hex_output)   # 48656c6c6f20576f726c64

# Formatted with spaces (matching common dump format)
hex_spaced = " ".join(hex_output[i:i+2] for i in range(0, len(hex_output), 2))
print(hex_spaced)   # 48 65 6c 6c 6f 20 57 6f 72 6c 64

# Convert a file to hex
with open("myfile.bin", "rb") as f:
    data = f.read()
print(data.hex())

# Decode hex that may contain non-ASCII bytes (use latin-1 or handle errors)
hex_with_extended = "c0a80101"  # 192.168.1.1 as raw IP bytes
ip_bytes = bytes.fromhex(hex_with_extended)
print(".".join(str(b) for b in ip_bytes))  # 192.168.1.1
```

### Handling non-ASCII bytes

Not all hex data decodes to valid ASCII. Raw binary data (images, executables, encrypted content) will contain byte values outside the 0–127 ASCII range:

```python
# This raises UnicodeDecodeError for bytes > 0x7F
try:
    bytes.fromhex("ff fe fd").decode("ascii")
except UnicodeDecodeError as e:
    print(f"Not valid ASCII: {e}")

# Use latin-1 (maps bytes 0x00-0xFF directly to Unicode code points)
text = bytes.fromhex("ff fe fd").decode("latin-1")
print(repr(text))  # '\xff\xfe\xfd'

# Or use 'errors' parameter to handle gracefully
text = bytes.fromhex("48 65 ff 6c 6f".replace(" ", "")).decode("ascii", errors="replace")
print(text)  # "He?lo" (0xFF replaced with ?)
```

## JavaScript examples

```js
// Hex to ASCII (browser and Node.js)
function hexToAscii(hex) {
  // Remove spaces and validate
  const clean = hex.replace(/\s/g, "");
  if (clean.length % 2 !== 0) throw new Error("Odd-length hex string");

  let result = "";
  for (let i = 0; i < clean.length; i += 2) {
    const byte = parseInt(clean.slice(i, i + 2), 16);
    result += String.fromCharCode(byte);
  }
  return result;
}

hexToAscii("48 65 6C 6C 6F");  // "Hello"
hexToAscii("47455420 2F20 485454502F312E310D0A");  // "GET / HTTP/1.1\r\n"

// ASCII to hex
function asciiToHex(text) {
  return Array.from(text)
    .map(c => c.charCodeAt(0).toString(16).padStart(2, "0"))
    .join("");
}

asciiToHex("Hello");  // "48656c6c6f"

// For binary data in Node.js, use Buffer
const buf = Buffer.from("48656c6c6f", "hex");
console.log(buf.toString("ascii"));  // Hello

const hex = Buffer.from("Hello").toString("hex");
console.log(hex);  // 48656c6c6f
```

## Common pitfalls

**Odd-length hex strings.** Hex bytes always come in pairs. If you have 5 hex characters, something is wrong (a leading zero was stripped, for example). `5` should be `05`.

**Case sensitivity.** `4F`, `4f`, and `4f` are all the same value. `parseInt("4F", 16)` works in JavaScript; `bytes.fromhex("4F")` works in Python.

**Spaces and separators.** Hex dumps often include spaces every 2 characters, colons (MAC addresses: `AA:BB:CC:DD:EE:FF`), or no separators at all. Strip separators before parsing.

**Big-endian vs little-endian.** Multi-byte integers in hex have byte order issues. The hex string `0100` could mean 256 (big-endian) or 1 (little-endian). Always know the byte order of your data source.

**Non-ASCII output.** Hex data from network packets, binary files, or encrypted content often contains byte values above 127 that are not valid ASCII. Use UTF-8 or binary decoding instead.

## Try hex conversion online

[encodeonline.io](/) includes a hex-to-text converter that handles hex strings with or without spaces, supports both ASCII and UTF-8 output, and shows the byte values for each character — useful for inspecting protocol data or verifying implementations.
