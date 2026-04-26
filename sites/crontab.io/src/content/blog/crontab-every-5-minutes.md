---
title: "Crontab Every 5 Minutes (and Other Intervals Explained)"
description: "Learn crontab syntax for running jobs every 5 minutes, every 10, 15, 30, and 60 minutes. Understand step values and interval scheduling with examples."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["cron", "crontab", "cron interval", "every 5 minutes", "scheduling"]
draft: false
---

Scheduling jobs at fixed intervals is the most common cron use case. Here's how interval scheduling works in cron, with ready-to-use expressions for every common interval.

## How interval scheduling works

Cron uses the `/` (slash) character to specify step values. `*/5` in the minutes field means "every 5 minutes starting from 0":

```
*/5 * * * * /script.sh
```

This runs at: 0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55 — every hour, all day.

The pattern `*/N` always starts from 0. You can't say "starting from 3" cleanly in standard cron — you'd need a list or an external check.

## Every N minutes

```bash
# Every 1 minute
* * * * * /script.sh

# Every 2 minutes
*/2 * * * * /script.sh

# Every 5 minutes
*/5 * * * * /script.sh

# Every 10 minutes
*/10 * * * * /script.sh

# Every 15 minutes
*/15 * * * * /script.sh

# Every 20 minutes
*/20 * * * * /script.sh

# Every 30 minutes
*/30 * * * * /script.sh
```

## Every N hours

```bash
# Every hour (at :00)
0 * * * * /script.sh

# Every 2 hours
0 */2 * * * /script.sh

# Every 3 hours
0 */3 * * * /script.sh

# Every 4 hours
0 */4 * * * /script.sh

# Every 6 hours
0 */6 * * * /script.sh

# Every 8 hours
0 */8 * * * /script.sh

# Every 12 hours
0 */12 * * * /script.sh
```

## Why `*/5` runs 12 times per hour

`*/5` means "all values from 0 to 59 where the value is divisible by 5":
```
0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55
```

That's 12 values, so the job runs 12 times per hour × 24 hours = 288 times per day.

## Common mistake: minutes vs. hours

This is wrong — it runs every 5 hours (not every 5 minutes):

```bash
# Wrong: 5 in the hours field
0 */5 * * * /script.sh     # runs at 00:00, 05:00, 10:00, 15:00, 20:00
```

This is correct for every 5 minutes:

```bash
# Correct: 5 in the minutes field
*/5 * * * * /script.sh
```

## Restrict intervals to specific hours

Run every 5 minutes, but only during business hours:

```bash
# Every 5 minutes, 9am to 5pm
*/5 9-17 * * * /script.sh

# Every 15 minutes during business hours, weekdays only
*/15 9-17 * * 1-5 /script.sh
```

## Sub-minute intervals: not supported in standard cron

Standard cron has a 1-minute resolution. You can't schedule something every 10 seconds in a crontab.

For sub-minute scheduling:

```bash
# Workaround: run multiple times in a single cron invocation
* * * * * /script.sh; sleep 30; /script.sh
```

This runs every 30 seconds (roughly). It's fragile — if the first invocation takes more than 30 seconds, the second starts late.

For true sub-minute scheduling, use a process supervisor (systemd timer with `OnUnitActiveSec`, supervisor, or an application-level scheduler like APScheduler).

## Combine interval with specific times

```bash
# Every 5 minutes starting at noon
0,5,10,15,20,25,30,35,40,45,50,55 12 * * * /script.sh
# Or equivalently:
*/5 12 * * * /script.sh

# Every 10 minutes between 8am and 10am
*/10 8-10 * * * /script.sh
```

## Real-world examples for 5-minute jobs

```bash
# Health check ping every 5 minutes
*/5 * * * * curl -fsS https://hc-ping.com/YOUR_UUID > /dev/null 2>&1

# Queue worker: process jobs every 5 minutes
*/5 * * * * /usr/bin/php /var/www/html/artisan queue:work --once >> /var/log/queue.log 2>&1

# Sync data from external API every 5 minutes
*/5 * * * * /usr/bin/python3 /opt/sync/fetch.py >> /var/log/sync.log 2>&1

# Update IP whitelist every 5 minutes
*/5 * * * * /usr/local/bin/update-firewall.sh >> /var/log/firewall.log 2>&1

# Monitor disk space every 10 minutes
*/10 * * * * /usr/local/bin/check-disk.sh
```

Build and test your cron schedule at [crontab.io](/).
