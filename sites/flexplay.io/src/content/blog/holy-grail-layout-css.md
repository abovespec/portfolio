---
title: "The Holy Grail Layout with Flexbox (and Why It's No Longer Holy)"
description: "The holy grail layout — header, footer, two sidebars, and main content — was once a CSS puzzle. Here's how to build it with Flexbox, and why CSS Grid makes it trivial."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["flexbox", "css grid", "layout", "css"]
draft: false
---

The name "holy grail layout" came from the days when achieving it was considered an almost mythical feat of CSS engineering. The layout itself is unremarkable by modern standards: a full-page structure with a header at the top, a footer at the bottom, and three columns in between — a left sidebar, a main content area, and a right sidebar.

That's it. And it nearly broke CSS developers for a decade.

## Why It Was Hard Before Flexbox

The classic implementation requirements made it deceptively difficult:

1. All three columns must be the same height regardless of content
2. The main content column must come first in the HTML for SEO and accessibility reasons
3. The left and right sidebars must have fixed widths; the center must be fluid
4. The footer must stick to the bottom even when the page content is short

Pre-Flexbox, achieving all four of those simultaneously required float hacks, negative margins, padding tricks, and often JavaScript polyfills. Multiple competing solutions existed, each with different trade-offs. The fact that there was no clean CSS-only answer is what made it "holy."

For more on this topic, see [*What Is CSS Flexbox? A Plain-English Introduction*](/blog/what-is-flexbox).

## Implementing It with Flexbox

Flexbox makes this substantially easier. Here is the HTML structure:

```html
<div class="page">
  <header class="header">Header</header>
  <div class="body">
    <main class="main">Main Content</main>
    <aside class="sidebar sidebar--left">Left Sidebar</aside>
    <aside class="sidebar sidebar--right">Right Sidebar</aside>
  </div>
  <footer class="footer">Footer</footer>
</div>
```

Note: the `main` element appears first in the HTML for source order reasons, even though it renders in the center. Flexbox's `order` property handles the visual rearrangement.

For more on this topic, see [*CSS Flexbox Cheat Sheet: Every Property Explained*](/blog/flexbox-cheat-sheet).

### The CSS

```css
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.page {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.header,
.footer {
  padding: 1rem 2rem;
  background: #1a1a2e;
  color: #ffffff;
}

.body {
  display: flex;
  flex: 1; /* expand to fill available vertical space */
}

.sidebar {
  flex: 0 0 220px; /* fixed width, no grow, no shrink */
  background: #f0f0f5;
  padding: 1.5rem;
}

.sidebar--left {
  order: -1; /* visually move left sidebar before main content */
}

.main {
  flex: 1; /* take all remaining horizontal space */
  padding: 1.5rem;
  background: #ffffff;
}
```

### How Each Part Works

**`.page` as a column flex container** — the outer container stacks header, body section, and footer vertically. `min-height: 100vh` ensures the page fills the full viewport even when there's little content.

**`flex: 1` on `.body`** — this is what makes the footer stick to the bottom. The body section grows to fill whatever vertical space is left after the header and footer take their natural heights.

**`.body` as a row flex container** — this is the inner flex layout for the three columns. By default, flex items in a row container stretch to the same height (`align-items: stretch`), which is exactly what solves the equal-height columns problem.

**`flex: 0 0 220px` on sidebars** — zero grow, zero shrink, fixed 220px basis. The sidebars stay exactly 220px wide no matter what.

**`flex: 1` on `.main`** — takes all horizontal space that the sidebars don't claim.

**`order: -1` on `.sidebar--left`** — the main content is first in HTML, but `order: -1` moves the left sidebar before it visually without touching the markup.

## The Modern Approach: CSS Grid

Here is the same layout using CSS Grid:

```css
.page {
  display: grid;
  grid-template-columns: 220px 1fr 220px;
  grid-template-rows: auto 1fr auto;
  grid-template-areas:
    "header  header  header"
    "sidebar-left  main  sidebar-right"
    "footer  footer  footer";
  min-height: 100vh;
}

.header        &#123; grid-area: header; &#125;
.main          &#123; grid-area: main; &#125;
.sidebar--left  &#123; grid-area: sidebar-left; &#125;
.sidebar--right &#123; grid-area: sidebar-right; &#125;
.footer        &#123; grid-area: footer; &#125;
```

That is the entire layout. No nested containers, no `order` tricks, no `flex: 1` on an intermediate wrapper. The structure is declared explicitly in `grid-template-areas` and each element uses a `grid-area` name to slot into position.

With Grid, the HTML order no longer matters for visual placement. The main content can be first in markup without needing `order` to fix the column sequence.

## Flexbox vs Grid for This Layout

| Concern | Flexbox | Grid |
|---------|---------|------|
| Lines of CSS (roughly) | ~25 | ~15 |
| Nesting required | Yes (outer column + inner row) | No |
| HTML order flexibility | Requires `order` | Unrestricted |
| Cross-browser support | Excellent | Excellent (IE 11 with `-ms-` prefix) |
| Readability | Moderate | High |

For more on this topic, see [*Flexbox vs CSS Grid: When to Use Each*](/blog/flexbox-vs-grid).

The honest assessment: CSS Grid wins for this layout. The holy grail is a classic two-dimensional problem — rows and columns simultaneously — and that's Grid's native domain.

## When to Still Use Flexbox for This

The Flexbox version remains useful in two scenarios:

1. **You're supporting an older environment** where Grid isn't available or reliable. This is increasingly rare but does come up in embedded webviews and certain corporate tooling.

2. **You need the layout to be dynamic based on item count.** Flexbox wrapping behavior adapts to content in ways Grid tracks do not, and for certain fluid layouts that can be an advantage.

For a new project with modern browser targets, use Grid for the outer page structure and Flexbox for alignment inside each region. The holy grail is now a 10-line exercise, which is perhaps the best evidence of how far CSS has come.
