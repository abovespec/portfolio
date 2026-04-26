---
title: "QR Code for Website: Link Any Page to a Scannable Code"
description: "Create a QR code for any website URL. Covers URL optimization, UTM tracking, landing page tips, size requirements, and how to embed QR codes in print and digital content."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["qr code", "website", "url", "marketing", "utm tracking"]
draft: false
---

The most common QR code use case is linking to a website URL. Scan the code → open the URL in the device's browser. Here's how to do it well — from generating the code to tracking who scanned it.

## Creating a QR code for a URL

1. Copy the full URL of the page you want to link (including `https://`)
2. Paste it into [qrcodegen.io](/)
3. Choose error correction level M or H for print
4. Download as SVG (for print) or PNG (for digital use)

That's it for basic use. The sections below cover making it work better.

## Shorten the URL first

Longer URLs produce denser QR codes with more modules. Dense codes are harder to scan at small sizes.

**Before:** `https://example.com/products/summer-collection-2026?utm_source=qr&utm_medium=print&utm_campaign=june-flyer&utm_content=back-panel`

**After:** `https://example.com/s/june-flyer`

Options:
- **Custom path** on your own domain: `example.com/qr-menu` (best — no third-party dependency)
- **Bit.ly or similar**: `bit.ly/abc123` (easy, but you depend on their service)
- **UTM parameters as a redirect**: redirect a short URL to a long tracked URL

## Add UTM tracking

UTM parameters let your analytics tool attribute traffic to the specific QR code:

```
https://example.com/landing?utm_source=qr&utm_medium=print&utm_campaign=storefront-2026
```

Recommended UTM parameters for QR codes:

| Parameter | Value | Example |
|-----------|-------|---------|
| `utm_source` | `qr` | Origin is a QR code |
| `utm_medium` | Placement type | `print`, `digital`, `email` |
| `utm_campaign` | Campaign name | `spring-sale`, `menu-2026` |
| `utm_content` | Specific code | `front-door`, `table-tent` |

If you have multiple QR codes in the same campaign, `utm_content` distinguishes them.

Keep the full UTM URL in a spreadsheet for your records — the QR code itself won't tell you what UTM parameters it contains without scanning.

## Landing page tips

The landing page should be:
- **Mobile-first** — 95%+ of scans happen on phones
- **Fast loading** — under 2 seconds on mobile; people abandon slow pages
- **Specific** — send to the exact page, not the homepage
- **Relevant to context** — if the QR is on a product package, link to that product

Avoid linking to:
- PDFs directly (bad mobile UX; put the PDF behind a page)
- Files that trigger a download
- Login walls (if the user just found you)

## QR code for restaurant menu

```
URL: https://yourrestaurant.com/menu?utm_source=qr&utm_medium=print&utm_campaign=table
```

If the menu changes seasonally, set up a redirect on your own domain:
```
https://yourrestaurant.com/menu → redirects to current menu PDF/page
```

Change the redirect target whenever the menu updates — the QR code never changes.

## QR code for events

For ticket validation or check-in, each QR code should encode a unique identifier:

```
https://yourapp.com/checkin/event-2026/ticket-id-abc123
```

The backend validates the ticket ID on scan. This is a different use case from marketing QR codes — here the data inside the QR code must be unique per ticket.

## Embedding QR codes in email and digital content

QR codes in email are unusual — people read email on their phone and would have to scan with a second device. Use a hyperlinked button or text instead for email.

For digital contexts where QR codes make sense (digital signage, websites shown on a second screen):
- Use PNG at 256–512px
- Maintain the quiet zone by not placing the image flush against other elements
- Test that the code is scannable from the screen

## Size for print

| Print format | Minimum QR size | Recommended |
|-------------|----------------|------------|
| Business card | 1.5 cm | 2 cm |
| A5 flyer | 3 cm | 4 cm |
| A4 flyer | 4 cm | 5 cm |
| A3 poster | 5 cm | 7 cm |
| Roll-up banner | 8 cm | 12 cm |

Always export as SVG or PDF for print. Never use JPEG.

Generate QR codes for your website at [qrcodegen.io](/).
