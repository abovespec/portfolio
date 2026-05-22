---
title: "How to Create a QR Code for WiFi: Share Your Network Instantly"
description: "Learn how to create a WiFi QR code so guests can join your network without typing a password. Covers the exact format, security types, and tips for printing."
publishDate: 2026-05-22
updatedDate: 2026-05-22
author: "Editorial Team"
tags: ["qr code", "wifi", "how-to", "networking", "guest access"]
draft: false
---

A WiFi QR code lets anyone join your network by scanning with their phone camera — no password typing required. It takes about a minute to set up and is one of the most practical QR code uses for homes, cafés, hotels, and offices.

## How WiFi QR codes work

When a smartphone camera (iOS 11+ or Android 10+) scans a WiFi QR code, the operating system automatically prompts the user to join the encoded network. No app required. The QR code contains a short text string that follows the WiFi provisioning format.

## The WiFi QR code format

The encoded string follows this structure:

```
WIFI:T:<security-type>;S:<SSID>;P:<password>;H:<hidden>;;
```

**Fields:**
- `T` — Security type: `WPA` (for WPA2/WPA3), `WEP`, or `nopass` (open networks)
- `S` — SSID: your network name
- `P` — Password
- `H` — `true` if the network is hidden, omit or leave blank if visible

**Example for a standard WPA2 home or business network:**
```
WIFI:T:WPA;S:CafeGuest;P:welcome2026;;
```

**Example for an open (no password) network:**
```
WIFI:T:nopass;S:AirportFreeWifi;;
```

**Example for a hidden network:**
```
WIFI:T:WPA;S:HiddenOfficeNet;P:s3cur3pass;H:true;;
```

Note the double semicolon `;;` at the end — this is required by the spec.

## Step-by-step: creating the QR code

1. Gather your network details: SSID (network name), password, and security type (check your router settings — almost all modern routers use WPA2 or WPA3, both encoded as `WPA`).
2. Construct the string using the format above.
3. Go to [QR code generator](/) and paste the string into the text/URL input field.
4. Set error correction to **M (15%)** or **Q (25%)** — more resilient if the printed code gets slightly damaged.
5. Download as SVG for print, or PNG for digital display.
6. Scan with your own phone to verify it works before printing.

## Handling special characters

If your SSID or password contains any of these characters, escape them with a backslash:

`\` `;` `,` `"` `:`

Example — password `pa$$:word` becomes `pa$$\:word` in the string:
```
WIFI:T:WPA;S:MyNetwork;P:pa$$\:word;;
```

If your SSID or password contains spaces, no escaping is needed — spaces are fine as-is.

## Printing and display tips

**Where to display it:**
- Framed sign on a café counter or restaurant table
- Hotel room door or welcome card
- Office reception desk
- Airbnb welcome book

**Sizing:**
- Counter sign: at least 5 × 5 cm (2 in) — guests scan from 30–50 cm away
- Table tent: 3 × 3 cm (1.2 in) is workable at close range
- Always include a quiet zone (white border) of at least 4 modules wide

**Label it clearly.** Print the network name and a short instruction like "Scan to join WiFi" next to the code. Some guests won't know what to do without a prompt.

**Include the password as plain text too.** Older devices and some security-conscious users may prefer to type it. Place the plain text below the QR code so the printed card serves both.

## Security considerations

**Do not use a QR code for your primary network.** Create a separate guest network on your router and encode those credentials. This way:
- Guests get internet access
- Your main devices and NAS stay on a separate, private network
- You can change the guest password without updating every device on your network

**WEP is insecure.** If your router only supports WEP, upgrade the firmware or replace the router. WEP can be cracked in minutes. Most modern routers support WPA2 or WPA3.

**Changing your password.** If you update your WiFi password, you need to generate a new QR code. This is a reason to use a password that you don't change frequently for a guest network, or to use a dynamic QR code that redirects to a page with updated credentials.

## Testing across devices

Before putting the QR code on display, scan it with:
- An iPhone (camera app, no third-party needed on iOS 11+)
- An Android phone (camera app on Android 10+, or Google Lens on older versions)

If the network join prompt doesn't appear, double-check:
1. The double semicolon `;;` at the end of the string
2. Escaped special characters in the password
3. The correct security type (`WPA` not `WPA2` — the spec uses `WPA` for both WPA2 and WPA3)

Generate your WiFi QR code at [qrcodegen.io](/).
