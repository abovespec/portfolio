---
title: "CSS linear-gradient: Syntax, Direction, Color Stops, and Examples"
description: "Master CSS linear-gradient with syntax breakdowns, direction keywords, degree angles, color stops, hard stops, and real design examples including backgrounds and buttons."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["css", "linear-gradient", "gradient", "web design", "background"]
draft: false
---

`linear-gradient()` is the most-used CSS gradient function. It creates a smooth transition between colors along a straight line. This guide covers the full syntax with practical examples.

## Basic syntax

```css
background: linear-gradient(direction, color-stop-1, color-stop-2, ...);
```

The direction is optional (defaults to top-to-bottom). You need at least two color stops.

## Direction: keywords

```css
/* Top to bottom (default when direction is omitted) */
background: linear-gradient(#667eea, #764ba2);
background: linear-gradient(to bottom, #667eea, #764ba2);

/* Bottom to top */
background: linear-gradient(to top, #667eea, #764ba2);

/* Left to right */
background: linear-gradient(to right, #667eea, #764ba2);

/* Right to left */
background: linear-gradient(to left, #667eea, #764ba2);

/* Diagonal */
background: linear-gradient(to bottom right, #667eea, #764ba2);
background: linear-gradient(to top left, #667eea, #764ba2);
background: linear-gradient(to bottom left, #667eea, #764ba2);
background: linear-gradient(to top right, #667eea, #764ba2);
```

## Direction: degree angles

```css
/* 0deg = to top */
background: linear-gradient(0deg, #667eea, #764ba2);

/* 90deg = to right */
background: linear-gradient(90deg, #667eea, #764ba2);

/* 180deg = to bottom */
background: linear-gradient(180deg, #667eea, #764ba2);

/* 270deg = to left */
background: linear-gradient(270deg, #667eea, #764ba2);

/* 45deg = top-left to bottom-right */
background: linear-gradient(45deg, #667eea, #764ba2);

/* 135deg = top-right to bottom-left */
background: linear-gradient(135deg, #667eea, #764ba2);
```

Angles increase clockwise from "to top". So 45° points toward the top-right corner.

## Color stops

```css
/* Two colors — evenly distributed */
background: linear-gradient(to right, #f093fb, #f5576c);

/* Three or more colors — evenly distributed */
background: linear-gradient(to right, #f00, #ff0, #0f0, #00f);

/* Custom stop positions (percentages) */
background: linear-gradient(to right,
  #f093fb 0%,
  #f5576c 50%,
  #764ba2 100%
);

/* Custom stop positions (pixel values) */
background: linear-gradient(to right,
  #f093fb 0px,
  #f5576c 200px,
  #764ba2 400px
);

/* Mix of units */
background: linear-gradient(to right,
  #f093fb 0%,
  #f5576c 200px,
  #764ba2 100%
);
```

## Hard stops (no transition)

When two stops share the same position, the color changes abruptly:

```css
/* Vertical stripe: 50% blue, 50% red */
background: linear-gradient(to right,
  #667eea 50%,
  #f5576c 50%
);

/* Three stripes */
background: linear-gradient(to right,
  #f00 0% 33.33%,
  #0f0 33.33% 66.66%,
  #00f 66.66% 100%
);

/* Diagonal stripes (45 degrees) */
background: linear-gradient(45deg,
  #667eea 25%,
  transparent 25%,
  transparent 50%,
  #667eea 50%,
  #667eea 75%,
  transparent 75%
);
background-size: 40px 40px;
```

## Real examples

**Full-page gradient background:**

```css
body {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

**Subtle card background:**

```css
.card {
  background: linear-gradient(to bottom right, #f8fafc, #e2e8f0);
  border-radius: 12px;
  padding: 24px;
}
```

**Gradient button:**

```css
.btn-gradient {
  background: linear-gradient(to right, #f093fb, #f5576c);
  border: none;
  color: white;
  padding: 12px 24px;
  border-radius: 8px;
  cursor: pointer;
  transition: opacity 0.2s;
}

.btn-gradient:hover {
  opacity: 0.9;
}
```

**Image overlay — dark gradient at bottom:**

```css
.hero {
  position: relative;
}

.hero::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(
    to top,
    rgba(0, 0, 0, 0.7) 0%,
    rgba(0, 0, 0, 0) 50%
  );
}
```

For more on this topic, see [*CSS Gradient Background: Full-Page, Section, and Hero Techniques*](/blog/css-gradient-background).

**Fade out edge (for text overflow):**

```css
.fade-right {
  -webkit-mask-image: linear-gradient(to right, black 80%, transparent 100%);
  mask-image: linear-gradient(to right, black 80%, transparent 100%);
}
```

**Navbar with subtle gradient:**

```css
nav {
  background: linear-gradient(to bottom, rgba(0,0,0,0.15), transparent);
  padding: 16px 24px;
}
```

## Using with CSS custom properties

```css
:root {
  --gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  --gradient-accent: linear-gradient(to right, #f093fb, #f5576c);
}

.hero {
  background: var(--gradient-primary);
}

.cta {
  background: var(--gradient-accent);
}
```

## Tailwind CSS equivalent

```html
<!-- to right gradient -->
<div class="bg-gradient-to-r from-purple-500 to-pink-500"></div>

<!-- diagonal gradient -->
<div class="bg-gradient-to-br from-indigo-500 to-purple-700"></div>

<!-- with via color stop -->
<div class="bg-gradient-to-r from-purple-500 via-pink-500 to-red-500"></div>
```

Generate linear gradient CSS at [gradientcss.io](/).


For more on this topic, see [*CSS radial-gradient: Circles, Ellipses, and Spotlight Effects*](/blog/radial-gradient-css).

For more on this topic, see [*CSS Gradient Animation: Moving and Shifting Gradient Backgrounds*](/blog/css-gradient-animation).