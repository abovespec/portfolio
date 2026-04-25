# financalc.io Redesign Spec
*INF-19 — Multi-tool + YMYL-financial pilot*
*Date: 2026-04-25*

## Goal

Redesign financalc.io as a **multi-tool financial calculator site** with YMYL-financial legitimacy signals, following the patterns established in bmicalc.io (INF-14). This site validates the multi-tool + YMYL-financial patterns before we fan out to the full 30-site network.

---

## Architecture

### Site config changes
- Enable `hasTool: true` and `hasBlog: true` in `site.config.ts`
- Add `{ label: 'Tools', href: '/tools/' }` and `{ label: 'Blog', href: '/blog/' }` to nav

### Page structure
| Page | Purpose |
|------|---------|
| `/` | Tool directory: hero + trust signals + tool cards grid + SEO intro + YMYL disclaimer |
| `/tools/` | Alias redirect to `/` (or same content) |
| `/tools/loan-calculator/` | Loan calculator above fold + SEO content below |
| `/tools/compound-interest-calculator/` | Compound interest + SEO content |
| `/tools/roi-calculator/` | ROI calculator + SEO content |
| `/tools/savings-goal-calculator/` | Savings goal + SEO content |
| `/blog/` | Blog listing (Calliope will populate) |
| `/blog/[slug]/` | Article with YMYL financial chrome |

---

## Index Page (`/`) — Tool Directory

```
┌──────────────────────────────────────────────────────┐
│  Hero: "Free Financial Calculators"                  │
│  Subtitle + 4 trust signal badges                   │
├──────────────────────────────────────────────────────┤
│  Tool cards grid (2-col mobile → 4-col desktop)      │
│  [Loan] [Compound Interest] [ROI] [Savings Goal]     │
├──────────────────────────────────────────────────────┤
│  YMYL disclaimer (amber box)                        │
│  SEO intro prose: "What is FinanceCalc?" 2–3 ¶      │
│  Recent blog articles (3-col, shown when hasBlog)   │
└──────────────────────────────────────────────────────┘
```

Each tool card: icon + title + 1-line description + "Open Calculator →" link to `/tools/[slug]/`.

---

## Per-Tool Page (`/tools/[slug]/`) — Two-Column Layout

Matches bmicalc.io's sticky-right pattern:

```
┌──────────────────────────────┬────────────────────┐
│  LEFT (scrolls)              │  RIGHT (sticky)    │
│  Breadcrumb                  │  Calculator card   │
│  h1 title                    │  (400px, top-8)    │
│  YMYL disclaimer (amber)     │                    │
│  What Is This? (prose)       │                    │
│  How to Use (prose)          │                    │
│  Formula (prose)             │                    │
│  FAQ                         │                    │
│  Related tools               │                    │
├──────────────────────────────────────────────────┤
│  Sources footer (if any)                          │
└──────────────────────────────────────────────────┘
```

Grid: `md:grid-cols-[1fr_400px]` — identical to bmicalc pattern.

---

## YMYL-Financial Chrome

### Amber disclaimer (on all calculator pages + index)
> **Important:** Results are estimates for informational purposes only. This calculator does not constitute financial advice. Consult a licensed financial advisor before making investment or borrowing decisions.

### Reviewed-by badge (ToolLayout + PostLayout)
- Empty slot (`reviewedBy` prop optional) — leave placeholder text "Content reviewed for accuracy" until Calliope sources a reviewer
- When populated: green badge with checkmark + "Reviewed by [name]" + last-reviewed date

### Sources footer
- Numbered list at bottom of per-tool pages and blog articles
- Only shown when `sources.length > 0`

### Financial disclaimer tag (PostLayout)
- "Not financial advice" note below article metadata

---

## New Preact Calculator Components

All four follow the BmiCalculator pattern: `useState` + `useMemo`, live results, color-coded output, inline disclaimer.

### LoanCalculator.tsx
Inputs: Loan Amount ($), Interest Rate (%/yr), Term (years)
Outputs: Monthly Payment, Total Paid, Total Interest, amortization summary bar

### CompoundInterestCalculator.tsx
Inputs: Principal ($), Annual Rate (%), Years, Compounds/Year (select: 1/2/4/12/365)
Outputs: Final Amount, Interest Earned, growth bar (principal vs interest proportion)

### ROICalculator.tsx
Inputs: Initial Investment ($), Final Value ($), optional Time Period (years) for annualized
Outputs: ROI %, Net Profit, Annualized Return (if years provided)

### SavingsGoalCalculator.tsx
Inputs: Goal Amount ($), Initial Deposit ($), Monthly Contribution ($), Annual Rate (%)
Outputs: Months to reach goal, Years, Total Contributed, Total Interest Earned

---

## ToolLayout.astro — Updated Props

```typescript
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
```

Renders: two-column grid, breadcrumb, h1, YMYL amber disclaimer, `<slot name="tool" />` in right sticky card, prose content in left column, FAQ slot, reviewed-by badge, sources footer.

---

## PostLayout.astro — YMYL Fields Added

Add to existing interface:
```typescript
reviewedBy?: string;
lastReviewedAt?: Date | string;
sources?: Array<{ text: string; url?: string }>;
```

Renders reviewed-by badge below article metadata + sources footer at article end. Matches bmicalc.io PostLayout pattern exactly, adapted with "financial advice" language.

---

## Content Collection Updates

### `src/content/config.ts` — blog schema additions
```typescript
reviewedBy: z.string().optional(),
lastReviewedAt: z.coerce.date().optional(),
sources: z.array(z.object({ text: z.string(), url: z.string().optional() })).default([]),
```

Tools schema already has the right shape; no changes needed.

---

## Tool Content Files (MDX)

Four files: `src/content/tools/loan-calculator.md`, `compound-interest-calculator.md`, `roi-calculator.md`, `savings-goal-calculator.md`

Each includes: frontmatter (title, description, urlSlug, publishDate), placeholder SEO prose (What Is This, How to Use, Formula, When to Use), and a stub FAQ. Calliope will expand the prose.

---

## Color / Branding

Keep existing purple brand (#312e81, accent #4f46e5) from `site.config.ts`. Indigo/purple is appropriate for financial/professional tools. No changes to global.css or theme tokens.

---

## Routing / Feature Flags

- `/tools/index.astro` currently redirects to `/` when `hasTool: false`. After enabling `hasTool: true`, it renders the tool listing.
- `/tools/[...slug].astro` uses `getStaticPaths` gated by `hasTool` — already works when flag is on.
- The per-tool page needs the Preact component slot wired up per tool slug.

---

## Out of Scope (This Heartbeat)

- Blog article content — Calliope owns this
- Hero images — Hephaestus queue
- Mortgage calculator — follow-up after Calliope's keyword research
- Percentage / compound frequency advanced modes
