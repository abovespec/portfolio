---
title: "CSS Gradient Background: Full-Page, Section, and Hero Techniques"
description: "Create stunning CSS gradient backgrounds for full pages, hero sections, cards, and UI components. Includes multi-layer gradients, image overlays, and Tailwind examples."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["css", "gradient background", "background", "hero", "web design"]
draft: false
---

Gradient backgrounds are one of the most effective tools in modern web design. This guide covers practical patterns for full-page backgrounds, hero sections, cards, and multi-layer effects.

## Full-page gradient

```css
/* Simple two-color full-page background */
body {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* Subtle light gradient */
body {
  min-height: 100vh;
  background: linear-gradient(to bottom right, #f8fafc, #e2e8f0);
}

/* Dark mode gradient */
body {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
}
```

## Hero section gradient

```css
/* Diagonal hero gradient */
.hero {
  min-height: 80vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Hero with radial glow */
.hero {
  min-height: 80vh;
  background:
    radial-gradient(ellipse at top, rgba(102, 126, 234, 0.3), transparent 50%),
    #0f172a;
}

/* Three-color hero gradient */
.hero {
  background: linear-gradient(135deg,
    #f093fb 0%,
    #f5576c 50%,
    #764ba2 100%
  );
}
```

## Image + gradient overlay

```css
/* Dark overlay at the bottom (for text readability) */
.hero-image {
  background-image:
    linear-gradient(to top, rgba(0,0,0,0.7) 0%, rgba(0,0,0,0) 50%),
    url('/hero.jpg');
  background-size: cover;
  background-position: center;
  min-height: 70vh;
}

/* Full dark overlay with color tint */
.hero-image {
  background-image:
    linear-gradient(to bottom, rgba(102,126,234,0.5), rgba(118,75,162,0.5)),
    url('/hero.jpg');
  background-size: cover;
  background-position: center;
}

/* Gradient only on the left half (for split layout) */
.split-hero {
  background-image:
    linear-gradient(to right, rgba(102,126,234,0.9) 50%, transparent 50%),
    url('/hero.jpg');
  background-size: cover;
}
```

## Section dividers and transitions

```css
/* Section with gradient background */
.feature-section {
  background: linear-gradient(to bottom, #f8fafc, #e2e8f0);
  padding: 80px 0;
}

/* Flowing transition between sections */
.section-top {
  background: linear-gradient(to bottom, #667eea, #764ba2);
}

.section-bottom {
  background: linear-gradient(to bottom, #764ba2, #0f172a);
}

/* SVG wave divider alternative: use a pseudo-element with gradient */
.section-wave::after {
  content: '';
  display: block;
  height: 80px;
  background: linear-gradient(to bottom right, #667eea 50%, #f8fafc 50%);
}
```

## Card backgrounds

```css
/* Light card with subtle gradient */
.card {
  background: linear-gradient(to bottom right, #ffffff, #f1f5f9);
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

/* Dark card with gradient */
.card-dark {
  background: linear-gradient(135deg, #1e293b, #334155);
  border-radius: 12px;
  padding: 24px;
  color: white;
}

/* Colorful card with gradient border effect */
.card-gradient-border {
  background: white;
  border-radius: 12px;
  padding: 2px;
  background-image: linear-gradient(135deg, #667eea, #764ba2);
}

.card-gradient-border-inner {
  background: white;
  border-radius: 10px;
  padding: 22px;
}
```

## Using background-size and background-position

```css
/* Gradient stripe as repeating background */
.stripes {
  background: repeating-linear-gradient(
    45deg,
    #f8fafc,
    #f8fafc 10px,
    #e2e8f0 10px,
    #e2e8f0 20px
  );
}

/* Moving gradient (large background, shift with transform) */
.animated-bg {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
  background-size: 200% 200%;
  animation: gradientShift 6s ease infinite;
}

@keyframes gradientShift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
```

## Tailwind CSS gradient backgrounds

```html
<!-- Simple gradient to right -->
<div class="min-h-screen bg-gradient-to-r from-indigo-500 to-purple-700"></div>

<!-- Diagonal hero gradient -->
<div class="min-h-screen bg-gradient-to-br from-purple-600 to-pink-500"></div>

<!-- Dark gradient -->
<div class="min-h-screen bg-gradient-to-br from-gray-900 to-indigo-950"></div>

<!-- Three-stop gradient -->
<div class="bg-gradient-to-r from-purple-500 via-pink-500 to-red-500"></div>

<!-- Hero with opacity overlay using arbitrary values -->
<div class="bg-[linear-gradient(135deg,#667eea_0%,#764ba2_100%)]"></div>
```

Generate gradient CSS at [gradientcss.io](/).
