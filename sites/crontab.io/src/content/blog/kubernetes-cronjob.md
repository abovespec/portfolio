---
title: "Kubernetes CronJob: A Complete Guide with YAML Examples"
description: "Learn how to create and manage Kubernetes CronJob resources, configure schedules, handle concurrency, set history limits, and debug common issues."
publishDate: 2026-06-07
updatedDate: 2026-06-07
author: "Editorial Team"
tags: ["kubernetes", "cronjob", "cron", "scheduling", "devops"]
draft: false
heroImage: "/images/blog/kubernetes-cronjob-hero.png"
---

Kubernetes CronJobs bring the familiar cron scheduling model to containerized workloads. Rather than running a cron daemon on a VM, you define a `CronJob` resource that Kubernetes manages — spawning Job (and therefore Pod) objects on your configured schedule. This guide covers everything you need to configure and operate Kubernetes CronJobs reliably.

## CronJob vs Job in Kubernetes

A `Job` runs a task once to completion. It creates one or more Pods, waits for them to finish successfully, and then the Job is done.

A `CronJob` is a controller that creates `Job` objects on a recurring schedule. The relationship is:

```
CronJob → Job(s) → Pod(s)
```

CronJobs do not manage Pods directly. They create Jobs, and Jobs manage Pods. This distinction matters when debugging: if your scheduled task is not running, check both the CronJob and the Jobs it spawned.

## The spec.schedule Field

The `spec.schedule` field uses standard cron syntax — five fields representing minute, hour, day-of-month, month, and day-of-week:

```yaml
spec:
  schedule: "0 2 * * *"      # 2 AM every day
  schedule: "*/15 * * * *"   # Every 15 minutes
  schedule: "0 8 * * 1-5"    # 8 AM on weekdays
  schedule: "0 0 1 * *"      # Midnight on the 1st of every month
```

All times are evaluated in UTC by default in Kubernetes, unless you set `spec.timeZone` (discussed below).

## Timezone Support: spec.timeZone

Since Kubernetes 1.27, CronJobs support a `spec.timeZone` field that accepts IANA timezone names. Before 1.27, all schedules were interpreted as UTC.

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: morning-report
spec:
  schedule: "0 9 * * 1-5"
  timeZone: "America/New_York"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: reporter
            image: myrepo/reporter:latest
          restartPolicy: OnFailure
```

Verify your cluster version supports `spec.timeZone`:

```bash
kubectl version --short
# If server version >= 1.27, timeZone is supported
```

## concurrencyPolicy

By default, if a Job from the previous schedule run is still executing when the next run is due, Kubernetes starts a new Job anyway. The `concurrencyPolicy` field controls this behavior:

| Value | Behavior |
|-------|----------|
| `Allow` | Default. Multiple Jobs may run concurrently. |
| `Forbid` | Skip the new run if the previous Job is still running. |
| `Replace` | Terminate the running Job and start a new one. |

For most use cases — database backups, report generation, data sync — you want `Forbid` to prevent overlapping runs:

```yaml
spec:
  schedule: "0 2 * * *"
  concurrencyPolicy: Forbid
```

Use `Replace` when you want to ensure only the latest version of the task runs and old runs are irrelevant (e.g., generating a live status page).

## startingDeadlineSeconds

If the CronJob controller misses a scheduled run (e.g., because the controller was down), `startingDeadlineSeconds` defines a window within which the job can still be started late:

```yaml
spec:
  schedule: "0 2 * * *"
  startingDeadlineSeconds: 3600   # Start up to 1 hour late
```

If the deadline passes without a start, the run is counted as missed. If more than 100 consecutive runs are missed, Kubernetes stops scheduling the CronJob and logs an error. This limit exists because the controller counts missed runs by iterating over the schedule history, and a large count can cause performance problems.

Setting `startingDeadlineSeconds` to a value that fits your tolerance for lateness helps avoid hitting the 100-missed-run limit during extended control plane outages.

## Job History: successfulJobsHistoryLimit and failedJobsHistoryLimit

Kubernetes keeps completed Jobs around for inspection. The defaults are:

- `successfulJobsHistoryLimit: 3` — Keep the 3 most recent successful Jobs
- `failedJobsHistoryLimit: 1` — Keep the 1 most recent failed Job

Adjust these based on how much history you need:

```yaml
spec:
  successfulJobsHistoryLimit: 5
  failedJobsHistoryLimit: 3
```

Setting either to `0` deletes Jobs (and their Pods) immediately after completion, which keeps the namespace clean but makes debugging harder.

## backoffLimit

The `backoffLimit` in the Job spec controls how many times Kubernetes will retry a failed Pod before marking the Job as failed:

```yaml
spec:
  jobTemplate:
    spec:
      backoffLimit: 2   # Retry up to 2 times after initial failure
```

With `backoffLimit: 2`, Kubernetes will attempt the Pod up to 3 times total (1 initial + 2 retries). Retries use exponential backoff with a cap of 6 minutes between attempts.

## Complete YAML Example: Daily Database Backup

Here is a production-ready CronJob that performs a daily PostgreSQL database backup and uploads it to S3:

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: postgres-backup
  namespace: production
  labels:
    app: postgres-backup
    tier: maintenance
spec:
  schedule: "0 2 * * *"
  timeZone: "UTC"
  concurrencyPolicy: Forbid
  startingDeadlineSeconds: 3600
  successfulJobsHistoryLimit: 7
  failedJobsHistoryLimit: 3
  jobTemplate:
    spec:
      backoffLimit: 2
      template:
        metadata:
          labels:
            app: postgres-backup
        spec:
          restartPolicy: OnFailure
          containers:
          - name: backup
            image: myrepo/db-backup:v2.1.0
            imagePullPolicy: IfNotPresent
            env:
            - name: PGHOST
              valueFrom:
                secretKeyRef:
                  name: postgres-credentials
                  key: host
            - name: PGUSER
              valueFrom:
                secretKeyRef:
                  name: postgres-credentials
                  key: username
            - name: PGPASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgres-credentials
                  key: password
            - name: S3_BUCKET
              value: "my-backups-bucket"
            - name: S3_PREFIX
              value: "postgres/daily"
            resources:
              requests:
                memory: "256Mi"
                cpu: "100m"
              limits:
                memory: "512Mi"
                cpu: "500m"
          serviceAccountName: backup-sa
```

Apply it:

```bash
kubectl apply -f postgres-backup-cronjob.yaml
kubectl get cronjobs -n production
kubectl describe cronjob postgres-backup -n production
```

## Managing and Monitoring CronJobs

### List CronJobs and their schedules

```bash
kubectl get cronjobs -A
# NAMESPACE    NAME             SCHEDULE    SUSPEND   ACTIVE   LAST SCHEDULE   AGE
# production   postgres-backup  0 2 * * *   False     0        4h              30d
```

### Check recent Jobs spawned by a CronJob

```bash
kubectl get jobs -n production -l app=postgres-backup
```

### View logs for the most recent run

```bash
# Get the most recent pod for the CronJob
kubectl get pods -n production -l app=postgres-backup --sort-by=.metadata.creationTimestamp

# Get logs from the most recent pod
kubectl logs -n production <pod-name>
```

### Manually trigger a CronJob for testing

```bash
kubectl create job --from=cronjob/postgres-backup manual-backup-test -n production
```

This creates a one-off Job from the CronJob's template — useful for testing without waiting for the next scheduled run.

### Suspend and resume a CronJob

```bash
# Pause new runs (does not affect already-running Jobs)
kubectl patch cronjob postgres-backup -n production -p '{"spec":{"suspend":true}}'

# Resume
kubectl patch cronjob postgres-backup -n production -p '{"spec":{"suspend":false}}'
```

## Common Issues and Solutions

### Pods Fail Immediately

Check if the container image can be pulled and if the environment variables and secrets are correctly configured:

```bash
kubectl describe pod <pod-name> -n production
# Look for ImagePullBackOff, ErrImagePull, or missing secret errors
```

### Job Runs Later Than Expected

This usually means the CronJob controller was temporarily unavailable. Check `startingDeadlineSeconds` — if it is not set or is very small, runs may be skipped. Examine the CronJob events:

```bash
kubectl describe cronjob postgres-backup -n production
# Look for "Missed scheduled time to start a job" events
```

### Resource Pressure Causing Pod Eviction

Set resource requests and limits in the container spec. Without requests, Pods may be scheduled on overloaded nodes and fail due to memory pressure. Set `resources.requests` conservatively and `resources.limits` at a safe ceiling.

### Duplicate Runs

If you see the same job running multiple times per schedule, check `concurrencyPolicy`. It is probably set to `Allow` (the default). Change it to `Forbid` if your task is not idempotent.

## Cron Expression Reference for Kubernetes

Kubernetes CronJob uses the same five-field cron syntax as traditional cron. To build and validate expressions, use [crontab.io](https://crontab.io). The interactive editor lets you construct expressions and preview upcoming fire times — which is especially useful when combined with `spec.timeZone`, since seeing the UTC-equivalent times helps verify the schedule before deploying to your cluster.

## Summary

Kubernetes CronJobs wrap the familiar cron scheduling model in a container-native resource. Set `spec.schedule` with standard cron syntax, configure `spec.timeZone` for non-UTC timezones (requires Kubernetes 1.27+), use `concurrencyPolicy: Forbid` for non-idempotent tasks, tune `startingDeadlineSeconds` to handle controller outages gracefully, and set history limits to control how many completed Jobs are retained. For debugging, combine `kubectl describe cronjob`, `kubectl get jobs`, and `kubectl logs` to trace exactly what ran and when.
