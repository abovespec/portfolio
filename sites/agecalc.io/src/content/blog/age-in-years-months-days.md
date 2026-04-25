---
title: "How to Calculate Age in Years, Months, and Days"
description: "Learn the step-by-step method to break down your exact age into years, months, and days—including how to handle unequal months and leap years."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["age calculator", "years months days", "exact age", "age calculation"]
draft: false
---

Saying you're "34 years old" is usually sufficient. But there are situations where "34 years, 3 months, and 17 days" is the correct answer—and knowing how to get there manually saves you from guessing.

This article walks through the full calculation method, explains the tricky edge cases (unequal month lengths, year-crossing), and shows you when a tool like our [age calculator](/) is the faster choice.

## When You Need Age in Years, Months, and Days

Most of the time, your year-age is enough. The granular breakdown becomes relevant when:

- **Medical records** require exact age for dosing, screening schedules, or developmental assessments
- **Legal documents** specify eligibility as of a particular date ("must be 18 years of age as of contract signing")
- **Visa and passport applications** ask you to confirm age at date of travel
- **Benefit calculations** use birth-month precision for Social Security, pension, or insurance start dates
- **Personal milestones** — many people want to know exactly how old they'll be on a future date

## Step-by-Step Calculation

Let's work through an example.

**Birth date:** March 15, 1991  
**Today's date:** April 25, 2026

**Step 1: Calculate complete years**

Starting from 2026, count back to 1991:
> 2026 − 1991 = 35

Check: has the birthday (March 15) passed yet in 2026? Yes — March 15 was 41 days ago.

**Complete years: 35**

**Step 2: Count complete months since the last birthday**

Last birthday: March 15, 2026.  
From March 15 to April 25:
- April 15 marks one complete month.
- We're now at April 25, which is 10 days into the second month.

**Complete months: 1**

**Step 3: Count remaining days**

From April 15 to April 25 = 10 days.

**Remaining days: 10**

**Full age: 35 years, 1 month, 10 days**

## The Tricky Part: Unequal Month Lengths

The manual calculation runs into trouble when birth days and current days don't align neatly. Two common scenarios:

### Case 1: Born on the 31st, counting through a shorter month

Born January 31. Counting to March 1.

- January 31 + 1 month → "February 31" doesn't exist.
- Convention: the last day of February (28 or 29 in a leap year) counts as the one-month mark.
- February 28 to March 1 = 1 day.

So from January 31 to March 1 = **1 month, 1 day** (not 1 month, 0 days as you might expect).

### Case 2: Current day is earlier in the month than birth day

Born July 20. Today is June 5.

- Preliminary years: current year − birth year, minus 1 (birthday hasn't passed yet this year).
- Last birthday: July 20 of last year.
- From July 20 last year to June 5 this year:
  - August, September, October, November, December, January, February, March, April, May = 10 complete months
  - May 20 to June 5 = 16 days

**Age:** (current year − birth year − 1) years, 10 months, 16 days.

If you're doing this without a calculator, drawing a mini-calendar helps. With one, the [age calculator](/) handles these edge cases correctly every time.

## Leap Year Considerations

Leap years affect day-counts but not year/month age in most practical contexts. The exception: if you were born on **February 29**, your birthday in non-leap years requires a convention.

Most systems (and countries) treat **March 1** as the equivalent birthday in years without February 29. So:

- Born February 29, 1996
- In 2026 (not a leap year), birthday = March 1
- On April 25, 2026: birthday was March 1, so you've completed one month, 24 days past your birthday
- Age: 30 years, 1 month, 25 days

## Calculating in Excel or Google Sheets

Excel's `DATEDIF` function is designed exactly for this:

| Formula | Result |
|---------|--------|
| `=DATEDIF(A1, TODAY(), "Y")` | Complete years |
| `=DATEDIF(A1, TODAY(), "YM")` | Complete months after full years |
| `=DATEDIF(A1, TODAY(), "MD")` | Remaining days after full months |

Where `A1` contains the birth date. Combine them:

```
=DATEDIF(A1,TODAY(),"Y")&" yrs, "&DATEDIF(A1,TODAY(),"YM")&" mo, "&DATEDIF(A1,TODAY(),"MD")&" d"
```

This is the same logic an age calculator runs under the hood, made visible.

## Quick Reference: Which Method to Use

| Scenario | Best approach |
|----------|---------------|
| Quick year-age | Mental math: current year − birth year ±1 |
| Document requiring years/months/days | Step-by-step manual or Excel |
| Day-precise age (including leap days) | Online age calculator |
| Bulk calculations across many dates | Excel DATEDIF |
| Future date age ("how old will I be on X?") | Online age calculator |

The step-by-step method is worth knowing once. After that, our [age calculator](/) returns the full years/months/days breakdown instantly without the edge-case arithmetic.
