---
title: "QR Code for Business Card: vCard Setup and Best Practices"
description: "How to add a QR code to your business card using the vCard format. Covers what data to include, sizing, placement, and how to keep contact details current."
publishDate: 2026-05-22
updatedDate: 2026-05-22
author: "Editorial Team"
tags: ["qr code", "business card", "vcard", "networking", "professional"]
draft: false
---

A QR code on a business card lets recipients save your contact details with a single scan — no manual typing. When done correctly, it encodes your full contact record directly in the code or links to an always-current profile. Here is how to set it up properly.

## Two approaches: vCard vs. URL

**Embedded vCard (no internet required)**
The QR code encodes your contact information directly. When scanned, the phone offers to add you to contacts immediately — even offline. Best for events, conferences, and situations where phone data is unreliable.

**URL to an online profile**
The QR code links to a LinkedIn profile, personal website, or digital business card service. The contact info lives online, so you can update it without reprinting cards. Requires an internet connection to scan.

For most business cards, the embedded vCard approach is the better choice: it works everywhere, adds no dependency on a third-party service, and transfers data instantly.

## The vCard format

vCard 3.0 is the most widely supported version across iOS and Android. Here is a complete example:

```
BEGIN:VCARD
VERSION:3.0
FN:Sarah Chen
N:Chen;Sarah;;;
ORG:Apex Solutions
TITLE:Head of Product
TEL;TYPE=WORK,VOICE:+1-415-555-0192
TEL;TYPE=CELL,VOICE:+1-415-555-0187
EMAIL;TYPE=WORK:sarah.chen@apexsolutions.com
URL:https://apexsolutions.com
ADR;TYPE=WORK:;;1200 Market St;San Francisco;CA;94102;USA
NOTE:Let's connect on LinkedIn: linkedin.com/in/sarahchen
END:VCARD
```

**Field reference:**

| Field | Purpose | Required? |
|-------|---------|-----------|
| `FN` | Full display name | Yes |
| `N` | Structured name (Last;First;;;) | Recommended |
| `ORG` | Company name | Optional |
| `TITLE` | Job title | Optional |
| `TEL` | Phone number (add TYPE for work/cell) | Optional |
| `EMAIL` | Email address | Recommended |
| `URL` | Website | Optional |
| `ADR` | Mailing address | Optional |
| `NOTE` | Free-form note | Optional |

## What data to include

**Keep it minimal.** Every additional field increases the amount of data in the QR code, which means more modules, smaller modules, and a harder-to-scan code. Include only what a new contact actually needs.

**Recommended minimum:**
- Full name (`FN` and `N`)
- Primary email
- Primary phone (cell or work, one number)
- Company and title if relevant

**Add if useful:**
- Website URL
- LinkedIn in the `NOTE` field (or as a second `URL`)
- Office address if clients visit you

**Skip:** Multiple redundant phone numbers, personal social handles, fax numbers, and secondary emails unless genuinely necessary.

## Generating the QR code

1. Write your vCard string in a text editor. Ensure it starts with `BEGIN:VCARD` and ends with `END:VCARD`.
2. Go to [QR code generator](/) and paste the full vCard string into the text input.
3. Set error correction to **M (15%)** — a good balance of data density and resilience for a business card.
4. If you want to add a logo, use **Q (25%)** or **H (30%)** instead.
5. Download as SVG for professional print production.

## Sizing for business cards

Standard business card dimensions are 85 × 54 mm (3.5 × 2.1 in) in the US, or 90 × 55 mm in Europe.

**Recommended QR code size on a business card: 18–22 mm (0.7–0.9 in).**

This is the practical minimum at typical business card scanning distance (10–20 cm). Smaller than 15 mm (0.6 in) risks scan failures on older phones.

**Quiet zone:** Maintain at least 3–4 mm of white space around the code. No design elements should touch or overlap the code.

**File format:** Always supply the QR code as SVG or high-resolution PNG (at least 600 × 600 px) to your print designer or print shop. Never use JPEG — compression artifacts corrupt the code.

## Placement on the card

**Back of the card** is the most common placement — it leaves the front for your name, title, and branding, and the back becomes a functional space.

**Bottom-right or bottom-left corner** on the back is typical. Some designers center it. Either works.

**Label it.** Print a small caption: "Scan to save contact" or "Save to contacts." Recipients unfamiliar with vCard QR codes may not know what happens when they scan it.

**Do not crowd it.** Give the QR code visual breathing room. A cluttered back with dense small text next to the code looks unprofessional and may reduce scan rates.

## Keeping contact info current

The main limitation of embedded vCard QR codes: if your phone number, email, or company changes, the QR code is outdated and you need to reprint.

**Strategies to minimize this:**
- Use an email address on a domain you own rather than a company address — company email changes when you change jobs
- Link to a personal website URL in addition to the vCard, so people can find current info even if individual fields change
- If you change jobs frequently, consider encoding a URL to your LinkedIn profile instead of a full vCard

## Testing

Before sending cards to print, test the QR code:
1. On an iPhone: open the camera app, point at the code, and confirm "Add to Contacts" appears
2. On an Android: use the camera app or Google Lens, confirm contact import prompt appears
3. Verify every field imports correctly — name, company, phone, and email

Print one test card and scan it from a physical copy, not just from your screen. Print quality and lamination can affect scan reliability.

Create your business card QR code at [qrcodegen.io](/).
