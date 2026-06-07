---
title: "GitHub Actions Scheduled Workflows: Using the schedule Trigger"
description: "Learn how to schedule GitHub Actions workflows with cron syntax, handle UTC times, avoid common pitfalls, and combine schedules with other triggers."
publishDate: 2026-06-07
updatedDate: 2026-06-07
author: "Editorial Team"
tags: ["github actions", "cron", "ci/cd", "automation", "scheduling"]
draft: false
---

GitHub Actions supports scheduled workflow runs using standard cron syntax via the `schedule` trigger. This is ideal for nightly builds, weekly reports, dependency updates, and any task that should run automatically on a time-based interval.

## Basic Syntax

```yaml
on:
  schedule:
    - cron: '0 2 * * *'  # Run at 2:00 AM UTC every day
```

The `cron` value follows standard 5-field cron syntax:

```
┌───────────── minute (0-59)
│ ┌───────────── hour (0-23)
│ │ ┌───────────── day of month (1-31)
│ │ │ ┌───────────── month (1-12)
│ │ │ │ ┌───────────── day of week (0-6, Sunday=0)
│ │ │ │ │
* * * * *
```

**All times are UTC.** GitHub Actions does not support timezone configuration in the cron expression directly — if you need to schedule for a specific local time, calculate the UTC offset manually.

## Common Schedule Examples

```yaml
# Every 15 minutes
- cron: '*/15 * * * *'

# Every hour
- cron: '0 * * * *'

# Daily at 3:00 AM UTC
- cron: '0 3 * * *'

# Every Monday at 9:00 AM UTC
- cron: '0 9 * * 1'

# Every weekday (Mon-Fri) at 8:00 AM UTC
- cron: '0 8 * * 1-5'

# First day of every month at midnight UTC
- cron: '0 0 1 * *'

# Every Sunday at 6:00 AM UTC
- cron: '0 6 * * 0'

# Three times a day: 6 AM, 12 PM, 6 PM UTC
- cron: '0 6,12,18 * * *'
```

Use [crontab.io](/) to build and validate cron expressions interactively.

## Multiple Schedules

You can define multiple cron schedules for the same workflow:

```yaml
on:
  schedule:
    - cron: '0 2 * * 1-5'   # Weeknights at 2 AM UTC
    - cron: '0 6 * * 6,0'   # Weekend mornings at 6 AM UTC
```

## Combining schedule with Other Triggers

A common pattern is to allow both scheduled runs and manual runs:

```yaml
on:
  schedule:
    - cron: '0 2 * * *'
  workflow_dispatch:        # Allow manual trigger from the GitHub UI
    inputs:
      environment:
        description: 'Target environment'
        required: false
        default: 'staging'

  push:                     # Also run on push to main
    branches: [main]
```

Within the workflow, you can check how it was triggered:

```yaml
steps:
  - name: Print trigger
    run: echo "Triggered by ${{ github.event_name }}"
    # Output: "schedule", "workflow_dispatch", or "push"
```

## Example: Nightly Test Run

```yaml
name: Nightly Tests

on:
  schedule:
    - cron: '0 3 * * *'  # 3:00 AM UTC daily
  workflow_dispatch:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm ci

      - name: Run full test suite
        run: npm test -- --coverage

      - name: Upload coverage report
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: coverage/
```

## Example: Weekly Dependency Update Check

```yaml
name: Weekly Dependency Check

on:
  schedule:
    - cron: '0 9 * * 1'  # Every Monday at 9:00 AM UTC

jobs:
  check-deps:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Check for outdated packages
        run: npm outdated || true  # Don't fail on outdated packages

      - name: Run security audit
        run: npm audit

      - name: Notify on vulnerabilities
        if: failure()
        uses: actions/github-script@v7
        with:
          script: |
            await github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: 'Security vulnerabilities detected',
              body: 'npm audit found vulnerabilities. Check the Actions run for details.',
              labels: ['security', 'dependencies']
            });
```

## Important Limitations and Gotchas

### Schedules Are UTC Only

GitHub does not support IANA timezone names in cron expressions. All schedules run in UTC.

If you need 9:00 AM EST (UTC-5): use `'0 14 * * *'` (9 AM + 5 hours = 14:00 UTC).
If you need 9:00 AM EDT (UTC-4): use `'0 13 * * *'`.

This means you may need to update your cron expression when DST changes if the schedule is meant to fire at a consistent local time.

### Minimum Interval: 5 Minutes

GitHub Actions does not allow schedules more frequent than every 5 minutes. The minimum valid cron expression is `*/5 * * * *`.

### Schedule Delays During High Load

GitHub does not guarantee exact execution timing. Scheduled workflows may be delayed during periods of high load on GitHub's infrastructure. If a workflow is time-sensitive (within minutes), the `schedule` trigger is not appropriate. Consider an external scheduler (AWS EventBridge, Render Cron Jobs, etc.) that calls your workflow via the API.

### Disabled Workflows for Inactive Repositories

GitHub automatically disables scheduled workflows in repositories with no activity (pushes, PRs, comments) for **60 days**. This affects personal projects and open source repos that aren't actively developed.

To keep scheduled workflows active:
- Add a `workflow_dispatch` trigger as a fallback
- Commit something periodically (a README update, a changelog entry)
- Re-enable the workflow from the Actions tab when it gets disabled

### Fork Behavior

Forked repositories do not run scheduled workflows by default. The fork owner must enable Actions in the fork's settings and optionally modify the schedule.

## Conditional Logic Based on Schedule

Sometimes you want different behavior depending on whether the workflow was triggered manually or by schedule:

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to staging (always)
        run: ./deploy.sh staging

      - name: Deploy to production (scheduled only)
        if: github.event_name == 'schedule'
        run: ./deploy.sh production
```

## Checking Last Scheduled Run

There's no built-in GitHub API to see the last time a scheduled workflow ran successfully. Use workflow run history in the Actions tab, or implement your own tracking:

```yaml
- name: Record successful run timestamp
  run: |
    echo "$(date -u)" > .last-scheduled-run
    git config user.email "actions@github.com"
    git config user.name "GitHub Actions"
    git add .last-scheduled-run
    git commit -m "chore: record scheduled run [skip ci]" || true
    git push || true
```

Note: this pattern can cause issues if used carelessly — commits triggering more workflow runs. The `[skip ci]` convention and the `|| true` on push prevent most problems.
