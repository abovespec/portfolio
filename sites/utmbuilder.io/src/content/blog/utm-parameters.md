---
title: "UTM Parameters Explained: Source, Medium, Campaign, Content, Term"
description: "Learn what UTM parameters are and how each one works: utm_source, utm_medium, utm_campaign, utm_content, and utm_term with examples and best practices."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["utm", "utm parameters", "google analytics", "campaign tracking", "marketing"]
draft: false
---

UTM parameters are tags you add to URLs that tell your analytics tool where visitors came from. When someone clicks a UTM-tagged link, Google Analytics (and other tools) capture those values and associate them with the session.

## The five UTM parameters

### utm_source

**What:** Identifies the origin — where traffic is coming from.

**Required:** Yes

**Examples:**
```
utm_source=google
utm_source=facebook
utm_source=newsletter
utm_source=linkedin
utm_source=partner-site
```

Think of it as the referring website or platform.

### utm_medium

**What:** Identifies the marketing channel or medium.

**Required:** Yes

**Examples:**
```
utm_medium=cpc          ← paid search (cost per click)
utm_medium=email        ← email campaign
utm_medium=social       ← organic social media
utm_medium=banner       ← display advertising
utm_medium=affiliate    ← affiliate partner
utm_medium=referral     ← from another website
utm_medium=qr           ← physical QR code
```

Medium is the type of traffic, not the platform. Facebook organic posts and Facebook ads should have the same source (`facebook`) but different mediums (`social` vs. `cpc`).

### utm_campaign

**What:** Identifies the specific marketing campaign.

**Required:** Yes

**Examples:**
```
utm_campaign=spring-sale-2026
utm_campaign=product-launch-april
utm_campaign=newsletter-weekly
utm_campaign=retargeting-cart-abandoners
```

Use descriptive, consistent names. Your campaign name should make sense 6 months later when you're reviewing reports.

### utm_content

**What:** Differentiates between multiple links in the same campaign. Used for A/B testing or distinguishing ad variants.

**Required:** No (optional)

**Examples:**
```
utm_content=blue-cta-button
utm_content=hero-image-link
utm_content=footer-link
utm_content=version-a
utm_content=top-banner
```

If you have two different ads in the same campaign, `utm_content` tells you which one drove the conversion.

### utm_term

**What:** Identifies the paid search keyword that triggered the ad.

**Required:** No (usually set automatically by Google Ads)

**Examples:**
```
utm_term=buy+running+shoes
utm_term=best+crm+software
utm_term=project+management+tool
```

Primarily used for paid search campaigns. For Google Ads, you can use `{keyword}` as a ValueTrack parameter to auto-populate this.

## How UTM parameters are added to a URL

Append parameters after a `?` with `&` between them:

```
Base URL: https://example.com/landing-page

With UTMs:
https://example.com/landing-page?utm_source=newsletter&utm_medium=email&utm_campaign=spring-sale-2026
```

**Special characters must be URL-encoded:**
- Spaces → `%20` or `+`
- Ampersand → `%26`
- Equals → `%3D`

Use a UTM builder at [utmbuilder.io](/) to handle encoding automatically.

## Complete example URL

Email campaign for a spring sale:

```
https://example.com/spring-sale?utm_source=newsletter&utm_medium=email&utm_campaign=spring-sale-2026&utm_content=hero-cta&utm_term=
```

Or with a specific product target:

```
https://example.com/product/blue-widget?utm_source=google&utm_medium=cpc&utm_campaign=widget-ads&utm_content=blue-button&utm_term=buy+blue+widget
```

## Where to see UTM data in GA4

1. Go to **Reports** → **Acquisition** → **Traffic acquisition**
2. Set the dimension to "Session source / medium" or "Session campaign"
3. Filter by date range

You can also see UTM data in:
- **Acquisition** → **Campaign acquisition** → filter by campaign name
- **Explore** → create a custom exploration with UTM dimensions

## UTM parameter naming conventions

Consistency is critical — `Email` and `email` are tracked as different values in most analytics tools.

**Rules:**
1. **Lowercase everything** — `email`, not `Email` or `EMAIL`
2. **Use hyphens** instead of spaces or underscores — `spring-sale`, not `spring_sale` or `spring sale`
3. **Be specific but not too granular** — `newsletter` is better than `weekly-newsletter-issue-47`
4. **Document your conventions** — use a shared naming spreadsheet

Build UTM links at [utmbuilder.io](/).
