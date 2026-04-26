---
title: "DNS_PROBE_FINISHED_NXDOMAIN Fix: Step-by-Step Solutions"
description: "Fix the DNS_PROBE_FINISHED_NXDOMAIN error with proven troubleshooting steps for Windows, Mac, and mobile devices."
publishDate: 2026-04-25
tags: ["dns error", "nxdomain", "fix", "troubleshooting"]
canonical: "dns-probe-finished-nxdomain-fix-step-by-step-solutions"
---

# DNS_PROBE_FINISHED_NXDOMAIN Fix: Step-by-Step Solutions

The DNS_PROBE_FINISHED_NXDOMAIN error means your browser cannot find the website's IP address. The domain either does not exist, or your DNS resolver cannot locate it. This guide provides step-by-step fixes for Windows, Mac, and mobile devices.

## What NXDOMAIN Means

NXDOMAIN stands for "Non-Existent Domain." Your DNS query returned no results. This can mean:
- The domain is misspelled
- The domain does not exist
- Your DNS server is failing
- Your hosts file blocks the domain

## Fix 1: Check the URL

The most common cause is a typo. Verify the spelling. Try adding or removing "www." Some sites redirect one to the other.

## Fix 2: Flush DNS Cache

**Windows:**
```
ipconfig /flushdns
```

**Mac (Ventura and later):**
```
sudo dscacheutil -flushcache
sudo killall -HUP mDNSResponder
```

**Mac (Monterey and earlier):**
```
sudo killall -HUP mDNSResponder
```

Restart your browser after flushing.

## Fix 3: Change DNS Servers

Switch to public DNS:
- **Google:** 8.8.8.8 and 8.8.4.4
- **Cloudflare:** 1.1.1.1 and 1.0.0.1
- **Quad9:** 9.9.9.9

**Windows:**
1. Control Panel -> Network and Sharing Center
2. Change adapter settings
3. Right-click your connection -> Properties
4. Select IPv4 -> Properties
5. Enter preferred and alternate DNS

**Mac:**
1. System Settings -> Network
2. Click your connection -> Details
3. DNS tab -> add servers

## Fix 4: Reset Network Settings

**Windows:**
```
netsh winsock reset
netsh int ip reset
ipconfig /release
ipconfig /renew
```
Restart your computer.

**Mac:** Remove and re-add your WiFi network in System Settings.

## Fix 5: Check Hosts File

Malware and some privacy tools modify the hosts file to block domains.

**Windows:** Open `C:\Windows\System32\drivers\etc\hosts` in Notepad (run as administrator)
**Mac:** Open `/etc/hosts` in Terminal with sudo

Look for the domain on any line starting with an IP address. Remove the line if found.

## Fix 6: Disable VPN and Proxy

VPNs and proxies can route DNS queries through servers that fail. Disable them temporarily to test.

## Fix 7: Restart Router

Unplug your router for 30 seconds. This clears the router's DNS cache and refreshes your connection.

## Mobile Fixes

**iPhone:**
1. Settings -> WiFi -> tap the "i" next to your network
2. Configure DNS -> Manual -> add 8.8.8.8

**Android:**
1. Settings -> WiFi -> long-press your network
2. Modify network -> Show advanced options
3. Change IP settings to Static
4. Enter DNS 8.8.8.8

## When Nothing Works

If the domain truly does not exist, no DNS fix helps. Verify the domain with our [status checker](/) or a WHOIS lookup. If the domain is registered but not resolving, the issue is on the website owner's side.

## The Bottom Line

DNS_PROBE_FINISHED_NXDOMAIN is usually a local DNS issue. Work through these fixes methodically. Most resolve within minutes.