---
title: "CSS Gradient Text: How to Apply Gradients to Text"
description: "Learn how to create CSS gradient text using background-clip and -webkit-text-fill-color. Includes browser support, accessibility, and multi-color text examples."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["css", "gradient text", "text gradient", "background-clip", "web design"]
draft: false
---

CSS gradient text uses a layered technique: apply a gradient as a background, clip it to the text shape, and make the text color transparent. The result is text that appears filled with a gradient.

## The technique

```css
.gradient-text {
  background: linear-gradient(90deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
```

Three properties work together:
1. **`background`** — sets the gradient (or any image)
2. **`-webkit-background-clip: text`** — clips the background to the text shape
3. **`-webkit-text-fill-color: transparent`** — makes the text fill transparent so the gradient shows through

The `-webkit-` prefix is required for Safari. Modern Chrome, Firefox, and Edge support the non-prefixed versions but the prefixed versions work everywhere, so include both.

## Basic examples

```css
/* Horizontal gradient */
.gradient-text {
  background: linear-gradient(to right, #f093fb, #f5576c);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Diagonal gradient */
.gradient-text {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Rainbow gradient */
.gradient-text {
  background: linear-gradient(to right, #f00, #ff0, #0f0, #0ff, #00f, #f0f);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Radial gradient on text */
.gradient-text {
  background: radial-gradient(circle, #f093fb, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
```

## Applying to headings

```css
/* Hero heading */
.hero h1 {
  font-size: clamp(2rem, 6vw, 5rem);
  font-weight: 800;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1.1;
}

/* Section heading accent */
.section-title span {
  background: linear-gradient(to right, #f093fb, #f5576c);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
```

## Combining with animation

Since the gradient is a background, you can animate `background-position` using `background-size`:

```css
.animated-gradient-text {
  background: linear-gradient(90deg, #667eea, #764ba2, #f093fb, #667eea);
  background-size: 200% auto;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: gradient-text-shift 3s linear infinite;
}

@keyframes gradient-text-shift {
  0% { background-position: 0% center; }
  100% { background-position: 200% center; }
}
```

## Caveats and limitations

**`text-shadow` doesn't work** — `text-shadow` applies to the text fill color, which is transparent. Use `filter: drop-shadow()` instead:

```css
.gradient-text {
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.3));
}
```

**`color` fallback** — because `-webkit-text-fill-color` overrides `color`, browsers that don't support it still see the `color` property. Set a sensible fallback:

```css
.gradient-text {
  color: #667eea;              /* fallback for unsupported browsers */
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
```

**Inline elements** — `background-clip: text` works on block and inline elements, but you may need to set `display: inline-block` for inline elements to ensure the gradient spans correctly:

```css
.gradient-inline {
  display: inline-block;
  background: linear-gradient(to right, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
```

## Accessibility

Gradient text maintains accessibility as long as the contrast is sufficient. Since the text is rendered as the gradient colors, check contrast at both ends of the gradient:

```css
/* Good contrast: both #667eea and #764ba2 are dark on white backgrounds */
.gradient-text {
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Risky: light yellow (#ffeb3b) on white may fail contrast at that color stop */
```

Use a contrast checker (WebAIM Contrast Checker) for both end stops.

## Browser support

- Chrome, Edge, Opera: supported
- Safari: requires `-webkit-` prefix (still required)
- Firefox: supported since Firefox 49 (non-prefixed)

Always include both `-webkit-background-clip: text` and `background-clip: text`.

Generate gradient CSS at [gradientcss.io](/).
