---
title: "Time Zone Converter Guide: How to Convert Between Any Two Time Zones"
description: "A practical guide to converting time zones — including EST to PST, EST to GMT, EST to IST, and how DST and the Date Line affect your calculations."
publishDate: 2026-06-07
updatedDate: 2026-06-07
author: "Editorial Team"
tags: ["time zone converter", "time zones", "UTC offsets", "EST", "PST", "IST", "DST"]
draft: false
heroImage: "/images/blog/time-zone-converter-guide-hero.png"
---

Converting between time zones looks complicated at first, but it reduces to a single consistent method: convert to UTC first, then convert to the destination. Once you understand UTC offsets and a few seasonal caveats, you can work out any time zone math in your head. This guide covers the method, the most common conversions, the DST complications, and the Date Line.

## The Core Method: Use UTC as the Bridge

Every time zone is defined as an offset from Coordinated Universal Time (UTC). To convert between any two time zones:

1. Convert the source time to UTC by applying the source offset (add if behind UTC, subtract if ahead)
2. Convert the UTC time to the destination by applying the destination offset (subtract if behind UTC, add if ahead)

**Example**: It's 9 AM Eastern Standard Time (EST, UTC-5). What time is it in India (IST, UTC+5:30)?

- Step 1: 9:00 AM EST → add 5 hours → 14:00 UTC
- Step 2: 14:00 UTC → add 5 hours 30 minutes → 19:30 IST

Result: 9 AM EST = 7:30 PM IST.

This method works for any pair of time zones. The only variables are the offsets and whether DST is in effect.

For more on this topic, see [*What Is UTC? The Time Standard That Keeps the World in Sync*](/blog/what-is-utc).

## UTC Offsets for Major Time Zones

### United States

| Abbreviation | Full Name | Standard Offset | DST Offset |
|---|---|---|---|
| EST | Eastern Standard Time | UTC-5 | — |
| EDT | Eastern Daylight Time | — | UTC-4 |
| CST | Central Standard Time | UTC-6 | — |
| CDT | Central Daylight Time | — | UTC-5 |
| MST | Mountain Standard Time | UTC-7 | — |
| MDT | Mountain Daylight Time | — | UTC-6 |
| PST | Pacific Standard Time | UTC-8 | — |
| PDT | Pacific Daylight Time | — | UTC-7 |
| AKST | Alaska Standard Time | UTC-9 | — |
| AKDT | Alaska Daylight Time | — | UTC-8 |
| HST | Hawaii Standard Time | UTC-10 | (no DST) |

### Americas

| Abbreviation | Full Name | Offset |
|---|---|---|
| AST | Atlantic Standard Time (Canada) | UTC-4 |
| BRT | Brasília Time (Brazil) | UTC-3 |
| ART | Argentina Time | UTC-3 |
| COT | Colombia Time | UTC-5 |
| PET | Peru Time | UTC-5 |
| CLT | Chile Standard Time | UTC-3 (UTC-4 in winter) |

### Europe

| Abbreviation | Full Name | Standard Offset | DST Offset |
|---|---|---|---|
| GMT | Greenwich Mean Time (UK winter) | UTC+0 | — |
| BST | British Summer Time | — | UTC+1 |
| WET | Western European Time | UTC+0 | — |
| WEST | Western European Summer Time | — | UTC+1 |
| CET | Central European Time | UTC+1 | — |
| CEST | Central European Summer Time | — | UTC+2 |
| EET | Eastern European Time | UTC+2 | — |
| EEST | Eastern European Summer Time | — | UTC+3 |
| MSK | Moscow Standard Time | UTC+3 | (no DST since 2014) |

### Asia-Pacific

| Abbreviation | Full Name | Offset |
|---|---|---|
| IST | India Standard Time | UTC+5:30 (no DST) |
| NPT | Nepal Time | UTC+5:45 (no DST) |
| PKT | Pakistan Standard Time | UTC+5 (no DST) |
| BST | Bangladesh Standard Time | UTC+6 (no DST) |
| ICT | Indochina Time (Thailand, Vietnam) | UTC+7 (no DST) |
| CST | China Standard Time | UTC+8 (no DST) |
| SGT | Singapore Time | UTC+8 (no DST) |
| JST | Japan Standard Time | UTC+9 (no DST) |
| KST | Korea Standard Time | UTC+9 (no DST) |
| AEST | Australian Eastern Standard Time | UTC+10 |
| AEDT | Australian Eastern Daylight Time | UTC+11 |
| NZST | New Zealand Standard Time | UTC+12 |
| NZDT | New Zealand Daylight Time | UTC+13 |

## Common Conversions: EST to Other Time Zones

During **Eastern Standard Time** (EST, UTC-5, roughly November through mid-March):

| EST | UTC | PST (UTC-8) | CST (UTC-6) | GMT/UTC+0 | CET (UTC+1) | IST (UTC+5:30) | JST (UTC+9) |
|-----|-----|-------------|-------------|-----------|-------------|----------------|-------------|
| 12:00 AM | 5:00 AM | 9:00 PM (prev) | 11:00 PM (prev) | 5:00 AM | 6:00 AM | 10:30 AM | 2:00 PM |
| 6:00 AM | 11:00 AM | 3:00 AM | 5:00 AM | 11:00 AM | 12:00 PM | 4:30 PM | 8:00 PM |
| 9:00 AM | 2:00 PM | 6:00 AM | 8:00 AM | 2:00 PM | 3:00 PM | 7:30 PM | 11:00 PM |
| 12:00 PM | 5:00 PM | 9:00 AM | 11:00 AM | 5:00 PM | 6:00 PM | 10:30 PM | 2:00 AM (+1) |
| 5:00 PM | 10:00 PM | 2:00 PM | 4:00 PM | 10:00 PM | 11:00 PM | 3:30 AM (+1) | 7:00 AM (+1) |
| 8:00 PM | 1:00 AM (+1) | 5:00 PM | 7:00 PM | 1:00 AM (+1) | 2:00 AM (+1) | 6:30 AM (+1) | 10:00 AM (+1) |

*(+1) indicates the next calendar day*

During **Eastern Daylight Time** (EDT, UTC-4, roughly mid-March through November), subtract one less hour from EST to UTC — so 9 AM EDT = 1:00 PM UTC instead of 2:00 PM UTC, and all subsequent conversions shift accordingly.

## The DST Complication

Daylight Saving Time (DST) is the most common source of time zone conversion errors. The main issues:

**Different countries observe DST on different dates.** The US "springs forward" on the second Sunday in March and "falls back" on the first Sunday in November. The EU observes changes on the last Sunday in March and last Sunday in October. Australia observes it in the Southern Hemisphere autumn and spring, so their transitions are the inverse of the North.

**Many countries don't observe DST at all.** Japan, China, India, most of Africa, and most of Southeast Asia keep a fixed offset year-round. If you're converting between New York and Tokyo, the difference changes between 13 hours (EDT, UTC-4 vs JST UTC+9) and 14 hours (EST, UTC-5 vs JST UTC+9).

**The US-EU transition gap creates a moving target.** In mid-March, after the US springs forward but before the EU does, the difference between New York and London narrows by an hour. In late October after the EU falls back but before the US does, the same shrinkage recurs. During these windows — typically about a week each — any recurring scheduled call needs manual verification.

For more on this topic, see [*Daylight Saving Time Explained: Why It Exists and How It Works*](/blog/daylight-saving-time-explained).

For more on this topic, see [*EST vs EDT: What's the Difference and When Does Each Apply?*](/blog/est-vs-edt).

## The International Date Line

The International Date Line (IDL) runs roughly along the 180° meridian in the Pacific. When your conversion crosses the IDL, the calendar day changes:

- Traveling west across the IDL: you advance one calendar day
- Traveling east across the IDL: you go back one calendar day

**Example**: It's Monday 8:00 PM in New York (EST, UTC-5). What day and time is it in Auckland, New Zealand (NZDT, UTC+13 in austral summer)?

- 8:00 PM EST → add 5 hours → 1:00 AM Tuesday UTC
- 1:00 AM Tuesday UTC → add 13 hours → 2:00 PM Tuesday NZDT

The date here advances through UTC, not because of the IDL per se, but because the UTC time has crossed midnight. The IDL concept helps visualize why Auckland can be in a different calendar day from New York, but the UTC math handles the calculation correctly without needing to reason about the IDL directly.

## Quick Reference: How Many Hours Ahead or Behind?

| From / To | PST (UTC-8) | MST (UTC-7) | CST (UTC-6) | EST (UTC-5) | GMT (UTC+0) | CET (UTC+1) | IST (UTC+5:30) | CST (UTC+8) | JST (UTC+9) |
|-----------|-------------|-------------|-------------|-------------|-------------|-------------|----------------|-------------|-------------|
| PST | — | +1 | +2 | +3 | +8 | +9 | +13:30 | +16 | +17 |
| EST | -3 | -2 | -1 | — | +5 | +6 | +10:30 | +13 | +14 |
| GMT | -8 | -7 | -6 | -5 | — | +1 | +5:30 | +8 | +9 |
| IST | -13:30 | -12:30 | -11:30 | -10:30 | -5:30 | -4:30 | — | +2:30 | +3:30 |
| JST | -17 | -16 | -15 | -14 | -9 | -8 | -3:30 | +1 | — |

*Note: These are standard-time offsets. DST will shift applicable zones by ±1 hour.*

## When to Use a Live Converter

The tables above are reliable for standard and daylight time as currently defined, but time zone rules change. Countries occasionally shift their UTC offset, abolish DST, or temporarily observe a different rule. For any conversion where accuracy matters — a job interview, a business call, a legal deadline — use a live tool.

worldclock.io lets you pin any combination of cities and see their current local times simultaneously. You can type in a hypothetical time and see how it maps across all your pinned zones, accounting for today's actual DST status in each location. This is faster and more reliable than offset math when you're juggling multiple time zones at once.

The underlying principle is always the same: UTC is the common reference, offsets are additive, and DST is a seasonal adjustment that varies by jurisdiction. Once that mental model is in place, any converter — whether a tool or a calculation — becomes straightforward to use.
