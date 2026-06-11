---
title: "Cron PATH Variable: Fix 'Command Not Found' Errors in Cron Jobs"
description: "Why cron's restricted PATH causes jobs to fail silently, and how to fix it with absolute paths, PATH overrides, sourcing profiles, and bash -l."
publishDate: 2026-06-07
updatedDate: 2026-06-07
author: "Editorial Team"
tags: ["cron", "PATH", "crontab", "debugging", "linux"]
draft: false
heroImage: "/images/blog/cron-path-variable-hero.png"
---

The single most common reason a cron job works perfectly in your terminal but fails when scheduled is the `PATH` variable. Cron runs with a stripped-down `PATH` that excludes most directories where tools are installed. This guide explains why it happens, how to diagnose it, and how to fix it permanently.

## What PATH Does Cron Use?

When cron executes a job it sets:

```
PATH=/usr/bin:/bin
```

That is the entire `PATH`. Your login shell typically has a much longer `PATH` — something like:

```
/home/deploy/.nvm/versions/node/v20.11.0/bin:/home/deploy/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin
```

Any binary installed in `/usr/local/bin`, `/usr/sbin`, `/snap/bin`, your home directory, or a version manager like `nvm`, `pyenv`, or `rbenv` is invisible to cron. When cron tries to run the command, the shell reports "command not found" — or, if the command is the script itself that calls a missing tool, the script exits with an unhelpful error code.

## Symptoms

- Job runs fine manually, fails in cron with no output.
- You see "command not found" in `/var/log/syslog` or cron's mail output.
- The cron mail says "No such file or directory" for a script that clearly exists.
- A Python or Node script exits immediately when run as a cron job.
- `crontab -e` entries with just the command name (e.g., `python`) fail while `python3` entries fail too, but `/usr/bin/python3` works.

## Diagnosing the Problem

First, confirm what `PATH` cron is actually using. Add a temporary job:

```crontab
* * * * * echo $PATH > /tmp/cron-path.txt
```

Wait one minute, then:

```bash
cat /tmp/cron-path.txt
# Output: /usr/bin:/bin
```

Next, find where your tool actually lives:

```bash
which python3
# /usr/bin/python3

which node
# /home/deploy/.nvm/versions/node/v20.11.0/bin/node

which pip
# /home/deploy/.local/bin/pip

which my-custom-script
# /usr/local/bin/my-custom-script
```

Any path outside `/usr/bin` or `/bin` is invisible to cron unless you explicitly configure it.

## Fix 1: Use Absolute Paths

The most reliable fix is to replace every command in your crontab with its full absolute path. This removes any `PATH` dependency entirely:

```crontab
# Before (works in terminal, fails in cron)
*/15 * * * * python3 /opt/scripts/health-check.py

# After (works in cron)
*/15 * * * * /usr/bin/python3 /opt/scripts/health-check.py
```

Use `which` to find the absolute path for every tool you use, then hardcode those paths into your crontab entries.

## Fix 2: Set PATH at the Top of the Crontab

Add a `PATH=` line at the very top of your crontab. This overrides the default for every job in the file:

```crontab
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin

# All jobs below now use this PATH
0 2 * * * backup.sh
*/5 * * * * health-check.sh
0 8 * * 1-5 morning-report.sh
```

Get the right value for `PATH` by running `echo $PATH` in your regular terminal and copying the output. You can trim it down to only the directories you actually need — a shorter `PATH` is faster to search.

## Fix 3: Source a Profile Before Running the Command

For version-managed tools like Node via nvm or Python via pyenv, sourcing the appropriate init script before your command is the most complete solution:

```crontab
# nvm
0 3 * * * . /home/deploy/.nvm/nvm.sh && node /opt/app/worker.js

# pyenv
0 4 * * * export PYENV_ROOT=/home/deploy/.pyenv && export PATH=$PYENV_ROOT/bin:$PATH && eval "$(pyenv init -)" && python /opt/app/report.py

# rbenv
0 5 * * * . /home/deploy/.rbenv/bin/rbenv init - && ruby /opt/app/task.rb
```

The dot-space (`. `) operator sources the file in the current shell session without spawning a subshell, so the exported variables are available to the subsequent command.

## Fix 4: Run Commands in a Login Shell with bash -l

A login shell sources `/etc/profile`, `/etc/profile.d/*`, `~/.bash_profile`, and `~/.bashrc`, giving you the same environment you have at the terminal. Use `bash -l -c` to wrap your command:

```crontab
# Run in a login shell — gets full environment including nvm, pyenv, etc.
0 2 * * * /bin/bash -l -c '/opt/scripts/nightly-build.sh'
0 6 * * * /bin/bash -l -c 'node /opt/app/jobs/sync.js'
0 8 * * 1 /bin/bash -l -c 'python /opt/app/weekly-report.py'
```

The `-l` flag makes bash act as a login shell. The `-c` flag passes the command as a string. This approach is convenient but slightly heavier than the alternatives because it sources multiple profile files on each execution.

## Real-World Example: Python Script

Consider a Python script that uses a virtualenv and works fine when run manually:

```bash
# Terminal — works fine
python report.py
```

But the crontab entry fails:

```crontab
# This fails: python is not in /usr/bin:/bin on many systems
0 8 * * 1 python /opt/app/report.py
```

**Debugging steps:**

```bash
# 1. Find where python lives
which python
# /usr/bin/python (maybe /usr/bin/python3, not the venv version)

# 2. Find the virtualenv python
ls /opt/app/venv/bin/python
# /opt/app/venv/bin/python

# 3. Check what the script imports
head -5 /opt/app/report.py
# import pandas
# import requests
# These are in the venv, not the system python
```

**Fixed crontab:**

```crontab
# Use the virtualenv's Python directly
0 8 * * 1 /opt/app/venv/bin/python /opt/app/report.py >> /var/log/report.log 2>&1
```

Or with activation:

```crontab
0 8 * * 1 . /opt/app/venv/bin/activate && python /opt/app/report.py >> /var/log/report.log 2>&1
```

## Debugging with Full Output Capture

Always redirect both stdout and stderr when debugging cron jobs. The `2>&1` redirect combines stderr into stdout, and `>>` appends to a log file:

```crontab
0 2 * * * /opt/scripts/backup.sh >> /var/log/backup.log 2>&1
```

Without this redirection, errors appear only in cron's mail output (if mail is configured) or are silently discarded.

To also capture the exit code:

```crontab
0 2 * * * /opt/scripts/backup.sh >> /var/log/backup.log 2>&1; echo "Exit: $?" >> /var/log/backup.log
```

## Full Environment Simulation for Testing

Before adding a job to crontab, test your command in an environment that matches what cron will provide:

```bash
# Simulate cron's minimal environment
env -i HOME=/home/deploy \
    LOGNAME=deploy \
    USER=deploy \
    PATH=/usr/bin:/bin \
    /bin/sh -c '/opt/scripts/backup.sh'
```

If this fails but running the script directly succeeds, you have a `PATH` or environment variable issue. Fix it in the simulated environment first, then translate the fix into the correct crontab form.

## Summary of Solutions

| Problem | Solution |
|---------|----------|
| Binary not in `/usr/bin` or `/bin` | Use full absolute path |
| Many binaries from custom locations | Set `PATH=` at top of crontab |
| Version manager (nvm, pyenv, rbenv) | Source the version manager's init script |
| Complex environment needed | Use `bash -l -c 'command'` |
| Virtualenv Python | Reference `venv/bin/python` directly |

## Build and Validate Schedules at crontab.io

Once you have the environment issue sorted, get your cron expression right with [crontab.io](https://crontab.io). The interactive builder lets you construct any cron expression and immediately see a list of the next scheduled run times, so you can confirm the frequency and timing before committing the job to your crontab. Combining a correct schedule expression with the right PATH configuration is all it takes to run cron jobs reliably.
