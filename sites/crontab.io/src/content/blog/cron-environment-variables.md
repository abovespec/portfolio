---
title: "Cron Environment Variables: How to Set and Use Them Correctly"
description: "Learn how cron's minimal environment works, how to set variables in crontab, configure MAILTO, source profiles, and debug missing env vars."
publishDate: 2026-06-07
updatedDate: 2026-06-07
author: "Editorial Team"
tags: ["cron", "environment variables", "crontab", "linux", "debugging"]
draft: false
heroImage: "/images/blog/cron-environment-variables-hero.png"
---

One of the most common reasons cron jobs fail silently is the difference between the shell environment you see when you log in and the stripped-down environment that cron provides at runtime. Understanding how cron handles environment variables is essential for writing reliable scheduled tasks.

## The Minimal Cron Environment

When cron executes a job, it does not inherit your login shell environment. Instead it starts with a bare minimum set of variables:

```
SHELL=/bin/sh
PATH=/usr/bin:/bin
HOME=/root          # or the home dir of the user whose crontab is running
LOGNAME=<username>
USER=<username>
```

That's essentially it. Variables you rely on every day — `JAVA_HOME`, `NVM_DIR`, `GOPATH`, `PYENV_ROOT`, custom `PATH` extensions, `LD_LIBRARY_PATH` — are all absent. A script that works perfectly from your terminal can fail immediately in a cron job because a binary or library simply cannot be found.

## Setting Environment Variables in a Crontab

The crontab file itself supports variable assignment lines. Any line of the form `VARIABLE=value` before or between job entries sets that variable for all subsequent jobs in the file:

```crontab
# Set custom environment variables at the top of the crontab
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
MAILTO=ops@example.com
HOME=/home/deploy

# Now the jobs run with these variables in scope
0 2 * * * /opt/scripts/nightly-backup.sh
*/15 * * * * /opt/scripts/health-check.sh
30 8 * * 1 /opt/scripts/weekly-report.sh
```

Variable values do not need to be quoted unless they contain spaces. If a value contains a `%` character, you must escape it as `\%` because unescaped `%` signs have special meaning in crontab (they become newlines in the command).

## MAILTO: Controlling Email Output

By default, cron emails any stdout or stderr output from a job to the owner of the crontab. The `MAILTO` variable controls where that output goes:

```crontab
# Send output to a specific address
MAILTO=admin@example.com

# Send to multiple addresses
MAILTO=admin@example.com,oncall@example.com

# Suppress all email (silently discard output)
MAILTO=""

0 * * * * /opt/scripts/hourly-sync.sh
```

Setting `MAILTO=""` is a common pattern when you redirect output to log files yourself. If you leave `MAILTO` unset and the system has a mail server configured, you may accumulate a large amount of local mail for the cron user.

## Sourcing a Profile to Load Your Full Environment

The cleanest way to give a cron job access to your full login environment is to source the appropriate profile file before running the command. Use a subshell inline:

```crontab
# Source bash_profile before running the command
0 3 * * * . /home/deploy/.bash_profile && /opt/scripts/deploy.sh

# Source /etc/profile for system-wide settings
0 6 * * * . /etc/profile && /opt/scripts/system-check.sh

# Use bash -l (login shell) to source all profile files
30 2 * * * /bin/bash -l -c '/opt/scripts/node-task.js'
```

The `. /path/to/file` syntax (dot-space-path) is the POSIX-portable way to source a file. It is equivalent to `source /path/to/file` in bash but works with any `SHELL` setting.

If you are running Python scripts with a virtual environment, activate it explicitly:

```crontab
0 4 * * * . /home/deploy/venv/bin/activate && python /opt/scripts/report.py
```

Or reference the virtualenv's Python binary directly, which is usually simpler and more reliable:

```crontab
0 4 * * * /home/deploy/venv/bin/python /opt/scripts/report.py
```

## Printing the Cron Environment for Debugging

Before diagnosing why a job fails, it helps to see exactly what environment cron provides. Add a temporary job that dumps the environment to a file:

```crontab
# Dump the cron environment — remove after debugging
* * * * * env > /tmp/cron-env.txt 2>&1
```

Wait one minute, then inspect the file:

```bash
cat /tmp/cron-env.txt
```

You will see exactly which variables are set, their values, and any errors. This output is frequently surprising — the `PATH` is often far shorter than expected, and variables you assumed were always present are missing entirely.

A more complete debugging entry that also captures the working directory and user:

```crontab
* * * * * echo "USER=$USER HOME=$HOME PWD=$(pwd)" >> /tmp/cron-debug.txt && env >> /tmp/cron-debug.txt
```

## Setting Variables for Individual Jobs

You can scope a variable to a single command by prepending `VAR=value` inline. This overrides the file-level setting for just that one job:

```crontab
PATH=/usr/local/bin:/usr/bin:/bin

# This job uses the PATH set above
0 1 * * * backup.sh

# This job uses a custom JAVA_HOME for just itself
0 2 * * * JAVA_HOME=/opt/jdk-21 /opt/scripts/java-task.sh
```

This pattern is useful when different jobs on the same crontab need different versions of a tool.

## Common Issues Caused by Missing Environment Variables

### Node.js / nvm

`nvm` installs Node into `~/.nvm/versions/node/...` and adds itself to `PATH` via `.bashrc` or `.bash_profile`. Cron does not source either file, so `node` and `npm` are not found. Solutions:

```crontab
# Option 1: Use the full path from nvm
0 * * * * /home/deploy/.nvm/versions/node/v20.11.0/bin/node /opt/app/worker.js

# Option 2: Source nvm before running
0 * * * * . /home/deploy/.nvm/nvm.sh && node /opt/app/worker.js
```

### Python with pyenv

```crontab
# Use the full pyenv shim path or the direct binary
0 * * * * /home/deploy/.pyenv/shims/python /opt/scripts/job.py

# Or activate pyenv first
0 * * * * export PYENV_ROOT=$HOME/.pyenv && export PATH=$PYENV_ROOT/bin:$PATH && eval "$(pyenv init -)" && python /opt/scripts/job.py
```

### Ruby with rbenv or rvm

```crontab
# rbenv
0 * * * * /bin/bash -l -c 'rbenv exec ruby /opt/scripts/task.rb'

# rvm
0 * * * * /bin/bash -l -c 'source /usr/local/rvm/scripts/rvm && ruby /opt/scripts/task.rb'
```

## Best Practices for Cron Environment Variables

1. **Always set `PATH` explicitly** at the top of every crontab. Include `/usr/local/bin` if you install tools there.
2. **Use absolute paths** for commands in job entries. Do not rely on `PATH` to resolve them.
3. **Set `MAILTO`** so you know where output goes, even if it is `""` to discard it.
4. **Test in a minimal environment** before adding a job. Run `env -i HOME=$HOME PATH=/usr/bin:/bin /bin/sh -c 'your-command'` to simulate cron.
5. **Log explicitly**: redirect stdout and stderr to a file so you can inspect job results later.

```crontab
0 2 * * * /opt/scripts/backup.sh >> /var/log/backup.log 2>&1
```

## Using crontab.io to Build and Test Schedules

Getting the schedule expression right is half the battle. Before adding any new cron job, use [crontab.io](https://crontab.io) to build and validate your cron expression. The visual editor shows you exactly when each expression fires, making it easy to confirm your job will run at the expected times without having to wait and see. Once you have the right expression, paste it directly into your crontab alongside the correctly scoped environment variables covered in this article.

## Summary

Cron runs in a deliberately minimal environment. The `PATH` is narrow, login profiles are not sourced, and variables you depend on daily are absent. Solve this by setting `PATH` and other required variables at the top of your crontab, sourcing profile files when needed, or using absolute paths to every binary. When something goes wrong, dump the cron environment to a file with `env > /tmp/cron-env.txt` to see exactly what is available at runtime.
