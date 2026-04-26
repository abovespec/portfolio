---
title: "CSS radial-gradient: Circles, Ellipses, and Spotlight Effects"
description: "Learn CSS radial-gradient syntax for circles, ellipses, color stops, and custom centers. Includes spotlight effects, background dots, and glow examples."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["css", "radial-gradient", "gradient", "web design", "background"]
draft: false
---

`radial-gradient()` creates gradients that radiate outward from a center point. The shape can be a circle or an ellipse. This guide covers the full syntax with practical design examples.

## Basic syntax

```css
background: radial-gradient(shape size at position, color-stop-1, color-stop-2, ...);
```

All parameters except the color stops are optional.

## Shape: circle vs. ellipse

```css
/* Default: ellipse (fills the element) */
background: radial-gradient(#667eea, #764ba2);

/* Circle: equal radius in all directions */
background: radial-gradient(circle, #667eea, #764ba2);

/* Explicit ellipse */
background: radial-gradient(ellipse, #667eea, #764ba2);
```

Use `circle` for spotlights and radial highlights. Use `ellipse` (default) when you want the gradient to match the element's shape.

## Position: center point

```css
/* Default: center center */
background: radial-gradient(circle, #667eea, #764ba2);
background: radial-gradient(circle at center, #667eea, #764ba2);

/* Custom positions */
background: radial-gradient(circle at top, #667eea, #764ba2);
background: radial-gradient(circle at bottom right, #667eea, #764ba2);
background: radial-gradient(circle at 20% 80%, #667eea, #764ba2);
background: radial-gradient(circle at 100px 50px, #667eea, #764ba2);
```

## Size keywords

```css
/* closest-side: gradient edge reaches the nearest side */
background: radial-gradient(circle closest-side at 20% 50%, #667eea, #764ba2);

/* farthest-side: gradient edge reaches the farthest side */
background: radial-gradient(circle farthest-side at 20% 50%, #667eea, #764ba2);

/* closest-corner */
background: radial-gradient(circle closest-corner at 30% 50%, #667eea, #764ba2);

/* farthest-corner (default for both shapes) */
background: radial-gradient(circle farthest-corner at 30% 50%, #667eea, #764ba2);
```

## Explicit size

```css
/* Circle with fixed radius */
background: radial-gradient(circle 100px, #667eea, #764ba2);

/* Ellipse with width and height */
background: radial-gradient(ellipse 200px 100px at center, #667eea, #764ba2);

/* Ellipse as percentages */
background: radial-gradient(ellipse 80% 60% at center, #667eea, #764ba2);
```

## Color stops

```css
/* Two colors */
background: radial-gradient(circle, #667eea, #764ba2);

/* Three colors */
background: radial-gradient(circle, #f00, #ff0, #0f0);

/* With explicit positions */
background: radial-gradient(circle,
  #667eea 0%,
  #9ca3af 50%,
  #764ba2 100%
);

/* Hard stop (concentric rings) */
background: radial-gradient(circle,
  #667eea 40%,
  #764ba2 40%
);
```

## Transparency

```css
/* Glow effect: color at center fades to transparent */
background: radial-gradient(circle, rgba(102, 126, 234, 0.6), transparent);

/* Dark corners vignette */
background: radial-gradient(ellipse at center, transparent 50%, rgba(0,0,0,0.5) 100%);

/* Spotlight on a dark background */
.spotlight {
  background:
    radial-gradient(circle at 50% 30%, rgba(255,255,255,0.15), transparent 50%),
    #1a1a2e;
}
```

## Repeating radial gradients

```css
/* Concentric rings */
background: repeating-radial-gradient(
  circle,
  #667eea 0px,
  #667eea 10px,
  transparent 10px,
  transparent 20px
);

/* Target/bullseye pattern */
background: repeating-radial-gradient(
  circle,
  #f00 0,
  #f00 10px,
  #fff 10px,
  #fff 20px
);
```

## Real examples

**Background with glowing orb:**

```css
.hero {
  background:
    radial-gradient(circle at 70% 30%, rgba(102, 126, 234, 0.4) 0%, transparent 50%),
    radial-gradient(circle at 20% 80%, rgba(118, 75, 162, 0.3) 0%, transparent 40%),
    #0f0f23;
}
```

**Vignette effect over an image:**

```css
.photo-container {
  position: relative;
}

.photo-container::after {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse at center, transparent 40%, rgba(0,0,0,0.7) 100%);
}
```

**Polka dot background:**

```css
.dots {
  background-color: #f0f4f8;
  background-image: radial-gradient(circle, #94a3b8 1px, transparent 1px);
  background-size: 24px 24px;
}
```

**Spotlight button hover:**

```css
.btn {
  position: relative;
  overflow: hidden;
  background: #1e293b;
  color: white;
  padding: 12px 28px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
}

.btn::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  background: radial-gradient(circle, rgba(255,255,255,0.2), transparent 70%);
  transform: translate(-50%, -50%);
  transition: width 0.4s ease, height 0.4s ease;
}

.btn:hover::before {
  width: 300px;
  height: 300px;
}
```

Generate radial gradient CSS at [gradientcss.io](/).
