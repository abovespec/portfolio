---
title: "How to Calculate Age in Excel: DATEDIF and Other Formulas"
description: "A practical guide to calculating age in Excel using DATEDIF, YEARFRAC, and other formulas—with worked examples and common pitfalls to avoid."
publishDate: 2026-05-22
updatedDate: 2026-05-22
author: "Editorial Team"
tags: ["age calculation", "Excel", "DATEDIF", "spreadsheet", "age formula"]
draft: false
---

Excel can calculate age automatically once you know which functions to reach for. The most reliable is `DATEDIF`—an undocumented but long-stable function that handles month-end quirks and leap years without any extra logic on your part.

## The DATEDIF Function

`DATEDIF` takes three arguments: a start date, an end date, and a unit code.

```
=DATEDIF(start_date, end_date, unit)
```

The unit codes relevant to age calculation:

For more on this topic, see [*How Old Am I in Months? Converting Your Age to Months*](/blog/how-old-am-i-in-months).

| Unit | Returns |
|------|---------|
| `"Y"` | Complete years between the two dates |
| `"M"` | Complete months between the two dates |
| `"D"` | Complete days between the two dates |
| `"YM"` | Remaining months after subtracting complete years |
| `"YD"` | Remaining days after subtracting complete years |
| `"MD"` | Remaining days after subtracting complete months |

For more on this topic, see [*How to Calculate Your Exact Age in Years, Months, and Days*](/blog/how-to-calculate-exact-age-years-months-days).

**Basic age in years:**

```
=DATEDIF(A2, TODAY(), "Y")
```

Put the date of birth in cell A2, and this formula returns the person's current age in complete years—automatically updated every time the spreadsheet recalculates.

**Example:** A2 contains `14/09/1992`. Today is 22 May 2026. The formula returns **33**, because the 34th birthday (14 September 2026) hasn't arrived yet.

## Age in Years, Months, and Days

To get a full breakdown, combine three DATEDIF calls:

```
=DATEDIF(A2, TODAY(), "Y") & " years, " &
 DATEDIF(A2, TODAY(), "YM") & " months, " &
 DATEDIF(A2, TODAY(), "MD") & " days"
```

With the same birthdate of 14 September 1992 and today's date of 22 May 2026, this returns:

**33 years, 8 months, 8 days**

The `YM` unit gives remaining months after complete years are accounted for. The `MD` unit gives remaining days after complete months within the final partial year. You never need to write the month-boundary logic yourself.

## Why DATEDIF Is Undocumented

Microsoft removed DATEDIF from Excel's official function documentation starting with Excel 2000, but the function has remained in every version since. It was inherited from Lotus 1-2-3 for compatibility. Because it's undocumented, Excel's formula autocomplete won't suggest it—you have to type the full function name manually. It works identically in Google Sheets and LibreOffice Calc.

## Alternative: YEARFRAC

If you want age as a decimal (useful for prorating things like insurance premiums or payroll), use `YEARFRAC`:

```
=YEARFRAC(A2, TODAY())
```

For the birthdate 14 September 1992 evaluated on 22 May 2026, this returns approximately **33.69**—meaning the person is 33.69 years old, or about 69% through their 34th year.

`YEARFRAC` accepts an optional third argument for day-count basis (0 = US 30/360, 1 = actual/actual, 3 = actual/365). For age calculations, basis 1 (actual/actual) is most accurate:

```
=YEARFRAC(A2, TODAY(), 1)
```

## Calculating Age as of a Specific Date

Replace `TODAY()` with a fixed date when you need age at a past or future point:

```
=DATEDIF(A2, DATE(2025,1,1), "Y")
```

This returns the person's age on 1 January 2025. The `DATE` function constructs a date from year, month, and day arguments, which is cleaner than typing a date string directly.

**Practical use:** An HR spreadsheet might calculate each employee's age as of the last day of the fiscal year to determine benefit eligibility, not as of today.

## Calculating Age for a List of People

If you have a column of birthdates (say, A2:A50), drag the formula down. Excel adjusts the row reference automatically:

```
Column A: Birthdate
Column B: =DATEDIF(A2, TODAY(), "Y")   → Age in years
Column C: =DATEDIF(A2, TODAY(), "YM")  → Remaining months
```

Select B2 and C2, then drag the fill handle down to B50 and C50. Each row picks up the correct birthdate from column A.

## Common Errors

**#NUM! error:** DATEDIF returns `#NUM!` if the start date is later than the end date. This happens when someone accidentally enters the dates in the wrong order. Wrap the formula in `IFERROR` to catch this:

```
=IFERROR(DATEDIF(A2, TODAY(), "Y"), "Check date")
```

**Date stored as text:** If your dates were imported from a CSV and Excel treats them as text, DATEDIF will return `#VALUE!`. Select the column, go to Data > Text to Columns, and confirm the date format to convert them to proper date values.

**Regional date formats:** Excel interprets date strings based on your system locale. `5/22/2026` means May 22 in the US but 22 May in many European systems—use the `DATE(year, month, day)` function or ISO format `2026-05-22` to avoid ambiguity.

## Age Brackets for Sorting or Filtering

To assign people to age groups, nest DATEDIF inside an IFS or nested IF:

```
=IFS(
  DATEDIF(A2,TODAY(),"Y") < 18, "Under 18",
  DATEDIF(A2,TODAY(),"Y") < 40, "18–39",
  DATEDIF(A2,TODAY(),"Y") < 65, "40–64",
  TRUE, "65+"
)
```

This is useful for survey analysis, insurance groupings, or any report where raw ages need to be bucketed.

## When a Calculator Is Faster

For one-off lookups—checking your own age, verifying someone's age quickly—the formulas above are more setup than they're worth. The [age calculator](/) gives you an instant breakdown in years, months, and days without opening a spreadsheet.

For more on this topic, see [*How to Calculate Age in Years, Months, and Days*](/blog/age-in-years-months-days).

Excel's DATEDIF shines when you need to process a column of dates in bulk, automate a report, or embed age logic inside a larger formula. For everything else, the manual method or an online tool is quicker.

## Quick Reference

```
Current age in years:              =DATEDIF(A2, TODAY(), "Y")
Full breakdown (text):             =DATEDIF(A2,TODAY(),"Y")&" yrs "&DATEDIF(A2,TODAY(),"YM")&" mo "&DATEDIF(A2,TODAY(),"MD")&" days"
Age as decimal:                    =YEARFRAC(A2, TODAY(), 1)
Age as of specific date:           =DATEDIF(A2, DATE(2025,12,31), "Y")
Total months lived:                =DATEDIF(A2, TODAY(), "M")
Total days lived:                  =DATEDIF(A2, TODAY(), "D")
```

These six formulas cover the vast majority of age-in-Excel use cases. Save this page and paste the one you need.
