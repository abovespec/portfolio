---
title: "Reading Time Calculator: How Long Will Readers Spend on Your Content?"
description: "How reading time is calculated, what affects it, average reading speeds by content type, and how to use reading time estimates for better content planning."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["reading time", "word count", "content writing", "blogging", "ux writing"]
draft: false
---

Reading time estimates — "5 min read", "2 min read" — appear on blog platforms, news sites, and reading apps. They're calculated from word count and average reading speed. Here's how the math works and why it matters for content planning.

## The formula

```
Reading time = Word count ÷ Average reading speed (WPM)
```

**Average adult reading speed: 200–250 words per minute** for general online content.

For more on this topic, see [*Average Words Per Page: Every Format Explained*](/blog/average-words-per-page).

Medium uses 265 WPM. Most content tools use 200–250 WPM. Some research-backed estimates put typical adult silent reading at 200–400 WPM depending on reading difficulty and content type.

| Word count | Reading time (at 230 WPM) |
|------------|--------------------------|
| 500 | ~2 min |
| 800 | ~3.5 min |
| 1,000 | ~4.5 min |
| 1,500 | ~6.5 min |
| 2,000 | ~9 min |
| 3,000 | ~13 min |
| 5,000 | ~22 min |

For more on this topic, see [*How to Check Word Count in Google Docs (Every Method)*](/blog/word-count-google-docs).

## Reading speed varies by content type

The 200–250 WPM figure applies to average prose. Content difficulty significantly affects reading speed:

| Content type | Typical reading speed |
|-------------|----------------------|
| Easy fiction, news | 250–300 WPM |
| General nonfiction | 200–250 WPM |
| Technical content / code | 100–150 WPM |
| Academic papers | 100–200 WPM |
| Dense legal/scientific text | 50–100 WPM |

Code blocks, tables, and diagrams require more processing time per "word" than flowing prose. A technical tutorial with 1,500 words and 10 code blocks will take longer to read than a 1,500-word narrative essay.

Some reading time tools adjust for this: they add extra time per code block (typically 30 seconds per block) rather than treating code words identically to prose words.

## Why reading time matters for content strategy

**Blog posts:** Medium originally popularized reading time display to help readers decide upfront whether to commit to an article. Research suggested that posts with displayed reading times had higher engagement and lower bounce rates on longer content — readers who started a long article had opted in to spending time.

**Email newsletters:** Subject line reading time hints ("3 min read") can set expectations and improve open rates for longer email content.

**Slide decks and presentations:** At an average speaking pace of 130–150 words per minute, a 10-minute talk requires roughly 1,300–1,500 words of written content. Use this to estimate speech length from scripts or vice versa.

**SEO content length:** Reading time is a proxy for content depth. Articles targeting competitive keywords typically need 1,500–3,000 words (6–13 minutes of reading) to compete. Very competitive queries often require 3,000+ words. Short content (< 500 words) rarely ranks for head keywords.

## How much detail is appropriate?

There's no universally optimal reading time. Match content depth to the reader's intent:

- **Navigational queries** ("how to open Google Docs") — 300–500 words is usually enough
- **Informational definitions** ("what is snake case") — 600–1,000 words
- **How-to guides** — 1,000–2,000 words
- **Comparison articles** — 1,500–3,000 words
- **Comprehensive reference guides** — 2,000–5,000 words

Padding thin content with filler to hit a word count target doesn't help. Thin + padded = still thin. Depth comes from covering the topic thoroughly, not from repeating ideas or adding unrelated sections.

## Reading speed by education and language

Research from [Rayner et al. (2016)](https://journals.sagepub.com/doi/10.1177/1529100615623200) found that average silent reading speed for college students in English was approximately 300 WPM. Non-native speakers typically read 15–30% slower.

Audience considerations:
- **Native speaker, native language:** 250–300 WPM
- **ESL reader:** 180–220 WPM
- **Technical expert reading their domain:** Up to 400+ WPM (skimming familiar content)
- **General audience, dense content:** 150–200 WPM

For international audiences or technical content, consider aiming for shorter average sentence length (15–20 words) and plain language, which improves both reading speed and comprehension.

For more on this topic, see [*What Is Flesch-Kincaid Readability? A Plain-Language Guide*](/blog/what-is-flesch-kincaid-readability).

## Displaying reading time

**Implementing in code (JavaScript):**

```js
function readingTime(text, wpm = 230) {
  const words = text.trim().split(/\s+/).length;
  const minutes = Math.ceil(words / wpm);
  return `${minutes} min read`;
}

readingTime("Lorem ipsum dolor sit amet..."); // "1 min read"
```

**Python:**

```python
import math

def reading_time(text: str, wpm: int = 230) -> str:
    words = len(text.split())
    minutes = math.ceil(words / wpm)
    return f"{minutes} min read"
```

For articles with code blocks, add an adjustment:

```python
import re, math

def reading_time(text: str, wpm: int = 230) -> str:
    code_blocks = re.findall(r'```[\s\S]*?```', text)
    # Remove code from prose and add 30 sec per block
    prose = re.sub(r'```[\s\S]*?```', '', text)
    words = len(prose.split())
    minutes = words / wpm + len(code_blocks) * 0.5
    return f"{math.ceil(minutes)} min read"
```

## Calculate reading time now

Paste your article into [wordcounttools.com](/) to see the estimated reading time alongside word count, character count, and readability score.
