---
title: "systemd Timer vs Cron: Which Should You Use?"
description: "Compare systemd timers and traditional cron jobs. Learn the syntax, advantages of each, when to choose one over the other, and how to migrate."
publishDate: 2026-06-07
updatedDate: 2026-06-07
author: "Editorial Team"
tags: ["systemd", "cron", "crontab", "linux", "scheduling"]
draft: false
---

Most Linux systems today ship with both `cron` and `systemd`, and both can schedule recurring tasks. Cron has been the default for decades. systemd timers are newer, more powerful in certain ways, and deeply integrated with modern Linux init systems. Choosing between them is a practical decision that depends on your requirements, your team's tooling preferences, and the complexity of the task.

## How Cron Works

Cron reads job entries from crontab files — per-user files edited with `crontab -e`, and system files at `/etc/crontab`, `/etc/cron.d/`, and `/etc/cron.daily/` etc. Each entry specifies a schedule as five time fields and a command:

```
# minute hour day-of-month month day-of-week command
0 2 * * * /opt/scripts/backup.sh >> /var/log/backup.log 2>&1
*/15 * * * * /opt/scripts/health-check.sh
0 8 * * 1-5 /opt/scripts/morning-report.sh
```

The cron daemon wakes up every minute, reads the current time, and runs any jobs whose expression matches.

## How systemd Timers Work

A systemd timer consists of two unit files:

1. A `.timer` file that defines the schedule.
2. A `.service` file that defines what to run.

The timer activates the service at the specified times. Here is a basic example:

**`/etc/systemd/system/backup.service`**

```ini
[Unit]
Description=Nightly database backup

[Service]
Type=oneshot
User=deploy
ExecStart=/opt/scripts/backup.sh
StandardOutput=journal
StandardError=journal
```

**`/etc/systemd/system/backup.timer`**

```ini
[Unit]
Description=Run backup nightly at 2 AM

[Timer]
OnCalendar=*-*-* 02:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

Enable and start the timer:

```bash
systemctl daemon-reload
systemctl enable --now backup.timer
systemctl list-timers --all
```

## OnCalendar Syntax: The systemd Equivalent of Cron Expressions

systemd uses its own calendar event syntax in `OnCalendar`. It is more verbose than cron but also more readable:

| Cron expression | OnCalendar equivalent |
|----------------|----------------------|
| `0 2 * * *` | `*-*-* 02:00:00` |
| `*/15 * * * *` | `*-*-* *:0/15:00` |
| `0 8 * * 1-5` | `Mon..Fri *-*-* 08:00:00` |
| `0 0 1 * *` | `*-*-01 00:00:00` |
| `@daily` | `daily` |
| `@weekly` | `weekly` |
| `@reboot` | _(use `OnBootSec=` instead)_ |

Check when a calendar expression will next fire:

```bash
systemd-analyze calendar '*-*-* 02:00:00'
# Output shows next scheduled times
```

## Monotonic Timers

In addition to `OnCalendar` (realtime timers), systemd supports monotonic timers that fire relative to a boot or activation event:

```ini
[Timer]
# Run 5 minutes after the system boots
OnBootSec=5min

# Then repeat every hour
OnUnitActiveSec=1h
```

Monotonic timers are useful for tasks that should run after boot (like initializing a service) rather than at a specific clock time. Cron has no equivalent; the closest approximation is the `@reboot` special string which runs once at cron daemon startup, not at a relative delay.

## Advantages of systemd Timers

### Logging to journald

systemd captures all output from the service unit and stores it in the journal. No manual log redirection needed:

```bash
journalctl -u backup.service
journalctl -u backup.service --since "1 hour ago"
journalctl -u backup.service -f   # follow live
```

With cron, you must redirect output yourself (`>> /var/log/backup.log 2>&1`) and manage log rotation separately.

### Dependency Ordering

Service units support `After=`, `Requires=`, `Wants=`, and other dependency directives. You can ensure a job only runs after the network is up, after a database service is ready, or after another unit has completed:

```ini
[Unit]
After=network-online.target postgresql.service
Requires=postgresql.service
```

Cron has no dependency mechanism at all.

### Resource Limits

Service units support cgroup-based resource controls:

```ini
[Service]
CPUQuota=25%
MemoryMax=512M
IOWeight=50
```

This prevents a runaway backup job from starving other processes. Cron offers no resource controls natively.

### Randomized Delay

Add jitter to prevent all servers in a fleet from hitting a shared resource simultaneously:

```ini
[Timer]
OnCalendar=*-*-* 02:00:00
RandomizedDelaySec=15min
```

This fires the job sometime between 02:00 and 02:15, chosen randomly each time. Cron has no equivalent.

### Persistent Timers

The `Persistent=true` directive in a timer means that if the system was off when the job was supposed to run, it will run immediately at next boot (similar to `anacron`). Cron skips missed jobs by default.

## Advantages of Cron

### Simpler Syntax

A single crontab line is all you need. No unit files to write, no `daemon-reload`, no `enable` command. For simple recurring tasks, cron's five-field expression is much faster to write and easier to read at a glance.

### Universal Availability

Cron is available on virtually every Unix-like system: Linux, macOS, BSD, old embedded systems, Docker containers running Alpine. systemd is Linux-only and is not available on macOS, most BSD variants, or minimal containers without init systems.

### Per-User Crontabs Without sudo

Any user can manage their own crontab with `crontab -e`. There is no need for root access. To create a systemd user timer, you use `systemctl --user`, which is available in most setups but requires lingering to be enabled (`loginctl enable-linger username`) for jobs that should persist after logout.

### Portability

Crontab syntax is standardized by POSIX. Scripts that reference cron will work across many different operating systems and distributions without modification.

## When to Use systemd Timers

- You need structured logging without setting up a log file yourself.
- The job has dependencies on other systemd services.
- You want resource limits (CPU, memory, I/O).
- You need randomized delay across a fleet.
- You need the job to run after a missed schedule (Persistent=true).
- The task is complex enough to warrant a dedicated service definition.

## When to Use Cron

- You want simplicity and quick setup.
- The task runs on macOS, BSD, or a minimal container.
- You need per-user scheduling without sudo.
- Your team is already familiar with crontab syntax.
- You are writing a portable script that must run on multiple operating systems.

## Migrating from Cron to systemd Timer

Here is a practical migration example. Starting crontab entry:

```crontab
0 3 * * * /opt/scripts/db-backup.sh >> /var/log/db-backup.log 2>&1
```

Step 1 — create the service unit:

```bash
cat > /etc/systemd/system/db-backup.service << 'EOF'
[Unit]
Description=Daily database backup

[Service]
Type=oneshot
User=deploy
ExecStart=/opt/scripts/db-backup.sh
StandardOutput=journal
StandardError=journal
EOF
```

Step 2 — create the timer unit:

```bash
cat > /etc/systemd/system/db-backup.timer << 'EOF'
[Unit]
Description=Run database backup daily at 3 AM

[Timer]
OnCalendar=*-*-* 03:00:00
Persistent=true

[Install]
WantedBy=timers.target
EOF
```

Step 3 — enable and start:

```bash
systemctl daemon-reload
systemctl enable --now db-backup.timer
```

Step 4 — verify:

```bash
systemctl list-timers db-backup.timer
journalctl -u db-backup.service --since "1 day ago"
```

Step 5 — remove the cron entry with `crontab -e` and delete the line.

## Getting Cron Expressions Right with crontab.io

Whether you stay with cron or migrate to systemd, the schedule expression logic is identical. [crontab.io](https://crontab.io) lets you build and preview any cron expression interactively. Enter an expression and see a list of upcoming fire times instantly — useful both for traditional crontab entries and for verifying the logic before converting to an `OnCalendar` value in a systemd timer unit.

## Summary

systemd timers win on features: better logging, dependency management, resource controls, and persistent execution. Cron wins on simplicity, portability, and universal availability. For most production servers running systemd, new complex jobs are better served by timer units. For simple scripts, personal tasks, or cross-platform work, cron remains a fast and dependable choice.
