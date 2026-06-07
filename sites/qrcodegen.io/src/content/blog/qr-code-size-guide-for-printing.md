---
title: "QR Code Size Guide for Printing: Minimum Sizes, DPI, and Scan Distance"
description: "The complete guide to QR code print sizing. Minimum dimensions by use case, DPI requirements, quiet zone rules, and how scan distance determines the size you need."
publishDate: 2026-05-22
updatedDate: 2026-05-22
author: "Editorial Team"
tags: ["qr code", "printing", "size", "dpi", "design"]
draft: false
---

Printing a QR code too small is the most common reason they fail to scan. This guide gives you exact sizing specifications for every print context, plus the DPI and file format requirements to ensure clean output.

## The fundamental rule: 10x scan distance

The most reliable sizing rule is that **the minimum scan distance is roughly 10 times the physical size of the QR code**. 

For more on this topic, see [*QR Code vs Barcode: Differences, Use Cases, and When to Use Each*](/blog/qr-code-vs-barcode).

- A 2.5 cm code scans from up to 25 cm away
- A 5 cm code scans from up to 50 cm away  
- A 10 cm code scans from up to 1 m away

For more on this topic, see [*Dynamic QR Code vs Static QR Code: What's the Difference?*](/blog/dynamic-vs-static-qr-code).

This is a floor, not a ceiling. Larger is always better. When in doubt, size up.

## Minimum sizes by use case

| Use case | Minimum size | Recommended size | Max scan distance |
|----------|-------------|-----------------|-------------------|
| Business card | 1.5 × 1.5 cm (0.6 in) | 2 × 2 cm (0.8 in) | 15–20 cm |
| Brochure / flyer | 2.5 × 2.5 cm (1 in) | 3.5 × 3.5 cm (1.4 in) | 25–35 cm |
| A4 / Letter document | 3 × 3 cm (1.2 in) | 4 × 4 cm (1.6 in) | 30–40 cm |
| Restaurant table tent | 3 × 3 cm (1.2 in) | 5 × 5 cm (2 in) | 20–50 cm |
| Poster (A3 / tabloid) | 5 × 5 cm (2 in) | 7 × 7 cm (2.8 in) | 50–70 cm |
| Retail shelf label | 2 × 2 cm (0.8 in) | 3 × 3 cm (1.2 in) | 15–30 cm |
| Storefront window | 10 × 10 cm (4 in) | 15 × 15 cm (6 in) | 1–1.5 m |
| Outdoor sign / banner | 20 × 20 cm (8 in) | 30 × 30 cm (12 in) | 2–3 m |
| Billboard | 40 × 40 cm (16 in) | 60 × 60 cm (24 in) | 4–6 m |

These measurements assume standard data density (a short URL). Codes encoding more data have more modules and may need to be larger to remain scannable.

For more on this topic, see [*How QR Codes Work: Encoding, Structure, and Error Correction*](/blog/how-qr-codes-work).

## DPI requirements

**DPI (dots per inch)** determines print sharpness. For QR codes specifically:

| Print type | Minimum DPI | Recommended DPI |
|-----------|------------|----------------|
| Standard office laser print | 200 DPI | 300 DPI |
| Professional offset print | 300 DPI | 300–600 DPI |
| Large format / banner | 72–150 DPI at final size | 150 DPI at final size |
| Fine art / photo print | 300 DPI | 600 DPI |

**The practical rule:** At 300 DPI, a 1000 × 1000 px PNG prints cleanly at approximately 8.5 × 8.5 cm (3.3 in). If you need a 5 cm code, a 600 × 600 px PNG at 300 DPI is sufficient.

If your QR code file is too small in pixels, the printer will upscale it, creating blurry edges on the modules. Blurry module edges are a common cause of scan failure in print.

## File format for print

**SVG is always the best choice for print.** SVG is vector-based — it scales to any size without quality loss. No pixels, no blur, no artifacts. Most professional print workflows accept SVG.

**PNG is the second choice.** Use PNG, not JPEG. JPEG compression introduces artifacts (small color shifts at the edges of modules) that can confuse scanners, especially on codes with high module density.

When generating from [QR code generator](/), always download the SVG version for any print work. Use PNG only if your print vendor or design tool cannot accept SVG.

## The quiet zone: white space around the code

The quiet zone is the blank margin surrounding the QR code. It is not decorative — scanners use it to locate the code boundary. Without an adequate quiet zone, the code may not be detected at all.

**Minimum quiet zone: 4 module widths on all sides.**

A "module" is the smallest square in the QR code grid. For a QR code with 25 modules across, printed at 5 cm, each module is 2 mm. The quiet zone should be at least 4 × 2 mm = 8 mm on each side.

In practice, aim for a margin of at least 3–4 mm on small codes (business card, label) and 5–10 mm on larger codes.

**Never bleed design elements into the quiet zone.** No text, graphics, or background patterns should touch or overlap the code's white border.

## Data density affects required size

The amount of data encoded determines the number of modules in the QR code. More modules = smaller individual modules at a given print size = harder to scan.

| Content type | Typical data length | Relative module density |
|-------------|--------------------|-----------------------|
| Short URL (30 chars) | Low | Low — can print smaller |
| Full URL with parameters (80+ chars) | Medium | Medium |
| WiFi string | Medium | Medium |
| vCard (200+ chars) | High | High — needs larger print |
| Plain text paragraph | Very high | Very high — size up significantly |

**Practical implication:** A short URL like `https://qrcodegen.io` can be printed at 2 cm and scan reliably. A full vCard with phone, email, and address may need 3–4 cm minimum to scan from the same distance.

Use the shortest possible URL for print QR codes. Link shorteners or a clean `/go/campaign` path on your own domain reduces data density and improves scan reliability at small sizes.

## Common print mistakes

**Printing on textured or colored paper.** Dark paper, textured stock, and kraft paper all reduce contrast. Use white or off-white coated stock for QR codes.

**Lamination glare.** Glossy lamination on table tents or cards can create specular glare that makes scanning impossible from certain angles. Use matte lamination for QR codes that will be scanned in ambient light.

**Printing on a curved surface.** QR codes on curved packaging (bottles, cups) may not scan reliably. Flat labels on curved surfaces are better than printing directly on the curve.

**Testing only on screen.** Always print a physical test copy and scan it in real-world lighting before committing to a full print run.

Generate print-ready QR codes at [qrcodegen.io](/).
