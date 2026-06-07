---
title: "UTM Tracking: How to Set Up and Measure Marketing Campaigns"
description: "Set up UTM tracking for email, social, paid ads, and QR codes. Learn how to read campaign reports in Google Analytics 4 and troubleshoot missing UTM data."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["utm tracking", "google analytics", "campaign tracking", "ga4", "marketing"]
draft: false
---

UTM tracking tells you which marketing efforts drive traffic and conversions. Set up correctly, it gives you a complete picture of where your customers come from. Here's a practical implementation guide.

## How UTM tracking works

1. You add UTM parameters to a link
2. A user clicks the link
3. Their browser lands on your site with `?utm_source=...&utm_medium=...` in the URL
4. Google Analytics reads those parameters and stores them with the session
5. You can query those values in reports

For more on this topic, see [*Google Analytics UTM: Campaign Tracking in GA4*](/blog/google-analytics-utm).

The tracking happens client-side — GA4's JavaScript snippet reads `document.location.search` on page load and extracts UTM values.

## Setting up tracking for each channel

### Email campaigns

Every link in your email should have UTMs. Use consistent values across your email provider:

```
utm_source=newsletter
utm_medium=email
utm_campaign=april-digest-2026
utm_content=hero-cta        ← for the main button
utm_content=article-link-1  ← for article links
```

**Mailchimp:** Use the built-in Google Analytics integration — it auto-appends UTMs with your campaign name.

**Manual:** Build links with [utmbuilder.io](/) and paste them into your email template.

### Social media

**Organic posts:**
```
utm_source=facebook
utm_medium=social
utm_campaign=product-launch-2026
```

**Paid social (Facebook Ads):** Use Facebook's URL Parameters field in the ad set:
```
utm_source=facebook&utm_medium=cpc&utm_campaign={{campaign.name}}&utm_content={{ad.name}}
```

For more on this topic, see [*UTM Parameters Explained: Source, Medium, Campaign, Content, Term*](/blog/utm-parameters).

Facebook substitutes `{{campaign.name}}` with the actual campaign name automatically.

### Paid search (Google Ads)

Enable auto-tagging in Google Ads settings — it appends `gclid` automatically. UTMs are optional but useful for compatibility with third-party analytics tools:

```
utm_source=google
utm_medium=cpc
utm_campaign={campaign}
utm_content={creative}
utm_term={keyword}
```

Use ValueTrack parameters (`{campaign}`, `{keyword}`) — Google substitutes the actual values.

### QR codes

QR codes are physical, so they're treated like print advertising. Add UTMs so you can measure scan-to-visit rates:

```
utm_source=qr
utm_medium=print
utm_campaign=storefront-2026
utm_content=front-door   ← identifies which specific code
```

### Partner referrals and affiliate links

```
utm_source=partner-name
utm_medium=referral
utm_campaign=affiliate-program
utm_content=homepage-link
```

## Viewing UTM data in GA4

**Traffic acquisition report:**
1. Reports → Acquisition → Traffic acquisition
2. Dimension: "Session source / medium"
3. See traffic by `newsletter / email`, `google / cpc`, etc.

**Campaign report:**
1. Reports → Acquisition → Traffic acquisition
2. Change dimension to "Session campaign"
3. Filter by campaign name

**Custom exploration:**
1. Explore → Blank → Create new exploration
2. Add dimensions: Session source, Session medium, Session campaign, Session content
3. Add metrics: Sessions, Engaged sessions, Conversions
4. Use this to analyze campaign performance in detail

## UTM best practices

**1. Always use lowercase**

Most analytics tools are case-sensitive. `Email` and `email` are tracked separately:

```
# Inconsistent (bad)
utm_medium=Email
utm_medium=email
utm_medium=EMAIL

# Consistent (good)
utm_medium=email
```

**2. Use a naming spreadsheet**

Create a shared doc or spreadsheet with your UTM naming conventions. Everyone on the team uses the same values.

| Channel | utm_source | utm_medium | utm_campaign |
|---------|-----------|-----------|-------------|
| Newsletter | newsletter | email | [campaign-name] |
| Google Ads | google | cpc | [campaign-name] |
| Facebook Ads | facebook | cpc | [campaign-name] |
| Organic Facebook | facebook | social | [campaign-name] |
| LinkedIn organic | linkedin | social | [campaign-name] |

For more on this topic, see [*utm_source, utm_medium, utm_campaign: A Complete Guide*](/blog/utm-source-medium-campaign).

**3. Use campaign names that are time-bound and descriptive**

```
# Vague (bad)
utm_campaign=sale

# Descriptive (good)
utm_campaign=spring-sale-2026-q2
```

**4. Test before publishing**

Click your UTM link and check GA4's Realtime report. You should see your session appear with the correct source/medium/campaign values.

## Troubleshooting missing UTM data

**UTM shows as (not set) in GA4:**
- Confirm the link has UTM parameters (copy and check)
- Check that the landing page doesn't redirect and strip the parameters
- Check that your GA4 tag fires on the landing page

**UTM shows as (direct):**
- Redirects often strip UTM parameters — add them to the final destination URL, not an intermediate redirect
- Some email clients strip UTMs — check with a test click

**Inconsistent values:**
- Case inconsistency (`Email` vs `email`) is usually the cause
- Enforce lowercase in your UTM template

Build and validate UTM links at [utmbuilder.io](/).
