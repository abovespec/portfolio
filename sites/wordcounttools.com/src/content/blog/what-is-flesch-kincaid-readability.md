---
title: "What Is Flesch-Kincaid Readability? A Plain-Language Guide"
description: "Flesch-Kincaid readability scores measure how easy text is to read. Here's what the formulas calculate, what the numbers mean, and how to improve your score."
publishDate: 2026-05-22
updatedDate: 2026-05-22
author: "Editorial Team"
tags: ["readability", "flesch kincaid", "writing quality", "content writing", "seo", "plain language"]
draft: false
---

Flesch-Kincaid is a readability formula — a mathematical way to estimate how difficult a piece of writing is to read. It's built into Microsoft Word, Hemingway App, Grammarly, and most SEO tools. Understanding it helps you write content matched to your audience.

## There are two Flesch-Kincaid scores

The "Flesch-Kincaid" name covers two distinct formulas that measure slightly different things:

1. **Flesch Reading Ease** — scores from 0 to 100; higher = easier to read
2. **Flesch-Kincaid Grade Level** — outputs a US school grade level; lower = easier

They use the same two variables: average sentence length and average syllables per word.

## Flesch Reading Ease: the 0–100 scale

Developed by Rudolf Flesch in 1948, the Reading Ease score predicts how easily a typical adult can read a piece of text.

**The formula:**

```
Score = 206.835 − (1.015 × ASL) − (84.6 × ASW)

ASL = Average Sentence Length (words per sentence)
ASW = Average Syllables per Word
```

**Score interpretation:**

| Score | Reading level | Typical audience |
|-------|--------------|-----------------|
| 90–100 | Very easy | 5th grade; children's books |
| 80–90 | Easy | 6th grade; plain English |
| 70–80 | Fairly easy | 7th grade; popular fiction |
| 60–70 | Standard | 8th–9th grade; typical web content |
| 50–60 | Fairly difficult | 10th–12th grade; magazines |
| 30–50 | Difficult | College level; academic writing |
| 0–30 | Very difficult | Graduate level; scientific/legal |

**Real-world benchmarks:**

| Publication / text | Approximate score |
|-------------------|------------------|
| USA Today | ~68 |
| Time magazine | ~52 |
| Harvard Law Review | ~32 |
| IKEA assembly instructions | ~65 |
| US tax code | ~15 |
| Most blog posts (target) | 60–70 |

## Flesch-Kincaid Grade Level

Developed in 1975 by J. Peter Kincaid for the US Navy to assess technical manuals, this formula converts the same variables into a school grade level.

**The formula:**

```
Grade Level = (0.39 × ASL) + (11.8 × ASW) − 15.59
```

A score of 8 means an 8th-grader can read it. A score of 13 means college-level reading. Most plain-language guidelines target grade 8 or below for general public communication.

**Grade level benchmarks:**

| Text | Approximate grade level |
|------|------------------------|
| Simple news article | 7–9 |
| Business email | 8–10 |
| Average blog post | 9–12 |
| Academic journal | 14–18 |
| Legal documents | 16–20+ |
| US plain-language target | ≤ 8 |

The US Plain Writing Act of 2010 requires federal agencies to write public-facing documents at a grade 8 level or below.

## What drives the score — and what it ignores

**Only two variables matter:**
- Sentence length: longer sentences = lower readability score
- Syllable count per word: longer/more complex words = lower score

**What the formula completely ignores:**
- Whether words are familiar or unfamiliar to the reader
- Active vs. passive voice (though shorter active constructions score better incidentally)
- Paragraph and document structure
- Visual organization: headers, bullets, whitespace
- Word order and syntax complexity
- Jargon and technical terminology (a short jargon word scores well even if readers don't know it)

This is the formula's main limitation: you can mechanically improve your Flesch score without actually improving comprehension. Replacing "utilize" with "use" (3 syllables → 1) raises the score — and also genuinely improves the writing. But chopping every long sentence in half regardless of meaning can produce choppy, unclear prose with a high score.

**Use the score as a diagnostic signal, not a goal to optimize.**

## How to improve your readability score

### Shorten sentences

Long sentences are the primary readability killer. Target an average sentence length of 15–20 words. Mix short punchy sentences with longer ones — uniformly short sentences feel robotic; the key is keeping the average down.

Before: "The software allows users to configure the notification settings, including frequency, delivery channels, and the types of events that trigger an alert, through the preferences panel."

After: "Configure notifications in the preferences panel. Set alert frequency, choose delivery channels, and pick which events trigger a notification."

### Replace long words with shorter ones

| Complex | Simpler |
|---------|---------|
| utilize | use |
| commence | start |
| facilitate | help |
| approximately | about |
| subsequently | then |
| demonstrate | show |
| endeavor | try |
| additional | more, extra |
| terminate | end |

Every unnecessary polysyllabic word lowers the score and usually weakens the writing.

### Cut passive voice

Passive: "The document was reviewed by the committee."
Active: "The committee reviewed the document."

Active constructions tend to be shorter and simpler, which improves both the score and the reading experience.

### Break up dense paragraphs

The formulas don't count paragraphs, but readers do. Long unbroken paragraphs slow reading regardless of the sentence lengths within them. Three to five sentences per paragraph is a reasonable target for web content.

## Checking your score

**Microsoft Word:** Go to File → Options → Proofing → check "Show readability statistics." Run spell check; the Flesch scores appear in the summary dialog.

**Hemingway Editor:** Paste your text at hemingwayapp.com. The grade level appears in the sidebar, and the editor highlights problematic sentences.

**Online:** Paste into [wordcounttools.com](/) to see the Flesch Reading Ease score, Flesch-Kincaid Grade Level, word count, and reading time in one view.

**Python:**

```python
import textstat

text = "Your article text goes here."
print(textstat.flesch_reading_ease(text))   # e.g. 62.4
print(textstat.flesch_kincaid_grade(text))  # e.g. 9.1
```

## When a low score is appropriate

Not all content should score 60+. Technical documentation, academic writing, legal contracts, and medical literature are necessarily complex. A legal contract isn't poorly written because it scores 15 on Reading Ease — it's written for lawyers, not the general public.

Match your target score to your audience:

- General public: aim for 60+ Reading Ease, grade 7–9
- Business readers: 50–65 Reading Ease, grade 9–12
- Technical/specialist audience: 30–55 Reading Ease, grade 12–16
- Academic audience: don't optimize for this score at all — optimize for precision and evidence

The Flesch-Kincaid score is one signal among many. Pair it with user feedback, comprehension testing, and your own editorial judgment for the clearest picture of whether your writing is working.
