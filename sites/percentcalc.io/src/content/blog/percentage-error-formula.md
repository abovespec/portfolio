---
title: "Percentage Error Formula: How to Calculate It in Science and Math"
description: "Learn the percentage error formula used in science and mathematics, see worked examples, and understand when percentage error matters versus other error metrics."
publishDate: 2026-05-22
updatedDate: 2026-05-22
author: "Editorial Team"
tags: ["percentage error", "percentage formula", "science", "math", "measurement error"]
draft: false
---

Percentage error quantifies how far a measured or estimated value deviates from the true or accepted value. It is fundamental in science, engineering, and any field where measurements must be validated against a known standard.

## The percentage error formula

```
Percentage Error = ((|Measured Value − True Value|) / |True Value|) × 100
```

The vertical bars indicate absolute value — you take the magnitude of the difference, ignoring whether the measurement was too high or too low. The result is always a non-negative number.

Some fields use a signed version (without absolute values) when the direction of the error matters — but the standard formula gives unsigned percentage error.

For more on this topic, see [*Percentage Change Formula: How to Calculate Increase and Decrease*](/blog/percentage-change-formula).

## Step-by-step worked examples

### Example 1 — Lab measurement

A student measures the boiling point of ethanol in a lab and records 77.2 °C. The accepted value is 78.4 °C. What is the percentage error?

For more on this topic, see [*How to Calculate Percentage Decrease: Formula, Examples, and Use Cases*](/blog/how-to-calculate-percentage-decrease).

1. Find the absolute difference: |77.2 − 78.4| = 1.2
2. Divide by the true value: 1.2 / 78.4 = 0.01531
3. Multiply by 100: 0.01531 × 100 = **1.53%**

The measurement was 1.53% below the accepted value.

### Example 2 — Estimated vs. actual cost

An engineer estimates a construction project will cost $340,000. The actual cost comes in at $382,500. What is the percentage error in the estimate?

1. |$340,000 − $382,500| = $42,500
2. $42,500 / $382,500 = 0.1111
3. 0.1111 × 100 = **11.1%**

The estimate had an 11.1% error.

### Example 3 — Density measurement

A student calculates the density of a metal block as 8.42 g/cm³. The accepted density for that metal is 8.96 g/cm³.

1. |8.42 − 8.96| = 0.54
2. 0.54 / 8.96 = 0.0603
3. 0.0603 × 100 = **6.0%**

Percentage error = 6.0%.

### Example 4 — Weighing a sample

A balance reads 14.87 g for a sample known to weigh 15.00 g.

1. |14.87 − 15.00| = 0.13
2. 0.13 / 15.00 = 0.00867
3. 0.00867 × 100 = **0.87%**

This is a relatively small error, suggesting the balance is reasonably accurate.

## Why absolute value?

The absolute value in the formula prevents positive and negative errors from cancelling out. Without it, a measurement that is 5% too high and one that is 5% too low would both report as 0% error if averaged — which is misleading.

If you want to know the *direction* of error (whether you over- or underestimated), use the signed version:

```
Signed % Error = ((Measured Value − True Value) / True Value) × 100
```

- Positive result: measured value was too high
- Negative result: measured value was too low

## What counts as acceptable percentage error?

There is no universal threshold — it depends entirely on the field and the application.

| Field | Typical acceptable error |
|---|---|
| Physics / chemistry lab (student) | 5–10% |
| Engineering tolerances (general) | 1–5% |
| Pharmaceutical manufacturing | < 0.5–2% |
| High-precision manufacturing | < 0.1% |
| Everyday estimates | 10–20% |

A 2% error in a student chemistry experiment might be excellent. A 2% error in a drug dosage calculation is potentially dangerous.

## Percentage error vs. percentage difference

These two concepts are often confused:

- **Percentage error** compares a measurement to a *known true value*. There is a reference point.
- **Percentage difference** compares two values when neither is considered the definitive "true" value — for example, comparing two suppliers' prices or two experimental readings. See the formula: `|Value 1 − Value 2| / ((Value 1 + Value 2) / 2) × 100`.

For more on this topic, see [*How to Calculate Percentage Increase: Formula and Step-by-Step Guide*](/blog/how-to-calculate-percentage-increase).

Use percentage error when you have a standard or accepted value to measure against. Use percentage difference when you are comparing two measurements of equal standing.

## Percentage error vs. absolute error

**Absolute error** is simply the difference in the same units as the measurement:

```
Absolute Error = |Measured Value − True Value|
```

For Example 1 above, the absolute error is 1.2 °C. This tells you the raw deviation.

**Percentage error** normalises this deviation relative to the true value, making comparisons across different measurements meaningful. A 1.2 °C error when measuring something at 78 °C is very different from a 1.2 °C error when measuring something at 5 °C.

## Sources of percentage error

Understanding where error comes from helps reduce it:

**Instrument error:** Every measuring instrument has a finite precision. A ruler marked in millimetres cannot reliably measure to 0.1 mm.

**Parallax error:** Reading a scale at an angle rather than straight-on introduces systematic misreadings.

**Human error:** Transcription mistakes, rounding during intermediate steps, or misreading a display.

**Environmental factors:** Temperature, pressure, and humidity can affect measurements in sensitive instruments.

**Random error:** Unpredictable fluctuations in experimental conditions — usually reduced by taking multiple readings and averaging.

## Reducing percentage error

- Calibrate instruments before use.
- Use equipment with appropriate precision for the measurement needed.
- Take multiple readings and calculate the mean.
- Avoid rounding during intermediate steps — only round the final result.
- Control environmental variables where possible.

For straightforward percentage error calculations, the [percentage calculator](/) can handle the arithmetic once you have your measured and true values in hand.
