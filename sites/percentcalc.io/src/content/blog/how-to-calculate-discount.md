---
title: "How to Calculate a Discount Percentage (and the Final Price)"
description: "Learn how to calculate discount percentages and final sale prices with step-by-step formulas, worked examples, and a quick reference for common discounts."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["discount", "percentage", "sale price", "shopping math", "discount calculator"]
draft: false
---

Shops advertise discounts as percentages because "30% off" sounds better than "you save $18 on a $60 item." But to know whether a deal is actually good — or to compare two different offers — you need to do the math yourself. This guide covers everything: finding the discount percentage, calculating the final price, and working backwards from a sale price.

## The two discount calculations

There are two questions shoppers most often need to answer:

1. **The discount amount:** How many dollars do you save?
2. **The final price:** What do you actually pay?

Both start with the same two inputs: the original price and the discount percentage.

For more on this topic, see [*How to Calculate Percentage Decrease: Formula, Examples, and Use Cases*](/blog/how-to-calculate-percentage-decrease).

## Calculating the discount amount

```
Discount Amount = (Discount % / 100) × Original Price
```

**Example:** A $75 jacket is 20% off. How much do you save?

```
Discount Amount = (20 / 100) × 75 = 0.20 × 75 = $15
```

You save **$15**.

## Calculating the final (sale) price

**Method 1 — Subtract the discount:**
```
Final Price = Original Price − Discount Amount
```

Continuing the example: `$75 − $15 = $60`

**Method 2 — Multiply by the remaining fraction (faster):**
```
Final Price = Original Price × (1 − Discount % / 100)
```

```
Final Price = 75 × (1 − 0.20) = 75 × 0.80 = $60
```

Method 2 is one step faster and less prone to arithmetic errors. It works because "20% off" means you pay **80%** of the original price.

For more on this topic, see [*Percentage of a Number: What It Means and How to Calculate It*](/blog/percentage-of-a-number).

## Finding the discount percentage from prices

Sometimes you see a crossed-out original price and a sale price, and you want to know what percentage discount that represents.

For more on this topic, see [*How to Calculate Percentage Increase: Formula and Step-by-Step Guide*](/blog/how-to-calculate-percentage-increase).

```
Discount % = ((Original Price − Sale Price) / Original Price) × 100
```

**Example:** A TV is listed at $499.99, now marked down to $374.99.

```
Discount % = ((499.99 − 374.99) / 499.99) × 100
           = (125.00 / 499.99) × 100
           = 25.0%
```

The TV is **25% off**.

## Working backwards: finding the original price

You see a "sale price" tag but no original. You are told the discount was 30%.

```
Original Price = Sale Price / (1 − Discount % / 100)
```

**Example:** A pair of trainers costs $84 after a 30% discount. What was the original price?

```
Original Price = 84 / (1 − 0.30) = 84 / 0.70 = $120
```

The original price was **$120**.

A common mistake here is to add 30% to the sale price instead. Adding 30% to $84 gives $109.20 — which is wrong. You must divide by the remaining fraction.

## Stacked discounts

Retailers sometimes apply multiple discounts — "30% off, then an extra 10% off at checkout." These do **not** add up to 40%.

**How to calculate stacked discounts:**

Apply each discount sequentially:

1. Price after first discount: `$100 × (1 − 0.30) = $70`
2. Price after second discount: `$70 × (1 − 0.10) = $63`

Effective discount: `((100 − 63) / 100) × 100 = 37%`

**Not** 40%. The second 10% is applied to the already-reduced price, not the original.

## Quick reference: common discount calculations

| Original price | Discount | You save | You pay |
|---|---|---|---|
| $50 | 10% | $5.00 | $45.00 |
| $50 | 20% | $10.00 | $40.00 |
| $50 | 25% | $12.50 | $37.50 |
| $50 | 30% | $15.00 | $35.00 |
| $50 | 50% | $25.00 | $25.00 |
| $100 | 15% | $15.00 | $85.00 |
| $100 | 40% | $40.00 | $60.00 |
| $200 | 20% | $40.00 | $160.00 |
| $199.99 | 25% | $50.00 | $149.99 |
| $350 | 35% | $122.50 | $227.50 |

## Discount vs. markup: understanding both sides

If you sell goods, you need to understand markup as well as discount.

- **Discount** reduces a price toward the consumer. It is calculated on the *selling price*.
- **Markup** adds profit above cost. It is calculated on the *cost price*.

A product that costs you $40 and sells for $60 has:
- **Markup:** `((60 − 40) / 40) × 100 = 50%`
- **Margin:** `((60 − 40) / 60) × 100 = 33.3%`

When a retailer offers "30% off," the discount always comes off the selling price (which already includes markup).

## Comparing two discounts

Suppose you can buy the same item from two stores:

- Store A: Original $89.99, now $62.99
- Store B: $79.99 with a 20% discount coupon

**Store A discount percentage:**
```
((89.99 − 62.99) / 89.99) × 100 = 30.0%
```
Store A final price: $62.99

**Store B final price:**
```
79.99 × (1 − 0.20) = 79.99 × 0.80 = $63.99
```

Store A is the better deal — $1 cheaper despite the smaller original price.

## Tips for shopping with discounts

**Check the original price.** Retailers sometimes inflate the "original" price before marking it down. If you can, verify the item's regular price from a different retailer.

**Combine coupons with sales strategically.** When a store offers a percentage-off coupon on top of a sale, apply them in the right order. A 10% coupon applied to a sale price of $70 saves more absolute dollars than applying it first to $100 (then taking 30% off).

**Use the 10% shortcut.** To quickly estimate any discount, find 10% (move the decimal left one place) and scale up. 30% of $45 = three times 10% of $45 = $4.50 × 3 = $13.50.

## Try the calculator

When you are comparing multiple deals or juggling stacked discounts, mental arithmetic can get messy. Use our [percentage calculator](/) to check any discount in seconds — enter the original price and the discount percentage, and it will tell you exactly what you pay and what you save.
