---
title: "PST vs PDT: Pacific Time Explained"
description: "PST is UTC-8 and PDT is UTC-7. Here's when each applies, which states observe Pacific Time, and why 'PT' is often the clearest term to use."
publishDate: 2026-06-07
updatedDate: 2026-06-07
author: "Editorial Team"
tags: ["PST", "PDT", "Pacific Time", "time zones", "DST", "California"]
draft: false
---

If you've ever seen a product launch announced for "10 AM PST" in April and felt confused — PST isn't active in April — you've encountered one of the most common time zone errors in US tech and entertainment, where Pacific Time reigns but the abbreviations get muddled constantly. PST and PDT are not interchangeable. Here's what each one means, when it applies, and how to use the right term.

## PST: Pacific Standard Time

PST stands for Pacific Standard Time. It is a fixed UTC offset of UTC-8, meaning the Pacific US and Canada are eight hours behind Coordinated Universal Time when standard time is in effect.

PST applies from the first Sunday in November through the second Sunday in March. During this period, the Pacific states are at their "standard" offset. If it's 12:00 PM UTC noon on a December day, it's 4:00 AM PST on the West Coast.

PST is active for roughly four months of the year — from early November to mid-March. That's significantly less than half the year.

For more on this topic, see [*What Is UTC? The Time Standard That Keeps the World in Sync*](/blog/what-is-utc).

## PDT: Pacific Daylight Time

PDT stands for Pacific Daylight Time. It is a fixed UTC offset of UTC-7, meaning the Pacific region is seven hours behind UTC when daylight saving time is in effect.

PDT applies from the second Sunday in March through the first Sunday in November. In 2026, that means PDT began on March 8 and will end on November 1. During this window — roughly eight months — the Pacific Coast is at UTC-7 rather than UTC-8.

The practical result: if it's 12:00 PM UTC noon on a July afternoon, it's 5:00 AM PDT in Los Angeles. If you calculated using PST (UTC-8), you'd get 4:00 AM — an hour off.

Because PDT covers eight of twelve months, it is actually the *dominant* Pacific time for most of the calendar year. The persistent use of "PST" as a year-round catch-all is technically wrong about 67% of the time.

## The Transition Dates in 2026

The US transitions between standard and daylight time on specific Sundays, at 2:00 AM local time:

- **Spring forward (PST → PDT)**: Sunday, March 8, 2026. At 2:00 AM PST, clocks jumped to 3:00 AM PDT. One hour was "lost."
- **Fall back (PDT → PST)**: Sunday, November 1, 2026. At 2:00 AM PDT, clocks will fall to 1:00 AM PST. One hour will be "gained."

These dates are set by federal law (the Uniform Time Act of 1966, amended in 2005). They apply uniformly to all US states that observe daylight saving time.

For more on this topic, see [*Spring Forward, Fall Back: The DST Mnemonic and What It Actually Means*](/blog/spring-forward-fall-back).

## Which States Observe Pacific Time?

The following US states are in the Pacific Time Zone and observe both PST and PDT:

- **California** — the most populous Pacific state; Los Angeles, San Francisco, San Diego
- **Washington** — Seattle, Spokane, Olympia
- **Oregon** — Portland, Salem, Eugene (with one notable exception below)
- **Nevada** — Las Vegas, Reno

**The Oregon exception**: Most of Oregon is on Pacific Time, but Malheur County in the far eastern corner of the state observes Mountain Time (MST/MDT) because it's economically and geographically integrated with Idaho.

**Idaho**: Most of Idaho is on Mountain Time, but the north of the state (Coeur d'Alene, Moscow) is on Pacific Time, for similar economic connectivity reasons with eastern Washington and Spokane.

**Parts of Nevada**: All of Nevada observes Pacific Time. This includes Las Vegas, which is geographically farther east than Los Angeles but chose Pacific alignment for tourism and economic reasons.

In Canada, the Pacific Time Zone covers British Columbia (including Vancouver and Victoria) and small parts of the Yukon near the BC border.

## Are There Pacific Zone States That Don't Observe DST?

In the continental US, no state in the Pacific Time Zone refuses DST. All four states — California, Washington, Oregon, and Nevada — observe both PST and PDT.

This is notable because there have been legislative efforts, particularly in California (Proposition 7, passed by voters in 2018), to authorize year-round daylight saving time. However, implementing year-round DST in the US requires an act of Congress — states can't unilaterally adopt it. As of 2026, this change has not been enacted federally, so California and the other Pacific states continue switching between PST and PDT.

Contrast this with **Arizona**, which is in the Mountain Time Zone and does *not* observe daylight saving time. Arizona stays on Mountain Standard Time (MST, UTC-7) year-round. During the DST period, when Mountain Daylight Time (MDT, UTC-6) is in effect in other Mountain states, Arizona effectively lines up with Pacific Daylight Time (PDT, also UTC-7) rather than its Mountain Zone neighbors.

**The Navajo Nation exception**: The Navajo Nation, which spans parts of Arizona, Utah, and New Mexico, does observe DST, creating an enclave within Arizona that temporarily shifts to UTC-6 in summer. The Hopi Reservation, which is entirely surrounded by the Navajo Nation within Arizona, does not observe DST, creating nested zones within the same state.

For more on this topic, see [*US Time Zones Explained: All 6 and What States They Cover*](/blog/us-time-zones).

## "PT" as the Umbrella Term

The cleanest way to refer to Pacific time without specifying whether it's standard or daylight is to use **PT** — Pacific Time. PT is season-agnostic: it means "whichever offset the Pacific zone is currently observing," which is UTC-8 in winter and UTC-7 in summer.

Many tech companies, TV networks, and event organizers in the Pacific region use PT for this reason. "The keynote starts at 10:00 AM PT" is correct regardless of what month the keynote falls in — the offset will be whatever Pacific Time happens to be on that date.

If you need to specify the exact UTC offset (for international conversions, API documentation, or technical scheduling), be explicit:

- "10:00 AM UTC-8" in January is unambiguous
- "10:00 AM UTC-7" in July is unambiguous
- "10:00 AM PST" in July is technically wrong (PST is not active in July)
- "10:00 AM PT" in July is correct if you mean whatever Pacific time is in effect

## PST and PDT Conversions at a Glance

| Pacific Time | UTC | EST/EDT | GMT | CET/CEST | IST | JST |
|---|---|---|---|---|---|---|
| 6:00 AM PST | 2:00 PM | 9:00 AM EST | 2:00 PM | 3:00 PM CET | 7:30 PM | 11:00 PM |
| 9:00 AM PST | 5:00 PM | 12:00 PM EST | 5:00 PM | 6:00 PM CET | 10:30 PM | 2:00 AM (+1) |
| 12:00 PM PST | 8:00 PM | 3:00 PM EST | 8:00 PM | 9:00 PM CET | 1:30 AM (+1) | 5:00 AM (+1) |
| 5:00 PM PST | 1:00 AM (+1) | 8:00 PM EST | 1:00 AM (+1) | 2:00 AM (+1) | 6:30 AM (+1) | 10:00 AM (+1) |

*(PST = UTC-8, EST = UTC-5, CET = UTC+1, IST = UTC+5:30, JST = UTC+9)*

| Pacific Time | UTC | EST/EDT | GMT | CET/CEST | IST | JST |
|---|---|---|---|---|---|---|
| 6:00 AM PDT | 1:00 PM | 9:00 AM EDT | 1:00 PM | 3:00 PM CEST | 6:30 PM | 10:00 PM |
| 9:00 AM PDT | 4:00 PM | 12:00 PM EDT | 4:00 PM | 6:00 PM CEST | 9:30 PM | 1:00 AM (+1) |
| 12:00 PM PDT | 7:00 PM | 3:00 PM EDT | 7:00 PM | 9:00 PM CEST | 12:30 AM (+1) | 4:00 AM (+1) |
| 5:00 PM PDT | 12:00 AM (+1) | 8:00 PM EDT | 12:00 AM (+1) | 2:00 AM (+1) | 5:30 AM (+1) | 9:00 AM (+1) |

*(PDT = UTC-7, EDT = UTC-4, CEST = UTC+2, IST = UTC+5:30, JST = UTC+9)*

## Quick Reference

| Abbreviation | Full Name | UTC Offset | Active Period (2026) |
|---|---|---|---|
| PST | Pacific Standard Time | UTC-8 | Nov 1 – Mar 8 |
| PDT | Pacific Daylight Time | UTC-7 | Mar 8 – Nov 1 |
| PT | Pacific Time | UTC-8 or UTC-7 | Year-round (safe umbrella) |

## Using a World Clock for Pacific Time

When you're working with colleagues or customers in the Pacific time zone from elsewhere in the US or internationally, the cleanest approach is to use a live world clock. worldclock.io lets you pin Pacific Time alongside any other zone and see the current local time on both sides of the equation — no manual offset arithmetic required, and no risk of using PST when it's actually PDT.

The PST/PDT distinction matters most in international contexts. When converting Pacific time to IST, JST, or AEST for colleagues in Asia or Australia, a one-hour error from using the wrong Pacific offset compounds with whatever DST situation exists in the destination zone. Getting it right means knowing which abbreviation is active — or skipping the abbreviations entirely and working in UTC or a live tool.
