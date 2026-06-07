---
title: "utm_source, utm_medium, utm_campaign: A Complete Guide"
description: "Master utm_source, utm_medium, and utm_campaign parameter values. Includes naming conventions, standard values for each channel, and common mistakes to avoid."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["utm", "utm source", "utm medium", "utm campaign", "campaign tracking"]
draft: false
---

The three required UTM parameters — source, medium, and campaign — form the backbone of campaign attribution. Using consistent, well-chosen values makes your analytics data reliable and actionable.

## utm_source

Source identifies **where** the traffic is coming from. It's typically the platform, site, or publisher sending the traffic.

**Rules:**
- Lowercase, no spaces
- Use the platform's common name or abbreviation
- Be specific about the origin

**Standard source values:**

| Traffic origin | utm_source |
|---------------|-----------|
| Google (paid) | `google` |
| Bing Ads | `bing` |
| Facebook Ads | `facebook` |
| Instagram Ads | `instagram` |
| LinkedIn Ads | `linkedin` |
| Twitter/X Ads | `twitter` |
| TikTok Ads | `tiktok` |
| Pinterest Ads | `pinterest` |
| Newsletter | `newsletter` |
| Weekly digest | `newsletter` (same — use campaign to differentiate) |
| Partner site | `partnersite-name` |
| QR code | `qr` |
| Print ad | `print` |
| Podcast ad | `podcast` |

**Less obvious sources:**
```
utm_source=google           ← Google search or display
utm_source=google-display   ← if you want to distinguish from search
utm_source=direct-mail      ← physical mail campaign
utm_source=conference       ← booth or event
```

## utm_medium

Medium identifies **how** the traffic arrived — the marketing channel type.

For more on this topic, see [*How to Track Marketing Campaigns: A Complete Guide with UTMs*](/blog/how-to-track-marketing-campaigns).

**Rules:**
- Lowercase
- Standardize across all channels — GA4 uses medium values to define channel groups
- Stick to recognized values for GA4's default channel groupings to work correctly

**Standard medium values (GA4-compatible):**

| Channel | utm_medium |
|---------|-----------|
| Paid search (Google/Bing) | `cpc` |
| Paid social | `paid-social` or `cpc` |
| Organic social | `social` |
| Email newsletter | `email` |
| Display advertising | `display` or `banner` |
| Affiliate | `affiliate` |
| Referral from another site | `referral` |
| QR code | `qr` |
| Push notification | `push` |
| SMS marketing | `sms` |
| In-app notification | `in-app` |

For more on this topic, see [*UTM Tracking: How to Set Up and Measure Marketing Campaigns*](/blog/utm-tracking).

**GA4 channel grouping — how medium maps to channels:**

| utm_medium value | GA4 channel group |
|-----------------|------------------|
| `cpc`, `ppc`, `paidsearch` | Paid Search |
| `social`, `social-network` | Organic Social |
| `paid-social` | Paid Social |
| `email`, `newsletter` | Email |
| `banner`, `display` | Display |
| `affiliate` | Affiliates |
| `referral` | Referral |
| `organic` (shouldn't be used manually) | Organic Search |

Using non-standard medium values (like `paid_social` with underscore instead of hyphen) may cause GA4 to classify traffic as "Unassigned" instead of mapping to a channel group.

## utm_campaign

Campaign identifies **which marketing effort** drove the traffic. This is the name of your campaign, promotion, or content initiative.

**Rules:**
- Lowercase, hyphens for spaces
- Include a date or quarter for time-bounded campaigns
- Be descriptive but concise

**Campaign naming patterns:**

```
# Email campaigns
utm_campaign=weekly-newsletter-2026-04
utm_campaign=product-launch-april-2026
utm_campaign=spring-sale-q2-2026

# Paid campaigns
utm_campaign=brand-awareness-q2
utm_campaign=retargeting-cart-abandoners
utm_campaign=competitor-comparison-ads

# Social campaigns
utm_campaign=influencer-partnership-may
utm_campaign=ugc-contest-2026

# Content/SEO promotions
utm_campaign=ebook-lead-magnet
utm_campaign=webinar-registration
```

**Naming conventions to avoid:**

```
# Too vague
utm_campaign=sale
utm_campaign=email

# Include dates for time-bounded campaigns
utm_campaign=spring         ← which spring?
utm_campaign=spring-2026    ← better
```

## Putting it all together

**Email newsletter:**
```
utm_source=newsletter&utm_medium=email&utm_campaign=spring-sale-2026
```

**Google paid search:**
```
utm_source=google&utm_medium=cpc&utm_campaign=brand-keywords-q2
```

**Organic Facebook post:**
```
utm_source=facebook&utm_medium=social&utm_campaign=product-launch-april
```

**Facebook paid ad:**
```
utm_source=facebook&utm_medium=paid-social&utm_campaign=retargeting-q2
```

**LinkedIn content promotion:**
```
utm_source=linkedin&utm_medium=social&utm_campaign=thought-leadership-2026
```

For more on this topic, see [*UTM Parameters Explained: Source, Medium, Campaign, Content, Term*](/blog/utm-parameters).

**QR code on packaging:**
```
utm_source=qr&utm_medium=print&utm_campaign=product-packaging-2026&utm_content=back-panel
```

## A reference table to copy

| Channel | utm_source | utm_medium | utm_campaign |
|---------|-----------|-----------|-------------|
| Google Ads (search) | google | cpc | [campaign-name] |
| Google Display | google | display | [campaign-name] |
| Bing Ads | bing | cpc | [campaign-name] |
| Facebook paid | facebook | paid-social | [campaign-name] |
| Facebook organic | facebook | social | [campaign-name] |
| Instagram paid | instagram | paid-social | [campaign-name] |
| LinkedIn paid | linkedin | paid-social | [campaign-name] |
| LinkedIn organic | linkedin | social | [campaign-name] |
| Newsletter | newsletter | email | [campaign-name] |
| Transactional email | [platform] | email | transactional |
| Partner referral | [partner-name] | referral | partner-program |
| QR code (print) | qr | print | [placement] |
| Podcast ad | [podcast-name] | podcast | [campaign-name] |

Build UTM links with consistent values at [utmbuilder.io](/).
