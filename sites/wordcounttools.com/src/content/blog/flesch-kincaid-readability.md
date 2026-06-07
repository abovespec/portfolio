---
title: "Flesch-Kincaid Readability Score: What It Means and How to Improve It"
description: "The Flesch Reading Ease and Flesch-Kincaid Grade Level formulas explained. How the scores are calculated, what the numbers mean, and how to write for your target audience."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["readability", "flesch kincaid", "writing quality", "content writing", "seo"]
draft: false
---

The Flesch Reading Ease score and Flesch-Kincaid Grade Level are the most widely used readability metrics in English writing. Microsoft Word, Hemingway App, and most SEO tools include them. Here's how they work and what to do with the numbers.

## Flesch Reading Ease

The **Flesch Reading Ease** score (developed by Rudolf Flesch in 1948) predicts how easy text is to read on a scale of 0–100. Higher = easier.

**Formula:**

```
Score = 206.835 - (1.015 × ASL) - (84.6 × ASW)

ASL = Average Sentence Length (words per sentence)
ASW = Average Syllables per Word
```

For more on this topic, see [*Average Words Per Minute for Reading: What the Research Says*](/blog/average-words-per-minute-reading).

**Score interpretation:**

| Score | Difficulty | Notes |
|-------|-----------|-------|
| 90–100 | Very easy | 5th grade; comic books, basic English |
| 80–90 | Easy | 6th grade; conversational English |
| 70–80 | Fairly easy | 7th grade; typical newspaper |
| 60–70 | Standard | 8th–9th grade; plain language goal |
| 50–60 | Fairly difficult | 10th–12th grade; academic magazines |
| 30–50 | Difficult | College level; academic writing |
| 0–30 | Very difficult | Graduate level; professional/scientific |

**Example scores:**

- Time magazine: ~50–60
- Harvard Law Review: ~30
- IKEA instructions: ~60–70
- Stephen King's *The Shining*: ~70
- US tax code: ~10–20

## Flesch-Kincaid Grade Level

The **Flesch-Kincaid Grade Level** (developed by Kincaid et al. in 1975 for the US Navy) converts the Flesch score to a US school grade level.

**Formula:**

```
Grade = (0.39 × ASL) + (11.8 × ASW) - 15.59
```

A score of 8 means the text is readable by someone with an 8th-grade education. A score of 12 corresponds to high school senior; 13+ corresponds to college-level reading.

**Example grade levels:**

- Sports page: grade 9
- Reader's Digest: grade 9–11
- Time magazine: grade 12
- New England Journal of Medicine: grade 17–18
- Most government documents: grade 14–16

## How to use these scores

The "right" score depends on your audience:

| Audience | Target Flesch Score | Target Grade Level |
|----------|--------------------|--------------------|
| General public / blog | 60–70 | 7–9 |
| News / journalism | 50–60 | 9–12 |
| Business communication | 50–65 | 8–11 |
| Technical documentation | 40–55 | 10–14 |
| Academic journals | 30–45 | 13–17 |
| Legal/medical | 20–40 | 14+ |

**Plain language guidelines** (used by US federal agencies under the [Plain Writing Act of 2010](https://www.plainlanguage.gov/)) target grade 8 or below for public-facing content — Flesch Reading Ease 60+.

For more on this topic, see [*What Is Flesch-Kincaid Readability? A Plain-Language Guide*](/blog/what-is-flesch-kincaid-readability).

## What drives the score

Only two variables matter:

1. **Sentence length** (ASL) — longer sentences lower the score
2. **Syllables per word** (ASW) — polysyllabic words lower the score

The formulas ignore:
- Word familiarity (a long familiar word vs. a short technical one)
- Sentence structure complexity (passive vs. active)
- Paragraph structure
- Visual organization (bullets, headers)

This means the score is a proxy, not a complete readability measure. You can game the Flesch score by shortening sentences without actually improving clarity. Use it as a signal, not a goal.

## How to improve your score

**Reduce average sentence length:**

Cut long sentences in half at conjunctions (and, but, because, when, while). Aim for an average of 15–20 words per sentence. A mix of short and long sentences reads better than uniform length.

```
Before: "The platform allows users to configure their notification preferences, 
including the frequency of alerts, the channels through which they receive 
them, and the types of events that will trigger a notification."

After: "Configure your notification preferences in Settings. You can set 
alert frequency, choose delivery channels, and pick which events trigger 
a notification."
```

**Replace polysyllabic words with simpler alternatives:**

| Complex | Simpler |
|---------|---------|
| utilize | use |
| facilitate | help |
| commence | start |
| endeavor | try |
| approximately | about |
| subsequently | then, next |
| demonstrate | show |
| additional | more |

**Use active voice:**

Active voice uses fewer syllables and shorter sentence structures:

```
Passive: "The configuration was updated by the system administrator."
Active:  "The system administrator updated the configuration."
```

**Break up long paragraphs:**

Paragraph breaks give readers a rest point. Three to five sentences per paragraph is a common guideline for online writing.

## Calculating readability

**Microsoft Word:** Review → Check Document → Spelling & Grammar → Shows Flesch scores in the summary.

**Hemingway App:** Paste text at hemingwayapp.com for grade level and highlighted problem sentences.

**Online:** Paste into [wordcounttools.com](/) to see Flesch Reading Ease, Flesch-Kincaid Grade Level, and other readability metrics alongside word count and reading time.

For more on this topic, see [*Reading Time Calculator: How Long Will Readers Spend on Your Content?*](/blog/reading-time-calculator).

**Python:**

```python
import textstat

text = "Your article text here..."
print(textstat.flesch_reading_ease(text))   # 0–100
print(textstat.flesch_kincaid_grade(text))  # US grade level
```

## Other readability metrics

Flesch-Kincaid is the most common, but several others exist:

- **Gunning Fog Index** — similar to FK grade level; focuses on complex words
- **SMOG Index** — counts polysyllabic words; common in health writing
- **Coleman-Liau Index** — uses characters instead of syllables; works on text where syllabification is hard
- **Dale-Chall Formula** — uses a list of "familiar" words; better for estimating comprehension rather than just difficulty

No single metric is definitive. Use them as sanity checks, not as absolute targets.
