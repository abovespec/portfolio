---
title: "CSS Flexbox Cheat Sheet: Every Property Explained"
description: "A complete CSS Flexbox cheat sheet covering every container and item property with explanations, common values, and code examples for the trickier ones."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["flexbox", "css", "reference", "cheat sheet"]
draft: false
---

This reference covers every Flexbox property — the ones on containers and the ones on individual items. Each entry explains what the property does, lists the valid values, and shows a code example where the behavior isn't immediately obvious from the value names.

---

## Container Properties

These properties are applied to the **flex container** — the parent element that has `display: flex`.

---

### `display`

Establishes the element as a flex container.

```css
.container {
  display: flex;        /* block-level flex container */
  display: inline-flex; /* inline-level flex container */
}
```

`inline-flex` makes the container itself behave like an inline element while its children still use flex layout internally.

---

### `flex-direction`

Sets the direction of the main axis — the direction flex items flow.

```css
.container {
  flex-direction: row;            /* left to right (default) */
  flex-direction: row-reverse;    /* right to left */
  flex-direction: column;         /* top to bottom */
  flex-direction: column-reverse; /* bottom to top */
}
```

Changing `flex-direction` rotates both axes. In `column` mode, `justify-content` distributes along the vertical axis and `align-items` works horizontally.

---

### `flex-wrap`

Controls whether items stay on one line or wrap onto multiple lines.

```css
.container {
  flex-wrap: nowrap;       /* default — single line, items may overflow */
  flex-wrap: wrap;         /* items wrap onto additional lines */
  flex-wrap: wrap-reverse; /* wrap, but lines appear in reverse order */
}
```

When items wrap, `align-content` (not `align-items`) controls how the wrapped lines are distributed.

---

### `flex-flow`

Shorthand for `flex-direction` and `flex-wrap`.

```css
.container {
  flex-flow: row wrap;        /* flex-direction: row; flex-wrap: wrap; */
  flex-flow: column nowrap;   /* flex-direction: column; flex-wrap: nowrap; */
}
```

---

### `justify-content`

Distributes items and space along the **main axis** (the direction of flow).

```css
.container {
  justify-content: flex-start;    /* default — items packed to start */
  justify-content: flex-end;      /* items packed to end */
  justify-content: center;        /* items centered */
  justify-content: space-between; /* equal gaps between items; no edge gaps */
  justify-content: space-around;  /* equal space on each side of each item */
  justify-content: space-evenly;  /* equal space between items and edges */
}
```

`space-between` vs `space-around` vs `space-evenly` is a common trip-up. The quick mental model: `between` has no outer gap, `around` has half-size outer gaps, `evenly` has full-size outer gaps.

---

### `align-items`

Aligns items on the **cross axis** (perpendicular to flow) within a single line.

```css
.container {
  align-items: stretch;    /* default — items stretch to fill the container height */
  align-items: flex-start; /* items align to start of cross axis */
  align-items: flex-end;   /* items align to end of cross axis */
  align-items: center;     /* items center on cross axis */
  align-items: baseline;   /* items align by their text baselines */
}
```

`stretch` is the reason all sibling flex items end up the same height by default — they expand to fill the container's cross-axis dimension.

---

### `align-content`

Distributes **wrapped lines** along the cross axis. Only applies when `flex-wrap: wrap` is set and there are multiple lines.

```css
.container {
  align-content: flex-start;    /* lines packed to start */
  align-content: flex-end;      /* lines packed to end */
  align-content: center;        /* lines centered */
  align-content: space-between; /* equal gaps between lines */
  align-content: space-around;  /* equal space around each line */
  align-content: space-evenly;  /* equal space between lines and edges */
  align-content: stretch;       /* default — lines stretch to fill container */
}
```

A common mistake is applying `align-content` to a single-line flex container and wondering why it has no effect. It only does something when there are two or more wrapped lines.

---

### `gap`

Sets spacing between flex items. Much cleaner than margin-based spacing.

```css
.container {
  gap: 1rem;          /* same gap in both row and column directions */
  gap: 1rem 2rem;     /* row-gap column-gap */
  row-gap: 1rem;      /* only between rows */
  column-gap: 2rem;   /* only between columns */
}
```

`gap` does not add space at the outer edges of the container — only between items. This makes it preferable to `margin` in most cases, since you don't need to cancel the margin on the first or last item.

---

## Item Properties

These properties are applied to the **flex items** — the direct children of a flex container.

---

### `order`

Controls the visual order of flex items without changing the HTML.

```css
.item {
  order: 0;  /* default — items appear in source order */
  order: -1; /* move to the front */
  order: 1;  /* move toward the end */
}
```

Items with the same `order` value appear in source order relative to each other. This is useful for reordering content for mobile-first designs.

Note: `order` affects visual order only, not tab order for keyboard navigation. Use with caution for accessibility-sensitive layouts.

---

### `flex-grow`

Defines how much a flex item will grow relative to siblings when there's extra space.

```css
.item {
  flex-grow: 0; /* default — does not grow */
  flex-grow: 1; /* grows to fill available space */
  flex-grow: 2; /* grows at twice the rate of flex-grow: 1 siblings */
}
```

If three items have `flex-grow: 1`, `flex-grow: 2`, and `flex-grow: 1`, the available space is divided into 4 parts. The second item gets 2 parts, the others get 1 each.

---

### `flex-shrink`

Defines how much a flex item will shrink when there's not enough space.

```css
.item {
  flex-shrink: 1; /* default — shrinks proportionally */
  flex-shrink: 0; /* does not shrink (will overflow if needed) */
  flex-shrink: 2; /* shrinks at twice the rate of flex-shrink: 1 siblings */
}
```

Setting `flex-shrink: 0` on a sidebar alongside a `flex-grow: 1` main content area is a very common pattern: the sidebar stays fixed-width while the main area flexes.

```css
.sidebar  &#123; flex-shrink: 0; width: 250px; &#125;
.main     &#123; flex-grow: 1; &#125;
```

---

### `flex-basis`

Sets the initial size of a flex item before growing or shrinking is calculated.

```css
.item {
  flex-basis: auto;   /* default — use the item's natural width/height */
  flex-basis: 0;      /* start from zero; growth is calculated from there */
  flex-basis: 200px;  /* item starts at 200px, then grows/shrinks from there */
  flex-basis: 25%;    /* item starts at 25% of the container */
}
```

`flex-basis: 0` combined with `flex-grow: 1` means items share space equally regardless of their content size. `flex-basis: auto` means items start at their content size and then grow or shrink from there.

---

### `flex` (shorthand)

The shorthand for `flex-grow`, `flex-shrink`, and `flex-basis`. Recommended over setting the three properties individually.

```css
.item {
  flex: 0 1 auto;   /* default — no grow, shrink, auto basis */
  flex: 1;          /* shorthand for flex: 1 1 0% */
  flex: auto;       /* shorthand for flex: 1 1 auto */
  flex: none;       /* shorthand for flex: 0 0 auto (rigid item) */
  flex: 1 1 200px;  /* grow and shrink from a 200px base */
}
```

`flex: 1` is the most commonly used value. It causes the item to grow, shrink, and start from zero, making all siblings share space equally.

```css
/* Three equal-width columns */
.column {
  flex: 1;
}
```

---

### `align-self`

Overrides the container's `align-items` value for an individual item.

```css
.item {
  align-self: auto;       /* default — inherits align-items from container */
  align-self: flex-start; /* align this item to start of cross axis */
  align-self: flex-end;   /* align this item to end of cross axis */
  align-self: center;     /* center this item on cross axis */
  align-self: stretch;    /* stretch this item on cross axis */
  align-self: baseline;   /* align by text baseline */
}
```

This is useful when you want most items to align one way but need one specific item to behave differently — for example, a "pinned" badge that should sit at the top while other items are centered.

---

## Quick Reference Table

| Property | Applies to | Controls |
|----------|------------|---------|
| `display` | Container | Enable flex layout |
| `flex-direction` | Container | Main axis direction |
| `flex-wrap` | Container | Single vs multiple lines |
| `flex-flow` | Container | Shorthand for direction + wrap |
| `justify-content` | Container | Main axis alignment |
| `align-items` | Container | Cross axis alignment (single line) |
| `align-content` | Container | Cross axis alignment (multi-line) |
| `gap` | Container | Space between items |
| `order` | Item | Visual position |
| `flex-grow` | Item | How much item grows |
| `flex-shrink` | Item | How much item shrinks |
| `flex-basis` | Item | Starting size |
| `flex` | Item | Shorthand for grow + shrink + basis |
| `align-self` | Item | Override cross-axis alignment for this item |
