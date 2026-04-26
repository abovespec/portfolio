---
title: "How to Reduce Image File Size for the Web (Without Ruining Quality)"
description: "A step-by-step guide to reducing image file sizes for web performance. Covers format choice, resizing, compression, EXIF removal, and modern formats like WebP and AVIF."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["web performance", "compression", "tutorial", "core web vitals", "optimization"]
draft: false
---

Images are almost always the largest assets on a web page, and they are almost always the easiest ones to fix. Unlike JavaScript bundles or third-party scripts, you can often cut your image weight in half with a few straightforward steps and no change to how your page looks. This guide walks through each step in order, because the order matters — you get the best results by working through them systematically rather than jumping straight to compression.

## Why image size matters for the web

A slow-loading image is not just an annoyance. Google's Core Web Vitals include Largest Contentful Paint (LCP), which measures how quickly the biggest visual element on the page becomes visible. For most pages, that element is a hero image, a product photo, or a banner. A heavy image pushes LCP past the three-second threshold that Google considers "poor," which affects both your search ranking and your visitors' willingness to stay.

Beyond LCP, every kilobyte you serve costs the visitor bandwidth. On mobile connections — which represent more than half of web traffic globally — a 3 MB hero image can mean a multi-second wait before anything useful loads. Users on metered connections pay for that bandwidth directly. Getting your images lean is one of the most impactful things you can do for real-world page performance.

## Step 1: Choose the right format first

Before you compress anything, make sure you are using the right format. This one decision often matters more than any compression setting you pick afterward.

The short version: JPG for photographs, PNG for graphics with hard edges or transparency, WebP for either when you want the best size-to-quality ratio and your audience is on modern browsers. If you are not sure where to start, the [format comparison guide](/blog/jpg-vs-png-vs-webp) covers this in detail.

The practical impact of a wrong format choice can be enormous. A photograph saved as PNG instead of JPG might be four times the file size with zero visible quality improvement. A logo saved as JPG instead of PNG will be smaller but covered in ringing artifacts around the edges. Format first, compression second.

## Step 2: Resize to the actual display dimensions

The single most common cause of oversized web images is serving a photo at full camera resolution when the page only displays it at a fraction of that size. Your phone camera probably produces images that are 4000 pixels wide or larger. If your blog article column is 800 pixels wide, you are making every visitor download roughly 25 times more pixels than they can see, and their browser is silently resizing it on arrival.

Before you compress, figure out the largest size the image will actually be displayed. Then resize the image to that size, or perhaps 2x that size if you want to look sharp on high-density (Retina) screens. A 1600-pixel wide JPG of a photo at a decent quality setting will almost always be smaller than the same photo at 4000 pixels even at a higher quality setting.

Resizing is not the same as compressing, and it does not reduce quality in the way compression does — it just removes pixels you were not using.

## Step 3: Compress the result

Now you are ready to compress. The key decision here is lossy versus lossless compression.

Lossless compression reorganizes the file data without touching the pixels. The output is identical to the input. PNG only does lossless. The savings depend heavily on what is in the image — flat-color graphics can shrink dramatically, photographs barely at all.

Lossy compression, which is what JPG and WebP use, actually discards image detail. The encoder decides which pixel information is least likely to be noticed and throws it away. The "quality" setting controls how aggressively it does this.

For JPG, a quality setting of 80 to 85 is usually the sweet spot for web images. At quality 85, most photos are visually indistinguishable from quality 95, but noticeably smaller. Going below 80 starts to introduce visible artifacts on detailed areas like foliage, hair, and fabric. Going above 90 produces diminishing returns in quality with rapidly increasing file sizes. You do not need quality 100 for the web; that setting is for archival originals, not served assets.

If you need to hit a specific file size ceiling — say, an upload portal that will only accept images under 500 KB — a tool like the [image compressor at makepicsmall.com](/) can binary-search for the highest quality setting that keeps the file under your target, rather than forcing you to guess manually.

## Step 4: Strip EXIF metadata

EXIF is the block of metadata baked into most photos by the device that took them. It contains the camera model, exposure settings, date and time, and often GPS coordinates of where the photo was taken. None of this is useful to a web browser rendering a product photo or a blog illustration, but it adds weight to the file — anywhere from a few kilobytes to over 100 KB on some camera systems.

More importantly, EXIF that includes GPS data is a privacy concern. If you are publishing photos of people, or photos taken at a private location, stripping EXIF before upload removes geolocation data you probably do not want embedded in publicly accessible files.

Most compression tools strip EXIF as part of the encoding pass. If yours does not, it is worth checking whether the tool has an explicit option to remove metadata.

## Step 5: Consider modern formats

If you went through the steps above using JPG or PNG and your results are still heavier than you would like, WebP is worth trying. At equivalent visual quality, WebP typically produces files 25 to 35 percent smaller than JPG. For a site serving a lot of images, that translates directly into faster page loads.

WebP works in all modern browsers. The practical complication is tooling: your CMS needs to accept WebP uploads, your CDN needs to serve them with the right content type, and if you want older browser fallbacks, you need a `<picture>` element with a JPG fallback. Most modern web frameworks handle this automatically. If you are on a framework like Astro or Next.js, the built-in image components will handle format conversion and resizing for you at build time or on demand.

AVIF is the next step after WebP — even smaller files, better quality handling, but slower to encode and still maturing in terms of tooling support. It is worth watching, especially for build-time image pipelines.

## The "good enough" principle

Optimization for the web does not mean producing the smallest possible file. It means producing a file that is small enough to load quickly without looking noticeably worse.

In practice, this usually means targeting something in the range of 100 to 300 KB for a full-width hero image, 50 to 150 KB for a blog article image, and under 50 KB for thumbnails. Those are rough targets, not laws — a very complex photographic image might need more, and a simple illustration might need far less. The right test is: does it look good, and does it load fast enough that a visitor on a mid-tier mobile connection does not bounce before they see it?

Tools like Lighthouse (built into Chrome DevTools) will flag images that fail the threshold and tell you how much you could save, which is a faster way to prioritize than auditing everything by hand.

## A practical checklist

When you add or update images on a site, run through this list:

1. Is this the right format for the content type?
2. Is the image resized to no more than 2x its display dimensions?
3. Is it compressed — quality 80-85 for JPG, lossless optimization for PNG?
4. Is EXIF metadata stripped?
5. Is WebP or AVIF available for modern browsers?

That covers 95 percent of what matters. The remaining 5 percent — things like responsive images with `srcset`, image CDNs, lazy loading — are worth knowing about, but they build on the foundation these five steps provide.

If you need to compress an image right now without installing anything, [makepicsmall.com](/) runs the compression in your browser. No upload, no account, no waiting. Drag the file in and download the result.
