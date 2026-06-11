---
title: "Hex Color Codes Explained: How to Read, Write, and Use Them"
description: "Hex color codes are the standard way to specify colors in web design. Learn how to read the RR/GG/BB format, convert from RGB, use shorthand, and add transparency."
publishDate: 2026-06-07
updatedDate: 2026-06-07
author: "Editorial Team"
tags: ["hex color codes", "CSS colors", "RGB", "web design", "color reference"]
draft: false
heroImage: "/images/blog/hex-color-codes-hero.png"
---

If you've spent any time in a browser's developer tools, a design application, or a CSS file, you've encountered hex color codes. They appear everywhere: `#FF5733`, `#0A0A0A`, `#fff`. They're concise, widely supported, and once you understand their structure, entirely readable. Here's everything you need to know to work with them confidently.

## What Is a Hex Color Code?

A hexadecimal color code is a six-character string (preceded by a `#` symbol) that specifies a color by encoding its red, green, and blue channel values in base-16 (hexadecimal) notation. The full format is:

```
#RRGGBB
```

Where:
- `RR` is the red component (00 to FF)
- `GG` is the green component (00 to FF)
- `BB` is the blue component (00 to FF)

Each pair represents a number from 0 to 255 in decimal — the full range of a single RGB channel — expressed as two hexadecimal digits.

## Understanding Hexadecimal (Base 16)

Decimal (base 10) counts 0 through 9, then wraps to 10. Hexadecimal counts 0 through 9, then continues with letters A through F before wrapping to 10. This means:

- `0` in hex = 0 in decimal
- `9` in hex = 9 in decimal
- `A` in hex = 10 in decimal
- `F` in hex = 15 in decimal
- `10` in hex = 16 in decimal
- `FF` in hex = 255 in decimal

A two-digit hex number can represent values from 00 (0) to FF (255). That's exactly the range of a single RGB channel — which is why two hex digits map perfectly to one color channel.

## Reading a Hex Code

Take the color `#3A7BD5`:

- `3A` = red = 58 in decimal (a low-to-medium red value)
- `7B` = green = 123 in decimal (medium green)
- `D5` = blue = 213 in decimal (high blue)

The dominant channel here is blue, with a meaningful green component and relatively low red — so this is a medium-dark blue, which is exactly what you'd see if you rendered it.

With a bit of practice, you can read hex codes at a glance:

- **Both digits low (00–3F):** channel is in the darker range
- **Both digits in the middle (40–BF):** channel is in the midtone range
- **Both digits high (C0–FF):** channel is bright

So a code like `#CCBB44` would read as: moderately high red, moderately high green, low-ish blue — a golden yellow. That's a reasonable intuition even without converting to decimal.

## Common Hex Colors Reference

| Color | Hex Code | Notes |
|-------|----------|-------|
| Pure white | `#FFFFFF` | All channels at maximum |
| Pure black | `#000000` | All channels at zero |
| Pure red | `#FF0000` | Red at max, others at zero |
| Pure green | `#00FF00` | Green at max, others at zero |
| Pure blue | `#0000FF` | Blue at max, others at zero |
| Mid gray | `#808080` | All channels equal, midpoint |
| Dark gray | `#333333` | Common dark UI background |
| Light gray | `#CCCCCC` | Common border/divider color |
| Yellow | `#FFFF00` | Red + green at max |
| Cyan | `#00FFFF` | Green + blue at max |
| Magenta | `#FF00FF` | Red + blue at max |
| Orange | `#FF8000` | Max red, half green, no blue |
| Navy | `#001F5B` | Deep blue, very low red/green |
| Coral | `#FF6B6B` | High red, medium green and blue |
| Teal | `#008080` | No red, medium-equal green and blue |
| Gold | `#FFD700` | Max red, high green, no blue |
| Charcoal | `#36454F` | Dark blue-gray, common in design |

## The 3-Digit Shorthand

When both digits in each channel are identical, a hex code can be shortened to three characters:

- `#FFFF00` → `#FF0` (not valid; digits aren't paired duplicates)
- `#FFFF00` stays as `#FFFF00`
- `#FF6600` → `#F60`
- `#FFFFFF` → `#FFF`
- `#000000` → `#000`
- `#336699` → `#369`

The shorthand works because `#369` is expanded to `#336699` by the browser — each digit is simply doubled. This means shorthand codes can only represent a subset of the full 16.7 million colors available in the 6-digit format. They're useful for common values and quick prototyping.

## Adding Transparency: 8-Digit Hex Codes

The 6-digit hex format specifies a fully opaque color. To add transparency (alpha channel), you can use the 8-digit format:

```
#RRGGBBAA
```

Where `AA` is the alpha (transparency) value, from `00` (fully transparent) to `FF` (fully opaque). This format is supported in modern browsers and many design tools.

Examples:
- `#FF000080` — red at 50% opacity (80 in hex = 128 in decimal, roughly half of 255)
- `#0000FFCC` — blue at approximately 80% opacity (CC = 204 in decimal)
- `#FFFFFF00` — white at 0% opacity (invisible)

**Note on browser support:** The 8-digit hex format is well-supported in modern browsers (Chrome, Firefox, Safari, Edge) but may not work in very old browsers. CSS `rgba()` notation (`rgba(255, 0, 0, 0.5)`) is an alternative that has broader legacy support. In modern projects, 8-digit hex is generally fine.

## Hex Colors in CSS

In CSS, hex codes work in any property that accepts a color value:

```css
/* Text color */
color: #333333;

/* Background */
background-color: #F5F5F5;

/* Border */
border: 1px solid #E0E0E0;

/* With transparency (8-digit) */
background-color: #0000FF80;

/* Shorthand */
color: #fff;
```

Case doesn't matter in CSS — `#FF6600` and `#ff6600` are treated identically. Convention varies: some codebases use all-uppercase, some use all-lowercase. The main thing is consistency within a project.

## Hex vs RGB vs HSL: Which to Use?

All three formats specify the same colors. The difference is in readability and workflow:

**Hex** is compact and widely used. It's the native language of design tools and most color reference sources. Its weakness is that it's not intuitive — you can't easily adjust a color by reading a hex code.

**RGB** (`rgb(58, 123, 213)`) is more readable for understanding channel values but equally opaque for human color intuition.

**HSL** (`hsl(215, 63%, 54%)`) is the most human-readable format. It expresses hue (the color family, 0–360 degrees), saturation (how vivid, 0–100%), and lightness (how light or dark, 0–100%). This makes it easy to adjust — you can increase lightness to create a tint or reduce saturation to create a tone.

In CSS, all three formats are valid and functionally equivalent. Many developers work with hex for static colors (copying from design files or tools) and HSL for dynamic manipulation in CSS variables or component logic.

## Converting Between Hex and RGB

The conversion is straightforward:

**Hex to RGB:** Convert each two-digit hex pair to decimal.
- `#3A7BD5` → R: 3A = 58, G: 7B = 123, B: D5 = 213
- Result: `rgb(58, 123, 213)`

**RGB to hex:** Convert each decimal value (0–255) to a two-digit hex string.
- `rgb(255, 99, 71)` → R: FF, G: 63, B: 47
- Result: `#FF6347`

In practice, you'll rarely do this conversion by hand. Design tools, browser developer panels, and online color tools handle it automatically. colorpalette.io displays hex codes for every color in your generated palette, with conversion to RGB and HSL available alongside.

## Picking and Using Hex Codes in Your Workflow

For brand and design work, hex codes are the reliable common currency. They're specific (a six-character code means exactly one color), compact (easy to store and copy), and universally understood across design tools, CSS, and browser dev tools.

When building a color palette, start by generating or selecting your primary brand colors and noting their hex values. Use those hex codes as the canonical reference across your team — in design files, in code, in documentation. Consistency in hex codes across a product prevents the subtle color drift that happens when different team members pick "close enough" variations from memory.

The hex format also makes it easy to programmatically manipulate colors at scale. CSS custom properties, design tokens, and JavaScript color libraries all work naturally with hex strings. Once you have your core hex codes defined, the entire color system can be derived from them.

Understanding hex codes won't change what you see on screen — but it will change how confidently and efficiently you can work with color in any technical context.
