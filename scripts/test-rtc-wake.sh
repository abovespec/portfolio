#!/usr/bin/env bash
# test-rtc-wake.sh
#
# Tests whether this machine's BIOS/ACPI supports RTC wake from full power-off (S5).
# Sets an alarm 3 minutes in the future, then shuts down.
# If the machine powers back on automatically in ~3 min, RTC wake from S5 works.
#
# WARNING: This will SHUT DOWN the machine.
# Run as root: sudo bash scripts/test-rtc-wake.sh

set -euo pipefail

WAKE_DELAY_SECS=180  # 3 minutes

NOW=$(date +%s)
WAKE_AT=$((NOW + WAKE_DELAY_SECS))
WAKE_HUMAN=$(date -d "@${WAKE_AT}" '+%H:%M:%S UTC')

echo "=== RTC Wake-from-S5 Test ==="
echo "Will set RTC alarm for ${WAKE_HUMAN} (3 minutes from now)"
echo "Then shut down. If BIOS supports wake-from-S5, machine will power on automatically."
echo ""
read -r -p "Proceed? This will SHUT DOWN the machine. [y/N] " CONFIRM

if [[ "$CONFIRM" != "y" && "$CONFIRM" != "Y" ]]; then
    echo "Aborted."
    exit 0
fi

# Clear and set alarm
echo 0 > /sys/class/rtc/rtc0/wakealarm
echo "$WAKE_AT" > /sys/class/rtc/rtc0/wakealarm

echo "Alarm set for ${WAKE_HUMAN}"
echo "Shutting down in 5 seconds..."
sleep 5

systemctl poweroff
