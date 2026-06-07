---
title: "How to Create a Favicon for Your Website (Quick and Easy)"
description: "Learn how to create a favicon from scratch or from your logo — including design tips, format choices, and exactly how to add it to your website's HTML."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["favicon", "how to", "web design", "favicon generator"]
draft: false
---

Creating a favicon sounds like a small task, and it is — but it trips up a lot of people because it sits at the intersection of image design, file formats, and HTML. This guide walks you through the whole process from start to finish: picking or creating your source artwork, preparing it correctly, generating the right files, and adding them to your site.

## Step 1: Start With the Right Source Image

Your favicon starts with a piece of artwork. You have two options: use an existing logo or brand mark, or create something new specifically for use as a favicon.

### Using Your Logo

If you already have a logo, it probably works as a starting point — but not necessarily in its full form. Most logos are designed to be read at larger sizes and include fine details, wordmarks, or multiple elements that will disappear or blur at 16×16 pixels.

Look at your logo and ask: what element makes it distinctive? For most brands, that is one of these:
- A single initial or monogram
- A simple icon or symbol from the logo
- A distinctive geometric shape

That element is what your favicon should show. A favicon is not a shrunk-down version of your full logo — it is a representative glyph that stands in for your brand at a tiny scale.

For more on this topic, see [*What Is a Favicon? The Tiny Icon That Does a Big Job*](/blog/what-is-a-favicon).

### Creating Something New

If you do not have an existing logo, or if your logo does not translate well to square-and-small, you can design a favicon directly. You do not need sophisticated software — a simple design in any vector tool, or even a carefully chosen emoji converted to an image, can produce an effective favicon.

Whatever approach you take, work in square format. Favicons are always displayed in a square container, so a 1:1 aspect ratio source image is essential. If your artwork is wider than it is tall, you will end up with letterboxing (padding on top and bottom) that makes the icon look small and awkward inside the tab.

## Step 2: Design for Small Sizes

This is where most favicon designs go wrong. Something that looks great at 512×512 can become an unreadable smudge at 16×16. A few principles will help:

### Keep It Simple

Every line, curve, and detail in your design is competing for a tiny number of pixels. At 16×16, you have 256 pixels total to work with. An image that looks clean at full size will look like noise at that resolution. Strip away everything that is not essential to recognition.

Geometric shapes — circles, squares, triangles, bold letterforms — survive the scaling process far better than illustrations, thin lines, or photography.

### Use Strong Contrast

Your favicon will appear against both light and dark browser chrome (the UI surrounding the browser's content area). An icon that relies on subtle color differences or low-contrast details will disappear in some contexts. Aim for strong contrast between your icon's foreground and its background.

Consider what the icon looks like on both a white and a dark gray background before you finalize it.

### Avoid Thin Lines

Lines that look elegant at full resolution become intermittent or disappear entirely at small sizes due to antialiasing and rounding. If your design uses thin strokes, make them heavier before generating your favicon.

### Test at Actual Size

Before you generate anything, look at your artwork at 32×32 and 16×16 pixels. Most image editors and design tools let you zoom out — the goal is to see exactly what you will get, not how your design looks when zoomed in. If it reads clearly at those sizes, you are ready.

## Step 3: Prepare Your File

For best results, provide your favicon generator with a PNG file. Specifically:

- **Format:** PNG
- **Dimensions:** At least 512×512 pixels (larger is fine; the generator will scale it down)
- **Background:** Either a solid color or transparent — whichever suits your design
- **Color space:** sRGB

If your source is an SVG, many favicon generators can accept it directly and will produce better results because they can render the vector at exactly the target resolution rather than scaling a raster image.

Avoid using a JPEG as your source. JPEG compression introduces artifacts that look fine at large sizes but become visible and distracting at small ones. PNG or SVG are the right choices.

## Step 4: Generate Your Favicon Files

A favicon generator takes your source image and produces all the files you need: a multi-resolution ICO, PNG files at standard sizes, and apple-touch-icon variants. Using a generator is the right approach here — manually resizing and saving individual files, and then packaging an ICO container, is tedious and error-prone.

For more on this topic, see [*Favicon ICO vs PNG: Which Format Should You Use?*](/blog/favicon-ico-vs-png).

Upload your prepared source image, let the generator process it, and download the resulting package. You should expect to get:

- `favicon.ico` — a multi-resolution file containing 16×16, 32×32, and 48×48 layers
- `favicon-16x16.png` and `favicon-32x32.png` — PNG equivalents for browsers that prefer them
- `apple-touch-icon.png` — 180×180 PNG for iOS home screen
- `icon-192x192.png` and `icon-512x512.png` — for Android and PWA use
- `site.webmanifest` — the web app manifest file that references the Android icons

Some generators also produce an SVG favicon, which is worth having for dark mode support and future-proofing.

## Step 5: Add the Files to Your Site

Place the generated files in your website's root directory (the same level as your `index.html`). Putting them in the root is the conventional location, and `favicon.ico` specifically is often requested directly from the root by browsers even without an explicit HTML declaration.

If your setup requires a different location — for example, if you are working with a framework that has a public or static assets folder — you can place them there and use explicit paths in your HTML.

## Step 6: Add the HTML Tags

Add these lines inside the `<head>` section of your HTML. If you are using a CMS, framework, or site builder, this goes in the section of your theme or layout template where other head metadata lives:

```html
<link rel="icon" type="image/x-icon" href="/favicon.ico">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
```

Browsers read these tags and choose the best match for their context. The `sizes` attribute helps the browser pick the right resolution.

## Step 7: Test in Multiple Browsers

After deploying, verify that your favicon appears correctly:

**Chrome:** Open your site in a new tab. The favicon should appear immediately. If it does not, do a hard refresh (Ctrl+Shift+R on Windows/Linux, Cmd+Shift+R on macOS).

**Firefox:** Same as Chrome — the favicon should appear in the tab.

**Safari on iOS:** Open your site on an iPhone, then use the Share menu to tap "Add to Home Screen." The resulting home screen icon should use your apple-touch-icon.

**Incognito/Private mode:** Testing in a private window bypasses any cached favicon, so if you recently changed your favicon, this is the fastest way to see the new version.

If your favicon is not appearing, the most common causes are a browser cache issue, a wrong file path, or a missing `<link>` tag in your HTML. The troubleshooting guide on this site covers all of those scenarios in detail.

For more on this topic, see [*Favicon Sizes: The Complete Size Guide for Every Browser and Device*](/blog/favicon-sizes).

## The Short Version

1. Prepare a square PNG or SVG, at least 512×512 pixels, using a simple high-contrast design
2. Run it through a favicon generator
3. Place the output files in your site's root directory
4. Add the `<link>` tags to your `<head>`
5. Test in Chrome, Firefox, and on iOS

That is the whole process. It takes about ten minutes once you have your source artwork ready.
