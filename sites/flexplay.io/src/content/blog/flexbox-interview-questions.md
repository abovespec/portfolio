---
title: "CSS Flexbox Interview Questions and Answers (2026 Edition)"
description: "12 CSS Flexbox interview questions with clear answers. Covers core concepts, common gotchas, and what interviewers actually expect to hear from junior and mid-level developers."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["flexbox", "css", "interview", "reference"]
draft: false
---

CSS Flexbox questions come up in nearly every frontend interview, from junior roles to senior positions. The questions themselves are rarely tricky — interviewers are checking that you understand the mental model, not just that you've memorized property names. These answers are written to be both technically accurate and conversationally natural, which is what works in an actual interview setting.

---

## 1. What is Flexbox?

**Answer:** Flexbox is a CSS layout model designed for arranging elements along a single axis — either a row or a column. You activate it by applying `display: flex` to a parent element, which makes that element a flex container and its direct children flex items. The model gives you control over how items are sized, spaced, and aligned without using floats or manual position calculations.

For more on this topic, see [*What Is CSS Flexbox? A Plain-English Introduction*](/blog/what-is-flexbox).

The core value of Flexbox is that it handles three things that were painful before it existed: equal-height columns, vertical centering, and distributing space dynamically between items.

For more on this topic, see [*The Holy Grail Layout with Flexbox (and Why It's No Longer Holy)*](/blog/holy-grail-layout-css).

---

## 2. What is the difference between `justify-content` and `align-items`?

**Answer:** Both are alignment properties on the flex container, but they each control a different axis.

`justify-content` controls alignment along the **main axis** — the direction flex items flow. If items are in a row, `justify-content` distributes them horizontally.

`align-items` controls alignment along the **cross axis** — perpendicular to the flow direction. In a row layout, `align-items` controls vertical alignment.

A common interview follow-up: what happens when you switch to `flex-direction: column`? The axes swap. Now `justify-content` distributes items vertically and `align-items` controls horizontal alignment.

```css
/* Center something both ways */
.container {
  display: flex;
  justify-content: center; /* horizontal (main axis) */
  align-items: center;     /* vertical (cross axis) */
}
```

---

## 3. What does `flex: 1` mean?

**Answer:** `flex: 1` is shorthand for `flex-grow: 1; flex-shrink: 1; flex-basis: 0%`.

Breaking that down:
- `flex-grow: 1` — the item will grow to fill available space
- `flex-shrink: 1` — the item will shrink if there's not enough space
- `flex-basis: 0%` — the item starts from zero width before growing

When multiple siblings all have `flex: 1`, they each get an equal share of the available space. This is the standard way to create equal-width columns.

```css
.column {
  flex: 1; /* each column gets equal width */
}
```

---

## 4. How do you center an element with Flexbox?

**Answer:** Apply `display: flex`, `justify-content: center`, and `align-items: center` to the parent element. If you're centering within the full viewport, add `min-height: 100vh`.

```css
.parent {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}
```

That is the complete solution. Before Flexbox, this required a combination of `position: absolute`, `top: 50%`, `transform: translateY(-50%)`, and similar tricks.

---

## 5. What is the difference between `flex-start` and `flex-end` on the main axis vs the cross axis?

**Answer:** `flex-start` and `flex-end` are values used for both `justify-content` and `align-items`, but what "start" and "end" mean depends on which axis and which direction you're working with.

On the **main axis** with `flex-direction: row`:
- `justify-content: flex-start` packs items to the **left**
- `justify-content: flex-end` packs items to the **right**

On the **cross axis** with `flex-direction: row`:
- `align-items: flex-start` aligns items to the **top**
- `align-items: flex-end` aligns items to the **bottom**

When you switch to `flex-direction: column`, everything rotates. `justify-content: flex-start` now means "packed to the top" and `align-items: flex-start` means "packed to the left."

The key mental model: `flex-start` is always the start of whatever axis you're on, and what that means spatially depends on the direction.

---

## 6. When would you choose Grid over Flexbox?

**Answer:** When you need to control layout in two dimensions simultaneously.

Flexbox is one-dimensional — it arranges items along a single axis. Grid is two-dimensional — it lets you place items by row and column at the same time.

For more on this topic, see [*Flexbox vs CSS Grid: When to Use Each*](/blog/flexbox-vs-grid).

Choose Grid when:
- You're building a page-level layout with a header, sidebar, main content, and footer
- You need items in different rows to align with each other across columns
- You want to span an item across multiple rows or columns
- You're building an image gallery or data table where column alignment matters across rows

The short version: if you're thinking about rows and columns at the same time, reach for Grid.

---

## 7. What does `flex-shrink` do?

**Answer:** `flex-shrink` controls how much a flex item shrinks relative to its siblings when the container doesn't have enough space to fit everything at their natural or flex-basis sizes.

The default value is `1`, which means all items shrink proportionally. Setting `flex-shrink: 0` on an item makes it refuse to shrink — it holds its size even if siblings get smaller.

```css
.sidebar {
  flex: 0 0 240px; /* flex-grow: 0, flex-shrink: 0, flex-basis: 240px */
}

.main {
  flex: 1; /* grows and shrinks */
}
```

In this example, the sidebar stays exactly 240px regardless of the container size. The main area absorbs all size changes.

---

## 8. What is the default `flex-direction`?

**Answer:** The default is `row`, which means flex items are laid out horizontally from left to right (in left-to-right languages). This is why applying `display: flex` immediately lines items up in a row without any other changes.

The other values are `row-reverse`, `column`, and `column-reverse`.

---

## 9. How does `flex-wrap` work?

**Answer:** By default, flex items all try to fit on a single line even if they overflow. Setting `flex-wrap: wrap` allows items to break onto additional lines when there isn't enough room.

```css
.container {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.item {
  flex: 1 1 200px; /* minimum 200px wide, then grow */
}
```

This pattern — `flex-wrap: wrap` combined with a `flex-basis` minimum width — is the standard way to build a responsive card grid without media queries.

When wrapping is enabled, a related property becomes relevant: `align-content`. While `align-items` aligns items within a single line on the cross axis, `align-content` distributes the multiple wrapped lines relative to each other.

---

## 10. What is `align-content` and when does it apply?

**Answer:** `align-content` distributes the space between and around **wrapped lines** on the cross axis. It is similar to `justify-content`, but for lines rather than individual items, and it operates on the cross axis rather than the main axis.

It only has an effect when two conditions are met:
1. The container has `flex-wrap: wrap` (or `wrap-reverse`)
2. The container is tall enough that there is extra space beyond what the lines need

```css
.container {
  display: flex;
  flex-wrap: wrap;
  align-content: space-between; /* distribute wrapped lines vertically */
  height: 500px;
}
```

If there is only one line of items, `align-content` does nothing. This is a common source of confusion when developers try to use it on a single-row container and see no effect.

---

## 11. What does `align-self` do, and how is it different from `align-items`?

**Answer:** `align-items` is set on the container and applies to all flex items. `align-self` is set on an individual item and overrides `align-items` for just that one item.

```css
.container {
  display: flex;
  align-items: center; /* all items centered by default */
}

.special {
  align-self: flex-start; /* this item ignores the container rule */
}
```

This is useful when you want most items aligned one way but need one item (like a badge, icon, or label) to position differently.

---

## 12. What happens to items with `display: flex` when they overflow the container?

**Answer:** By default, with `flex-wrap: nowrap`, items will overflow the container rather than wrapping. They maintain their flex-basis or content size and push past the container edge.

To prevent overflow, you have two main options:

1. **Add `flex-wrap: wrap`** so items break onto a new line instead of overflowing.
2. **Let `flex-shrink` do its job** — the default `flex-shrink: 1` means items will compress to fit. If items still overflow, it's often because a minimum content size (`min-width: auto`) is preventing further shrinking.

```css
/* Fix for items that won't shrink below their content size */
.item {
  min-width: 0; /* remove the automatic minimum */
}
```

Setting `min-width: 0` on flex items is a useful debugging trick when items refuse to shrink as expected — it removes the browser's default minimum content sizing constraint.

---

## Preparation Tips

These questions cover the core Flexbox model. For interviews, make sure you can explain the axis model without hesitation — which property controls which axis, and what changes when `flex-direction` switches to `column`. That single concept underlies most of the other answers.

Practicing with an interactive playground (like the one on this site) is more effective than re-reading property lists. You'll internalize the behavior faster when you can see each property change the layout in real time.
