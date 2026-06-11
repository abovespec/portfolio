---
title: "Cron Timezone Configuration: Handle Time Zones and DST Correctly"
description: "Learn how cron handles timezones, set TZ per job or globally, avoid DST issues, and understand why running cron jobs in UTC is the safest approach."
publishDate: 2026-06-07
updatedDate: 2026-06-07
author: "Editorial Team"
tags: ["cron", "timezone", "crontab", "UTC", "DST", "linux"]
draft: false
heroImage: "/images/blog/cron-timezone-hero.png"
---

Scheduling a cron job at "9 AM every weekday" sounds simple, but time zones introduce complexity that can cause jobs to run at the wrong time, fire twice, or be skipped entirely. This article explains how cron interprets time, how to configure time zones properly, and why UTC is usually the safest choice for production systems.

## How Cron Interprets Time

By default, cron uses the system's local timezone. When the cron daemon evaluates whether a job should run, it compares the current local time against the schedule expression. If your server is set to `America/New_York`, a cron entry of `0 9 * * 1-5` fires at 9 AM Eastern time.

This works fine until:
- Your server's timezone changes (common after a migration or misconfiguration).
- Daylight Saving Time transitions occur.
- Your team is distributed across time zones and members disagree on what "9 AM" means.

## Checking the System Timezone

Before configuring timezone-aware cron jobs, confirm what timezone your system is running:

```bash
# Modern systemd-based systems
timedatectl

# Output includes:
#    Local time: Sat 2026-06-07 09:00:00 EDT
#  Universal time: Sat 2026-06-07 13:00:00 UTC
#        RTC time: Sat 2026-06-07 13:00:00
#       Time zone: America/New_York (EDT, -0400)

# Check via /etc/localtime symlink
ls -la /etc/localtime
# /etc/localtime -> /usr/share/zoneinfo/America/New_York

# Check /etc/timezone (Debian/Ubuntu)
cat /etc/timezone
# America/New_York
```

## Setting the Timezone for All Jobs in a Crontab

Most modern cron implementations (Vixie cron, cronie, and their derivatives) support a `TZ` variable at the top of a crontab file. Setting it changes the timezone used to evaluate all job schedules in that file:

```crontab
TZ=America/New_York

# These jobs now fire at Eastern time regardless of system timezone
0 9 * * 1-5 /opt/scripts/morning-report.sh
0 17 * * 1-5 /opt/scripts/end-of-day-report.sh
```

This is useful when you want jobs to always fire at a specific local time for a particular region, even if the server is set to UTC.

## Setting the Timezone for a Single Job

Some cron implementations support setting `TZ` as an environment variable prefix on a single job line:

```crontab
# Only this job runs in Tokyo time
0 9 * * 1-5 TZ=Asia/Tokyo /opt/scripts/tokyo-report.sh

# This job still uses the crontab-level TZ or system default
0 9 * * 1-5 /opt/scripts/local-report.sh
```

Support for this syntax varies by cron implementation, so test it on your specific system. The safer approach is to create separate crontab sections with explicit `TZ=` headers.

## CRON_TZ: An Older Variable

Some cron implementations use `CRON_TZ` instead of or in addition to `TZ`:

```crontab
CRON_TZ=Europe/London

0 8 * * * /opt/scripts/london-open.sh
0 16 * * * /opt/scripts/london-close.sh
```

`CRON_TZ` is recognized by some versions of Vixie cron and cronie. If `TZ` does not work on your system, try `CRON_TZ`. For portability, prefer using `TZ` since it is the standard POSIX environment variable for timezone selection.

## The DST Problem

Daylight Saving Time transitions cause two specific failure modes:

### Jobs Run Twice

When clocks "fall back" by one hour (e.g., 2:00 AM becomes 1:00 AM), any job scheduled between 1:00 AM and 2:00 AM runs twice: once during the original pass through that hour and once when the clock repeats it.

Example: a job at `0 1 * * *` during the fall-back transition will fire at 1:00 AM standard time and again at 1:00 AM after the clock moves back.

### Jobs Are Skipped

When clocks "spring forward" by one hour (e.g., 2:00 AM becomes 3:00 AM), any job scheduled in the skipped hour simply never runs. A job at `0 2 * * *` will not fire at all on the spring-forward day.

### DST Transition Dates in 2026

For reference, in the United States in 2026:
- **Spring forward**: Sunday, March 8 at 2:00 AM (clocks move to 3:00 AM)
- **Fall back**: Sunday, November 1 at 2:00 AM (clocks move to 1:00 AM)

European transitions follow different dates.

## The UTC Recommendation

The most reliable solution to all timezone and DST problems is to configure cron jobs to run in UTC. UTC never observes Daylight Saving Time, so there is never a skipped hour or a repeated hour.

Set the crontab timezone to UTC:

```crontab
TZ=UTC

# These run at fixed UTC times — no DST surprises
0 1 * * * /opt/scripts/nightly-backup.sh
0 14 * * 1-5 /opt/scripts/afternoon-report.sh
```

Or set the system timezone to UTC:

```bash
timedatectl set-timezone UTC
```

When you run in UTC and need to schedule something at "9 AM New York time", convert the UTC offset manually. During EST (UTC-5): 9 AM EST = 14:00 UTC. During EDT (UTC-4): 9 AM EDT = 13:00 UTC. You will need two crontab entries if you want to adjust for the seasonal shift — or just pick a time that doesn't matter if it drifts by an hour.

## Practical Examples for Multiple Timezones

Suppose you manage jobs for three regions and your server is in UTC:

```crontab
TZ=UTC

# New York business day open (14:00 UTC in summer / 15:00 UTC in winter)
# Using 14:00 UTC — accepts ~1 hour drift for DST transitions
0 14 * * 1-5 /opt/scripts/ny-open.sh

# London business day close (16:00 UTC in BST / 17:00 UTC in GMT)
0 17 * * 1-5 /opt/scripts/london-close.sh

# Tokyo morning report (00:00 UTC = 09:00 JST, JST is UTC+9 with no DST)
0 0 * * 1-5 /opt/scripts/tokyo-morning.sh
```

Japan Standard Time (JST) is UTC+9 and does not observe DST, making it one of the easiest timezones to schedule for.

## Scheduling Timezone-Sensitive Jobs: A Template

When building a timezone-sensitive cron job:

1. Decide on a canonical timezone for the job (UTC recommended).
2. Set `TZ=` at the top of the relevant crontab section.
3. Convert your intended local time to UTC using a world clock.
4. Account for DST if the local timezone observes it (document the UTC equivalents for both summer and winter).
5. Test around DST transition weekends.

```crontab
# === Jobs that run in UTC (no DST) ===
TZ=UTC
0 6 * * * /opt/scripts/global-morning-sync.sh

# === Jobs synchronized to US Eastern Time ===
# NOTE: 14:00 UTC = 10:00 AM EDT (summer), 09:00 AM EST (winter)
# Acceptable 1-hour drift for this report
TZ=UTC
0 14 * * 1-5 /opt/scripts/us-east-report.sh
```

## systemd Timers and Timezones

If you are using systemd timers instead of cron, the `OnCalendar` directive evaluates times in the local system timezone by default. Set the `[Timer]` section's time in UTC explicitly by using the `z` suffix, or ensure the system is set to UTC:

```ini
[Timer]
# Explicitly UTC time using the z suffix
OnCalendar=*-*-* 02:00:00 UTC
```

This is more explicit than cron's `TZ` variable and less ambiguous.

## Build Your Schedule at crontab.io

Timezone math is error-prone, especially when accounting for DST. [crontab.io](https://crontab.io) provides an interactive cron expression builder that shows you upcoming scheduled times clearly, making it easy to verify that an expression fires when you intend before adding it to your crontab. Check your UTC expressions there before deployment to avoid off-by-one-hour bugs that only manifest twice a year.

## Summary

Cron uses the system timezone by default. Set `TZ=` or `CRON_TZ=` in your crontab to specify a different timezone for all or specific jobs. DST transitions cause jobs in non-UTC timezones to fire twice (fall back) or be skipped (spring forward). The safest approach for production systems is to run all cron jobs in UTC, where no DST transitions occur and times are unambiguous. Convert local times to UTC at schedule setup time and document the conversion for your team.
