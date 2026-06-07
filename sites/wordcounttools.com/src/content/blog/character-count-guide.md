---
title: "Character Count: Limits for Every Platform and Use Case"
description: "Character count limits for Twitter, Instagram, SMS, meta descriptions, email subjects, and more. Plus how to count characters accurately including vs. excluding spaces."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["character count", "writing", "seo", "social media", "text limits"]
draft: false
---

Character count matters anywhere text appears in a constrained space: social posts, SMS, meta tags, email subjects, and database fields. Here are the definitive limits for every common context.

## Social media character limits

| Platform | Limit | Notes |
|----------|-------|-------|
| Twitter / X | 280 characters | Basic accounts; verified get more |
| Twitter / X (paid) | 25,000 characters | X Premium (Blue) articles |
| Instagram caption | 2,200 characters | Display truncated at ~125 |
| Instagram bio | 150 characters | |
| Facebook post | 63,206 characters | Practically unlimited for most uses |
| Facebook ad primary text | 125 characters | Before "See more" truncation |
| LinkedIn post | 3,000 characters | |
| LinkedIn article | 125,000 characters | Long-form |
| LinkedIn headline | 220 characters | |
| YouTube title | 100 characters | ~70 displayed in search |
| YouTube description | 5,000 characters | ~157 shown in search snippet |
| TikTok caption | 2,200 characters | |
| Pinterest description | 500 characters | ~75-100 visible in feed |
| Reddit post title | 300 characters | |

For more on this topic, see [*How Long Should a Blog Post Be for SEO in 2026?*](/blog/how-long-should-a-blog-post-be).

## SEO and web character limits

| Field | Recommended | Maximum | Notes |
|-------|------------|---------|-------|
| Title tag | 50–60 chars | ~580px width | Google truncates at ~580px; ~60 chars at 16px font |
| Meta description | 150–160 chars | ~920px width | Google truncates; use 155 chars as target |
| Open Graph title | 40–60 chars | — | Truncation varies by platform |
| Open Graph description | 200 chars | — | Facebook/LinkedIn |
| URL slug | 50–75 chars | — | Shorter is better |
| H1 heading | No hard limit | — | ~60 chars works well in practice |
| Alt text | 125 chars | — | Screen reader guideline |

## Email character limits

| Field | Recommended | Maximum | Notes |
|-------|------------|---------|-------|
| Subject line | 40–50 chars | ~998 chars (RFC 5321) | Mobile shows ~30–40 on lock screen |
| Preview text | 40–100 chars | — | Varies by email client |
| From name | ~20 chars | — | Mobile truncation |

**Subject line display by device:**
- Gmail desktop: ~77 chars with preview text combined
- Gmail mobile: ~30 chars in notification
- Apple Mail iPhone: ~35 chars in inbox view
- Outlook desktop: varies by window size

The most-opened subject lines tend to be under 50 characters — long enough to be descriptive, short enough to display fully on mobile.

## SMS character limits

SMS uses two encodings:

**GSM-7** (standard characters — letters, digits, basic punctuation): 160 characters per message. Multi-part SMS splits at 153 characters per segment (7 chars for headers).

**UCS-2** (Unicode — emojis, non-Latin scripts): 70 characters per message. Multi-part at 67 per segment.

If your SMS contains a single emoji or any character outside GSM-7's character set, the entire message switches to UCS-2 and your 160-char message becomes a 70-char message.

Common characters that trigger UCS-2:
- Any emoji
- Smart quotes (" ") — use `"` instead
- Em dash (—) — use `-` instead
- Accented characters beyond basic Western Latin

## Database and API character limits

| Context | Limit | Notes |
|---------|-------|-------|
| PostgreSQL VARCHAR | 10,485,760 chars | Practical limit is usually column definition |
| MySQL VARCHAR | 65,535 bytes | |
| SQL Server NVARCHAR(MAX) | ~1.07 billion chars | |
| JSON string | No spec limit | Practical limits from parser/framework |
| AWS DynamoDB item | 400 KB total | |
| URL (practical) | 2,048 chars | IE limit; browsers vary |
| Cookie value | 4,096 bytes | |
| HTTP header value | 8 KB (Apache/Nginx default) | |
| Git commit message subject | 50 chars | Soft convention; 72 for body lines |
| Excel cell | 32,767 chars | |

## Characters with spaces vs. without

Most word processors and character counters offer both:

- **Characters with spaces:** Every character, including spaces. This is the raw character count.
- **Characters without spaces:** Only non-space characters. This is the "printable character" count.

For more on this topic, see [*How to Check Word Count in Google Docs (Every Method)*](/blog/word-count-google-docs).

For SEO meta lengths, Google measures in *pixel width*, not character count. A title with many narrow letters (`i`, `l`, `1`) fits more characters than one with wide letters (`W`, `M`). Tools like [wordcounttools.com](/) show character counts; for pixel-precise SEO preview, use a SERP preview tool.

For more on this topic, see [*How Many Words Is a Novel? Genre-by-Genre Word Count Guide*](/blog/how-many-words-in-a-novel).

## How to count characters accurately

**Command line:**

```bash
# Characters (including newlines)
echo -n "hello world" | wc -c    # -c = bytes (= chars for ASCII)

# For Unicode text, use Python:
python3 -c "print(len('hello world'))"   # 11
python3 -c "print(len('café'))"          # 4 (one char per codepoint)
```

**Python:**

```python
text = "Hello, world!"
len(text)                              # 13 (with spaces)
len(text.replace(" ", ""))            # 12 (without spaces)
len(text.replace(" ", "").replace(",", "").replace("!", ""))  # 10 (letters only)
```

**JavaScript:**

```js
const text = "Hello, world!";
text.length              // 13 (with spaces)
text.replace(/\s/g, '').length  // 12 (no spaces)
```

Note: JavaScript `.length` counts UTF-16 code units. Emoji and some special characters count as 2:

```js
"😀".length     // 2 in JavaScript (it's a surrogate pair)
[..."😀"].length // 1 — correct grapheme count using spread
```

For accurate character counting with emoji, use `[...text].length` in JavaScript.

## Quick character count

Paste any text into [wordcounttools.com](/) to get character counts (with and without spaces), word count, reading time, and more.
