---
title: "Percentage Difference vs. Percentage Change: What's the Difference?"
description: "Percentage difference and percentage change are not the same thing. Learn when to use each formula, see worked examples, and avoid the most common mistake."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["percentage difference", "percentage change", "comparison", "formula", "math concepts"]
draft: false
---

These two terms sound almost identical, and many people use them interchangeably. They should not — they measure different things, use different formulas, and give different answers from the same pair of numbers.

Understanding the distinction prevents genuine errors in analysis, reporting, and everyday reasoning.

## The core distinction

| Term | Question it answers | Has direction? | Formula |
|---|---|---|---|
| **Percentage change** | How much did this value change relative to a starting point? | Yes (increase or decrease) | `((New − Old) / Old) × 100` |
| **Percentage difference** | How different are these two values relative to their average? | No | `(\|V1 − V2\| / ((V1 + V2) / 2)) × 100` |

For more on this topic, see [*What Percentage Is X of Y? The Simple Formula Explained*](/blog/what-percentage-is-x-of-y).

The key insight:

- **Percentage change** has a clear "before" and "after" — a time sequence, or a reference and a comparison. The old value is the denominator.
- **Percentage difference** treats both values symmetrically — neither one is the reference. The average of the two values is the denominator.

## Percentage change: formula and examples

Use percentage change when one value clearly comes **before** or **is the baseline** for the other.

```
Percentage Change = ((New Value − Old Value) / Old Value) × 100
```

### Example 1 — Price over time

A product cost $80 in January and costs $96 in June.

```
((96 − 80) / 80) × 100 = (16 / 80) × 100 = +20%
```

The price **increased by 20%** relative to January.

### Example 2 — Year-on-year revenue

Revenue was $1.2M last year and is $1.08M this year.

```
((1.08 − 1.20) / 1.20) × 100 = (−0.12 / 1.20) × 100 = −10%
```

Revenue **decreased by 10%**.

The direction (positive/negative) matters here because January and last year are the defined baselines.

## Percentage difference: formula and examples

Use percentage difference when you are comparing two values **without a clear baseline** — two measurements at the same time, two competing options, two data points from different sources.

```
Percentage Difference = (|V1 − V2| / ((V1 + V2) / 2)) × 100
```

The denominator is the **average** (mean) of the two values, sometimes called the "midpoint" or "reference value."

### Example 1 — Two stores' prices

Store A sells the same item for $45; Store B sells it for $55. What is the percentage difference in price?

```
|45 − 55| = 10
Average = (45 + 55) / 2 = 50
Percentage Difference = (10 / 50) × 100 = 20%
```

The prices differ by **20%** (using the average price as the reference).

### Example 2 — Two lab measurements

Two technicians measured the same chemical sample: Technician A recorded 8.4 g and Technician B recorded 9.2 g. What is the percentage difference between the measurements?

```
|8.4 − 9.2| = 0.8
Average = (8.4 + 9.2) / 2 = 8.8
Percentage Difference = (0.8 / 8.8) × 100 = 9.09%
```

The measurements differ by approximately **9.1%**. Neither measurement is treated as the "correct" reference — both are equally uncertain.

## Why percentage difference uses the average as the denominator

This is the question most people ask. The reason comes down to symmetry.

Suppose you compare $45 and $55 using percentage change:

- From $45 perspective: `((55 − 45) / 45) × 100 = 22.2%`
- From $55 perspective: `((45 − 55) / 55) × 100 = −18.2%`

The same price gap gives you completely different percentages depending on which number you put in the denominator. That asymmetry is fine when one value is a true baseline (that is percentage change), but it is a problem when both values are equally valid.

For more on this topic, see [*Percentage of a Number: What It Means and How to Calculate It*](/blog/percentage-of-a-number).

Using the average as the denominator gives a single, symmetric answer: 20%.

## Side-by-side comparison with the same numbers

Take two values: **100 and 130**.

| Calculation | Formula | Result |
|---|---|---|
| % change from 100 to 130 | `((130 − 100) / 100) × 100` | **+30%** |
| % change from 130 to 100 | `((100 − 130) / 130) × 100` | **−23.1%** |
| % difference between 100 and 130 | `(30 / 115) × 100` | **26.1%** |

Three different numbers from the same pair of values — because each formula asks a different question.

## When to use each

**Use percentage change when:**
- You are tracking something over time (prices, sales, weight, temperature)
- You have a clear "before" and "after"
- You are measuring performance against a target or benchmark
- Direction matters (you want to know if it went up or down)

**Use percentage difference when:**
- You are comparing two simultaneous measurements
- Neither value is the "original" or "reference"
- You want a symmetric comparison (the order of V1 and V2 should not matter)
- You are reporting measurement error or variability between two instruments or observers

For more on this topic, see [*Percentage Error Formula: How to Calculate It in Science and Math*](/blog/percentage-error-formula).

## A note on percentage points

There is a third related concept worth keeping clear: **percentage points**.

Percentage points are used when both values are already expressed as percentages.

- An unemployment rate changing from 5% to 7% is an increase of **2 percentage points**.
- As a percentage change: `((7 − 5) / 5) × 100 = 40%` — a 40% increase in the rate itself.

Confusing these is extremely common in media reporting. "The interest rate rose 2%" and "the interest rate rose 2 percentage points" describe completely different moves.

## Common mistakes

**Mistake 1 — Using percentage change for symmetric comparisons.**
If you are comparing the price at two stores and neither is the "original," using `(A − B) / B` privileges store B unfairly. Use the average as the denominator.

**Mistake 2 — Using percentage difference for time-series data.**
If sales grew from Q1 to Q2, percentage difference gives a misleading result. You have a clear baseline (Q1), so use percentage change.

**Mistake 3 — Saying "percentage change" when you mean "percentage points."**
If a tax rate went from 20% to 25%, it increased by 5 percentage points, or by 25% as a percentage change. Be explicit.

## Calculate either instantly

Both formulas are straightforward once you identify which applies. Our [percentage calculator](/) handles both percentage change and percentage difference — enter your two values and let it decide the arithmetic.
