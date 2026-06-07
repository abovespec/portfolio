---
title: "Dynamic QR Code vs Static QR Code: What's the Difference?"
description: "Compare dynamic and static QR codes: editability, tracking, URL redirects, and when to use each. Includes use cases for print, marketing, and permanent links."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["qr code", "dynamic qr code", "static qr code", "marketing", "tracking"]
draft: false
---

Static and dynamic QR codes look identical — they're both scannable squares — but they work very differently. The choice affects whether you can edit the destination, track scans, and how much data the code contains.

## Static QR codes

A **static QR code** encodes the destination directly in the code's modules. The URL or text is baked into the pattern.

For more on this topic, see [*How to Create a QR Code: A Complete Beginner's Guide*](/blog/how-to-create-a-qr-code).

**Characteristics:**
- The content is permanent — once printed, it can't be changed
- Free to generate, no account required
- No tracking — you won't know how many times it was scanned
- Works offline — no redirect service needed
- Can be shared freely — no dependency on a third-party service

**When to use static:**
- Permanent destinations that won't change (product pages, social profiles)
- One-off use cases (event, document)
- Situations where you don't need tracking
- Privacy-sensitive contexts where you don't want a third party to see scan data
- When you want the code to work even if a redirect service goes down

**Example:** A QR code for your GitHub profile page — `https://github.com/username` — is unlikely to change and doesn't need tracking.

For more on this topic, see [*QR Code for Website: Link Any Page to a Scannable Code*](/blog/qr-code-for-website).

## Dynamic QR codes

A **dynamic QR code** encodes a short URL that redirects to the actual destination. The redirection is managed by the QR code service.

**Characteristics:**
- The destination can be changed without reprinting the QR code
- Scan tracking: see when, where (roughly), and how often the code was scanned
- Requires a third-party redirect service (or your own redirect infrastructure)
- The code encodes a short URL (shorter data = smaller, denser-free code)
- The code stops working if the redirect service goes down

**When to use dynamic:**
- Print campaigns where the destination might change (seasonal promotions, menus)
- Marketing materials where scan analytics matter
- Situations where you might want to redirect traffic based on time or device
- Testing multiple destinations (A/B testing)

## Feature comparison

| Feature | Static | Dynamic |
|---------|--------|---------|
| Editable destination | No | Yes |
| Scan tracking | No | Yes |
| Cost | Free | Usually paid |
| Works offline | Yes | Redirect required |
| Depends on third-party | No | Yes |
| Code size | Larger (full URL) | Smaller (short URL) |
| Privacy | Higher | Lower |

For more on this topic, see [*QR Code Best Practices: Design, Size, Placement, and Testing*](/blog/qr-code-best-practices).

## Tracking with static codes (using UTM parameters)

You don't need a dynamic code to track scans — use UTM parameters in a static code:

```
https://example.com/product?utm_source=qr&utm_medium=print&utm_campaign=flyer-2026
```

When someone scans and visits, Google Analytics (or your analytics tool) captures the UTM parameters. You see the traffic attributed to the QR code without a redirect service.

This approach gives you tracking data in your existing analytics tool with no additional service dependency.

## Building your own redirect system

For teams who want dynamic codes without a third-party service:

```javascript
// Simple redirect server (Node.js / Express)
const express = require('express');
const app = express();

const redirects = {
  'abc123': 'https://example.com/landing-page',
  'def456': 'https://example.com/product',
};

app.get('/r/:code', (req, res) => {
  const destination = redirects[req.params.code];
  if (destination) {
    // Log the scan (to database, analytics, etc.)
    console.log(`Scan: ${req.params.code} at ${new Date().toISOString()}`);
    res.redirect(302, destination);
  } else {
    res.status(404).send('Not found');
  }
});
```

The QR code encodes `https://yourdomain.com/r/abc123`. You own the redirect and the analytics.

## Choosing the right type

**Start with static** for most use cases. Static codes are free, permanent, and don't depend on any service.

**Use dynamic** when:
- You have a print run that might need the destination updated after printing
- You need detailed analytics (geographic data, device type, scan counts over time)
- The cost and service dependency are acceptable

Generate QR codes at [qrcodegen.io](/).
