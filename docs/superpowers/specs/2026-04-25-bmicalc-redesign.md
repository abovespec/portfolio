# bmicalc.io Redesign Spec — INF-14

**Date:** 2026-04-25  
**Issue:** [INF-14](/INF/issues/INF-14)  
**Agent:** Athena (UI/UX)

---

## Goal

Redesign bmicalc.io as the pilot site for INF-13 (30-site UX overhaul). The result
must look like a 2026 production site, pass `pnpm --filter bmicalc.io build`, and
generalize to the other calculator sites in the network.

---

## Constraints & Context

- Astro 5 + Preact + Tailwind v4 monorepo
- Existing `BaseLayout` constrains `<main>` to `max-w-5xl` (64 rem) with `px-4`
- Green theme: `--site-theme-color: #15803d`, `--site-accent-color: #4ade80`
- Custom prose styles in `global.css` (no @tailwindcss/typography)
- Tailwind v4 tokens: `bg-brand` = `#15803d`, `bg-accent` = `#4ade80`
- YMYL site — health content legitimacy is required

---

## Approach Chosen

Three approaches were considered:

**A. Full-width hero + sticky calculator sidebar (Chosen)**  
Two-column layout on desktop: left = copy + trust signals + SEO content, right = sticky
calculator card. On mobile: stacked (heading → calculator → SEO content). The sticky
calculator stays visible while the user reads educational content below.

**B. Calculator-first hero (full width, copy below)**  
Calculator spans full width above fold, copy below. Simpler but less authoritative —
health sites need more than just a tool.

**C. Card-based dashboard layout**  
Multiple BMI-related cards on the homepage (calculator, BMI table, quick facts).
Too complex for an MVP; generalizes poorly to other calculator sites.

**Chosen: A** — sticky two-column delivers the best balance of calculator prominence
(always above the fold, always reachable) and editorial authority (educational copy
visible alongside the tool). It generalizes well to other calculator sites.

---

## Components to Build / Modify

### 1. `BmiCalculator.tsx` (new — Preact island)

Interactive BMI calculator, hydrated `client:load`.

**Inputs:**
- Unit toggle: Imperial | Metric (pill tabs)
- Imperial: Height ft + in (two inputs) + Weight lbs
- Metric: Height cm + Weight kg

**Behavior:** Auto-calculates on every keystroke (no button). Shows result when both
height and weight are non-zero.

**Result display:**
- Large BMI number (1 decimal, e.g. "24.5")
- Category badge (color-coded): Underweight · Normal weight · Overweight · Obese
- Visual gauge: horizontal gradient bar (blue → green → orange → red) with a marker
  dot positioned at the user's BMI (15–40 scale, clamped)
- Category range label

**Category thresholds (WHO):**
| Category | Range | Color |
|---|---|---|
| Underweight | < 18.5 | `#3b82f6` (blue) |
| Normal weight | 18.5 – 24.9 | `#15803d` (green/brand) |
| Overweight | 25 – 29.9 | `#f97316` (orange) |
| Obese | ≥ 30 | `#ef4444` (red) |

**Footer:** One-line disclaimer: "For informational purposes only. Consult a healthcare
professional for medical advice."

**Accessibility:** All inputs have `aria-label`. Result region has `role="status"`
so screen readers announce updates. Unit toggle buttons are `type="button"`.

---

### 2. `index.astro` (redesign)

**Structure:**

```
<BaseLayout>
  <!-- Page header: full copy line, clean -->
  <header class="pt-4 pb-8">
    <h1>BMI Calculator</h1>
    <p>subtitle</p>
  </header>

  <!-- Main grid: copy left, calculator right (sticky) -->
  <div class="grid md:grid-cols-[1fr_420px] gap-8 items-start">
    <!-- Left: trust signals + disclaimer + SEO content -->
    <div>
      <ul>trust badges</ul>
      <aside>YMYL disclaimer</aside>
      <!-- SEO sections: What is BMI, Categories table, Limitations -->
    </div>
    <!-- Right: sticky calculator -->
    <div class="md:sticky md:top-8">
      <div class="calculator card">
        <BmiCalculator client:load />
      </div>
    </div>
  </div>

  <!-- YMYL footer: reviewed-by slot + sources -->
  <footer class="mt-16 border-t pt-8">
    <!-- reviewed-by slot (empty until Calliope fills) -->
    <!-- sources list -->
  </footer>
</BaseLayout>
```

**YMYL legitimacy elements (on homepage):**
- Amber disclaimer box immediately below the trust badges: "BMI is a screening tool,
  not a diagnostic measure. Results are for general informational purposes only.
  Always consult a qualified healthcare professional."
- `reviewedBy` slot in page footer (empty initially, comment indicates Calliope fills)
- `lastReviewed` date in the footer (static, set to 2026-04-25)
- Sources section with 3 citations: WHO, CDC, NHLBI

**SEO content sections (below the grid):**
1. BMI Categories (table with 6 rows, WHO classification)
2. What is BMI?
3. How is BMI Calculated?
4. BMI Limitations (important for YMYL)
5. When to See a Doctor

---

### 3. `PostLayout.astro` (extend with YMYL fields)

New props (all optional):
```ts
reviewedBy?: string
lastReviewedAt?: Date | string
sources?: Array<{ text: string; url?: string }>
```

**Rendered additions:**
- After author/date meta line: green "Medically reviewed by" pill (only when
  `reviewedBy` is set)
- After article content: "Sources" section with numbered citation list (only when
  `sources.length > 0`)

---

### 4. `src/content/config.ts` (extend blog schema)

Add to the `blog` collection:
```ts
reviewedBy: z.string().optional(),
lastReviewedAt: z.coerce.date().optional(),
sources: z.array(z.object({ text: z.string(), url: z.string().optional() })).default([]),
```

---

### 5. `src/pages/blog/index.astro` (redesign)

Replace the dark `bg-slate-800` card style with clean white cards matching the
site's green palette:
- White card, border-slate-200, hover:border-green-300
- Date displayed prominently (small, muted, uppercase)
- Tags as small green pills
- Descriptive subtitle (line-clamp-2)
- Page heading: "Health & BMI Articles" with a subtitle

---

### 6. `site.config.ts` (enable features)

- `hasBlog: true`
- Add `{ label: 'Blog', href: '/blog/' }` to `nav.primary`
- Update `description` to "Free BMI calculator with instant results. Medically reviewed
  BMI information for adults."

---

## Responsiveness Requirements

| Breakpoint | Calculator layout |
|---|---|
| 375px (mobile) | Single column: h1 → calculator card → SEO content |
| 768px (md) | Two-column grid activated |
| 1280px (desktop) | Two-column, calculator sticky at `top: 2rem` |

The sticky calculator must not overflow the viewport height. Max height:
`max-h-[calc(100vh-4rem)]` with `overflow-y: auto` on the card if needed.

---

## Non-Goals (this ticket)

- Creating actual blog articles (Calliope's task)
- Hero images (Hephaestus's task — leave `<img>` slot empty)
- About page rewrite (separate task)
- Privacy/Terms customization (separate task)

---

## Spec Self-Review

- No placeholder TBDs left
- Architecture matches feature descriptions
- YMYL legitimacy is addressed at both homepage and PostLayout level
- Scope is contained to 6 files, implementable in one session
- All requirements from INF-14 covered: calculator above fold ✓, /blog templates ✓,
  YMYL treatment ✓, mobile/desktop pass ✓, build must pass ✓
