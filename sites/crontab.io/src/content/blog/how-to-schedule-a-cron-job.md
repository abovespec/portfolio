---
title: "How to Schedule a Cron Job on Linux: Step-by-Step"
description: "Learn how to schedule cron jobs on Linux using crontab -e. Covers editing the crontab, setting PATH, running scripts, logging output, and verifying jobs run."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["cron", "crontab", "linux", "automation", "scheduling"]
draft: false
---

Cron lets you automate recurring tasks on Linux — from database backups to report generation to cache clearing. This guide walks through creating your first cron job and getting it to run reliably.

## Prerequisites

Verify cron is running:

```bash
systemctl status cron        # Debian/Ubuntu (cronie or cron)
systemctl status crond       # CentOS/RHEL
```

If it's not running:

```bash
sudo systemctl enable cron
sudo systemctl start cron
```

## Step 1: Open your crontab for editing

```bash
crontab -e
```

This opens your user's crontab file in the default editor (usually `vi` or `nano`). Each line is a scheduled job.

**To use a different editor:**

```bash
EDITOR=nano crontab -e
```

Or set it permanently:

```bash
export VISUAL=nano
```

## Step 2: Write the cron expression

The format is five time fields followed by the command:

```
MINUTE HOUR DOM MONTH DOW COMMAND
```

Example — run a backup script every day at 2am:

```bash
0 2 * * * /home/ubuntu/backup.sh
```

Example — run a Python script every 15 minutes:

```bash
*/15 * * * * /usr/bin/python3 /home/ubuntu/scripts/sync.py
```

## Step 3: Use full paths for everything

Cron runs with a minimal PATH (`/usr/bin:/bin`). Commands in your shell might not be found in cron. Use full paths:

```bash
# Check where a command lives
which python3
# /usr/bin/python3

which node
# /usr/local/bin/node
```

Then use those full paths in your crontab:

```bash
*/15 * * * * /usr/bin/python3 /home/ubuntu/scripts/sync.py >> /var/log/sync.log 2>&1
```

Or set PATH at the top of your crontab (before any job lines):

```bash
PATH=/usr/local/bin:/usr/bin:/bin
HOME=/home/ubuntu

*/15 * * * * python3 /home/ubuntu/scripts/sync.py >> /var/log/sync.log 2>&1
```

## Step 4: Handle output

By default, cron emails output to the local user. To manage output:

```bash
# Suppress everything (silent)
0 2 * * * /home/ubuntu/backup.sh > /dev/null 2>&1

# Log to a file
0 2 * * * /home/ubuntu/backup.sh >> /var/log/backup.log 2>&1

# Log with timestamp
0 2 * * * echo "$(date) - starting backup" >> /var/log/backup.log && /home/ubuntu/backup.sh >> /var/log/backup.log 2>&1
```

## Step 5: Save and verify

Save and exit the editor. Cron will automatically install the new crontab.

List your active cron jobs:

```bash
crontab -l
```

To see the cron daemon's own logs:

```bash
# Debian/Ubuntu
grep CRON /var/log/syslog | tail -20

# CentOS/RHEL
grep CRON /var/log/cron | tail -20
```

## Complete examples

**Daily database backup at 3am:**

```bash
0 3 * * * /usr/bin/pg_dump -U postgres mydb > /backups/mydb-$(date +\%Y\%m\%d).sql 2>> /var/log/backup.log
```

Note: `%` must be escaped as `\%` in crontab (unescaped `%` is interpreted as a newline).

**Clear application cache every hour:**

```bash
0 * * * * /usr/bin/php /var/www/html/artisan cache:clear >> /var/log/cache.log 2>&1
```

**Check disk usage every 10 minutes and alert if over 80%:**

```bash
*/10 * * * * /usr/local/bin/check-disk.sh
```

`/usr/local/bin/check-disk.sh`:
```bash
#!/bin/bash
USAGE=$(df / | tail -1 | awk '{print $5}' | tr -d '%')
if [ "$USAGE" -gt 80 ]; then
    echo "Disk usage at ${USAGE}%" | mail -s "Disk Alert" admin@example.com
fi
```

**Run on startup:**

```bash
@reboot sleep 30 && /home/ubuntu/start-worker.sh >> /var/log/worker.log 2>&1
```

The `sleep 30` gives the system time to fully boot before the script starts.

## Running as root

To schedule a system-level job (as root):

```bash
sudo crontab -e
```

Or add it to `/etc/crontab`, which has an extra user field:

```bash
# /etc/crontab format: MINUTE HOUR DOM MONTH DOW USER COMMAND
0 2 * * * root /usr/local/bin/backup.sh
```

## Verifying it ran

Check the cron log after the scheduled time:

```bash
grep CRON /var/log/syslog | grep backup
```

Output looks like:
```
Apr 25 02:00:01 hostname CRON[12345]: (ubuntu) CMD (/home/ubuntu/backup.sh)
```

If you don't see it, double-check the expression, confirm cron is running, and make sure your user has permission to run the command.

Build and validate cron expressions at [crontab.io](/).
