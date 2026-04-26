---
title: "Google Analytics UTM: Campaign Tracking in GA4"
description: "Set up UTM campaign tracking in Google Analytics 4. Learn how GA4 handles utm_source, utm_medium, utm_campaign, and where to find campaign reports in the UI."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["utm", "google analytics", "ga4", "campaign tracking", "analytics"]
draft: false
---

Google Analytics 4 (GA4) reads UTM parameters automatically from the URL when visitors land on your site. No additional setup is required beyond having the GA4 tag installed. Here's how it works and where to find the data.

## How GA4 processes UTM parameters

When a visitor lands on a page with UTM parameters in the URL, the GA4 tag reads them on page load. GA4 maps each UTM parameter to an event property and session dimension:

| UTM Parameter | GA4 Dimension |
|---------------|--------------|
| utm_source | Session source |
| utm_medium | Session medium |
| utm_campaign | Session campaign |
| utm_content | Session content |
| utm_term | Session term |
| utm_id | Campaign ID |

GA4 stores these on the **session** level. The first UTM-tagged hit in a session sets the session's source/medium/campaign — subsequent pageviews in the same session don't override it.

## Auto-tagging vs. manual UTM tagging

**Auto-tagging (Google Ads):** When you enable auto-tagging in Google Ads, Google appends `?gclid=...` to your destination URLs. GA4 reads the `gclid` and maps it to the corresponding Google Ads campaign data. You don't need manual UTMs for Google Ads if auto-tagging is enabled.

**Manual UTMs:** Used for all other traffic sources — email, social media, affiliate links, partner sites, print/QR codes. Always manual — no platform tags your links automatically (except Google Ads with auto-tagging).

If both auto-tagging and UTMs are present, auto-tagging takes priority for Google Ads traffic.

## Where to find UTM data in GA4

### Traffic acquisition report

**Reports → Acquisition → Traffic acquisition**

The default view shows "Session default channel group" — a GA4-defined grouping that uses UTMs to classify traffic:

| Channel group | Conditions |
|--------------|------------|
| Organic Search | medium = organic |
| Paid Search | medium = cpc, ppc, paidsearch |
| Organic Social | medium = social, social-network, social-media |
| Paid Social | medium = paid-social |
| Email | medium = email, e-mail, e_mail, newsletter |
| Referral | medium = referral |
| Direct | No UTMs and no referrer |
| Affiliates | medium = affiliate |
| Display | medium = banner, display |

Change the primary dimension to "Session source / medium" to see the raw UTM values.

### Campaign details

**Reports → Acquisition → Traffic acquisition** → change dimension to "Session campaign"

Shows performance grouped by `utm_campaign` value.

### Custom exploration

For deeper analysis, build an exploration:

1. **Explore** → Blank → Name it "Campaign Analysis"
2. **Dimensions:** Session source, Session medium, Session campaign, Session content
3. **Metrics:** Sessions, Engaged sessions, Engagement rate, Conversions, Total revenue
4. **Technique:** Free form table
5. Apply date range and filters as needed

### Real-time testing

To confirm a UTM link is working:
1. Click your UTM-tagged link (opens your site)
2. In GA4: **Reports → Realtime**
3. You should see your session in the "User activity in the last 30 minutes" section
4. Click on it — you can see the UTM values captured

## Setting up GA4 for campaign tracking

**Step 1: Confirm GA4 is installed**

The GA4 tag must fire on all pages that are destinations for UTM-tagged links. Check with Google Tag Assistant or the GA4 Realtime report.

**Step 2: Create conversion events (optional)**

For meaningful campaign ROI analysis, mark key events as conversions:

1. **Admin → Events** → find the event (e.g., `purchase`, `generate_lead`, `sign_up`)
2. Toggle "Mark as conversion"
3. Conversions will now appear in the Traffic acquisition report, segmented by campaign

**Step 3: Configure channel groupings (optional)**

GA4's default channel groupings use medium values to classify traffic. If you use non-standard mediums, configure custom channel groups:

**Admin → Data display → Channel groups → Create custom channel group**

## GA4 data-driven attribution

GA4 uses data-driven attribution by default (previously, UA used last-click). This means conversion credit is distributed across all touchpoints in the conversion path, not just the last one.

This affects how your UTM campaign data appears in reports. A campaign that assisted many conversions but wasn't the final touchpoint may show fewer conversions in last-click reports but more in the default GA4 reports.

**Reports → Advertising → Attribution → Model comparison** — compare attribution models for your UTM campaign data.

## Common GA4 UTM issues

**"(not set)" in campaign reports:**
- The page load fires before the UTM is processed (rare)
- The landing page redirects and strips the UTM
- The GA4 tag only fires on some pages

**"(direct) / (none)" instead of UTM values:**
- The link doesn't have UTMs
- An intermediate redirect stripped the UTMs
- The user bookmarked or manually typed the URL

**Inconsistent case:**
- `Email` and `email` appear as separate rows
- Enforce lowercase across all your UTM links

Build UTM links at [utmbuilder.io](/).
