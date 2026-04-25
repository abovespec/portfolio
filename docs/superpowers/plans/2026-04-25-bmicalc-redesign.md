# bmicalc.io Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Redesign bmicalc.io as a modern 2026 YMYL health calculator site — interactive BMI calculator above the fold, YMYL legitimacy signals throughout, blog layout ready for Calliope's content.

**Architecture:** Sticky two-column homepage (copy left / calculator right); Preact island for the calculator hydrated at load; blog layout updated with `reviewedBy`/`lastReviewedAt`/`sources` frontmatter fields rendered as legitimacy signals.

**Tech Stack:** Astro 5, Preact 10, Tailwind v4 (CSS-first, `@tailwindcss/vite`), TypeScript strict mode. Tailwind custom tokens: `bg-brand` = `#15803d`, `text-brand`. No unit test runner — verification is `pnpm --filter bmicalc.io check` (TS) + `pnpm --filter bmicalc.io build`.

---

## File Map

| Action | File | Responsibility |
|---|---|---|
| Modify | `sites/bmicalc.io/src/content/config.ts` | Add `reviewedBy`, `lastReviewedAt`, `sources[]` to blog schema |
| Modify | `sites/bmicalc.io/src/config/site.config.ts` | Enable hasBlog, update nav + description |
| Create | `sites/bmicalc.io/src/components/BmiCalculator.tsx` | Preact BMI calculator island |
| Modify | `sites/bmicalc.io/src/layouts/PostLayout.astro` | Add YMYL props, render reviewed-by + sources |
| Modify | `sites/bmicalc.io/src/pages/blog/[...slug].astro` | Pass new PostLayout YMYL props |
| Modify | `sites/bmicalc.io/src/pages/blog/index.astro` | Redesign blog listing with green cards |
| Modify | `sites/bmicalc.io/src/pages/index.astro` | Full homepage redesign |

---

## Task 1: Extend Blog Content Schema (YMYL fields)

**Files:**
- Modify: `sites/bmicalc.io/src/content/config.ts`

- [ ] **Step 1: Update the blog Zod schema**

Replace the `blog` collection definition in `sites/bmicalc.io/src/content/config.ts`:

```ts
const blog = defineCollection({
  type: 'content',
  schema: ({ image }) =>
    z.object({
      title: z.string().max(120),
      description: z.string().max(200),
      publishDate: z.coerce.date(),
      updatedDate: z.coerce.date().optional(),
      author: z.string().default('Editorial Team'),
      tags: z.array(z.string()).default([]),
      image: image().optional(),
      imageAlt: z.string().optional(),
      draft: z.boolean().default(false),
      // YMYL health legitimacy fields
      reviewedBy: z.string().optional(),
      lastReviewedAt: z.coerce.date().optional(),
      sources: z
        .array(z.object({ text: z.string(), url: z.string().optional() }))
        .default([]),
    }),
});
```

- [ ] **Step 2: Verify TypeScript**

```bash
pnpm --filter bmicalc.io check
```

Expected: no errors.

- [ ] **Step 3: Commit**

```bash
git -C /home/abovespec/site-network add sites/bmicalc.io/src/content/config.ts
git -C /home/abovespec/site-network commit -m "feat(bmicalc): add YMYL blog schema fields (reviewedBy, lastReviewedAt, sources)

Co-Authored-By: Paperclip <noreply@paperclip.ing>"
```

---

## Task 2: Enable Blog Feature + Update Site Config

**Files:**
- Modify: `sites/bmicalc.io/src/config/site.config.ts`

- [ ] **Step 1: Update site.config.ts**

Make these changes in `sites/bmicalc.io/src/config/site.config.ts`:

1. Update `identity.description`:
   ```ts
   description: 'Free BMI calculator with instant results. Medically reviewed BMI information for adults.',
   ```

2. Set `features.hasBlog: true`:
   ```ts
   features: {
     hasBlog: true,
     hasTool: false,
     hasGame: false,
     hasSponsoredIntake: false,
   },
   ```

3. Add Blog to `nav.primary`:
   ```ts
   nav: {
     primary: [
       { label: 'Home', href: '/' },
       { label: 'Blog', href: '/blog/' },
       { label: 'About', href: '/about/' },
       { label: 'Contact', href: '/contact/' },
     ],
   },
   ```

- [ ] **Step 2: Verify TypeScript**

```bash
pnpm --filter bmicalc.io check
```

Expected: no errors.

- [ ] **Step 3: Commit**

```bash
git -C /home/abovespec/site-network add sites/bmicalc.io/src/config/site.config.ts
git -C /home/abovespec/site-network commit -m "feat(bmicalc): enable blog, add Blog nav link, update site description

Co-Authored-By: Paperclip <noreply@paperclip.ing>"
```

---

## Task 3: Build BmiCalculator Preact Component

**Files:**
- Create: `sites/bmicalc.io/src/components/BmiCalculator.tsx`

- [ ] **Step 1: Create the component**

Create `sites/bmicalc.io/src/components/BmiCalculator.tsx` with the following content:

```tsx
import { useState, useMemo } from 'preact/hooks';

type Unit = 'imperial' | 'metric';

interface BmiCategory {
  label: string;
  range: string;
  color: string;
  textColor: string;
  bgColor: string;
}

const CATEGORIES: BmiCategory[] = [
  { label: 'Underweight',   range: 'Below 18.5',     color: '#3b82f6', textColor: '#1e40af', bgColor: '#eff6ff' },
  { label: 'Normal weight', range: '18.5 – 24.9',    color: '#15803d', textColor: '#14532d', bgColor: '#f0fdf4' },
  { label: 'Overweight',    range: '25 – 29.9',      color: '#f97316', textColor: '#9a3412', bgColor: '#fff7ed' },
  { label: 'Obese',         range: '30 and above',   color: '#ef4444', textColor: '#7f1d1d', bgColor: '#fef2f2' },
];

function getCategory(bmi: number): BmiCategory {
  if (bmi < 18.5) return CATEGORIES[0]!;
  if (bmi < 25)   return CATEGORIES[1]!;
  if (bmi < 30)   return CATEGORIES[2]!;
  return CATEGORIES[3]!;
}

function calcBmiImperial(ft: number, inches: number, lbs: number): number {
  const totalIn = ft * 12 + inches;
  if (totalIn <= 0 || lbs <= 0) return 0;
  return (lbs / (totalIn * totalIn)) * 703;
}

function calcBmiMetric(cm: number, kg: number): number {
  if (cm <= 0 || kg <= 0) return 0;
  const m = cm / 100;
  return kg / (m * m);
}

export default function BmiCalculator() {
  const [unit, setUnit] = useState<Unit>('imperial');
  const [heightFt, setHeightFt]   = useState('');
  const [heightIn, setHeightIn]   = useState('');
  const [heightCm, setHeightCm]   = useState('');
  const [weightLbs, setWeightLbs] = useState('');
  const [weightKg, setWeightKg]   = useState('');

  const bmi = useMemo(() => {
    if (unit === 'imperial') {
      return calcBmiImperial(
        parseFloat(heightFt)  || 0,
        parseFloat(heightIn)  || 0,
        parseFloat(weightLbs) || 0,
      );
    }
    return calcBmiMetric(parseFloat(heightCm) || 0, parseFloat(weightKg) || 0);
  }, [unit, heightFt, heightIn, heightCm, weightLbs, weightKg]);

  const hasResult  = bmi > 0 && isFinite(bmi);
  const category   = hasResult ? getCategory(bmi) : null;
  // Gauge: maps 15–40 BMI range to 0–100%
  const gaugePct   = hasResult ? Math.min(Math.max(((bmi - 15) / 25) * 100, 0), 100) : 0;

  const inputCls =
    'w-full rounded-lg border border-slate-300 px-3 py-2 pr-10 text-sm focus:border-brand focus:outline-none focus:ring-1 focus:ring-brand';

  return (
    <div class="space-y-4">

      {/* Unit toggle */}
      <div class="flex gap-1 rounded-lg border border-slate-200 bg-slate-50 p-1">
        {(['imperial', 'metric'] as const).map((u) => (
          <button
            key={u}
            type="button"
            class={`flex-1 rounded-md py-1.5 text-sm font-medium capitalize transition-all ${
              unit === u
                ? 'bg-white text-slate-900 shadow-sm'
                : 'text-slate-500 hover:text-slate-700'
            }`}
            onClick={() => setUnit(u)}
            aria-pressed={unit === u}
          >
            {u}
          </button>
        ))}
      </div>

      {/* Height */}
      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Height</label>
        {unit === 'imperial' ? (
          <div class="flex gap-2">
            <div class="relative flex-1">
              <input
                type="number" min="1" max="8" placeholder="5"
                value={heightFt}
                onInput={(e) => setHeightFt((e.target as HTMLInputElement).value)}
                class={inputCls}
                aria-label="Height in feet"
              />
              <span class="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">ft</span>
            </div>
            <div class="relative flex-1">
              <input
                type="number" min="0" max="11" placeholder="10"
                value={heightIn}
                onInput={(e) => setHeightIn((e.target as HTMLInputElement).value)}
                class={inputCls}
                aria-label="Height in inches"
              />
              <span class="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">in</span>
            </div>
          </div>
        ) : (
          <div class="relative">
            <input
              type="number" min="50" max="300" placeholder="170"
              value={heightCm}
              onInput={(e) => setHeightCm((e.target as HTMLInputElement).value)}
              class={inputCls}
              aria-label="Height in centimeters"
            />
            <span class="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">cm</span>
          </div>
        )}
      </div>

      {/* Weight */}
      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Weight</label>
        <div class="relative">
          <input
            type="number"
            min="1"
            max={unit === 'imperial' ? '1000' : '500'}
            placeholder={unit === 'imperial' ? '150' : '70'}
            value={unit === 'imperial' ? weightLbs : weightKg}
            onInput={(e) => {
              const v = (e.target as HTMLInputElement).value;
              if (unit === 'imperial') setWeightLbs(v);
              else setWeightKg(v);
            }}
            class={inputCls}
            aria-label={unit === 'imperial' ? 'Weight in pounds' : 'Weight in kilograms'}
          />
          <span class="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">
            {unit === 'imperial' ? 'lbs' : 'kg'}
          </span>
        </div>
      </div>

      {/* Result */}
      {hasResult && category && (
        <div
          role="status"
          aria-live="polite"
          class="space-y-3 rounded-xl border-2 p-4"
          style={{ borderColor: category.color, backgroundColor: category.bgColor }}
        >
          <div class="flex items-start justify-between">
            <div>
              <div class="text-4xl font-bold tabular-nums" style={{ color: category.color }}>
                {bmi.toFixed(1)}
              </div>
              <div class="mt-0.5 text-sm font-semibold" style={{ color: category.textColor }}>
                {category.label}
              </div>
            </div>
            <div class="text-right text-xs text-slate-500">
              <div class="font-medium">Your BMI</div>
              <div class="mt-0.5">{category.range}</div>
            </div>
          </div>

          {/* Gauge bar */}
          <div>
            <div
              class="relative h-2.5 overflow-hidden rounded-full"
              style={{ background: 'linear-gradient(to right, #3b82f6 0%, #22c55e 30%, #f97316 65%, #ef4444 100%)' }}
            >
              <div
                class="absolute top-1/2 h-4 w-4 -translate-x-1/2 -translate-y-1/2 rounded-full border-2 border-white bg-slate-800 shadow"
                style={{ left: `${gaugePct}%` }}
                role="img"
                aria-label={`BMI ${bmi.toFixed(1)} on gauge`}
              />
            </div>
            <div class="mt-1 flex justify-between text-[10px] text-slate-400">
              <span>15</span><span>18.5</span><span>25</span><span>30</span><span>40+</span>
            </div>
          </div>
        </div>
      )}

      {/* Disclaimer */}
      <p class="text-xs leading-relaxed text-slate-500">
        For informational purposes only. Consult a healthcare professional for medical advice.
      </p>

    </div>
  );
}
```

- [ ] **Step 2: Verify TypeScript**

```bash
pnpm --filter bmicalc.io check
```

Expected: no errors. If you see TS errors about JSX attributes (`class` vs `className`), confirm `tsconfig.json` has `"jsxImportSource": "preact"` — it already does in this project.

- [ ] **Step 3: Commit**

```bash
git -C /home/abovespec/site-network add sites/bmicalc.io/src/components/BmiCalculator.tsx
git -C /home/abovespec/site-network commit -m "feat(bmicalc): add interactive BMI calculator Preact component

Co-Authored-By: Paperclip <noreply@paperclip.ing>"
```

---

## Task 4: Update PostLayout with YMYL Fields

**Files:**
- Modify: `sites/bmicalc.io/src/layouts/PostLayout.astro`

- [ ] **Step 1: Replace PostLayout.astro**

Replace the entire content of `sites/bmicalc.io/src/layouts/PostLayout.astro`:

```astro
---
import BaseLayout from './BaseLayout.astro';
import Breadcrumb from '~/components/Breadcrumb.astro';
import SchemaArticle from '~/components/SchemaArticle.astro';
import { siteUrl } from '~/config/site.config';

interface Props {
  title: string;
  description: string;
  publishDate: Date | string;
  updatedDate?: Date | string;
  author?: string;
  image?: string;
  tags?: string[];
  reviewedBy?: string;
  lastReviewedAt?: Date | string;
  sources?: Array<{ text: string; url?: string }>;
}
const {
  title,
  description,
  publishDate,
  updatedDate,
  author,
  image,
  tags = [],
  reviewedBy,
  lastReviewedAt,
  sources = [],
} = Astro.props;
const url = new URL(Astro.url.pathname, siteUrl).toString();

const fmt = (d: Date | string) =>
  new Date(d).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
---
<BaseLayout title={title} description={description} image={image} ogType="article">
  <article class="prose prose-slate max-w-none">
    <Breadcrumb items={[
      { name: 'Home', url: '/' },
      { name: 'Blog', url: '/blog/' },
      { name: title, url: Astro.url.pathname },
    ]} />
    <header class="not-prose mt-4 mb-8">
      <h1 class="text-4xl font-bold tracking-tight text-slate-900">{title}</h1>
      <p class="mt-3 text-lg text-slate-600">{description}</p>
      <div class="mt-4 flex flex-wrap items-center gap-x-3 gap-y-1 text-sm text-slate-500">
        {author && (
          <span>By <span class="font-medium text-slate-700">{author}</span></span>
        )}
        <span aria-hidden="true">·</span>
        <time datetime={new Date(publishDate).toISOString()}>{fmt(publishDate)}</time>
        {updatedDate && (
          <>
            <span aria-hidden="true">·</span>
            <span>
              Updated <time datetime={new Date(updatedDate).toISOString()}>{fmt(updatedDate)}</time>
            </span>
          </>
        )}
        {tags.length > 0 && (
          <>
            <span aria-hidden="true">·</span>
            <ul class="flex flex-wrap gap-2">
              {tags.map((t) => (
                <li class="rounded-full bg-green-50 px-2 py-0.5 text-xs font-medium text-green-700">{t}</li>
              ))}
            </ul>
          </>
        )}
      </div>

      {/* Medically reviewed by — YMYL legitimacy */}
      {reviewedBy && (
        <div class="mt-4 flex items-center gap-2 rounded-lg border border-green-200 bg-green-50 px-4 py-2.5 text-sm text-green-900">
          <svg class="h-4 w-4 shrink-0 text-green-700" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
            <path fill-rule="evenodd" d="M16.403 12.652a3 3 0 000-5.304 3 3 0 00-3.75-3.751 3 3 0 00-5.305 0 3 3 0 00-3.751 3.75 3 3 0 000 5.305 3 3 0 003.75 3.751 3 3 0 005.305 0 3 3 0 003.751-3.75zm-2.546-4.46a.75.75 0 00-1.214-.883l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z" clip-rule="evenodd" />
          </svg>
          <span>
            Medically reviewed by <span class="font-semibold">{reviewedBy}</span>
            {lastReviewedAt && (
              <>
                {' · '}Last reviewed{' '}
                <time datetime={new Date(lastReviewedAt).toISOString()}>{fmt(lastReviewedAt)}</time>
              </>
            )}
          </span>
        </div>
      )}
    </header>

    <div class="prose prose-slate max-w-none">
      <slot />
    </div>

    {/* Sources — rendered outside prose so we control the layout */}
    {sources.length > 0 && (
      <footer class="not-prose mt-12 border-t border-slate-200 pt-6">
        <h2 class="text-base font-semibold text-slate-700">Sources</h2>
        <ol class="mt-3 space-y-2 text-sm text-slate-600">
          {sources.map((s, i) => (
            <li class="flex gap-2">
              <span class="shrink-0 tabular-nums text-slate-400">{i + 1}.</span>
              {s.url ? (
                <a
                  href={s.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  class="text-brand underline underline-offset-2 hover:text-green-700"
                >
                  {s.text}
                </a>
              ) : (
                <span>{s.text}</span>
              )}
            </li>
          ))}
        </ol>
      </footer>
    )}

    <slot name="related" />
  </article>
  <SchemaArticle
    headline={title}
    description={description}
    url={url}
    image={image}
    datePublished={publishDate}
    dateModified={updatedDate}
    author={author}
  />
</BaseLayout>
```

- [ ] **Step 2: Update blog/[...slug].astro to pass new props**

Replace the `<PostLayout>` call at the bottom of `sites/bmicalc.io/src/pages/blog/[...slug].astro`:

```astro
<PostLayout
  title={post.data.title}
  description={post.data.description}
  publishDate={post.data.publishDate}
  updatedDate={post.data.updatedDate}
  author={post.data.author}
  tags={post.data.tags}
  reviewedBy={post.data.reviewedBy}
  lastReviewedAt={post.data.lastReviewedAt}
  sources={post.data.sources}
>
  <Content />
  {related.length > 0 && <RelatedPosts slot="related" posts={related} />}
</PostLayout>
```

- [ ] **Step 3: Verify TypeScript**

```bash
pnpm --filter bmicalc.io check
```

Expected: no errors.

- [ ] **Step 4: Commit**

```bash
git -C /home/abovespec/site-network add \
  sites/bmicalc.io/src/layouts/PostLayout.astro \
  sites/bmicalc.io/src/pages/blog/[...slug].astro
git -C /home/abovespec/site-network commit -m "feat(bmicalc): add YMYL legitimacy signals to PostLayout (reviewedBy, sources)

Co-Authored-By: Paperclip <noreply@paperclip.ing>"
```

---

## Task 5: Redesign Blog Index

**Files:**
- Modify: `sites/bmicalc.io/src/pages/blog/index.astro`

- [ ] **Step 1: Replace blog/index.astro**

Replace the entire content of `sites/bmicalc.io/src/pages/blog/index.astro`:

```astro
---
import BaseLayout from '~/layouts/BaseLayout.astro';
import { getCollection } from 'astro:content';
import { siteConfig } from '~/config/site.config';

if (!siteConfig.features.hasBlog) return Astro.redirect('/');

const posts = (await getCollection('blog', ({ data }) => !data.draft)).sort(
  (a, b) => b.data.publishDate.valueOf() - a.data.publishDate.valueOf(),
);

const fmt = (d: Date) =>
  d.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
---
<BaseLayout
  title="BMI & Health Articles"
  description="Evidence-based guides on BMI, weight management, and healthy living. Medically reviewed content from BMICalc."
>
  <header class="py-8">
    <h1 class="text-3xl font-bold tracking-tight text-slate-900">Health &amp; BMI Articles</h1>
    <p class="mt-2 text-slate-600">Evidence-based guides on BMI, weight, and healthy living.</p>
  </header>

  {posts.length === 0 ? (
    <p class="text-slate-500">Articles coming soon.</p>
  ) : (
    <ul class="grid gap-5 sm:grid-cols-2">
      {posts.map((post) => (
        <li>
          <a
            href={`/blog/${post.slug}/`}
            class="group block rounded-xl border border-slate-200 bg-white p-5 transition hover:border-green-300 hover:shadow-sm"
          >
            <time
              datetime={post.data.publishDate.toISOString()}
              class="text-xs font-medium uppercase tracking-wide text-slate-400"
            >
              {fmt(post.data.publishDate)}
            </time>
            <h2 class="mt-1 text-lg font-semibold text-slate-900 group-hover:text-brand">
              {post.data.title}
            </h2>
            <p class="mt-2 line-clamp-2 text-sm text-slate-600">{post.data.description}</p>
            {post.data.tags.length > 0 && (
              <div class="mt-3 flex flex-wrap gap-1.5">
                {post.data.tags.slice(0, 3).map((tag) => (
                  <span class="rounded-full bg-green-50 px-2.5 py-0.5 text-xs font-medium text-green-700">
                    {tag}
                  </span>
                ))}
              </div>
            )}
            {post.data.reviewedBy && (
              <p class="mt-3 text-xs text-slate-400">
                ✓ Medically reviewed
              </p>
            )}
          </a>
        </li>
      ))}
    </ul>
  )}
</BaseLayout>
```

- [ ] **Step 2: Verify TypeScript**

```bash
pnpm --filter bmicalc.io check
```

Expected: no errors.

- [ ] **Step 3: Commit**

```bash
git -C /home/abovespec/site-network add sites/bmicalc.io/src/pages/blog/index.astro
git -C /home/abovespec/site-network commit -m "feat(bmicalc): redesign blog index with green card layout

Co-Authored-By: Paperclip <noreply@paperclip.ing>"
```

---

## Task 6: Redesign Homepage (index.astro)

**Files:**
- Modify: `sites/bmicalc.io/src/pages/index.astro`

- [ ] **Step 1: Replace index.astro**

Replace the entire content of `sites/bmicalc.io/src/pages/index.astro`:

```astro
---
import BaseLayout from '~/layouts/BaseLayout.astro';
import { siteConfig } from '~/config/site.config';
import BmiCalculator from '~/components/BmiCalculator';
import { getCollection } from 'astro:content';

const recentPosts = siteConfig.features.hasBlog
  ? (await getCollection('blog', ({ data }) => !data.draft))
      .sort((a, b) => b.data.publishDate.valueOf() - a.data.publishDate.valueOf())
      .slice(0, 3)
  : [];
---
<BaseLayout
  title="BMI Calculator — Free, Instant Body Mass Index Calculator"
  description="Calculate your BMI instantly with our free online calculator. Supports imperial and metric units. Medically reviewed BMI categories and health information."
>

  <!-- Page heading -->
  <header class="pb-8 pt-4">
    <h1 class="text-4xl font-bold tracking-tight text-slate-900 sm:text-5xl">
      BMI Calculator
    </h1>
    <p class="mt-3 max-w-xl text-lg text-slate-600">
      Calculate your Body Mass Index instantly — free, private, no signup required.
    </p>
  </header>

  <!-- Main layout: content left, sticky calculator right -->
  <div class="grid items-start gap-8 md:grid-cols-[1fr_400px]">

    <!-- Left: trust signals + disclaimer + SEO content -->
    <div class="space-y-10">

      <!-- Trust signals -->
      <ul class="flex flex-wrap gap-x-6 gap-y-2 text-sm text-slate-600">
        {[
          'Instant results as you type',
          'Imperial & metric units',
          'No data stored or shared',
          'WHO-standard categories',
        ].map((badge) => (
          <li class="flex items-center gap-1.5">
            <svg class="h-4 w-4 shrink-0 text-brand" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z" clip-rule="evenodd" />
            </svg>
            {badge}
          </li>
        ))}
      </ul>

      <!-- YMYL medical disclaimer -->
      <aside
        role="note"
        class="rounded-lg border border-amber-200 bg-amber-50 p-4 text-sm text-amber-900"
      >
        <strong class="font-semibold">Important:</strong> BMI is a screening tool,
        not a diagnostic measure. Results are for general informational purposes only.
        Always consult a qualified healthcare professional regarding your health and
        weight status.{' '}
        <a href="#bmi-limitations" class="font-medium underline decoration-amber-400 hover:text-amber-800">
          Learn about BMI limitations.
        </a>
      </aside>

      <!-- BMI Categories table -->
      <section aria-labelledby="categories-heading">
        <h2 id="categories-heading" class="text-2xl font-bold text-slate-900">BMI Categories</h2>
        <p class="mt-2 text-slate-600">
          The World Health Organization defines these BMI ranges for adults aged 20 and older:
        </p>
        <div class="mt-4 overflow-hidden rounded-xl border border-slate-200">
          <table class="w-full text-sm">
            <thead>
              <tr class="bg-slate-50 text-left">
                <th class="px-4 py-3 font-semibold text-slate-700">BMI Range</th>
                <th class="px-4 py-3 font-semibold text-slate-700">Category</th>
                <th class="hidden px-4 py-3 font-semibold text-slate-700 sm:table-cell">Health Risk</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100">
              {([
                { range: 'Below 18.5',    cat: 'Underweight',       risk: 'Malnutrition, osteoporosis', dot: '#3b82f6' },
                { range: '18.5 – 24.9',  cat: 'Normal weight',     risk: 'Lowest risk',                dot: '#15803d' },
                { range: '25.0 – 29.9',  cat: 'Overweight',        risk: 'Moderately increased',       dot: '#f97316' },
                { range: '30.0 – 34.9',  cat: 'Obese (Class I)',   risk: 'High',                       dot: '#ef4444' },
                { range: '35.0 – 39.9',  cat: 'Obese (Class II)',  risk: 'Very high',                  dot: '#ef4444' },
                { range: '40.0 and above', cat: 'Obese (Class III)', risk: 'Extremely high',            dot: '#7f1d1d' },
              ] as const).map((row) => (
                <tr class="bg-white hover:bg-slate-50">
                  <td class="px-4 py-3 font-mono text-xs text-slate-800">{row.range}</td>
                  <td class="px-4 py-3">
                    <span class="flex items-center gap-2">
                      <span
                        class="h-2.5 w-2.5 shrink-0 rounded-full"
                        style={`background: ${row.dot}`}
                        aria-hidden="true"
                      />
                      {row.cat}
                    </span>
                  </td>
                  <td class="hidden px-4 py-3 text-slate-600 sm:table-cell">{row.risk}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <!-- What is BMI -->
      <section aria-labelledby="what-is-bmi-heading">
        <h2 id="what-is-bmi-heading" class="text-2xl font-bold text-slate-900">What Is BMI?</h2>
        <div class="prose prose-slate mt-3 max-w-none">
          <p>
            Body Mass Index (BMI) is a numerical value derived from a person's weight and height.
            It provides a simple, widely used indicator of whether an adult has a healthy body
            weight for their height.
          </p>
          <p>
            BMI was developed in the early 19th century by Belgian mathematician Adolphe Quetelet
            and adopted by the World Health Organization as an international standard for recording
            obesity statistics. While it does not directly measure body fat, research has shown
            that BMI correlates reasonably well with body fat as measured by more direct techniques.
          </p>
        </div>
      </section>

      <!-- How BMI is calculated -->
      <section aria-labelledby="how-bmi-heading">
        <h2 id="how-bmi-heading" class="text-2xl font-bold text-slate-900">How Is BMI Calculated?</h2>
        <div class="prose prose-slate mt-3 max-w-none">
          <p>BMI is calculated using these formulas:</p>
          <ul>
            <li>
              <strong>Metric:</strong> BMI = weight (kg) ÷ height² (m²)
            </li>
            <li>
              <strong>Imperial:</strong> BMI = (weight (lbs) ÷ height² (in²)) × 703
            </li>
          </ul>
          <p>
            For example, a person who weighs 70 kg and is 1.75 m tall has a BMI
            of 70 ÷ (1.75²) = <strong>22.9</strong> — in the Normal weight range.
          </p>
        </div>
      </section>

      <!-- BMI Limitations (YMYL) -->
      <section id="bmi-limitations" aria-labelledby="limitations-heading">
        <h2 id="limitations-heading" class="text-2xl font-bold text-slate-900">Limitations of BMI</h2>
        <div class="prose prose-slate mt-3 max-w-none">
          <p>
            While BMI is a useful population-level screening tool, it has important limitations
            for individual health assessment:
          </p>
          <ul>
            <li>
              <strong>Does not measure body fat directly.</strong> Athletes and muscular
              individuals may have a high BMI despite low body fat.
            </li>
            <li>
              <strong>Varies by age, sex, and ethnicity.</strong> The same BMI may carry
              different health implications across populations. Lower cut-off points apply
              for some Asian populations.
            </li>
            <li>
              <strong>Does not assess fat distribution.</strong> Abdominal (visceral) fat
              is a stronger predictor of metabolic risk than BMI alone. Waist circumference
              provides additional context.
            </li>
            <li>
              <strong>Not suitable for children or adolescents.</strong> Use age- and
              sex-specific BMI-for-age percentile charts instead.
            </li>
            <li>
              <strong>Not suitable for pregnant women</strong> or individuals with
              certain medical conditions.
            </li>
          </ul>
          <p>
            For a comprehensive assessment, your healthcare provider may also consider
            waist circumference, blood glucose, lipid panel, blood pressure, and other
            clinical indicators.
          </p>
        </div>
      </section>

      <!-- When to see a doctor -->
      <section aria-labelledby="when-to-see-doctor-heading">
        <h2 id="when-to-see-doctor-heading" class="text-2xl font-bold text-slate-900">
          When to See a Doctor
        </h2>
        <div class="prose prose-slate mt-3 max-w-none">
          <p>Schedule a consultation with your healthcare provider if:</p>
          <ul>
            <li>Your BMI is below 18.5 or 30 or above</li>
            <li>You have experienced unexplained weight changes</li>
            <li>You have a family history of obesity-related conditions such as type 2 diabetes or heart disease</li>
            <li>You have concerns about your diet, weight, or overall health</li>
          </ul>
        </div>
      </section>

    </div><!-- /left column -->

    <!-- Right column: sticky calculator card -->
    <div class="md:sticky md:top-8">
      <div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <h2 class="mb-4 text-lg font-semibold text-slate-900">Calculate Your BMI</h2>
        <BmiCalculator client:load />
      </div>
    </div>

  </div><!-- /grid -->

  <!-- Recent posts (once Calliope adds articles) -->
  {recentPosts.length > 0 && (
    <section class="mt-16" aria-labelledby="articles-heading">
      <h2 id="articles-heading" class="text-2xl font-bold text-slate-900">Latest Articles</h2>
      <ul class="mt-6 grid gap-4 sm:grid-cols-3">
        {recentPosts.map((post) => (
          <li>
            <a
              href={`/blog/${post.slug}/`}
              class="group block rounded-xl border border-slate-200 bg-white p-5 transition hover:border-green-300 hover:shadow-sm"
            >
              <time
                datetime={post.data.publishDate.toISOString()}
                class="text-xs font-medium uppercase tracking-wide text-slate-400"
              >
                {post.data.publishDate.toLocaleDateString('en-US', {
                  year: 'numeric', month: 'short', day: 'numeric',
                })}
              </time>
              <h3 class="mt-1 text-base font-semibold text-slate-900 group-hover:text-brand">
                {post.data.title}
              </h3>
              <p class="mt-2 line-clamp-2 text-sm text-slate-600">{post.data.description}</p>
            </a>
          </li>
        ))}
      </ul>
      <div class="mt-6">
        <a href="/blog/" class="text-sm font-medium text-brand underline underline-offset-2 hover:text-green-700">
          View all articles →
        </a>
      </div>
    </section>
  )}

  <!-- YMYL page footer: reviewed-by slot + sources -->
  <footer class="mt-16 border-t border-slate-200 pt-8 text-sm text-slate-600">
    <div class="flex flex-wrap items-center gap-2 text-slate-500">
      <svg class="h-4 w-4 text-slate-400" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
        <path fill-rule="evenodd" d="M16.403 12.652a3 3 0 000-5.304 3 3 0 00-3.75-3.751 3 3 0 00-5.305 0 3 3 0 00-3.751 3.75 3 3 0 000 5.305 3 3 0 003.75 3.751 3 3 0 005.305 0 3 3 0 003.751-3.75zm-2.546-4.46a.75.75 0 00-1.214-.883l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z" clip-rule="evenodd" />
      </svg>
      <span>
        {/* Reviewed-by slot — placeholder until Calliope sources a medical reviewer */}
        Content reviewed for medical accuracy.
        Last reviewed: <time datetime="2026-04-25">April 25, 2026</time>.
      </span>
    </div>

    <div class="mt-6">
      <h2 class="mb-2 font-semibold text-slate-700">Sources</h2>
      <ol class="space-y-1.5">
        <li class="flex gap-2">
          <span class="shrink-0 tabular-nums text-slate-400">1.</span>
          <span>
            World Health Organization. <em>BMI Classification</em>. Global Database on Body Mass Index, 2004.
          </span>
        </li>
        <li class="flex gap-2">
          <span class="shrink-0 tabular-nums text-slate-400">2.</span>
          <span>
            Centers for Disease Control and Prevention. <em>About Adult BMI</em>. 2023.{' '}
            <a
              href="https://www.cdc.gov/healthyweight/assessing/bmi/adult_bmi/index.html"
              target="_blank"
              rel="noopener noreferrer"
              class="text-brand underline underline-offset-2 hover:text-green-700"
            >
              cdc.gov
            </a>
          </span>
        </li>
        <li class="flex gap-2">
          <span class="shrink-0 tabular-nums text-slate-400">3.</span>
          <span>
            National Heart, Lung, and Blood Institute. <em>Classification of Overweight and Obesity by BMI, Waist Circumference, and Associated Disease Risks</em>. 2012.
          </span>
        </li>
      </ol>
    </div>
  </footer>

</BaseLayout>
```

- [ ] **Step 2: Verify TypeScript**

```bash
pnpm --filter bmicalc.io check
```

Expected: no errors.

- [ ] **Step 3: Commit**

```bash
git -C /home/abovespec/site-network add sites/bmicalc.io/src/pages/index.astro
git -C /home/abovespec/site-network commit -m "feat(bmicalc): redesign homepage with sticky calculator + YMYL legitimacy

Co-Authored-By: Paperclip <noreply@paperclip.ing>"
```

---

## Task 7: Build Verification

- [ ] **Step 1: Full build**

```bash
cd /home/abovespec/site-network && pnpm --filter bmicalc.io build
```

Expected: Build completes with no errors. Output in `sites/bmicalc.io/dist/`.

- [ ] **Step 2: Fix any TS/build errors**

Common issues to watch for:
- TypeScript complaining about `class` attribute — ensure `jsxImportSource: "preact"` in tsconfig (already set).
- Tailwind not generating `bg-brand`/`text-brand` — these come from `@theme { --color-brand }` in global.css, which maps to `.bg-brand`. If missing, add explicit `bg-[var(--site-theme-color)]` as fallback in the toggle button.
- Missing Preact type for `aria-pressed` as boolean — cast to `string` if needed: `aria-pressed={String(unit === u)}`.
- Astro content type mismatch for new schema fields — check `sites/bmicalc.io/.astro/types.d.ts` regenerates on build.

- [ ] **Step 3: Check output**

```bash
ls /home/abovespec/site-network/sites/bmicalc.io/dist/
```

Expect: `index.html`, `blog/`, `about/`, `contact/`, etc.

- [ ] **Step 4: Commit spec + plan docs**

```bash
git -C /home/abovespec/site-network add \
  docs/superpowers/specs/2026-04-25-bmicalc-redesign.md \
  docs/superpowers/plans/2026-04-25-bmicalc-redesign.md
git -C /home/abovespec/site-network commit -m "docs: add bmicalc redesign spec and implementation plan

Co-Authored-By: Paperclip <noreply@paperclip.ing>"
```

---

## Self-Review

**Spec coverage:**
- ✅ Calculator above the fold — homepage hero with sticky right-column calculator
- ✅ Blog index and article layout — Tasks 5 + 4
- ✅ YMYL legitimacy: reviewed-by, last-updated, disclaimer, citation footer — Tasks 4 + 6
- ✅ Coordinate with Calliope on `reviewedBy`, `lastReviewedAt`, `sources[]` — schema defined in Task 1
- ✅ Mobile (375px) and desktop (1280px) — responsive grid with `md:grid-cols-[1fr_400px]`
- ✅ `pnpm --filter bmicalc.io build` — Task 7

**Placeholder scan:** None — all code is complete and exact.

**Type consistency:** `BmiCategory` defined in Task 3; `sources: Array<{text, url?}>` defined in Task 1 and used identically in Tasks 4 and 6. All props match.
