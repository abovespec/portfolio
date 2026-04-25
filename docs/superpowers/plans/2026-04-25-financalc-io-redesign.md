# financalc.io Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Redesign financalc.io as a multi-tool financial calculator site with YMYL-financial chrome, two-column sticky layouts, and four Preact calculator components, mirroring the bmicalc.io design system.

**Architecture:** The homepage becomes a tool-directory landing page linking to individual `/tools/[slug]/` pages; each tool page uses a two-column sticky layout (prose left, calculator right) adapted from bmicalc.io's index pattern. ToolLayout and PostLayout gain YMYL props (reviewedBy, sources, financial disclaimer). Four Preact components replace the current inline-JS calculators.

**Tech Stack:** Astro 5, Preact 10, Tailwind v4, TypeScript. Build: `pnpm --filter @site/financalc-io build`. Type-check: `pnpm --filter @site/financalc-io check`.

---

## File Map

| Action | File | Responsibility |
|--------|------|---------------|
| Modify | `sites/financalc.io/src/config/site.config.ts` | Enable hasTool + hasBlog flags, update nav |
| Modify | `sites/financalc.io/src/content/config.ts` | Add YMYL fields to blog schema |
| Modify | `sites/financalc.io/src/layouts/ToolLayout.astro` | Two-column sticky + YMYL chrome |
| Modify | `sites/financalc.io/src/layouts/PostLayout.astro` | Add reviewedBy, sources, financial disclaimer |
| Modify | `sites/financalc.io/src/pages/index.astro` | Tool-directory homepage |
| Modify | `sites/financalc.io/src/pages/tools/[...slug].astro` | Wire Preact calculators by slug |
| Create | `sites/financalc.io/src/components/LoanCalculator.tsx` | Preact loan amortization component |
| Create | `sites/financalc.io/src/components/CompoundInterestCalculator.tsx` | Preact compound interest component |
| Create | `sites/financalc.io/src/components/ROICalculator.tsx` | Preact ROI / annualized return component |
| Create | `sites/financalc.io/src/components/SavingsGoalCalculator.tsx` | Preact savings-to-goal component |
| Create | `sites/financalc.io/src/content/tools/loan-calculator.md` | SEO prose for loan calculator |
| Create | `sites/financalc.io/src/content/tools/compound-interest-calculator.md` | SEO prose for compound interest |
| Create | `sites/financalc.io/src/content/tools/roi-calculator.md` | SEO prose for ROI calculator |
| Create | `sites/financalc.io/src/content/tools/savings-goal-calculator.md` | SEO prose for savings goal |

---

## Task 1: Enable Feature Flags and Update Nav

**Files:**
- Modify: `sites/financalc.io/src/config/site.config.ts`

- [ ] **Step 1: Update site.config.ts**

Replace the `features` and `nav.primary` blocks:

```typescript
  features: {
    hasBlog: true,
    hasTool: true,
    hasGame: false,
    hasSponsoredIntake: false,
  },
```

```typescript
  nav: {
    primary: [
      { label: 'Home', href: '/' },
      { label: 'Tools', href: '/tools/' },
      { label: 'Blog', href: '/blog/' },
      { label: 'About', href: '/about/' },
      { label: 'Contact', href: '/contact/' },
    ],
  },
```

- [ ] **Step 2: Verify type-check passes**

```bash
cd /home/abovespec/site-network
pnpm --filter @site/financalc-io check
```

Expected: no type errors.

- [ ] **Step 3: Commit**

```bash
git add sites/financalc.io/src/config/site.config.ts
git commit -m "feat(financalc.io): enable hasTool + hasBlog, add Tools + Blog nav

Co-Authored-By: Paperclip <noreply@paperclip.ing>"
```

---

## Task 2: Add YMYL Fields to Blog Content Schema

**Files:**
- Modify: `sites/financalc.io/src/content/config.ts`

- [ ] **Step 1: Add YMYL fields to the blog schema**

In `sites/financalc.io/src/content/config.ts`, update the `blog` collection schema (after the existing `draft` field):

```typescript
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
      reviewedBy: z.string().optional(),
      lastReviewedAt: z.coerce.date().optional(),
      sources: z.array(z.object({
        text: z.string(),
        url: z.string().optional(),
      })).default([]),
    }),
});
```

- [ ] **Step 2: Verify type-check**

```bash
pnpm --filter @site/financalc-io check
```

Expected: no errors.

- [ ] **Step 3: Commit**

```bash
git add sites/financalc.io/src/content/config.ts
git commit -m "feat(financalc.io): add reviewedBy + sources YMYL fields to blog schema

Co-Authored-By: Paperclip <noreply@paperclip.ing>"
```

---

## Task 3: Refactor ToolLayout to Two-Column Sticky + YMYL Chrome

**Files:**
- Modify: `sites/financalc.io/src/layouts/ToolLayout.astro`

- [ ] **Step 1: Replace ToolLayout.astro entirely**

```astro
---
import BaseLayout from './BaseLayout.astro';
import Breadcrumb from '~/components/Breadcrumb.astro';
import SchemaSoftwareApplication from '~/components/SchemaSoftwareApplication.astro';
import { siteUrl } from '~/config/site.config';

interface Props {
  title: string;
  description: string;
  slug: string;
  reviewedBy?: string;
  lastReviewedAt?: Date | string;
  sources?: Array<{ text: string; url?: string }>;
  applicationCategory?: string;
  operatingSystem?: string;
  price?: string;
  priceCurrency?: string;
  ratingValue?: number;
  ratingCount?: number;
}

const {
  title, description, slug,
  reviewedBy, lastReviewedAt, sources = [],
  applicationCategory, operatingSystem, price, priceCurrency, ratingValue, ratingCount,
} = Astro.props;

const url = new URL(Astro.url.pathname, siteUrl).toString();

const fmtDate = (d: Date | string) =>
  new Date(d).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
---
<BaseLayout title={title} description={description}>

  <Breadcrumb items={[
    { name: 'Home', url: '/' },
    { name: 'Tools', url: '/tools/' },
    { name: title, url: `/tools/${slug}/` },
  ]} />

  <header class="pb-8 pt-4">
    <h1 class="text-4xl font-bold tracking-tight text-slate-900 sm:text-5xl">{title}</h1>
    <p class="mt-3 max-w-xl text-lg text-slate-600">{description}</p>
  </header>

  <!-- Two-column grid: prose left, sticky calculator right -->
  <div class="grid items-start gap-8 md:grid-cols-[1fr_400px]">

    <!-- Left: YMYL disclaimer + SEO prose -->
    <div class="space-y-10">

      <!-- YMYL financial disclaimer -->
      <aside
        role="note"
        class="rounded-lg border border-amber-200 bg-amber-50 p-4 text-sm text-amber-900"
      >
        <strong class="font-semibold">Important:</strong> Results are estimates for informational
        purposes only. This calculator does not constitute financial advice. Consult a licensed
        financial advisor before making investment or borrowing decisions.
      </aside>

      <!-- SEO content slot -->
      <div class="prose prose-slate max-w-none">
        <slot />
      </div>

      <!-- FAQ slot -->
      <slot name="faq" />

    </div><!-- /left column -->

    <!-- Right: sticky calculator card -->
    <div class="md:sticky md:top-8">
      <div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <h2 class="mb-4 text-lg font-semibold text-slate-900">{title}</h2>
        <slot name="tool" />
      </div>
    </div>

  </div><!-- /main grid -->

  <!-- YMYL page footer: reviewed-by + sources -->
  <footer class="mt-16 border-t border-slate-200 pt-8 text-sm text-slate-600">
    {reviewedBy ? (
      <div class="flex items-center gap-2 rounded-lg border border-green-200 bg-green-50 px-4 py-2.5 text-sm text-green-900">
        <svg class="h-4 w-4 shrink-0 text-green-600" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
          <path fill-rule="evenodd" d="M16.403 12.652a3 3 0 000-5.304 3 3 0 00-3.75-3.751 3 3 0 00-5.305 0 3 3 0 00-3.751 3.75 3 3 0 000 5.305 3 3 0 003.75 3.751 3 3 0 005.305 0 3 3 0 003.751-3.75zm-2.546-4.46a.75.75 0 00-1.214-.883l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z" clip-rule="evenodd" />
        </svg>
        <span>
          Reviewed by <span class="font-semibold">{reviewedBy}</span>
          {lastReviewedAt && (
            <> · Last reviewed <time datetime={new Date(lastReviewedAt).toISOString()}>{fmtDate(lastReviewedAt)}</time></>
          )}
        </span>
      </div>
    ) : (
      <div class="flex items-center gap-2 text-slate-500">
        <svg class="h-4 w-4 shrink-0 text-slate-400" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
          <path fill-rule="evenodd" d="M16.403 12.652a3 3 0 000-5.304 3 3 0 00-3.75-3.751 3 3 0 00-5.305 0 3 3 0 00-3.751 3.75 3 3 0 000 5.305 3 3 0 003.75 3.751 3 3 0 005.305 0 3 3 0 003.751-3.75zm-2.546-4.46a.75.75 0 00-1.214-.883l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z" clip-rule="evenodd" />
        </svg>
        <span>Content reviewed for accuracy. Last reviewed: <time datetime="2026-04-25">April 25, 2026</time>.</span>
      </div>
    )}

    {sources.length > 0 && (
      <div class="mt-6">
        <h2 class="mb-2 font-semibold text-slate-700">Sources</h2>
        <ol class="space-y-1.5">
          {sources.map((s, i) => (
            <li class="flex gap-2">
              <span class="shrink-0 tabular-nums text-slate-400">{i + 1}.</span>
              {s.url
                ? <a href={s.url} target="_blank" rel="noopener noreferrer" class="text-brand underline underline-offset-2 hover:opacity-80">{s.text}</a>
                : <span>{s.text}</span>
              }
            </li>
          ))}
        </ol>
      </div>
    )}
  </footer>

  <SchemaSoftwareApplication
    name={title}
    description={description}
    url={url}
    applicationCategory={applicationCategory}
    operatingSystem={operatingSystem}
    price={price}
    priceCurrency={priceCurrency}
    ratingValue={ratingValue}
    ratingCount={ratingCount}
  />
</BaseLayout>
```

- [ ] **Step 2: Verify type-check**

```bash
pnpm --filter @site/financalc-io check
```

Expected: no errors.

- [ ] **Step 3: Commit**

```bash
git add sites/financalc.io/src/layouts/ToolLayout.astro
git commit -m "feat(financalc.io): refactor ToolLayout to two-column sticky + YMYL chrome

Co-Authored-By: Paperclip <noreply@paperclip.ing>"
```

---

## Task 4: Add YMYL Fields to PostLayout

**Files:**
- Modify: `sites/financalc.io/src/layouts/PostLayout.astro`

- [ ] **Step 1: Replace PostLayout.astro**

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
  title, description, publishDate, updatedDate, author, image, tags = [],
  reviewedBy, lastReviewedAt, sources = [],
} = Astro.props;

const url = new URL(Astro.url.pathname, siteUrl).toString();

const fmt = (d: Date | string) =>
  new Date(d).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
---
<BaseLayout title={title} description={description} image={image} ogType="article">
  <article>
    <Breadcrumb items={[
      { name: 'Home', url: '/' },
      { name: 'Blog', url: '/blog/' },
      { name: title, url: Astro.url.pathname },
    ]} />

    <header class="not-prose mt-4 mb-8">
      <h1 class="text-4xl font-bold tracking-tight text-slate-900">{title}</h1>
      <p class="mt-3 text-lg text-slate-600">{description}</p>

      <div class="mt-4 flex flex-wrap items-center gap-x-3 gap-y-1 text-sm text-slate-500">
        {author && <span>By <span class="font-medium text-slate-700">{author}</span></span>}
        <span aria-hidden="true">·</span>
        <time datetime={new Date(publishDate).toISOString()}>{fmt(publishDate)}</time>
        {updatedDate && (
          <>
            <span aria-hidden="true">·</span>
            <span>Updated <time datetime={new Date(updatedDate).toISOString()}>{fmt(updatedDate)}</time></span>
          </>
        )}
        {tags.length > 0 && (
          <>
            <span aria-hidden="true">·</span>
            <ul class="flex flex-wrap gap-2">
              {tags.map((t) => <li class="rounded bg-slate-100 px-2 py-0.5 text-xs">{t}</li>)}
            </ul>
          </>
        )}
      </div>

      <!-- Financial disclaimer note -->
      <p class="mt-3 text-xs text-slate-500 italic">
        Not financial advice. For informational purposes only. Consult a licensed financial advisor.
      </p>

      {reviewedBy && (
        <div class="mt-4 flex items-center gap-2 rounded-lg border border-green-200 bg-green-50 px-4 py-2.5 text-sm text-green-900">
          <svg class="h-4 w-4 shrink-0 text-green-600" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
            <path fill-rule="evenodd" d="M16.403 12.652a3 3 0 000-5.304 3 3 0 00-3.75-3.751 3 3 0 00-5.305 0 3 3 0 00-3.751 3.75 3 3 0 000 5.305 3 3 0 003.75 3.751 3 3 0 005.305 0 3 3 0 003.751-3.75zm-2.546-4.46a.75.75 0 00-1.214-.883l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z" clip-rule="evenodd" />
          </svg>
          <span>
            Reviewed by <span class="font-semibold">{reviewedBy}</span>
            {lastReviewedAt && (
              <> · Last reviewed <time datetime={new Date(lastReviewedAt).toISOString()}>{fmt(lastReviewedAt)}</time></>
            )}
          </span>
        </div>
      )}
    </header>

    <div class="prose prose-slate max-w-none">
      <slot />
    </div>

    <slot name="related" />

    {sources.length > 0 && (
      <footer class="not-prose mt-12 border-t border-slate-200 pt-6">
        <h2 class="font-semibold text-slate-700">Sources</h2>
        <ol class="mt-3 space-y-2 text-sm text-slate-600">
          {sources.map((s, i) => (
            <li class="flex gap-2">
              <span class="shrink-0 tabular-nums text-slate-400">{i + 1}.</span>
              {s.url
                ? <a href={s.url} target="_blank" rel="noopener noreferrer" class="text-brand underline underline-offset-2 hover:opacity-80">{s.text}</a>
                : <span>{s.text}</span>
              }
            </li>
          ))}
        </ol>
      </footer>
    )}
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

- [ ] **Step 2: Verify type-check**

```bash
pnpm --filter @site/financalc-io check
```

Expected: no errors.

- [ ] **Step 3: Commit**

```bash
git add sites/financalc.io/src/layouts/PostLayout.astro
git commit -m "feat(financalc.io): add YMYL financial chrome to PostLayout

Co-Authored-By: Paperclip <noreply@paperclip.ing>"
```

---

## Task 5: LoanCalculator Preact Component

**Files:**
- Create: `sites/financalc.io/src/components/LoanCalculator.tsx`

- [ ] **Step 1: Create LoanCalculator.tsx**

```tsx
import { useState, useMemo } from 'preact/hooks';

function calcLoan(principal: number, annualRate: number, years: number) {
  if (principal <= 0 || annualRate < 0 || years <= 0) return null;
  const r = annualRate / 100 / 12;
  const n = years * 12;
  const monthly = r === 0
    ? principal / n
    : (principal * r) / (1 - Math.pow(1 + r, -n));
  const total = monthly * n;
  const interest = total - principal;
  return { monthly, total, interest, interestPct: (interest / total) * 100 };
}

function fmtUsd(n: number) {
  return '$' + n.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

const inputCls =
  'w-full rounded-lg border border-slate-300 px-3 py-2 pr-10 text-sm focus:border-brand focus:outline-none focus:ring-1 focus:ring-brand';

export default function LoanCalculator() {
  const [principal, setPrincipal] = useState('20000');
  const [rate, setRate]           = useState('6.5');
  const [years, setYears]         = useState('5');

  const result = useMemo(
    () => calcLoan(parseFloat(principal) || 0, parseFloat(rate) || 0, parseFloat(years) || 0),
    [principal, rate, years],
  );

  return (
    <div class="space-y-4">
      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Loan Amount</label>
        <div class="relative">
          <span class="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">$</span>
          <input
            type="number" min="1" placeholder="20000"
            value={principal}
            onInput={(e) => setPrincipal((e.target as HTMLInputElement).value)}
            class={`${inputCls} pl-6`}
            aria-label="Loan amount in dollars"
          />
        </div>
      </div>

      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Annual Interest Rate</label>
        <div class="relative">
          <input
            type="number" min="0" max="100" step="0.1" placeholder="6.5"
            value={rate}
            onInput={(e) => setRate((e.target as HTMLInputElement).value)}
            class={inputCls}
            aria-label="Annual interest rate as percentage"
          />
          <span class="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">%</span>
        </div>
      </div>

      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Loan Term</label>
        <div class="relative">
          <input
            type="number" min="1" max="30" placeholder="5"
            value={years}
            onInput={(e) => setYears((e.target as HTMLInputElement).value)}
            class={inputCls}
            aria-label="Loan term in years"
          />
          <span class="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">yrs</span>
        </div>
      </div>

      {result && (
        <div role="status" aria-live="polite" class="space-y-3 rounded-xl border border-brand/20 bg-indigo-50 p-4">
          <div class="flex items-baseline justify-between">
            <span class="text-sm text-slate-600">Monthly Payment</span>
            <span class="text-2xl font-bold tabular-nums text-brand">{fmtUsd(result.monthly)}</span>
          </div>
          <div class="h-px bg-slate-200" />
          <div class="grid grid-cols-2 gap-2 text-sm">
            <div>
              <div class="text-slate-500">Total Paid</div>
              <div class="font-semibold text-slate-900">{fmtUsd(result.total)}</div>
            </div>
            <div>
              <div class="text-slate-500">Total Interest</div>
              <div class="font-semibold text-slate-900">{fmtUsd(result.interest)}</div>
            </div>
          </div>
          {/* Principal vs interest bar */}
          <div>
            <div class="mb-1 flex justify-between text-[11px] text-slate-500">
              <span>Principal {(100 - result.interestPct).toFixed(0)}%</span>
              <span>Interest {result.interestPct.toFixed(0)}%</span>
            </div>
            <div class="flex h-2.5 overflow-hidden rounded-full">
              <div class="bg-brand" style={{ width: `${100 - result.interestPct}%` }} />
              <div class="bg-orange-400" style={{ width: `${result.interestPct}%` }} />
            </div>
          </div>
        </div>
      )}

      <p class="text-xs leading-relaxed text-slate-500">
        For informational purposes only. Consult a licensed financial advisor.
      </p>
    </div>
  );
}
```

- [ ] **Step 2: Verify type-check**

```bash
pnpm --filter @site/financalc-io check
```

Expected: no errors.

- [ ] **Step 3: Commit**

```bash
git add sites/financalc.io/src/components/LoanCalculator.tsx
git commit -m "feat(financalc.io): add LoanCalculator Preact component

Co-Authored-By: Paperclip <noreply@paperclip.ing>"
```

---

## Task 6: CompoundInterestCalculator Preact Component

**Files:**
- Create: `sites/financalc.io/src/components/CompoundInterestCalculator.tsx`

- [ ] **Step 1: Create CompoundInterestCalculator.tsx**

```tsx
import { useState, useMemo } from 'preact/hooks';

const FREQ_OPTIONS = [
  { label: 'Annually (1×)', value: 1 },
  { label: 'Semi-annually (2×)', value: 2 },
  { label: 'Quarterly (4×)', value: 4 },
  { label: 'Monthly (12×)', value: 12 },
  { label: 'Daily (365×)', value: 365 },
];

function calcCI(principal: number, rate: number, years: number, freq: number) {
  if (principal <= 0 || rate < 0 || years <= 0 || freq <= 0) return null;
  const r = rate / 100;
  const A = principal * Math.pow(1 + r / freq, freq * years);
  const interest = A - principal;
  return { finalAmount: A, interest, principalPct: (principal / A) * 100 };
}

function fmtUsd(n: number) {
  return '$' + n.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

const inputCls =
  'w-full rounded-lg border border-slate-300 px-3 py-2 pr-10 text-sm focus:border-brand focus:outline-none focus:ring-1 focus:ring-brand';

export default function CompoundInterestCalculator() {
  const [principal, setPrincipal] = useState('10000');
  const [rate, setRate]           = useState('7');
  const [years, setYears]         = useState('10');
  const [freq, setFreq]           = useState(12);

  const result = useMemo(
    () => calcCI(parseFloat(principal) || 0, parseFloat(rate) || 0, parseFloat(years) || 0, freq),
    [principal, rate, years, freq],
  );

  return (
    <div class="space-y-4">
      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Principal</label>
        <div class="relative">
          <span class="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">$</span>
          <input
            type="number" min="1" placeholder="10000"
            value={principal}
            onInput={(e) => setPrincipal((e.target as HTMLInputElement).value)}
            class={`${inputCls} pl-6`}
            aria-label="Principal amount in dollars"
          />
        </div>
      </div>

      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Annual Rate</label>
        <div class="relative">
          <input
            type="number" min="0" max="100" step="0.1" placeholder="7"
            value={rate}
            onInput={(e) => setRate((e.target as HTMLInputElement).value)}
            class={inputCls}
            aria-label="Annual interest rate as percentage"
          />
          <span class="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">%</span>
        </div>
      </div>

      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Time Period</label>
        <div class="relative">
          <input
            type="number" min="1" max="50" placeholder="10"
            value={years}
            onInput={(e) => setYears((e.target as HTMLInputElement).value)}
            class={inputCls}
            aria-label="Investment period in years"
          />
          <span class="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">yrs</span>
        </div>
      </div>

      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Compounding Frequency</label>
        <select
          class="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-brand focus:outline-none focus:ring-1 focus:ring-brand"
          value={freq}
          onChange={(e) => setFreq(parseInt((e.target as HTMLSelectElement).value, 10))}
          aria-label="Compounding frequency"
        >
          {FREQ_OPTIONS.map((o) => (
            <option key={o.value} value={o.value}>{o.label}</option>
          ))}
        </select>
      </div>

      {result && (
        <div role="status" aria-live="polite" class="space-y-3 rounded-xl border border-brand/20 bg-indigo-50 p-4">
          <div class="flex items-baseline justify-between">
            <span class="text-sm text-slate-600">Final Amount</span>
            <span class="text-2xl font-bold tabular-nums text-brand">{fmtUsd(result.finalAmount)}</span>
          </div>
          <div class="h-px bg-slate-200" />
          <div class="grid grid-cols-2 gap-2 text-sm">
            <div>
              <div class="text-slate-500">Principal</div>
              <div class="font-semibold text-slate-900">{fmtUsd(parseFloat(principal))}</div>
            </div>
            <div>
              <div class="text-slate-500">Interest Earned</div>
              <div class="font-semibold text-green-700">{fmtUsd(result.interest)}</div>
            </div>
          </div>
          {/* Principal vs growth bar */}
          <div>
            <div class="mb-1 flex justify-between text-[11px] text-slate-500">
              <span>Principal {result.principalPct.toFixed(0)}%</span>
              <span>Growth {(100 - result.principalPct).toFixed(0)}%</span>
            </div>
            <div class="flex h-2.5 overflow-hidden rounded-full">
              <div class="bg-brand" style={{ width: `${result.principalPct}%` }} />
              <div class="bg-green-400" style={{ width: `${100 - result.principalPct}%` }} />
            </div>
          </div>
        </div>
      )}

      <p class="text-xs leading-relaxed text-slate-500">
        For informational purposes only. Consult a licensed financial advisor.
      </p>
    </div>
  );
}
```

- [ ] **Step 2: Verify type-check**

```bash
pnpm --filter @site/financalc-io check
```

Expected: no errors.

- [ ] **Step 3: Commit**

```bash
git add sites/financalc.io/src/components/CompoundInterestCalculator.tsx
git commit -m "feat(financalc.io): add CompoundInterestCalculator Preact component

Co-Authored-By: Paperclip <noreply@paperclip.ing>"
```

---

## Task 7: ROICalculator Preact Component

**Files:**
- Create: `sites/financalc.io/src/components/ROICalculator.tsx`

- [ ] **Step 1: Create ROICalculator.tsx**

```tsx
import { useState, useMemo } from 'preact/hooks';

function calcROI(initial: number, finalVal: number, years: number | null) {
  if (initial <= 0 || finalVal < 0) return null;
  const roi = ((finalVal - initial) / initial) * 100;
  const netProfit = finalVal - initial;
  const annualized = (years && years > 0)
    ? (Math.pow(finalVal / initial, 1 / years) - 1) * 100
    : null;
  return { roi, netProfit, annualized };
}

function fmtUsd(n: number) {
  return '$' + n.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function fmtPct(n: number) {
  return (n >= 0 ? '+' : '') + n.toFixed(2) + '%';
}

const inputCls =
  'w-full rounded-lg border border-slate-300 px-3 py-2 pr-10 text-sm focus:border-brand focus:outline-none focus:ring-1 focus:ring-brand';

export default function ROICalculator() {
  const [initial, setInitial]   = useState('5000');
  const [finalVal, setFinalVal] = useState('7500');
  const [years, setYears]       = useState('');

  const result = useMemo(
    () => calcROI(
      parseFloat(initial) || 0,
      parseFloat(finalVal) || 0,
      years ? parseFloat(years) : null,
    ),
    [initial, finalVal, years],
  );

  const isPositive = result ? result.roi >= 0 : true;

  return (
    <div class="space-y-4">
      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Initial Investment</label>
        <div class="relative">
          <span class="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">$</span>
          <input
            type="number" min="0.01" step="any" placeholder="5000"
            value={initial}
            onInput={(e) => setInitial((e.target as HTMLInputElement).value)}
            class={`${inputCls} pl-6`}
            aria-label="Initial investment in dollars"
          />
        </div>
      </div>

      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Final Value</label>
        <div class="relative">
          <span class="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">$</span>
          <input
            type="number" min="0" step="any" placeholder="7500"
            value={finalVal}
            onInput={(e) => setFinalVal((e.target as HTMLInputElement).value)}
            class={`${inputCls} pl-6`}
            aria-label="Final value in dollars"
          />
        </div>
      </div>

      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">
          Time Period <span class="font-normal text-slate-400">(optional, for annualized return)</span>
        </label>
        <div class="relative">
          <input
            type="number" min="0.1" step="any" placeholder="e.g. 3"
            value={years}
            onInput={(e) => setYears((e.target as HTMLInputElement).value)}
            class={inputCls}
            aria-label="Investment period in years (optional)"
          />
          <span class="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">yrs</span>
        </div>
      </div>

      {result && (
        <div
          role="status"
          aria-live="polite"
          class={`space-y-3 rounded-xl border p-4 ${isPositive ? 'border-green-200 bg-green-50' : 'border-red-200 bg-red-50'}`}
        >
          <div class="flex items-baseline justify-between">
            <span class="text-sm text-slate-600">ROI</span>
            <span class={`text-3xl font-bold tabular-nums ${isPositive ? 'text-green-700' : 'text-red-600'}`}>
              {fmtPct(result.roi)}
            </span>
          </div>
          <div class="h-px bg-slate-200" />
          <div class={`grid gap-2 text-sm ${result.annualized !== null ? 'grid-cols-3' : 'grid-cols-2'}`}>
            <div>
              <div class="text-slate-500">Net Profit</div>
              <div class={`font-semibold ${isPositive ? 'text-green-700' : 'text-red-600'}`}>
                {fmtUsd(result.netProfit)}
              </div>
            </div>
            <div>
              <div class="text-slate-500">Initial</div>
              <div class="font-semibold text-slate-900">{fmtUsd(parseFloat(initial))}</div>
            </div>
            {result.annualized !== null && (
              <div>
                <div class="text-slate-500">Annualized</div>
                <div class="font-semibold text-slate-900">{fmtPct(result.annualized)}</div>
              </div>
            )}
          </div>
        </div>
      )}

      <p class="text-xs leading-relaxed text-slate-500">
        For informational purposes only. Consult a licensed financial advisor.
      </p>
    </div>
  );
}
```

- [ ] **Step 2: Verify type-check**

```bash
pnpm --filter @site/financalc-io check
```

Expected: no errors.

- [ ] **Step 3: Commit**

```bash
git add sites/financalc.io/src/components/ROICalculator.tsx
git commit -m "feat(financalc.io): add ROICalculator Preact component

Co-Authored-By: Paperclip <noreply@paperclip.ing>"
```

---

## Task 8: SavingsGoalCalculator Preact Component

**Files:**
- Create: `sites/financalc.io/src/components/SavingsGoalCalculator.tsx`

- [ ] **Step 1: Create SavingsGoalCalculator.tsx**

```tsx
import { useState, useMemo } from 'preact/hooks';

function calcSavings(goal: number, initial: number, monthly: number, annualRate: number) {
  if (goal <= 0 || monthly < 0) return null;
  const r = annualRate / 100 / 12;
  let balance = initial;
  let months = 0;
  // Iterate month by month (cap at 600 months = 50 years)
  while (balance < goal && months < 600) {
    balance = balance * (1 + r) + monthly;
    months++;
  }
  if (balance < goal) return null; // unreachable with zero contribution
  const totalContributed = initial + monthly * months;
  const interestEarned = balance - totalContributed;
  return { months, years: months / 12, totalContributed, interestEarned, finalBalance: balance };
}

function fmtUsd(n: number) {
  return '$' + n.toLocaleString('en-US', { minimumFractionDigits: 0, maximumFractionDigits: 0 });
}

const inputCls =
  'w-full rounded-lg border border-slate-300 px-3 py-2 pr-10 text-sm focus:border-brand focus:outline-none focus:ring-1 focus:ring-brand';

export default function SavingsGoalCalculator() {
  const [goal, setGoal]         = useState('50000');
  const [initial, setInitial]   = useState('1000');
  const [monthly, setMonthly]   = useState('500');
  const [rate, setRate]         = useState('4');

  const result = useMemo(
    () => calcSavings(
      parseFloat(goal) || 0,
      parseFloat(initial) || 0,
      parseFloat(monthly) || 0,
      parseFloat(rate) || 0,
    ),
    [goal, initial, monthly, rate],
  );

  return (
    <div class="space-y-4">
      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Savings Goal</label>
        <div class="relative">
          <span class="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">$</span>
          <input
            type="number" min="1" placeholder="50000"
            value={goal}
            onInput={(e) => setGoal((e.target as HTMLInputElement).value)}
            class={`${inputCls} pl-6`}
            aria-label="Savings goal in dollars"
          />
        </div>
      </div>

      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Initial Deposit</label>
        <div class="relative">
          <span class="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">$</span>
          <input
            type="number" min="0" placeholder="1000"
            value={initial}
            onInput={(e) => setInitial((e.target as HTMLInputElement).value)}
            class={`${inputCls} pl-6`}
            aria-label="Initial deposit in dollars"
          />
        </div>
      </div>

      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Monthly Contribution</label>
        <div class="relative">
          <span class="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">$</span>
          <input
            type="number" min="0" placeholder="500"
            value={monthly}
            onInput={(e) => setMonthly((e.target as HTMLInputElement).value)}
            class={`${inputCls} pl-6`}
            aria-label="Monthly contribution in dollars"
          />
        </div>
      </div>

      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Annual Return Rate</label>
        <div class="relative">
          <input
            type="number" min="0" max="100" step="0.1" placeholder="4"
            value={rate}
            onInput={(e) => setRate((e.target as HTMLInputElement).value)}
            class={inputCls}
            aria-label="Annual return rate as percentage"
          />
          <span class="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">%</span>
        </div>
      </div>

      {result ? (
        <div role="status" aria-live="polite" class="space-y-3 rounded-xl border border-brand/20 bg-indigo-50 p-4">
          <div class="flex items-baseline justify-between">
            <span class="text-sm text-slate-600">Time to Goal</span>
            <span class="text-2xl font-bold tabular-nums text-brand">
              {result.years < 1
                ? `${result.months} mo`
                : `${result.years.toFixed(1)} yrs`}
            </span>
          </div>
          <div class="h-px bg-slate-200" />
          <div class="grid grid-cols-2 gap-2 text-sm">
            <div>
              <div class="text-slate-500">Total Contributed</div>
              <div class="font-semibold text-slate-900">{fmtUsd(result.totalContributed)}</div>
            </div>
            <div>
              <div class="text-slate-500">Interest Earned</div>
              <div class="font-semibold text-green-700">{fmtUsd(result.interestEarned)}</div>
            </div>
          </div>
          {/* Contribution vs interest bar */}
          <div>
            {(() => {
              const contribPct = (result.totalContributed / result.finalBalance) * 100;
              return (
                <>
                  <div class="mb-1 flex justify-between text-[11px] text-slate-500">
                    <span>Contributions {contribPct.toFixed(0)}%</span>
                    <span>Interest {(100 - contribPct).toFixed(0)}%</span>
                  </div>
                  <div class="flex h-2.5 overflow-hidden rounded-full">
                    <div class="bg-brand" style={{ width: `${contribPct}%` }} />
                    <div class="bg-green-400" style={{ width: `${100 - contribPct}%` }} />
                  </div>
                </>
              );
            })()}
          </div>
        </div>
      ) : (
        <div class="rounded-xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-800">
          Goal unreachable in 50 years with these inputs. Try increasing your monthly contribution or rate.
        </div>
      )}

      <p class="text-xs leading-relaxed text-slate-500">
        For informational purposes only. Consult a licensed financial advisor.
      </p>
    </div>
  );
}
```

- [ ] **Step 2: Verify type-check**

```bash
pnpm --filter @site/financalc-io check
```

Expected: no errors.

- [ ] **Step 3: Commit**

```bash
git add sites/financalc.io/src/components/SavingsGoalCalculator.tsx
git commit -m "feat(financalc.io): add SavingsGoalCalculator Preact component

Co-Authored-By: Paperclip <noreply@paperclip.ing>"
```

---

## Task 9: Tool Content Files (MDX)

**Files:**
- Create: `sites/financalc.io/src/content/tools/loan-calculator.md`
- Create: `sites/financalc.io/src/content/tools/compound-interest-calculator.md`
- Create: `sites/financalc.io/src/content/tools/roi-calculator.md`
- Create: `sites/financalc.io/src/content/tools/savings-goal-calculator.md`

- [ ] **Step 1: Create loan-calculator.md**

```markdown
---
title: "Loan Calculator"
description: "Calculate monthly payments, total interest, and total cost for any loan. Works for personal loans, auto loans, and fixed-rate mortgages."
urlSlug: "loan-calculator"
publishDate: 2026-04-25
schema:
  applicationCategory: "FinanceApplication"
  operatingSystem: "Web"
  price: "0"
  priceCurrency: "USD"
---

## What Is a Loan Calculator?

A loan calculator computes your fixed monthly payment based on three inputs: the amount you borrow (principal), the annual interest rate, and the repayment term. It uses the standard amortization formula to show exactly how much of each payment goes toward interest versus principal.

## How to Use This Calculator

1. Enter the **loan amount** — the total amount you want to borrow.
2. Enter the **annual interest rate** as a percentage (e.g., 6.5 for 6.5%).
3. Enter the **loan term** in years.

The calculator updates instantly as you type.

## The Loan Payment Formula

The monthly payment *M* is calculated as:

**M = P × [r(1 + r)^n] / [(1 + r)^n − 1]**

Where:
- *P* = principal loan amount
- *r* = monthly interest rate (annual rate ÷ 12)
- *n* = total number of monthly payments (years × 12)

## Understanding Your Results

**Monthly Payment** is the fixed amount due each month for the life of the loan.

**Total Paid** is monthly payment × number of payments — the full cost of the loan.

**Total Interest** is total paid minus the original principal. This is the cost of borrowing.

The principal-to-interest bar shows the proportion of your total payments that go to interest. Shorter terms and lower rates reduce the interest share significantly.

## When to Use a Loan Calculator

- Comparing offers from multiple lenders before signing
- Deciding between a shorter term (higher payment, less interest) and a longer term (lower payment, more interest)
- Estimating affordability before applying for a personal loan or auto loan
- Understanding how extra payments would reduce your total interest

## Limitations

This calculator assumes a fixed interest rate and equal monthly payments. It does not account for origination fees, prepayment penalties, variable-rate adjustments, or taxes and insurance (relevant for mortgages).
```

- [ ] **Step 2: Create compound-interest-calculator.md**

```markdown
---
title: "Compound Interest Calculator"
description: "See how your money grows with compound interest. Calculate final balance and total interest earned for any principal, rate, time, and compounding frequency."
urlSlug: "compound-interest-calculator"
publishDate: 2026-04-25
schema:
  applicationCategory: "FinanceApplication"
  operatingSystem: "Web"
  price: "0"
  priceCurrency: "USD"
---

## What Is Compound Interest?

Compound interest is interest calculated on both the initial principal and the accumulated interest from previous periods. Unlike simple interest (calculated only on the principal), compound interest causes your balance to grow exponentially over time — a phenomenon often called "the eighth wonder of the world."

## How to Use This Calculator

1. Enter your **principal** — the initial amount you invest or deposit.
2. Enter the **annual interest rate** as a percentage.
3. Enter the **time period** in years.
4. Select the **compounding frequency** — how often interest is added to the balance.

## The Compound Interest Formula

**A = P × (1 + r/n)^(n×t)**

Where:
- *A* = final amount
- *P* = principal
- *r* = annual interest rate (decimal)
- *n* = compounding periods per year
- *t* = time in years

## How Compounding Frequency Affects Growth

More frequent compounding produces slightly higher returns because interest earns interest sooner:

| Frequency | $10,000 at 7% for 10 years |
|-----------|---------------------------|
| Annually | $19,671.51 |
| Quarterly | $20,015.75 |
| Monthly | $20,096.61 |
| Daily | $20,137.33 |

The difference becomes more meaningful over longer periods and higher balances.

## The Power of Time

Time is the most powerful variable in compound interest. Starting early, even with a smaller principal, often outperforms a larger investment made later:

- $5,000 at 7% for 30 years → $38,061
- $10,000 at 7% for 20 years → $38,697

Both produce nearly identical results, but the first requires half the initial investment.

## Limitations

This calculator assumes a constant rate, no additional contributions, and no withdrawals. Real investments fluctuate in value. Past performance does not guarantee future results.
```

- [ ] **Step 3: Create roi-calculator.md**

```markdown
---
title: "ROI Calculator"
description: "Calculate return on investment (ROI) as a percentage. Includes annualized return when you provide the investment period."
urlSlug: "roi-calculator"
publishDate: 2026-04-25
schema:
  applicationCategory: "FinanceApplication"
  operatingSystem: "Web"
  price: "0"
  priceCurrency: "USD"
---

## What Is ROI?

Return on Investment (ROI) measures the gain or loss on an investment relative to its cost. It is one of the most widely used metrics for evaluating investment performance across asset classes — stocks, real estate, business investments, and more.

## How to Use This Calculator

1. Enter your **initial investment** — the amount you put in.
2. Enter the **final value** — what the investment is worth now (or at exit).
3. Optionally enter the **time period** in years to see the annualized return.

## The ROI Formula

**ROI = [(Final Value − Initial Investment) / Initial Investment] × 100**

For example: invest $5,000, sell for $7,500 → ROI = [(7500 − 5000) / 5000] × 100 = **50%**

## Annualized Return (CAGR)

A simple ROI percentage doesn't account for how long you held the investment. To compare investments held for different periods, use the **Compound Annual Growth Rate (CAGR)**:

**CAGR = [(Final Value / Initial Investment)^(1/years) − 1] × 100**

A 50% total return over 2 years is a ~22.5% CAGR. Over 5 years it would be ~8.4% CAGR — a very different picture.

## Interpreting Results

- **Positive ROI** means you gained money relative to what you invested.
- **Negative ROI** means a loss.
- The **annualized return** allows fair comparison between investments held for different time periods.

## What ROI Does Not Capture

ROI is simple to calculate but ignores:
- **Risk** — a 20% ROI in a volatile asset is not equivalent to 20% in a stable one.
- **Time value of money** — money received sooner is worth more than money received later.
- **Taxes and fees** — transaction costs, capital gains taxes, and management fees reduce real returns.
- **Inflation** — a nominal 5% return with 3% inflation is only 2% in real terms.

Always consider ROI alongside risk-adjusted metrics when evaluating investment decisions.
```

- [ ] **Step 4: Create savings-goal-calculator.md**

```markdown
---
title: "Savings Goal Calculator"
description: "Find out how long it takes to reach a savings goal with regular monthly contributions and compound interest. Plan for a house down payment, emergency fund, or any target."
urlSlug: "savings-goal-calculator"
publishDate: 2026-04-25
schema:
  applicationCategory: "FinanceApplication"
  operatingSystem: "Web"
  price: "0"
  priceCurrency: "USD"
---

## What Is a Savings Goal Calculator?

A savings goal calculator tells you how long it will take to reach a specific savings target given your starting balance, regular contributions, and expected annual return. It combines the future value of a lump sum with the future value of an annuity (regular contributions).

## How to Use This Calculator

1. Enter your **savings goal** — the target balance you want to reach.
2. Enter your **initial deposit** — any amount you're starting with (can be zero).
3. Enter your **monthly contribution** — how much you'll add each month.
4. Enter your **annual return rate** as a percentage (use a savings account rate or a conservative investment return).

## How the Calculation Works

Each month, your balance earns interest and then receives your contribution:

**Balance(month+1) = Balance(month) × (1 + r) + monthly_contribution**

Where *r* is the monthly rate (annual rate ÷ 12). The calculator iterates this formula until the balance reaches your goal.

## Common Savings Goals

| Goal | Typical Target | Strategy |
|------|---------------|----------|
| Emergency fund | 3–6 months of expenses | High-yield savings, FDIC insured |
| House down payment | 5–20% of purchase price | HYSA or short-term bonds |
| New car | $5,000–$40,000 | Short-term savings or CD |
| Retirement milestone | Varies | Tax-advantaged accounts (401k, IRA) |

## Tips for Reaching Your Goal Faster

- **Increase your monthly contribution** — even small increases compound significantly over time.
- **Start with a larger initial deposit** — a bigger starting balance means more interest from day one.
- **Use a high-yield savings account** — online HYSA rates can be 4–5% versus 0.01% at traditional banks.
- **Automate transfers** — automatic monthly contributions remove the temptation to spend.

## Limitations

This calculator assumes a fixed rate of return and consistent monthly contributions. It does not account for taxes on interest, account fees, or investment volatility. For retirement planning over long horizons, consider consulting a certified financial planner.
```

- [ ] **Step 5: Verify type-check and build**

```bash
pnpm --filter @site/financalc-io check && pnpm --filter @site/financalc-io build
```

Expected: clean build with 4 tool pages generated.

- [ ] **Step 6: Commit**

```bash
git add sites/financalc.io/src/content/tools/
git commit -m "feat(financalc.io): add 4 tool content files with SEO prose

Co-Authored-By: Paperclip <noreply@paperclip.ing>"
```

---

## Task 10: Wire Preact Calculators into tools/[...slug].astro

**Files:**
- Modify: `sites/financalc.io/src/pages/tools/[...slug].astro`

- [ ] **Step 1: Replace tools/[...slug].astro**

```astro
---
import ToolLayout from '~/layouts/ToolLayout.astro';
import { getCollection, type CollectionEntry } from 'astro:content';
import { siteConfig } from '~/config/site.config';
import LoanCalculator from '~/components/LoanCalculator';
import CompoundInterestCalculator from '~/components/CompoundInterestCalculator';
import ROICalculator from '~/components/ROICalculator';
import SavingsGoalCalculator from '~/components/SavingsGoalCalculator';

export async function getStaticPaths() {
  if (!siteConfig.features.hasTool) return [];
  const tools = await getCollection('tools', ({ data }) => !data.draft);
  return tools.map((tool) => ({
    params: { slug: tool.data.urlSlug },
    props: { tool },
  }));
}

interface Props { tool: CollectionEntry<'tools'> }
const { tool } = Astro.props;
const { Content } = await tool.render();
const s = tool.data.schema;

const calculatorMap: Record<string, any> = {
  'loan-calculator': LoanCalculator,
  'compound-interest-calculator': CompoundInterestCalculator,
  'roi-calculator': ROICalculator,
  'savings-goal-calculator': SavingsGoalCalculator,
};

const ToolComponent = calculatorMap[tool.data.urlSlug];
---
<ToolLayout
  title={tool.data.title}
  description={tool.data.description}
  slug={tool.data.urlSlug}
  applicationCategory={s.applicationCategory}
  operatingSystem={s.operatingSystem}
  price={s.price}
  priceCurrency={s.priceCurrency}
  ratingValue={s.ratingValue}
  ratingCount={s.ratingCount}
>
  {ToolComponent
    ? <ToolComponent slot="tool" client:load />
    : (
      <div slot="tool" class="rounded border border-dashed border-slate-300 bg-white p-6 text-center text-sm text-slate-500">
        Calculator coming soon.
      </div>
    )
  }
  <Content />
</ToolLayout>
```

- [ ] **Step 2: Verify build**

```bash
pnpm --filter @site/financalc-io build
```

Expected: clean build, 4 tool pages at `/tools/loan-calculator/`, `/tools/compound-interest-calculator/`, `/tools/roi-calculator/`, `/tools/savings-goal-calculator/`.

- [ ] **Step 3: Commit**

```bash
git add sites/financalc.io/src/pages/tools/
git commit -m "feat(financalc.io): wire Preact calculators into per-tool pages

Co-Authored-By: Paperclip <noreply@paperclip.ing>"
```

---

## Task 11: Redesign Homepage as Tool Directory

**Files:**
- Modify: `sites/financalc.io/src/pages/index.astro`

- [ ] **Step 1: Replace index.astro**

```astro
---
import BaseLayout from '~/layouts/BaseLayout.astro';
import { siteConfig } from '~/config/site.config';
import { getCollection } from 'astro:content';

const recentPosts = siteConfig.features.hasBlog
  ? (await getCollection('blog', ({ data }) => !data.draft))
      .sort((a, b) => b.data.publishDate.valueOf() - a.data.publishDate.valueOf())
      .slice(0, 3)
  : [];

const tools = siteConfig.features.hasTool
  ? await getCollection('tools', ({ data }) => !data.draft)
  : [];

const TOOL_ICONS: Record<string, string> = {
  'loan-calculator':               '🏦',
  'compound-interest-calculator':  '📈',
  'roi-calculator':                '💹',
  'savings-goal-calculator':       '🏆',
};
---
<BaseLayout
  title="Free Financial Calculators — FinanceCalc"
  description="Free online financial calculators: loan payment, compound interest, ROI, and savings goal. Accurate, instant results — no signup required."
>

  <!-- Hero -->
  <header class="pb-8 pt-4">
    <h1 class="text-4xl font-bold tracking-tight text-slate-900 sm:text-5xl">
      Free Financial Calculators
    </h1>
    <p class="mt-3 max-w-xl text-lg text-slate-600">
      Instant, accurate calculators for loans, investments, and savings goals — all client-side, no data sent to servers.
    </p>
  </header>

  <!-- Trust signals -->
  <ul class="flex flex-wrap gap-x-6 gap-y-2 text-sm text-slate-600">
    {[
      'Instant results as you type',
      'No data stored or shared',
      'Free, no signup required',
      'Mobile & desktop friendly',
    ].map((badge) => (
      <li class="flex items-center gap-1.5">
        <svg class="h-4 w-4 shrink-0 text-brand" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z" clip-rule="evenodd" />
        </svg>
        {badge}
      </li>
    ))}
  </ul>

  <!-- Tool cards grid -->
  {tools.length > 0 && (
    <section class="mt-10" aria-labelledby="tools-heading">
      <h2 id="tools-heading" class="sr-only">Our Calculators</h2>
      <ul class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {tools.map((tool) => (
          <li>
            <a
              href={`/tools/${tool.data.urlSlug}/`}
              class="group flex h-full flex-col rounded-2xl border border-slate-200 bg-white p-5 transition hover:border-brand/40 hover:shadow-md"
            >
              <span class="text-3xl" aria-hidden="true">
                {TOOL_ICONS[tool.data.urlSlug] ?? '🧮'}
              </span>
              <h3 class="mt-3 text-base font-semibold text-slate-900 group-hover:text-brand">
                {tool.data.title}
              </h3>
              <p class="mt-1 flex-1 text-sm text-slate-600 line-clamp-2">{tool.data.description}</p>
              <span class="mt-3 text-sm font-medium text-brand">
                Open Calculator →
              </span>
            </a>
          </li>
        ))}
      </ul>
    </section>
  )}

  <!-- YMYL financial disclaimer -->
  <aside
    role="note"
    class="mt-10 rounded-lg border border-amber-200 bg-amber-50 p-4 text-sm text-amber-900"
  >
    <strong class="font-semibold">Important:</strong> All calculators provide estimates for
    informational purposes only. Results do not constitute financial advice. Consult a licensed
    financial advisor before making investment, borrowing, or savings decisions.
  </aside>

  <!-- SEO intro -->
  <section class="prose prose-slate mt-10 max-w-none">
    <h2>About FinanceCalc</h2>
    <p>
      FinanceCalc offers a growing suite of free financial calculators designed to help you
      make smarter money decisions. Whether you're comparing loan offers, projecting investment
      growth, or planning how long it takes to reach a savings milestone, our tools give you
      instant, accurate answers without requiring an account or sharing personal data.
    </p>
    <p>
      Every calculation runs locally in your browser. We do not collect, store, or transmit
      any of the numbers you enter. Our calculators implement standard financial formulas —
      the same methods used by banks and financial planning software — and are reviewed
      regularly for accuracy.
    </p>
    <h3>How to Choose the Right Calculator</h3>
    <ul>
      <li><strong>Borrowing money?</strong> Use the <a href="/tools/loan-calculator/">Loan Calculator</a> to find your monthly payment and total interest cost.</li>
      <li><strong>Growing an investment?</strong> Use the <a href="/tools/compound-interest-calculator/">Compound Interest Calculator</a> to project your balance over time.</li>
      <li><strong>Evaluating a past investment?</strong> Use the <a href="/tools/roi-calculator/">ROI Calculator</a> to measure your return and annualized rate.</li>
      <li><strong>Saving toward a goal?</strong> Use the <a href="/tools/savings-goal-calculator/">Savings Goal Calculator</a> to find out when you'll get there.</li>
    </ul>
  </section>

  <!-- Recent blog posts -->
  {recentPosts.length > 0 && (
    <section class="mt-16" aria-labelledby="articles-heading">
      <h2 id="articles-heading" class="text-2xl font-bold text-slate-900">Latest Articles</h2>
      <ul class="mt-6 grid gap-4 sm:grid-cols-3">
        {recentPosts.map((post) => (
          <li>
            <a
              href={`/blog/${post.slug}/`}
              class="group block rounded-xl border border-slate-200 bg-white p-5 transition hover:border-brand/40 hover:shadow-sm"
            >
              <time
                datetime={post.data.publishDate.toISOString()}
                class="text-xs font-medium uppercase tracking-wide text-slate-400"
              >
                {post.data.publishDate.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })}
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
        <a href="/blog/" class="text-sm font-medium text-brand underline underline-offset-2 hover:opacity-80">
          View all articles →
        </a>
      </div>
    </section>
  )}

</BaseLayout>
```

- [ ] **Step 2: Run full build**

```bash
pnpm --filter @site/financalc-io build
```

Expected: clean build with homepage + 4 tool pages.

- [ ] **Step 3: Commit**

```bash
git add sites/financalc.io/src/pages/index.astro
git commit -m "feat(financalc.io): redesign homepage as tool-directory landing page

Co-Authored-By: Paperclip <noreply@paperclip.ing>"
```

---

## Task 12: Final Verification

- [ ] **Step 1: Run full build**

```bash
pnpm --filter @site/financalc-io build
```

Expected: zero errors, dist folder generated.

- [ ] **Step 2: Run type-check**

```bash
pnpm --filter @site/financalc-io check
```

Expected: zero TypeScript errors.

- [ ] **Step 3: Confirm expected pages in dist**

```bash
ls /home/abovespec/site-network/sites/financalc.io/dist/tools/
```

Expected directories: `loan-calculator/`, `compound-interest-calculator/`, `roi-calculator/`, `savings-goal-calculator/`

---

## Self-Review Notes

**Spec coverage check:**
- ✅ Multi-tool index as tool directory — Task 11
- ✅ Two-column sticky layout per tool page — Task 3 (ToolLayout)
- ✅ YMYL financial disclaimer (amber box) — Tasks 3, 11
- ✅ Reviewed-by slot — Tasks 3, 4
- ✅ Sources footer — Tasks 3, 4
- ✅ 4 Preact calculator components — Tasks 5–8
- ✅ Enable hasTool + hasBlog — Task 1
- ✅ YMYL blog schema fields — Task 2
- ✅ PostLayout financial chrome — Task 4
- ✅ Tool content files (SEO prose) — Task 9
- ✅ Wire calculators to tool pages — Task 10
- ✅ `pnpm --filter @site/financalc-io build` clean — Task 12

**Type consistency:**
- `fmtUsd` is defined locally in each calculator component (no shared utility) — intentional, avoids premature abstraction
- `sources` prop type `Array<{ text: string; url?: string }>` is consistent across ToolLayout, PostLayout
- `reviewedBy?: string`, `lastReviewedAt?: Date | string` consistent across both layouts
- `calculatorMap` in `[...slug].astro` uses `any` — acceptable at the Astro page boundary since Preact components accept no external props in this use case
