---
title: "CSS Flexbox Tutorial: Build Real Layouts from Scratch"
description: "A hands-on CSS Flexbox tutorial building three practical layouts: a navigation bar, a card grid, and a vertically-centered hero section. Full code included."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["flexbox", "css", "tutorial", "layout"]
draft: false
---

The fastest way to get comfortable with Flexbox is to build real things with it. Reading property tables only gets you so far — the concepts click when you see why each declaration makes the layout work the way it does.

This tutorial builds three layouts you'll encounter constantly in real projects: a navigation bar, a responsive card grid, and a vertically-centered hero section. Each one introduces a few new Flexbox properties with an explanation of exactly what they're doing.

## Prerequisites

You need a basic HTML file. The structure we'll work with looks like this:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link rel="stylesheet" href="style.css" />
  <title>Flexbox Practice</title>
</head>
<body>
  <!-- layouts go here -->
</body>
</html>
```

All CSS goes in `style.css`. Paste each layout's HTML and CSS as you work through it.

---

## Layout 1: A Navigation Bar

A navigation bar has a logo on the left, links in the middle or right, and sometimes a call-to-action button. The items need to be aligned horizontally and vertically centered within the bar's height.

### The HTML

```html
<nav class="navbar">
  <a href="/" class="navbar__logo">MySite</a>
  <ul class="navbar__links">
    <li><a href="/features">Features</a></li>
    <li><a href="/pricing">Pricing</a></li>
    <li><a href="/docs">Docs</a></li>
  </ul>
  <a href="/signup" class="navbar__cta">Get Started</a>
</nav>
```

### The CSS

```css
/* Reset default list styles */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 2rem;
  height: 64px;
  background-color: #1a1a2e;
  color: #ffffff;
}

.navbar__logo {
  font-size: 1.25rem;
  font-weight: 700;
  color: #ffffff;
  text-decoration: none;
}

.navbar__links {
  display: flex;
  gap: 2rem;
  list-style: none;
}

.navbar__links a {
  color: #cccccc;
  text-decoration: none;
  font-size: 0.9rem;
}

.navbar__cta {
  background-color: #e94560;
  color: #ffffff;
  padding: 0.5rem 1.25rem;
  border-radius: 4px;
  text-decoration: none;
  font-size: 0.9rem;
}
```

### Why it works

`justify-content: space-between` on the `.navbar` pushes the three children (logo, links, CTA) to the edges with space between them. `align-items: center` vertically centers all three within the 64px height.

The `navbar__links` is itself a flex container, which lines the list items up in a row with `gap: 2rem` between them. That `gap` property is far cleaner than applying `margin` to individual items.

---

## Layout 2: A Responsive Card Grid

A row of cards where each card has an image, title, and description. Cards should be equal height, wrap to new lines on smaller screens, and grow to fill available space.

### The HTML

```html
<section class="card-grid">
  <article class="card">
    <img class="card__image" src="https://picsum.photos/seed/a/400/200" alt="" />
    <div class="card__body">
      <h2 class="card__title">Card Title One</h2>
      <p class="card__text">A short description about this card's content goes right here.</p>
    </div>
    <a href="#" class="card__link">Read more</a>
  </article>

  <article class="card">
    <img class="card__image" src="https://picsum.photos/seed/b/400/200" alt="" />
    <div class="card__body">
      <h2 class="card__title">Card Title Two</h2>
      <p class="card__text">Another description here, which happens to be a bit longer than the first one.</p>
    </div>
    <a href="#" class="card__link">Read more</a>
  </article>

  <article class="card">
    <img class="card__image" src="https://picsum.photos/seed/c/400/200" alt="" />
    <div class="card__body">
      <h2 class="card__title">Card Title Three</h2>
      <p class="card__text">Short text.</p>
    </div>
    <a href="#" class="card__link">Read more</a>
  </article>
</section>
```

### The CSS

```css
.card-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  padding: 2rem;
}

.card {
  display: flex;
  flex-direction: column;
  flex: 1 1 280px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
  background: #ffffff;
}

.card__image {
  width: 100%;
  height: 180px;
  object-fit: cover;
}

.card__body {
  flex: 1; /* push the link to the bottom */
  padding: 1rem;
}

.card__title {
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
}

.card__text {
  color: #555;
  font-size: 0.9rem;
  line-height: 1.5;
}

.card__link {
  display: block;
  padding: 0.75rem 1rem;
  border-top: 1px solid #e0e0e0;
  text-align: center;
  text-decoration: none;
  color: #e94560;
  font-size: 0.9rem;
}
```

### Why it works

`flex: 1 1 280px` on each card means: grow to fill space, shrink if needed, start with a base width of 280px. Combined with `flex-wrap: wrap` on the container, cards will sit in a row when there's room and break onto new lines when there isn't — no media queries needed for the column count.

The deeper technique is the vertical Flexbox layout inside each card. By making `.card` a column-direction flex container and setting `flex: 1` on `.card__body`, the body expands to fill the available space. That forces `.card__link` to sit at the bottom of every card regardless of how much text each card contains — a common design requirement that Flexbox solves cleanly.

---

## Layout 3: A Vertically-Centered Hero Section

A hero section with a heading, subheading, and two buttons, centered both horizontally and vertically within the full viewport height.

### The HTML

```html
<section class="hero">
  <div class="hero__content">
    <h1 class="hero__title">Build better interfaces faster</h1>
    <p class="hero__subtitle">A visual playground for learning CSS Flexbox and Grid, interactively.</p>
    <div class="hero__actions">
      <a href="#" class="btn btn--primary">Try the Playground</a>
      <a href="#" class="btn btn--secondary">Read the Docs</a>
    </div>
  </div>
</section>
```

### The CSS

```css
.hero {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  padding: 2rem;
}

.hero__content {
  max-width: 640px;
  text-align: center;
  color: #ffffff;
}

.hero__title {
  font-size: clamp(2rem, 5vw, 3.5rem);
  font-weight: 800;
  line-height: 1.2;
  margin-bottom: 1rem;
}

.hero__subtitle {
  font-size: 1.125rem;
  color: #aaaacc;
  margin-bottom: 2rem;
  line-height: 1.6;
}

.hero__actions {
  display: flex;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.btn {
  display: inline-flex;
  align-items: center;
  padding: 0.75rem 1.75rem;
  border-radius: 6px;
  font-size: 1rem;
  text-decoration: none;
  font-weight: 600;
}

.btn--primary {
  background-color: #e94560;
  color: #ffffff;
}

.btn--secondary {
  border: 2px solid #ffffff;
  color: #ffffff;
}
```

### Why it works

The outer `.hero` uses `justify-content: center` and `align-items: center` to center `.hero__content` in both axes. `min-height: 100vh` gives the section enough height for the vertical centering to matter.

Inside `.hero__actions`, another flex container with `justify-content: center` and `gap: 1rem` places the buttons next to each other with even spacing. `flex-wrap: wrap` lets them stack on very narrow screens without explicit breakpoints.

Notice that the buttons use `display: inline-flex` with `align-items: center`. This is useful when buttons contain both text and an icon — it keeps them vertically centered within the button boundary.

---

## What You've Built

Three layouts, three sets of concepts:

- **Navbar**: `space-between` and `align-items: center` for horizontal bars
- **Card grid**: `flex-wrap`, `flex: 1 1 <min-width>`, and nested column flex for equal-height cards with pushed footers
- **Hero**: outer centering with `justify-content` + `align-items`, inner button group with another flex container

These patterns repeat throughout real codebases. Once you're comfortable adapting them, the majority of UI layout work becomes straightforward.
