---
title: "CSS Gradient Animation: Moving and Shifting Gradient Backgrounds"
description: "Animate CSS gradients using background-position, background-size, and CSS custom properties. Includes moving gradients, color shift animations, and performance tips."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["css", "gradient animation", "animation", "background", "web design"]
draft: false
---

CSS doesn't support animating gradient values directly — `gradient-color-stop` isn't an animatable property. But you can create convincing gradient animations using two techniques: animating `background-position` on a large gradient, or using CSS custom properties with JavaScript.

## Technique 1: animate background-position

Create a gradient wider than the element, then shift the position:

```css
.animated-bg {
  background: linear-gradient(135deg,
    #667eea 0%,
    #764ba2 25%,
    #f093fb 50%,
    #764ba2 75%,
    #667eea 100%
  );
  background-size: 300% 300%;
  animation: gradient-shift 6s ease infinite;
}

@keyframes gradient-shift {
  0%   { background-position: 0% 50%; }
  50%  { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
```

For more on this topic, see [*CSS Gradient Background: Full-Page, Section, and Hero Techniques*](/blog/css-gradient-background).

**How it works:** The gradient is 300% wide. `background-position` shifts from left to right and back, creating a looping color transition.

## Aurora / mesh gradient effect

```css
.aurora {
  background:
    radial-gradient(ellipse at 20% 50%, rgba(102, 126, 234, 0.4), transparent 50%),
    radial-gradient(ellipse at 80% 20%, rgba(118, 75, 162, 0.4), transparent 50%),
    radial-gradient(ellipse at 60% 80%, rgba(240, 147, 251, 0.3), transparent 50%),
    #0f172a;
  background-size: 200% 200%, 200% 200%, 200% 200%, 100% 100%;
  animation: aurora 12s ease infinite;
}

@keyframes aurora {
  0%   { background-position: 0% 0%, 100% 0%, 50% 100%, 0% 0%; }
  33%  { background-position: 100% 50%, 0% 100%, 100% 0%, 0% 0%; }
  66%  { background-position: 50% 100%, 50% 0%, 0% 50%, 0% 0%; }
  100% { background-position: 0% 0%, 100% 0%, 50% 100%, 0% 0%; }
}
```

## Scrolling gradient stripe

```css
.stripe-scroll {
  background: repeating-linear-gradient(
    45deg,
    #667eea,
    #667eea 10px,
    #764ba2 10px,
    #764ba2 20px
  );
  background-size: 200% 200%;
  animation: stripe-move 2s linear infinite;
}

@keyframes stripe-move {
  0%   { background-position: 0 0; }
  100% { background-position: 40px 0; }
}
```

## Gradient transition on hover

Instead of animating continuously, trigger on hover using `transition`. Because gradients aren't directly animatable, use `opacity` between two layered elements:

```css
.btn {
  position: relative;
  background: linear-gradient(to right, #667eea, #764ba2);
  padding: 12px 28px;
  border-radius: 8px;
  color: white;
  border: none;
  cursor: pointer;
  isolation: isolate;
}

.btn::after {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: 8px;
  background: linear-gradient(to right, #764ba2, #f093fb);
  opacity: 0;
  transition: opacity 0.4s ease;
  z-index: -1;
}

.btn:hover::after {
  opacity: 1;
}
```

## Animate with CSS custom properties (+ JS)

CSS custom properties are animatable. Define color stops as variables and tween them with JavaScript:

For more on this topic, see [*CSS linear-gradient: Syntax, Direction, Color Stops, and Examples*](/blog/linear-gradient-css).

For more on this topic, see [*CSS radial-gradient: Circles, Ellipses, and Spotlight Effects*](/blog/radial-gradient-css).

```css
.dynamic-gradient {
  --color-start: #667eea;
  --color-end: #764ba2;
  background: linear-gradient(135deg, var(--color-start), var(--color-end));
  transition: --color-start 0.5s, --color-end 0.5s;
}
```

```javascript
const el = document.querySelector('.dynamic-gradient');

el.addEventListener('mouseenter', () => {
  el.style.setProperty('--color-start', '#f093fb');
  el.style.setProperty('--color-end', '#f5576c');
});

el.addEventListener('mouseleave', () => {
  el.style.setProperty('--color-start', '#667eea');
  el.style.setProperty('--color-end', '#764ba2');
});
```

Note: custom property transitions require the browser to interpolate the color value. This works in Chrome and Safari but check Firefox support for your use case.

## Full-page animated background

```css
body {
  min-height: 100vh;
  background: linear-gradient(-45deg,
    #ee7752,
    #e73c7e,
    #23a6d5,
    #23d5ab
  );
  background-size: 400% 400%;
  animation: gradient 12s ease infinite;
}

@keyframes gradient {
  0%   { background-position: 0% 50%; }
  50%  { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
```

## Performance tips

**Use `will-change` sparingly** — it hints to the browser to composite the element:

```css
.animated-bg {
  will-change: background-position;
}
```

Remove `will-change` after the animation completes to free GPU memory.

**Prefer compositing** — `background-position` animation triggers layout in older browsers. Prefer `transform` when possible. For gradient shifts that must animate, `background-position` is currently the most compatible option.

**Reduce motion** — respect users who prefer less motion:

```css
@media (prefers-reduced-motion: reduce) {
  .animated-bg {
    animation: none;
    background-position: 0% 50%;
  }
}
```

Generate gradient CSS at [gradientcss.io](/).
