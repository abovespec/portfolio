---
title: "How to Add a Logo to a QR Code: Error Correction and Best Practices"
description: "Learn how to safely add a logo or image to a QR code without breaking it. Covers error correction levels, logo size limits, contrast rules, and software options."
publishDate: 2026-05-22
updatedDate: 2026-05-22
author: "Editorial Team"
tags: ["qr code", "logo", "branding", "design", "error correction"]
draft: false
---

Adding a logo to a QR code is one of the most common branding requests — and one of the most common ways to break a QR code. Done correctly, it looks polished and still scans reliably. Done wrong, the code becomes unreadable. This guide covers the right way to do it.

## Why logos and QR codes can coexist

QR codes include built-in error correction. When part of the code is obscured or damaged, the scanner uses redundant data to reconstruct the original content. There are four error correction levels:

| Level | Redundancy | Max data recovery |
|-------|-----------|------------------|
| L | Low | 7% |
| M | Medium | 15% |
| Q | Quartile | 25% |
| H | High | 30% |

A logo placed in the center of a QR code obscures some modules. As long as the logo covers less than the recoverable percentage of the code's surface area, the scanner can still decode it.

**For logo use, always choose H (30%) or Q (25%) error correction.** This is non-negotiable. If you generate a code at L and overlay a logo, you will almost certainly break the code.

## The logo size rule

The safe maximum logo size is **30% of the QR code's total area** when using H-level error correction. In practice, keeping the logo to **20–25%** provides a safety margin.

For more on this topic, see [*QR Code Best Practices: Design, Size, Placement, and Testing*](/blog/qr-code-best-practices).

For a QR code that is 100 × 100 mm, the logo should be no larger than 25 × 25 mm (625 sq mm = 25% of 10,000 sq mm total area). For most use cases, a logo of 20–22% of the code area scans reliably.

**Square logos are easier to size.** If your logo is wide and short (landscape), you may need to add white padding to make it square before inserting it — this reduces the effective obscured area.

## Step-by-step: adding a logo

**Method 1: Use a generator with built-in logo support**

1. Go to [QR code generator](/).
2. Enter your URL or content.
3. Set error correction to **H (30%)**.
4. Use the logo upload feature to add your image.
5. Ensure the generator scales the logo automatically to a safe size.
6. Download as SVG or high-resolution PNG.
7. Scan to verify.

**Method 2: Manual overlay in a design tool (Figma, Illustrator, Photoshop)**

1. Generate the QR code at error correction level H, download as SVG.
2. Open the SVG in your design tool.
3. Prepare your logo: ideally PNG with transparent background, or SVG.
4. Center the logo over the QR code.
5. Scale the logo so it covers no more than 25% of the code area.
6. Optionally add a white or solid background behind the logo to mask the modules clearly — this improves readability.
7. Export the final design as SVG or PNG.
8. Scan to verify — do not skip this step.

## Do's and don'ts

**Do:**
- Use error correction level H when adding any logo
- Add a white or solid background behind the logo (a "logo plate") to create clean contrast
- Keep the logo centered — the center of a QR code has less structural importance than the three corner finder patterns
- Test on both iOS and Android before finalizing
- Keep the logo simple — complex, detailed logos at small sizes become noise

For more on this topic, see [*How to Create a QR Code: A Complete Beginner's Guide*](/blog/how-to-create-a-qr-code).

**Don't:**
- Obscure the three square finder patterns in the corners — these are essential for decoding and must not be covered
- Use a semi-transparent logo — transparency over the modules creates ambiguous contrast
- Invert the QR code colors when using a logo (light modules on dark background) — many scanners struggle with inverted codes
- Assume it works without testing — even a correctly sized logo can create scan problems at certain print sizes

## Contrast and color

The QR code must maintain sufficient contrast between its dark and light modules. When adding a colored logo:

- The logo's background plate should match the QR code's light module color (usually white)
- The QR code modules should remain high contrast — black on white is most reliable
- If using a colored QR code, verify contrast ratio is at least 4:1 between dark and light modules

Avoid placing a dark logo directly over dark modules without a white plate — this creates a blended area that scanners cannot resolve.

## Sizing considerations at print

A QR code with a logo needs to be somewhat larger than a plain QR code of equivalent data, because the logo obscures modules that would otherwise aid scanning. As a rule of thumb:

- For business cards: 20 mm minimum (compared to 15 mm for a plain code)
- For flyers and posters: 40 mm minimum for logo codes
- At very small print sizes (under 20 mm), skip the logo — it will hurt scan reliability

For more on this topic, see [*QR Code Size Guide for Printing: Minimum Sizes, DPI, and Scan Distance*](/blog/qr-code-size-guide-for-printing).

## Testing: the critical final step

Always test the finished code before printing at scale:

1. Export the final file (not a screen capture — export the actual file)
2. Open it on your phone from camera roll or a printed test copy
3. Scan with iPhone camera app
4. Scan with Android camera app or Google Lens
5. Scan in lower light conditions (a café table, not just bright studio light)

If the code fails to scan, the logo is likely too large or the error correction level was not set to H. Regenerate the code with H error correction and reduce the logo to 20% of the code area.

Generate a QR code with logo support at [qrcodegen.io](/).
