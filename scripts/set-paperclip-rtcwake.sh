#!/usr/bin/env bash
# set-paperclip-rtcwake.sh
#
# Sets an RTC wake alarm so the machine powers on at 06:50 AM EDT
# before the Paperclip Morning Report routine fires at 07:00 AM EDT.
#
# Must run as root (writes to /sys/class/rtc/rtc0/wakealarm).
# Called by paperclip-rtc-wake.service at boot and before shutdown.
#
# Usage: sudo bash set-paperclip-rtcwake.sh

set -euo pipefail

WAKE_HOUR=6
WAKE_MIN=50
TZ_WAKE="America/New_York"

NOW_EPOCH=$(date +%s)

# Next 06:50 AM in the target timezone, expressed as UTC epoch
NEXT_WAKE=$(TZ="$TZ_WAKE" date -d "today ${WAKE_HOUR}:${WAKE_MIN}" +%s)

if [[ "$NOW_EPOCH" -ge "$NEXT_WAKE" ]]; then
    # Already past today's wake window; aim for tomorrow
    NEXT_WAKE=$(TZ="$TZ_WAKE" date -d "tomorrow ${WAKE_HOUR}:${WAKE_MIN}" +%s)
fi

NEXT_WAKE_HUMAN=$(TZ="$TZ_WAKE" date -d "@${NEXT_WAKE}" '+%Y-%m-%d %H:%M %Z')

# Clear any existing alarm first
echo 0 > /sys/class/rtc/rtc0/wakealarm

# Set the new alarm (UTC epoch seconds)
echo "$NEXT_WAKE" > /sys/class/rtc/rtc0/wakealarm

WRITTEN=$(cat /sys/class/rtc/rtc0/wakealarm)
echo "RTC wake alarm set: ${NEXT_WAKE_HUMAN} (epoch ${WRITTEN})"
logger "paperclip-rtc-wake: alarm set for ${NEXT_WAKE_HUMAN} (epoch ${WRITTEN})"
