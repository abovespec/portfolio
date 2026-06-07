---
title: "How to Track Marketing Campaigns: A Complete Guide with UTMs"
description: "Learn how to track marketing campaigns end-to-end with UTM parameters. Covers campaign planning, UTM setup, GA4 reporting, and measuring ROI by channel."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["campaign tracking", "utm", "marketing analytics", "ga4", "roi"]
draft: false
---

Tracking marketing campaigns answers the question: "Which of our marketing efforts actually drive revenue?" Without tracking, you're guessing. With it, you can cut what doesn't work and scale what does.

## The tracking stack

A complete campaign tracking setup has three layers:

1. **UTM parameters** — tag your links with campaign info
2. **Analytics platform** — Google Analytics 4 reads UTM values and stores them
3. **Conversion tracking** — mark which events (purchase, signup, lead form) count as conversions

For more on this topic, see [*UTM Tracking: How to Set Up and Measure Marketing Campaigns*](/blog/utm-tracking).

When someone clicks a UTM-tagged link and converts, you can trace that conversion back to the specific campaign, ad, or email that drove it.

## Step 1: Set up GA4

If you haven't already:
1. Create a GA4 property at analytics.google.com
2. Install the GA4 tracking code on your website (or via Google Tag Manager)
3. Verify it's working with the Realtime report

GA4 reads UTM parameters automatically — no additional plugin needed.

## Step 2: Define your tracking plan

Before creating UTM links, decide on naming conventions:

```
Document your standards:

SOURCES:         google, bing, facebook, instagram, linkedin, newsletter, qr
MEDIUMS:         cpc, paid-social, social, email, display, referral, print, qr
CAMPAIGN FORMAT: [initiative]-[month/quarter]-[year]
                 e.g., spring-sale-q2-2026, brand-awareness-q3-2026
```

Share this with everyone who creates links. Inconsistency in naming makes your data unreliable.

## Step 3: Create UTM-tagged links

For each marketing asset that links to your site:

**Email campaign:**
```
https://example.com/offer?utm_source=newsletter&utm_medium=email&utm_campaign=spring-sale-q2-2026&utm_content=hero-button
```

For more on this topic, see [*UTM Parameters Explained: Source, Medium, Campaign, Content, Term*](/blog/utm-parameters).

**Paid search ad:**
```
https://example.com/product?utm_source=google&utm_medium=cpc&utm_campaign=brand-keywords-q2-2026&utm_term={keyword}
```

**Social media post:**
```
https://example.com/blog/post?utm_source=linkedin&utm_medium=social&utm_campaign=content-marketing-2026
```

Use [utmbuilder.io](/) to build and validate links before publishing.

## Step 4: Mark conversions in GA4

For campaign ROI to make sense, you need to track conversions:

**Admin → Events** — find the event that represents a successful outcome:
- `purchase` — for e-commerce
- `generate_lead` — for lead generation
- `sign_up` — for registrations
- `form_submit` — for contact forms

Toggle "Mark as conversion" for each relevant event.

## Step 5: Use UTM link tracking spreadsheet

Maintain a running log of all UTM links you create:

For more on this topic, see [*UTM Builder Guide: How to Create and Manage UTM Links*](/blog/utm-builder-guide).

| Date | Campaign | Channel | utm_source | utm_medium | utm_campaign | Full URL |
|------|---------|---------|-----------|-----------|-------------|---------|
| 2026-04-25 | Spring Sale | Email | newsletter | email | spring-sale-q2-2026 | https://... |
| 2026-04-25 | Spring Sale | Google Ads | google | cpc | spring-sale-q2-2026 | https://... |

This serves as a reference when analyzing data — you can look up which UTM values map to which campaign.

## Step 6: Measure campaign performance

In GA4, open **Reports → Acquisition → Traffic acquisition** and change the primary dimension to "Session campaign."

Key metrics to evaluate each campaign:

| Metric | What it tells you |
|--------|------------------|
| Sessions | Volume of traffic |
| Engaged sessions | Quality of traffic |
| Engagement rate | % of sessions that engaged |
| Conversions | Goal completions |
| Conversion rate | Conversions / sessions |
| Total revenue | Revenue attributed (e-commerce) |

Compare campaigns against each other. Which has the highest conversion rate? Which has the lowest cost-per-conversion?

## Step 7: Calculate ROI by channel

To connect spend to conversions:

1. Export GA4 campaign data (conversions + revenue by utm_campaign)
2. Match campaign names to ad spend in your advertising platform
3. Calculate ROI: `(Revenue - Spend) / Spend × 100`

```python
campaigns = {
    'spring-sale-google': {'spend': 5000, 'revenue': 18000},
    'spring-sale-facebook': {'spend': 3000, 'revenue': 7500},
    'spring-sale-email': {'spend': 500, 'revenue': 12000},
}

for name, data in campaigns.items():
    roi = (data['revenue'] - data['spend']) / data['spend'] * 100
    roas = data['revenue'] / data['spend']
    print(f"{name}: ROI={roi:.0f}%, ROAS={roas:.1f}x")
```

```
spring-sale-google:   ROI=260%, ROAS=3.6x
spring-sale-facebook: ROI=150%, ROAS=2.5x
spring-sale-email:    ROI=2300%, ROAS=24x
```

## Common tracking failures

**Redirects stripping UTMs:** If your marketing URL redirects to the final destination, UTMs may be dropped. Always put UTMs on the final destination URL, not an intermediate redirect.

**Server-side redirects:** A 301 redirect from `example.com` to `www.example.com` can strip UTM parameters. Verify your redirects pass query strings.

**Conversions on external domains:** If your checkout is on a different domain (e.g., `pay.example.com`), you need cross-domain tracking configured in GA4.

**UTMs on internal links:** Don't add UTMs to links between pages on your own site. It overwrites the original campaign attribution for the session.

Build and manage UTM links at [utmbuilder.io](/).
