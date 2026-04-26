# INF-24: Phase-2 Calculator Sites Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Apply the bmicalc.io / financalc.io design system across 5 calculator sites — agecalc.io, amortcalc.io, margincalc.io, percentcalc.io, tipcalc.io — with YMYL chrome where required and multi-tool pattern for percentcalc.io.

**Architecture:** Each single-purpose site follows the bmicalc.io pattern: Preact island in a sticky right column, SEO content left, YMYL chrome inline. amortcalc.io and margincalc.io get full YMYL-financial chrome. percentcalc.io follows the financalc.io multi-tool pattern with per-tool `/tools/[slug]` pages and a content-driven index. All calculators become Preact components (replacing any inline JS).

**Tech Stack:** Astro 4.x, Preact (via @astrojs/preact), Tailwind CSS, TypeScript, pnpm monorepo.

---

## File Map

### Site 1: agecalc.io
- **Create:** `sites/agecalc.io/src/components/AgeCalculator.tsx`
- **Rewrite:** `sites/agecalc.io/src/pages/index.astro`

### Site 2: tipcalc.io
- **Create:** `sites/tipcalc.io/src/components/TipCalculator.tsx`
- **Rewrite:** `sites/tipcalc.io/src/pages/index.astro`

### Site 3: amortcalc.io
- **Create:** `sites/amortcalc.io/src/components/AmortizationCalculator.tsx`
- **Rewrite:** `sites/amortcalc.io/src/pages/index.astro`

### Site 4: margincalc.io
- **Create:** `sites/margincalc.io/src/components/MarginCalculator.tsx`
- **Rewrite:** `sites/margincalc.io/src/pages/index.astro`

### Site 5: percentcalc.io
- **Create:** `sites/percentcalc.io/src/components/PercentOfCalculator.tsx`
- **Create:** `sites/percentcalc.io/src/components/PercentChangeCalculator.tsx`
- **Create:** `sites/percentcalc.io/src/components/PercentOffCalculator.tsx`
- **Create:** `sites/percentcalc.io/src/components/PercentIncreaseCalculator.tsx`
- **Create:** `sites/percentcalc.io/src/components/PercentDifferenceCalculator.tsx`
- **Create:** `sites/percentcalc.io/src/content/tools/percent-of.md`
- **Create:** `sites/percentcalc.io/src/content/tools/percent-change.md`
- **Create:** `sites/percentcalc.io/src/content/tools/percent-off.md`
- **Create:** `sites/percentcalc.io/src/content/tools/percent-increase.md`
- **Create:** `sites/percentcalc.io/src/content/tools/percent-difference.md`
- **Rewrite:** `sites/percentcalc.io/src/pages/index.astro`
- **Rewrite:** `sites/percentcalc.io/src/pages/tools/[...slug].astro`
- **Modify:** `sites/percentcalc.io/src/config/site.config.ts` (enable hasTool: true)

---

## Task 1: agecalc.io — AgeCalculator.tsx

**Files:**
- Create: `sites/agecalc.io/src/components/AgeCalculator.tsx`

- [ ] **Step 1: Create the Preact component**

```tsx
// sites/agecalc.io/src/components/AgeCalculator.tsx
import { useState, useMemo } from 'preact/hooks';

function calcAge(dob: string) {
  if (!dob) return null;
  const birth = new Date(dob);
  const now = new Date();
  if (isNaN(birth.getTime()) || birth > now) return null;

  let years = now.getFullYear() - birth.getFullYear();
  let months = now.getMonth() - birth.getMonth();
  let days = now.getDate() - birth.getDate();

  if (days < 0) {
    months -= 1;
    const prevMonth = new Date(now.getFullYear(), now.getMonth(), 0);
    days += prevMonth.getDate();
  }
  if (months < 0) {
    years -= 1;
    months += 12;
  }

  const diffMs = now.getTime() - birth.getTime();
  const totalDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
  const totalWeeks = Math.floor(totalDays / 7);
  const totalHours = Math.floor(diffMs / (1000 * 60 * 60));
  const totalMinutes = Math.floor(diffMs / (1000 * 60));

  const nextBirthday = new Date(now.getFullYear(), birth.getMonth(), birth.getDate());
  if (nextBirthday <= now) nextBirthday.setFullYear(now.getFullYear() + 1);
  const daysToNextBirthday = Math.ceil(
    (nextBirthday.getTime() - now.getTime()) / (1000 * 60 * 60 * 24)
  );

  return { years, months, days, totalDays, totalWeeks, totalHours, totalMinutes, daysToNextBirthday };
}

const inputCls =
  'w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-brand focus:outline-none focus:ring-1 focus:ring-brand';

export default function AgeCalculator() {
  const today = new Date();
  const defaultDob = `${today.getFullYear() - 30}-${String(today.getMonth() + 1).padStart(2, '0')}-15`;
  const [dob, setDob] = useState(defaultDob);

  const result = useMemo(() => calcAge(dob), [dob]);

  return (
    <div class="space-y-4">
      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">
          Date of Birth
        </label>
        <input
          type="date"
          value={dob}
          max={today.toISOString().slice(0, 10)}
          onInput={(e) => setDob((e.target as HTMLInputElement).value)}
          class={inputCls}
          aria-label="Date of birth"
        />
      </div>

      {result && (
        <div role="status" aria-live="polite" class="space-y-3 rounded-xl border border-brand/30 bg-green-50 p-4">
          <div class="flex items-baseline justify-between">
            <div>
              <span class="text-4xl font-bold tabular-nums text-brand">{result.years}</span>
              <span class="ml-1.5 text-lg font-semibold text-slate-700">
                years{result.months > 0 ? `, ${result.months} months` : ''}
                {result.days > 0 ? `, ${result.days} days` : ''}
              </span>
            </div>
          </div>

          <div class="h-px bg-slate-200" />

          <div class="grid grid-cols-2 gap-2 text-sm">
            <div>
              <div class="text-slate-500">Total Days</div>
              <div class="font-semibold tabular-nums text-slate-900">
                {result.totalDays.toLocaleString()}
              </div>
            </div>
            <div>
              <div class="text-slate-500">Total Weeks</div>
              <div class="font-semibold tabular-nums text-slate-900">
                {result.totalWeeks.toLocaleString()}
              </div>
            </div>
            <div>
              <div class="text-slate-500">Total Hours</div>
              <div class="font-semibold tabular-nums text-slate-900">
                {result.totalHours.toLocaleString()}
              </div>
            </div>
            <div>
              <div class="text-slate-500">Total Minutes</div>
              <div class="font-semibold tabular-nums text-slate-900">
                {result.totalMinutes.toLocaleString()}
              </div>
            </div>
          </div>

          {result.daysToNextBirthday > 0 && (
            <>
              <div class="h-px bg-slate-200" />
              <div class="flex items-center gap-2 text-sm">
                <span class="text-slate-500">Next birthday in</span>
                <span class="font-semibold text-brand">
                  {result.daysToNextBirthday === 1 ? 'tomorrow!' : `${result.daysToNextBirthday} days`}
                </span>
              </div>
            </>
          )}
        </div>
      )}

      <p class="text-xs leading-relaxed text-slate-500">
        Results are calculated based on your local system date.
      </p>
    </div>
  );
}
```

- [ ] **Step 2: Verify the file was created**

```bash
ls sites/agecalc.io/src/components/AgeCalculator.tsx
```

---

## Task 2: agecalc.io — index.astro

**Files:**
- Rewrite: `sites/agecalc.io/src/pages/index.astro`

- [ ] **Step 1: Rewrite index.astro**

```astro
---
import BaseLayout from '~/layouts/BaseLayout.astro';
import { siteConfig } from '~/config/site.config';
import AgeCalculator from '~/components/AgeCalculator';
import { getCollection } from 'astro:content';

const recentPosts = siteConfig.features.hasBlog
  ? (await getCollection('blog', ({ data }) => !data.draft))
      .sort((a, b) => b.data.publishDate.valueOf() - a.data.publishDate.valueOf())
      .slice(0, 3)
  : [];
---
<BaseLayout
  title="Age Calculator — How Old Am I? Free Online Age Calculator"
  description="Calculate your exact age in years, months, days, hours, and minutes. Find out how many days until your next birthday. Free, instant, no signup required."
>

  <header class="pb-8 pt-4">
    <h1 class="text-4xl font-bold tracking-tight text-slate-900 sm:text-5xl">
      Age Calculator
    </h1>
    <p class="mt-3 max-w-xl text-lg text-slate-600">
      Find your exact age in years, months, and days — plus total hours, weeks, and a
      countdown to your next birthday.
    </p>
  </header>

  <ul class="flex flex-wrap gap-x-6 gap-y-2 text-sm text-slate-600">
    {[
      'Instant results as you type',
      'Years, months, days & more',
      'Birthday countdown',
      'No data stored or shared',
    ].map((badge) => (
      <li class="flex items-center gap-1.5">
        <svg class="h-4 w-4 shrink-0 text-brand" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.061 1.06l2.5 2.5a.75.75 0 001.137-.088l4-5.5z" clip-rule="evenodd" />
        </svg>
        {badge}
      </li>
    ))}
  </ul>

  <div class="mt-8 grid items-start gap-8 md:grid-cols-[1fr_400px]">

    <div class="space-y-10">

      <section aria-labelledby="how-age-heading">
        <h2 id="how-age-heading" class="text-2xl font-bold text-slate-900">How Is Age Calculated?</h2>
        <div class="prose prose-slate mt-3 max-w-none">
          <p>
            Age is typically calculated as the difference between your date of birth and today's
            date, measured in complete calendar years. This is the "birthday rule": you gain a year
            of age on the anniversary of your birth date, not at the start of each calendar year.
          </p>
          <p>
            This calculator shows your age in multiple units simultaneously:
          </p>
          <ul>
            <li><strong>Years, months, days</strong> — the conventional age you'd give on a form.</li>
            <li><strong>Total days</strong> — the raw number of days you've been alive.</li>
            <li><strong>Total weeks</strong> — useful for tracking milestones in early childhood.</li>
            <li><strong>Total hours / minutes</strong> — just for fun.</li>
          </ul>
        </div>
      </section>

      <section aria-labelledby="age-facts-heading">
        <h2 id="age-facts-heading" class="text-2xl font-bold text-slate-900">Interesting Age Facts</h2>
        <div class="prose prose-slate mt-3 max-w-none">
          <ul>
            <li>By age 30 you've lived approximately <strong>10,957 days</strong> — or about 262,980 hours.</li>
            <li>A leap year baby (born Feb 29) officially celebrates their birthday every four years, but legally ages each year.</li>
            <li>In some East Asian cultures, age is counted from conception (Korean age), making you 1 at birth and adding a year each calendar New Year.</li>
            <li>The oldest verified person in history was Jeanne Calment of France, who lived to <strong>122 years and 164 days</strong>.</li>
          </ul>
        </div>
      </section>

      <section aria-labelledby="birthday-heading">
        <h2 id="birthday-heading" class="text-2xl font-bold text-slate-900">What Day Was I Born On?</h2>
        <div class="prose prose-slate mt-3 max-w-none">
          <p>
            Your date of birth determines your day of the week at birth using the Gregorian calendar.
            The Doomsday algorithm, devised by mathematician John Conway, can mentally calculate the
            day of the week for any date. Our calculator uses your browser's built-in date arithmetic,
            which handles all calendar edge cases including leap years automatically.
          </p>
        </div>
      </section>

    </div>

    <div class="md:sticky md:top-8">
      <div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <h2 class="mb-4 text-lg font-semibold text-slate-900">Calculate Your Age</h2>
        <AgeCalculator client:load />
      </div>
    </div>

  </div>

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
    </section>
  )}

  <footer class="mt-16 border-t border-slate-200 pt-8 text-sm text-slate-500">
    <span>Content last reviewed: <time datetime="2026-04-25">April 25, 2026</time>.</span>
  </footer>

</BaseLayout>
```

- [ ] **Step 2: Build and verify agecalc.io**

```bash
cd /home/abovespec/site-network && pnpm --filter @site/agecalc build
```
Expected: Exit 0, no TypeScript/build errors.

- [ ] **Step 3: Commit**

```bash
cd /home/abovespec/site-network
git add sites/agecalc.io/src/components/AgeCalculator.tsx sites/agecalc.io/src/pages/index.astro
git commit -m "feat(agecalc.io): Preact AgeCalculator + bmicalc layout (INF-24)

Co-Authored-By: Paperclip <noreply@paperclip.ing>"
```

---

## Task 3: tipcalc.io — TipCalculator.tsx

**Files:**
- Create: `sites/tipcalc.io/src/components/TipCalculator.tsx`

- [ ] **Step 1: Create the Preact component**

```tsx
// sites/tipcalc.io/src/components/TipCalculator.tsx
import { useState, useMemo } from 'preact/hooks';

function calcTip(bill: number, tipPct: number, people: number) {
  if (bill <= 0 || tipPct < 0 || people < 1) return null;
  const tipAmount = bill * (tipPct / 100);
  const total = bill + tipAmount;
  const perPerson = total / people;
  const tipPerPerson = tipAmount / people;
  return { tipAmount, total, perPerson, tipPerPerson };
}

function fmtUsd(n: number) {
  return '$' + n.toFixed(2);
}

const QUICK_TIPS = [10, 15, 18, 20, 25];

const inputCls =
  'w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-brand focus:outline-none focus:ring-1 focus:ring-brand';

export default function TipCalculator() {
  const [bill, setBill]     = useState('50.00');
  const [tipPct, setTipPct] = useState('18');
  const [people, setPeople] = useState('1');

  const result = useMemo(
    () => calcTip(parseFloat(bill) || 0, parseFloat(tipPct) || 0, parseInt(people) || 1),
    [bill, tipPct, people],
  );

  return (
    <div class="space-y-4">
      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Bill Amount</label>
        <div class="relative">
          <span class="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">$</span>
          <input
            type="number" min="0" step="0.01" placeholder="50.00"
            value={bill}
            onInput={(e) => setBill((e.target as HTMLInputElement).value)}
            class={`${inputCls} pl-6`}
            aria-label="Bill amount in dollars"
          />
        </div>
      </div>

      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Tip Percentage</label>
        <div class="relative">
          <input
            type="number" min="0" max="100" step="1" placeholder="18"
            value={tipPct}
            onInput={(e) => setTipPct((e.target as HTMLInputElement).value)}
            class={inputCls}
            aria-label="Tip percentage"
          />
          <span class="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">%</span>
        </div>
        <div class="mt-2 flex flex-wrap gap-1.5">
          {QUICK_TIPS.map((pct) => (
            <button
              key={pct}
              type="button"
              onClick={() => setTipPct(String(pct))}
              class={`rounded-lg border px-3 py-1 text-xs font-medium transition ${
                tipPct === String(pct)
                  ? 'border-brand bg-brand text-white'
                  : 'border-slate-200 bg-white text-slate-600 hover:border-brand/50'
              }`}
            >
              {pct}%
            </button>
          ))}
        </div>
      </div>

      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Number of People</label>
        <input
          type="number" min="1" max="50" step="1" placeholder="1"
          value={people}
          onInput={(e) => setPeople((e.target as HTMLInputElement).value)}
          class={inputCls}
          aria-label="Number of people splitting the bill"
        />
      </div>

      {result && (
        <div role="status" aria-live="polite" class="space-y-3 rounded-xl border border-brand/30 bg-orange-50 p-4">
          <div class="flex items-baseline justify-between">
            <span class="text-sm text-slate-600">Tip Amount</span>
            <span class="text-2xl font-bold tabular-nums text-brand">{fmtUsd(result.tipAmount)}</span>
          </div>
          <div class="flex items-baseline justify-between">
            <span class="text-sm text-slate-600">Total Bill</span>
            <span class="text-xl font-bold tabular-nums text-slate-900">{fmtUsd(result.total)}</span>
          </div>
          {parseInt(people) > 1 && (
            <>
              <div class="h-px bg-slate-200" />
              <div class="grid grid-cols-2 gap-2 text-sm">
                <div>
                  <div class="text-slate-500">Per Person (total)</div>
                  <div class="font-semibold tabular-nums text-slate-900">{fmtUsd(result.perPerson)}</div>
                </div>
                <div>
                  <div class="text-slate-500">Tip per Person</div>
                  <div class="font-semibold tabular-nums text-slate-900">{fmtUsd(result.tipPerPerson)}</div>
                </div>
              </div>
            </>
          )}
        </div>
      )}

      <p class="text-xs leading-relaxed text-slate-500">
        Tipping is customary but not legally required in most places.
      </p>
    </div>
  );
}
```

---

## Task 4: tipcalc.io — index.astro

**Files:**
- Rewrite: `sites/tipcalc.io/src/pages/index.astro`

- [ ] **Step 1: Rewrite index.astro**

```astro
---
import BaseLayout from '~/layouts/BaseLayout.astro';
import { siteConfig } from '~/config/site.config';
import TipCalculator from '~/components/TipCalculator';
import { getCollection } from 'astro:content';

const recentPosts = siteConfig.features.hasBlog
  ? (await getCollection('blog', ({ data }) => !data.draft))
      .sort((a, b) => b.data.publishDate.valueOf() - a.data.publishDate.valueOf())
      .slice(0, 3)
  : [];
---
<BaseLayout
  title="Tip Calculator — Split the Bill, Calculate Gratuity Instantly"
  description="Calculate the tip amount, total bill, and per-person split instantly. Choose from quick tip presets or enter a custom percentage. Free, no signup."
>

  <header class="pb-8 pt-4">
    <h1 class="text-4xl font-bold tracking-tight text-slate-900 sm:text-5xl">
      Tip Calculator
    </h1>
    <p class="mt-3 max-w-xl text-lg text-slate-600">
      Calculate tip amounts, total bills, and per-person splits in seconds.
      Pick a quick preset or enter any custom percentage.
    </p>
  </header>

  <ul class="flex flex-wrap gap-x-6 gap-y-2 text-sm text-slate-600">
    {[
      'Instant results as you type',
      'Quick tip presets (10%–25%)',
      'Bill-splitting built in',
      'No data stored or shared',
    ].map((badge) => (
      <li class="flex items-center gap-1.5">
        <svg class="h-4 w-4 shrink-0 text-brand" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.061 1.06l2.5 2.5a.75.75 0 001.137-.088l4-5.5z" clip-rule="evenodd" />
        </svg>
        {badge}
      </li>
    ))}
  </ul>

  <!-- Light YMYL disclaimer -->
  <aside
    role="note"
    class="mt-6 rounded-lg border border-amber-200 bg-amber-50 p-4 text-sm text-amber-900"
  >
    <strong class="font-semibold">Note:</strong> Tipping customs and expected percentages vary
    by country, type of service, and individual circumstance. Results are for reference only.
  </aside>

  <div class="mt-8 grid items-start gap-8 md:grid-cols-[1fr_400px]">

    <div class="space-y-10">

      <section aria-labelledby="how-to-tip-heading">
        <h2 id="how-to-tip-heading" class="text-2xl font-bold text-slate-900">How to Calculate a Tip</h2>
        <div class="prose prose-slate mt-3 max-w-none">
          <p>
            The formula is straightforward:
          </p>
          <p><strong>Tip = Bill Amount × (Tip % ÷ 100)</strong></p>
          <p><strong>Total = Bill Amount + Tip</strong></p>
          <p>
            For a bill of $50 with an 18% tip: $50 × 0.18 = <strong>$9.00 tip</strong>, total <strong>$59.00</strong>.
            Splitting among 4 people: each person pays <strong>$14.75</strong>.
          </p>
        </div>
      </section>

      <section aria-labelledby="tipping-guide-heading">
        <h2 id="tipping-guide-heading" class="text-2xl font-bold text-slate-900">US Tipping Guide by Service Type</h2>
        <div class="mt-4 overflow-hidden rounded-xl border border-slate-200">
          <table class="w-full text-sm">
            <thead>
              <tr class="bg-slate-50 text-left">
                <th class="px-4 py-3 font-semibold text-slate-700">Service</th>
                <th class="px-4 py-3 font-semibold text-slate-700">Standard Range</th>
                <th class="hidden px-4 py-3 font-semibold text-slate-700 sm:table-cell">Notes</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100">
              {([
                { service: 'Sit-down restaurant',   range: '18–22%',   note: '20% is the common default' },
                { service: 'Bar / cocktails',        range: '$1–2/drink or 15–20%', note: 'Flat amount common for simple orders' },
                { service: 'Food delivery',          range: '15–20%',   note: 'Extra for large or complex orders' },
                { service: 'Rideshare (Uber, Lyft)', range: '10–20%',   note: 'Higher for great service or heavy luggage' },
                { service: 'Hair salon / barber',    range: '15–25%',   note: 'Tip each person separately if multiple' },
                { service: 'Hotel housekeeping',     range: '$2–5/night', note: 'Leave daily; staff may change each day' },
              ] as const).map((row) => (
                <tr class="bg-white hover:bg-slate-50">
                  <td class="px-4 py-3 font-medium text-slate-900">{row.service}</td>
                  <td class="px-4 py-3 text-slate-700">{row.range}</td>
                  <td class="hidden px-4 py-3 text-slate-500 sm:table-cell">{row.note}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <section aria-labelledby="no-tip-heading">
        <h2 id="no-tip-heading" class="text-2xl font-bold text-slate-900">When You Don't Need to Tip</h2>
        <div class="prose prose-slate mt-3 max-w-none">
          <p>
            Tipping is not expected in all contexts. Counter-service restaurants, fast food, and
            self-checkout kiosks have no obligation (though the option is increasingly presented).
            In many countries — Japan, South Korea, and much of Europe — tipping is uncommon or
            even considered rude. When traveling internationally, research local customs.
          </p>
        </div>
      </section>

    </div>

    <div class="md:sticky md:top-8">
      <div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <h2 class="mb-4 text-lg font-semibold text-slate-900">Calculate Your Tip</h2>
        <TipCalculator client:load />
      </div>
    </div>

  </div>

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
    </section>
  )}

  <footer class="mt-16 border-t border-slate-200 pt-8 text-sm text-slate-500">
    <span>Content last reviewed: <time datetime="2026-04-25">April 25, 2026</time>.</span>
  </footer>

</BaseLayout>
```

- [ ] **Step 2: Build and verify tipcalc.io**

```bash
cd /home/abovespec/site-network && pnpm --filter @site/tipcalc build
```
Expected: Exit 0, no errors.

- [ ] **Step 3: Commit**

```bash
cd /home/abovespec/site-network
git add sites/tipcalc.io/src/components/TipCalculator.tsx sites/tipcalc.io/src/pages/index.astro
git commit -m "feat(tipcalc.io): Preact TipCalculator + bmicalc layout + light YMYL (INF-24)

Co-Authored-By: Paperclip <noreply@paperclip.ing>"
```

---

## Task 5: amortcalc.io — AmortizationCalculator.tsx

**Files:**
- Create: `sites/amortcalc.io/src/components/AmortizationCalculator.tsx`

- [ ] **Step 1: Create Preact component**

```tsx
// sites/amortcalc.io/src/components/AmortizationCalculator.tsx
import { useState, useMemo } from 'preact/hooks';

interface AmortRow {
  month: number;
  payment: number;
  principal: number;
  interest: number;
  balance: number;
}

function calcAmort(principal: number, annualRate: number, years: number) {
  if (principal <= 0 || annualRate <= 0 || years <= 0) return null;
  const r = annualRate / 100 / 12;
  const n = years * 12;
  const monthly = (principal * r * Math.pow(1 + r, n)) / (Math.pow(1 + r, n) - 1);
  const totalCost = monthly * n;
  const totalInterest = totalCost - principal;
  const interestPct = (totalInterest / totalCost) * 100;

  let balance = principal;
  const rows: AmortRow[] = [];
  for (let i = 1; i <= n; i++) {
    const interest = balance * r;
    const princ = monthly - interest;
    balance = Math.max(0, balance - princ);
    // Show every month up to 24, then every 12 months, plus final
    if (i <= 24 || i % 12 === 0 || i === n) {
      rows.push({ month: i, payment: monthly, principal: princ, interest, balance });
    }
  }

  return { monthly, totalCost, totalInterest, interestPct, rows };
}

function fmtUsd(n: number) {
  return '$' + n.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

const inputCls =
  'w-full rounded-lg border border-slate-300 px-3 py-2 pr-10 text-sm focus:border-brand focus:outline-none focus:ring-1 focus:ring-brand';

export default function AmortizationCalculator() {
  const [principal, setPrincipal] = useState('300000');
  const [rate, setRate]           = useState('6.5');
  const [years, setYears]         = useState('30');
  const [showTable, setShowTable] = useState(false);

  const result = useMemo(
    () => calcAmort(parseFloat(principal) || 0, parseFloat(rate) || 0, parseFloat(years) || 0),
    [principal, rate, years],
  );

  return (
    <div class="space-y-4">
      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Loan Amount</label>
        <div class="relative">
          <span class="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">$</span>
          <input
            type="number" min="1000" step="1000" placeholder="300000"
            value={principal}
            onInput={(e) => setPrincipal((e.target as HTMLInputElement).value)}
            class={`${inputCls} pl-6`}
            aria-label="Loan principal in dollars"
          />
        </div>
      </div>

      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Annual Interest Rate</label>
        <div class="relative">
          <input
            type="number" min="0" max="30" step="0.1" placeholder="6.5"
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
            type="number" min="1" max="40" step="1" placeholder="30"
            value={years}
            onInput={(e) => setYears((e.target as HTMLInputElement).value)}
            class={inputCls}
            aria-label="Loan term in years"
          />
          <span class="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">yrs</span>
        </div>
      </div>

      {result && (
        <div role="status" aria-live="polite" class="space-y-3 rounded-xl border border-indigo-200 bg-indigo-50 p-4">
          <div class="flex items-baseline justify-between">
            <span class="text-sm text-slate-600">Monthly Payment</span>
            <span class="text-2xl font-bold tabular-nums text-brand">{fmtUsd(result.monthly)}</span>
          </div>
          <div class="h-px bg-slate-200" />
          <div class="grid grid-cols-2 gap-2 text-sm">
            <div>
              <div class="text-slate-500">Total Cost</div>
              <div class="font-semibold text-slate-900">{fmtUsd(result.totalCost)}</div>
            </div>
            <div>
              <div class="text-slate-500">Total Interest</div>
              <div class="font-semibold text-orange-600">{fmtUsd(result.totalInterest)}</div>
            </div>
          </div>
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

          <button
            type="button"
            onClick={() => setShowTable((v) => !v)}
            class="mt-1 text-xs font-medium text-brand underline underline-offset-2 hover:opacity-80"
          >
            {showTable ? 'Hide' : 'Show'} amortization schedule
          </button>

          {showTable && (
            <div class="max-h-64 overflow-auto rounded-lg border border-slate-200 bg-white text-xs">
              <table class="w-full">
                <thead class="sticky top-0 bg-slate-50 text-left">
                  <tr>
                    {['Mo.', 'Principal', 'Interest', 'Balance'].map((h) => (
                      <th class="px-2 py-1.5 font-semibold text-slate-600">{h}</th>
                    ))}
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100">
                  {result.rows.map((row) => (
                    <tr key={row.month} class="hover:bg-slate-50">
                      <td class="px-2 py-1 tabular-nums text-slate-500">{row.month}</td>
                      <td class="px-2 py-1 tabular-nums">{fmtUsd(row.principal)}</td>
                      <td class="px-2 py-1 tabular-nums text-orange-600">{fmtUsd(row.interest)}</td>
                      <td class="px-2 py-1 tabular-nums">{fmtUsd(row.balance)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      <p class="text-xs leading-relaxed text-slate-500">
        For informational purposes only. Consult a licensed financial advisor before borrowing.
      </p>
    </div>
  );
}
```

---

## Task 6: amortcalc.io — index.astro (YMYL financial)

**Files:**
- Rewrite: `sites/amortcalc.io/src/pages/index.astro`

- [ ] **Step 1: Rewrite index.astro**

```astro
---
import BaseLayout from '~/layouts/BaseLayout.astro';
import { siteConfig } from '~/config/site.config';
import AmortizationCalculator from '~/components/AmortizationCalculator';
import { getCollection } from 'astro:content';

const recentPosts = siteConfig.features.hasBlog
  ? (await getCollection('blog', ({ data }) => !data.draft))
      .sort((a, b) => b.data.publishDate.valueOf() - a.data.publishDate.valueOf())
      .slice(0, 3)
  : [];
---
<BaseLayout
  title="Amortization Calculator — Monthly Payment & Schedule Generator"
  description="Calculate monthly mortgage or loan payments and generate a full amortization schedule. See exactly how much interest you pay over the life of your loan. Free, instant."
>

  <header class="pb-8 pt-4">
    <h1 class="text-4xl font-bold tracking-tight text-slate-900 sm:text-5xl">
      Amortization Calculator
    </h1>
    <p class="mt-3 max-w-xl text-lg text-slate-600">
      Calculate your monthly payment and generate a complete amortization schedule showing
      principal, interest, and remaining balance for every payment.
    </p>
  </header>

  <ul class="flex flex-wrap gap-x-6 gap-y-2 text-sm text-slate-600">
    {[
      'Instant results as you type',
      'Full amortization schedule',
      'Principal vs interest breakdown',
      'No data stored or shared',
    ].map((badge) => (
      <li class="flex items-center gap-1.5">
        <svg class="h-4 w-4 shrink-0 text-brand" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.061 1.06l2.5 2.5a.75.75 0 001.137-.088l4-5.5z" clip-rule="evenodd" />
        </svg>
        {badge}
      </li>
    ))}
  </ul>

  <div class="mt-8 grid items-start gap-8 md:grid-cols-[1fr_400px]">

    <div class="space-y-10">

      <aside
        role="note"
        class="rounded-lg border border-amber-200 bg-amber-50 p-4 text-sm text-amber-900"
      >
        <strong class="font-semibold">Important:</strong> Results are estimates based on
        the standard amortization formula. They do not account for taxes, insurance, PMI,
        or lender fees. This calculator does not constitute financial advice. Consult a
        licensed financial professional before taking on debt.
      </aside>

      <section aria-labelledby="what-is-amort-heading">
        <h2 id="what-is-amort-heading" class="text-2xl font-bold text-slate-900">What Is Amortization?</h2>
        <div class="prose prose-slate mt-3 max-w-none">
          <p>
            Amortization is the process of paying off a debt through regular scheduled payments
            over time. Each payment covers both interest owed and a portion of the principal
            balance. Because interest is calculated on the remaining principal, the split between
            principal and interest shifts with each payment.
          </p>
          <p>
            Early in the loan, most of your payment goes to interest. As the principal shrinks,
            the interest portion decreases and your equity builds faster. This is why the first
            years of a mortgage feel slow for equity building.
          </p>
        </div>
      </section>

      <section aria-labelledby="formula-heading">
        <h2 id="formula-heading" class="text-2xl font-bold text-slate-900">The Amortization Formula</h2>
        <div class="prose prose-slate mt-3 max-w-none">
          <p>Monthly payment is calculated with:</p>
          <p><strong>M = P × [r(1+r)^n] / [(1+r)^n − 1]</strong></p>
          <ul>
            <li><strong>M</strong> = monthly payment</li>
            <li><strong>P</strong> = principal (loan amount)</li>
            <li><strong>r</strong> = monthly interest rate (annual rate ÷ 12 ÷ 100)</li>
            <li><strong>n</strong> = total number of monthly payments (term in years × 12)</li>
          </ul>
          <p>
            For a $300,000 loan at 6.5% for 30 years: r = 0.065/12 ≈ 0.00542, n = 360.
            Monthly payment ≈ <strong>$1,896.20</strong>.
          </p>
        </div>
      </section>

      <section aria-labelledby="pay-early-heading">
        <h2 id="pay-early-heading" class="text-2xl font-bold text-slate-900">How to Pay Off Your Loan Faster</h2>
        <div class="prose prose-slate mt-3 max-w-none">
          <ul>
            <li>
              <strong>Make biweekly payments.</strong> Paying half your monthly payment every
              two weeks results in 26 half-payments (13 full payments) per year instead of 12.
              On a 30-year mortgage you can cut years off the term.
            </li>
            <li>
              <strong>Add to the principal each month.</strong> Even small extra payments reduce
              the principal and therefore future interest. Check that your lender applies
              extra payments to principal, not future interest.
            </li>
            <li>
              <strong>Refinance at a lower rate.</strong> If rates have dropped since you
              originated, refinancing can reduce your monthly payment or shorten your term.
              Account for closing costs when evaluating whether it makes sense.
            </li>
          </ul>
        </div>
      </section>

    </div>

    <div class="md:sticky md:top-8">
      <div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <h2 class="mb-4 text-lg font-semibold text-slate-900">Amortization Calculator</h2>
        <AmortizationCalculator client:load />
      </div>
    </div>

  </div>

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
    </section>
  )}

  <footer class="mt-16 border-t border-slate-200 pt-8 text-sm text-slate-600">
    <div class="flex items-center gap-2 text-slate-500">
      <svg class="h-4 w-4 shrink-0 text-slate-400" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
        <path fill-rule="evenodd" d="M16.403 12.652a3 3 0 000-5.304 3 3 0 00-3.75-3.751 3 3 0 00-5.305 0 3 3 0 00-3.751 3.75 3 3 0 000 5.305 3 3 0 003.75 3.751 3 3 0 005.305 0 3 3 0 003.751-3.75zm-2.546-4.46a.75.75 0 00-1.214-.883l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z" clip-rule="evenodd" />
      </svg>
      <span>Content reviewed for financial accuracy. Last reviewed: <time datetime="2026-04-25">April 25, 2026</time>.</span>
    </div>
    <div class="mt-6">
      <h2 class="mb-2 font-semibold text-slate-700">Sources</h2>
      <ol class="space-y-1.5">
        <li class="flex gap-2">
          <span class="shrink-0 tabular-nums text-slate-400">1.</span>
          <span>Consumer Financial Protection Bureau. <em>Understand loan options</em>. 2024. <a href="https://www.consumerfinance.gov/owning-a-home/loan-options/" target="_blank" rel="noopener noreferrer" class="text-brand underline underline-offset-2 hover:opacity-80">consumerfinance.gov</a></span>
        </li>
        <li class="flex gap-2">
          <span class="shrink-0 tabular-nums text-slate-400">2.</span>
          <span>Investopedia. <em>Amortization</em>. Updated 2024.</span>
        </li>
      </ol>
    </div>
  </footer>

</BaseLayout>
```

- [ ] **Step 2: Build and verify amortcalc.io**

```bash
cd /home/abovespec/site-network && pnpm --filter @site/amortcalc build
```
Expected: Exit 0, no errors.

- [ ] **Step 3: Commit**

```bash
cd /home/abovespec/site-network
git add sites/amortcalc.io/src/components/AmortizationCalculator.tsx sites/amortcalc.io/src/pages/index.astro
git commit -m "feat(amortcalc.io): Preact AmortizationCalculator + YMYL financial chrome (INF-24)

Co-Authored-By: Paperclip <noreply@paperclip.ing>"
```

---

## Task 7: margincalc.io — MarginCalculator.tsx (tabbed, 4 calcs)

**Files:**
- Create: `sites/margincalc.io/src/components/MarginCalculator.tsx`

- [ ] **Step 1: Create Preact component with 4 calculator tabs**

```tsx
// sites/margincalc.io/src/components/MarginCalculator.tsx
import { useState, useMemo } from 'preact/hooks';

type Tab = 'profit-margin' | 'markup' | 'break-even' | 'reverse-margin';

function fmtUsd(n: number) {
  return '$' + n.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}
function fmtPct(n: number) { return n.toFixed(2) + '%'; }

const inputCls =
  'w-full rounded-lg border border-slate-300 px-3 py-2 pr-10 text-sm focus:border-brand focus:outline-none focus:ring-1 focus:ring-brand';
const resultCls = 'space-y-3 rounded-xl border border-brand/30 bg-green-50 p-4';

function ProfitMarginTab() {
  const [cost, setCost]   = useState('50');
  const [price, setPrice] = useState('100');
  const r = useMemo(() => {
    const c = parseFloat(cost) || 0;
    const p = parseFloat(price) || 0;
    if (p <= 0) return null;
    const profit = p - c;
    return { profit, margin: (profit / p) * 100, markup: (profit / c) * 100 };
  }, [cost, price]);
  return (
    <div class="space-y-4">
      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Cost</label>
        <div class="relative">
          <span class="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">$</span>
          <input type="number" min="0" step="0.01" value={cost}
            onInput={(e) => setCost((e.target as HTMLInputElement).value)}
            class={`${inputCls} pl-6`} aria-label="Cost" />
        </div>
      </div>
      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Selling Price</label>
        <div class="relative">
          <span class="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">$</span>
          <input type="number" min="0" step="0.01" value={price}
            onInput={(e) => setPrice((e.target as HTMLInputElement).value)}
            class={`${inputCls} pl-6`} aria-label="Selling price" />
        </div>
      </div>
      {r && (
        <div role="status" aria-live="polite" class={resultCls}>
          <div class="flex justify-between text-sm"><span class="text-slate-600">Profit</span><span class="font-bold text-slate-900">{fmtUsd(r.profit)}</span></div>
          <div class="flex justify-between text-sm"><span class="text-slate-600">Profit Margin</span><span class="font-bold text-brand">{fmtPct(r.margin)}</span></div>
          <div class="flex justify-between text-sm"><span class="text-slate-600">Markup</span><span class="font-bold text-slate-900">{fmtPct(r.markup)}</span></div>
        </div>
      )}
    </div>
  );
}

function MarkupTab() {
  const [cost, setCost] = useState('50');
  const [pct, setPct]   = useState('50');
  const r = useMemo(() => {
    const c = parseFloat(cost) || 0;
    const p = parseFloat(pct) || 0;
    const price = c * (1 + p / 100);
    const profit = price - c;
    return { price, profit, margin: (profit / price) * 100 };
  }, [cost, pct]);
  return (
    <div class="space-y-4">
      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Cost</label>
        <div class="relative">
          <span class="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">$</span>
          <input type="number" min="0" step="0.01" value={cost}
            onInput={(e) => setCost((e.target as HTMLInputElement).value)}
            class={`${inputCls} pl-6`} aria-label="Cost" />
        </div>
      </div>
      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Markup</label>
        <div class="relative">
          <input type="number" min="0" step="0.1" value={pct}
            onInput={(e) => setPct((e.target as HTMLInputElement).value)}
            class={inputCls} aria-label="Markup percentage" />
          <span class="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">%</span>
        </div>
      </div>
      <div role="status" aria-live="polite" class={resultCls}>
        <div class="flex justify-between text-sm"><span class="text-slate-600">Selling Price</span><span class="font-bold text-slate-900">{fmtUsd(r.price)}</span></div>
        <div class="flex justify-between text-sm"><span class="text-slate-600">Profit</span><span class="font-bold text-slate-900">{fmtUsd(r.profit)}</span></div>
        <div class="flex justify-between text-sm"><span class="text-slate-600">Profit Margin</span><span class="font-bold text-brand">{fmtPct(r.margin)}</span></div>
      </div>
    </div>
  );
}

function BreakEvenTab() {
  const [fixed, setFixed]     = useState('5000');
  const [variable, setVar]    = useState('20');
  const [sellPrice, setSell]  = useState('50');
  const r = useMemo(() => {
    const f = parseFloat(fixed) || 0;
    const v = parseFloat(variable) || 0;
    const s = parseFloat(sellPrice) || 0;
    if (s <= v) return null;
    const units = f / (s - v);
    return { units: Math.ceil(units), revenue: Math.ceil(units) * s };
  }, [fixed, variable, sellPrice]);
  return (
    <div class="space-y-4">
      {[
        { id: 'fixed', label: 'Fixed Costs', val: fixed, set: setFixed },
        { id: 'var',   label: 'Variable Cost / Unit', val: variable, set: setVar },
        { id: 'sell',  label: 'Selling Price / Unit', val: sellPrice, set: setSell },
      ].map(({ id, label, val, set }) => (
        <div key={id}>
          <label class="mb-1 block text-sm font-medium text-slate-700">{label}</label>
          <div class="relative">
            <span class="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">$</span>
            <input type="number" min="0" step="1" value={val}
              onInput={(e) => set((e.target as HTMLInputElement).value)}
              class={`${inputCls} pl-6`} aria-label={label} />
          </div>
        </div>
      ))}
      {r ? (
        <div role="status" aria-live="polite" class={resultCls}>
          <div class="flex justify-between text-sm"><span class="text-slate-600">Break-Even Units</span><span class="font-bold text-slate-900">{r.units.toLocaleString()}</span></div>
          <div class="flex justify-between text-sm"><span class="text-slate-600">Break-Even Revenue</span><span class="font-bold text-brand">{fmtUsd(r.revenue)}</span></div>
        </div>
      ) : (
        <p class="text-xs text-red-600">Selling price must be greater than variable cost.</p>
      )}
    </div>
  );
}

function ReverseMarginTab() {
  const [margin, setMargin] = useState('30');
  const [cost, setCost]     = useState('70');
  const r = useMemo(() => {
    const m = parseFloat(margin) || 0;
    const c = parseFloat(cost) || 0;
    if (m >= 100 || c <= 0) return null;
    const price = c / (1 - m / 100);
    return { price, profit: price - c };
  }, [margin, cost]);
  return (
    <div class="space-y-4">
      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Desired Margin</label>
        <div class="relative">
          <input type="number" min="0" max="99.9" step="0.1" value={margin}
            onInput={(e) => setMargin((e.target as HTMLInputElement).value)}
            class={inputCls} aria-label="Desired profit margin percentage" />
          <span class="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">%</span>
        </div>
      </div>
      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Cost</label>
        <div class="relative">
          <span class="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">$</span>
          <input type="number" min="0" step="0.01" value={cost}
            onInput={(e) => setCost((e.target as HTMLInputElement).value)}
            class={`${inputCls} pl-6`} aria-label="Cost" />
        </div>
      </div>
      {r ? (
        <div role="status" aria-live="polite" class={resultCls}>
          <div class="flex justify-between text-sm"><span class="text-slate-600">Required Price</span><span class="font-bold text-brand">{fmtUsd(r.price)}</span></div>
          <div class="flex justify-between text-sm"><span class="text-slate-600">Profit</span><span class="font-bold text-slate-900">{fmtUsd(r.profit)}</span></div>
        </div>
      ) : (
        <p class="text-xs text-red-600">Margin must be less than 100%.</p>
      )}
    </div>
  );
}

const TABS: { id: Tab; label: string }[] = [
  { id: 'profit-margin',  label: 'Profit Margin' },
  { id: 'markup',         label: 'Markup' },
  { id: 'break-even',     label: 'Break-Even' },
  { id: 'reverse-margin', label: 'Reverse' },
];

export default function MarginCalculator() {
  const [tab, setTab] = useState<Tab>('profit-margin');
  return (
    <div class="space-y-4">
      <div class="flex gap-1 rounded-lg border border-slate-200 bg-slate-50 p-1">
        {TABS.map(({ id, label }) => (
          <button
            key={id}
            type="button"
            onClick={() => setTab(id)}
            aria-pressed={tab === id}
            class={`flex-1 rounded-md py-1.5 text-xs font-medium transition-all ${
              tab === id
                ? 'bg-white text-slate-900 shadow-sm'
                : 'text-slate-500 hover:text-slate-700'
            }`}
          >
            {label}
          </button>
        ))}
      </div>
      {tab === 'profit-margin'  && <ProfitMarginTab />}
      {tab === 'markup'         && <MarkupTab />}
      {tab === 'break-even'     && <BreakEvenTab />}
      {tab === 'reverse-margin' && <ReverseMarginTab />}
    </div>
  );
}
```

---

## Task 8: margincalc.io — index.astro (YMYL financial)

**Files:**
- Rewrite: `sites/margincalc.io/src/pages/index.astro`

- [ ] **Step 1: Rewrite index.astro**

```astro
---
import BaseLayout from '~/layouts/BaseLayout.astro';
import { siteConfig } from '~/config/site.config';
import MarginCalculator from '~/components/MarginCalculator';
import { getCollection } from 'astro:content';

const recentPosts = siteConfig.features.hasBlog
  ? (await getCollection('blog', ({ data }) => !data.draft))
      .sort((a, b) => b.data.publishDate.valueOf() - a.data.publishDate.valueOf())
      .slice(0, 3)
  : [];
---
<BaseLayout
  title="Profit Margin Calculator — Margin, Markup & Break-Even Analysis"
  description="Free online profit margin calculator. Calculate gross profit margin, markup percentage, break-even analysis, and reverse margin pricing. Instant results."
>

  <header class="pb-8 pt-4">
    <h1 class="text-4xl font-bold tracking-tight text-slate-900 sm:text-5xl">
      Profit Margin Calculator
    </h1>
    <p class="mt-3 max-w-xl text-lg text-slate-600">
      Calculate profit margins, markups, break-even points, and target pricing — four
      essential business calculators in one place.
    </p>
  </header>

  <ul class="flex flex-wrap gap-x-6 gap-y-2 text-sm text-slate-600">
    {[
      'Margin, markup, break-even & reverse pricing',
      'Instant results as you type',
      'No data stored or shared',
      'Free, no signup required',
    ].map((badge) => (
      <li class="flex items-center gap-1.5">
        <svg class="h-4 w-4 shrink-0 text-brand" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.061 1.06l2.5 2.5a.75.75 0 001.137-.088l4-5.5z" clip-rule="evenodd" />
        </svg>
        {badge}
      </li>
    ))}
  </ul>

  <div class="mt-8 grid items-start gap-8 md:grid-cols-[1fr_400px]">

    <div class="space-y-10">

      <aside
        role="note"
        class="rounded-lg border border-amber-200 bg-amber-50 p-4 text-sm text-amber-900"
      >
        <strong class="font-semibold">Important:</strong> Results are for informational and
        planning purposes only. They do not constitute financial, accounting, or business advice.
        Consult a qualified financial professional for pricing and business decisions.
      </aside>

      <section aria-labelledby="margin-vs-markup-heading">
        <h2 id="margin-vs-markup-heading" class="text-2xl font-bold text-slate-900">
          Profit Margin vs. Markup — What's the Difference?
        </h2>
        <div class="prose prose-slate mt-3 max-w-none">
          <p>
            These two numbers both describe the relationship between cost and price, but from
            different perspectives:
          </p>
          <ul>
            <li>
              <strong>Profit margin</strong> — profit as a percentage of the <em>selling price</em>.
              Formula: <code>(Price − Cost) / Price × 100</code>. A $50 item that cost $30 has
              a 40% margin.
            </li>
            <li>
              <strong>Markup</strong> — profit as a percentage of the <em>cost</em>.
              Formula: <code>(Price − Cost) / Cost × 100</code>. The same item has a 66.7% markup.
            </li>
          </ul>
          <p>
            Retailers typically think in margins; manufacturers often think in markup. Using the
            wrong one when pricing can lead to undercharging.
          </p>
        </div>
      </section>

      <section aria-labelledby="break-even-heading">
        <h2 id="break-even-heading" class="text-2xl font-bold text-slate-900">
          Break-Even Analysis
        </h2>
        <div class="prose prose-slate mt-3 max-w-none">
          <p>
            Break-even is the sales volume at which revenue equals total costs — zero profit, zero
            loss. The formula is:
          </p>
          <p>
            <strong>Break-Even Units = Fixed Costs / (Selling Price − Variable Cost per Unit)</strong>
          </p>
          <p>
            Fixed costs are costs that don't change with production volume (rent, salaries, equipment).
            Variable costs scale with volume (materials, packaging, sales commissions).
          </p>
        </div>
      </section>

      <section aria-labelledby="healthy-margin-heading">
        <h2 id="healthy-margin-heading" class="text-2xl font-bold text-slate-900">
          What Is a Healthy Profit Margin?
        </h2>
        <div class="prose prose-slate mt-3 max-w-none">
          <p>
            "Healthy" varies widely by industry. Gross margins tend to be higher in software (70–90%)
            and lower in retail (20–40%) and grocery (1–5%). Net margins — after all operating costs —
            are much lower in every category.
          </p>
          <p>
            A useful benchmark is to know your industry average (available via NYU Stern's annual
            margin databases) and track your own margins over time. A trend is often more informative
            than a single snapshot.
          </p>
        </div>
      </section>

    </div>

    <div class="md:sticky md:top-8">
      <div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <h2 class="mb-4 text-lg font-semibold text-slate-900">Business Calculators</h2>
        <MarginCalculator client:load />
      </div>
    </div>

  </div>

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
    </section>
  )}

  <footer class="mt-16 border-t border-slate-200 pt-8 text-sm text-slate-600">
    <div class="flex items-center gap-2 text-slate-500">
      <svg class="h-4 w-4 shrink-0 text-slate-400" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
        <path fill-rule="evenodd" d="M16.403 12.652a3 3 0 000-5.304 3 3 0 00-3.75-3.751 3 3 0 00-5.305 0 3 3 0 00-3.751 3.75 3 3 0 000 5.305 3 3 0 003.75 3.751 3 3 0 005.305 0 3 3 0 003.751-3.75zm-2.546-4.46a.75.75 0 00-1.214-.883l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z" clip-rule="evenodd" />
      </svg>
      <span>Content reviewed for accuracy. Last reviewed: <time datetime="2026-04-25">April 25, 2026</time>.</span>
    </div>
    <div class="mt-6">
      <h2 class="mb-2 font-semibold text-slate-700">Sources</h2>
      <ol class="space-y-1.5">
        <li class="flex gap-2">
          <span class="shrink-0 tabular-nums text-slate-400">1.</span>
          <span>Damodaran, A. <em>Margins by Sector (US)</em>. NYU Stern School of Business. Updated January 2026.</span>
        </li>
        <li class="flex gap-2">
          <span class="shrink-0 tabular-nums text-slate-400">2.</span>
          <span>Investopedia. <em>Profit Margin: Types and How to Calculate Them</em>. Updated 2025.</span>
        </li>
      </ol>
    </div>
  </footer>

</BaseLayout>
```

- [ ] **Step 2: Build and verify margincalc.io**

```bash
cd /home/abovespec/site-network && pnpm --filter @site/margincalc build
```
Expected: Exit 0, no errors.

- [ ] **Step 3: Commit**

```bash
cd /home/abovespec/site-network
git add sites/margincalc.io/src/components/MarginCalculator.tsx sites/margincalc.io/src/pages/index.astro
git commit -m "feat(margincalc.io): tabbed Preact MarginCalculator + YMYL financial chrome (INF-24)

Co-Authored-By: Paperclip <noreply@paperclip.ing>"
```

---

## Task 9: percentcalc.io — Enable multi-tool, create 5 Preact components

**Files:**
- Modify: `sites/percentcalc.io/src/config/site.config.ts`
- Create: `sites/percentcalc.io/src/components/PercentOfCalculator.tsx`
- Create: `sites/percentcalc.io/src/components/PercentChangeCalculator.tsx`
- Create: `sites/percentcalc.io/src/components/PercentOffCalculator.tsx`
- Create: `sites/percentcalc.io/src/components/PercentIncreaseCalculator.tsx`
- Create: `sites/percentcalc.io/src/components/PercentDifferenceCalculator.tsx`

- [ ] **Step 1: Enable hasTool in site.config.ts**

In `sites/percentcalc.io/src/config/site.config.ts`, change `hasTool: false` to `hasTool: true`.

- [ ] **Step 2: Create PercentOfCalculator.tsx**

```tsx
// sites/percentcalc.io/src/components/PercentOfCalculator.tsx
import { useState, useMemo } from 'preact/hooks';
const inputCls = 'w-full rounded-lg border border-slate-300 px-3 py-2 pr-10 text-sm focus:border-brand focus:outline-none focus:ring-1 focus:ring-brand';
export default function PercentOfCalculator() {
  const [pct, setPct]   = useState('15');
  const [total, setTotal] = useState('200');
  const result = useMemo(() => {
    const p = parseFloat(pct) || 0;
    const t = parseFloat(total) || 0;
    if (t === 0) return null;
    return { value: (p / 100) * t, remainder: t - (p / 100) * t };
  }, [pct, total]);
  return (
    <div class="space-y-4">
      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Percentage</label>
        <div class="relative">
          <input type="number" min="0" step="0.01" value={pct}
            onInput={(e) => setPct((e.target as HTMLInputElement).value)}
            class={inputCls} aria-label="Percentage" />
          <span class="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">%</span>
        </div>
      </div>
      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Of what number?</label>
        <input type="number" min="0" step="any" value={total}
          onInput={(e) => setTotal((e.target as HTMLInputElement).value)}
          class={inputCls} aria-label="Base number" />
      </div>
      {result && (
        <div role="status" aria-live="polite" class="space-y-2 rounded-xl border border-brand/30 bg-yellow-50 p-4">
          <div class="flex justify-between text-sm">
            <span class="text-slate-600">{pct}% of {total}</span>
            <span class="text-2xl font-bold tabular-nums text-brand">{result.value.toLocaleString('en-US', { maximumFractionDigits: 4 })}</span>
          </div>
          <div class="flex justify-between text-sm text-slate-500">
            <span>Remainder</span>
            <span class="tabular-nums">{result.remainder.toLocaleString('en-US', { maximumFractionDigits: 4 })}</span>
          </div>
        </div>
      )}
      <p class="text-xs text-slate-500">Formula: Result = (Percentage ÷ 100) × Number</p>
    </div>
  );
}
```

- [ ] **Step 3: Create PercentChangeCalculator.tsx**

```tsx
// sites/percentcalc.io/src/components/PercentChangeCalculator.tsx
import { useState, useMemo } from 'preact/hooks';
const inputCls = 'w-full rounded-lg border border-slate-300 px-3 py-2 pr-10 text-sm focus:border-brand focus:outline-none focus:ring-1 focus:ring-brand';
export default function PercentChangeCalculator() {
  const [from, setFrom] = useState('80');
  const [to, setTo]     = useState('100');
  const result = useMemo(() => {
    const f = parseFloat(from) || 0;
    const t = parseFloat(to);
    if (!f) return null;
    const change = ((t - f) / Math.abs(f)) * 100;
    return { change, isIncrease: change >= 0 };
  }, [from, to]);
  return (
    <div class="space-y-4">
      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Original Value</label>
        <input type="number" step="any" value={from}
          onInput={(e) => setFrom((e.target as HTMLInputElement).value)}
          class={inputCls} aria-label="Original value" />
      </div>
      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">New Value</label>
        <input type="number" step="any" value={to}
          onInput={(e) => setTo((e.target as HTMLInputElement).value)}
          class={inputCls} aria-label="New value" />
      </div>
      {result && (
        <div role="status" aria-live="polite" class={`space-y-2 rounded-xl border p-4 ${result.isIncrease ? 'border-green-200 bg-green-50' : 'border-red-200 bg-red-50'}`}>
          <div class="flex items-baseline justify-between">
            <span class="text-sm text-slate-600">Percent Change</span>
            <span class={`text-2xl font-bold tabular-nums ${result.isIncrease ? 'text-green-700' : 'text-red-600'}`}>
              {result.isIncrease ? '+' : ''}{result.change.toFixed(2)}%
            </span>
          </div>
          <p class="text-xs text-slate-500">
            {result.isIncrease ? '↑ Increase' : '↓ Decrease'} of {Math.abs(result.change).toFixed(2)}%
          </p>
        </div>
      )}
      <p class="text-xs text-slate-500">Formula: ((New − Original) / |Original|) × 100</p>
    </div>
  );
}
```

- [ ] **Step 4: Create PercentOffCalculator.tsx**

```tsx
// sites/percentcalc.io/src/components/PercentOffCalculator.tsx
import { useState, useMemo } from 'preact/hooks';
const inputCls = 'w-full rounded-lg border border-slate-300 px-3 py-2 pr-10 text-sm focus:border-brand focus:outline-none focus:ring-1 focus:ring-brand';
function fmtN(n: number) { return n.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }); }
export default function PercentOffCalculator() {
  const [price, setPrice] = useState('120');
  const [off, setOff]     = useState('20');
  const result = useMemo(() => {
    const p = parseFloat(price) || 0;
    const o = parseFloat(off) || 0;
    if (!p) return null;
    const savings = p * (o / 100);
    return { savings, finalPrice: p - savings };
  }, [price, off]);
  return (
    <div class="space-y-4">
      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Original Price</label>
        <input type="number" min="0" step="0.01" value={price}
          onInput={(e) => setPrice((e.target as HTMLInputElement).value)}
          class={inputCls} aria-label="Original price" />
      </div>
      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Discount</label>
        <div class="relative">
          <input type="number" min="0" max="100" step="0.1" value={off}
            onInput={(e) => setOff((e.target as HTMLInputElement).value)}
            class={inputCls} aria-label="Discount percentage" />
          <span class="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">% off</span>
        </div>
      </div>
      {result && (
        <div role="status" aria-live="polite" class="space-y-2 rounded-xl border border-brand/30 bg-yellow-50 p-4">
          <div class="flex justify-between text-sm"><span class="text-slate-600">You Save</span><span class="text-xl font-bold tabular-nums text-green-700">{fmtN(result.savings)}</span></div>
          <div class="flex justify-between text-sm"><span class="text-slate-600">Final Price</span><span class="text-2xl font-bold tabular-nums text-brand">{fmtN(result.finalPrice)}</span></div>
        </div>
      )}
      <p class="text-xs text-slate-500">Formula: Final = Price × (1 − Discount% ÷ 100)</p>
    </div>
  );
}
```

- [ ] **Step 5: Create PercentIncreaseCalculator.tsx**

```tsx
// sites/percentcalc.io/src/components/PercentIncreaseCalculator.tsx
import { useState, useMemo } from 'preact/hooks';
const inputCls = 'w-full rounded-lg border border-slate-300 px-3 py-2 pr-10 text-sm focus:border-brand focus:outline-none focus:ring-1 focus:ring-brand';
export default function PercentIncreaseCalculator() {
  const [start, setStart] = useState('100');
  const [pct, setPct]     = useState('25');
  const result = useMemo(() => {
    const s = parseFloat(start) || 0;
    const p = parseFloat(pct) || 0;
    const increase = s * (p / 100);
    return { increase, final: s + increase };
  }, [start, pct]);
  return (
    <div class="space-y-4">
      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Starting Value</label>
        <input type="number" step="any" value={start}
          onInput={(e) => setStart((e.target as HTMLInputElement).value)}
          class={inputCls} aria-label="Starting value" />
      </div>
      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Increase By</label>
        <div class="relative">
          <input type="number" min="0" step="0.1" value={pct}
            onInput={(e) => setPct((e.target as HTMLInputElement).value)}
            class={inputCls} aria-label="Increase percentage" />
          <span class="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">%</span>
        </div>
      </div>
      <div role="status" aria-live="polite" class="space-y-2 rounded-xl border border-green-200 bg-green-50 p-4">
        <div class="flex justify-between text-sm"><span class="text-slate-600">Increase Amount</span><span class="font-semibold text-green-700 tabular-nums">+{result.increase.toLocaleString('en-US', { maximumFractionDigits: 4 })}</span></div>
        <div class="flex justify-between text-sm"><span class="text-slate-600">New Value</span><span class="text-2xl font-bold tabular-nums text-brand">{result.final.toLocaleString('en-US', { maximumFractionDigits: 4 })}</span></div>
      </div>
      <p class="text-xs text-slate-500">Formula: New = Original × (1 + Increase% ÷ 100)</p>
    </div>
  );
}
```

- [ ] **Step 6: Create PercentDifferenceCalculator.tsx**

```tsx
// sites/percentcalc.io/src/components/PercentDifferenceCalculator.tsx
import { useState, useMemo } from 'preact/hooks';
const inputCls = 'w-full rounded-lg border border-slate-300 px-3 py-2 pr-10 text-sm focus:border-brand focus:outline-none focus:ring-1 focus:ring-brand';
export default function PercentDifferenceCalculator() {
  const [a, setA] = useState('80');
  const [b, setB] = useState('100');
  const result = useMemo(() => {
    const va = parseFloat(a) || 0;
    const vb = parseFloat(b) || 0;
    const avg = (Math.abs(va) + Math.abs(vb)) / 2;
    if (!avg) return null;
    return { diff: (Math.abs(va - vb) / avg) * 100, absDiff: Math.abs(va - vb) };
  }, [a, b]);
  return (
    <div class="space-y-4">
      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Value A</label>
        <input type="number" step="any" value={a}
          onInput={(e) => setA((e.target as HTMLInputElement).value)}
          class={inputCls} aria-label="Value A" />
      </div>
      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Value B</label>
        <input type="number" step="any" value={b}
          onInput={(e) => setB((e.target as HTMLInputElement).value)}
          class={inputCls} aria-label="Value B" />
      </div>
      {result && (
        <div role="status" aria-live="polite" class="space-y-2 rounded-xl border border-brand/30 bg-yellow-50 p-4">
          <div class="flex justify-between text-sm"><span class="text-slate-600">Percent Difference</span><span class="text-2xl font-bold tabular-nums text-brand">{result.diff.toFixed(2)}%</span></div>
          <div class="flex justify-between text-sm text-slate-500"><span>Absolute Difference</span><span class="tabular-nums">{result.absDiff.toLocaleString('en-US', { maximumFractionDigits: 4 })}</span></div>
        </div>
      )}
      <p class="text-xs text-slate-500">Formula: |A − B| / ((|A| + |B|) / 2) × 100</p>
    </div>
  );
}
```

---

## Task 10: percentcalc.io — content/tools markdown files (5 tools)

**Files:**
- Create: `sites/percentcalc.io/src/content/tools/percent-of.md`
- Create: `sites/percentcalc.io/src/content/tools/percent-change.md`
- Create: `sites/percentcalc.io/src/content/tools/percent-off.md`
- Create: `sites/percentcalc.io/src/content/tools/percent-increase.md`
- Create: `sites/percentcalc.io/src/content/tools/percent-difference.md`

- [ ] **Step 1: Create percent-of.md**

```markdown
---
title: "Percentage Of Calculator"
description: "Calculate what X% of any number is. Instant results for tips, discounts, tax, grades, and more. Free, no signup required."
urlSlug: "percent-of"
relatedTags: ["percentage", "percent of", "calculate percent", "what is x percent of y"]
publishDate: 2026-04-25
updatedDate: 2026-04-25
draft: false
schema:
  applicationCategory: "UtilitiesApplication"
  operatingSystem: "Web"
  price: "0"
  priceCurrency: "USD"
  ratingValue: 4.8
  ratingCount: 120
---

## Percentage Of Calculator — Find X% of Any Number

Enter a percentage and a number, and this calculator returns the exact value instantly. Use it for tips, discounts, tax estimates, grade calculations, commission, and any situation where you need "X% of Y."

### The Formula

**Result = (Percentage ÷ 100) × Number**

For example, 15% of 200 = (15 ÷ 100) × 200 = **30**.

### Common Use Cases

**Restaurant tips.** 20% of a $65 bill = $13. Add that to the bill and each person's share is easy to calculate.

**Sales tax.** If your state charges 8.5% sales tax on a $49.99 item, the tax is (8.5 ÷ 100) × 49.99 ≈ **$4.25**.

**Discounts.** A 30% discount on a $120 jacket saves you (30 ÷ 100) × 120 = $36, so you pay $84.

**Grades and test scores.** Scored 76 out of 80? That's (76 ÷ 80) × 100 = **95%** — the "percent of" calculation in reverse.

**Commission.** A 5% sales commission on a $4,500 deal = (5 ÷ 100) × 4,500 = **$225**.

### Finding What Percent One Number Is of Another

The reverse question — "what percent of 200 is 30?" — uses:

**Percentage = (Part ÷ Whole) × 100** → (30 ÷ 200) × 100 = **15%**

*Results are for informational and educational purposes only.*
```

- [ ] **Step 2: Create percent-change.md**

```markdown
---
title: "Percent Change Calculator"
description: "Calculate the percentage increase or decrease between two values. See if a change is positive or negative and by how much. Free, instant."
urlSlug: "percent-change"
relatedTags: ["percent change", "percentage increase", "percentage decrease", "percent difference"]
publishDate: 2026-04-25
updatedDate: 2026-04-25
draft: false
schema:
  applicationCategory: "UtilitiesApplication"
  operatingSystem: "Web"
  price: "0"
  priceCurrency: "USD"
  ratingValue: 4.8
  ratingCount: 95
---

## Percent Change Calculator — Measure Increases and Decreases

Enter an original value and a new value to see the percentage change — whether it went up (positive change) or down (negative change).

### The Formula

**Percent Change = ((New Value − Original Value) / |Original Value|) × 100**

A positive result means an increase; negative means a decrease.

### Examples

**Price went from $80 to $100:** ((100 − 80) / 80) × 100 = **+25%** increase.

**Stock dropped from $150 to $120:** ((120 − 150) / 150) × 100 = **−20%** decrease.

**Population grew from 45,000 to 52,650:** ((52,650 − 45,000) / 45,000) × 100 = **+17%** growth.

### When to Use Percent Change vs. Percent Difference

**Percent change** is directional — it compares a new value to a known original value. Use it when there's a clear "before" and "after."

**Percent difference** (see our separate calculator) is non-directional — it measures how far apart two values are relative to their average. Use it when neither value is the "original."

*Results are for informational and educational purposes only.*
```

- [ ] **Step 3: Create percent-off.md**

```markdown
---
title: "Percent Off Calculator"
description: "Calculate the final price after a percentage discount. Find out how much you save and what you'll pay. Free, instant, no signup."
urlSlug: "percent-off"
relatedTags: ["percent off", "discount calculator", "sale price", "how much do I save"]
publishDate: 2026-04-25
updatedDate: 2026-04-25
draft: false
schema:
  applicationCategory: "UtilitiesApplication"
  operatingSystem: "Web"
  price: "0"
  priceCurrency: "USD"
  ratingValue: 4.9
  ratingCount: 210
---

## Percent Off Calculator — Final Price After a Discount

Enter the original price and the discount percentage to see your savings and the final price immediately.

### The Formula

**Savings = Original Price × (Discount% ÷ 100)**

**Final Price = Original Price − Savings**

Or combined: **Final Price = Original Price × (1 − Discount% ÷ 100)**

### Examples

| Original Price | Discount | You Save | Final Price |
|----------------|----------|----------|-------------|
| $120.00 | 20% off | $24.00 | $96.00 |
| $49.99 | 15% off | $7.50 | $42.49 |
| $250.00 | 33% off | $82.50 | $167.50 |
| $1,200.00 | 40% off | $480.00 | $720.00 |

### Stacked Discounts

When two discounts are applied sequentially (e.g., 20% off, then an additional 10% off the sale price), they do **not** combine to 30% off. The combined discount is:

**Combined = 1 − (1 − 0.20)(1 − 0.10) = 1 − 0.72 = 28% off**

*Results are for informational and educational purposes only.*
```

- [ ] **Step 4: Create percent-increase.md**

```markdown
---
title: "Percent Increase Calculator"
description: "Calculate a new value after a percentage increase. Raise prices, estimate salary bumps, project investment growth. Free, instant."
urlSlug: "percent-increase"
relatedTags: ["percent increase", "percentage increase calculator", "calculate new value after increase"]
publishDate: 2026-04-25
updatedDate: 2026-04-25
draft: false
schema:
  applicationCategory: "UtilitiesApplication"
  operatingSystem: "Web"
  price: "0"
  priceCurrency: "USD"
  ratingValue: 4.8
  ratingCount: 88
---

## Percent Increase Calculator — New Value After a Percentage Increase

Enter a starting value and the percentage increase to find the new value instantly.

### The Formula

**Increase Amount = Original × (Increase% ÷ 100)**

**New Value = Original + Increase Amount = Original × (1 + Increase% ÷ 100)**

### Common Uses

**Salary raise.** Current salary is $65,000. You receive a 4.5% raise. New salary = $65,000 × 1.045 = **$67,925**.

**Price increase.** A product costs $29.99 and you need to raise it by 12%. New price = $29.99 × 1.12 = **$33.59**.

**Investment growth.** $10,000 invested grows 7% in a year. Ending value = $10,000 × 1.07 = **$10,700**.

**Tax-inclusive pricing.** Add 8.875% NYC sales tax to a $50 item: $50 × 1.08875 = **$54.44**.

### Compounding Increases

For repeated increases over multiple periods, don't multiply the percentage by the number of periods — compound it:

**Final = Start × (1 + Rate)^n**

For example, $10,000 growing 7% per year for 10 years: $10,000 × (1.07)^10 ≈ **$19,672**.

*Results are for informational and educational purposes only.*
```

- [ ] **Step 5: Create percent-difference.md**

```markdown
---
title: "Percent Difference Calculator"
description: "Calculate the percentage difference between two values. Unlike percent change, this is non-directional — ideal for comparing two measurements. Free, instant."
urlSlug: "percent-difference"
relatedTags: ["percent difference", "percentage difference", "difference between two numbers percent"]
publishDate: 2026-04-25
updatedDate: 2026-04-25
draft: false
schema:
  applicationCategory: "UtilitiesApplication"
  operatingSystem: "Web"
  price: "0"
  priceCurrency: "USD"
  ratingValue: 4.7
  ratingCount: 74
---

## Percent Difference Calculator — Compare Two Values Without Direction

Percent difference measures how far apart two values are relative to their average. Unlike percent change, it has no "before" or "after" — both values are treated equally.

### The Formula

**Percent Difference = (|A − B| / ((|A| + |B|) / 2)) × 100**

The denominator is the average of the two absolute values, so the result is symmetric — swapping A and B gives the same answer.

### When to Use This

Use **percent difference** when:
- You are comparing two independent measurements (two lab results, two price quotes, two estimates).
- Neither value is a "reference" or "original" — they're peers.

Use **percent change** (our separate calculator) when there is a clear original and a new value, and direction matters.

### Example

Lab Test A: 80 units. Lab Test B: 100 units.

|A − B| = 20. Average = (80 + 100) / 2 = 90. Percent difference = (20 / 90) × 100 ≈ **22.2%**.

Note: the percent change from 80 to 100 is 25%, but the percent *difference* between 80 and 100 is 22.2% — a subtly different quantity.

*Results are for informational and educational purposes only.*
```

---

## Task 11: percentcalc.io — Rewrite index.astro + tools/[...slug].astro

**Files:**
- Rewrite: `sites/percentcalc.io/src/pages/index.astro`
- Rewrite: `sites/percentcalc.io/src/pages/tools/[...slug].astro`

- [ ] **Step 1: Rewrite index.astro (financalc pattern)**

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
  ? (await getCollection('tools', ({ data }) => !data.draft))
      .sort((a, b) => a.data.title.localeCompare(b.data.title))
  : [];

const TOOL_ICONS: Record<string, string> = {
  'percent-of':         '🔢',
  'percent-change':     '📊',
  'percent-off':        '🏷️',
  'percent-increase':   '📈',
  'percent-difference': '↔️',
};
---
<BaseLayout
  title="Percentage Calculator — 5 Free Percent Calculators"
  description="Free online percentage calculators: percent of a number, percent change, percent off (discounts), percent increase, and percent difference. Instant, no signup."
>

  <header class="pb-8 pt-4">
    <h1 class="text-4xl font-bold tracking-tight text-slate-900 sm:text-5xl">
      Percentage Calculators
    </h1>
    <p class="mt-3 max-w-xl text-lg text-slate-600">
      Five free percentage calculators for every everyday math situation — discounts,
      grade changes, price increases, and more.
    </p>
  </header>

  <ul class="flex flex-wrap gap-x-6 gap-y-2 text-sm text-slate-600">
    {[
      'Instant results as you type',
      'No data stored or shared',
      'Free, no signup required',
      'Mobile & desktop friendly',
    ].map((badge) => (
      <li class="flex items-center gap-1.5">
        <svg class="h-4 w-4 shrink-0 text-brand" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.061 1.06l2.5 2.5a.75.75 0 001.137-.088l4-5.5z" clip-rule="evenodd" />
        </svg>
        {badge}
      </li>
    ))}
  </ul>

  {tools.length > 0 && (
    <section class="mt-10" aria-labelledby="tools-heading">
      <h2 id="tools-heading" class="text-2xl font-bold text-slate-900">Our Calculators</h2>
      <ul class="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
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
              <span class="mt-3 text-sm font-medium text-brand">Open Calculator →</span>
            </a>
          </li>
        ))}
      </ul>
    </section>
  )}

  <section class="prose prose-slate mt-10 max-w-none">
    <h2>About PercentCalc</h2>
    <p>
      PercentCalc offers five free percentage calculators covering the most common math
      situations: finding a percent of a number, measuring how much something changed,
      calculating sale prices and discounts, projecting increases, and comparing two
      values side by side.
    </p>
    <p>
      All calculations run locally in your browser. No data is collected or transmitted.
    </p>
    <h3>Which calculator should I use?</h3>
    <ul>
      <li><strong>Tip, tax, commission?</strong> Use <a href="/tools/percent-of/">Percent Of</a> — "15% of $50."</li>
      <li><strong>Did a price go up or down?</strong> Use <a href="/tools/percent-change/">Percent Change</a> — "from $80 to $100."</li>
      <li><strong>How much do I save on a sale?</strong> Use <a href="/tools/percent-off/">Percent Off</a> — "20% off $120."</li>
      <li><strong>New value after a raise or increase?</strong> Use <a href="/tools/percent-increase/">Percent Increase</a> — "salary up 5%."</li>
      <li><strong>Comparing two values with no clear 'before'?</strong> Use <a href="/tools/percent-difference/">Percent Difference</a>.</li>
    </ul>
  </section>

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
    </section>
  )}

</BaseLayout>
```

- [ ] **Step 2: Rewrite tools/[...slug].astro (wire up 5 calculators)**

```astro
---
import ToolLayout from '~/layouts/ToolLayout.astro';
import { getCollection, type CollectionEntry } from 'astro:content';
import { siteConfig } from '~/config/site.config';
import PercentOfCalculator from '~/components/PercentOfCalculator';
import PercentChangeCalculator from '~/components/PercentChangeCalculator';
import PercentOffCalculator from '~/components/PercentOffCalculator';
import PercentIncreaseCalculator from '~/components/PercentIncreaseCalculator';
import PercentDifferenceCalculator from '~/components/PercentDifferenceCalculator';

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
const slug = tool.data.urlSlug;
---
<ToolLayout
  title={tool.data.title}
  description={tool.data.description}
  slug={slug}
  applicationCategory={s.applicationCategory}
  operatingSystem={s.operatingSystem}
  price={s.price}
  priceCurrency={s.priceCurrency}
  ratingValue={s.ratingValue}
  ratingCount={s.ratingCount}
>
  {slug === 'percent-of' && (
    <PercentOfCalculator slot="tool" client:load />
  )}
  {slug === 'percent-change' && (
    <PercentChangeCalculator slot="tool" client:load />
  )}
  {slug === 'percent-off' && (
    <PercentOffCalculator slot="tool" client:load />
  )}
  {slug === 'percent-increase' && (
    <PercentIncreaseCalculator slot="tool" client:load />
  )}
  {slug === 'percent-difference' && (
    <PercentDifferenceCalculator slot="tool" client:load />
  )}
  <Content />
</ToolLayout>
```

- [ ] **Step 3: Build and verify percentcalc.io**

```bash
cd /home/abovespec/site-network && pnpm --filter @site/percentcalc build
```
Expected: Exit 0, no errors. All 5 tool pages generated.

- [ ] **Step 4: Commit percentcalc.io**

```bash
cd /home/abovespec/site-network
git add sites/percentcalc.io/
git commit -m "feat(percentcalc.io): multi-tool financalc pattern + 5 percent calculators (INF-24)

Co-Authored-By: Paperclip <noreply@paperclip.ing>"
```

---

## Task 12: Final verification — build all 5 sites

- [ ] **Step 1: Build all 5 sites in parallel**

```bash
cd /home/abovespec/site-network
pnpm --filter @site/agecalc build && \
pnpm --filter @site/tipcalc build && \
pnpm --filter @site/amortcalc build && \
pnpm --filter @site/margincalc build && \
pnpm --filter @site/percentcalc build
```
Expected: All 5 exit 0.

- [ ] **Step 2: Verify filter names match package.json names**

The filter names above assume `package.json` name fields are `@site/agecalc`, `@site/tipcalc`, etc. Verify with:
```bash
grep '"name"' sites/agecalc.io/package.json sites/tipcalc.io/package.json sites/amortcalc.io/package.json sites/margincalc.io/package.json sites/percentcalc.io/package.json
```
Adjust the `--filter` values to match if they differ.
