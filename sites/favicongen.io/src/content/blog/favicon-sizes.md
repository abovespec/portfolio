---
title: "Favicon Sizes: The Complete Size Guide for Every Browser and Device"
description: "A definitive guide to favicon sizes — from the original 16x16 ICO to Apple touch icons, Android PWA icons, and SVG favicons. Know exactly what to generate."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["favicon", "favicon sizes", "web design", "PWA", "apple touch icon"]
draft: false
---

If you have ever tried to figure out exactly which favicon sizes you need, you have probably ended up with a list that looks longer than you expected. The favicon landscape has grown from a single 16×16 file into a family of assets that spans browsers, operating systems, and device types. This guide walks through every size you need to know, what it is used for, and how to wire it all up in HTML.

## Where It All Started: 16×16

The original favicon specification called for a 16×16 pixel ICO file placed at the root of your domain as `favicon.ico`. When Internet Explorer 5 introduced favicons in 1999, this was the only size that mattered.

For more on this topic, see [*How to Create a Favicon for Your Website (Quick and Easy)*](/blog/how-to-create-a-favicon).

The 16×16 icon still matters today. It is the size displayed in browser tabs on most desktop browsers, in bookmark lists, and in browser history panels. At this resolution, every pixel counts. Your design needs to read clearly with almost no detail — a single initial, a simple geometric shape, or a heavily simplified version of your logo.

## The Modern Desktop Set

Modern browsers request larger versions of your favicon to display on higher-density screens and in contexts where more pixels are available. The sizes you should include in your ICO file or as separate PNG declarations are:

### 16×16

The baseline. Used in browser tabs, bookmark bars, and history.

### 32×32

The standard for most desktop browsers when the display is a standard-density screen. Windows uses this size for taskbar shortcuts. Most browsers that support multiple resolutions will prefer 32×32 over 16×16 when available.

### 48×48

Windows uses 48×48 for desktop shortcuts and some system UI contexts. Including it in your ICO container ensures your icon looks sharp in these locations.

### 64×64

Some browsers and operating systems use 64×64 in contexts like the Windows taskbar at certain display scaling levels. It is worth including if you want comprehensive coverage.

The simplest way to serve all of these at once is to pack them into a single multi-resolution ICO file. A favicon generator handles this automatically — you provide one source image and get an ICO that contains all the sizes in a single container.

## Apple Touch Icons (iOS and macOS)

When an iOS user taps "Add to Home Screen," Safari reaches for a specific icon type: the apple-touch-icon. This is a plain PNG with no transparency (Apple applies its own rounded-corner mask). The sizes Apple uses vary by device and context:

### 180×180

The primary apple-touch-icon size. This covers modern iPhones with standard and high-density screens. If you only declare one apple-touch-icon, make it 180×180.

For more on this topic, see [*Apple Touch Icon: Size, Setup, and Why You Need One*](/blog/apple-touch-icon).

### 152×152

Used by iPad. If you want a pixel-perfect result on iPads, include this size alongside 180×180.

### 120×120

Older iPhones (pre-Retina era equivalents). You can include this for broad compatibility, though most devices in active use today will pull the larger sizes.

Declare your apple-touch-icon in your HTML like this:

```html
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon-180x180.png">
<link rel="apple-touch-icon" sizes="152x152" href="/apple-touch-icon-152x152.png">
```

If you only include one, you can omit the `sizes` attribute and browsers will use it as the default:

```html
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
```

**Design note for apple-touch-icons:** Use a solid background color rather than transparency. Apple's rounding and display treatment assumes an opaque image. A transparent PNG will often render with a black background on iOS, which is rarely what you want.

## Android and Progressive Web Apps

Android Chrome and other Chromium-based mobile browsers look for icons declared in your Web App Manifest (`site.webmanifest` or `manifest.json`). These icons are used when a user adds your site to their home screen and when the browser launches your site as a PWA.

### 192×192

The minimum icon size required for Android to treat your site as installable. Chrome shows the install prompt and uses this icon for the home screen launcher.

### 512×512

Used for splash screens and high-density displays. Google recommends including this size alongside 192×192. It is also used in some operating system UI contexts when a PWA is installed.

Your manifest file includes them like this:

```json
{
  "icons": [
    &#123;
      "src": "/icon-192x192.png",
      "sizes": "192x192",
      "type": "image/png"
    &#125;,
    &#123;
      "src": "/icon-512x512.png",
      "sizes": "512x512",
      "type": "image/png"
    &#125;
  ]
}
```

For PWA icons, consider also generating a maskable version. Maskable icons follow the "safe zone" convention — your logo stays within the central 80% of the image, and the outer 20% can be filled with a background color. Android uses this to create adaptive icons that match the device's icon shape (circle, squircle, etc.).

## Windows Tiles

Older Windows and some versions of Microsoft Edge used a separate tile image system for pinned Start menu tiles and taskbar icons. The relevant sizes were 70×70, 150×150, and 310×310 (and a wide tile at 310×150).

For most sites today, Windows compatibility is covered by your standard ICO file and the general favicon declarations. The full tile system (declared via `browserconfig.xml` or meta tags) is increasingly optional unless you are specifically targeting Windows users who pin sites to the Start menu. If you want to cover it, a favicon generator will produce the assets and the configuration file.

## The Modern Approach: SVG Favicons

SVG favicons are the most forward-looking option. An SVG is a vector file that scales to any resolution without losing quality. Modern desktop browsers — Chrome, Firefox, and Edge — support SVG favicons. Safari does not yet.

The main advantages of SVG:
- **Resolution independence.** One file looks sharp at every density.
- **Dark mode support.** You can embed a `prefers-color-scheme` media query inside the SVG to switch between light and dark icon versions automatically.
- **Small file size.** An SVG file for a simple icon is often smaller than a multi-resolution ICO.

Declare an SVG favicon like this:

```html
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
```

Because Safari does not support SVG favicons, always include it alongside a fallback ICO:

```html
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="icon" type="image/x-icon" href="/favicon.ico">
```

Browsers that understand SVG will use it. Others fall back to the ICO.

## Putting It All Together: The Complete HTML

Here is a complete, production-ready set of favicon declarations for your `<head>`:

```html
<!-- Standard favicon -->
<link rel="icon" type="image/x-icon" href="/favicon.ico">

<!-- SVG favicon (modern browsers) -->
<link rel="icon" type="image/svg+xml" href="/favicon.svg">

For more on this topic, see [*What Is a Favicon? The Tiny Icon That Does a Big Job*](/blog/what-is-a-favicon).

<!-- PNG fallback -->
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">

<!-- Apple touch icon -->
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">

<!-- Web App Manifest (for Android and PWA) -->
<link rel="manifest" href="/site.webmanifest">
```

Your `favicon.ico` should be a multi-resolution container with 16×16, 32×32, and 48×48 layers inside it. The PNG files are used by browsers that prefer PNG over ICO. The apple-touch-icon covers iOS. The manifest covers Android and PWA contexts.

## Which Sizes Do You Actually Need?

If you want the minimal viable set that covers the vast majority of users:

1. `favicon.ico` — multi-res containing 16×16 and 32×32
2. `apple-touch-icon.png` — 180×180
3. `icon-192x192.png` and `icon-512x512.png` — referenced in your manifest

Add `favicon.svg` if you want dark mode support and future-proofing. Add 152×152 and 120×120 apple-touch-icon variants if you want pixel-perfect iOS coverage.

A good favicon generator produces all of these from a single source image, so you are not manually resizing anything — you just drop in your artwork and download the package.
