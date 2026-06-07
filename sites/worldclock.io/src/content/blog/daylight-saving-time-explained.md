---
title: "Daylight Saving Time Explained: Why It Exists and How It Works"
description: "Daylight saving time shifts clocks forward in spring and back in fall. Here's the real history, which countries use it, and why software engineers dread it."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["daylight saving time", "DST", "time zones", "clocks", "scheduling"]
draft: false
---

Twice a year, clocks change and people complain. The mechanics of daylight saving time are simple — you move clocks forward or back by one hour — but the reasons it exists, the uneven way it's applied around the world, and the very real technical problems it causes are worth understanding properly.

## A Brief, Accurate History

The idea of adjusting clocks to make better use of daylight has been attributed to Benjamin Franklin, but this is only partially accurate. Franklin wrote a satirical letter in 1784 suggesting Parisians could save candles by waking earlier — but he proposed no clock changes, and the letter was largely a joke.

The first practical implementation of daylight saving time came during World War I. Germany and its allies moved clocks forward in April 1916 to reduce coal consumption by shortening the period of evening artificial lighting. Britain followed weeks later. The wartime practice spread across several countries, then was largely abandoned when the war ended.

For more on this topic, see [*How to Schedule Meetings Across Time Zones Without the Confusion*](/blog/how-to-schedule-meetings-across-time-zones).

A second wave came during World War II, again for energy conservation reasons. After the war, practices diverged wildly — in the US, states and even cities could individually choose whether to observe DST and when to switch, creating a patchwork of local times that made interstate scheduling chaotic. The US Uniform Time Act of 1966 standardized the transition dates nationally, though it still allowed states to opt out entirely.

For more on this topic, see [*US Time Zones Explained: All 6 and What States They Cover*](/blog/us-time-zones).

## How It Works: Spring Forward, Fall Back

The phrase "spring forward, fall back" is a useful mnemonic:

- **In spring**, clocks move forward by one hour. In the US, this happens at 2:00 AM on the second Sunday in March. At that moment, clocks jump directly from 2:00 AM to 3:00 AM — one hour disappears. The day feels shorter; it also means that in the days after the transition, sunsets happen noticeably later in the evening.

- **In fall**, clocks move back by one hour. In the US, this happens at 2:00 AM on the first Sunday in November. At that moment, clocks fall from 2:00 AM back to 1:00 AM — that hour repeats. The day feels longer; sunrises come earlier, and evenings get darker sooner.

In the European Union, the transition dates are slightly different: clocks spring forward on the last Sunday of March and fall back on the last Sunday of October.

The US and EU transitions don't happen on the same day, which creates a window each spring and autumn where the offset between Eastern US time and Western European time is temporarily one hour different from its usual value. This frequently trips up international scheduling during those transition weeks.

## Which Countries Observe DST and Which Don't

Daylight saving time is not universal. Adoption breaks down roughly as follows:

**Countries that observe DST**: The US (most states), Canada (most provinces), the EU member states, the UK, Australia (most states), New Zealand, and a number of others.

**Countries that do not observe DST**: Japan, China, India, most of Africa, most of Southeast Asia, Iceland, and much of the Middle East. Japan dropped the practice after World War II and has never reinstated it. China uses a single time zone (UTC+8) nationwide and makes no seasonal adjustment.

**US exceptions**: Arizona observes Mountain Standard Time year-round and does not participate in DST — with the exception of the Navajo Nation, which does observe DST within Arizona's borders. Hawaii also doesn't observe DST, keeping Hawaii Standard Time (UTC-10) throughout the year.

**EU changes**: The European Union voted in 2019 to abolish mandatory clock changes, with each member state permitted to choose whether to permanently adopt summer time or winter time. However, implementation has been repeatedly delayed, and as of 2026 EU member states are still changing clocks biannually.

## Why Some People Want to Abolish It

The original justification for DST — energy savings — has been scrutinized more carefully in recent decades. Modern studies on energy consumption are mixed at best, with some finding that heating and cooling costs actually increase when clocks shift, offsetting any savings from reduced evening lighting.

Health researchers have also documented that the spring transition in particular is associated with short-term increases in heart attacks, traffic accidents, and workplace injuries in the days after the clock change — effects attributed to disrupted sleep.

The argument for keeping DST often comes down to evening recreation: longer daylit evenings in summer are genuinely valued by many people, particularly in higher latitudes where the difference in daylight hours between seasons is more dramatic. This doesn't require clock changes, though — it could be achieved just as well by permanently adopting summer time (i.e., year-round UTC-4 for Eastern states rather than switching between UTC-5 and UTC-4).

For more on this topic, see [*EST vs EDT: What's the Difference and When Does Each Apply?*](/blog/est-vs-edt).

## The Software Engineering Nightmare

For software developers, DST is a perennial source of bugs. The most infamous problem is the "repeated hour" that occurs when clocks fall back.

When clocks roll back from 2:00 AM to 1:00 AM, every time between 1:00 AM and 2:00 AM occurs twice. A log entry timestamped at 1:30 AM could refer to either of two distinct moments. If your application stores timestamps in local time, those records are ambiguous during this window.

The standard solution is to store all timestamps internally in UTC and convert to local time only for display purposes. UTC has no repeated hours, no skipped hours, and no seasonal ambiguity whatsoever.

The "skipped hour" from the spring transition creates a complementary problem: any time between 2:00 AM and 3:00 AM on the transition date doesn't exist in local time. If a scheduled job is set to run at 2:30 AM, it either runs an hour early, runs an hour late, or doesn't run at all — depending on how the scheduling system handles the gap. Well-engineered systems either schedule relative to UTC or include explicit handling for the DST transition.

Beyond the repeated/missing hour problem, DST introduces ongoing complexity in date arithmetic. "24 hours from now" and "tomorrow at the same time" can differ by an hour near a transition if your code isn't careful about which it intends.

## Practical Tips for Scheduling During Transitions

If you're managing any cross-region scheduling — meetings, automated jobs, reminders, delivery windows — around the spring and fall transition weeks:

- **Use UTC for internal scheduling**. Convert to local time for display, but let UTC be the anchor.
- **Double-check recurring events** the week of each transition. A standing meeting at "9 AM ET" will usually auto-adjust in calendar apps, but manual coordination can slip.
- **Remember the US/EU gap**. From the second Sunday of March to the last Sunday of March each spring, and from the last Sunday of October to the first Sunday of November each fall, the standard US-to-EU offset doesn't hold.
- **Look up Arizona and Hawaii separately** when scheduling with US colleagues, since those states have fixed offsets year-round.

DST isn't going away soon, despite ongoing debate. Until it does, a world clock that shows current times across all relevant zones — not the offsets you memorized six months ago — is the most reliable tool for staying accurate through the transitions.
