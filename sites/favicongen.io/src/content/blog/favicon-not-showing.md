---
title: "Favicon Not Showing? Here's How to Fix It"
description: "Favicon not appearing in your browser tab? Walk through the most common causes — browser cache, wrong path, missing tags, HTTPS issues — and how to fix each one."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["favicon", "troubleshooting", "browser cache", "web development"]
draft: false
---

You uploaded your favicon, added the `<link>` tag, deployed your site — and the favicon still is not showing up. Or it was showing up, then it stopped. Or it shows up in Firefox but not Chrome. This is one of those problems that should be simple and yet manages to be frustrating every time.

The good news: the causes are well understood and the fixes are straightforward once you know where to look. Work through these steps in order, starting with the most common cause.

## Step 1: Clear Your Browser Cache (Start Here)

The most common reason a favicon does not show up — by a wide margin — is browser cache. Browsers aggressively cache favicons because they are fetched on every page load and change infrequently. Once a browser has seen your site's favicon (or decided there is no favicon at your URL), it holds onto that information for a long time.

For more on this topic, see [*How to Create a Favicon for Your Website (Quick and Easy)*](/blog/how-to-create-a-favicon).

**Hard refresh the page:**
- Windows/Linux: `Ctrl + Shift + R`
- macOS: `Cmd + Shift + R`

This forces the browser to reload the page and its assets from the server, bypassing the cache for that specific page load.

**If a hard refresh does not work, clear the favicon cache specifically:**

In Chrome:
1. Open DevTools (`F12` or `Ctrl + Shift + I`)
2. Click the Network tab
3. Check the "Disable cache" checkbox
4. Reload the page

Alternatively, go to Chrome's address bar and type `chrome://favicon/` followed by your domain — this sometimes forces a refresh of the stored favicon.

**Test in an incognito/private window:**

A private browsing window starts with a fresh cache every time. Open your site in an incognito tab (Chrome: `Ctrl + Shift + N`, Firefox: `Ctrl + Shift + P`). If your favicon appears there but not in a regular tab, the issue is definitely cache — continue clearing it in your main browser.

For more on this topic, see [*Favicon Sizes: The Complete Size Guide for Every Browser and Device*](/blog/favicon-sizes).

## Step 2: Verify the File Is Actually There

A missing or misplaced file is the second most common cause. Open your browser and navigate directly to the favicon URL:

```
https://yourdomain.com/favicon.ico
```

If you see your icon, the file is being served correctly. If you get a 404 error, the file is not where you think it is.

**Check your deployment:** Many site builders, static site generators, and frameworks have a specific "public" or "static" directory where assets need to live in order to be served at the root of your domain. If your favicon is in the wrong folder in your source code, it will not be accessible at the right URL after deployment.

**Check case sensitivity:** File systems on Linux servers (which most web servers run) are case-sensitive. `Favicon.ico` and `favicon.ico` are different files. Make sure your file name and your `href` attribute use exactly the same casing.

## Step 3: Check Your HTML `<link>` Tag

If the file exists at the correct URL, the next thing to check is whether your HTML is correctly declaring it.

Open your page's source code (right-click anywhere on the page, click "View Page Source") and search for `favicon` or `rel="icon"`.

For more on this topic, see [*What Is a Favicon? The Tiny Icon That Does a Big Job*](/blog/what-is-a-favicon).

The correct tag looks like this:

```html
<link rel="icon" type="image/x-icon" href="/favicon.ico">
```

Common mistakes to look for:

**Missing `rel` attribute:** The `rel="icon"` attribute is how the browser knows this link is a favicon. Without it, the tag is ignored. `rel="shortcut icon"` is an older form that still works but is no longer necessary — `rel="icon"` is the current standard.

**Wrong `type` attribute:** For an ICO file, the MIME type is `image/x-icon`. For a PNG, it is `image/png`. An incorrect type will cause some browsers to reject the file even if the path is right.

**Relative vs. absolute path:** Using `href="/favicon.ico"` (with a leading slash) means the path is relative to the root of your domain. Using `href="favicon.ico"` (no slash) means it is relative to the current page's URL. On a page at `/blog/my-post`, a relative `href="favicon.ico"` resolves to `/blog/favicon.ico`, not `/favicon.ico`. Use the root-relative path with a leading slash.

**Tag in the wrong place:** The `<link>` tag must be inside the `<head>` element, not in `<body>`. Check that your layout template or HTML file is placing it correctly.

## Step 4: Check for HTTPS and Mixed Content Issues

If your site is served over HTTPS (which it should be), all assets — including your favicon — must also be loaded over HTTPS. An HTTP reference to a file on an HTTPS site triggers a mixed content error, and browsers will silently block the request.

Check your `href` attribute: if you have used an absolute URL like `http://yourdomain.com/favicon.ico` (with `http://` not `https://`), change it to use `https://` or use a root-relative path like `/favicon.ico` instead.

You can verify whether the favicon request is being blocked by opening DevTools, going to the Console tab, and looking for any mixed content errors.

## Step 5: Inspect the Network Request in DevTools

DevTools' Network tab is your best diagnostic tool for favicon problems. Here is how to use it:

1. Open DevTools (`F12`)
2. Click the **Network** tab
3. In the filter box, type `favicon` to filter requests to just favicon-related files
4. Reload the page (`F5`)
5. Look at what requests appear and their status codes

**Status 200:** The file was found and served correctly. If you see this but the favicon still does not appear, the problem is likely a format issue — see the next step.

**Status 404:** The file was not found at the requested URL. Fix the path or deploy the file to the correct location.

**Status 301 or 302:** The request is being redirected. Follow the redirect chain to see where it ends up. A redirect loop or a redirect to an error page will prevent the favicon from loading.

**No request at all:** The browser did not attempt to fetch a favicon. This usually means there is no `<link>` tag in your HTML and no `favicon.ico` at the root of your domain. The browser has nothing to request.

## Step 6: Verify the ICO File Format

Not all files named `.ico` are valid ICO files. If you renamed a PNG or JPG file to `.ico` without actually converting it to the ICO format, most browsers will reject it (or display a broken icon) even though the file appears to exist.

To verify your ICO file is valid:
- Redownload it from your server and try opening it in an image viewer — on Windows, File Explorer can preview ICO files natively
- Use the browser's DevTools Network tab (as above) and check the response headers — a valid ICO served correctly will have `Content-Type: image/x-icon` or `image/vnd.microsoft.icon`
- Regenerate it using a favicon generator to ensure the output is a properly structured ICO file

If you used an image editor to save an ICO file, make sure the software actually supports the format and did not just change the extension.

## Step 7: Check Whether the Favicon Shows Up in Different Browsers

Favicon behavior is not identical across browsers. If your favicon shows up in one browser but not another, that helps narrow down the cause:

**Shows in Firefox but not Chrome:** Chrome caches favicons very aggressively. Try the cache-clearing steps from Step 1 specifically in Chrome.

**Shows in Chrome but not Safari:** Safari has historically been pickier about MIME types. Check that your file is served with the correct `Content-Type` header and that you have a valid ICO or PNG at the declared path.

**Shows on desktop but not mobile:** Mobile browsers, especially Safari on iOS, use the apple-touch-icon rather than the standard favicon for home screen shortcuts. Ensure you have an apple-touch-icon declared in your HTML.

## The Most Likely Fixes at a Glance

If you are in a hurry, the issue is almost certainly one of these four things:

1. **Browser cache** — test in incognito first, then hard-refresh
2. **Wrong file path** — navigate to `/favicon.ico` directly in your browser
3. **Missing or malformed `<link>` tag** — view your page source and check
4. **File is not a real ICO** — regenerate it with a favicon generator

Work through these four checks and you will resolve the problem in most cases. The deeper format and server-configuration issues are real but much less common.
