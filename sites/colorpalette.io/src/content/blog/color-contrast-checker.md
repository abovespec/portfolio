---
title: "How to Check Color Contrast (and Why Your Eyes Can Lie to You)"
description: "Your eyes adapt in ways that make poor contrast look fine—until someone else reads it. Learn how color contrast checkers work, what WCAG ratios mean, and common pitfalls to avoid."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["color contrast", "accessibility", "WCAG", "contrast checker", "web design"]
draft: false
---

You've chosen a text color that looks perfectly readable on your monitor in a bright office. Then someone opens your site on a phone in sunlight, or someone with low vision visits, or someone opens it on a display with slightly different color calibration — and suddenly that carefully chosen gray text on a white background is nearly invisible.

Your eyes are adaptive. A contrast checker is not. That's exactly why you need one.

## Why Contrast Matters

Readable contrast isn't just an aesthetic consideration — it's a functional one. When the foreground color (usually text) doesn't have sufficient luminance difference from the background, people have to strain to read. For users with low vision, cataracts, or color vision deficiencies, insufficient contrast doesn't cause mild discomfort; it makes content genuinely inaccessible.

The Web Content Accessibility Guidelines (WCAG) exist to set a minimum standard that serves a broad range of users. Meeting those standards is also a legal baseline in many jurisdictions for public-facing websites.

Beyond legal compliance, readable contrast is just better design. Text that reads clearly in any lighting condition, on any display, without effort is text that people actually read.

## How Your Eyes Lie to You

Several well-documented perceptual phenomena cause us to misjudge contrast:

**Adaptation.** Your visual system continuously adjusts to the lighting and color in your environment. If you've been looking at a bright white background for a while, your eye adapts and you perceive moderate contrast as adequate. Step away, come back fresh, and you'll often see it differently.

**Simultaneous contrast.** The same gray text looks different on a pure white background versus a slightly off-white or cream background. The surrounding color shifts your perception of the foreground color's lightness.

**Display variation.** Your monitor's brightness setting, gamma calibration, and panel technology all affect how contrast actually renders. A laptop screen viewed at an angle will show notably lower contrast than the same screen viewed straight on. A phone screen in direct sunlight requires significantly more contrast to compensate.

**Fatigue.** Moderate contrast might look fine when you're fresh and focused. The same contrast becomes harder to parse when you're tired, distracted, or reading for an extended period.

A contrast checker strips away all of this subjectivity. It computes a ratio based on the mathematical luminance of two colors — the same number regardless of your display, mood, or how long you've been staring at a screen.

## How Contrast Ratio Is Calculated

WCAG defines contrast ratio using a formula based on relative luminance — essentially, how much light a color reflects or emits relative to pure white.

Pure white has a relative luminance of 1.0. Pure black has a relative luminance of 0.0. The contrast ratio between them is 21:1, which is the maximum possible.

The formula for contrast ratio is:

```
(L1 + 0.05) / (L2 + 0.05)
```

Where L1 is the lighter color's relative luminance and L2 is the darker color's relative luminance. The result is expressed as a ratio — 4.5:1, 7:1, and so on.

You don't need to calculate this by hand. A contrast checker takes two hex codes (or RGB values), runs this math, and tells you the ratio and whether it passes or fails the relevant WCAG levels.

## What the Ratios Mean

**3:1** — The minimum for large text (18pt or 14pt bold) and for user interface components like input borders and icons. This level is required at WCAG Level AA.

**4.5:1** — The standard for normal-sized text at WCAG Level AA. This is the threshold that most accessibility requirements reference, and the one you should design for by default.

**7:1** — The stricter threshold for Level AAA compliance, for both normal and large text. This level isn't required for most projects but is appropriate for content primarily serving users with low vision.

**21:1** — Black on white, the theoretical maximum. Not practical as a design target, but useful to understand as the upper bound.

## Common Pitfalls

**Light gray text on white backgrounds.** This is probably the most common contrast failure on the modern web. Light gray text (#999 on white, for example) sits around 2.85:1 — well below the 4.5:1 threshold. It looks clean and minimal on a well-calibrated monitor. It's borderline unreadable in other conditions. If you want gray body text, you generally need to go darker than your instincts suggest: #767676 is the lightest gray that achieves 4.5:1 on white.

**White text on medium-value colors.** White text on a mid-range blue, green, or red can look confident and designed but fail contrast checks. A blue like #4A90D9 with white text produces around 3.1:1 — fine for large text, insufficient for body copy.

**Placeholder text.** Form placeholder text is commonly styled at very low contrast by default. Because it's meant to disappear when the user types, designers often treat it as decorative. But placeholder text carries functional information (field labels or examples), and it needs to meet the same contrast thresholds as any other text.

**Colored text on colored backgrounds.** When neither color is close to white or black, the contrast is often lower than it appears. An orange heading on a yellow background might look vivid and high-energy while having a contrast ratio below 2:1.

**Focus indicators.** WCAG 2.2 added specific requirements for focus indicator contrast. The visible outline when a keyboard user focuses on an element needs 3:1 contrast against adjacent colors. This is frequently overlooked.

## Using a Contrast Checker

The workflow is simple:

1. **Enter your foreground and background colors.** Use hex codes, RGB values, or HSL — most checkers accept all three. If you're not sure of the exact values in use, browser developer tools can pick them directly from any element.
2. **Read the ratio and pass/fail result.** The checker will tell you the computed ratio and whether it passes at the AA or AAA level for normal and large text.
3. **Adjust if needed.** If the text fails, darken the foreground color (or lighten it, if it's on a dark background) until the ratio hits your target. Most checkers update in real time as you adjust values.

A color palette generator with contrast checking built in is particularly useful early in the design process, when you're establishing your palette. If you test contrast during palette selection — before you've applied colors to dozens of components — you save yourself significant rework later.

## A Sustainable Approach

Rather than checking contrast as an afterthought at the end of a project, build it into your process at the palette stage. Designate your text colors, background colors, and surface colors, then verify every intended combination before you start applying them. If your primary text color passes 4.5:1 against your background color from the start, you're designing with confidence rather than hoping it works out.

Your eyes will tell you something looks readable. A contrast checker tells you whether it actually is.
