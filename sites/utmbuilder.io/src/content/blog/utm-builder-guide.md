---
title: "UTM Builder Guide: How to Create and Manage UTM Links"
description: "Learn how to use a UTM builder to create tracked marketing links. Covers the online builder tool, bulk UTM generation in Google Sheets, and link management tips."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["utm builder", "utm link", "campaign tracking", "marketing", "google sheets"]
draft: false
---

A UTM builder helps you create properly formatted tracking URLs without manually typing parameter strings. This guide covers online builders, Google Sheets automation, and link management.

## Using an online UTM builder

[utmbuilder.io](/) lets you fill in fields and generates the complete URL:

1. **Website URL** — your destination page (without UTM parameters)
2. **Campaign source** — where traffic comes from
3. **Campaign medium** — the channel type
4. **Campaign name** — your campaign identifier
5. **Campaign content** (optional) — for A/B testing
6. **Campaign term** (optional) — for paid search keywords

The builder automatically:
- Encodes special characters
- Combines fields into a valid URL
- Lets you copy with one click

**Example output:**

```
Input:
  URL: https://example.com/sale
  Source: newsletter
  Medium: email
  Campaign: spring-sale-2026
  Content: hero-button

Output:
  https://example.com/sale?utm_source=newsletter&utm_medium=email&utm_campaign=spring-sale-2026&utm_content=hero-button
```

## Google Sheets UTM builder

For campaigns with many links (product pages, multiple ads), build a spreadsheet formula:

```
Columns:
A: Base URL
B: utm_source
C: utm_medium
D: utm_campaign
E: utm_content (optional)
F: Generated URL

Formula in F2:
=A2&"?utm_source="&LOWER(B2)&"&utm_medium="&LOWER(C2)&"&utm_campaign="&LOWER(D2)&IF(E2<>"","&utm_content="&LOWER(E2),"")
```

This generates the full UTM URL for each row. Add more rows for additional links, and the formula handles encoding automatically.

**With URL encoding for special characters:**

```
=A2&"?utm_source="&ENCODEURL(LOWER(B2))&"&utm_medium="&ENCODEURL(LOWER(C2))&"&utm_campaign="&ENCODEURL(LOWER(D2))
```

`ENCODEURL()` in Google Sheets converts spaces to `%20` and handles special characters.

## Bulk UTM generation with Python

For programmatic bulk generation:

```python
from urllib.parse import urlencode, urlparse, urljoin

def build_utm_url(
    base_url: str,
    source: str,
    medium: str,
    campaign: str,
    content: str = None,
    term: str = None,
) -> str:
    params = {
        'utm_source': source.lower(),
        'utm_medium': medium.lower(),
        'utm_campaign': campaign.lower(),
    }
    if content:
        params['utm_content'] = content.lower()
    if term:
        params['utm_term'] = term.lower()

    separator = '&' if '?' in base_url else '?'
    return f"{base_url}{separator}{urlencode(params)}"


# Generate multiple variants
campaigns = [
    ('google', 'cpc', 'spring-sale-2026', None),
    ('facebook', 'paid-social', 'spring-sale-2026', 'carousel-ad'),
    ('newsletter', 'email', 'spring-sale-2026', 'hero-cta'),
    ('linkedin', 'social', 'spring-sale-2026', None),
]

base = 'https://example.com/spring-sale'
for source, medium, campaign, content in campaigns:
    url = build_utm_url(base, source, medium, campaign, content)
    print(url)
```

Output:
```
https://example.com/spring-sale?utm_source=google&utm_medium=cpc&utm_campaign=spring-sale-2026
https://example.com/spring-sale?utm_source=facebook&utm_medium=paid-social&utm_campaign=spring-sale-2026&utm_content=carousel-ad
https://example.com/spring-sale?utm_source=newsletter&utm_medium=email&utm_campaign=spring-sale-2026&utm_content=hero-cta
https://example.com/spring-sale?utm_source=linkedin&utm_medium=social&utm_campaign=spring-sale-2026
```

## Managing your UTM links

**Track all links in a spreadsheet.** Keep a log with:
- Date created
- Campaign name
- Channel
- Full UTM URL
- Notes (which ad, email, or post used it)

This becomes essential when reviewing analytics 6 months later and trying to remember what `utm_campaign=q2-promo` referred to.

**Use descriptive campaign names.** `spring-sale-2026-email-blast` is better than `sale`.

**Don't add UTMs to internal links.** UTMs on links between pages on your own site reset the session attribution. Only add UTMs to links in external marketing materials.

**Validate before publishing:**
1. Paste the URL in your browser — confirm the page loads
2. Check the URL bar — UTM parameters should be visible
3. Verify in GA4 Realtime — see your session with correct UTM values

## Link shorteners and UTMs

If you need short URLs for social media, add UTMs to the destination URL, then shorten the UTM URL (not the base URL):

```
1. Build UTM URL: https://example.com/sale?utm_source=twitter&utm_medium=social&utm_campaign=spring-2026
2. Shorten: bit.ly/abc123 → redirects to the above UTM URL
```

The shortener redirect passes through to the UTM URL, so GA4 still captures the parameters.

Some link shorteners (Bit.ly, Rebrandly) have built-in UTM builders — you can add UTM fields directly in their dashboard when creating a short link.

Build UTM links at [utmbuilder.io](/).
