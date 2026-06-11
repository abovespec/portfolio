#!/usr/bin/env bash
# deploy-rtc-wake.sh
#
# One-time setup: installs the RTC wake service so the machine auto-powers on
# at 06:50 AM EDT before the Paperclip Morning Report fires at 07:00 AM.
#
# Run as root: sudo bash scripts/deploy-rtc-wake.sh
# From the site-network repo root.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== Deploying Paperclip RTC wake service ==="

# Copy the wake script
cp "$SCRIPT_DIR/set-paperclip-rtcwake.sh" /usr/local/bin/set-paperclip-rtcwake.sh
chmod +x /usr/local/bin/set-paperclip-rtcwake.sh
echo "Installed: /usr/local/bin/set-paperclip-rtcwake.sh"

# Install the systemd unit
cp "$SCRIPT_DIR/paperclip-rtc-wake.service" /etc/systemd/system/paperclip-rtc-wake.service
echo "Installed: /etc/systemd/system/paperclip-rtc-wake.service"

# Enable and start
systemctl daemon-reload
systemctl enable paperclip-rtc-wake.service
systemctl start paperclip-rtc-wake.service

echo ""
echo "=== Current RTC alarm ==="
cat /sys/class/rtc/rtc0/wakealarm
TZ="America/New_York" date -d "@$(cat /sys/class/rtc/rtc0/wakealarm)" '+%Y-%m-%d %H:%M %Z' 2>/dev/null || echo "(alarm not set)"

echo ""
echo "=== Next step: test wake-from-S5 ==="
echo "Run the following to verify your BIOS supports RTC wake from full power-off:"
echo ""
echo "  sudo bash scripts/test-rtc-wake.sh"
echo ""
echo "If the machine powers back on ~2 minutes after shutdown, RTC wake works."
echo "If it does not power on, use the GitHub Actions approach instead."
