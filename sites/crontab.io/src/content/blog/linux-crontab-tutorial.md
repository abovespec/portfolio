---
title: "Linux Crontab Tutorial: From Basics to Real Automation"
description: "Complete Linux crontab tutorial for beginners. Learn to create, edit, list, and remove cron jobs. Covers syntax, environment setup, logging, and practical examples."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["cron", "crontab", "linux", "tutorial", "automation", "sysadmin"]
draft: false
---

Cron is Linux's built-in task scheduler. It runs commands at scheduled times — automatically, without you having to be logged in. This tutorial covers everything from your first cron job to reliable production automation.

## What is cron?

The `cron` daemon is a background process that wakes up every minute, checks for scheduled jobs, and runs any that are due. Each user (including root) has their own crontab file that lists their jobs.

The crontab (cron table) is a configuration file with lines in the format:

```
MINUTE HOUR DAY_OF_MONTH MONTH DAY_OF_WEEK COMMAND
```

A `*` in a field means "any value."

## Your first cron job

**Step 1:** Open your crontab:

```bash
crontab -e
```

**Step 2:** Add a job. This runs a script every day at 2am:

```bash
0 2 * * * /home/ubuntu/backup.sh >> /var/log/backup.log 2>&1
```

**Step 3:** Save and exit. Cron installs the file automatically.

**Step 4:** Verify it was saved:

```bash
crontab -l
```

## Crontab commands reference

```bash
crontab -e      # Edit your crontab (opens in $EDITOR)
crontab -l      # List your current cron jobs
crontab -r      # Remove all your cron jobs (dangerous!)
crontab -u user # Edit another user's crontab (as root)
sudo crontab -e # Edit root's crontab
```

## The 5 time fields explained

```
┌──────── Minute (0-59)
│ ┌────── Hour (0-23)
│ │ ┌──── Day of month (1-31)
│ │ │ ┌── Month (1-12 or Jan-Dec)
│ │ │ │ ┌ Day of week (0-7, 0 and 7 = Sunday, or Mon-Sun)
│ │ │ │ │
* * * * * command
```

**Special characters:**
- `*` — every value
- `,` — list: `1,15` means 1st and 15th
- `-` — range: `1-5` means 1 through 5
- `/` — step: `*/5` means every 5 units

## Common schedules

```bash
# Every minute (for testing — remove when done)
* * * * * /script.sh

# Every 5 minutes
*/5 * * * * /script.sh

# Every hour at :00
0 * * * * /script.sh

# Daily at midnight
0 0 * * * /script.sh

# Daily at 3am
0 3 * * * /script.sh

# Weekdays at 9am
0 9 * * 1-5 /script.sh

# Every Sunday at 4am
0 4 * * 0 /script.sh

# First day of each month at midnight
0 0 1 * * /script.sh

# On reboot
@reboot /script.sh
```

## Write a proper cron script

Scripts called from cron need to be self-contained:

```bash
#!/bin/bash
# /home/ubuntu/backup.sh

# Set strict error handling
set -euo pipefail

# Use absolute paths — cron doesn't have your PATH
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
BACKUP_DIR="/var/backups/db"
PG_DUMP="/usr/bin/pg_dump"
GZIP="/bin/gzip"

mkdir -p "$BACKUP_DIR"

$PG_DUMP -U postgres myapp | $GZIP > "$BACKUP_DIR/myapp-$TIMESTAMP.sql.gz"

# Keep only last 7 days
find "$BACKUP_DIR" -name "*.sql.gz" -mtime +7 -delete

echo "Backup completed: $BACKUP_DIR/myapp-$TIMESTAMP.sql.gz"
```

Make it executable:

```bash
chmod +x /home/ubuntu/backup.sh
```

Add to crontab:

```bash
0 2 * * * /home/ubuntu/backup.sh >> /var/log/backup.log 2>&1
```

## Handling environment variables

Cron doesn't load `.bashrc` or `.bash_profile`. Environment variables your script needs must be set explicitly.

**Option 1: Set variables in the crontab:**

```bash
PATH=/usr/local/bin:/usr/bin:/bin
MAILTO=""
DB_PASS=secret

0 2 * * * /home/ubuntu/backup.sh
```

**Option 2: Load a file in the script:**

```bash
#!/bin/bash
set -a
source /etc/app.env    # file with KEY=VALUE lines
set +a

# now use $DB_PASS, $API_KEY, etc.
```

**Option 3: Source the user profile:**

```bash
#!/bin/bash
source /home/ubuntu/.profile
```

## Managing output

```bash
# Discard all output (jobs that emit nothing don't need this)
*/5 * * * * /script.sh > /dev/null 2>&1

# Log stdout, discard stderr
*/5 * * * * /script.sh >> /var/log/myjob.log

# Log everything (recommended during development)
*/5 * * * * /script.sh >> /var/log/myjob.log 2>&1

# Add timestamp to each log entry
*/5 * * * * echo "=== $(date) ===" >> /var/log/myjob.log && /script.sh >> /var/log/myjob.log 2>&1
```

## System-wide cron files

Beyond user crontabs, cron reads these system files:

| File/Dir | Purpose |
|---------|---------|
| `/etc/crontab` | System-wide crontab (has extra user field) |
| `/etc/cron.d/` | Drop-in crontab files for packages |
| `/etc/cron.hourly/` | Scripts run hourly (via run-parts) |
| `/etc/cron.daily/` | Scripts run daily |
| `/etc/cron.weekly/` | Scripts run weekly |
| `/etc/cron.monthly/` | Scripts run monthly |

The `/etc/crontab` format adds a username field:

```bash
# /etc/crontab
0 2 * * * root /usr/local/bin/backup.sh
```

## Verifying jobs run

Check cron's log after the scheduled time:

```bash
grep CRON /var/log/syslog | grep script | tail -10

# journald systems
journalctl -u cron --since "2026-04-25 02:00" | head -20
```

For important jobs, add monitoring. Services like Healthchecks.io let you ping a URL from cron to confirm the job ran:

```bash
0 2 * * * /home/ubuntu/backup.sh && curl -fsS https://hc-ping.com/YOUR-UUID > /dev/null 2>&1
```

If the job doesn't ping within the expected window, you get alerted.

Build and test cron schedules at [crontab.io](/).
